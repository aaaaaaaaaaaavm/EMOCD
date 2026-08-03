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
pressure B_face^2/(2*mu0) at a mean face field, times the area. M2 replaces that one-point footprint estimate with a spatial stress integral and extends
the plane beyond the magnet footprint so fringe stress is included. The difference therefore
contains both field non-uniformity and the omitted fringe contribution; it is not a pure
Jensen term.

Run:  python3 validation/magpylib/maxwell_surface_force.py

Bands and the adoption rule are declared in validation/A12_inter_array_force.md, committed
before this file was written.
"""
import hashlib
import json
import math
import platform
import os
import sys
from pathlib import Path

import magpylib as magpy
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from analysis.motor_model import build_field, DEPTH, GAP, LAM, SLED_ACTIVE_LEN

MU0 = 4e-7 * math.pi

# The stress plane. It spans the ACTIVE overlap of the two arrays, which is the same
# footprint sizing.py's analytic form uses: the 340 mm array length by the 90 mm depth.
# It sits at y = 0, midway between the two faces, where neither array's block corners are
# close enough to make the field singular.
X_SPAN = 0.60  # extended beyond the 340 mm footprint for fringe-stress convergence
Z_SPAN = 0.22  # extended beyond the 90 mm footprint

# Grid resolutions, coarse to fine. Band 5 asks that halving the spacing move the answer
# by under 1 %, so the sequence has to include a halving.
GRIDS = [(100, 37), (200, 73), (400, 147), (800, 293)]
PLANE_EXTENTS = [(0.34, 0.09), (0.45, 0.15), (0.60, 0.22),
                 (0.80, 0.30), (1.00, 0.40)]


def surface_force(nx, nz, y=0.0, x_span=None, z_span=None):
    """Maxwell stress on the mid-gap plane, integrated by the midpoint rule.

    The midpoint grid is refined in both directions. The finite array is not periodic
    over this extended plane, so no integer-wavelength claim is made.
    """
    field = build_field()
    x_span = X_SPAN if x_span is None else x_span
    z_span = Z_SPAN if z_span is None else z_span
    xs = (np.arange(nx) + 0.5) / nx * x_span - x_span / 2
    zs = (np.arange(nz) + 0.5) / nz * z_span - z_span / 2
    X, Z = np.meshgrid(xs, zs, indexing='ij')
    pts = np.stack([X.ravel(), np.full(X.size, y), Z.ravel()], axis=1)
    B = field.getB(pts)
    Bx, By, Bz = B[:, 0], B[:, 1], B[:, 2]
    # Traction normal to the plane, y-component of the Maxwell stress tensor.
    t_y = (By * By - Bx * Bx - Bz * Bz) / (2 * MU0)
    dA = (x_span / nx) * (z_span / nz)
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

    print("\nplane-extent convergence at approximately 1 mm spacing:")
    extent_rows = []
    for x_span, z_span in PLANE_EXTENTS:
        nx, nz = round(x_span / 0.001), round(z_span / 0.001)
        extent_force, _, _ = surface_force(nx, nz, x_span=x_span, z_span=z_span)
        extent_rows.append(dict(x_span_m=x_span, z_span_m=z_span, nx=nx, nz=nz,
                                F_N=abs(extent_force)))
        print(f"  {x_span*1e3:4.0f} x {z_span*1e3:3.0f} mm  {abs(extent_force):8.2f} N")
    extent_conv_pct = abs(extent_rows[-1]['F_N'] - extent_rows[-2]['F_N']) / extent_rows[-1]['F_N'] * 100
    print(f"  largest two extents differ by {extent_conv_pct:.4f} %")

    out = dict(analysis="A12", method="M2, Maxwell stress integrated over the mid-gap plane",
               software=dict(python=platform.python_version(), numpy=np.__version__,
                             numpy_license="BSD-3-Clause", magpylib=magpy.__version__,
                             magpylib_license="BSD-3-Clause",
                             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                             motor_model_sha256=hashlib.sha256(
                                 (Path(__file__).resolve().parents[2] / "analysis" / "motor_model.py").read_bytes()
                             ).hexdigest()),
               solver_settings=dict(integration="midpoint rule", grids=GRIDS,
                                    plane_extents=PLANE_EXTENTS, extent_spacing_m=0.001,
                                    convergence_comparison="finest grid and largest plane extents"),
               plane=dict(x_span_m=X_SPAN, z_span_m=Z_SPAN, y_m=0.0),
               grids=rows, F_N=finest['F_N'],
               grid_convergence_pct=round(conv_pct, 3),
               plane_extent_sweep=extent_rows,
               plane_extent_convergence_pct=round(extent_conv_pct, 6),
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
