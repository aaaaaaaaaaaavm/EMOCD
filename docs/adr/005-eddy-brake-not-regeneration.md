# ADR-005: Eddy-current brake; sled kinetic energy is dissipated

**Status:** Accepted · **Date:** 2025 · **Phase:** I

## Context
The sled must be stopped after release. An earlier version of this work claimed 52 %
efficiency by crediting 55 % of the sled's energy back through regenerative braking.

## Decision
Contactless copper-fin eddy-current brake with a ring-spring backstop. **The sled's kinetic
energy is thrown away.** Efficiency is quoted electrical-to-payload with no regeneration
credit.

## Alternatives
- **Motor regeneration alone.** Rejected on physics: braking force is bounded by the same
  thrust constant as acceleration, so the motor cannot arrest the sled within the remaining
  track.
- **Mechanical brake.** Rejected: contact, wear, and particulate generation next to an
  unmodified customer satellite.

## Consequences
**This decision corrected an error in my own earlier work.** The 52 % figure was
double-counting; the honest number was 32 % and is now 19.6 % at the measured sled mass. It
also makes the sled mass doubly expensive, a heavier sled takes more of the shot energy *and*
throws more of it away, which is why efficiency fell so far when the mass was measured
(ADR-012). E8 records the thrown-away energy as an open inefficiency.

## Validation
Brake sizing is first-order plate drag from `legacy/c3_c4_em.py`. **No force, time profile for
the arrest exists anywhere** (E20). B-4 in `docs/BENCHTOP_TESTS.md` is a cheap drop test that
would give the first measured point.
