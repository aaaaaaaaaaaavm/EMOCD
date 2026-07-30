"""
VOLLEY | Parse GMAT output into validation/results/A5_astro.json.

Applies the acceptance bands declared in validation/A5_astro_orekit.md BEFORE any run:

    lifetime multiplier      x1.80  +/- 5 %
    invariance across        spread <= 5 %
      low/mean/high

Absolute lifetimes are recorded but are NOT a pass/fail criterion (OPEN_PROBLEMS E6):
astro.py uses a static exponential atmosphere and GMAT uses MSIS-class, so they are
expected to differ. The ratio is the claim.

Two legs:
  * bounded window  -- sma_window_<N>d.txt, decay RATE compared against astro.py
  * full decay      -- lifetime_<level>_{baseline,boosted}.txt, MULTIPLIER vs the band

Usage:  python3 parse_reports.py [--invocation '<the exact command that ran GMAT>']
"""
import argparse
import glob
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
OUTDIR = os.path.join(HERE, 'output')
sys.path.insert(0, os.path.join(REPO, 'analysis'))

MULTIPLIER_BAND_PCT = 5.0
INVARIANCE_SPREAD_PCT = 5.0


def read_report(path):
    """GMAT ReportFile: header line(s) then whitespace columns.

    `Report` commands re-emit the header each call, so header lines appear throughout the
    file, not only at the top. Rows are kept only when every field parses as a float.
    """
    header, rows = None, []
    for line in open(path):
        parts = line.split()
        if not parts:
            continue
        try:
            rows.append([float(p) for p in parts])
        except ValueError:
            if header is None:
                header = parts
    if not rows:
        raise SystemExit('%s: no numeric rows' % path)
    return header, rows


def column(header, rows, needle):
    idx = next((i for i, h in enumerate(header) if needle in h), None)
    if idx is None:
        raise SystemExit('no column matching %r (have %s)' % (needle, header))
    return [r[idx] for r in rows if len(r) > idx]


CAP_DAYS = 40 * 365.25          # astro.py lifetime() cap_yr, mirrored in the script


def decay_days(path):
    """Elapsed days at the last row, or None if the run has not finished.

    A finished run stops at the 120 km altitude floor (or the 40-year cap). Reading a file
    GMAT is still writing gives a partial decay and a meaningless multiplier -- which is
    exactly what happened on the first parse of an in-flight run, producing a confident
    FAIL. Check the stop condition was actually reached before trusting the last row.
    """
    header, rows = read_report(path)
    days = column(header, rows, 'ElapsedDays')[-1]
    alt = column(header, rows, 'Altitude')[-1]
    if alt > 121.0 and days < CAP_DAYS - 1:
        return None
    return days


