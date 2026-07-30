# Contributing

VOLLEY is a **design study**, not a software product. It exists to be reproduced,
scrutinised, and (eventually) replaced by measured data. Contributions are welcome on
those terms. The one thing this repository cares about above all is **provenance**: no
generated number may ever pass as a measured one.

## Ground rules (non-negotiable)

These mirror `docs/PROJECT_NOTES.md` and `PROVENANCE.md`. Read both before contributing.

1. **The scripts in `analysis/` are the source of truth, not the paper.** If a script and
   `paper/paper.tex` disagree, the paper is wrong, fix the paper to match the script,
   never the reverse. This principle has already caught four paper errors (see
   `CHANGELOG.md`, P2-01, P2-04).
2. **Do not reconstruct numbers from general knowledge.** If a value's origin cannot be
   traced to a script in `analysis/`, say "not traceable" rather than filling the gap
   plausibly. Several numbers here were wrong for exactly that reason and were only caught
   by re-running the analysis.
3. **Mark verification status on everything you add.** State whether a value is a model
   output, hand-checked, cross-validated against a second method, or measured. Nothing in
   this repository has been validated by hardware, FEA, or third-party review; keep that
   distinction visible.
4. **Log substantive changes** in `CHANGELOG.md` with a cause, a before/after, and a
   source-of-truth reference, in the existing format.

## Reproducing the analysis

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd analysis
python3 verify_field.py && python3 mass_properties.py && python3 motor_model.py && python3 sizing.py && python3 astro.py
```

Results are written to `analysis/results/*.json`. `astro.py` and `motor_model.py` are the
slow ones. Dependency note: `mass_properties.py` produces the sled mass that
`motor_model.py` hard-codes as `M_SLED`, if you change the mass model, update that
constant and re-run the motor model, then the paper.

To run anything under `validation/` you also need the external solvers (gmsh,
scikit-fem, GetDP, CalculiX, ngspice) and LaTeX. `tools/env-setup.sh` installs and
verifies the lot on Debian/Ubuntu.

## Reporting a discrepancy

If a script output does not match a value in the README or the paper, please open an issue
using the **Reproduction discrepancy** template. Include the script, the value it prints,
the value in the document, and your environment (Python, numpy, magpylib versions).

## Scope

By design this repository has **no CI, no test suite, and no build tooling**, it is a
research artifact, and the `analysis/` scripts are self-checking where a genuine
cross-check exists (field model vs magpylib; orbit-averaged decay vs Cowell RK4). Please
do not add software-product scaffolding without discussing it first.

## Citation and licence

Cite via `CITATION.cff`. The work is MIT-licensed (`LICENSE`). Any publication or
presentation that uses it must state that it is a design study at TRL 2-3 with no
experimental validation (`PROVENANCE.md`).
