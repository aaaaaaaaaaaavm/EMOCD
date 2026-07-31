"""M2 for A12: inter-array attraction by Maxwell stress integrated over a surface.

WHY A SECOND METHOD
-------------------
`check_inter_array_force.py` (M1) uses `magpylib.getFT()`, which meshes each magnet block
and integrates the field gradient over the block volume. Refining that mesh only shows the
method agreeing with itself. P17 needs evidence that the 36.7 % gap against the analytic
formula is real, and for that the second number has to come from different mathematics.

This is that second number. It integrates the Maxwell stress tensor over a PLANE in the
airgap rather than over the magnet volumes:

    F_y = (1/(2*mu0)) * integral over S of (B_y^2 - B_x^2 - B_z^2) dA

with S the mid-gap plane and y the gap-normal direction. The field never gets
differentiated; the blocks never get meshed. If M1 and M2 land together, the two share only
the block model of the magnets, which is the thing they are both allowed to assume.

WHAT IT IS ALSO A DIRECT TEST OF
--------------------------------
The analytic form in `sizing.py` is this same integral evaluated at ONE point: a uniform
pressure B_face^2/(2*mu0) at a mean face field, times the area. So M2 is the analytic
formula with the approximation removed, and the difference between them is exactly the
Jensen term P17 blames -- mean(B^2) >= mean(B)^2 for any non-uniform field.

Run:  python3 validation/magpylib/maxwell_surface_force.py

Bands and the adoption rule are declared in validation/A12_inter_array_force.md, committed
before this file was written.
"""
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from analysis.motor_model import build_field, DEPTH, GAP, LAM, SLED_ACTIVE_LEN

MU0 = 4e-7 * math.pi

# The stress plane. It spans the ACTIVE overlap of the two arrays, which is the same
# footprint sizing.py's analytic form uses: the 340 mm array length by the 90 mm depth.
# It sits at y = 0, midway between the two faces, where neither array's block corners are
# close enough to make the field singular.
X_SPAN = SLED_ACTIVE_LEN
Z_SPAN = DEPTH

# Grid resolutions, coarse to fine. Band 5 asks that halving the spacing move the answer
# by under 1 %, so the sequence has to include a halving.
GRIDS = [(96, 12), (192, 24), (384, 48), (768, 96)]


def surface_force(nx, nz, y=0.0):
    """Maxwell stress on the mid-gap plane, integrated by the midpoint rule.

    The field is periodic in x with wavelength LAM, so an integer number of samples per
    wavelength avoids aliasing the harmonics that carry the non-uniformity. nx is chosen
    as a multiple of the wavelength count for that reason.
    """
    field = build_field()
    xs = (np.arange(nx) + 0.5) / nx * X_SPAN - X_SPAN / 2
    zs = (np.arange(nz) + 0.5) / nz * Z_SPAN - Z_SPAN / 2
    X, Z = np.meshgrid(xs, zs, indexing='ij')
    pts = np.stack([X.ravel(), np.full(X.size, y), Z.ravel()], axis=1)
    B = field.getB(pts)
    Bx, By, Bz = B[:, 0], B[:, 1], B[:, 2]
    # Traction normal to the plane, y-component of the Maxwell stress tensor.
    t_y = (By * By - Bx * Bx - Bz * Bz) / (2 * MU0)
    dA = (X_SPAN / nx) * (Z_SPAN / nz)
    return float(np.sum(t_y) * dA), float(np.mean(np.abs(By))), float(np.mean(By * By))


def main():
    print(f"M2: Maxwell stress over the mid-gap plane, {X_SPAN*1e3:.0f} x {Z_SPAN*1e3:.0f} mm")
    print(f"    gap {GAP*1e3:.0f} mm, wavelength {LAM*1e3:.0f} mm, "
          f"{X_SPAN/LAM:.2f} wavelengths spanned\n")
    print(f"{'grid (nx,nz)':>16} {'samples':>9} {'F_y (N)':>12} {'delta':>10}")
    prev, force = None, None
    rows = []
    for nx, nz in GRIDS:
        force, mean_absBy, mean_By2 = surface_force(nx, nz)
        d = "" if prev is None else f"{force - prev:+10.2f}"
        print(f"{str((nx,nz)):>16} {nx*nz:>9} {abs(force):12.1f} {d:>10}")
        rows.append(dict(nx=nx, nz=nz, F_N=abs(force),
                         mean_abs_By_T=mean_absBy, mean_By2_T2=mean_By2))
        prev = force

    finest = rows[-1]
    coarser = rows[-2]
    conv_pct = abs(finest['F_N'] - coarser['F_N']) / finest['F_N'] * 100

    # The Jensen term, computed rather than asserted: the analytic form uses the square of
    # the mean field where the integral needs the mean of the square.
    mean_absBy = finest['mean_abs_By_T']
    mean_By2 = finest['mean_By2_T2']
    jensen = mean_By2 / (mean_absBy ** 2)

    print(f"\ngrid convergence, finest vs previous : {conv_pct:.2f} %")
    print(f"mean |B_y| on the plane              : {mean_absBy:.4f} T")
    print(f"mean B_y^2 on the plane              : {mean_By2:.4f} T^2")
    print(f"  square of the mean                 : {mean_absBy**2:.4f} T^2")
    print(f"  Jensen ratio mean(B^2)/mean(B)^2   : {jensen:.4f}")
    print("  (>1 for any non-uniform field, which is why a one-point")
    print("   evaluation at a mean field cannot be right)")

    out = dict(analysis="A12", method="M2, Maxwell stress integrated over the mid-gap plane",
               plane=dict(x_span_m=X_SPAN, z_span_m=Z_SPAN, y_m=0.0),
               grids=rows, F_N=finest['F_N'],
               grid_convergence_pct=round(conv_pct, 3),
               jensen_ratio=round(jensen, 4),
               bands_declared_in="validation/A12_inter_array_force.md")
    dest = Path(__file__).resolve().parents[1] / 'results' / 'A12_inter_array_force.json'
    os.makedirs(dest.parent, exist_ok=True)
    with open(dest, 'w') as fh:
        json.dump(out, fh, indent=2)
        fh.write("\n")
    print(f"\n-> {dest.relative_to(Path(__file__).resolve().parents[2])}")


if __name__ == "__main__":
    main()
