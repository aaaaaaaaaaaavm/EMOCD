# A4: Sled chassis structural (CalculiX or Code_Aster)

> ## RUN 2026-07-28, CalculiX ccx 2.21, structural leg complete
>
> | Band (declared below, before the run) | Result | |
> |---|---|---|
> | Airgap closure ≤ 0.025 mm per plate | **0.0194 mm** (pinned) / 0.0160 (clamped) | pass, 78 % of budget |
> | Von Mises ≤ 587 MPa | **33.7 MPa** | pass, 17x margin |
> | First mode > 200 Hz | **3408 Hz** | pass, 17x |
>
> The plate **as drawn** meets every constraint. It is not strength-driven and only
> moderately stiffness-driven. Full record, mesh, idealisations and caveats:
> [`../validation/results/A4_sled_structural.json`](../validation/results/A4_sled_structural.json);
> decks and logs in [`../validation/fea/`](../validation/fea/).
>
> **This does not close the mass question.** The run answers "does the drawn chassis meet
> the constraint" (yes) rather than "what is the lightest chassis that does". Uniform
> thinning is nearly worthless, deflection goes as 1/t³, so the budget is spent at ~5.5 mm
> for a 0.30 kg saving. Real reduction needs a rib-stiffened redesign, which nothing has
> evaluated. **The decision rule's ≥ 6.80 kg branch therefore stands: 16.53 m/s.**

**Closes:** `OPEN_PROBLEMS.md` **P5** (sled mass 4.86 vs 7.50 kg) and **P8** (exit
velocity 20.37 vs provisional 17.88 m/s).

This is the highest-leverage analysis in the repository. Everything headline,
velocity, efficiency, recoil, lifetime multiplier, hangs off the sled mass, and that
mass currently has two irreconcilable estimates, neither of them FEA'd.

## The question, stated so it can be answered

Not "what does the sled weigh" but: **what is the lightest chassis that holds the airgap
open to ±0.05 mm under load?** Mass is the output of that constraint, not an input.

## Inputs (all committed)

- Geometry: `cad/step/gen3/EMOCD_Sled_Gen3.step`, **Gen3, not an earlier generation.**
  Gen3 is the dimensionally corrected sled: 488x 140 mm chassis, where Gen2 was 360x 110.
  Meshing the Gen2 sled would size a chassis that no longer exists
- Dimensions and material: `cad/parameters.json`, sled group (6 mm Ti-6Al-4V chassis,
  flagged `PROVISIONAL_PENDING_FEA`)
- Loads, from `analysis/results/sizing.json`:
  - Inter-array attraction **3.68 kN** (`inter_array.force_kN`), the sizing case
    > **Superseded 2026-07-31 by A12: the real force is 2.69 kN and this run was 37 % heavy.**
    > A4's results are conservative and its verdict stands. **It is not re-run** — repeating a
    > passing structural analysis at a lighter load replaces a real result with a weaker one.
    > The bands below are left exactly as declared.
  - Axial acceleration **16.3 g** at the script operating point (12.5 g if the CAD sled
    mass holds, run both)
  - Arrest **9.54 kN** axial (`arrest.axial_kN`), a separate load case
- Material allowable: Ti-6Al-4V yield **880 MPa** (`inter_array.Ti_yield_MPa`)

## Acceptance band (declared 2026-07-27, before running)

| Quantity | Constraint |
|---|---|
| Airgap closure under 3.68 kN | ≤ 0.05 mm total, both sides combined |
| Von Mises peak, any load case | ≤ 880 MPa / 1.5 = 587 MPa |
| First mode, chassis | > 200 Hz (an order clear of the 128 ms shot pulse) |

The decision rule for the resulting mass **m**, fixed now:

- **m ≤ 5.35 kg** (4.86 + 10 %) to the parametric model stands. Close P5 and P8, delete
  the provisional 17.88 m/s note from `README.md`.
- **5.35 < m < 6.80 kg** to neither estimate is right. Update `mass_properties.py` to the
  FEA mass, re-run `motor_model.py`, then correct the paper. Log the whole chain.
- **m ≥ 6.80 kg** to the CAD estimate is substantially right. **17.88 m/s becomes the
  headline number**, `README.md` and `paper/paper.tex` both change, and P8 escalates to
  a paper correction on the scale of P1, P4.

Deciding this in advance is the point. After the run, the temptation will be to pick the
threshold that keeps 20.37 m/s.

## If the chassis fails the stiffness constraint

Then the 6 mm plate is not the design, and the mass question is open in the other
direction, a stiffer chassis is heavier still, pushing further into the third branch
above. Report the mass at the constraint, not the mass of a chassis that does not meet it.

## Output

`validation/results/A4_sled_structural.json`, chassis mass at the stiffness constraint,
peak deflection per load case, von Mises peak, first mode, plus `solver`, `version`,
`element_type`, `element_count`, `contact_treatment`.
