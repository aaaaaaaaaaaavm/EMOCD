"""
VOLLEY | Astrodynamics: lifetime multiplier, constellation seeding, conjunction, UQ.

Reproduces (paper Secs. IV-C, V-B, V-C) at the rated velocity of 16.388 m/s:
    lifetime multiplier         x1.80 at 450 km, BC 61 kg/m^2
    invariance                  x1.81 across BC 40-90 and 0.5-2.5x density
    Cowell vs orbit-averaged    99.4 % agreement on 30-day decay
    drift seeding 2/5/10 m/s    30 deg in 6.9 / 2.8 / 1.4 days
    differential drag (3:1)     30 deg in 25.0 days  <- the comparison baseline
    conjunction (screening)     4.6 km min / 12.3 km median at 20.37 m/s -- fragile
    phase realignment           8.1 days (the robust quantity; see OPEN_PROBLEMS P1)

MODEL LIMITATION: static exponential atmosphere (Vallado-class table, mean solar
activity). Absolute lifetimes carry severalfold uncertainty across the solar cycle;
the RATIO is what survives that uncertainty and is what the paper claims.

Conjunction results are SCREENING LEVEL. They do not replace per-shot COLA products.

Provenance: model output, not independently re-derived.
No result here has been checked against GMAT, STK, or any external propagator.
"""
import numpy as np
import math
import json
import os

# Outputs go next to this script, not next to whoever ran it. Every script here used to
# write to a cwd-relative "results/", so running one from the repository root created a
# SECOND, silently stale copy of its JSON at the root -- which is exactly what happened on
# 2026-07-30 and left a results/sizing.json carrying a superseded inter-array force. A
# duplicate that nothing regenerates is the defect class this repository logs twice
# already (P16, P19).
RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

MU = 3.986004418e14
RE = 6378.137e3
J2 = 1.08263e-3

# (base_alt_km, rho0 kg/m^3, scale height km) -- exponential atmosphere, mean activity
_TBL = [(150, 2.070e-9, 22.523), (180, 5.464e-10, 29.740), (200, 2.789e-10, 37.105),
        (250, 7.248e-11, 45.546), (300, 2.418e-11, 53.628), (350, 9.518e-12, 53.298),
        (400, 3.725e-12, 58.515), (450, 1.585e-12, 62.828), (500, 6.967e-13, 63.822),
        (600, 1.454e-13, 71.835), (700, 3.614e-14, 88.667)]
_BASES = np.array([t[0] for t in _TBL])
_RHOS = np.array([t[1] for t in _TBL])
_HS = np.array([t[2] for t in _TBL])


def rho(h_km, scale=1.0):
    i = np.clip(np.searchsorted(_BASES, h_km, side='right') - 1, 0, len(_TBL) - 1)
    return scale * _RHOS[i] * np.exp(-(h_km - _BASES[i]) / _HS[i])


def lifetime(a0, e0, BC=61.0, scale=1.0, cap_yr=40):
    """Per-revolution orbit-averaged decay via Gauss tangential equations."""
    a, e, t = a0, e0, 0.0
    E = np.linspace(0, 2 * np.pi, 181)
    while True:
        n = math.sqrt(MU / a ** 3)
        T = 2 * np.pi / n
        r = a * (1 - e * np.cos(E))
        h = (r - RE) / 1e3
        if (a * (1 - e) - RE) / 1e3 < 120:
            return t / 86400 / 365.25
        v = np.sqrt(MU * (2 / r - 1 / a))
        cosnu = (np.cos(E) - e) / (1 - e * np.cos(E))
        ft = -0.5 * rho(h, scale) * v ** 2 / BC
        dtdE = (1 - e * np.cos(E)) / n
        da = np.trapezoid(2 * a ** 2 * v / MU * ft * dtdE, E)
        de = np.trapezoid(2 * (e + cosnu) / v * ft * dtdE, E)
        k = max(1, int(min(abs(50 / (abs(da) + 1e-9)), 5000)))
        a += da * k
        e = max(0.0, e + de * k)
        t += T * k
        if t > cap_yr * 365.25 * 86400:
            return float(cap_yr)


def boosted_elements(alt_m, dv):
    r0 = RE + alt_m
    v0 = math.sqrt(MU / r0)
    a = 1 / (2 / r0 - (v0 + dv) ** 2 / MU)
    return a, 1 - r0 / a


