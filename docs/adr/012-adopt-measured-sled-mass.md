# ADR-012: Adopt the measured 9.445 kg sled

**Status:** Accepted · **Date:** 2026-07-29 · **Phase:** I (error correction)

## Context
Two estimates of the same part disagreed by 94 %. `mass_properties.py` gave a parametric
4.86 kg, which `motor_model.py` used and which set the 20.37 m/s headline. Exact OCC solid
volumes from `cad/step/gen3/EMOCD_Sled_Gen3.step` gave **9.445 kg** (P15).

**The decision rule was written before the analysis that resolved it.**
`validation/A4_sled_structural.md` fixed the consequence of each outcome in advance: ≤ 5.35 kg
the parametric model stands; 5.35-6.80 kg neither is right; **≥ 6.80 kg the headline changes
and the paper changes materially.**

## Decision
Adopt 9.445 kg across `analysis/`. The rated point becomes **16.537 m/s at 10.72 g**.

## Alternatives
- **Keep 4.86 kg pending further work.** Rejected: A4 ran, the drawn plate passed all three
  structural bands, and nothing forces a lighter chassis. Waiting would have been preferring
  the nicer number.
- **Use 7.50 kg**, the earlier CAD estimate giving 17.88 m/s. Rejected: not measured.
- **Design the lighter chassis first, then adopt.** Rejected as sequencing: the baseline must
  reflect what is drawn today. The rib-stiffened redesign is Phase II.

## Consequences
The first time a value in `analysis/` has moved. Exit velocity −19 %, efficiency 31.5 to 19.6 %,
lifetime multiplier x1.80 to x1.62. Three second-order effects that were not obvious:

- The closed-loop Monte Carlo **silently saturated**: its 20.0 m/s setpoint now sat above the
  open-loop ceiling (ADR-014).
- Arrest loads nearly doubled, 9.5 to 18.5 kN. This is the one place a heavier sled makes the
  machine *harder*, not merely slower.
- **It invalidated A5 and A8**, both run at the old point, discovered afterwards, logged as
  P19, and the reason `BASELINE.md` now requires every change to declare what it invalidates.

9.445 kg is the **as-drawn, unpocketed** geometry; A4 reports a 17x stress margin, so mass can
come out. Nobody has designed that chassis.

## Validation
A4 (CalculiX, run, all bands pass). The measurement method reproduces P8's 17.88 m/s exactly
when fed 7.50 kg, so the discrepancy is in the mass and not the method. Re-running A5 and A8
at the current point is on the roadmap.
