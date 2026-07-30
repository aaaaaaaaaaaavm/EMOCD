"""
VOLLEY | Independent magnetostatic verification of the Halbach airgap field.

Cross-checks the analytic decaying-wave model B(y) = B0*exp(-k*y) against
magpylib's analytic cuboid superposition (exact for ironless geometry).

Reproduces (paper Sec. IV-B):
    single-array mid-gap        0.351 T   (analytic: 0.351 T)
    double-sided mid-gap peak   0.694 T   (analytic: 0.702 T)
    winding-region mean |B_y|   0.483 T
    stray field 10/20/50 mm     22.7 / 4.7 / 1.0 mT

CONVENTION WARNING: the Halbach rotation sense is determined EMPIRICALLY by
probing a single array on both faces. Two sign errors were made and caught
this way during development. Do not assert the convention; measure it.

Provenance: model output, not independently re-derived.
"""
import numpy as np
import magpylib as magpy
import math
import json
import os

LAM, NBLK, TH, GAP, DEPTH, BR = 0.048, 4, 0.008, 0.012, 0.09, 1.32
W = LAM / NBLK


def make_array(y_face, step, n_wave=7):
    """step sign selects which face the Halbach strong side points toward."""
    mags = []
    for i in range(n_wave * NBLK):
        x = (i - n_wave * NBLK / 2 + 0.5) * W
        ang = (90 + step * i * 90) % 360
        pol = [BR * np.cos(np.radians(ang)), BR * np.sin(np.radians(ang)), 0]
        y_c = y_face + (TH / 2 if y_face > 0 else -TH / 2)
        mags.append(magpy.magnet.Cuboid(polarization=pol,
                                        dimension=(W, TH, DEPTH),
                                        position=(x, y_c, 0)))
    return magpy.Collection(mags)


def mean_absB(coll, y, xs):
    pts = np.array([[x, y, 0] for x in xs])
    return np.linalg.norm(coll.getB(pts)[:, :2], axis=1).mean()


def main():
    xs = np.linspace(-LAM / 2, LAM / 2, 97)
    out = {}

    # --- convention probe: which rotation sense faces the gap? ---
    probe = {}
    for step in (+1, -1):
        c = make_array(+GAP / 2, step)
        probe[str(step)] = dict(
            gap_side_T=round(float(mean_absB(c, 0.0, xs)), 4),
            back_side_T=round(float(mean_absB(c, GAP / 2 + TH + 0.006, xs)), 4))
    step_strong_down = -1 if probe['-1']['gap_side_T'] > probe['1']['gap_side_T'] else +1
    out['convention_probe'] = probe
    out['step_strong_toward_gap'] = step_strong_down

    # --- analytic wave model for comparison ---
    k = 2 * math.pi / LAM
    B0 = BR * (1 - math.exp(-k * TH)) * (math.sin(math.pi / NBLK) / (math.pi / NBLK))
    out['analytic_B0_surface_T'] = round(B0, 4)
    out['analytic_single_midgap_T'] = round(B0 * math.exp(-k * GAP / 2), 4)

    # --- single array ---
    single = make_array(+GAP / 2, step_strong_down)
    out['magpylib_single_midgap_T'] = round(float(mean_absB(single, 0.0, xs)), 4)

    # --- double-sided pair ---
    both = magpy.Collection([make_array(+GAP / 2, step_strong_down),
                             make_array(-GAP / 2, -step_strong_down)])
    B = both.getB(np.array([[x, 0, 0] for x in xs]))
    out['double_midgap_peak_T'] = round(float(np.linalg.norm(B[:, :2], axis=1).max()), 4)
    out['analytic_double_peak_T'] = round(2 * B0 * math.exp(-k * GAP / 2), 4)

    # --- winding-region spatial means (+/-5 mm) ---
    ys = np.linspace(-0.005, 0.005, 11)
    grid = np.array([[x, y, 0] for y in ys for x in xs])
    Bg = both.getB(grid)
    out['winding_mean_absB_T'] = round(float(np.linalg.norm(Bg[:, :2], axis=1).mean()), 4)
    out['winding_mean_absBy_T'] = round(float(np.abs(Bg[:, 1]).mean()), 4)

    # --- stray field behind array back face (magnetic keep-out) ---
    stray = {}
    for d in (0.010, 0.020, 0.050):
        pts = np.array([[x, GAP / 2 + TH + d, 0] for x in xs])
        stray[f'{int(d * 1e3)}mm_mT'] = round(
            float(np.linalg.norm(both.getB(pts), axis=1).max() * 1e3), 1)
    out['stray_field'] = stray
    return out


if __name__ == '__main__':
    r = main()
    for key, val in r.items():
        print(f"{key:32s} {val}")
    os.makedirs('results', exist_ok=True)
    json.dump(r, open('results/field_verification.json', 'w'), indent=2)
    print("\n-> results/field_verification.json")
