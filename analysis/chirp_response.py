"""A17: swept-excitation response of the track modes to the force-ripple chirp.

Bands declared in validation/A17_ripple_chirp.md at 13b4b3b, before this file existed.

Every shot sweeps the electrical frequency from zero as f = n*v/lambda, so the ripple chirps
through the track's structural modes twelve times per campaign. sizing.py checks the modes
against a static launch target, which is the right check for launch and the wrong one for the
shot.

E23 argues the sweep is too fast for resonant buildup. That argument depends on Q, and no Q,
damping ratio or loss factor appears anywhere in this repository -- so Q is SWEPT here, not
chosen, and the deliverable is the Q at which the argument stops holding.

Run:  python3 analysis/chirp_response.py
"""
import json
import math
import os

import numpy as np
from scipy.integrate import solve_ivp

import motor_model as mm
import sizing

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

Q_SWEEP = (20, 50, 100, 200, 350, 500)
GAP_BUDGET = 0.05e-3            # m, +/- gap shim tolerance, cad/parameters.json
M_TRACK_DIST = 20.0             # kg, sizing.track_first_mode's distributed mass
M_EFF = 0.5 * M_TRACK_DIST      # first-mode effective mass, uniform-beam proxy


def sweep_through(f_mode, rate_hz_s, Q, t_pad=0.75):
    """Peak dynamic amplification of an SDOF swept linearly through its own mode.

    Normalised: the forcing is unit amplitude per unit mass, so the returned number is
    max|x| divided by the static response 1/omega^2 and is independent of modal mass.
    """
    w = 2 * math.pi * f_mode
    t_cross = f_mode / rate_hz_s
    t0, t1 = max(0.0, t_cross - t_pad), t_cross + t_pad

    def rhs(t, y):
        phase = 2 * math.pi * 0.5 * rate_hz_s * t * t
        return [y[1], math.sin(phase) - (w / Q) * y[1] - w * w * y[0]]

    sol = solve_ivp(rhs, (t0, t1), [0.0, 0.0], max_step=1.0 / (40 * f_mode),
                    rtol=1e-8, atol=1e-12, dense_output=False)
    return float(np.max(np.abs(sol.y[0]))) * w * w, t_cross


