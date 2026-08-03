"""Independent check of the inter-array Halbach attraction used as the A4 FEA load.

`analysis/sizing.py::inter_array_attraction()` computes the force between the two
opposed Halbach faces from a flat-plate Maxwell-stress formula: a uniform pressure
B_face**2 / (2*mu0) at a mean face field of 0.55 T, applied over the 340 x 90 mm
footprint. That gives 3672 N, and that number was the applied load in the CalculiX
A4 structural run (`validation/results/A4_sled_structural.json`). It had never been
checked against anything.

This script recomputes the same force with `magpylib.getFT()`, which meshes each
magnet block and integrates the field gradient in three dimensions, driven by the
repo's own array geometry (`analysis/motor_model.py::build_field()`) so the two
methods cannot disagree about the magnets themselves.

Run:  python3 validation/magpylib/check_inter_array_force.py

Note on interpretation: mean(B**2) >= mean(B)**2 means a one-point form at the true
mean field underestimates. The superseded form was high because its assumed 0.55 T was
not the mean normal field, not because of Jensen's inequality.

Note on 3672 vs 3680 N: `inter_array_attraction()` rounds its pressure to 120.0 kPa
before reporting, and `validation/fea/build_deck.py` multiplied that rounded pressure
by the 0.0306 m2 footprint to get the 3672 N it applied. Carrying full precision gives
3683 N. The 11 N spread is irrelevant beside the 995 N discrepancy this script finds,
but it is recorded so the two numbers in the repo are traceable to each other.
"""

import hashlib
import json
import os
import platform
import sys
from pathlib import Path

import numpy as np
import magpylib as magpy

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from analysis.motor_model import build_field

# The superseded flat-plate value, kept as a literal on purpose. sizing.py no longer
# computes it: A12 adopted the numerical force on 2026-07-31, so calling
# inter_array_attraction() here would compare this method against itself.
ANALYTIC_N = 0.550 ** 2 / (2 * 4e-7 * 3.141592653589793) * 0.34 * 0.09

# Finite-difference step for the gradient. magpylib recommends
# 1e-5 * characteristic system size; blocks are ~10 mm, so 1e-7.
# Verified insensitive from 1e-5 to 1e-8 (identical to 0.1 N).
EPS = 1e-7

MESHES = [(2, 2, 2), (4, 4, 4), (6, 6, 6), (8, 8, 8), (10, 10, 10),
          (12, 12, 12), (14, 14, 14)]


def main():
    print(f"superseded flat-plate form: {ANALYTIC_N:.0f} N")
    print("  (0.55 T assumed at the face, one point, times 340 x 90 mm)")
    print()

    system = build_field()
    top, bottom = system.children
    targets = list(top.children)

    print("magpylib getFT, force on the upper array from the lower array:")
    previous = None
    force = None
    for mesh in MESHES:
        for magnet in targets:
            magnet.meshing = mesh
        F, _ = magpy.getFT(bottom, targets, eps=EPS)
        force = abs(np.sum(F, axis=0)[1])
        delta = "" if previous is None else f"   delta {force - previous:+7.1f}"
        print(f"  mesh {str(mesh):12} {force:8.1f} N{delta}")
        previous = force

    ratio = force / ANALYTIC_N
    print()
    print(f"finest mesh / analytic    : {ratio:.3f}")
    print(f"analytic is high by       : {1 / ratio - 1:.1%}")
    print()
    print("A12 adopted this value on 2026-07-31. The cause is NOT the Jensen term P17")
    print("blamed -- that acts the other way. See validation/A12_inter_array_force.md.")

    root = Path(__file__).resolve().parents[2]
    out = dict(
        analysis="A12", method="M1, Magpylib getFT volume/field-gradient force",
        software=dict(python=platform.python_version(), numpy=np.__version__,
                      numpy_license="BSD-3-Clause", magpylib=magpy.__version__,
                      magpylib_license="BSD-3-Clause",
                      source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      motor_model_sha256=hashlib.sha256(
                          (root / "analysis" / "motor_model.py").read_bytes()).hexdigest()),
        solver_settings=dict(finite_difference_step_m=EPS, meshes=MESHES),
        F_N=float(force), superseded_flat_plate_N=ANALYTIC_N,
        bands_declared_in="validation/A12_inter_array_force.md")
    dest = root / "validation" / "results" / "A12_inter_array_force_M1.json"
    os.makedirs(dest.parent, exist_ok=True)
    with open(dest, "w") as fh:
        json.dump(out, fh, indent=2)
        fh.write("\n")
    print(f"-> {dest.relative_to(root)}")


if __name__ == "__main__":
    main()
