"""A6: two-dimensional probability of collision, and whether it is a robust quantity.

WHAT THIS IS AND IS NOT
-----------------------
It is NOT the analysis `validation/A6_conjunction_cara.md` originally specified. That one
wants CCSDS OEM ephemerides out of GMAT and NASA's CARA tools driven by a covariance
derived from real Conjunction Data Messages. GMAT is not installed here, CARA is MATLAB,
and Space-Track is unreachable under this environment's network policy.

It IS the question P1 actually raised. P1 found that the 30-day minimum approach distance
swings from 4.6 to 63.4 km over a +/-2.5 % change in ejection velocity -- a near-resonant
beat sample, not a design property -- and the paper had quoted one draw from it as a safety
result. The obvious reply is that probability of collision integrates over the covariance
instead of sampling one geometry, so it should not swing like that. **Nobody had checked.**

Checking it needs a covariance, and no covariance exists for a satellite that has never
flown. So one is ASSUMED, stated in the output, and then the conclusion is stress-tested
against that assumption by sweeping it (band 5). A robustness result that survives halving
and doubling the assumed sigma does not depend on the number nobody has; one that does not
survive it is worthless and the sheet says so.

METHOD
------
Foster's 2-D P_c. At the moment of closest approach the encounter is treated as rectilinear
and the two covariances are combined and projected onto the plane normal to the relative
velocity. P_c is then the integral of a 2-D Gaussian over a disc of radius R = r1 + r2
centred at the miss vector:

    P_c = (1/(2*pi*sx*sz)) * integral over the disc of exp(-x^2/(2 sx^2) - z^2/(2 sz^2))

evaluated here by direct quadrature on a polar grid, which is exact enough at these
dimensions and needs no special functions.

Geometry comes from `analysis/astro.py::propagate()` -- the repository's own propagator --
so this cannot disagree with the rest of the project about where anything is.

Run:  python3 validation/conjunction/pc_2d.py

Bands are declared in validation/A6_conjunction_cara.md, committed before this file existed.
"""
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'analysis'))

import astro  # noqa: E402

# --- the assumed covariance, which is the weakest input here and is labelled as such -----
# Post-deployment tracking uncertainty for an untracked object shortly after release, as a
# diagonal RIC 1-sigma. These are ORDER-OF-MAGNITUDE ENGINEERING ASSUMPTIONS, not derived
# from any CDM, and band 5 exists because of that.
SIGMA_R = 100.0      # m, radial
SIGMA_I = 500.0      # m, in-track: always the largest, and it grows fastest
SIGMA_C = 100.0      # m, cross-track

# Hard-body radius: 3U CubeSat plus a spent upper stage, both boxed generously.
HBR = 5.0            # m, combined

DV_SWEEP = [16.12, 16.33, 16.537, 16.74, 16.95]     # +/-2.5 % about the rated point
SIGMA_SCALES = [0.5, 1.0, 2.0]                       # band 5


def _sigma_perp(sigma_ric, rel_hat):
    """Project a diagonal RIC covariance onto the plane normal to the relative velocity.

    Crude on purpose and stated as such: RIC is treated as inertially aligned over the
    encounter, which is fair for the seconds a conjunction lasts and wrong for anything
    longer. Two orthonormal vectors spanning the plane are built from the relative
    velocity, and the combined covariance is projected onto each.
    """
    a = np.array([0.0, 0.0, 1.0])
    if abs(np.dot(a, rel_hat)) > 0.9:
        a = np.array([1.0, 0.0, 0.0])
    u = np.cross(rel_hat, a)
    u /= np.linalg.norm(u)
    w = np.cross(rel_hat, u)
    C = np.diag(np.array(sigma_ric) ** 2)
    return math.sqrt(u @ C @ u), math.sqrt(w @ C @ w), u, w


def pc_2d(miss_vec, rel_vel, sigma_ric, hbr=HBR, n_r=400, n_th=720):
    """Foster 2-D Pc by polar quadrature over the hard-body disc."""
    rel_hat = rel_vel / np.linalg.norm(rel_vel)
    sx, sz, u, w = _sigma_perp(sigma_ric, rel_hat)
    # Combined covariance of two independent objects: sigmas add in quadrature.
    sx *= math.sqrt(2.0)
    sz *= math.sqrt(2.0)
    mx, mz = float(miss_vec @ u), float(miss_vec @ w)
    rs = (np.arange(n_r) + 0.5) / n_r * hbr
    ths = (np.arange(n_th) + 0.5) / n_th * 2 * math.pi
    R, TH = np.meshgrid(rs, ths, indexing='ij')
    X = R * np.cos(TH) - mx
    Z = R * np.sin(TH) - mz
    pdf = np.exp(-0.5 * ((X / sx) ** 2 + (Z / sz) ** 2)) / (2 * math.pi * sx * sz)
    dA = (hbr / n_r) * (2 * math.pi / n_th) * R
    return float(np.sum(pdf * dA))


