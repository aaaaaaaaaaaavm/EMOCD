# Where this project stands against the published work, and what to do about it

[`PRIOR_ART.md`](PRIOR_ART.md) records what five works say and what reading them changed.
[`LITERATURE.md`](LITERATURE.md) is a 163-entry reading list with provenance markers. Neither
answers the question a reviewer will actually ask, which is what this project intends to *do*
about any of it.

This file is that answer, organised by action rather than by author. A survey nobody acts on is
decoration.

**Nothing here may support a number in the paper.** The rule from `RELATED_WORK.md` holds: only
the five works marked read in `PRIOR_ART.md` are citable, and only for what they actually say.

---

## Adopt

| From | What | Status |
|---|---|---|
| Feng, Yang & Wu 2025 | **Reachable-domain analysis.** A 3-D envelope of the orbits one shot makes available, reconstructed by an alpha-shape algorithm | **PII-6**, deferred behind the A5 re-run |
| Xu *et al.* 2024 | **Attitude-disturbance cost for magazine indexing.** They optimise transfer paths against the pointing error the transfers themselves cause | **E24**, open and unmodelled |

Both are cases where a competitor answers a question this project either answers more narrowly
or has not asked. The reachable domain is strictly better than a scalar lifetime multiplier: a
deployer selling *programmable per-satellite velocity* should be able to state what that
velocity buys as a region.

E24 is the sharper one, because it was found by reading someone else's problem statement rather
than by examining this design. This project budgets 65.6 N·s of recoil from the shot and nothing
at all from moving a few kilograms of satellite across the structure between every pair of
shots. The quantity that matters is residual attitude rate at trigger, and it does not exist
anywhere in this repository.

## Cite, and for exactly what

| Work | Supports | Does **not** support |
|---|---|---|
| Feng, Yang & Wu 2025 | That on-orbit electromagnetic CubeSat launch is published prior art; the g-limit argument (1352 g mean, ~3060 g peak on a 20 kg body); coilgun efficiency at **14.9-19.9 %** | Any claim about dispersion. They quote none |
| Zhao *et al.* 2022 | Stacked-CubeSat electromagnetic deployment as precedent | Ejection velocity. It is a release mechanism, not a launcher |
| Xu *et al.* 2024 | Magazine-fed electromagnetic transport, and the disturbance problem | Anything about exit velocity |
| Zhao *et al.* 2025 | **The only measured comparator**: a built storage prototype, 32.8 mm/s transport | An electromagnetic launcher. It measures slow transport, not ejection |
| Einat & Orbach 2023 | A measured multi-stage reluctance launcher at 130 m/s, and a useful field survey | Anything at CubeSat scale. The projectile is **2.5 g** |

## Avoid

**Efficiency figures quoted out of their scale.** ADR-003 asserted coilgun efficiency of
"1-2 % in the literature" with no source. It was false, and it stayed live in the paper's own
trade table, the wiki and two docs for a day after being retracted in four other places. That is
**P25**, and the general lesson is that a retraction is not propagated until the artifacts move.

**Abstract-level conclusions.** `PRIOR_ART.md` was first written from abstracts and **three of
its conclusions were wrong**, including whether Feng had built hardware. All three are listed
there as corrections rather than silently fixed. Read the full text or say the entry is
abstract-level.

**Assuming a comparator's maturity from its venue.** Zhao 2025 sounded like a validated launcher
and is a measured transport mechanism. Feng sounded like it might be hardware and is simulation
throughout, the phrase "experimental results" appearing twice and meaning simulation runs both
times.

## Replicate

Zhao *et al.* 2025 built a prototype and reported observed collisions, including ones their
model did not predict. That is the standard [`BENCHTOP_TESTS.md`](BENCHTOP_TESTS.md) is written
to, and **B-1 is this project's equivalent at roughly ₹22,000**: two magnetisation directions,
eight blocks, a teslameter, and an afternoon.

The gap is not that this project lacks a launcher. It is that it has measured nothing at any
scale, and B-1 closes that for the price of two magnets.

## Concede

**Every comparable group has either hardware or a longer measurement record.** The paper says
so, `SKILLS.md` says so, and neither should stop saying it. Two of this project's three
cross-checks are model-against-model.

On maturity, this project and Feng's are peers: both are TRL 2-3 design studies. The Harbin line
is ahead on hardware and behind on velocity. Stating that plainly is more defensible than
claiming a lead that a reviewer with the comparison memorised will not grant.

---

## The gap the reading list found in itself, and what it cost

[`LITERATURE.md`](LITERATURE.md) sorts 163 entries into nine clusters. Until 2026-07-31,
**pulsed power and capacitors had two**, and the file named that cluster as the sample's blind
spot in its own words: reference harvesting inherits the biases of the papers harvested, and the
source set was coilgun-heavy and deployer-heavy.

On 2026-07-30 the supercapacitor bank was found to be specified at an ESR no commercial cell of
that capacitance achieves, and the shot does not close at a realistic value. That is **P26**, and
it is currently the largest open defect in the project.

**The one cluster nobody filled is the one that turned out to carry a defect big enough to stop
the machine.** That is worth more than any single citation in this file: a reading list that
honestly reports its own coverage tells you where to expect trouble, and this one did.

**So the next reading was not more prior art.** The cluster was filled on 2026-07-31 by a
targeted database search rather than by harvesting, taking it from 2 entries to 29: ESR
definition and measurement, ageing and derating, pulse-forming networks and capacitor-bank
architectures from the railgun community, lithium-ion capacitors including one flown system, and
SiC device literature for the drive the paper specifies without citing anything.

**That is a list, not an argument, and the distinction is the whole point of this file.** None of
it has been read. Two things the search surfaced already sharpen P26 — the published end-of-life
criterion for these parts is a **two-fold ESR increase**, and operation to −40 °C can **double
ESR without shortening life**, against an A10 ceiling with no margin for either — but a headline
returned by a search engine is not a result. PII-7 still cannot be argued until the three to five
entries bearing directly on P26 are read in full and a cell is chosen from a manufacturer
datasheet.
