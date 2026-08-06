"""P3 / P21 / P34: how far-field stray depends on modelled array length, and where 61 mT ends.

P3 records that verify_field.py reproduces 22.7 mT at 10 mm exactly but gives 4.3 and 0.4 mT at
20 and 50 mm against the paper's 4.7 and 1.0, and attributes it to sensitivity to modelled array
length. P21 records that a 2-D model cannot test the far field at all. A14 then found the decay
behind the array is exponential only to about 40 mm, after which an edge-effect tail dominates --
which is exactly the regime both items are about.

Nothing here needs a mesh. magpylib's Cuboid is an EXACT analytic solution for a uniformly
magnetised block, so the finite-array field is already three-dimensional and correct; what was
never done is checking how the answer moves with the number of wavelengths modelled.

motor_model.build_field(n_wave) defaults to 7 wavelengths = 336 mm. The CAD array
(cad/parameters.json, halbach_array_length) is 340 mm, so 7.083 wavelengths.

Run:  python3 analysis/far_field_sensitivity.py
"""
import json
import math
import os

import numpy as np

import motor_model as mm

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
CAD_ARRAY_LEN = 0.340
B_EARTH = 45e-6
MAG_FULL_SCALE = 100e-6
PAYLOAD_NEAR, PAYLOAD_FAR = 0.020, 0.120        # CAD z of the payload envelope


def peak_at(field, z, nx=240):
    xs = np.linspace(0, mm.LAM, nx, endpoint=False)
    pts = np.stack([xs, np.full(nx, z), np.zeros(nx)], axis=1)
    return float(np.linalg.norm(field.getB(pts), axis=1).max())


def main():
    back = mm.GAP / 2 + mm.TH                    # array back face, z = 0.014 m
    stations = [0.010, 0.020, 0.050]             # the three P3 probes, behind the back face
    n_waves = [3, 5, 7, 9, 11, 13, 15]

    sweep = []
    for n in n_waves:
        f = mm.build_field(n_wave=n)
        row = dict(n_wave=n, array_len_mm=n * mm.LAM * 1e3,
                   stray_mT={f'{int(d*1e3)}mm': peak_at(f, back + d) * 1e3 for d in stations})
        sweep.append(row)

    # converged reference: the largest array modelled
    conv = sweep[-1]['stray_mT']
    for row in sweep:
        row['dev_pct'] = {k: 100 * (row['stray_mT'][k] - conv[k]) / conv[k] for k in conv}

    # P34's extent: where does the field fall below the magnetometer comparator?
    f = mm.build_field()
    zs = np.concatenate([np.linspace(0.015, 0.20, 120), np.linspace(0.21, 1.0, 40)])
    prof = [(float(z), peak_at(f, z)) for z in zs]
    below = next((z for z, b in prof if b < MAG_FULL_SCALE), None)
    below_earth = next((z for z, b in prof if b < B_EARTH), None)
    near = peak_at(f, PAYLOAD_NEAR)
    far = peak_at(f, PAYLOAD_FAR)

    res = dict(
        analysis='P3/P21/P34 far-field sensitivity',
        method='magpylib finite-block analytic field; exact in free space, no mesh needed',
        cad_array_length_m=CAD_ARRAY_LEN,
        default_n_wave=7, default_array_length_m=7 * mm.LAM,
        sweep=sweep,
        paper_values_mT={'10mm': 22.7, '20mm': 4.7, '50mm': 1.0},
        payload=dict(near_face_z_m=PAYLOAD_NEAR, near_face_mT=near * 1e3,
                     far_face_z_m=PAYLOAD_FAR, far_face_mT=far * 1e3,
                     z_below_magnetometer_fullscale_m=below,
                     z_below_earth_field_m=below_earth))

    print("Far-field sensitivity to modelled array length\n")
    print(f"  {'n_wave':>7}{'array mm':>10}" + ''.join(f"{k:>12}" for k in conv))
    for row in sweep:
        print(f"  {row['n_wave']:7d}{row['array_len_mm']:10.0f}"
              + ''.join(f"{row['stray_mT'][k]:12.4f}" for k in conv))
    print(f"\n  {'':17}" + ''.join(f"{k+' dev%':>12}" for k in conv))
    for row in sweep:
        print(f"  n={row['n_wave']:<15}" + ''.join(f"{row['dev_pct'][k]:12.2f}" for k in conv))
    print(f"\n  paper: 22.7 / 4.7 / 1.0 mT     model at n=7: "
          f"{sweep[2]['stray_mT']['10mm']:.1f} / {sweep[2]['stray_mT']['20mm']:.1f} / "
          f"{sweep[2]['stray_mT']['50mm']:.2f} mT")
    print(f"\n  P34 extent, from the thrust line:")
    print(f"    payload near face  z = {PAYLOAD_NEAR*1e3:.0f} mm   {near*1e3:8.3f} mT"
          f"   {near/MAG_FULL_SCALE:8.1f}x magnetometer full scale")
    print(f"    payload far face   z = {PAYLOAD_FAR*1e3:.0f} mm  {far*1e3:8.3f} mT"
          f"   {far/MAG_FULL_SCALE:8.1f}x")
    print(f"    below full scale at z = {below*1e3:.0f} mm" if below else
          "    NEVER below magnetometer full scale within 1 m")
    print(f"    below Earth's field at z = {below_earth*1e3:.0f} mm" if below_earth else
          "    NEVER below Earth's field within 1 m")

    path = os.path.join(RESULTS, 'far_field_sensitivity.json')
    with open(path, 'w', encoding='utf-8') as f2:
        json.dump(res, f2, indent=2)
        f2.write('\n')
    print(f"\nwrote {path}")


if __name__ == '__main__':
    main()
