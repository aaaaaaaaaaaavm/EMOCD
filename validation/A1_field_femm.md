# A1: Airgap field, 2-D magnetostatic (FEMM)

**Closes:** the 2-D half of `OPEN_PROBLEMS.md` E1, and gives E2 its first
non-analytic check.
**Does not close:** 3-D end effects on Kt. Those need a 3-D solver (A2).

## Procedure

The step-by-step setup lives in `../analysis/femm/FEMM_RUN_SHEET.md` (geometry file
`../analysis/femm/emocd_cross_section.dxf`, one wavelength, periodic). Follow it as
written. This sheet exists to fix the acceptance band before the solver runs.

`../docs/FEMM_Run_Sheet.md` is the older sheet and is **superseded**: its ⟨B⟩ ≈ 0.62 T
target predates the winding-resolved motor model.

## Acceptance band (declared 2026-07-27, before running)

All reference values from `analysis/results/field_verification.json` and
`analysis/results/motor_results.json` as committed at `13a743f`.

| Quantity | Reference | Band | Source of reference |
|---|---|---|---|
| Double-sided mid-gap peak | 0.694 T | ±5 % | `double_midgap_peak_T` |
| Array-surface peak B₀ | 0.771 T | ±5 % | `analytic_B0_surface_T` |
| Winding mean \|B\| | 0.552 T | ±5 % | `winding_mean_absB_T` |
| Thrust at 140 kA/m rated | 1571 N (Kt 11.22 N per kA/m x 140) | ±10 % | `Kt_N_per_kA` |
| Stray \|B\| at 10 mm | 22.7 mT | factor 1.5 | `stray_field.10mm_mT` |
| Stray \|B\| at 20 mm | 4.3 mT | factor 1.5 | `stray_field.20mm_mT` |
| Stray \|B\| at 50 mm | 0.4 mT | factor 2 | `stray_field.50mm_mT` |

The stray bands are deliberately loose: these are small differences of large numbers far
from the source, sensitive to box size and mesh, and 20/50 mm are the two values that
were already wrong once (P3).

The thrust band is the one that matters. Kt sets exit velocity, efficiency, and every
downstream astro number.

## If the band is missed

1. Record the FEM/analytic ratio, mesh element count, boundary condition, and box size in
   `validation/results/A1_femm.json` **before** touching anything else.
2. Open a P-item describing the discrepancy. Do not edit `motor_model.py` to match.
3. Check the usual suspects in this order: air-box too small (A = 0 boundary pulling flux),
   magnetisation direction per DXF layer, N45SH Br/Hc override, periodic cell not centred.
4. Only after the cause is identified does anything downstream move, and then the paper
   moves with it, per the standing rule that the scripts are the source of truth.

## Output

`validation/results/A1_femm.json`, the seven quantities above as computed, each with its
ratio to the reference, plus `femm_version`, `mesh_elements`, `airgap_mesh_mm`,
`box_margin_mm`, `boundary`.
