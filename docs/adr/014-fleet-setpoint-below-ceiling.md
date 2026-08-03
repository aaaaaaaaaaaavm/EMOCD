# ADR-014: Fleet setpoint at 98.2 % of the open-loop ceiling

**Status:** Accepted · **Date:** 2026-07-29 · **Phase:** I

## Context
Adopting the 9.445 kg sled (ADR-012) dropped the open-loop ceiling to 16.537 m/s while
`closed_loop_mc()` still commanded a 20.0 m/s fleet setpoint. The servo gain pinned at
`K_RATED` and the run reported a "dispersion" of 0.267 m/s that was really a **2.27 m/s
shortfall**. The Monte Carlo was measuring saturation, not sensing noise, and it did so
silently.

## Decision
Set `V_FLEET = 16.2 m/s`, **98.2 % of the ceiling, the same fraction 20.0 held against the
old 20.37**, and add a guard that raises if the servo fails to reach its setpoint.

## Alternatives
- **Pick a round number (16.0).** Rejected: it would have worked, and it would have been a
  number chosen by taste. Preserving the *fraction* preserves the headroom argument the
  dispersion claim rests on.
- **Leave 20.0 and report the saturated figure.** Rejected: it is not a dispersion.
- **Raise the ceiling to meet the setpoint.** That is a design change, not a correction.
  Phase II.

## Consequences
Dispersion returns to 0.027 m/s, essentially unchanged, so the servo claim survives the mass
change. The rule matters more than the number: **a setpoint above the open-loop ceiling makes
the dispersion figure meaningless**, and nothing detected that before the guard existed.

## Validation
`motor_model.py` raises if `mc['mean'] < V_FLEET - 0.05`. E7 remains open: the dispersion still
rests on *assumed* sensor noise, and A7 plus benchtop B-3 would test it.

## Numerical correction, 2026-08-03

The fleet setpoint remains 16.2 m/s. Correcting the shared thrust quadrature moves the
open-loop ceiling from 16.537 to **16.388 m/s**, leaving 0.188 m/s of nominal headroom.
The decision remains accepted; the headroom fraction is now 98.85%, not 98.2%.
