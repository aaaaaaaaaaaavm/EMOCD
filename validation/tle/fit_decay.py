"""A9 -- fit decay rate from flown CubeSat element-set history, compare against astro.py.

STATUS: WRITTEN, NEVER RUN. CelesTrak and Space-Track are blocked by network policy in the
environment this was written in (403 on CONNECT, logged as a policy denial). Bands are
declared in validation/A9_tle_decay.md ahead of any run. Run it somewhere with ordinary
internet access and a free Space-Track account.

The point of this analysis: every other validation in this project compares one model
against another model. This one compares the model against something that happened.

Usage:
    export SPACETRACK_USER=... SPACETRACK_PASS=...
    python3 validation/tle/fit_decay.py --norad 40025 40044 --out results/A9_tle_decay.json

Method notes that matter:
  * Fit a RATE over a window; never difference two endpoints. A5 established why -- reported
    SMA is osculating and its short-period variation ran 12.2 km peak-to-peak against a
    decay of a few km over the same window. TLE-derived elements add their own noise on top.
  * Mean motion from a TLE is a Brouwer mean element, not osculating, which helps -- but SGP4
    mean elements are not the same as the mean elements astro.py integrates. That mismatch is
    a real limitation and is why the declared band is a factor of two, not a percentage.
  * Objects that manoeuvre must be excluded BEFORE fitting. Differential-drag attitude
    control counts, which rules out much of the Planet fleet despite it being the obvious
    source of 3U objects in this altitude band.
"""
import argparse
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'analysis'))
import astro                                                        # noqa: E402

MU = 3.986004418e14
SPACETRACK = "https://www.space-track.org"


def fetch_history(norad, user, password):
    """Element-set history for one object. Requires a free Space-Track account."""
    import requests
    s = requests.Session()
    r = s.post(f"{SPACETRACK}/ajaxauth/login",
               data={"identity": user, "password": password}, timeout=60)
    r.raise_for_status()
    q = (f"{SPACETRACK}/basicspacedata/query/class/gp_history/NORAD_CAT_ID/{norad}"
         f"/orderby/EPOCH%20asc/format/json")
    r = s.get(q, timeout=300)
    r.raise_for_status()
    return r.json()


def sma_series(records):
    """(days_from_first_epoch, semi-major axis in m) from mean motion."""
    import datetime as dt
    out = []
    for rec in records:
        try:
            n_rev_day = float(rec["MEAN_MOTION"])
            epoch = dt.datetime.fromisoformat(rec["EPOCH"].replace("Z", "+00:00"))
        except (KeyError, ValueError, TypeError):
            continue
        n = n_rev_day * 2 * math.pi / 86400.0                       # rad/s
        a = (MU / n ** 2) ** (1.0 / 3.0)
        out.append((epoch, a))
    if not out:
        return np.array([]), np.array([])
    out.sort(key=lambda r: r[0])
    t0 = out[0][0]
    days = np.array([(e - t0).total_seconds() / 86400.0 for e, _ in out])
    a = np.array([v for _, v in out])
    return days, a


def drop_manoeuvres(days, a, jump_m=2000.0):
    """Discard samples following any positive SMA jump larger than jump_m.

    Drag only removes energy. A rise beyond noise means a manoeuvre (or a bad element set),
    and either way the object stops being a clean drag measurement from that point on.
    """
    if len(a) < 3:
        return days, a, 0
    da = np.diff(a)
    bad = np.where(da > jump_m)[0]
    if len(bad) == 0:
        return days, a, 0
    cut = bad[0] + 1
    return days[:cut], a[:cut], len(a) - cut


def fit_rate(days, a, window_days=60.0):
    """Least-squares dA/dt over the final window, in m/day. Rate, not endpoints."""
    mask = days >= (days[-1] - window_days)
    if mask.sum() < 5:
        mask = np.ones_like(days, dtype=bool)
    p, res = np.polyfit(days[mask], a[mask], 1, full=True)[:2]
    slope = p[0]
    pred = np.polyval(p, days[mask])
    rms = float(np.sqrt(np.mean((a[mask] - pred) ** 2)))
    return slope, rms, int(mask.sum())


def model_rate(alt_m, bc, days=30.0):
    """astro.py's decay rate at the same altitude, in m/day, for comparison.

    LIMITATION, stated rather than hidden: cowell_sma_after() calls rho() without a density
    scale, so this comparison runs at astro.py's mean-activity atmosphere regardless of what
    the object's decay window actually experienced. Matching real F10.7 would need a scale
    argument threading through the Cowell path, which astro.py does not have. Until it does,
    an object that decayed near solar maximum will look like a model failure when it is
    partly an activity mismatch -- record it, do not silently correct for it.
    """
    a0 = astro.RE + alt_m
    a1 = astro.cowell_sma_after(days, alt_m=alt_m, BC=bc)
    return (a1 - a0) / days


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--norad", nargs="+", required=True, type=int)
    ap.add_argument("--bc", type=float, default=61.0, help="kg/m^2, astro.py nominal")
    ap.add_argument("--window", type=float, default=60.0, help="fit window, days")
    ap.add_argument("--out", default="results/A9_tle_decay.json")
    args = ap.parse_args()

    user, pw = os.environ.get("SPACETRACK_USER"), os.environ.get("SPACETRACK_PASS")
    if not (user and pw):
        sys.exit("Set SPACETRACK_USER and SPACETRACK_PASS (free account).")

    objects, ratios = [], []
    for norad in args.norad:
        recs = fetch_history(norad, user, pw)
        days, a = sma_series(recs)
        if len(a) < 10:
            objects.append(dict(norad=norad, status="insufficient history"))
            continue
        days, a, dropped = drop_manoeuvres(days, a)
        if len(a) < 10:
            objects.append(dict(norad=norad, status="excluded: manoeuvres"))
            continue
        fitted, rms, n = fit_rate(days, a, args.window)
        a_mean = float(np.mean(a[days >= days[-1] - args.window]))
        modelled = model_rate(a_mean - astro.RE, args.bc)
        ratio = modelled / fitted if fitted else float("nan")
        ratios.append(ratio)
        objects.append(dict(
            norad=norad, status="fitted", samples=n, samples_dropped=dropped,
            mean_alt_km=round((a_mean - astro.RE) / 1e3, 1),
            fitted_m_per_day=round(fitted, 1), residual_rms_m=round(rms, 1),
            model_m_per_day=round(modelled, 1), ratio_model_over_flown=round(ratio, 3)))

    fitted_only = [r for r in ratios if not math.isnan(r)]
    median = float(np.median(fitted_only)) if fitted_only else None
    within_factor2 = [abs(math.log(abs(r), 2)) <= 1 for r in fitted_only] if fitted_only else []
    signs = {("model faster" if r > 1 else "model slower") for r in fitted_only}

    res = dict(
        analysis="A9", tool="Space-Track gp_history + numpy least squares",
        bands_declared_in="validation/A9_tle_decay.md",
        objects=objects,
        median_ratio=round(median, 3) if median else None,
        median_within_40pct=(abs(median - 1.0) <= 0.40) if median else None,
        all_within_factor_2=all(within_factor2) if within_factor2 else None,
        sign_consistent=(len(signs) == 1),
        sign_note=("error changes sign across the set -- wrong profile shape, not a "
                   "calibration offset; see P16" if len(signs) > 1 else "consistent sign"),
        verdict=None)
    ok = (res["median_within_40pct"] and res["all_within_factor_2"])
    res["verdict"] = ("PASS" if ok else
                      "FAIL -- open a P-item; do not edit analysis/astro.py")

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    json.dump(res, open(args.out, "w"), indent=2)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
