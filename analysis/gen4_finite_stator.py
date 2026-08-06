"""A16: thrust against sled station when the Gen4 array runs off the end of the stator.

Bands declared in validation/A16_gen4_finite_stator.md at 13b4b3b, before this file existed.

The Phase I model assumes a uniform 1.30 m stator and computes one thrust constant. Gen4 gives
the same 488 mm sled a 900 mm stroke against a stator ending at x = 1295.5 mm, so the last
148.5 mm runs with the array only partly over energised copper.

This reuses motor_model.build_field() and the same six-sector belt pattern thrust_constant()
integrates, with the same Gauss-Legendre thickness quadrature, so the two cannot fork. The only
difference is that current exists only where the stator does.

UPPER BOUND, NOT A FORCE LAW
----------------------------
Truncating an otherwise-periodic winding captures the loss of energised length and nothing else.
End fields, winding termination and the phase-progression disturbance at the boundary are all
absent, and E27 names every one of them. Treat the run-out force as an upper bound.

NO NUMBER HERE IS A GEN4 PERFORMANCE FIGURE. docs/GEN4_STATUS.md keeps the export gate closed.

Run:  python3 analysis/gen4_finite_stator.py
"""
import json
import math
import os

import numpy as np

import motor_model as mm

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

# --- Gen4 stations, from docs/GEN4_STATUS.md (mm -> m) -----------------------
ARRAY_LOCAL_LO, ARRAY_LOCAL_HI = -0.096, 0.244      # array vs sled origin
STATOR_LO, STATOR_HI = 0.0005, 1.2955
S_STOW, S_RELEASE = 0.300, 1.200
FULL_OVERLAP_UNTIL = STATOR_HI - ARRAY_LOCAL_HI     # 1.0515 m


def overlap(s):
    """Length of array that is over energised stator at station s."""
    lo = max(s + ARRAY_LOCAL_LO, STATOR_LO)
    hi = min(s + ARRAY_LOCAL_HI, STATOR_HI)
    return max(0.0, hi - lo)