def main():
    with open(os.path.join(RESULTS, 'motor_results.json'), encoding='utf-8') as f:
        shot = json.load(f)['shot']
    F_cmd = shot['F_cmd']
    ripple_pct = 0.99
    F0 = F_cmd * ripple_pct / 100.0                     # N, ripple amplitude
    a = F_cmd / (mm.M_SAT + mm.M_SLED)                  # m/s^2

    modes = sizing.track_first_mode()
    f_pinned = modes['pinned_pinned_Hz']
    f_fixed = modes['fixed_fixed_Hz']

    cases = [
        ('6th harmonic through the pinned mode', f_pinned, 6),
        ('6th harmonic through the fixed mode', f_fixed, 6),
        ('fundamental through the fixed mode', f_fixed, 1),
    ]

    out = []
    for label, f_mode, n in cases:
        rate = n * a / mm.LAM                            # Hz/s
        v_cross = f_mode * mm.LAM / n
        row = dict(case=label, f_mode_Hz=f_mode, harmonic=n,
                   sweep_rate_Hz_s=rate, v_at_crossing_m_s=v_cross,
                   t_at_crossing_s=v_cross / a,
                   distance_into_stroke_m=0.5 * v_cross ** 2 / a,
                   force_amplitude_N=F0 * (1.0 if n == 6 else 1.0),
                   amplification={})
        for Q in Q_SWEEP:
            amp, _ = sweep_through(f_mode, rate, Q)
            row['amplification'][Q] = amp
        # displacement at the worst Q, using the first-mode effective mass
        w = 2 * math.pi * f_mode
        static_x = F0 / (M_EFF * w * w)
        row['static_deflection_m'] = static_x
        row['peak_disp_m'] = static_x * max(row['amplification'].values())
        row['peak_disp_pct_of_gap_budget'] = 100 * row['peak_disp_m'] / GAP_BUDGET
        out.append(row)

    def q_for_2x(row):
        """Q at which amplification first reaches 2x static, by interpolation."""
        qs = sorted(row['amplification'])
        for lo, hi in zip(qs[:-1], qs[1:]):
            a_lo, a_hi = row['amplification'][lo], row['amplification'][hi]
            if a_lo < 2.0 <= a_hi:
                return lo + (2.0 - a_lo) * (hi - lo) / (a_hi - a_lo)
        return None if max(row['amplification'].values()) < 2.0 else qs[0]

    fixed6 = out[1]
    pinned6 = out[0]
    fund = out[2]
    q2 = {r['case']: q_for_2x(r) for r in out}

    def verdict(row, q=200):
        return 'PASS' if row['amplification'][q] < 2.0 else 'FAIL'

    bands = [
        dict(band=1, q='Amplification at the 109 Hz fixed mode, Q <= 200',
             result=fixed6['amplification'][200], verdict=verdict(fixed6)),
        dict(band=2, q='Amplification at the 48 Hz pinned mode, Q <= 200',
             result=pinned6['amplification'][200], verdict=verdict(pinned6)),
        dict(band=3, q='Q at which amplification first reaches 2x',
             result=q2, verdict='REPORT -- the deliverable'),
        dict(band=4, q='Peak displacement vs the +/-0.05 mm gap budget',
             result_pct=max(r['peak_disp_pct_of_gap_budget'] for r in out),
             verdict='PASS' if max(r['peak_disp_pct_of_gap_budget']
                                   for r in out) < 25 else 'FAIL'),
        dict(band=5, q='Amplification at the fundamental crossing of 109 Hz',
             result=fund['amplification'][200], verdict=verdict(fund)),
    ]

    print("A17 ripple chirp through the track modes  (bands at 13b4b3b)\n")
    print(f"  ripple amplitude {F0:.2f} N on {F_cmd:.1f} N, sled acceleration {a:.2f} m/s^2")
    print(f"  modes: {f_pinned:.0f} Hz pinned-pinned, {f_fixed:.0f} Hz fixed-fixed\n")
    hdr = 'case'.ljust(38) + 'rate Hz/s'.rjust(11) + ''.join(f'Q={q}'.rjust(9) for q in Q_SWEEP)
    print(hdr)
    for r in out:
        line = r['case'].ljust(38) + f"{r['sweep_rate_Hz_s']:11.0f}"
        line += ''.join(f"{r['amplification'][q]:9.3f}" for q in Q_SWEEP)
        print(line)
    print()
    for r in out:
        print(f"  {r['case']:<38} crossing at {r['v_at_crossing_m_s']:5.2f} m/s, "
              f"{r['t_at_crossing_s']*1e3:6.1f} ms, {r['distance_into_stroke_m']*1e3:7.1f} mm in")
    print()
    for k, v in q2.items():
        print(f"  Q for 2x amplification, {k:<40} {'never in sweep' if v is None else f'{v:.0f}'}")
    print()
    for b in bands:
        print(f"    band {b['band']}: {b['verdict']:<22} {b['q']}")

    res = dict(analysis='A17', bands_declared_commit='13b4b3b',
               caveat=('SDOF per mode, normalised so amplification is independent of modal '
                       'mass. The ripple force travels with the sled; this moving-load aspect '
                       'is not modelled, and band 4 additionally assumes a uniform-beam '
                       'effective mass of half the distributed 20 kg.'),
               ripple_amplitude_N=F0, sled_acceleration_m_s2=a,
               modes=modes, q_sweep=list(Q_SWEEP), cases=out,
               q_for_2x=q2, bands=bands)
    path = os.path.join(RESULTS, 'chirp_response.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=2)
        f.write('\n')
    print(f"\nwrote {path}")


if __name__ == '__main__':
    main()
