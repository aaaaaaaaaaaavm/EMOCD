# A16: thrust against sled position when the array leaves the stator

**Closes:** `OPEN_PROBLEMS.md` **E27**. **Does not close P32** — P32 needs one controlled
propagation of every dependent result, which this analysis deliberately does not perform.

> ## BANDS DECLARED 2026-08-05. NOT YET RUN.
>
> Committed before `analysis/gen4_finite_stator.py` existed. `git log` is the evidence.

## Why

The Phase I model accelerates through a **uniform** 1.30 m stator and releases at 1500 mm. The
Gen4 working assembly puts the same 488 mm sled at s = 300 mm stowed and s = 1200 mm release — a
900 mm stroke — against a stator that ends at x = 1295.5 mm. From `docs/GEN4_STATUS.md`, with the
array at local x = −96 to +244 mm:

| | |
|---|---|
| Array fully over the stator while | s ≤ **1051.5 mm** |
| Partial-overlap run-out | the final **148.5 mm** of the stroke |
| Overlap remaining at release | **191.5 mm** of a 340 mm array, 56.3 % |

**A constant-thrust calculation shortened to 900 mm cannot describe this**, and E27 is explicit
that an overlap fraction alone is not an accepted force law. So this computes the Lorentz
integral over the **overlapped region only**, as a function of station, using the same field and
belt-winding pattern `motor_model.thrust_constant()` uses — so the two cannot fork.

## Method

`analysis/gen4_finite_stator.py`. For each station s, the stator carries current only over
x ∈ [0.5, 1295.5] mm, and the array spans [s − 96, s + 244] mm. Thrust is the Lorentz integral
over the intersection, at the rated sheet current, with the same Gauss-Legendre winding-thickness
quadrature the corrected `thrust_constant()` uses (P33's lineage: the superseded rule biased
K<sub>t</sub> 1.7 % high).

**Limitation, stated before the run.** This truncates an otherwise-periodic winding at the stator
end. It captures the loss of energised length; it does **not** capture end fields, winding
termination, or the phase-progression disturbance at the boundary, all of which E27 names. So a
result here is an **upper bound on the force in the run-out region** and must be labelled one.

## Acceptance bands

| # | Question | Band | What a miss means |
|---|---|---|---|
| 1 | Thrust over the fully-overlapped interval vs the Phase I periodic result | **within 2 %** | the finite integration disagrees with the model it is built from; suspect the implementation before the physics |
| 2 | Thrust at release, s = 1200 mm | **report**, expected near the 56.3 % overlap fraction | a large departure from the overlap fraction means end effects dominate and the upper-bound label is doing real work |
| 3 | Thrust monotonic and non-increasing through the run-out | **yes** | non-monotonic force would indicate a quadrature or indexing artefact |
| 4 | Exit velocity from integrating F(s) over the 900 mm stroke | **report only, NOT adopted** | — |
| 5 | Exit velocity against the Phase I 16.388 m/s | **report the ratio** | a Gen4 number above Phase I would be surprising on a shorter stroke and should be distrusted |

**Band 4 is deliberately not a pass/fail.** `docs/BASELINE.md` change control does not admit a new
operating point from an analysis that omits end fields, and `docs/GEN4_STATUS.md` states the
export gate stays closed until the affected results are propagated. **No number from this sheet
may be quoted as a Gen4 performance figure.**

## If band 1 fails

Suspect the implementation. The fully-overlapped interval is the one case where this analysis and
the periodic model describe the same physics, so a disagreement there is a bug, not a finding.
