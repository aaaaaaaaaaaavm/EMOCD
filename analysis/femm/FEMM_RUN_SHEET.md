# FEMM Run Sheet: VOLLEY Airgap Field (analysis A1, closes half of E1)

Geometry file: `emocd_cross_section.dxf` (same folder). All dimensions verified against the live Fusion CAD on 2026-07-23: magnet arrays z ±6 to ±14 mm (8 mm N45SH blocks), stator belts z −5 to +5 mm (10 mm winding), **1 mm mechanical airgap each side**, belts 7 mm wide on 8 mm pitch, Halbach wavelength λ = 48 mm (12 mm segments). The DXF holds ONE wavelength; the model is periodic.

## Setup (Magnetics problem, ~15 min)
1. New magnetics problem to Planar, units mm, **depth 90 mm** (array width), frequency 0.
2. File to Import DXF to `emocd_cross_section.dxf` (tolerance 0.01).
3. Materials (from library): **N45SH... use "NdFeB 40 MGOe" and set Hc to 891 kA/m / Br 1.32 T for N45SH** (edit material), **Copper** for belts, **Air** elsewhere.
4. Magnet block labels, one label per 12 mm segment, `Magnetization Direction` per DXF layer name:
   - MAG_UP = 90°, MAG_RIGHT = 0°, MAG_DOWN = 270°, MAG_LEFT = 180°.
   - Upper array as drawn; lower array layers are already the opposed pattern (double-sided drive).
5. Belt labels: Copper, circuits A/B/C, series turns = 1, currents for the static shot: **A = +I, B = −I/2, C = −I/2** with I = rated sheet current x pitch to use **1120 A-turns per belt** (140 kA/m x 8 mm) for the rated point; 0 A for the open-circuit field map.
6. Boundary: surround with an air box ≥ 60 mm beyond geometry; apply **A = 0** on the outer boundary. For strict periodicity, replicate the wavelength 3x and read the centre cell.
7. Mesh: default, then refine airgap to 0.25 mm mesh size.

## Runs & exports (300 dpi PNG screenshots + saved .ans)
- **Run 1 (I = 0):** open-circuit Halbach field. Export at **300 dpi**: (a) **|B| colour contour** across the airgap region; (b) **flux-line plot** (View to Contour/flux lines, ~30 lines) showing closure through the arrays and the weak-side self-shielding; (c) line plot of **Bz along z = 0 across one wavelength** to compare to the analytic model's **0.694 T double-sided peak** (target: within a few %). Items (a) and (c) are the IEEE §IV-A verification figure (FEA-1).
- **Run 2 (rated current):** force. Select the two magnet regions to Block integral to **Lorentz force (steady)** to x-force x (1300/48 wavelengths) to compare thrust from Kt = 11.03 N/(kA·m) at 140 kA/m ≈ 1544 N. Ratio = the 2-D FEA check on Kt.
- **Run 3 (stray field, I = 0):** line plots of |B| at 10 / 20 / 50 mm beyond the array back face to compare the **22.7 / 4.3 / 0.4 mT** keep-out profile (FEA-3, §XII). (The 4.7 / 1.0 mT figures previously quoted here were the pre-P3 values; corrected 2026-07-27 against `analysis/results/field_verification.json`.) Add a 1 mm steel sheet (silicon steel M-19) at the septum position and re-run to quantify attenuation.

## Acceptance band

Declared in `validation/A1_field_femm.md`, not here, read it before running. In short:
±5 % on the field quantities (0.694 T double-sided peak, 0.771 T surface, 0.552 T winding
mean), ±10 % on thrust at the rated point, looser factors on stray field.

## Record for the paper
Solver version, mesh element count, boundary condition, and the three comparison ratios (FEM/analytic). Any deviation >5% on Run 1 goes to the reconciliation list before the rated point is re-locked.

Note: this 2-D run does NOT close 3-D end effects, that needs ANSYS Maxwell 3D (analysis A2) or an explicit end-effect correction argument. State this in the paper's limitations if only 2-D is run.
