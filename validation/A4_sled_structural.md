# A4 — Sled chassis structural (CalculiX or Code_Aster)

**Closes:** `OPEN_PROBLEMS.md` **P5** (sled mass 4.86 vs 7.50 kg) and **P8** (exit
velocity 20.37 vs provisional 17.88 m/s).

This is the highest-leverage analysis in the repository. Everything headline —
velocity, efficiency, recoil, lifetime multiplier — hangs off the sled mass, and that
mass currently has two irreconcilable estimates, neither of them FEA'd.

## The question, stated so it can be answered

Not "what does the sled weigh" but: **what is the lightest chassis that holds the airgap
open to ±0.05 mm under load?** Mass is the output of that constraint, not an input.

## Inputs (all committed)

- Geometry: `cad/step/EMOCD_Sled.step`
- Dimensions and material: `cad/parameters.json`, sled group (6 mm Ti-6Al-4V chassis,
  flagged `PROVISIONAL_PENDING_FEA`)
- Loads, from `analysis/results/sizing.json`:
  - Inter-array attraction **3.68 kN** (`inter_array.force_kN`), the sizing case
  - Axial acceleration **16.3 g** at the script operating point (12.5 g if the CAD sled
    mass holds — run both)
  - Arrest **9.54 kN** axial (`arrest.axial_kN`), a separate load case
- Material allowable: Ti-6Al-4V yield **880 MPa** (`inter_array.Ti_yield_MPa`)

## Acceptance band (declared 2026-07-27, before running)

| Quantity | Constraint |
|---|---|
| Airgap closure under 3.68 kN | ≤ 0.05 mm total, both sides combined |
| Von Mises peak, any load case | ≤ 880 MPa / 1.5 = 587 MPa |
| First mode, chassis | > 200 Hz (an order clear of the 128 ms shot pulse) |

The decision rule for the resulting mass **m**, fixed now:

- **m ≤ 5.35 kg** (4.86 + 10 %) → the parametric model stands. Close P5 and P8, delete
  the provisional 17.88 m/s note from `README.md`.
- **5.35 < m < 6.80 kg** → neither estimate is right. Update `mass_properties.py` to the
  FEA mass, re-run `motor_model.py`, then correct the paper. Log the whole chain.
- **m ≥ 6.80 kg** → the CAD estimate is substantially right. **17.88 m/s becomes the
  headline number**, `README.md` and `paper/paper.tex` both change, and P8 escalates to
  a paper correction on the scale of P1–P4.

Deciding this in advance is the point. After the run, the temptation will be to pick the
threshold that keeps 20.37 m/s.

## If the chassis fails the stiffness constraint

Then the 6 mm plate is not the design, and the mass question is open in the other
direction — a stiffer chassis is heavier still, pushing further into the third branch
above. Report the mass at the constraint, not the mass of a chassis that does not meet it.

## Output

`validation/results/A4_sled_structural.json` — chassis mass at the stiffness constraint,
peak deflection per load case, von Mises peak, first mode, plus `solver`, `version`,
`element_type`, `element_count`, `contact_treatment`.