def window_leg(result):
    """Decay RATE over the bounded window, GMAT vs astro.py.

    Reported SMA is osculating, so short-period J2 and lunisolar terms (several km
    peak-to-peak here) swamp the ~0.1 km/day decay signal. Differencing the endpoints is
    therefore meaningless; a least-squares slope over all samples is the honest estimate,
    and the residual spread is reported so the reader can see how noisy the fit is.
    """
    paths = sorted(glob.glob(os.path.join(OUTDIR, 'sma_window_*d.txt')))
    if not paths:
        return
    from astro import cowell_sma_after, RE
    header, rows = read_report(paths[0])
    days = np.array(column(header, rows, 'day'))
    sma = np.array(column(header, rows, 'baseline.Earth.SMA'))
    A = np.vstack([days, np.ones_like(days)]).T
    slope, _ = np.linalg.lstsq(A, sma, rcond=None)[0]
    resid = sma - (slope * days + np.linalg.lstsq(A, sma, rcond=None)[0][1])
    n_days = float(days.max())
    a0 = (RE + 450e3) / 1e3
    astro_rate = (cowell_sma_after(n_days) / 1e3 - a0) / n_days
    result['window_leg'] = {
        'file': os.path.relpath(paths[0], REPO),
        'window_days': n_days,
        'samples': int(len(days)),
        'gmat_rate_km_per_day': round(float(slope), 5),
        'astro_rate_km_per_day': round(float(astro_rate), 5),
        'ratio_gmat_over_astro': round(float(slope / astro_rate), 3),
        'osculating_residual_rms_km': round(float(resid.std()), 2),
        'note': ('Rates, not endpoints: reported SMA is osculating and its short-period '
                 'variation exceeds the decay over this window. A rate difference is '
                 'expected -- static exponential atmosphere vs MSIS -- and is not a '
                 'failure. E6 defends the ratio, not the absolutes.'),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--invocation', default='',
                    help='the exact GMAT command that produced this output')
    args = ap.parse_args()

    ref = json.load(open(os.path.join(REPO, 'analysis', 'results', 'astro_results.json')))
    ref_multiplier = ref['lifetime']['mean']['multiplier']

    result = {
        'analysis': 'A5',
        'tool': 'GMAT R2022a (GmatConsole, headless)',
        'invocation': args.invocation,
        'bands_declared_in': 'validation/A5_astro_orekit.md',
        'force_models': {
            'atmosphere': 'MSISE90', 'gravity': '20x20', 'integrator': 'RungeKutta89',
            'point_masses': ['Luna', 'Sun'], 'srp': True,
        },
        'reference': {'multiplier': ref_multiplier,
                      'base_years': {k: v['base_yr'] for k, v in ref['lifetime'].items()},
                      'source': 'analysis/results/astro_results.json'},
        'levels': {},
        'ephemerides': sorted(os.path.relpath(p, REPO)
                              for p in glob.glob(os.path.join(OUTDIR, 'ephemeris', '*.oem'))),
    }

    window_leg(result)

    multipliers = []
    for tag, key in (('low', 'low_activity'), ('mean', 'mean'), ('high', 'high_activity')):
        base = os.path.join(OUTDIR, 'lifetime_%s_baseline.txt' % tag)
        boost = os.path.join(OUTDIR, 'lifetime_%s_boosted.txt' % tag)
        if not (os.path.exists(base) and os.path.exists(boost)):
            result['levels'][tag] = {'status': 'not run'}
            continue
        d0, d1 = decay_days(base), decay_days(boost)
        if d0 is None or d1 is None:
            result['levels'][tag] = {'status': 'in progress -- 120 km floor not reached'}
            continue
        entry = {'baseline_days': round(d0, 2), 'boosted_days': round(d1, 2),
                 'baseline_years': round(d0 / 365.25, 3), 'boosted_years': round(d1 / 365.25, 3),
                 'astro_baseline_years': ref['lifetime'][key]['base_yr']}
        if d0:
            mult = d1 / d0
            dev = 100.0 * (mult - ref_multiplier) / ref_multiplier
            entry.update(multiplier=round(mult, 4), deviation_pct=round(dev, 2),
                         within_band=abs(dev) <= MULTIPLIER_BAND_PCT)
            multipliers.append(mult)
        result['levels'][tag] = entry

    if len(multipliers) >= 2:   # only across *finished* levels
        spread = 100.0 * (max(multipliers) - min(multipliers)) / (sum(multipliers) / len(multipliers))
        result['invariance'] = {'spread_pct': round(spread, 2),
                                'within_band': spread <= INVARIANCE_SPREAD_PCT}

    checks = [v.get('within_band') for v in result['levels'].values() if 'within_band' in v]
    done = len(checks)
    if not checks:
        result['verdict'] = 'partial -- window leg only, no full decay finished'
    elif done < 3:
        ok = all(checks) and result.get('invariance', {}).get('within_band', True)
        result['verdict'] = ('partial -- %d of 3 activity levels complete, %s so far'
                             % (done, 'within band' if ok else 'OUT OF BAND'))
    elif all(checks) and result.get('invariance', {}).get('within_band', True):
        result['verdict'] = 'pass'
    else:
        result['verdict'] = 'FAIL -- open a P-item; do not edit analysis/astro.py'

    dest = os.path.join(REPO, 'validation', 'results', 'A5_astro.json')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    json.dump(result, open(dest, 'w'), indent=2)
    print(json.dumps(result, indent=2))
    print('\n-> %s' % os.path.relpath(dest, REPO))


if __name__ == '__main__':
    main()
