# A12: the inter-array attraction, and whether `sizing.py` adopts a corrected value

**Closes:** `OPEN_PROBLEMS.md` **P17**, which is HIGH and has been open since 2026-07-29.
**Does not close:** anything about A4's structural conclusions. Those survive either way, and
this sheet says why before it runs.

## Why this sheet exists at all

P17 found that `analysis/sizing.py::inter_array_attraction()` computes the force between the two
opposed Halbach faces from a flat-plate Maxwell-stress formula — a uniform pressure
`B_face^2/(2*mu0)` at a mean face field of 0.55 T over the 340 x 90 mm footprint — giving
**3672 N**, and that this number was the applied load in the CalculiX A4 run without ever having
been checked. `magpylib.getFT()` gave **2686.6 N** converged, so the analytic form is **36.7 %
high**.

**P17 closes with its own procedural failure recorded**, and that is what this sheet fixes:

> *"This was computed before an acceptance band was declared for it, which inverts this project's
> own rule. It is therefore logged as a discrepancy, not as a validated result. Proper closure
> needs a run sheet with a band declared in advance, and a decision about whether `sizing.py`
> adopts a corrected formula. **Do not edit `sizing.py` on the strength of this entry.**"*

**So this is not a blind test and it must not pretend to be.** The magpylib number is already
known. What is declared in advance here, and what actually matters, is two things a
knowing-the-answer run still cannot fake:

1. **An independent second method**, chosen because it can disagree. If two numerical methods
   built on different mathematics both land near 2687 N, that is evidence; one method agreeing
   with itself at finer mesh is not.
2. **The adoption rule** — what happens to `sizing.py` at each possible outcome, written down
   before the outcome is known. This is the same device `validation/A4_sled_structural.md` used
   for the sled mass, where the decision rule was fixed before the measurement that triggered it.

## The two methods

| | |
|---|---|
| **M1, force on sources** | `magpylib.getFT()`. Meshes each magnet block and integrates the field gradient over the block volume in three dimensions. Driven by `analysis/motor_model.py::build_field()` so it cannot disagree with the repo about the magnets themselves |
| **M2, Maxwell stress on a surface** | Integrate the Maxwell stress tensor numerically over a plane in the airgap midway between the arrays: `F_y = (1/2mu0) * ∫ (B_y^2 - B_x^2 - B_z^2) dA`, sampled on a grid from the same `build_field()`. Different mathematics: a surface integral of a field the solver never differentiates, against a volume integral of a gradient |

**M2 is what the analytic formula is a one-point approximation of.** The analytic form evaluates
`B^2/(2mu0)` once, at a mean `B`, and multiplies by the area. M2 evaluates the full tensor at
every point and integrates. If the Jensen argument in P17 is the whole story — that
`mean(B^2) >= mean(B)^2` and a Halbach face field is strongly non-uniform — then **M2 should land
near M1 and well below the analytic value**, and the gap is explained rather than merely observed.

## Acceptance bands, declared 2026-07-31 before M2 was written

| # | Quantity | Prediction | Accept if |
|---|---|---|---|
| 1 | M1 convergence | successive mesh deltas halve, settling near 2687 N | finest-mesh value within ±2 % of 2686.6 N |
| 2 | **M2 against M1** | **agreement** | **within ±10 %.** This is the test. Two methods from different mathematics landing together is the evidence P17 lacks |
| 3 | M2 against the analytic 3672 N | M2 is **low** | M2 below 3200 N, i.e. the analytic form overestimates by more than 15 % |
| 4 | Direction of the error | analytic is **high**, never low | any result showing the analytic form *underestimates* falsifies the Jensen argument and this entry |
| 5 | Grid convergence of M2 | stable | halving the sample spacing moves M2 by less than 1 % |

**Falsification.** Row 2 missing means one of the two methods is wrong and neither number may be
adopted — the correct outcome would then be that P17 stays open with a second discrepancy in it,
not that the closer-looking number wins. Row 4 failing would mean the mechanism P17 claims to
understand is not the mechanism, and the whole entry would need withdrawing.

## The adoption rule, declared before the run

**If bands 1–5 all hold**, `sizing.py` adopts the numerical value and propagates **once**, in this
order and no other:

1. `inter_array_attraction()` returns the numerically integrated force, with the analytic form
   kept in the file as the superseded method and a comment saying what replaced it and why.
2. Plate stress and margin follow from it — they are computed from the force, so they move with it.
3. `validation/results/A4_sled_structural.json` gains a note that its applied load was **37 %
   heavy**, so its results are conservative. **A4 is not re-run and its verdict does not change.**
4. `docs/BASELINE.md` regenerated; `make_baseline.py --check` clean afterwards.

**If any band fails**, nothing in `analysis/` moves and P17 stays open. That is the whole point of
writing the rule down first.

**What is not in scope.** The retention gate is sized from a 24 kg ascent stack at 25 g
(`retention_gate()`), not from the array attraction, so it does not move with this. P17 lists it
as affected; that is wrong and is corrected here.

