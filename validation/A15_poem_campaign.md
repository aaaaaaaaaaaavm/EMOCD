# A15: a twelve-satellite deployment campaign from POEM, propagated in GMAT

**Closes:** nothing on its own. **Exercises** the ConOps adopted in ADR-020 and tests whether the
deployment story this project tells survives an independent propagator.

> ## BANDS DECLARED 2026-08-05. GMAT INSTALLED AND SCRIPTS EXECUTING 2026-08-06.
>
> Everything below the "Acceptance bands" heading was committed **before**
> `validation/gmat/poem_campaign.script.tmpl` existed.
>
> ### The scripts did not run on first delivery, and I said they were cross-checked
>
> **They were rejected by GMAT's interpreter.** `ReportFile` has no `ReportStepSize` field —
> that belongs to `EphemerisFile` — and every one of the three scripts died on it at parse time:
>
> ```
> **** ERROR **** Interpreter Exception: The field name "ReportStepSize" on object
> "repsat01" is not permitted in line:
>    " 260: GMAT repsat01.ReportStepSize = 3600;"
> ```
>
> **My "generated and cross-checked" label was true and misleading.** The cross-check verified
> the *physics* against `astro.py` — semi-major axis to 0.0000 %, which it did correctly — and
> verified that no `@@PLACEHOLDER@@` survived. It never verified that GMAT would accept the
> syntax, because nothing here could. I wrote a caveat about not calling it a run and then let
> "cross-checked" carry more weight than it had earned.
>
> **GMAT R2022a is now installed in this environment** (`/opt/gmat/GMAT/R2022a`), the field is
> removed, and a one-day propagation of R1 returns **"Mission run completed."** with twelve
> report files whose epoch state matches the prediction: SMA 6857.586 km against a predicted
> 6857.59, inclination 51.6°, and RAAN regressing 4.84 °/day against a predicted 4.875.
>
> The integrator was loosened from 1e-11 to **1e-9** with `MinStep` 30 s, because at 1e-11 the
> report step was ~35 s and a 90-day run would emit 222 000 rows per satellite. The question
> A15 asks is secular J2 drift, which does not need that resolution. **That is a change to the
> analysis and it is recorded here rather than made quietly.**

## Result, all three cases, 2026-08-06

GMAT R2022a, 90 days, twelve satellites per case, ~60 000 rows each. Bands at `e067da8`.

| | R1 450/51.6 | R2 350/55.2 | R3 350/9.6 | Band |
|---|---:|---:|---:|---|
| 1 max inclination change | 0.1229° | 0.1220° | 0.1220° | ≤ 0.13° **PASS** |
| 2 altitude extent | 117.2 km | 114.6 km | 114.6 km | ≥ 100 km **PASS** |
| 3 max RAAN change at epoch | 0.1568° | 0.1486° | 0.7315° | ≤ 0.75° **PASS** |
| 4 RAAN spread at 90 d | 367.0° | 364.8° | 366.2° | ≥ 5° **PASS** |
| 5 SMA vs `astro.boosted_elements` | 0.0000 % | 0.0000 % | 0.0000 % | ≤ 0.5 % **PASS** |
| 6 min inter-object separation | 2.275 km | 3.763 km | 22.578 km | **NOT RELIABLY EVALUATED** |

**R3 exercises band 3 hardest**, reaching 0.7315° against a 0.75° limit — the low-inclination
case gives the largest RAAN change per cross-track shot, as predicted, and very nearly fails.

### Band 6 is not a pass and is not recorded as one

The minimum separations above are **sampled**, and the sampling is far too coarse to mean
anything: 4031 samples over 90 days is one point every **1929 s against a 5560 s orbital
period — 2.9 samples per orbit.** Two objects closing at kilometres per second can pass each
other entirely between samples.

So 2.275 km is *a distance seen at three arbitrary points per orbit*, not a minimum. **Band 6
remains unevaluated**, and the honest statement is that A15 has not established inter-object
safety. Closing it needs a real conjunction screen with adaptive refinement near candidate
minima — which is what `astro.py`'s `conjunction()` already does at 0.25 s sampling, and what
**A6** exists for. A6 returned three VOID rows and **P1 is still open**.

**This matters because of band 4.** 367° of nodal spread means the planes wrap and pairs
re-align during the campaign, so close approaches are plausible rather than hypothetical, and
band 6 was the band written to catch exactly that.

## Result, R1 detail: **band 4's prediction was wrong by 28x**

GMAT R2022a, 90 days, twelve satellites, 60 474 rows each. Bands committed at `e067da8`.

