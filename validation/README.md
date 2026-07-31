# Validation plan

Independent cross-checks of the claims in `analysis/`. **Six of the eleven below have run.**
One of them failed.

## Why it exists

This directory was written when `PROVENANCE.md` could point at only two cross-checks — the
Halbach field (analytic vs magpylib) and orbital decay (orbit-averaged vs Cowell RK4) — both
internal, and the field one analytic-against-analytic, so not confirmation by a different
physical method (`OPEN_PROBLEMS.md` E2).

**That has changed, and not uniformly in the project's favour.** A1 put a meshed PDE solve
against K<sub>t</sub> and agreed to 0.07 %. A4 put CalculiX against the chassis and it passed.
A12 put two independent numerical methods against the array attraction and found the published
value **37 % high**. And **A5 failed**: an independent propagator falsified an invariance claim
that was in the paper's own abstract.

**What has still never happened is a measurement.** Every row below is one model against
another model (E4). Each analysis closes a specific named item.

| # | Analysis | Tool | Closes | Status |
|---|---|---|---|---|
| A1 | Airgap field, 2-D magnetostatic | scikit-fem + gmsh (FEMM substituted) | E1 (2-D half), E2 (partly) | **RUN 2026-07-29**, verdict **PARTIAL**: K<sub>t</sub> agrees to 0.07 %, two bands missed with causes (P20, P21) |
| A4 | Sled chassis structural | CalculiX ccx 2.21 | **P5, P8** | **RUN 2026-07-28**: as-drawn plate passes all three bands |
| A5 | Orbital lifetime and seeding | GMAT R2022a | E6, hardens x1.80 | **RUN**, verdict **FAIL** on invariance. See [`../docs/RESULTS.md`](../docs/RESULTS.md) |
| A9 | Decay rate against flown CubeSats (TLE history) | Space-Track + numpy | **E6, against reality rather than another model** | **SPECIFIED, NOT RUN**: CelesTrak and Space-Track blocked by network policy here |
| A6 | Conjunction probability | scipy 2-D Pc (CARA substituted) | P1 — **not closed** | **RUN 2026-07-31**: P<sub>c</sub> ≤ 3.7e-8 for **any** covariance, two of five bands, three **void** |
| A7 | Separation and tip-off | Project Chrono | E7-adjacent | specified, not run |
| A8 | Pulse-power chain | ngspice / PySpice | E17 | **RUN 2026-07-30** as A8-R, at the current operating point |
| A10 | Shot against a realistic bank ESR | `motor_model.shot()` | nothing; **opened P26** | **RUN 2026-07-30**: hard ceiling 65 mohm, five of six bands, one void |
| A11 | Regenerative recovery of sled energy | `motor_model.regen_brake()` | nothing; asks what R5 did not | **RUN 2026-07-31**: 296.6 J recovered, eight of eight bands |
| A12 | Inter-array attraction, two numerical methods | magpylib + surface Maxwell stress | **P17** | **RUN 2026-07-31**: 2686.6 N adopted, five of five bands |

A10 and A11 are cross-checks of the model against its own physics rather than against an
external tool, which is a weaker class of check and is labelled as one. A12 is stronger than
both: its two methods share only the block model of the magnets. They are here because
both ask a question no external solver was going to be pointed at: whether the bank can source
the shot at all, and whether the sled's energy has to be thrown away.

> **This table was wrong about A1 for a day**, from 2026-07-30 to 2026-07-31: it said "specified,
> not run" while `OPEN_PROBLEMS.md` E1 and `docs/ROADMAP.md` both recorded A1 as run on
> 2026-07-29. The cause is worth keeping, because it is the reason A1 and A5 now carry their
> results inline. **Both run sheets were pure specifications**, with their outcomes living only in
> `OPEN_PROBLEMS.md`, `CHANGELOG.md` and `docs/RESULTS.md`, so a search of `validation/` for
> completed runs found A4, A8 and A10 and missed them. **A run sheet that does not record its own
> result is not a record.** A1 and A5 were written up on 2026-07-31 in the format A4, A8, A10 and
> A11 already used.

A2 (3-D field, end effects) and A3 are not specified here; A1 closes only the 2-D half of
E1, and the 3-D end effects still need a 3-D solver.

## The one rule that makes these tests rather than exercises

**The acceptance band is declared before the analysis runs.** Every run sheet in this
directory states its band up front, and each band is traceable to a current value in
`analysis/results/*.json`. A cross-check whose target is chosen after seeing the answer
proves nothing.

This is not hypothetical here. `docs/FEMM_Run_Sheet.md` was written against ⟨B⟩ ≈ 0.62 T
across the winding gap; the winding-resolved model now computes **0.552 T**, so that
sheet can no longer function as a test and is marked superseded. The replacement sheet
(`analysis/femm/FEMM_RUN_SHEET.md`) had the same problem in its stray-field targets,
they predated the P3 correction, and was fixed on 2026-07-27.

When a band is missed, the outcome is a new P-item, not a quietly widened band.

## Conventions

- Inputs come from what is already committed: `cad/step/gen3/*.step` (Gen3 is current,
  see `cad/README.md`), `cad/parameters.json`,
  `analysis/femm/emocd_cross_section.dxf`. Where a check needs an orbit or a constant, it
  imports from `analysis/*.py` rather than restating the value, see `gmat/build_scripts.py`.
- Outputs land in `validation/results/<analysis>.json` alongside the solver version,
  mesh size, and boundary conditions, the same way `analysis/results/*.json` works.
- A completed run gets a `CHANGELOG.md` entry with cause, before/after, and the P/E item
  it moves.
- `analysis/*.py` stays authoritative until a run closes the relevant item. **Do not
  hand-edit a script to match an FEA result**, record the discrepancy first, decide
  second.

## Licensing

Keep these tools external. CalculiX and Code_Aster are GPL, Elmer is LGPL, and this
repository is MIT, commit input decks and result JSON, never vendored solver code.
Orekit (Apache-2.0), Project Chrono (BSD-3) and pyleecan (Apache-2.0) are permissive.
NASA's CARA tools are MATLAB under a NASA open-source agreement; parts run under Octave,
and the licence should be read before anything is redistributed.