---

## Result, run 2026-07-31

`validation/magpylib/maxwell_surface_force.py` (M2) was written **after** the bands above were
committed in `fff034e`, and `check_inter_array_force.py` (M1) was re-run unchanged.

### M1, volume integral of the field gradient

| Mesh per block | Force | Delta |
|---|---|---|
| (2,2,2) | 2909.4 N | |
| (4,4,4) | 2773.0 N | −136.3 |
| (6,6,6) | 2720.8 N | −52.2 |
| (8,8,8) | 2701.6 N | −19.2 |
| (10,10,10) | 2693.3 N | −8.3 |
| (12,12,12) | 2689.0 N | −4.3 |
| **(14,14,14)** | **2686.6 N** | −2.5 |

### M2, Maxwell stress over the mid-gap plane

| Grid | Samples | Force | Delta |
|---|---|---|---|
| 96 x 12 | 1,152 | 2643.1 N | |
| 192 x 24 | 4,608 | 2630.7 N | −12.5 |
| 384 x 48 | 18,432 | 2628.2 N | −2.5 |
| **768 x 96** | **73,728** | **2627.6 N** | −0.6 |

### Against the declared bands

| # | Prediction | Result | |
|---|---|---|---|
| 1 | M1 converges within ±2 % of 2686.6 N | **2686.6 N**, deltas halving throughout | **pass** |
| 2 | **M2 within ±10 % of M1** | **2627.6 vs 2686.6 N, 2.2 % apart** | **pass** |
| 3 | M2 below 3200 N | 2627.6 N | **pass** |
| 4 | analytic is high, never low | high by 40.2 % against M2 | **pass** |
| 5 | M2 grid convergence under 1 % | **0.02 %** | **pass** |

**Five of five.** Two methods that share only the block model of the magnets — one integrating a
field gradient over magnet volumes, one integrating a stress tensor over a plane the field is
never differentiated on — land 2.2 % apart and 27 % below the analytic formula. **That is the
evidence P17 was missing.**

### And the mechanism P17 gave is backwards

P17 explains the overestimate by Jensen's inequality: *"Maxwell stress needs the mean of `B**2`;
the analytic form uses the square of the mean `B`; and `mean(B**2) >= mean(B)**2` for any
non-uniform field... so the analytic form must overestimate."*

**The inequality is right and the conclusion drawn from it is the wrong way round.** If
`mean(B²) ≥ mean(B)²`, then a one-point form evaluated at the *true* mean field
**under**estimates the true force. Jensen cannot be the reason the analytic value is high.

Decomposing M2's own field statistics on the stress plane:

| | Force | Effect |
|---|---|---|
| Analytic, `B_face = 0.550 T` assumed, one point | **3683 N** | as published |
| Same one-point form at the **actual** mean, `\|B_y\| = 0.4127 T` | 2073 N | **x1.776 overestimate from the assumed field** |
| Full integral, `mean(B_y²) = 0.2158 T²` | **2628 N** | **x1.267 *under*estimate corrected by Jensen** |

Net **x1.402**, against the observed 3683/2628 = **x1.402**. The two effects act in opposite
directions and the decomposition closes exactly.

**So the real cause is the input, not the formula.** `B_face = 0.55 T` is not the mean normal
field on the plane where the stress acts — that is 0.4127 T. The flat-plate form is a legitimate
approximation whose Jensen error is only 27 % and in the *safe* direction; it was fed a field
0.33x too high, and that swamps it.

**P17 is corrected in place rather than rewritten.** It found a real 37 % error and its number
was right; its explanation was not, and a wrong mechanism attached to a right number is exactly
the kind of thing that survives review and then misleads the next person.

### Adopted, per the rule declared before the run

`analysis/sizing.py::inter_array_attraction()` takes **2686.6 N** (M1, the more direct
computation of force on a body, and the more conservative of the two). Propagated once:

| | Before | After |
|---|---|---|
| Inter-array attraction | 3.68 kN | **2.69 kN** |
| Face pressure | 120 kPa | **88 kPa** |
| Ti side-plate stress | 33 MPa | **24 MPa** |
| Margin against 880 MPa yield | 20.2 | **28.1** |

**A4 is not re-run and its verdict does not change.** It was loaded at 3672 N, **37 % heavier
than the field model supports**, so its 0.0194 mm airgap closure and 33.7 MPa are conservative and
all three of its declared bands still pass. `validation/results/A4_sled_structural.json` records
the overload rather than being regenerated, because re-running a passing analysis at a lighter
load proves nothing that is not already known.

**The retention gate does not move.** P17 listed it as affected; it is sized from a 24 kg ascent
stack at 25 g and has no dependence on the array attraction.

## What this cannot settle

**Whether either numerical method is right.** Both are computed from the same analytic block model
of the magnets — ideal uniform magnetisation, sharp corners, no manufacturing tolerance, no
demagnetisation. They agree with each other about a shared idealisation. **A measurement would
settle it and none exists**, which is E4 again and is the same sentence that applies to every
number in this repository.
