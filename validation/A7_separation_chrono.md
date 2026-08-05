# A7: Separation and tip-off (Project Chrono)

**Relates to:** `OPEN_PROBLEMS.md` E7 (dispersion rests on assumed sensor noise) and the
tip-off claims in the paper, which are model outputs with no multibody model behind them.

Unlike A1 and A4, this one has a **measured benchmark to compare against**: spring
deployers have flown thousands of times and their tip-off performance is published.

## Inputs

- Geometry and masses: `cad/step/gen3/EMOCD_Sled_Gen3.step`,
  `cad/step/gen3/EMOCD_Payload_3U_Gen3.step`,
  `cad/parameters.json` (payload CDS corner rails, sled cradle, release at x = 1500 mm)
- Release conditions: exit velocity **16.388 m/s at 10.53 g** (`docs/BASELINE.md`). The sheet
  said 20.37 m/s at 16.3 g until 2026-07-31; that is the operating point abandoned when the
  CAD-derived sled mass was adopted (P15), and running against it would have been **P19** a third time.
- Contact: rail-on-cradle friction, coefficient stated as an assumption

## Acceptance band, **tightened 2026-07-31, before running**

> **Read this before the table, because a band that moves looks exactly like the thing this
> directory forbids.** The rule is that a band may not be edited *after seeing results* —
> `A1_field_femm.md` kept a band it failed for precisely that reason. **A7 has never run. There
> are no results.** Tightening it now, against a source, is the rule working rather than being
> bent. Doing it after a run would be indefensible; doing it before is the only chance.

### What was wrong with the old band, and it was not the number

The sheet declared **≤ 5 °/s**, citing the NRCSD-E interface document, and `OPEN_PROBLEMS.md` E7,
`docs/KILL_CRITERIA.md` §4 and PII-1's entry criterion all carried a flag that this "conflicts"
with a sibling NRCSD ICD quoting 2 °/s, unresolved.

**There is no conflict. They are two different deployers**, and both figures are correct:

| | Tip-off target | |
|---|---|---|
| **NRCSD**, internal, deployed through the ISS airlock | **< 2 °/s/axis** | flown many hundreds of times |
| **NRCSD-E**, external, mounted on Cygnus | **< 5 °/s/axis** | and NanoRacks states in the same document that *"additional testing and analysis are being completed... to refine and verify this value"* |

**So the flag dissolves and what it was hiding is worse than what it claimed.** The band was set
at the looser of two available comparators, taken from the document whose own publisher calls the
figure provisional, with no record that a tighter flown number existed. That is not a wrong
number — it is a band picked at the easy end of the evidence, which is the failure mode acceptance
bands exist to prevent. Logged as **P30**.

| Quantity | Criterion | Basis |
|---|---|---|
| **Tip-off rate, any axis** | **≤ 2 °/s** | **NRCSD IDD, internal deployer, < 2 °/s/axis.** The tighter of the two, from the one that has actually flown at scale. This is the number VOLLEY has to match to claim a benign release |
| Tip-off rate, secondary reference | ≤ 5 °/s | NRCSD-E. Recorded so a result between 2 and 5 °/s can be reported against both, and **flagged as provisional by its own publisher** |
| Re-contact after release | none, through 2 m of separation | fire-then-arrest ConOps assumes clean departure |
| Lateral velocity component | ≤ 2 % of axial | otherwise the ±0.10 km apogee placement claim is optimistic |

Beating a flown spring deployer on tip-off is a *claim VOLLEY makes implicitly* by positioning
itself as a controlled alternative. Putting a flown number in the band makes that claim
falsifiable rather than rhetorical — **and putting the flown number rather than the convenient one
is what makes it worth falsifying.**

> **What this costs, stated plainly.** A7 is now 2.5x harder to pass than it was, on a design
> whose release path has no multibody model behind it and whose payload centre of mass sits 70 mm
> off the thrust line (`cad/parameters.json`). A result between 2 and 5 °/s is now a *miss*, where
> yesterday it was a pass. That is the correct posture and it should be expected to hurt.

## A7-R, 2026-08-05: the tolerance the release mechanism has to hold

> **A7 itself remains UNRUN.** This is a reduced analysis and it does not produce a tip-off rate.
> Project Chrono is unavailable here, and — the more important reason — **the release mechanism it
> would simulate is not defined anywhere in this repository.** The paper says force is removed in
> the coast-trim zone and the sled then enters the brake while the satellite departs. It does not
> say how the cradle rails disengage, in what order, with what friction, or over what time. A
> multibody model of an undefined mechanism produces a number with no provenance.
>
> So A7-R asks the question that *is* answerable from the geometry already fixed in
> `cad/parameters.json`: **how symmetric does the release have to be to meet the 2 °/s band?**

The payload's centre of mass sits **70 mm off the thrust line**. Any longitudinal force not
reacted by a balancing couple torques it about the transverse axis. During acceleration the cradle
supplies that couple. Tip-off is whatever angular impulse survives the moment it stops.

With a 4.0 kg 3U at a transverse inertia of 0.04198 kg·m² and a 413.2 N push at 10.533 g, the
**entire angular-impulse budget for a 2 °/s release is 1.465 mN·m·s.**

| Unbalanced force | may persist for |
|---|---:|
| Full push, 413.2 N | **50.7 µs** |
| 10 % of push, 41.3 N | 507 µs |
| 1 % of push, 4.13 N | 5.07 ms |
| Force ripple alone, 4.09 N | 5.12 ms |
| 1 N of latch, harness or friction residual | 21 ms |

| If the asymmetry lasts | max unbalanced force |
|---|---:|
| 0.01 ms | 2093 N |
| 0.1 ms | 209 N |
| 1 ms | **20.9 N** |
| 10 ms | **2.09 N** |

### What this says

**The release is a microsecond-class symmetry problem at full force, or a newton-class one at
millisecond timescales.** If the cradle rails disengage even slightly out of step while the push
is still on, 50 µs of it spends the whole budget. If the push is genuinely zero by release — which
is what the coast-trim zone is for — then the binding term is residual latch, harness and friction
forces, and **1 N acting for 21 ms is enough to fail the band.**

**That makes the coast-trim zone load-bearing for tip-off, which nothing in this repository
currently says.** It is described as the zone where the servo makes its final velocity correction.
On these numbers its more important job may be ensuring the push is off *before* the constraint is
released. Whether it does that is a mechanism question, not an analysis one.

**This does not close A7 and does not close E7.** It converts them into a specification the
mechanism designer can be handed, and it says what has to be defined before Chrono would be worth
running: the disengagement sequence, its timing tolerance, and the residual force at release.

## If tip-off exceeds the band

That is not necessarily fatal, but it changes the pitch. A deployer that delivers precise
Δv with worse attitude disturbance than a spring is a different product from one that
improves both, and the paper currently implies the latter. Record it, open an E-item, and
adjust the framing before the next submission.

## Output

`validation/results/A7_separation.json`, tip-off rates per axis, lateral/axial velocity
ratio, minimum separation distance over the departure window, plus `tool`, `version`,
`friction_assumption`, `contact_model`, `timestep`.
