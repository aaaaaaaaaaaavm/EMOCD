# Correction, 2026-08-03

I found that both the reference implementation and the FEM post-processor used the same
invalid winding-thickness quadrature: nine endpoint-inclusive samples multiplied by
thickness divided by nine. That is neither a midpoint nor a trapezoidal rule. Replacing it
with nine-point Gauss-Legendre quadrature gives:

| Quantity | FEM | Reference | Ratio |
|---|---:|---:|---:|
| Thrust constant | 11.026 N per kA/m | 11.03 N per kA/m | 0.9997 |
| Ripple | 0.97% | 0.99% | — |

A1 remains **PARTIAL** because the same surface-field and 50 mm stray-field rows still miss.
The thrust comparison remains within its predeclared band, but the earlier 0.07% agreement
did not independently test the shared quadrature. The corrected agreement is 0.03%.

The original result remains below as the superseded run record.

---
# A1: Airgap field, 2-D magnetostatic (FEMM)

> ## RUN 2026-07-29. Verdict **PARTIAL**: five of seven bands, and the one that matters is met
>
> | Band (declared below, before the run) | FEM | Reference | Ratio | |
> |---|---|---|---|---|
> | Double-sided mid-gap peak, ±5 % | 0.6947 T | 0.6942 T | 1.0007 | **pass** |
> | Array-surface peak, ±5 % | 1.4641 T | 0.7714 T | 1.8979 | **fail, see P20** |
> | Winding mean \|B\|, ±5 % | 0.5523 T | 0.5518 T | 1.0010 | **pass** |
> | **Thrust at 140 kA/m, ±10 %** | **1571.9 N** | **1570.8 N** | **1.0007** | **pass** |
> | Stray \|B\| at 10 mm, factor 1.5 | 26.33 mT | 22.7 mT | 1.16 | **pass** |
> | Stray \|B\| at 20 mm, factor 1.5 | 4.91 mT | 4.3 mT | 1.14 | **pass** |
> | Stray \|B\| at 50 mm, factor 2 | 0.93 mT | 0.4 mT | 2.32 | **fail, see P21** |
>
> **K<sub>t</sub> = 11.228 N per kA/m against the model's 11.22, a ratio of 1.0007**, with force
> ripple 1.25 % against 1.26 %. Full results in `validation/results/A1_femm.json`.
>
> **Neither missed band is a model error, and both are logged rather than argued away.**
> **P20**: the array-surface reference in this sheet is mis-specified — it names a *single*
> array's fundamental where any plane in a double-sided machine also sees the opposing array.
> Against the correct double-sided value of 0.9317 T the FEM's fundamental is 0.9312 T, a ratio
> of 0.9994. **The row failed as declared and the model is right**, and both statements are
> recorded. **P21**: a 2-D solve has infinite depth, so it must overestimate far field; 50 mm is
> where that shows.
>
> **The bands below are left exactly as written on 2026-07-27.** A run sheet edited after seeing
> its results is worth nothing, so the P20 correction belongs in A2's sheet, not this one.
>
> **Solver substitution, recorded rather than presented as FEMM.** FEMM is Windows-only and was
> not available. This is a meshed differential-FEM solve of the same 2-D problem — scikit-fem
> 12.0.2 P1 Lagrange on a gmsh 4.15.2 mesh, 140,750 elements, 0.6 mm airgap mesh, 500 mm box,
> `Az = 0` on the far boundary. A differential solve on a mesh is what E2 asked for; FEMM was
> only ever the named tool for it.

**Closes:** the 2-D half of `OPEN_PROBLEMS.md` E1, and gives E2 its first
non-analytic check.
**Does not close:** 3-D end effects on Kt. Those need a 3-D solver (A2).

**What it establishes.** K<sub>t</sub> had only ever been checked analytic-against-analytic: a
closed-form travelling-wave model against magpylib, both superposing analytic solutions for
uniform blocks, neither solving a field equation. This solves the PDE on a mesh and agrees to
0.07 %. It was the project's largest single gap until it ran; the largest now is that **nothing
has been measured at any scale** (E4).

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