def thrust_profile(nx=240, ny=9, n_station=181):
    """Lorentz integral over the overlapped region only, at each station."""
    field = mm.build_field()
    xs = np.linspace(0, mm.LAM, nx, endpoint=False)
    y_nodes, y_w = np.polynomial.legendre.leggauss(ny)
    ys = y_nodes * mm.WIND_THICK / 2
    X, Y = np.meshgrid(xs, ys)
    By = field.getB(np.stack([X.ravel(), Y.ravel(), np.zeros(X.size)], 1))[:, 1].reshape(ny, nx)

    belt = mm.LAM / 6
    seq = [(0, +1), (2, -1), (1, +1), (0, -1), (2, +1), (1, -1)]
    ph = np.array([seq[int((x % mm.LAM) // belt)][0] for x in xs])
    sg = np.array([seq[int((x % mm.LAM) // belt)][1] for x in xs])
    dx = mm.LAM / nx
    K = mm.K_RATED * 0.9

    def force_per_metre(phi):
        """Thrust per metre of overlapped array, averaged over sled travel."""
        acc = []
        for shift in range(0, nx, 5):
            Byx = np.roll(By, +shift, axis=1)
            te = 2 * math.pi * (shift * dx) / mm.LAM - phi
            i = np.array([math.cos(te), math.cos(te - 2 * math.pi / 3),
                          math.cos(te + 2 * math.pi / 3)])
            Jz = K * i[ph] * sg / mm.WIND_THICK
            f = float((y_w[:, None] * Jz[None, :] * Byx).sum()
                      * dx * (mm.WIND_THICK / 2) * mm.DEPTH)
            acc.append(f / mm.LAM)          # per metre of array
        return float(np.mean(acc))

    phis = np.linspace(0, 2 * math.pi, 144, endpoint=False)
    f_per_m = max(force_per_metre(p) for p in phis)

    stations = np.linspace(S_STOW, S_RELEASE, n_station)
    rows = [dict(s_m=float(s), overlap_m=overlap(s),
                 overlap_frac=overlap(s) / mm.SLED_ACTIVE_LEN,
                 F_N=f_per_m * overlap(s)) for s in stations]
    return f_per_m, rows


def integrate(rows):
    """Velocity and energy from the position-dependent force."""
    m = mm.M_SAT + mm.M_SLED
    v = 0.0
    work = 0.0
    for a, b in zip(rows[:-1], rows[1:]):
        ds = b['s_m'] - a['s_m']
        F = 0.5 * (a['F_N'] + b['F_N'])
        work += F * ds
        v = math.sqrt(max(0.0, v * v + 2 * F / m * ds))
    return v, work


def main():
    with open(os.path.join(RESULTS, 'motor_results.json'), encoding='utf-8') as f:
        ref = json.load(f)
    F_periodic = ref['shot']['F_cmd']
    v_phase1 = ref['shot']['v_exit']

    f_per_m, rows = thrust_profile()
    F_full = f_per_m * mm.SLED_ACTIVE_LEN
    band1_pct = abs(F_full - F_periodic) / F_periodic * 100

    at_release = rows[-1]
    forces = [r['F_N'] for r in rows]
    monotonic = all(b <= a + 1e-6 for a, b in zip(forces[:-1], forces[1:])
                    if b < F_full - 1e-6 or True)
    run_out = [r for r in rows if r['s_m'] > FULL_OVERLAP_UNTIL]
    mono_runout = all(b['F_N'] <= a['F_N'] + 1e-6 for a, b in zip(run_out[:-1], run_out[1:]))

    v_gen4, work = integrate(rows)

    bands = [
        dict(band=1, q='Fully-overlapped thrust vs the Phase I periodic result',
             limit_pct=2.0, result_pct=band1_pct,
             verdict='PASS' if band1_pct < 2.0 else 'FAIL'),
        dict(band=2, q='Thrust at release, s = 1200 mm', result_N=at_release['F_N'],
             overlap_frac=at_release['overlap_frac'],
             force_frac=at_release['F_N'] / F_full, verdict='REPORT'),
        dict(band=3, q='Thrust monotonic non-increasing through the run-out',
             result=mono_runout, verdict='PASS' if mono_runout else 'FAIL'),
        dict(band=4, q='Exit velocity from integrating F(s) over 900 mm',
             result_m_s=v_gen4, verdict='REPORT ONLY, NOT ADOPTED'),
        dict(band=5, q='Ratio to the Phase I 16.388 m/s', result=v_gen4 / v_phase1,
             verdict='REPORT'),
    ]

    print("A16 Gen4 finite-stator thrust  (bands at 13b4b3b)\n")
    print(f"  thrust per metre of overlapped array   {f_per_m:10.2f} N/m")
    print(f"  full-overlap thrust                    {F_full:10.3f} N")
    print(f"  Phase I periodic F_cmd                 {F_periodic:10.3f} N"
          f"   -> {band1_pct:.3f} %  (band 1: < 2 %)")
    print(f"  full overlap holds until s =           {FULL_OVERLAP_UNTIL*1e3:10.1f} mm")
    print(f"  overlap at release                     {at_release['overlap_m']*1e3:10.1f} mm"
          f"  ({at_release['overlap_frac']*100:.1f} %)")
    print(f"  thrust at release                      {at_release['F_N']:10.3f} N"
          f"  ({at_release['F_N']/F_full*100:.1f} % of full)")
    print(f"  work over the 900 mm stroke            {work:10.1f} J")
    print(f"  exit velocity (REPORT ONLY)            {v_gen4:10.3f} m/s"
          f"  = {v_gen4/v_phase1:.3f} x Phase I\n")
    for b in bands:
        print(f"    band {b['band']}: {b['verdict']:<24} {b['q']}")

    res = dict(analysis='A16', bands_declared_commit='13b4b3b',
               caveat=('Upper bound on run-out force. End fields, winding termination and the '
                       'phase-progression disturbance are absent. NOT a Gen4 performance '
                       'figure; the export gate stays closed.'),
               stations=dict(stow_m=S_STOW, release_m=S_RELEASE,
                             stator_lo_m=STATOR_LO, stator_hi_m=STATOR_HI,
                             full_overlap_until_m=FULL_OVERLAP_UNTIL),
               force_per_metre_N_per_m=f_per_m, F_full_overlap_N=F_full,
               F_periodic_N=F_periodic, work_J=work,
               v_exit_reported_m_s=v_gen4, v_phase1_m_s=v_phase1,
               profile=rows, bands=bands)
    path = os.path.join(RESULTS, 'gen4_finite_stator.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=2)
        f.write('\n')
    print(f"\nwrote {path}")


if __name__ == '__main__':
    main()