| # | Question | Band | Predicted | GMAT | Verdict |
|---|---|---|---:|---:|---|
| 1 | Max inclination change, any one satellite | ≤ 0.13° | 0.1229° | **0.1229°** | **PASS** |
| 2 | Altitude extent | ≥ 100 km | 117.2 km | **117.2 km** | **PASS** |
| 3 | Max RAAN change at epoch | ≤ 0.75° | 0.1568° | **0.1568°** | **PASS** |
| 4 | RAAN spread after 90 days | ≥ 5° | 13.2° | **367.0°** | **PASS** |
| 5 | GMAT SMA vs `astro.boosted_elements` | ≤ 0.5 % | — | **0.0000 %** | **PASS** |

Bands 6, 7 and 8 were **not evaluated**: band 6 needs Cartesian positions the report set does not
carry, band 7 is a property of the script rather than a GMAT output, band 8's Case B is not
generated. They are open, not passed.

### Band 4 passed, and my prediction of it was badly wrong

**367° against 13.2°.** The analytic prediction assumed nodal regression at a *fixed* semi-major
axis, so the differential was frozen at the 0.147 °/day the initial 59 km spread produces. GMAT
propagates with drag, and drag makes the spread **grow**: the satellites left with lower perigees
decay faster, the semi-major axes diverge, and the RAAN rate difference widens with them. The
final SMA range is **6770 to 6848 km, a 78 km spread against the 59 km it started with.**

So the mechanism is not differential J2 at fixed altitude. It is **drag-amplified differential
J2**, and it is roughly 28 times stronger over 90 days than the frozen-altitude estimate.

**This is a pass that should be read carefully.** The band asked for ≥ 5° and got 367°, but a
number that far from prediction means the model behind the prediction was incomplete, not that
the design is 28 times better than thought. Two consequences follow and neither is comfortable:

- **367° is more than a full revolution of relative nodal position.** The planes do not simply
  spread — they wrap, so pairs of satellites re-align in RAAN at some point during the campaign.
  A15 band 6 was the one that would have caught whether that matters, and it could not be
  evaluated.
- **The spread is a decay artefact as much as a design feature.** Satellites separating in plane
  because they are falling at different rates is not the same product claim as satellites placed
  in different planes, and `SUMMARY.md` and the paper should not conflate them.

`docs/RESULTS.md` and the deployment framing need this distinction before either quotes a plane
spread.

## The question, and the thing it is easy to get wrong

VOLLEY's pitch is "twelve satellites, twelve different orbits". This analysis asks an independent
propagator what "different" actually means at 16.388 m/s.

**It is not inclination.** A cross-track impulse of 16.388 m/s against a 7.64 km/s orbital
velocity gives `Δi = 2·asin(Δv/2v)` = **0.123°**. That is the ceiling, it is reached only by
spending the entire shot on plane change and getting no altitude for it, and **any claim of
meaningful inclination spread from this deployer is false.** Band 1 exists to make that
falsifiable rather than merely stated.

**What does separate the planes is J2.** Satellites left at different semi-major axes regress
their nodes at different rates, because `Ω̇ ∝ a^-3.5·cos i`. A prograde-boosted and a
retrograde-boosted satellite differ by ~59 km of apogee, and that difference compounds:

| Reference orbit | Nodal regression | Differential | After 90 days |
|---|---:|---:|---:|
| 450 km, 51.6° | −4.875 °/day | 0.147 °/day | **13.3°** |
| 350 km, 55.2° | −4.717 °/day | 0.141 °/day | **12.7°** |
| 350 km, 9.6° | −8.149 °/day | 0.244 °/day | **22.0°** |

**Two orders of magnitude more plane separation than the impulse itself can buy**, for free, from
a perturbation the deployer does not control. That is the honest version of the claim, and it is
a better one than the version that overstates the Δv.

## Configuration

**Host:** POEM, the PSLV fourth stage operated as a stabilised platform — the flown precedent
ADR-002 and paper §VII already build on. Twelve 3U satellites, one magazine.

**Cadence: 1200 s**, adopted as the ConOps in **ADR-020**, closing P31. Twelve shots span 4.0 h
and about 2.6 orbits, so the shots distribute around the ground track rather than clustering.

**Three reference orbits, run parametrically**, because the result should not be hostage to one
assumed host orbit:

| Case | Altitude | Inclination | Provenance |
|---|---|---|---|
| R1 | 450 km | 51.6° | The repository's own default, used by `astro.py`, A5 and A6 |
| R2 | 350 km | 55.2° | POEM-4-like. **UNVERIFIED — to be confirmed or cited before this is published** |
| R3 | 350 km | 9.6° | POEM-3-like. **UNVERIFIED — same caveat** |

R2 and R3 are written from recollection of published PSLV mission profiles and are **flagged as
unverified inputs in the generated script and in the results JSON**. R1 is the only one traceable
to something already in this repository, and it is the one the bands are set against.

### Two cases

**Case A, VOLLEY only.** Twelve shots at 16.388 m/s, Δv directions mixed across prograde,
retrograde, cross-track and combinations, applied at whatever true anomaly the host has reached.
This is what the deployer can do unaided and it is the case that matters.

