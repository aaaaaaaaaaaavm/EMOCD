# Validation plan

Independent cross-checks of the claims in `analysis/`. Nothing here has been run yet,
this directory is the specification, not the result.

## Why it exists

`PROVENANCE.md` admits that only two results carry a genuine cross-check: the Halbach
field (analytic vs magpylib) and orbital decay (orbit-averaged vs Cowell RK4). Both are
internal, and the field one is analytic-vs-analytic, so it is not confirmation by a
different physical method (`OPEN_PROBLEMS.md` E2). Everything else is single-sourced.
Each analysis below closes a specific named item.

| # | Analysis | Tool | Closes | Status |
|---|---|---|---|---|
| A1 | Airgap field, 2-D magnetostatic | FEMM 4.2 | E1 (2-D half), E2 (partly) | specified, not run |
| A4 | Sled chassis structural | CalculiX ccx 2.21 | **P5, P8** | **RUN 2026-07-28**: as-drawn plate passes all three bands |
| A5 | Orbital lifetime and seeding | GMAT R2022a | E6, hardens x1.80 | **RUN**, verdict **FAIL** on invariance. See [`../docs/RESULTS.md`](../docs/RESULTS.md) |
| A9 | Decay rate against flown CubeSats (TLE history) | Space-Track + numpy | **E6, against reality rather than another model** | **SPECIFIED, NOT RUN**: CelesTrak and Space-Track blocked by network policy here |
| A6 | Conjunction probability | NASA CARA tools | P1 (properly) | specified, not run |
| A7 | Separation and tip-off | Project Chrono | E7-adjacent | specified, not run |
| A8 | Pulse-power chain | ngspice / PySpice | E17 | **RUN 2026-07-30** as A8-R, at the current operating point |
| A10 | Shot against a realistic bank ESR | `motor_model.shot()` | nothing; **opened P26** | **RUN 2026-07-30**: hard ceiling 65 mohm, five of six bands, one void |
| A11 | Regenerative recovery of sled energy | `motor_model.regen_brake()` | nothing; asks what R5 did not | **bands declared 2026-07-31, not yet run** |

A10 and A11 are cross-checks of the model against its own physics rather than against an
external tool, which is a weaker class of check and is labelled as one. They are here because
both ask a question no external solver was going to be pointed at: whether the bank can source
the shot at all, and whether the sled's energy has to be thrown away.

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