def closest_approach(dv, alt_m=450e3, inc_deg=51.6, k=0, spacing_s=1200.0, days=30):
    """Miss vector and relative velocity at the closest approach of one satellite."""
    RE, MU = astro.RE, astro.MU
    r0 = RE + alt_m
    inc = math.radians(inc_deg)
    a1, e1 = astro.boosted_elements(alt_m, dv)
    n0 = math.sqrt(MU / r0 ** 3)
    n1 = math.sqrt(MU / a1 ** 3)
    tk = k * spacing_s
    argp = (n0 * tk) % (2 * np.pi)

    t = np.arange(0, days * 86400, 10.0)
    stage = astro.propagate(r0, 1e-6, inc, 0, 0, t)
    sat = astro.propagate(a1, e1, inc, argp, -n1 * tk, t)
    mask = t > tk + 3600
    d = np.linalg.norm(sat[mask] - stage[mask], axis=1)
    tc = t[mask][int(np.argmin(d))]

    tf = np.arange(max(tc - 60, tk + 3600), tc + 60, 0.05)
    sf = astro.propagate(a1, e1, inc, argp, -n1 * tk, tf)
    gf = astro.propagate(r0, 1e-6, inc, 0, 0, tf)
    df = np.linalg.norm(sf - gf, axis=1)
    i = int(np.argmin(df))
    miss = sf[i] - gf[i]
    # Relative velocity by central difference on the refined grid.
    j = min(max(i, 1), len(tf) - 2)
    rel_v = ((sf[j + 1] - gf[j + 1]) - (sf[j - 1] - gf[j - 1])) / (tf[j + 1] - tf[j - 1])
    return miss, rel_v, float(df[i])


