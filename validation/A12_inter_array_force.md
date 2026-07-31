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

## What this cannot settle

**Whether either numerical method is right.** Both are computed from the same analytic block model
of the magnets — ideal uniform magnetisation, sharp corners, no manufacturing tolerance, no
demagnetisation. They agree with each other about a shared idealisation. **A measurement would
settle it and none exists**, which is E4 again and is the same sentence that applies to every
number in this repository.
