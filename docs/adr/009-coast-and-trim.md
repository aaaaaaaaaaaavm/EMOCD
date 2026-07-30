# ADR-009: Coast-and-trim release zone

**Status:** Accepted · **Date:** 2025 · **Phase:** I

## Context
Releasing the payload while the motor is still applying full thrust puts a large force through
the cradle interface at the moment of separation, which drives tip-off.

## Decision
A 0.2 m unpowered coast-and-trim zone at the end of the 1.5 m axis. Final velocity correction
is commanded from a measured position before release.

## Alternatives
- **Release under full thrust.** Rejected: the leading tip-off term alone would approach
  34 °/s against a requirement near 5 °/s.
- **Longer coast.** Rejected: costs stroke, and stroke buys velocity as √L.

## Consequences
This is what closes the tip-off budget to 3.9 °/s worst case, and it is what makes the
closed-loop dispersion claim possible, the servo corrects against a photogate measurement in
this zone. It costs 0.2 m of a 1.5 m envelope that is already 44 % over ESPA Grande (P9).

## Validation
Tip-off budget is a model output with **no multibody model behind it**: A7, unrun. The band
it would be judged against may itself be mis-sourced (5 °/s vs the NRCSD ICD's 2 °/s).
