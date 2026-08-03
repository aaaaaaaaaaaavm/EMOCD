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

## If tip-off exceeds the band

That is not necessarily fatal, but it changes the pitch. A deployer that delivers precise
Δv with worse attitude disturbance than a spring is a different product from one that
improves both, and the paper currently implies the latter. Record it, open an E-item, and
adjust the framing before the next submission.

## Output

`validation/results/A7_separation.json`, tip-off rates per axis, lateral/axial velocity
ratio, minimum separation distance over the departure window, plus `tool`, `version`,
`friction_assumption`, `contact_model`, `timestep`.
