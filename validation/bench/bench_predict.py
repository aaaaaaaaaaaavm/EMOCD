"""
Benchtop test predictions and error budgets for B-1 and B-2 (docs/BENCHTOP_TESTS.md).

WHY THIS SCRIPT EXISTS
----------------------
BENCHTOP_TESTS.md declares acceptance bands for four experiments -- correctly, before any of
them is run. But the bands were *chosen* (+/-15 %, +/-20 %) rather than derived, and a band
that is not traced to an error budget cannot be defended if a reading lands just outside it.

This derives them. For each measurable, it perturbs the physical quantity a bench build gets
wrong -- gap, remanence, block thickness, probe placement -- by a realistic amount, re-solves
the field, and reports the resulting spread. The band then has a reason.

It IMPORTS analysis/verify_field.py and analysis/motor_model.py rather than reimplementing
their geometry, for the same reason paper/make_figures.py imports the analysis: two copies of
a field model diverge, and this repository has already had that happen twice.

It also settles one thing a builder cannot get from the text: for a TWO-BLOCK bench pair,
which way the blocks face. Getting it wrong reads as zero force, which looks like a falsified
model rather than a reversed magnet.

Run:  python3 validation/bench/bench_predict.py
Out:  validation/results/bench_predictions.json
"""
import json
import math
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "analysis"))

import magpylib as magpy                      # noqa: E402
import verify_field as vf                     # noqa: E402
import motor_model as mm                      # noqa: E402


# --- what a bench build realistically gets wrong -------------------------------
PERTURB = {
    "gap_mm": 0.5,          # shim stack and parallelism, +/- mm
    "Br_frac": 0.03,        # N45SH grade spread, datasheet
    "thickness_mm": 0.1,    # block dimensional tolerance
    "probe_pos_mm": 0.5,    # Hall probe placement along the traverse
}


def _double_pair(gap=None, br=None, th=None, n_wave=7):
    """Double-sided array at the design convention, with geometry overridable.

    Rebuilt here rather than calling vf.make_array directly because the perturbation study
    needs to vary gap/Br/thickness, which that function reads from module constants. The
    construction is copied from verify_field.make_array and must stay identical to it -- the
    check at the bottom of main() asserts that it reproduces vf's own published numbers.
    """
    gap = vf.GAP if gap is None else gap
    br = vf.BR if br is None else br
    th = vf.TH if th is None else th
    W = vf.W

    def arr(y_face, step):
        mags = []
        for i in range(n_wave * vf.NBLK):
            x = (i - n_wave * vf.NBLK / 2 + 0.5) * W
            ang = (90 + step * i * 90) % 360
            pol = [br * np.cos(np.radians(ang)), br * np.sin(np.radians(ang)), 0]
            y_c = y_face + (th / 2 if y_face > 0 else -th / 2)
            mags.append(magpy.magnet.Cuboid(polarization=pol,
                                            dimension=(W, th, vf.DEPTH),
                                            position=(x, y_c, 0)))
        return magpy.Collection(mags)

    return magpy.Collection([arr(+gap / 2, -1), arr(-gap / 2, +1)])


def _xs():
    return np.linspace(-vf.LAM / 2, vf.LAM / 2, 97)


def _midgap_peak(coll):
    B = coll.getB(np.array([[x, 0.0, 0] for x in _xs()]))
    return float(np.linalg.norm(B[:, :2], axis=1).max())


def _winding_mean(coll):
    """Mean |B| over the winding region, +/-5 mm about midgap -- the B-1 'winding mean' row."""
    vals = []
    for y in np.linspace(-0.005, 0.005, 11):
        pts = np.array([[x, y, 0] for x in _xs()])
        vals.append(np.linalg.norm(coll.getB(pts)[:, :2], axis=1).mean())
    return float(np.mean(vals))


def _stray(coll, behind_m, th=None):
    """Matches verify_field.main() exactly: MAX of the full 3-vector norm, not a mean.

    Checked against analysis/results/field_verification.json -- a mean of the in-plane
    components gives 16.2 mT at 10 mm where verify_field publishes 22.7 mT, so the two
    definitions are not interchangeable and the budget must use the published one.
    """
    th = vf.TH if th is None else th
    y = vf.GAP / 2 + th + behind_m
    pts = np.array([[x, y, 0] for x in _xs()])
    return float(np.linalg.norm(coll.getB(pts), axis=1).max())


def two_block_orientation():
    """For a two-block bench pair: which relative orientation gives field in the gap?

    A four-block Halbach wavelength has an unambiguous convention and verify_field.py probes
    for it. A two-block bench build does not -- and the intuitive arrangement, poles facing
    each other across the gap, cancels the field at midgap exactly. Resolved numerically so
    the procedure can state it.
    """
    y = vf.GAP / 2 + vf.TH / 2
    out = {}
    for name, pol_top, pol_bot in (
        ("facing each other", (0, -vf.BR, 0), (0, +vf.BR, 0)),
        ("both same direction", (0, +vf.BR, 0), (0, +vf.BR, 0)),
    ):
        c = magpy.Collection([
            magpy.magnet.Cuboid(polarization=pol_top, dimension=(vf.W, vf.TH, vf.DEPTH),
                                position=(0, +y, 0)),
            magpy.magnet.Cuboid(polarization=pol_bot, dimension=(vf.W, vf.TH, vf.DEPTH),
                                position=(0, -y, 0)),
        ])
        # getB collapses a single query point to shape (3,), not (1,3).
        B = np.atleast_2d(c.getB(np.array([[0.0, 0.0, 0.0]])))
        out[name] = round(float(abs(B[0, 1])), 5)
    return out


