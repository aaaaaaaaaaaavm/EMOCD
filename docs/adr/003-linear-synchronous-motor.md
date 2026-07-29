# ADR-003 — Linear synchronous motor, not a coilgun

**Status:** Accepted · **Date:** mid-2025 · **Phase:** Load-bearing

## Context
The concept was built around a coilgun from 2021. The requirement that broke it is not
velocity but **velocity accuracy**: the value proposition is a programmable per-satellite
ejection velocity with dispersion small against its astrodynamic effect.

## Decision
Ironless double-sided Halbach linear synchronous motor driving a reusable sled.

## Alternatives
- **Coilgun (induction or reluctance).** Rejected. Its efficiency is 1–2 % in the literature;
  it needs an armature bolted to the customer satellite, which breaks the no-modification
  requirement (ADR-006); it offers no abort; and it cannot command velocity closed-loop.
  Its one advantage — very high velocity — is erased by the payload's own g-limit, which caps
  useful exit velocity near 26–35 m/s regardless of launcher.
- **Maglev-style rail.** The 2021 framing left this open. Converged with the LSM choice.

## Consequences
**Everything downstream follows from this decision** — Halbach array, reusable sled, eddy
brake, supercapacitor bank, and the servo that makes the dispersion claim possible. It also
sets the ceiling: a synchronous machine's thrust is bounded by the same constant in both
directions, which is why arrest needs a separate mechanism (ADR-005).

## Validation
K<sub>t</sub> = 11.22 N per kA/m from `analysis/motor_model.py`, currently checked only
analytic-against-analytic — **this is the weakest link in the project and A1 is the top
roadmap item.** The dispersion claim rests on E7's assumed sensor noise and needs A7.
