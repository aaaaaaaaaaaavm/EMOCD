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

`validation/results/A13_indexing.json`: impulses, peak rate against host mass, settling time,
campaign momentum, and the assumed host inertia model stated explicitly.
