"""A7-R: what tip-off tolerance the release mechanism has to hold, and why A7 cannot close here.

Bands were declared in validation/A7_separation_chrono.md on 2026-07-31 and tightened to
2 deg/s before any run (P30). They are not restated or widened here.

WHY THIS IS A7-R AND NOT A7
---------------------------
A7 specifies Project Chrono: a multibody contact simulation of the payload leaving the cradle.
Chrono is not available in this environment, and more importantly **the release mechanism it
would simulate is not defined anywhere in this repository**. The paper says force is removed in
the coast-trim zone and the sled then enters the brake while the satellite departs; it does not
say how the cradle rails disengage, in what order, with what friction, or over what time.

A multibody model of an undefined mechanism would produce a number with no provenance. So this
is deliberately the other analysis: **given the geometry that IS defined, how tight does the
release have to be to meet the 2 deg/s band?** That is a tolerance the mechanism designer can
be handed, and it is falsifiable.

The same substitution discipline A1 used for FEMM applies: the substitution is recorded, and
A7's verdict stays open rather than being claimed from a reduced model.

WHAT DRIVES TIP-OFF HERE
------------------------
The payload's centre of mass sits 70 mm off the thrust line (`cad/parameters.json`
`payload_com_offset_above_thrust_line`). Any longitudinal force that is not reacted by a
balancing couple therefore torques the payload about its transverse axis. During acceleration
the cradle supplies that couple. Tip-off is whatever angular impulse survives the moment the
couple stops being supplied.

Run:  python3 validation/chrono/tipoff_sensitivity.py
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'analysis'))

import motor_model as mm                                    # noqa: E402

RESULTS = os.path.join(ROOT, 'validation', 'results')

# --- payload, from cad/parameters.json payload_3u ----------------------------
M_SAT = 4.0
L_X, W_Y, H_Z = 0.3405, 0.100, 0.100
D_COM = 0.070                       # m, CoM above the thrust line
BAND_PRIMARY = 2.0                  # deg/s, NRCSD -- declared 2026-07-31
BAND_SECONDARY = 5.0                # deg/s, NRCSD-E, provisional


def inertia_transverse():
    """3U about its transverse axis through the CoM, uniform-density proxy."""
    return M_SAT * (W_Y ** 2 + L_X ** 2) / 12.0


def main():
    with open(os.path.join(ROOT, 'analysis', 'results', 'motor_results.json'),
              encoding='utf-8') as f:
        shot = json.load(f)['shot']

    a_g = shot['a_g']
    F_push = M_SAT * a_g * 9.80665          # N, force on the payload during acceleration
    ripple_pct = 0.99                        # from motor_results Kt ripple
    I = inertia_transverse()
    band_rad = math.radians(BAND_PRIMARY)

    # An unbalanced longitudinal force F acting D_COM off the CoM for time dt gives
    #     dw = F * D_COM * dt / I
    # Invert for the dt each candidate force may persist before the band is broken.
    def max_dt(F):
        return band_rad * I / (F * D_COM) if F > 0 else float('inf')

    cases = [
        ('full push unbalanced', F_push),
        ('10 % of push unbalanced', 0.10 * F_push),
        ('1 % of push unbalanced', 0.01 * F_push),
        ('force ripple only', F_push * ripple_pct / 100.0),
        ('1 N residual (latch, harness, friction)', 1.0),
    ]
    tol = [dict(case=c, force_N=F, max_duration_s=max_dt(F),
                max_duration_us=max_dt(F) * 1e6) for c, F in cases]

    # The inverse view: a fixed asymmetry duration, what force is permitted.
    durations = (1e-5, 1e-4, 1e-3, 1e-2)
    force_tol = [dict(duration_s=d, max_force_N=band_rad * I / (D_COM * d)) for d in durations]

    # Angular impulse budget: the total the payload may absorb at all.
    ang_impulse = band_rad * I

    res = dict(
        analysis='A7-R',
        status='REDUCED ANALYSIS. A7 REMAINS UNRUN -- see the run sheet',
        substitution=('Project Chrono unavailable, and the release mechanism it would '
                      'simulate is undefined in this repository. This computes the tolerance '
                      'the mechanism must hold instead of inventing one.'),
        bands_declared='2026-07-31, tightened to 2 deg/s before any run (P30)',
        inputs=dict(m_sat=M_SAT, a_g=a_g, F_push_N=F_push,
                    com_offset_m=D_COM, I_transverse_kgm2=I,
                    band_primary_deg_s=BAND_PRIMARY, band_secondary_deg_s=BAND_SECONDARY),
        angular_impulse_budget_Nms=ang_impulse,
        duration_tolerance=tol,
        force_tolerance=force_tol)

    print("A7-R: release tolerance against the 2 deg/s band declared 2026-07-31\n")
    print(f"  payload {M_SAT} kg, transverse inertia {I:.5f} kg m^2")
    print(f"  push during acceleration {F_push:.1f} N at {a_g:.3f} g")
    print(f"  CoM offset {D_COM*1e3:.0f} mm off the thrust line")
    print(f"  total angular impulse the payload may absorb: {ang_impulse*1e3:.3f} mN m s\n")
    print(f"  {'unbalanced force':<42}{'N':>9}{'may persist for':>18}")
    for t in tol:
        d = t['max_duration_us']
        s = f"{d:,.1f} us" if d < 1e4 else f"{d/1e6:,.3f} s"
        print(f"  {t['case']:<42}{t['force_N']:9.2f}{s:>18}")
    print(f"\n  {'if the asymmetry lasts':<42}{'max unbalanced force':>26}")
    for f in force_tol:
        print(f"  {f['duration_s']*1e3:>10.2f} ms{'':<30}{f['max_force_N']:20.3f} N")

    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, 'A7R_tipoff_sensitivity.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=2)
        f.write('\n')
    print(f"\nwrote {path}")


if __name__ == '__main__':
    main()
