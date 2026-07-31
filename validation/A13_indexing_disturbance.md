# A13: what indexing and sled return do to the host's attitude

**Closes:** `OPEN_PROBLEMS.md` **E24**, and `docs/KILL_CRITERIA.md` §5.
**Does not close:** E7. The dispersion claim's *sensor* assumption is a different gap.

## Why this exists

`analysis/astro.py` computes recoil as one line:

```python
res['recoil_Ns_per_shot'] = round(4.0 * DV, 1)
```

Payload mass times exit velocity. **That is the entire host-interaction budget in this
repository**, and it accounts for the shot alone.

Between every pair of shots, two other masses move:

- a **cassette follower advances a satellite** across the structure, transversely, so the
  system centre of mass shifts and the host sees a torque that is not the shot recoil;
- the **sled returns to the breech**, 9.445 kg travelling 1.5 m back along the track.

Neither appears in any budget here. E24 found this by reading a competitor's problem statement
(Xu et al., *Aerospace* 11(5) 394, 2024) rather than by examining this design, which is worth
restating because it says something about how the gap survived.

**This is the same class of defect as the bank ESR (P24): a budget published as if complete that
omits a term the hardware will have.** That makes it a Phase I error correction rather than an
improvement.

## The thing this analysis is forbidden from concluding

E24 ends: *"Explicitly **not** claimed to be negligible until that is done."* It also says why —
**P16 was "probably fine" until an independent propagator was pointed at it.**

So the bands below must be capable of failing, and the deliverable is a number with a band it
could have missed, **not a paragraph concluding that the disturbance is small**. If the numbers
come back small, that is a result; if the write-up *begins* from smallness, it is not an analysis.

## What is modelled, and what is assumed

| | |
|---|---|
| Indexed mass | one 3U satellite, 4.0 kg, across the cassette pitch |
| Sled return | 9.445 kg over the 1.5 m track, back to the breech |
| Deployer | 124.9 kg loaded (`mass_properties.json`), inertia from the CAD envelope |
| **Host** | **swept, not chosen.** 200 to 5000 kg with inertia scaled to a representative bus |
| Damping | none. Momentum exchange is treated as ideal and rigid |

**The host inertia is the weakest input, so it is swept rather than picked** — the posture A6
took with the covariance it could not obtain. Results are reported as a function of it, and a
conclusion that holds only at the heavy end must say so.

**Rigid-body only.** Structural modes are not modelled, so "settling time" here means the time to
null a rigid-body rate with reaction control, **not** the time for structure to stop ringing. That
second question is real and this analysis does not touch it.

## Acceptance bands, declared 2026-07-31 before `analysis/attitude_budget.py` existed

| # | Quantity | Prediction | Accept if |
|---|---|---|---|
| 1 | Indexing impulse, one satellite advanced | small against the shot's 66.1 N·s | **below 10 %** of the shot impulse |
| 2 | Sled-return impulse | comparable to indexing, opposite sense | **below 20 %** of the shot impulse |
| 3 | Peak attitude rate from one index cycle, 500 kg host | **below 0.05 °/s** | below 0.05 °/s |
| 4 | Same at the light end, 200 kg host | below 0.2 °/s | below 0.2 °/s |
| 5 | Settling to below 0.01 °/s with a 0.1 N·m RCS authority | **fast against the 10–20 s inter-shot interval** | **under 2 s at 500 kg** |
| 6 | Net momentum over a full 12-shot campaign, indexing only | **near zero**: the followers return and the CoM comes back | below 5 % of one index impulse |
| 7 | Whether the indexing term changes the campaign propellant bill | **no** | the 0.98 kN·s campaign figure moves by less than 2 % |

**Falsification.** Row 3 or 4 missing means the deterministic-placement claim needs a settling
requirement written into the ConOps before the next shot, and the 0.027 m/s dispersion figure
inherits an error the velocity servo cannot see — it measures position along the track, not the
track's orientation. Row 6 missing would mean the indexing sequence has a secular momentum bias,
which is a design defect in the feed order and is exactly what Xu et al. optimise against.

**Row 5 is the one that matters operationally**, because it is the only one that interacts with
the cadence. A disturbance that damps in 2 s is bookkeeping; one that damps in 200 s changes the
campaign.

## Output

`analysis/results/attitude_budget.json`: impulses, peak rate against host mass, settling time,
campaign momentum, and the assumed host inertia model stated explicitly.

---

## Result, run 2026-07-31. Verdict **FAIL**, four of seven

`analysis/attitude_budget.py`, written after the bands above were committed in `f11a93d`.

### One index cycle

| | Mass | Distance | Duration | Peak momentum | Against the shot's 66.1 N·s |
|---|---|---|---|---|---|
| Satellite advanced | 4.00 kg | 104 mm | 4 s | 0.208 N·s | **0.31 %** |
| **Sled returned** | **9.445 kg** | **1500 mm** | **6 s** | **4.723 N·s** | **7.14 %** |

### Attitude rate, host inertia swept

