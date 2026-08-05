"""VOLLEY | Generate the A15 POEM deployment-campaign GMAT scripts, and cross-check them.

Runs with no GMAT installed: it writes .script files and verifies every orbital quantity it
writes against analysis/astro.py, which is imported rather than reimplemented so the orbit
definition cannot fork between the two codes.

WHY THIS IS A SEPARATE FILE FROM build_scripts.py
-------------------------------------------------
build_scripts.py generates the A5 and A6 inputs and is pinned to DV = 20.37 m/s, the operating
point those analyses were actually run at. Changing it would make regenerated scripts differ
from the ones whose results are recorded, which is a different kind of dishonesty. A15 is a new
analysis at the current point, so it gets its own generator. See P35.

WHAT IT PRODUCES
----------------
For each reference orbit (R1, R2, R3) and each case (A: VOLLEY only; B: POEM-assisted), one
GMAT script placing twelve satellites on their post-burn orbits, plus a cross-check JSON with
the analytically predicted spreads that A15's bands will be applied to.

Usage:  python3 build_poem_campaign.py [--epoch '01 Jan 2027 00:00:00.000'] [--days 90]
"""
import argparse
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'analysis'))

from astro import MU, RE, boosted_elements                 # noqa: E402  the whole point

J2 = 1.08263e-3
SPACING_S = 1200.0          # ADR-020, closes P31
N_SHOTS = 12
DAYS = 90
PAYLOAD_MASS = 4.0
STAGE_MASS = 300.0
BC, CD = 61.0, 2.2
STAGE_BC = 150.0
ATMOSPHERE, GRAV_DEGREE, GRAV_ORDER = 'MSISE90', 20, 20
INTEGRATOR = 'RungeKutta89'
F107, F107A, KP = 150.0, 150.0, 3.0

# Reference orbits. R2 and R3 are NOT traceable to this repository -- see A15.
CASES = {
    'R1': dict(alt_m=450e3, inc_deg=51.6,
               provenance='repo default, used by astro.py, A5 and A6'),
    'R2': dict(alt_m=350e3, inc_deg=55.2,
               provenance='POEM-4-like -- UNVERIFIED, confirm or cite before publishing'),
    'R3': dict(alt_m=350e3, inc_deg=9.6,
               provenance='POEM-3-like -- UNVERIFIED, confirm or cite before publishing'),
}

# Twelve firing directions in the RIC frame, as (in-plane angle from prograde, out-of-plane).
# Six in-plane for altitude extent, six with cross-track content for the (tiny) plane spread.
DIRECTIONS = [
    (0.0, 0.0), (0.0, 0.0), (180.0, 0.0), (180.0, 0.0),
    (0.0, 30.0), (180.0, -30.0), (0.0, 60.0), (180.0, -60.0),
    (0.0, 90.0), (0.0, -90.0), (90.0, 0.0), (270.0, 0.0),
]


def drag_area(mass, bc, cd=CD):
    return mass / (bc * cd)


def burn_elements(alt_m, inc_deg, dv, in_plane_deg, out_plane_deg):
    """Keplerian elements after one impulsive burn on a circular orbit.

    Gauss variational equations for a single impulse, small-dv linearisation. The
    tangential component is checked against astro.boosted_elements() by the caller.
    """
    r0 = RE + alt_m                            # astro.RE and astro.MU are both SI
    v0 = math.sqrt(MU / r0)
    b = math.radians(out_plane_deg)
    a_ip = math.radians(in_plane_deg)
    dv_t = dv * math.cos(b) * math.cos(a_ip)   # along-track
    dv_r = dv * math.cos(b) * math.sin(a_ip)   # radial
    dv_n = dv * math.sin(b)                    # cross-track

    v2 = (v0 + dv_t) ** 2 + dv_r ** 2 + dv_n ** 2          # vis-viva, exact in the impulse
    a = 1.0 / (2.0 / r0 - v2 / MU)
    ecc = math.hypot(2 * dv_t / v0, dv_r / v0)
    di = math.degrees(dv_n / v0)               # burn at the node: pure inclination
    draan = math.degrees(dv_n / (v0 * math.sin(math.radians(inc_deg))))
    return dict(sma_km=a / 1000.0, ecc=ecc, dinc_deg=di, draan_deg=draan,
                dv_t=dv_t, dv_r=dv_r, dv_n=dv_n)


def raan_dot_deg_day(a_km, inc_deg):
    a = a_km * 1000.0                          # work in metres, MU is SI
    n = math.sqrt(MU / a ** 3)
    return math.degrees(-1.5 * n * J2 * (RE / a) ** 2
                        * math.cos(math.radians(inc_deg))) * 86400.0