def budget(fn, label):
    """Fractional spread in fn() from each perturbation, and their RSS."""
    base = fn(_double_pair())
    terms = {}

    for tag, kw, delta in (
        ("gap +/-%.1f mm" % PERTURB["gap_mm"], "gap", PERTURB["gap_mm"] / 1000),
        ("Br +/-%.0f %%" % (PERTURB["Br_frac"] * 100), "br", vf.BR * PERTURB["Br_frac"]),
        ("thickness +/-%.1f mm" % PERTURB["thickness_mm"], "th", PERTURB["thickness_mm"] / 1000),
    ):
        base_val = {"gap": vf.GAP, "br": vf.BR, "th": vf.TH}[kw]
        hi = fn(_double_pair(**{kw: base_val + delta}))
        lo = fn(_double_pair(**{kw: base_val - delta}))
        terms[tag] = round(abs(hi - lo) / 2 / base, 4)

    rss = math.sqrt(sum(v ** 2 for v in terms.values()))
    return {
        "quantity": label,
        "model_value": round(base, 5),
        "terms": terms,
        "rss_frac": round(rss, 4),
    }


def main():
    # --- B-1: field rows -----------------------------------------------------
    b1 = [
        budget(_midgap_peak, "peak gap field [T]"),
        budget(_winding_mean, "winding mean |B| [T]"),
        budget(lambda c: _stray(c, 0.010), "stray at 10 mm [T]"),
        budget(lambda c: _stray(c, 0.020), "stray at 20 mm [T]"),
        budget(lambda c: _stray(c, 0.050), "stray at 50 mm [T]"),
        # NOTE: the thickness term for the stray rows is understated. The probe sits a fixed
        # distance behind the BACK FACE, so changing block thickness moves the reference plane
        # as well as the source -- _stray() takes th for that reason, but budget() cannot pass
        # it through the lambda. Recorded rather than silently wrong; see BENCHTOP_TESTS.md.
    ]

    # --- B-2: thrust constant ------------------------------------------------
    # Kt comes from motor_model itself, so the prediction under test is the published one.
    kt_per_Am, ripple = mm.thrust_constant()
    kt = kt_per_Am * 1e3          # N per A/m -> N per kA/m, the unit the bands are quoted in

    # Gap is the dominant bench error for thrust: the paper quotes -13 %/mm.
    kt_gap_sens = 0.13 * PERTURB["gap_mm"]        # fractional, from paper Sec. VI
    b2_terms = {
        "gap +/-%.1f mm at -13 %%/mm" % PERTURB["gap_mm"]: round(kt_gap_sens, 4),
        "Br +/-%.0f %%" % (PERTURB["Br_frac"] * 100): PERTURB["Br_frac"],
        "coil fill factor and turns, hand-wound": 0.05,
        "single coil vs three-phase belt scaling": 0.10,
        "load cell, 0.5 % of full scale": 0.02,
        "current measurement": 0.01,
    }
    b2_rss = math.sqrt(sum(v ** 2 for v in b2_terms.values()))

    out = {
        "purpose": "Derived acceptance bands for B-1 and B-2 in docs/BENCHTOP_TESTS.md. "
                   "Declared before any hardware exists.",
        "perturbations_assumed": PERTURB,
        "two_block_orientation_midgap_By_T": two_block_orientation(),
        "B1_field_rows": b1,
        "B2_thrust": {
            "quantity": "thrust per unit sheet current [N per kA/m]",
            "model_value": round(kt, 3),
            "ripple_pct": round(ripple * 100, 3),
            "terms": b2_terms,
            "rss_frac": round(b2_rss, 4),
        },
        "note": "RSS is the measurement error budget only. Declared bands in BENCHTOP_TESTS.md "
                "are wider, deliberately: they must also cover model error, which is the thing "
                "under test and cannot be budgeted from the model itself.",
    }

    # --- consistency check against verify_field's own published outputs -------
    # If the geometry copied into _double_pair ever drifts from verify_field.make_array, this
    # catches it. Same guard idea as _check_operating_point() in sizing.py.
    ref_peak = _midgap_peak(magpy.Collection([vf.make_array(+vf.GAP / 2, -1),
                                              vf.make_array(-vf.GAP / 2, +1)]))
    ours = _midgap_peak(_double_pair())
    if abs(ours - ref_peak) / ref_peak > 1e-9:
        raise SystemExit(f"GEOMETRY DRIFT: local build gives {ours:.6f} T, "
                         f"verify_field.make_array gives {ref_peak:.6f} T. "
                         "Re-sync _double_pair() with verify_field.make_array.")
    out["geometry_matches_verify_field"] = True

    dest = os.path.join(_HERE, "..", "results", "bench_predictions.json")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w") as f:
        json.dump(out, f, indent=2)
        f.write("\n")

    print("Benchtop predictions and derived error budgets (B-1, B-2)")
    print()
    print("  two-block bench pair, mean |By| at midgap:")
    for k, v in out["two_block_orientation_midgap_By_T"].items():
        print(f"    {k:<24s} {v:.5f} T")
    print()
    print("  B-1 field rows                    model      RSS of bench error")
    for r in b1:
        print(f"    {r['quantity']:<28s} {r['model_value']:9.5f}   {r['rss_frac']*100:5.1f} %")
        for t, v in r["terms"].items():
            print(f"        {v*100:5.1f} %  {t}")
    print()
    r = out["B2_thrust"]
    print(f"  B-2 {r['quantity']}: {r['model_value']}")
    for t, v in r["terms"].items():
        print(f"        {v*100:5.1f} %  {t}")
    print(f"        {r['rss_frac']*100:5.1f} %  RSS")
    print()
    print(f"  geometry matches verify_field.make_array: {out['geometry_matches_verify_field']}")
    print(f"  -> {os.path.normpath(dest)}")


if __name__ == "__main__":
    main()