def cowell_sma_after(days, alt_m=450e3, BC=61.0, dt=30.0):
    """Independent RK4 Cowell propagation with drag, for cross-validation."""
    r0 = RE + alt_m
    r = np.array([r0, 0.0, 0.0])
    v = np.array([0.0, math.sqrt(MU / r0), 0.0])

    def acc(r_, v_):
        rn = np.linalg.norm(r_)
        return -MU * r_ / rn ** 3 - 0.5 * rho((rn - RE) / 1e3) * np.linalg.norm(v_) / BC * v_

    for _ in range(int(days * 86400 / dt)):
        k1, k1v = acc(r, v), v
        k2, k2v = acc(r + k1v * dt / 2, v + k1 * dt / 2), v + k1 * dt / 2
        k3, k3v = acc(r + k2v * dt / 2, v + k2 * dt / 2), v + k2 * dt / 2
        k4, k4v = acc(r + k3v * dt, v + k3 * dt), v + k3 * dt
        r = r + dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        v = v + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return -MU / 2 / (0.5 * np.dot(v, v) - MU / np.linalg.norm(r))


def _kepE(M, e):
    E = M.copy()
    for _ in range(15):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E


def propagate(a, e, inc, argp, M0, t):
    """Kepler + secular J2."""
    n = math.sqrt(MU / a ** 3)
    p = a * (1 - e ** 2)
    dO = -1.5 * J2 * n * (RE / p) ** 2 * math.cos(inc)
    dw = 0.75 * J2 * n * (RE / p) ** 2 * (5 * math.cos(inc) ** 2 - 1)
    dM = 0.75 * J2 * n * (RE / p) ** 2 * math.sqrt(1 - e ** 2) * (3 * math.cos(inc) ** 2 - 1)
    M = M0 + (n + dM) * t
    Om, w = dO * t, argp + dw * t
    E = _kepE(np.mod(M, 2 * np.pi), e)
    nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
    r = a * (1 - e * np.cos(E))
    xo, yo = r * np.cos(nu), r * np.sin(nu)
    cO, sO = np.cos(Om), np.sin(Om)
    ci, si = math.cos(inc), math.sin(inc)
    cw, sw = np.cos(w), np.sin(w)
    return np.stack([(cO * cw - sO * sw * ci) * xo + (-cO * sw - sO * cw * ci) * yo,
                     (sO * cw + cO * sw * ci) * xo + (-sO * sw + cO * cw * ci) * yo,
                     (sw * si) * xo + (cw * si) * yo], -1)


def conjunction(dv=16.388, alt_m=450e3, inc_deg=51.6, n_shots=12, spacing_s=1200.0,
                days=30, trace=False):
    r0 = RE + alt_m
    inc = math.radians(inc_deg)
    a1, e1 = boosted_elements(alt_m, dv)
    n0 = math.sqrt(MU / r0 ** 3)
    n1 = math.sqrt(MU / a1 ** 3)
    t = np.arange(0, days * 86400, 10.0)
    stage = propagate(r0, 1e-6, inc, 0, 0, t)
    mins = []
    for k in range(n_shots):
        tk = k * spacing_s
        argp = (n0 * tk) % (2 * np.pi)
        s = propagate(a1, e1, inc, argp, -n1 * tk, t)
        mask = t > tk + 3600
        d = np.linalg.norm(s[mask] - stage[mask], axis=1)
        tc = t[mask][int(np.argmin(d))]
        tf = np.arange(max(tc - 60, tk + 3600), tc + 60, 0.25)   # refine
        df = np.linalg.norm(propagate(a1, e1, inc, argp, -n1 * tk, tf)
                            - propagate(r0, 1e-6, inc, 0, 0, tf), axis=1)
        mins.append(df.min())
    T0 = 2 * np.pi / n0
    T1 = 2 * np.pi / n1
    out = dict(min_km=round(min(mins) / 1e3, 1), median_km=round(float(np.median(mins)) / 1e3, 1),
               realign_days=round(T0 / (T1 - T0) * T0 / 86400, 1))
    if trace:
        # coarse range history of the first satellite, for the conjunction figure
        s0 = propagate(a1, e1, inc, 0, 0, t)
        m0 = t > 3600
        out['trace_days'] = t[m0] / 86400
        out['trace_km'] = np.linalg.norm(s0[m0] - stage[m0], axis=1) / 1e3
        out['mins_km'] = np.array(mins) / 1e3
    return out


