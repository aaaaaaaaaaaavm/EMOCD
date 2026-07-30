---
name: Reproduction discrepancy
about: A script output does not match a value in the README or the paper
title: "[discrepancy] <quantity>, script vs document"
labels: discrepancy
---

<!-- The scripts in analysis/ are the source of truth. If a script and the paper
     disagree, the paper is assumed wrong. See CONTRIBUTING.md and PROVENANCE.md. -->

**Quantity**
<!-- e.g. peak current, exit velocity, stray field at 20 mm -->

**Script output**
<!-- Which script, and the value it prints. e.g. motor_model.py -> I_peak = 391.7 A -->

**Document value**
<!-- Where the differing value appears, with section or line. e.g. paper/paper.tex Sec. V-A -->

**Is the document value traceable to any script?**
- [ ] Yes, to: `analysis/<script>.py`
- [ ] No, not traceable (do NOT reconstruct it; flag it)

**Environment**
- OS:
- Python:
- numpy / magpylib:

**Anything else**
<!-- Suspected cause (e.g. superseded operating point), sweep sensitivity, etc. -->
