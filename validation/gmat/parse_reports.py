"""
EMOCD | Parse GMAT output into validation/results/A5_astro.json.

Applies the acceptance bands declared in validation/A5_astro_orekit.md BEFORE any run:

    lifetime multiplier      x1.80  +/- 5 %
    invariance across        spread <= 5 %
      low/mean/high
    seeding 10/5/2 m/s       1.4 / 2.8 / 6.9 days +/- 20 %   (not computed here --
                                                              seeding needs its own run)

Absolute lifetimes are recorded but are NOT a pass/fail criterion (OPEN_PROBLEMS E6).

Usage:  python3 parse_reports.py [--invocation '<the exact command that ran GMAT>']
"""
import argparse
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
OUTDIR = os.path.join(HERE, 'output')

MULTIPLIER_BAND_PCT = 5.0
INVARIANCE_SPREAD_PCT = 5.0


def read_report(path):
    """GMAT ReportFile: one header line of column names, then whitespace columns."""
    rows = []
    with open(path) as fh:
        header = fh.readline().split()
        for line in fh:
            parts = line.split()
            if len(parts) == len(header):
                try:
                    rows.append([float(p) for p in parts])
                except ValueError:
                    continue
    if not rows:
        raise SystemExit('%s: no numeric rows' % path)
    return header, rows


def decay_days(path):
    """Elapsed days at the last reported step -- the propagation stops at 120 km."""
    header, rows = read_report(path)
    try:
        col = next(i for i, h in enumerate(header) if 'ElapsedDays' in h)
    except StopIteration:
        raise SystemExit('%s: no ElapsedDays column (headers: %s)' % (path, header))
    return rows[-1][col]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--invocation', default='',
                    help='the exact GMAT command that produced this output')
    args = ap.parse_args()

    ref = json.load(open(os.path.join(REPO, 'analysis', 'results', 'astro_results.json')))
    ref_multiplier = ref['lifetime']['mean']['multiplier']

    result = {
        'analysis': 'A5',
        'tool': 'GMAT',
        'invocation': args.invocation,
        'bands_declared_in': 'validation/A5_astro_orekit.md',
        'reference': {
            'multiplier': ref_multiplier,
            'source': 'analysis/results/astro_results.json',
        },
        'levels': {},
        'ephemerides': sorted(
            os.path.relpath(p, REPO)
            for p in glob.glob(os.path.join(OUTDIR, 'ephemeris', '*.oem'))
        ),
        'notes': [
            'Absolute lifetimes are recorded, not judged: astro.py uses a static '
            'exponential atmosphere and GMAT uses MSIS-class, so they are expected to '
            'differ. E6 defends the ratio.',
            'Solar activity is parameterised by F10.7 here and by a density scale factor '
            'in astro.py; the two are not equivalent. See validation/gmat/README.md.',
        ],
    }

    multipliers = []
    for tag in ('low', 'mean', 'high'):
        base = os.path.join(OUTDIR, 'lifetime_%s_baseline.txt' % tag)
        boost = os.path.join(OUTDIR, 'lifetime_%s_boosted.txt' % tag)
        if not (os.path.exists(base) and os.path.exists(boost)):
            result['levels'][tag] = {'status': 'not run'}
            continue
        d0, d1 = decay_days(base), decay_days(boost)
        mult = d1 / d0 if d0 else None
        entry = {
            'baseline_days': round(d0, 2),
            'boosted_days': round(d1, 2),
            'baseline_years': round(d0 / 365.25, 3),
            'boosted_years': round(d1 / 365.25, 3),
            'multiplier': round(mult, 4) if mult else None,
        }
        if mult:
            dev = 100.0 * (mult - ref_multiplier) / ref_multiplier
            entry['deviation_pct'] = round(dev, 2)
            entry['within_band'] = abs(dev) <= MULTIPLIER_BAND_PCT
            multipliers.append(mult)
        result['levels'][tag] = entry

    if len(multipliers) >= 2:
        spread = 100.0 * (max(multipliers) - min(multipliers)) / (sum(multipliers) / len(multipliers))
        result['invariance'] = {
            'spread_pct': round(spread, 2),
            'within_band': spread <= INVARIANCE_SPREAD_PCT,
        }

    checks = [v.get('within_band') for v in result['levels'].values() if 'within_band' in v]
    if not checks:
        result['verdict'] = 'not run'
    elif all(checks) and result.get('invariance', {}).get('within_band', True):
        result['verdict'] = 'pass'
    else:
        result['verdict'] = 'FAIL -- open a P-item; do not edit analysis/astro.py'

    dest = os.path.join(REPO, 'validation', 'results', 'A5_astro.json')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    json.dump(result, open(dest, 'w'), indent=2)
    print(json.dumps(result, indent=2))
    print('\n-> %s' % os.path.relpath(dest, REPO))
    if result['verdict'].startswith('FAIL'):
        sys.exit(1)


if __name__ == '__main__':
    main()
