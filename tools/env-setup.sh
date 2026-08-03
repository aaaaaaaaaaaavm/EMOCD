#!/usr/bin/env bash
# Reconstruct the full toolchain this repository's validation scripts need.
#
# Every analysis in analysis/ runs on numpy/scipy/matplotlib alone. This script is for
# the validation layer, which needs external solvers:
#
#   validation/fem/          scikit-fem + gmsh  (A1 magnetostatic FEM, meshing)
#   validation/getdp/        getdp              (independent FE cross-check)
#   validation/fea/          calculix-ccx       (structural)
#   validation/circuit/      ngspice            (drive electronics)
#   validation/field/        magpylib           (superposition cross-check)
#   paper/                   texlive            (manuscript build)
#
# Safe to re-run. Intended as the setup script for a fresh container, but it is an
# ordinary shell script and works anywhere Debian/Ubuntu apt is available.

set -euo pipefail

# Setup scripts often run as root, where sudo may not be installed at all.
if [ "$(id -u)" -eq 0 ]; then SUDO=""; else SUDO="sudo"; fi

echo "==> apt index"
# Containers ship a stale index; installing texlive against it 404s on the first
# package fetch. Always refresh before installing.
$SUDO apt-get update -qq

echo "==> solvers"
$SUDO apt-get install -y --no-install-recommends \
    getdp \
    calculix-ccx \
    ngspice

echo "==> LaTeX"
# -latex-extra is deliberately NOT installed. Nothing in paper/ uses it, and it pulls a
# mesa/ruby dependency chain that fails to configure in a minimal container.
$SUDO apt-get install -y --no-install-recommends \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-fonts-recommended \
    lmodern \
    poppler-utils

echo "==> python"
pip install --quiet --upgrade \
    -r "$(dirname "$0")/../requirements.txt" \
    scipy \
    scikit-fem \
    gmsh

echo "==> optional: history tooling"
pip install --quiet git-filter-repo || echo "    (skipped -- only needed to rewrite git history)"

echo
echo "==> verify"
fail=0
for c in getdp ccx ngspice gmsh pdflatex pdfinfo; do
    if command -v "$c" >/dev/null; then
        printf '    %-10s ok\n' "$c"
    else
        printf '    %-10s MISSING\n' "$c"; fail=1
    fi
done
python3 - <<'PY' || fail=1
import importlib, sys
bad = []
for m in ("numpy", "scipy", "matplotlib", "magpylib", "skfem", "gmsh"):
    try:
        mod = importlib.import_module(m)
        print(f"    {m:<10} {getattr(mod, '__version__', 'ok')}")
    except Exception:
        print(f"    {m:<10} MISSING"); bad.append(m)
sys.exit(1 if bad else 0)
PY

if [ "$fail" -ne 0 ]; then
    echo
    echo "Setup incomplete -- see MISSING above."
    exit 1
fi

echo
echo "Toolchain ready. Sanity check:  python3 analysis/motor_model.py"
