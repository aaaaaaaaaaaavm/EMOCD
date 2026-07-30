# FEMM Run Sheet: VOLLEY Halbach Airgap Verification (Fig. 6)

> **SUPERSEDED (2026-07-27). Do not run against the targets in this sheet.** Its ⟨B⟩ ≈
> 0.62 T winding-gap target predates the winding-resolved motor model, which computes
> **0.552 T** (`analysis/results/field_verification.json`, `winding_mean_absB_T`), so this
> sheet can no longer function as a test. Use `analysis/femm/FEMM_RUN_SHEET.md` for the
> procedure and `validation/A1_field_femm.md` for the acceptance band. Kept for the record
> only.

Goal: verify the analytic airgap field (⟨B⟩ ≈ 0.62 T across the winding gap, B₀ ≈ 0.76 T at array surface) with a 2-D magnetostatic FEA, and export the two figures the report needs. Budget: one lab session.

## 1. Problem setup
- FEMM 4.2 to New to **Magnetics problem**.
- Problem type: **Planar**, depth = **90 mm** (sled width), units = millimeters, solver precision 1e-8, min angle 30.

## 2. Geometry (draw one wavelength, then copy)
Two opposed Halbach arrays facing each other across the winding gap. Coordinates in mm, y measured from gap centerline:
- **Gap:** total 12 mm (winding space), so magnet faces at y = +6 and y = −6.
- **Magnets:** thickness 8 mm to upper array occupies y = 6...14, lower array y = −14...−6.
- **Wavelength λ = 48 mm, 4 blocks per λ** to each block 12 mm wide x 8 mm tall.
- Draw 5 wavelengths (240 mm) to keep the middle wavelength free of edge effects; measure only in the central λ.
- Upper array magnetization sequence (block by block, degrees): **90, 0, 270, 180** (i.e. up, right, down, left, strong side faces DOWN into the gap).
- Lower array is the mirror: **90, 180, 270, 0** starting aligned under the upper blocks so both strong sides face the gap and the gap fields **add**. Check: if your mid-gap B comes out near zero, the lower array phase is flipped, shift it by 2 blocks.

## 3. Materials
- Magnet blocks: Materials Library to **NdFeB 40 MGOe** (closest stock to N45SH; Br ≈ 1.28 T). For exact N45SH create a copy with **Br = 1.32 T** (set Hc = Br/μ₀μᵣ with μᵣ = 1.05 to Hc ≈ 1.0e6 A/m). Set each block's magnetization direction per the sequence above.
- Everything else (gap, surround): **Air**. No iron anywhere, the design is ironless.

## 4. Boundary
- Enclose the model in a circle ~3x the array length. Properties to Boundary to **A = 0** on the outer circle (or use the "Open Boundary" IABC wizard, 7 shells).

## 5. Mesh & solve
- Mesh size inside gap and magnets: **0.5 mm** (set per-region). Elsewhere auto. Mesh to Solve to View results.

## 6. What to extract (these become Fig. 6 and one table row)
1. **Density plot:** View to Density Plot to |B| range 0-1.0 T, legend on. Screenshot the central wavelength. This is Fig. 6.
2. **Centerline profile:** draw a contour along y = 0 across the central wavelength to Plot **B·n (normal component)** vs length to export the plot and the CSV.
3. **Numbers for the comparison table:** on that contour, note **peak |B|** and compute **mean |B|** (FEMM: Integral to B·n average, or take it from the CSV). Repeat the line scan at y = ±3 mm (winding edges).
4. Optional but nice: same model with the lower array deleted to shows the single-sided field ≈ half, demonstrating why the double-sided layout was chosen.

## 7. Acceptance criteria (what the report will claim)
- Mid-gap peak in the range **0.55-0.75 T**, spatial mean over the ±5 mm winding region within **±20% of the analytic 0.62 T**. If FEMM comes in lower by more than that, note it honestly and we re-run the C3 shot model with the FEA value, the design has margin (force command is 90% of F_max, and 25 g cap sits above the 19.7 g operating point).
- Stray field check for the keep-out spec: line scan 20 mm outside the array back face to expect low tens of mT or less (Halbach weak side). Record the value; it feeds Section 4.8.

## 8. Export list (bring these back)
- `fig6_density.png` (density plot screenshot), `centerline_By.csv`, `y3mm_By.csv`, `strayfield_20mm.csv`, plus the .fem file itself for the appendix.