**Case B, POEM-assisted.** A host plane-change manoeuvre between shots. Paper §VII already records
that POEM's mass and control authority are **undisclosed**, so this case is parametric in the host
Δv budget and reports the propellant each degree of plane change costs. It is an illustration of
where the capability would have to come from, not a claim that it exists.

---

## Acceptance bands

Declared before the template exists. Each is capable of failing.

| # | Question | Band | What a miss means |
|---|---|---|---|
| 1 | **Largest inclination change of any one satellite**, Case A | **≤ 0.13°** | if the propagator produces more, it disagrees with the rocket equation and one of them is wrong |
| 2 | **Altitude extent**: highest apogee minus lowest perigee, Case A | **≥ 100 km** | the altitude lever is the one that works; below this the "twelve different orbits" claim weakens badly |
| 3 | **Largest RAAN change of any one satellite** from the impulse alone | **≤ 0.75°** | same test as band 1, on the other cross-track axis |
| 4 | RAAN spread after 90 days, from differential J2 | **≥ 5°** | **the band that carries the actual product claim.** Predicted 13–22° |
| 5 | GMAT boosted SMA against `astro.boosted_elements` at epoch | **within 0.5 %** | a fork between the two codes, which is what P19 and A5 exist to catch |
| 6 | Minimum inter-object separation over 90 days | **> 100 m at all times** | a deployment that puts its own satellites into conjunction is not a deployment |
| 7 | Campaign duration | **exactly 12 × 1200 s = 4.0 h** | consistency with ADR-020; a miss means the script and the ADR disagree |
| 8 | Case B: host Δv per degree of plane change | **report**; VOID as a capability claim | POEM's authority is undisclosed (E5) |

### Three of these eight bands were corrected on 2026-08-05, before the run

**Bands 1 and 3 named a fleet spread while their limits were computed as single-shot maxima.**
The physical ceiling is per satellite: 0.123° of inclination and 0.74° of RAAN for one shot
spending its entire Δv on plane change. A campaign firing one satellite cross-track and another
anti-cross-track doubles the *spread* to 0.246° and 1.46° without either satellite exceeding the
ceiling. **The limits are unchanged — 0.13° and 0.75° — and only the named quantity is corrected**,
which is the narrowest possible fix and the one least able to hide a moved goalpost.

**Band 2 was mis-specified differently.** As first declared it read *"apogee spread across the
twelve ≥ 100 km"*, which does not measure what it was for. A prograde impulse at a circular orbit
raises apogee by 58.9 km and leaves
perigee alone; a retrograde impulse lowers perigee by 58.6 km and leaves *apogee* alone. So the
apogee spread alone is only ~59 km and the band would have failed for a reason that has nothing
to do with the machine. The quantity that carries the claim is the **altitude extent**, highest
apogee to lowest perigee, which is ~117 km.

**A15 has not run.** Correcting a band before any result exists, with the correction dated and
the original stated, is the same act `validation/A7_separation_chrono.md` performed under **P30**
— the rule working rather than being bent. Had this been found after a run, the failure would
have stood and the mis-specification would have become a numbered defect.

**Band 4 is the one to watch.** It is the only band here whose failure would damage the product
argument rather than the model. If differential J2 does not separate the planes — because drag
equalises the orbits faster than the nodes drift apart, which is plausible at 350 km — then twelve
satellites from one host end up in twelve orbits that are distinguishable in phase and altitude
but not in plane, and the deployment story has to be told without the word "planes" in it.

**Band 6 is a real safety question, not a formality.** A6 already found the conjunction geometry
fragile (P1), and A6's own three void rows mean this project has never established a defensible
collision probability. Band 6 tests separation distance, which is a robust quantity, rather than
probability, which A6 showed is not.

## What happens at each outcome, fixed now

1. **Bands 1 and 3 fail.** The propagator and the analytic model disagree about something
   elementary. Suspect the script before the physics, and do not publish either number until it
   is resolved.
2. **Band 2 or 4 fails.** The deployment claim narrows, and `SUMMARY.md`, `README.md` and the
   paper's abstract all need their "twelve different orbits" phrasing corrected. That is a P-item.
3. **Band 5 fails.** A fork between `astro.py` and GMAT, which is P19's failure mode repeating.
4. **Band 6 fails.** A new HIGH defect, and the ConOps cadence adopted in ADR-020 has to be
   re-opened, because spacing is what controls it.

**No band may be widened after the reports come back.**

## Provenance

Orbital quantities come from `analysis/astro.py` by import, not by reimplementation, the same rule
`build_scripts.py` already follows so the orbit definition cannot fork. The operating point is
`motor_results.json`. **R2 and R3's orbital elements are the only inputs in this sheet not
traceable to this repository or to `astro.py`, and they are marked unverified everywhere they
appear.**