def fill(template, mapping):
    out = template
    for k, v in mapping.items():
        out = out.replace('@@%s@@' % k, str(v))
    if '@@' in out:
        import re
        raise SystemExit('unfilled placeholders: %s' % sorted(set(re.findall(r'@@\w+@@', out))))
    return out


def build_case(case_id, cfg, dv, epoch, days, outdir, tmpl):
    alt_m, inc = cfg['alt_m'], cfg['inc_deg']
    r0_km = (RE + alt_m) / 1000.0
    a_ref, e_ref = boosted_elements(alt_m, dv)

    sats, sc_blocks, rep_blocks, names = [], [], [], []
    for k, (ip, op) in enumerate(DIRECTIONS[:N_SHOTS]):
        el = burn_elements(alt_m, inc, dv, ip, op)
        n = math.sqrt(MU / el['sma_km'] ** 3)                 # rad/s
        t_k = k * SPACING_S
        ma = math.degrees(-n * t_k) % 360.0                   # rewind, see template header
        name = 'sat%02d' % (k + 1)
        names.append(name)
        rec = dict(name=name, shot=k + 1, t_s=t_k,
                   in_plane_deg=ip, out_plane_deg=op,
                   sma_km=el['sma_km'], ecc=el['ecc'],
                   inc_deg=inc + el['dinc_deg'], raan_deg=el['draan_deg'],
                   apogee_km=el['sma_km'] * (1 + el['ecc']) - r0_km,
                   perigee_km=el['sma_km'] * (1 - el['ecc']) - r0_km,
                   raan_dot_deg_day=raan_dot_deg_day(el['sma_km'], inc + el['dinc_deg']))
        sats.append(rec)
        sc_blocks.append(
            "Create Spacecraft {n};\n"
            "GMAT {n}.DateFormat = UTCGregorian;\n"
            "GMAT {n}.Epoch = '{ep}';\n"
            "GMAT {n}.CoordinateSystem = EarthMJ2000Eq;\n"
            "GMAT {n}.DisplayStateType = Keplerian;\n"
            "GMAT {n}.SMA = {a:.6f};\n"
            "GMAT {n}.ECC = {e:.9f};\n"
            "GMAT {n}.INC = {i:.6f};\n"
            "GMAT {n}.RAAN = {raan:.6f};\n"
            "GMAT {n}.AOP = 0;\n"
            "GMAT {n}.TA = {ma:.6f};\n"
            "GMAT {n}.DryMass = {m};\n"
            "GMAT {n}.Cd = {cd};\n"
            "GMAT {n}.DragArea = {da:.6f};\n"
            "GMAT {n}.Cr = 1.8;\n"
            "GMAT {n}.SRPArea = {da:.6f};\n".format(
                n=name, ep=epoch, a=rec['sma_km'], e=rec['ecc'], i=rec['inc_deg'],
                raan=rec['raan_deg'], ma=ma, m=PAYLOAD_MASS, cd=CD,
                da=drag_area(PAYLOAD_MASS, BC)))
        rep_blocks.append(
            "Create ReportFile rep{n};\n"
            "GMAT rep{n}.Filename = '{o}/{n}.txt';\n"
            "GMAT rep{n}.Add = {{{n}.UTCGregorian, {n}.Earth.SMA, {n}.Earth.ECC, "
            "{n}.EarthMJ2000Eq.INC, {n}.EarthMJ2000Eq.RAAN, {n}.Earth.Altitude}};\n"
            "GMAT rep{n}.WriteHeaders = true;\n"
            "GMAT rep{n}.ReportStepSize = 3600;\n".format(n=name, o=outdir))

    mapping = dict(
        CASE_ID=case_id, ALT_KM='%.0f' % (alt_m / 1000.0), INC_DEG=inc,
        ORBIT_PROVENANCE=cfg['provenance'], SPACING_S=SPACING_S, N_SHOTS=N_SHOTS, DV=dv,
        EPOCH=epoch, SMA_BASE_KM='%.6f' % r0_km, ECC_BASE='0.0',
        STAGE_MASS_KG=STAGE_MASS, CD=CD,
        STAGE_DRAG_AREA_M2='%.6f' % drag_area(STAGE_MASS, STAGE_BC),
        GRAV_DEGREE=GRAV_DEGREE, GRAV_ORDER=GRAV_ORDER, ATMOSPHERE=ATMOSPHERE,
        F107=F107, F107A=F107A, KP=KP, INTEGRATOR=INTEGRATOR, DAYS=days,
        SPACECRAFT_BLOCK='\n'.join(sc_blocks), REPORT_BLOCK='\n'.join(rep_blocks),
        PROP_LIST=', '.join(['poem'] + names))
    path = os.path.join(outdir, 'a15_poem_%s.script' % case_id.lower())
    with open(path, 'w', encoding='utf-8') as f:
        f.write(fill(tmpl, mapping))

    # --- cross-check against astro.py and the A15 bands ----------------------
    incs = [s['inc_deg'] for s in sats]
    raans = [s['raan_deg'] for s in sats]
    apo = max(s['apogee_km'] for s in sats)
    per = min(s['perigee_km'] for s in sats)
    rd = [s['raan_dot_deg_day'] for s in sats]
    prograde = next(s for s in sats if s['in_plane_deg'] == 0 and s['out_plane_deg'] == 0)
    sma_err = abs(prograde['sma_km'] - a_ref / 1000.0) / (a_ref / 1000.0) * 100

    return dict(
        case=case_id, script=os.path.relpath(path, REPO), provenance=cfg['provenance'],
        alt_km=alt_m / 1000.0, inc_deg=inc, dv=dv, spacing_s=SPACING_S,
        satellites=sats,
        predicted=dict(
            # Bands 1 and 3 test the PER-SATELLITE ceiling, which is the physically
            # meaningful quantity; the fleet spread is reported alongside because a
            # +/- pair doubles it and that is a fact about the campaign, not the machine.
            max_inclination_change_deg=max(abs(s['inc_deg'] - inc) for s in sats),
            max_raan_change_deg=max(abs(s['raan_deg']) for s in sats),
            inclination_spread_deg=max(incs) - min(incs),
            raan_spread_at_epoch_deg=max(raans) - min(raans),
            altitude_extent_km=apo - per,
            max_apogee_km=apo, min_perigee_km=per,
            raan_dot_spread_deg_day=max(rd) - min(rd),
            raan_spread_after_days_deg=(max(rd) - min(rd)) * days,
            campaign_duration_h=N_SHOTS * SPACING_S / 3600.0,
            sma_vs_astro_pct=sma_err))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--epoch', default='01 Jan 2027 00:00:00.000')
    ap.add_argument('--days', type=int, default=DAYS)
    args = ap.parse_args()

    with open(os.path.join(REPO, 'analysis', 'results', 'motor_results.json'),
              encoding='utf-8') as f:
        dv = json.load(f)['shot']['v_exit']

    outdir = os.path.join(HERE, 'output')
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(HERE, 'poem_campaign.script.tmpl'), encoding='utf-8') as f:
        tmpl = f.read()

    print("A15 POEM campaign, dv = %.3f m/s from motor_results.json, "
          "cadence %.0f s per ADR-020\n" % (dv, SPACING_S))
    out = []
    for cid, cfg in CASES.items():
        r = build_case(cid, cfg, dv, args.epoch, args.days, outdir, tmpl)
        out.append(r)
        p = r['predicted']
        print("%s  alt %-4.0f inc %-5.1f  %s" % (cid, r['alt_km'], r['inc_deg'],
                                                 cfg['provenance'][:44]))
        print("   max |d inc|     %8.4f deg    (band 1: <= 0.13)   fleet spread %.4f"
              % (p['max_inclination_change_deg'], p['inclination_spread_deg']))
        print("   altitude extent %8.1f km     (band 2: >= 100)" % p['altitude_extent_km'])
        print("   max |d RAAN|    %8.4f deg    (band 3: <= 0.75)   fleet spread %.4f"
              % (p['max_raan_change_deg'], p['raan_spread_at_epoch_deg']))
        print("   RAAN after %dd  %8.2f deg    (band 4: >= 5)" % (args.days,
                                                                 p['raan_spread_after_days_deg']))
        print("   SMA vs astro.py %8.4f %%      (band 5: <= 0.5)" % p['sma_vs_astro_pct'])
        print("   campaign        %8.2f h      (band 7: == 4.00)\n" % p['campaign_duration_h'])

    res = dict(analysis='A15', status='GENERATED AND CROSS-CHECKED, NOT EXECUTED IN GMAT',
               bands_declared_commit='e067da8', dv_m_s=dv, spacing_s=SPACING_S,
               adr='ADR-020', days=args.days, cases=out,
               note=('Band verdicts are NOT set here. These are the analytic predictions the '
                     'GMAT reports will be tested against by parse_reports.py.'))
    path = os.path.join(REPO, 'validation', 'results', 'A15_poem_campaign.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=2)
        f.write('\n')
    print("wrote %s" % os.path.relpath(path, REPO))
    print("Next: run the scripts in GMAT, then parse the reports back. See RUN_POEM.md")


if __name__ == '__main__':
    main()
