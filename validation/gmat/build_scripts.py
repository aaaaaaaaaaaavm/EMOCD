"""
VOLLEY | Fill the GMAT script templates for analysis A5 (and the A6 ephemeris input).

Runs with no GMAT installed: it only writes .script files. Every orbital quantity comes
from analysis/astro.py itself -- boosted_elements() and _kepE() are imported, not
reimplemented, so the orbit definition cannot fork between the two codes.

Bands are NOT restated here. They live in validation/A5_astro_orekit.md and are applied
by parse_reports.py.

GMAT resolves relative ReportFile paths against its own bin/../output directory, not the
working directory, so every output path written into a script here is absolute.

Usage:  python3 build_scripts.py [--epoch '01 Jan 2027 00:00:00.000'] [--days 30]
Writes: output/emocd_lifetime_{low,mean,high}.script, output/emocd_fleet.script
"""
import argparse
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'analysis'))

from astro import MU, RE, boosted_elements, _kepE          # noqa: E402  the whole point

# --- operating point: identical to astro.py __main__ and conjunction() defaults --------
DV = 20.37                # m/s, rated exit velocity (motor_model.py)
ALT_M = 450e3             # host orbit
INC_DEG = 51.6
N_SHOTS = 12
SPACING_S = 1200.0
DAYS = 30
BC = 61.0                 # kg/m^2, the ballistic coefficient astro.py carries
CD = 2.2                  # matches the diff-drag baseline in astro.py seeding()
PAYLOAD_MASS = 4.0        # kg, 3U
STAGE_MASS = 300.0        # kg, lower bound of the 300-900 kg host class (E5)
STAGE_BC = 150.0          # kg/m^2, upper-body proxy -- an assumption, flagged in the JSON
CAP_YR = 40               # astro.py lifetime() cap_yr

# --- GMAT force-model settings, recorded into the results JSON by parse_reports.py -----
ATMOSPHERE = 'MSISE90'
GRAV_DEGREE = 20
GRAV_ORDER = 20
INTEGRATOR = 'RungeKutta89'
EPH_STEP_S = 60
ACTIVITY = {                      # F10.7, F10.7A, Kp -- see README: NOT equivalent to
    'low': (70.0, 70.0, 2.0),     # astro.py's 0.5/1.0/2.5 density scaling
    'mean': (150.0, 150.0, 3.0),
    'high': (250.0, 250.0, 4.0),
}


def drag_area(mass, bc, cd=CD):
    """A = m / (Cd * BC) -- inverts the BC convention used in astro.py rho/drag terms."""
    return mass / (cd * bc)


def true_anomaly_deg(M_rad, e):
    """Mean -> true anomaly, via astro.py's own Newton iteration."""
    E = float(_kepE(np.array([M_rad % (2 * math.pi)]), e)[0])
    nu = 2 * math.atan2(math.sqrt(1 + e) * math.sin(E / 2),
                        math.sqrt(1 - e) * math.cos(E / 2))
    return math.degrees(nu % (2 * math.pi))