def seeding(alt_m=450e3, splits=(2, 5, 10), target_deg=30):
    r0 = RE + alt_m
    v0 = math.sqrt(MU / r0)
    T = 2 * np.pi * math.sqrt(r0 ** 3 / MU)
    out = {}
    for dv in splits:
        da = 2 * r0 * dv / v0
        dT = 1.5 * da / r0 * T
        deg_day = dT / T * 360 * (86400 / T)
        out[f'{dv}m/s'] = round(target_deg / deg_day, 1)
    # differential drag baseline, 3:1 area ratio, same density model
    n = math.sqrt(MU / r0 ** 3)
    q = 0.5 * rho((r0 - RE) / 1e3) * v0 ** 2
    df = q * 2.2 * 0.03 / 4 - q * 2.2 * 0.01 / 4
    t30 = math.sqrt(math.radians(target_deg) * 2 * v0 / (3 * n * df))
    out['differential_drag_days'] = round(t30 / 86400, 1)
    return out


if __name__ == '__main__':
    # Rated exit velocity, from motor_model.py at the CAD-derived 9.445 kg sled (P15).
    # Was 20.37 m/s against the 4.86 kg parametric estimate until 2026-07-29.
    DV = 16.388
    res = {}

    print("=== lifetime multiplier, 450 km ===")
    r0 = RE + 450e3
    mult = {}
    for scale, tag in [(0.5, 'low_activity'), (1.0, 'mean'), (2.5, 'high_activity')]:
        L0 = lifetime(r0, 1e-6, scale=scale)
        a, e = boosted_elements(450e3, DV)
        L1 = lifetime(a, e, scale=scale)
        mult[tag] = dict(base_yr=round(L0, 2), multiplier=round(L1 / L0, 2))
        print(f"  {tag:15s} base {L0:5.2f} yr  x{L1/L0:.2f}")
    for BC in (40, 90):
        L0 = lifetime(r0, 1e-6, BC=BC)
        a, e = boosted_elements(450e3, DV)
        print(f"  BC={BC:<3d}          x{lifetime(a, e, BC=BC)/L0:.2f}")
    res['lifetime'] = mult

    print("\n=== cross-validation: 30-day decay ===")
    a_cow = cowell_sma_after(30)
    a, e, t = r0, 1e-6, 0.0
    E = np.linspace(0, 2 * np.pi, 181)
    while t < 30 * 86400:
        n = math.sqrt(MU / a ** 3)
        T = 2 * np.pi / n
        r = a * (1 - e * np.cos(E))
        v = np.sqrt(MU * (2 / r - 1 / a))
        cn = (np.cos(E) - e) / (1 - e * np.cos(E))
        ft = -0.5 * rho((r - RE) / 1e3) * v ** 2 / 61.0
        dtdE = (1 - e * np.cos(E)) / n
        a += np.trapezoid(2 * a ** 2 * v / MU * ft * dtdE, E)
        e = max(0.0, e + np.trapezoid(2 * (e + cn) / v * ft * dtdE, E))
        t += T
    agree = 100 * min(r0 - a_cow, r0 - a) / max(r0 - a_cow, r0 - a)
    print(f"  Cowell da {r0-a_cow:.0f} m | orbit-averaged {r0-a:.0f} m | agreement {agree:.1f} %")
    res['cross_validation_pct'] = round(agree, 1)

    print("\n=== constellation seeding vs differential drag ===")
    s = seeding()
    for k, v in s.items():
        print(f"  {k:24s} {v} days")
    res['seeding_days'] = s

    print("\n=== conjunction screening ===")
    c = conjunction(dv=DV)
    print(f"  min {c['min_km']} km | median {c['median_km']} km | realign {c['realign_days']} d")
    res['conjunction'] = c

    r0_ = RE + 450e3
    v0_ = math.sqrt(MU / r0_)
    res['apogee_placement_km'] = round(4 * r0_ * 0.027 / v0_ / 1e3, 2)
    res['recoil_Ns_per_shot'] = round(4.0 * DV, 1)
    res['plane_change_ceiling_deg'] = round(math.degrees(DV / v0_), 2)
    print(f"\napogee placement +/-{res['apogee_placement_km']} km | "
          f"recoil {res['recoil_Ns_per_shot']} N.s | plane ceiling {res['plane_change_ceiling_deg']} deg")

    os.makedirs(RESULTS, exist_ok=True)
    json.dump(res, open(os.path.join(RESULTS, 'astro_results.json'), 'w'), indent=2)
    print("\n-> results/astro_results.json")
