# A15: a twelve-satellite deployment campaign from POEM, propagated in GMAT

**Closes:** nothing on its own. **Exercises** the ConOps adopted in ADR-020 and tests whether the
deployment story this project tells survives an independent propagator.

> ## BANDS DECLARED 2026-08-05. NOT RUN — and it cannot be run here.
>
> Everything below the "Acceptance bands" heading was committed **before**
> `validation/gmat/poem_campaign.script.tmpl` existed.
>
> **GMAT is not installed in this environment.** The script is generated and cross-checked
> against `analysis/astro.py` here; the GMAT execution happens elsewhere and the reports come
> back to `parse_reports.py`. Until they do, this sheet says **generated and cross-checked, not
> executed**, and it must not be described as a run. A1 spent a day mislabelled in
> `validation/README.md` for exactly this reason.

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
