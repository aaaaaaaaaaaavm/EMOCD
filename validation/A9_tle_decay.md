# A9: Decay rate against flown CubeSats (TLE history)

**Closes:** the half of `OPEN_PROBLEMS.md` E6 that A5 could not. **Status: SPECIFIED, NOT RUN
the data source is unreachable from the working environment.**

Every validation this project has run compares one model against another model. A5 put
`astro.py` against GMAT: two independently implemented force models, which is a real check
and caught a real defect (P16). It is still two models. **This analysis is the only one
specified anywhere in `validation/` that would compare the model against something that
actually happened.**

Roughly 3-5 non-manoeuvring 3U CubeSats have decayed from the 450-500 km band with public
element-set histories covering the whole descent. Fitting their mean-motion history gives a
measured decay rate at a known altitude and an inferable ballistic coefficient. That is a
measurement, not an output.

## Why it is not run

CelesTrak and Space-Track are blocked by this environment's network policy, `curl` and the
fetch tooling both receive `403` on `CONNECT`, logged by the proxy as a policy denial rather
than an upstream failure. **No workaround was attempted.** The script is written and the
bands are declared; running it needs a machine with ordinary internet access and a free
Space-Track account.

## Inputs

- **Object selection.** 3U CubeSats, no propulsion, decayed from 450-500 km, with element
  sets spanning at least the final 200 days. Flock and Lemur series are the obvious
  candidates, same mass class as the paper's comparator, and numerous enough to pick
  non-manoeuvring members.
- **Exclusion rule, applied before fitting:** discard any object whose mean motion shows a
  discontinuity inconsistent with drag. Differential-drag attitude control counts as a
  manoeuvre for this purpose, and Planet's satellites do exactly that, which is precisely
  why the selection has to be deliberate rather than convenient.
- **Ballistic coefficient** inferred from the fit, then compared against `astro.py`'s 61
  kg/m² nominal. Not assumed equal.
- **Space weather:** actual F10.7 and Ap over each object's decay window, not a nominal level.
  Using nominal activity against a real decay would test nothing.

## Acceptance band (declared 2026-07-29, before any run)

| Quantity | Reference | Band |
|---|---|---|
| Decay-rate ratio, `astro.py` vs fitted, per object | 1.0 | **within a factor of 2** |
| Median across the object set | 1.0 | **±40 %** |
| Sign consistency of the error across objects | | **report; a sign change is a finding** |
| Inferred BC vs `astro.py` nominal 61 kg/m² | | **report only, no pass/fail** |

### Why these bands are wide, and why widening them is not cheating

Shambaugh (arXiv 2601.02453, `docs/RELATED_WORK.md`) backtests a purpose-built lifetime
pipeline against 934 decayed satellites and reports **12.4 % median error under fully
predictive conditions**, with estimated ballistic coefficients and forecast space weather,
which is the honest comparison. That is the state of the art for tooling far more careful
than a static exponential atmosphere.

`astro.py` uses a static exponential table. Holding it to a tighter band than the state of the
art would guarantee a failure that says nothing. **±40 % on the median is roughly three times
the best achievable**, which is the right posture for a model that does not attempt space
weather at all.

**The sign-consistency row is the one that matters most.** A5 found that `astro.py`'s error
against GMAT *changes sign* across the activity range, 2.5x long at low activity, 23 % short
at high, and an error that changes sign is a wrong profile shape, not a calibration offset.
If the same sign change appears against flown data, that is independent confirmation of the
P16 mechanism from a direction no model can supply.

## Method

`validation/tle/fit_decay.py`, written and committed unrun.

1. Fetch element-set history per NORAD ID (Space-Track `gp_history`, or CelesTrak for recent
   objects). Free account, no approval delay.
2. Convert mean motion to semi-major axis per object per epoch.
3. Least-squares fit of decay rate over sliding windows, **rate, not endpoint difference.**
   A5 established why: reported SMA is osculating and its short-period variation exceeded the
   decay over a 30-day window by several times. The same trap applies here and is worse,
   because TLE-derived elements carry their own noise on top.
4. Drive `astro.py` `lifetime()` at each object's altitude and inferred BC over the same
   window, with matched solar activity.
5. Compare rates. Apply the bands above. Emit `validation/results/A9_tle_decay.json`.

## On failure

The standing rule: **open a P-item, do not edit `analysis/astro.py`.** If the model
disagrees with flown data outside the band, that is a finding about the atmosphere model, and
the correct response is a variable-shape atmosphere or a narrowed claim, a decision, not a
patch. E6 already concedes absolute lifetimes are uncertain; this would tell us *how*
uncertain, against reality rather than against another model.

