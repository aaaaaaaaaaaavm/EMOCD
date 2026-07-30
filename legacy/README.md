# Legacy scripts: SUPERSEDED, do not cite

These produced earlier results that the current `analysis/` scripts replace.
Kept only so the evolution of the work is traceable.

| File | What it was | Why superseded |
|---|---|---|
| `c3_c4_em.py` | Lumped surface-current motor model + eddy brake | Assumed 0.62 T effective field and omitted the one-half traveling-wave factor; gave 22.4 m/s. Replaced by `analysis/motor_model.py` (winding-resolved, 20.37 m/s). |
| `c1_c2_astro.py` | First lifetime + drift run | Used 15/25 m/s, velocities the machine cannot reach. Replaced by `analysis/astro.py` at 20.37 m/s. |
| `c5_conj.py` | First conjunction attempt | Bug: all satellites initialised co-located with the stage, returning 0.0 km minima. |
| `c5b_conj.py` | Staggered-firing conjunction | Correct method, but run at superseded velocities. See OPEN_PROBLEMS P1, this is the origin of the paper's 45.3 km figure. |
| `c6_c10.py` | Budgets and rollups | Dry mass ~105 kg by top-down estimate; replaced by `analysis/mass_properties.py` (72.3 kg parametric solids). |
| `make_figs.py`, `make_diagrams.py` | Figure set v1 | Plot older numbers. Figures in `paper/figures/` are the current set. |
| `build_ieee.js`, `build_skeleton.js` | docx builders (docx-js) | The paper is now maintained as LaTeX in `paper/paper.tex`. |
| `concept.py`, `banner*.py` | Illustration generators | Presentation assets, not analysis. |