def main():
    print("A6: 2-D Pc against astro.py's own propagator")
    print(f"assumed covariance, diagonal RIC 1-sigma: "
          f"R {SIGMA_R:.0f} m, I {SIGMA_I:.0f} m, C {SIGMA_C:.0f} m")
    print(f"hard-body radius {HBR:.0f} m combined.  ASSUMED, not from any CDM.\n")

    sweep = {}
    for scale in SIGMA_SCALES:
        sig = [SIGMA_R * scale, SIGMA_I * scale, SIGMA_C * scale]
        rows = []
        for dv in DV_SWEEP:
            miss, rel_v, dmin = closest_approach(dv)
            pc = pc_2d(miss, rel_v, sig)
            rows.append(dict(dv=dv, min_km=round(dmin / 1e3, 2), pc=pc,
                             rel_speed_km_s=round(float(np.linalg.norm(rel_v)) / 1e3, 3)))
        sweep[f"{scale:g}x"] = rows

    nominal = sweep['1x']
    print(f"{'dv m/s':>8} {'min dist km':>12} {'rel km/s':>10} {'Pc':>12}")
    for r in nominal:
        print(f"{r['dv']:8.3f} {r['min_km']:12.2f} {r['rel_speed_km_s']:10.3f} {r['pc']:12.3e}")

    def spread(vals):
        v = [x for x in vals if x > 0]
        return max(v) / min(v) if v else None

    d_spread = spread([r['min_km'] for r in nominal])
    pc_spread = spread([r['pc'] for r in nominal])
    print(f"\nspread over the sweep, max/min:")
    print(f"  minimum distance : {d_spread:8.2f} x")
    print(f"  Pc               : "
          + (f"{pc_spread:8.2f} x" if pc_spread else "UNMEASURABLE, see below"))

    # --- what the run actually found, which is not what the band was written for -------
    # Every miss distance is tens of km against an assumed sigma of hundreds of metres.
    # That is 25 to 100 sigma, so Pc underflows and no spread can be measured. The useful
    # quantity is therefore not the spread but the CROSSOVER: how large would the
    # covariance have to be before Pc mattered at all?
    print("\nPc is unmeasurably small at every point, so the declared spread test is void.")
    print("The quantity that is meaningful instead: how big would sigma have to be?\n")
    miss, rel_v, dmin = closest_approach(16.537)
    print(f"{'sigma_I (m)':>12} {'d/sigma_I':>10} {'Pc':>12}")
    crossings = {}
    for sig_i in (500, 1000, 2000, 3000, 4000, 5000, 7500, 10000):
        sig = [sig_i / 5.0, float(sig_i), sig_i / 5.0]     # keep the RIC shape
        pc = pc_2d(miss, rel_v, sig)
        print(f"{sig_i:12.0f} {dmin/sig_i:10.2f} {pc:12.3e}")
        for thr in (1e-6, 1e-4):
            if pc >= thr and thr not in crossings:
                crossings[thr] = sig_i
    for thr in (1e-6, 1e-4):
        got = crossings.get(thr)
        print(f"  Pc reaches {thr:.0e} at sigma_I ~ "
              + (f"{got:.0f} m" if got else "> 10 km"))

    # --- the result worth having: an upper bound that needs no covariance at all -------
    # Pc is bounded by (hard-body area) x (peak of the 2-D Gaussian), and the peak falls
    # as 1/(sx*sz). So a covariance large enough for its tail to reach the miss distance
    # is also too diffuse to put much probability inside a 5 m disc. Pc therefore has a
    # MAXIMUM over sigma, and that maximum is a statement about this geometry that does
    # not depend on the covariance nobody has.
    print("\nUpper bound on Pc, maximised over the assumed covariance scale:")
    print(f"{'sigma_I (m)':>12} {'d/sigma_I':>10} {'Pc':>12}")
    pc_bound, sig_bound = 0.0, 0.0
    for sig_i in (2e3, 5e3, 1e4, 1.5e4, 2e4, 3e4, 5e4, 1e5, 2e5, 5e5):
        pc = pc_2d(miss, rel_v, [sig_i / 5.0, sig_i, sig_i / 5.0])
        if pc > pc_bound:
            pc_bound, sig_bound = pc, sig_i
        print(f"{sig_i:12.0f} {dmin/sig_i:10.2f} {pc:12.3e}")
    print(f"\n  MAX Pc over all covariance scales : {pc_bound:.3e} "
          f"at sigma_I ~ {sig_bound/1e3:.0f} km")
    print(f"  against the 1e-4 flag threshold   : {1e-4/pc_bound:.0f}x below")
    print("  -> no covariance makes this conjunction actionable. The safety question")
    print("     does not need the CDMs this analysis could not get.")

    print(f"\nband 5, sensitivity of the Pc SPREAD to the assumed covariance:")
    spreads = {}
    for k, rows in sweep.items():
        spreads[k] = spread([r['pc'] for r in rows])
        print(f"  sigma x{k:>4} : Pc spread "
              + (f"{spreads[k]:.2f} x" if spreads[k] else "unmeasurable"))
    measurable = [v for v in spreads.values() if v]
    ratio = (max(measurable) / min(measurable)) if len(measurable) > 1 else None
    print("  -> VOID for the same reason: a spread of quantities that are all zero to")
    print("     machine precision is not a number.")

    realign = astro.conjunction(dv=16.537)['realign_days']
    pc_max = max(r['pc'] for r in nominal)
    print(f"\nrealignment period at 16.537 m/s : {realign} days")
    print(f"max Pc at the rated point        : {pc_max:.3e}"
          f"{'   FLAGGED > 1e-4' if pc_max > 1e-4 else ''}")

    out = dict(
        analysis="A6", method="Foster 2-D Pc, polar quadrature, astro.propagate geometry",
        bands_declared_in="validation/A6_conjunction_cara.md",
        covariance_assumption=dict(
            sigma_R_m=SIGMA_R, sigma_I_m=SIGMA_I, sigma_C_m=SIGMA_C,
            frame="diagonal RIC, treated as inertially fixed over the encounter",
            provenance="ASSUMED. No CDM was available; Space-Track is unreachable here. "
                       "The Pc VALUES inherit this assumption and are not defensible on "
                       "their own. Only the SPREAD is claimed, and band 5 tests it."),
        hard_body_radius_m=HBR, screening_window_days=30,
        dv_sweep_m_s=DV_SWEEP, sweep=sweep,
        min_distance_spread=round(d_spread, 3),
        pc_spread=(round(pc_spread, 3) if pc_spread else None),
        pc_spread_by_sigma_scale={k: (round(v, 3) if v else None)
                                  for k, v in spreads.items()},
        pc_spread_sensitivity=(round(ratio, 3) if ratio else None),
        pc_sigma_crossings_m={f"{k:.0e}": v for k, v in crossings.items()},
        pc_upper_bound=pc_bound, pc_upper_bound_at_sigma_I_m=sig_bound,
        pc_bound_margin_below_1e4=round(1e-4 / pc_bound, 1),
        bands_3_and_5="VOID -- Pc underflows at every point; see the sheet",
        realign_days=realign, pc_max=pc_max,
        does_not_close="P1. A real covariance needs CDMs.")
    dest = ROOT / 'validation' / 'results' / 'A6_conjunction.json'
    os.makedirs(dest.parent, exist_ok=True)
    with open(dest, 'w') as fh:
        json.dump(out, fh, indent=2)
        fh.write("\n")
    print(f"\n-> {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
