# ADR-013: Drop the lifetime-ratio invariance claim

**Status:** Accepted · **Date:** 2026-07-29 · **Phase:** I (error correction)

## Context
The paper's abstract claimed the lifetime multiplier was "shown invariant across ballistic
coefficient and a fivefold solar-activity density range", and the Limitations section
nominated that invariance as **the defensible result**: the thing that survived when absolute
lifetimes did not.

GMAT R2022a, run headless against bands declared before the run, reproduced the multiplier at
mean (1.775) and high (1.730) activity but returned **2.074 at low**: an 18.5 % spread against
a ≤5 % band. A5's verdict is FAIL.

## Decision
Remove the invariance claim from the paper and every front page. Quote the multiplier at a
**stated activity level**. Claim no invariance.

## Alternatives
- **Widen the band.** Rejected outright: the band was declared before the run precisely so it
  could not be widened after it.
- **Report only mean activity and say nothing.** Rejected as concealment.
- **Fix `astro.py` first.** Rejected: the standing rule is record, analyse, then propagate,
  and the parser's own failure text says *open a P-item; do not edit analysis/astro.py*.

## Consequences
The claim the paper nominated as its most defensible is the one an independent propagator did
not reproduce. Worse than first recorded: the **ballistic-coefficient half is the identical
tautology.** In `lifetime()` the drag term is `-0.5 * rho(h, scale) * v**2 / BC`, so `scale`
and `1/BC` occupy the same multiplicative slot, a reciprocal test confirms BC=61/scale=2.0
and BC=30.5/scale=1.0 both return 1.7987. **Neither half was ever tested by a method capable
of failing.** The x1.80 point value survives at mean and high activity; the invariance does
not.

## Validation
GMAT, three activity levels, propagated to the 120 km floor. The mechanism was tested rather
than guessed: sweeping `astro.py`'s density scale over 40x moves the multiplier only
1.7992 to 1.7968. Closing the BC half needs GMAT at BC 40 and 90, until then the honest
position is *unknown*, not *invariant*.
