# ADR-020: The inter-shot cadence is 1200 s

**Status:** Accepted · **Date:** 2026-08-05 · **Phase:** Load-bearing · **Closes:** P31

## Context

This repository has carried **two different inter-shot intervals since the beginning and never
reconciled them**, which is `OPEN_PROBLEMS.md` **P31**:

| Source | Interval | What depends on it |
|---|---|---|
| `paper.tex` §III-C | **10–20 s** | the thermal argument, the recharge argument |
| `analysis/astro.py` `conjunction(spacing_s=1200.0)` | **1200 s** | the conjunction geometry, the realignment period, the whole deployment safety case |

Twenty seconds and twenty minutes, for the same event, in the same project. They are not
necessarily contradictory — a machine able to fire every 18 s may still be *operated* every twenty
minutes — but **nothing anywhere stated which is the ConOps**, and two published analyses were
computed against different answers.

It stopped being a documentation problem when A13 ran. Attitude settling after the sled returns is
0.7 % of a 1200 s interval and a large fraction of a 20 s one, so **the same validation failure is
either negligible or dominant depending on a number nobody had written down.** Building the A15
POEM campaign forced the question, because a deployment script cannot be written without it.

## Decision

**The ConOps inter-shot interval is 1200 s.** Twelve shots span 4.0 h and about 2.6 orbits.

## Why this one

1. **It is the number the existing analysis already uses.** `astro.py`'s conjunction model, the
   realignment period and the deployment safety case are all computed at 1200 s. Adopting it
   invalidates nothing. Adopting 10–20 s would require re-running A6 and re-deriving the
   safety case against a geometry the project has never evaluated.
2. **The 10–20 s figure was never derived, and the reason it was believed was wrong.** The paper
   attributed the cadence to supercapacitor recharge. Recharge is 8.6 s at 300 W and 17.2 s at
   150 W, so the range looked right and was never examined — which is why the error survived. The
   mechanical chain is slower than either, and A13's later correction withdrew the specific floor
   without restoring the recharge claim.
3. **It makes the machine's own constraints comfortable rather than marginal.** Bank recharge,
   attitude settling, brake-fin cooling and magazine indexing all fit inside 1200 s with large
   margin. At 20 s several do not, and the thermal case in particular has no transient model
   behind it (**E26**).
4. **It suits the mission.** A hosted payload on a spent stage is not rate-limited by anything
   operational. There is no reason to fire every twenty seconds and good reason not to.

## What this does not do

**It does not re-declare A13's failed bands.** P31 explicitly warned that re-declaring bands 3–5
against 1200 s "is a band change and belongs declared and dated, not quietly applied to an
existing failure". A13's rows 3 and 4 remain **FAIL** on transient peak rate. What changes is the
*operational significance* of that failure, not its verdict. If those bands are to be re-declared
against this interval, that is a separate, dated act with a re-run behind it.

**It does not close E26.** The brake fin's between-shot cooling still has no transient model. A
longer interval makes it more likely to be fine and does not establish that it is.

**It does not validate the 1200 s conjunction geometry.** A6 returned three VOID rows and P1 stays
open. Adopting the interval those analyses used does not make their results stronger.

## Consequences

- `paper.tex` §III-C's cadence sentence must state 1200 s as the ConOps and describe 10–20 s as
  the machine's floor rather than its operating point.
- `astro.py`'s `spacing_s` becomes the single source and should be read from a named constant
  rather than carried as a default literal, which is the second half of what P31 asked for.
- A15's campaign is built on it, and A15's band 7 tests that the generated script and this ADR
  agree.

## Validation

None yet. This is a decision, not a measurement. A15 exercises it in an independent propagator and
**band 6 could still force it open** — if twelve satellites at 1200 s spacing come within 100 m of
each other over 90 days, the interval is wrong and this ADR is superseded.
