# ADR-003: Linear synchronous motor, not a coilgun

**Status:** Accepted · **Date:** mid-2025 · **Phase:** Load-bearing

## Context
The concept was built around a coilgun from 2021. The requirement that broke it is not
velocity but **velocity accuracy**: the value proposition is a programmable per-satellite
ejection velocity with dispersion small against its astrodynamic effect.

## Decision
Ironless double-sided Halbach linear synchronous motor driving a reusable sled.

## Alternatives
- **Coilgun (induction or reluctance).** Rejected. It needs a conductive armature, either bolted
  to the customer satellite, breaking the no-modification requirement (ADR-006), or separated as a
  sabot with its own release event; it offers no abort; and **no published coilgun demonstrates
  velocity dispersion at the level this application needs.**
  Its one advantage (very high velocity) is erased by the payload's own g-limit, which caps
  useful exit velocity near 26-35 m/s regardless of launcher.

  > **Amended 2026-07-30, after reading the papers.** Two statements here were weaker than they
  > read, and one of them was simply wrong. See [`../PRIOR_ART.md`](../PRIOR_ART.md).
  >
  > **"Efficiency is 1-2 % in the literature" was wrong, and it was unsourced.** Feng et al. (IJAE
  > 2025) report **14.9-19.9 %** for a three-stage induction coilgun at 20 kg, the same order as
  > this design's own 20 % electrical-to-payload figure. Einat & Orbach (Sci. Rep. 2023) measure a
  > multi-stage reluctance launcher but at a **2.5 g** projectile, five orders of magnitude below a
  > CubeSat, so it cannot settle the question at this scale either way. **The efficiency argument is
  > withdrawn entirely**, it was never load-bearing, and it was wrong.
  >
  > **"Cannot command velocity closed-loop" overstated.** Feng varies exit velocity 230 to 321.56
  > m/s by charging voltage, 10 to 16 kV, approximately linearly, and uses armature position/velocity
  > feedback for stage trigger timing. That is genuine velocity *selection*. What no published
  > coilgun reports is a **dispersion figure**: Feng quotes none, so the supportable claim is about
  > absent evidence, and it is written that way above.
  >
  > **The decision stands, on the two reasons that were always load-bearing.** Both are now numbers
  > rather than assertions:
  >
  > | | Feng et al. 2025 | This design |
  > |---|---|---|
  > | Payload interface | Aluminium **armature coils** on the payload | Magnets on a reusable sled; satellite untouched |
  > | Acceleration | 3.9 m barrel to **1352 g** mean; >600 kN peak on 20 kg to **~3060 g** | 91 m/s² = 9.3 g mean, 10.7 g peak |
  > | Energy per shot | **6.91 MJ** | 2.80 kJ |
  >
  > A standard CubeSat qualifies to ~14 g quasi-static. Feng's design is ~100x that, and needs 2470x
  > the energy per shot. Neither is a secondary payload on an upper stage, and neither is a defect in
  > their work, they are solving a different problem. It is why this one is not a coilgun.
- **Maglev-style rail.** The 2021 framing left this open. Converged with the LSM choice.

## Consequences
**Everything downstream follows from this decision**, Halbach array, reusable sled, eddy
brake, supercapacitor bank, and the servo that makes the dispersion claim possible. It also
sets the ceiling: a synchronous machine's thrust is bounded by the same constant in both
directions, which is why arrest needs a separate mechanism (ADR-005).

## Validation
K<sub>t</sub> = 11.03 N per kA/m from `analysis/motor_model.py`, currently checked only
analytic-against-analytic, **this is the weakest link in the project and A1 is the top
roadmap item.** The dispersion claim rests on E7's assumed sensor noise and needs A7.