| Host | Inertia | From indexing | **From sled return** | Total | Settling at 0.1 N·m |
|---|---|---|---|---|---|
| 200 kg | 63 kg·m² | 0.031 °/s | **0.709 °/s** | **0.740 °/s** | 8.2 s |
| **500 kg** | 292 kg·m² | 0.007 °/s | **0.154 °/s** | **0.161 °/s** | **8.2 s** |
| 1000 kg | 926 kg·m² | 0.002 °/s | 0.049 °/s | 0.051 °/s | 8.2 s |
| 2000 kg | 2940 kg·m² | 0.001 °/s | 0.015 °/s | 0.016 °/s | 8.2 s |
| 5000 kg | 13538 kg·m² | 0.0002 °/s | 0.003 °/s | 0.003 °/s | 8.2 s |

### Against the declared bands

| # | Prediction | Result | |
|---|---|---|---|
| 1 | indexing impulse below 10 % of shot | **0.31 %** | **pass** |
| 2 | sled-return impulse below 20 % of shot | **7.14 %** | **pass** |
| 3 | peak rate below 0.05 °/s at 500 kg | **0.161 °/s** | **FAIL, 3.2x over** |
| 4 | peak rate below 0.2 °/s at 200 kg | **0.740 °/s** | **FAIL, 3.7x over** |
| 5 | settle below 0.01 °/s in under 2 s | **8.2 s** | **FAIL, 4x over** |
| 6 | campaign secular momentum near zero | 0, by construction | **pass** |
| 7 | campaign propellant bill unchanged | unchanged | **pass** |

**Four of seven, and the three that failed are the three that mattered.**

### E24 was worried about the wrong mass

E24 is titled *"Attitude disturbance from magazine indexing"* and its argument is about
satellites moving inside the deployer. **Indexing is negligible: 0.31 % of the shot impulse, and
0.007 °/s at a 500 kg host.** E24's own instinct that "the indexed mass is a few kg against a
124.9 kg loaded system" was right.

**It is the sled return that does the damage, and nothing in E24 or anywhere else in this
repository mentions it.** 9.445 kg travelling 1.5 m is **23x the indexing momentum** — a heavier
mass over fourteen times the distance — and it is the largest unbudgeted term in the host
interaction by a wide margin.

That is the finding. The gap was found by reading a competitor's problem statement, the
competitor's problem was the indexing, and **this design's problem is somewhere that paper never
had to look** — because a machine that does not reuse its sled does not return one.

### What this costs the deterministic-placement claim

At a 500 kg host, one index cycle leaves **0.16 °/s** and nulling it takes **8.2 s against a
10–20 s inter-shot interval**. That is most of the cadence spent settling, and the settling time
is independent of host mass — the momentum to remove is fixed and so is the assumed authority.

**The velocity servo cannot see any of it.** It measures position along the track, not the
track's orientation, so a residual attitude rate at trigger becomes a pointing error that the
0.027 m/s dispersion figure does not include and cannot detect.

### What would pass, which is not the same as passing

The sled return duration is a **free variable nobody has specified**. Peak momentum goes as
`1/T`, so:

| Return duration | Peak momentum | Rate at 500 kg | Settling | Band 3 | Band 5 |
|---|---|---|---|---|---|
| 4 s | 7.08 N·s | 0.238 °/s | 12.1 s | FAIL | FAIL |
| **6 s, assumed** | **4.72 N·s** | **0.161 °/s** | **8.2 s** | **FAIL** | **FAIL** |
| 10 s | 2.83 N·s | 0.099 °/s | 5.1 s | FAIL | FAIL |
| 15 s | 1.89 N·s | 0.068 °/s | 3.5 s | FAIL | FAIL |
| 20 s | 1.42 N·s | 0.053 °/s | 2.7 s | FAIL | FAIL |
| 30 s | 0.94 N·s | 0.038 °/s | 1.9 s | pass | pass |

**Nothing inside the cadence passes.** The inter-shot interval is 10–20 s, and the bands are only
met at a 30 s return, which does not fit. **The bands failed and this table does not un-fail
them**; it says what the design would have to become.

Three routes, none costed here:

1. **Slow the return and lengthen the cadence.** A 30 s return inside a 40 s interval. Costs
   campaign duration, which nothing currently constrains.
2. **More control authority.** Settling scales as `1/torque`; 0.4 N·m brings 8.2 s to 2.0 s. That
   is a *host* requirement, not a deployer one, and it belongs in the four-item interface spec,
   which currently does not ask for it.
3. **Return the sled against a counter-mass.** A reaction mass moving opposite cancels the
   momentum at source. It is the only route that fixes the disturbance rather than absorbing it,
   and it costs deployer mass on a design already failing kill criterion 1.

### The honest limits of this

**Rigid-body only.** "Settling" is reaction control nulling a rate. It is **not** structure
ringing down, so E24's concern about "structural motion that has not damped out" is only half
answered.

**The motion profiles are assumed, and they are the optimistic end.** Both are the slowest
constant-acceleration moves that plausibly fit the interval. A faster mechanism makes every number
here worse.

**The host inertia is a uniform cylinder scaled from mass.** It is swept rather than chosen for
exactly that reason, and **the failure holds across the whole sweep below 1000 kg**.