def fill(template, mapping):
    out = template
    for key, value in mapping.items():
        out = out.replace('@@%s@@' % key, str(value))
    leftover = [tok for tok in out.split('@@') if tok.isupper() and '_' in tok]
    if leftover:
        raise SystemExit('unfilled placeholders: %s' % sorted(set(leftover)))
    # GMAT's interpreter rejects any script containing non-ASCII characters outright,
    # with an error that does not name the offending line. Catch it here instead.
    bad = sorted(set(ch for ch in out if ord(ch) > 127))
    if bad:
        raise SystemExit('non-ASCII characters in generated script: %s' % bad)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--epoch', default='01 Jan 2027 00:00:00.000',
                    help='UTCGregorian epoch; fixed so runs are reproducible')
    ap.add_argument('--days', type=int, default=30,
                    help='window for the bounded SMA-decay leg (full decay takes ~1.3 yr)')
    args = ap.parse_args()

    outdir = os.path.join(HERE, 'output')
    os.makedirs(outdir, exist_ok=True)

    ref_path = os.path.join(REPO, 'analysis', 'results', 'astro_results.json')
    ref = json.load(open(ref_path))

    r0 = RE + ALT_M
    a1, e1 = boosted_elements(ALT_M, DV)
    n0 = math.sqrt(MU / r0 ** 3)
    n1 = math.sqrt(MU / a1 ** 3)

    common = {
        'EPOCH': args.epoch,
        'SMA_BASE_KM': round(r0 / 1e3, 6),
        'ECC_BASE': 1e-6,
        'SMA_BOOST_KM': round(a1 / 1e3, 6),
        'ECC_BOOST': round(e1, 9),
        'INC_DEG': INC_DEG,
        'MASS_KG': PAYLOAD_MASS,
        'CD': CD,
        'DRAG_AREA_M2': round(drag_area(PAYLOAD_MASS, BC), 6),
        'GRAV_DEGREE': GRAV_DEGREE,
        'GRAV_ORDER': GRAV_ORDER,
        'ATMOSPHERE': ATMOSPHERE,
        'INTEGRATOR': INTEGRATOR,
    }

    # --- A5: one lifetime script per activity level ------------------------------------
    tmpl = open(os.path.join(HERE, 'emocd_lifetime.script.tmpl')).read()
    life_ref = ref['lifetime']
    for tag, (f107, f107a, kp) in ACTIVITY.items():
        key = {'low': 'low_activity', 'mean': 'mean', 'high': 'high_activity'}[tag]
        mapping = dict(common)
        mapping.update({
            'ACTIVITY': tag,
            'F107': f107, 'F107A': f107a, 'KP': kp,
            'REF_MULTIPLIER': life_ref[key]['multiplier'],
            'REF_BASE_YR': life_ref[key]['base_yr'],
            'CAP_YR': CAP_YR,
            'CAP_DAYS': int(CAP_YR * 365.25),
            'OUT_BASELINE': os.path.join(outdir, 'lifetime_%s_baseline.txt' % tag),
            'OUT_BOOSTED': os.path.join(outdir, 'lifetime_%s_boosted.txt' % tag),
        })
        path = os.path.join(outdir, 'emocd_lifetime_%s.script' % tag)
        open(path, 'w').write(fill(tmpl, mapping))
        print('wrote %s' % os.path.relpath(path, REPO))

    # --- A5 bounded leg: SMA decay over a fixed window ---------------------------------
    tmpl = open(os.path.join(HERE, 'emocd_sma_window.script.tmpl')).read()
    f107, f107a, kp = ACTIVITY['mean']
    mapping = dict(common)
    mapping.update({
        'F107': f107, 'F107A': f107a, 'KP': kp,
        'DV': DV,
        'DAYS': args.days,
        'OUT_SMA': os.path.join(outdir, 'sma_window_%dd.txt' % args.days),
    })
    path = os.path.join(outdir, 'emocd_sma%dd.script' % args.days)
    open(path, 'w').write(fill(tmpl, mapping))
    print('wrote %s' % os.path.relpath(path, REPO))

    # --- A6 input: fleet ephemerides ---------------------------------------------------
    sc_blocks, eph_blocks, names = [], [], ['stage']
    for k in range(N_SHOTS):
        tk = k * SPACING_S
        name = 'sat%02d' % (k + 1)
        names.append(name)
        aop = math.degrees((n0 * tk) % (2 * math.pi))
        ta = true_anomaly_deg(-n1 * tk, e1)
        sc_blocks.append('\n'.join([
            'Create Spacecraft %s;' % name,
            "GMAT %s.DateFormat = UTCGregorian;" % name,
            "GMAT %s.Epoch = '%s';" % (name, args.epoch),
            'GMAT %s.CoordinateSystem = EarthMJ2000Eq;' % name,
            'GMAT %s.DisplayStateType = Keplerian;' % name,
            'GMAT %s.SMA = %.6f;' % (name, a1 / 1e3),
            'GMAT %s.ECC = %.9f;' % (name, e1),
            'GMAT %s.INC = %s;' % (name, INC_DEG),
            'GMAT %s.RAAN = 0;' % name,
            'GMAT %s.AOP = %.6f;' % (name, aop),
            'GMAT %s.TA = %.6f;' % (name, ta),
            'GMAT %s.DryMass = %s;' % (name, PAYLOAD_MASS),
            'GMAT %s.Cd = %s;' % (name, CD),
            'GMAT %s.DragArea = %.6f;' % (name, drag_area(PAYLOAD_MASS, BC)),
            'GMAT %s.Cr = 1.8;' % name,
            'GMAT %s.SRPArea = %.6f;' % (name, drag_area(PAYLOAD_MASS, BC)),
            '',
        ]))
        eph_blocks.append('\n'.join([
            'Create EphemerisFile eph%s;' % name,
            'GMAT eph%s.Spacecraft = %s;' % (name, name),
            "GMAT eph%s.Filename = '%s/%s.oem';" % (name, os.path.join(outdir, 'ephemeris'), name),
            'GMAT eph%s.FileFormat = CCSDS-OEM;' % name,
            'GMAT eph%s.CoordinateSystem = EarthMJ2000Eq;' % name,
            'GMAT eph%s.StepSize = %s;' % (name, EPH_STEP_S),
            '',
        ]))

    tmpl = open(os.path.join(HERE, 'emocd_fleet.script.tmpl')).read()
    mapping = dict(common)
    f107, f107a, kp = ACTIVITY['mean']
    mapping.update({
        'F107': f107, 'F107A': f107a, 'KP': kp,
        'SPACING_S': SPACING_S,
        'DAYS': DAYS,
        'STAGE_MASS_KG': STAGE_MASS,
        'STAGE_DRAG_AREA_M2': round(drag_area(STAGE_MASS, STAGE_BC), 6),
        'EPH_STEP_S': EPH_STEP_S,
        'OUT_DIR': os.path.join(outdir, 'ephemeris'),
        'SPACECRAFT_BLOCK': '\n'.join(sc_blocks),
        'EPHEMERIS_BLOCK': '\n'.join(eph_blocks),
        'PROP_LIST': ', '.join(names),
    })
    path = os.path.join(outdir, 'emocd_fleet.script')
    open(path, 'w').write(fill(tmpl, mapping))
    os.makedirs(os.path.join(outdir, 'ephemeris'), exist_ok=True)
    print('wrote %s' % os.path.relpath(path, REPO))

    # --- self-check: the generated orbit must equal astro.py's, exactly ----------------
    a_check, e_check = boosted_elements(ALT_M, DV)
    assert abs(a_check - a1) == 0.0 and abs(e_check - e1) == 0.0
    print('\nboosted orbit from astro.boosted_elements(%g, %g): a = %.3f km, e = %.9f'
          % (ALT_M, DV, a1 / 1e3, e1))
    print('reference multiplier x%s, seeding %s'
          % (ref['lifetime']['mean']['multiplier'], ref['seeding_days']))
    print('\nNext: run the scripts headless, then python3 parse_reports.py')


if __name__ == '__main__':
    main()
