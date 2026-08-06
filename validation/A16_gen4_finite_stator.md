# A16: thrust against sled position when the array leaves the stator

**Closes:** `OPEN_PROBLEMS.md` **E27**. **Does not close P32** — P32 needs one controlled
propagation of every dependent result, which this analysis deliberately does not perform.

> ## RUN 2026-08-05. Verdict **both testable bands PASS — and Gen4 does not reach the Phase I velocity**
>
> Bands committed at **`13b4b3b`**, before `analysis/gen4_finite_stator.py` existed. None widened.
>
> | # | Question | Band | Result | Verdict |
> |---|---|---|---:|---|
> | 1 | Fully-overlapped thrust vs the periodic result | within 2 % | **0.000 %** | **PASS** |
> | 2 | Thrust at release, s = 1200 mm | report | **782.5 N**, 56.3 % of full | reported |
> | 3 | Monotonic non-increasing through the run-out | yes | yes | **PASS** |
> | 4 | Exit velocity over the 900 mm stroke | report only | **13.390 m/s** | **not adopted** |
> | 5 | Ratio to the Phase I 16.388 m/s | report | **0.817** | reported |
>
> **The Gen4 stationing costs 18.3 % of exit velocity, and this is an upper bound.**

## Result, 2026-08-05

Thrust per metre of overlapped array is **4086.0 N/m**. At full overlap that gives
**1389.255 N**, reproducing `motor_results.json`'s `F_cmd` to **0.000 %** — band 1's whole
purpose, and the one regime where this analysis and the periodic model describe the same physics.
Agreement there means the finite integration is sound and the run-out numbers are not an
implementation artefact.

Force at release falls to **782.5 N**, which is **56.3 %** of full — exactly the overlap fraction.
That is expected from a truncation model and is precisely why band 2 was declared *report* rather
than pass/fail: the proportionality is an output of the method, not evidence about end fields.

### The finding

**Work over the 900 mm stroke is 1205.3 J against the Phase I 1806 J over 1300 mm, and exit
velocity comes out at 13.390 m/s — 81.7 % of 16.388.**

Two effects compound. The stroke is 400 mm shorter, and the last 148.5 mm of it runs at
declining force. Neither is a defect in the CAD; both are consequences of a stationing chosen to
give the brake a physical interaction interval without lengthening the track
(`docs/GEN4_STATUS.md`).

**And 13.390 m/s is an upper bound.** The method truncates an otherwise-periodic winding, so it
captures lost energised length and nothing else — no end fields, no winding termination, no
phase-progression disturbance at the boundary. Every one of those is named in E27 and every one
of them subtracts. The real Gen4 figure is below this.

### What this does and does not settle

**E27 is closed**: a position-dependent force calculation now exists, its inputs and stations come
from the recorded Gen4 geometry, and it agrees with the periodic model where it should.

**P32 stays open, and this makes it sharper rather than smaller.** P32 is not "there is no
calculation" — it is that the working geometry has no corresponding *operating point*, and
producing one needs a controlled propagation through power, energy, thermal, braking, orbit,
paper and validation records. This analysis performs none of that.

**No number here is a Gen4 performance figure.** The export gate in `docs/GEN4_STATUS.md` stays
closed. What has changed is that the gate now has a number behind it: **a Gen4 built to the
current stationing would be an 18 % slower machine**, and that is a design decision to take
deliberately rather than discover after export.

---

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