## What a pass would buy

`PROVENANCE.md` can currently say of every number in this project that it is a model output.
A pass here would not change that for the machine, but it would mean the astrodynamics half
reproduces something that physically occurred, which is a different class of claim from
anything the repository currently makes.

---

## Candidate objects, assembled 2026-07-31

**Re-tested on 2026-07-31 and the block is real.** `celestrak.org:443` returns 403 at the CONNECT,
logged by this environment's proxy as a policy denial rather than an upstream failure. Space-Track
needs an account regardless. **A9 still cannot run here.**

What was missing besides the data was the *object selection*, and that can be built from published
mission records without touching the element feed. It is done below, so this run becomes an
afternoon on a machine with ordinary internet rather than an open-ended research task.

### Why QB50 is the right cohort

QB50 was a constellation of 2U and 3U CubeSats built to measure the lower thermosphere. It has
three properties nothing else in this altitude band has together:

1. **No propulsion, by design.** The orbits decayed under drag alone, which was the point of the
   mission.
2. **Two cohorts at two altitudes.** Twenty-eight deployed from the ISS in May 2017 at ~400 km,
   all reentered by December 2018 — nineteen months of continuous decay. Eight more launched on
   **PSLV-C38, 23 June 2017, into ~505 km SSO**, which is the band A9 specifies.
3. **Long element histories**, because they were tracked from deployment to reentry.

### The shortlist

| Object | SATCAT | Form | Orbit at launch | Decayed | |
|---|---|---|---|---|---|
| **Aalto-1** | **42775** | 3U | ~505 km SSO | 2024-09-01 | **Primary candidate**, seven years of history — *conditional on the check below* |
| URSA MAIOR | 42776 | 3U | ~505 km SSO | | QB50 |
| UCLSat | 42789 | 3U | ~505 km SSO | | QB50 |
| VZLUSAT-1 | 42790 | **2U** | ~505 km SSO | 2023-06-06 | Six years. **2U, so a different area-to-mass ratio** — usable as a cross-check, not as a 3U datum |

**Aalto-1 carries an electrostatic plasma brake payload and that must be checked before it is
used.** If the brake was deployed, Aalto-1 is a manoeuvring object under the sheet's own exclusion
rule and must be discarded — a deorbit device is exactly the class of thing that rule exists to
catch. If it was never successfully deployed, Aalto-1 is the best object available. **This is the
first thing to verify and it decides the primary candidate.**

### Explicit exclusions

| | |
|---|---|
| **InflateSail** (same launch) | deployed a drag sail and decayed in about 72 days. A deorbit device, excluded by the rule |
| **QARMAN** (QB50) | carried an aerobrake for a re-entry experiment. Excluded for the same reason |
| **Planet Flock** | flies differential-drag attitude control, which the sheet already names as a manoeuvre |

### What is verified here and what is not

- **Launch dates, altitudes, form factors and the two decay dates** come from published mission
  records and are reliable at the level quoted.
- **The SATCAT numbers are not confirmed against the catalogue.** They trace to a Doppler-based
  identification of the PSLV-C38 cluster, which is how objects from a multi-satellite deployment
  get attributed before official association settles. That is exactly the kind of provisional
  identification that is sometimes revised. **Confirm each against the catalogue before fitting**,
  and if an object's launch epoch and initial orbit do not match the table above, it is the wrong
  object.
- **This is a candidate list, not a selection.** The exclusion rule in the sheet above is applied
  at run time against the actual element history, not here.

### Worth considering: widen the band to include the ISS cohort

A9 specifies 450–500 km. The ISS-deployed QB50 cohort sits at ~400 km and is otherwise ideal —
twenty-eight objects, no propulsion, complete decay histories, all reentered inside nineteen
months. **Widening to 380–520 km would take the sample from three or four objects to roughly
thirty**, which matters because the declared band is a *median across the set*.

**That is a change to a declared band and it is not made here.** If it is wanted, it should be
declared as an amended band, dated, and before any fitting — the way A7's band was tightened on
2026-07-31 and the way A6's was re-declared.

### To run it

```
export SPACETRACK_USER=... SPACETRACK_PASS=...
python3 validation/tle/fit_decay.py --norad 42775 42776 42789 --out validation/results/A9_tle_decay.json
```

A free Space-Track account takes a few minutes to obtain. The script is 180 lines and has never
been executed — **expect to debug it**, and note that a first run that crashes is not a band
failure and must not be recorded as one.

**Why this is worth an afternoon.** Every result in this repository is one model checked against
another model. Eight validations have run and not one of them has compared anything here to a
measurement. A9 is the only specified analysis anywhere in the project that would.
