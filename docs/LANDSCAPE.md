# Where VOLLEY sits against what actually flies

An honest comparison of this design study against fielded CubeSat deployers and the
last-mile transfer vehicles at the other end of the market.

> **Source status.** VOLLEY's own figures come from `analysis/results/*.json` and are model
> outputs. Competitor figures were collected from vendor and agency material on 2026-07-28
> and are **recorded as leads, not verified**: the same E16 rule that applies to
> `RELATED_WORK.md`. Fetch and read the primary document before any of these numbers enters
> `paper/paper.tex`. Where a figure could not be pinned down, this file says so rather than
> estimating.

## The three families

| | **Spring deployers** | **VOLLEY** | **Orbital transfer vehicles** |
|---|---|---|---|
| Examples | P-POD, ISIPOD, NRCSD, CSD, EXOpod, **Dhruva DSOD** | this design study | D-Orbit ION, Momentus Vigoride |
| Δv imparted | **1-2 m/s** | **16.5 m/s** (model) | hundreds of m/s upward, propulsive |
| Mechanism | compressed spring | linear synchronous motor, reusable sled | chemical or electric propulsion |
| Programmable per satellite | no | **yes**: the distinguishing claim | yes, by manoeuvre |
| Satellite modification | none (CDS rails) | **none**: magnets ride the sled | mounting to the carrier |
| Power required | none | ~2.6 kJ per shot, supercapacitor bank | full propulsion system |
| Maturity | **flight-proven, thousands deployed** | **TRL 2-3, nothing built** | flown, commercially operating |

The gap VOLLEY targets is real: nothing fielded delivers a *programmable* 10-30 m/s to an
unmodified CubeSat. Springs cannot, and OTVs solve a different problem at a different price.

## Against the incumbents, honestly

> **This comparison is against dispensers, and that is the wrong benchmark.** A customer wanting
> 16.5 m/s can fit a 0.5 to 1.2 kg cold-gas module instead, which VOLLEY loses to by about 8x at
> 3U. See [`KILL_CRITERIA.md`](KILL_CRITERIA.md) threat 1 and
> [`PAYLOAD_CLASSES.md`](PAYLOAD_CLASSES.md), where smaller payloads reverse it.

**Mass per satellite is the surprise, and it is not embarrassing.** VOLLEY's 76.5 kg dry
carries twelve 3U satellites, **6.4 kg of deployer per satellite**. Planetary Systems'
canisterized dispensers run about 2 kg per U (12 kg for 6U, 24 kg for 12U, 54 kg for 27U),
so a 3U-equivalent slot is in the same 6 kg neighbourhood. A magazine-fed electromagnetic
launcher lands in the same mass class as a canister of springs, per satellite.

Two caveats that cut against VOLLEY: the 76.9 kg **excludes** the enclosure, radiator and
avionics (P10, open), and springs need no power, no capacitor bank, no thermal system and no
sequencer.

**The closest comparator is Indian, and it flies.** Dhruva Space's DSOD family (1U / 3U /
6U / 12U / 16U) was space-qualified on ISRO's PSLV-C55 on 22 April 2023, having flown
earlier on PSLV-C53. It uses a **non-pyrotechnic hold-down and release mechanism** and
carries **onboard telemetry for deployment confirmation and ejection-velocity measurement**.
Published ejection velocity is **< 2 m/s** across the whole family.

**A sourced upper bound on the whole spring class, added 2026-07-31.** The NanoRacks NRCSD-E
interface document specifies that a CubeSat *"shall be capable of withstanding a deployment
velocity of **0.5 to 2.5 m/s** at ejection"*. That is the widest published figure in the flown
spring family, and it is the number the "eight times a spring" comparison should be made against
rather than the 2 m/s used elsewhere here: **16.5 / 2.5 = 6.6x, not 8x.** The comparison is
weaker than the one this project has been making, and the honest version is still an order of
magnitude in the regime that matters.

Three things follow, and none of them are comfortable:

- **It is the exact product VOLLEY argues against**, built by the Indian company whose
  business this design study is closest to. Any reader from that part of the industry will
  know it. Omitting it would read as either not having looked or having looked and avoided
  it.
- **They measure their ejection velocity on orbit.** VOLLEY's entire differentiator is
  velocity *accuracy*, and the incumbent already flies the instrumentation that would
  settle such a claim. This project's 0.027 m/s (3σ) is a model output; theirs is telemetry.
- **Non-pyrotechnic release is not a differentiator.** It is already the fielded standard,
  so VOLLEY's contactless release has to compete on velocity and programmability alone.

What VOLLEY still has against it is the thing the DSOD cannot do: **> 2 m/s, programmable per
satellite**. That is the whole argument, and it is narrower than "electromagnetic beats
springs".

*Sources: Dhruva Space product pages and the PSLV-C55 qualification announcement, retrieved
2026-07-29. Deployer dry mass per unit was not obtainable, the specification pages return
403 to automated retrieval, so no mass-per-satellite comparison against DSOD is made here.
Marked unverified under the E16 rule.*

**Tip-off is where the incumbents are strong and VOLLEY is unproven.** The NRCSD-E interface
document is cited here and in `validation/A7_separation_chrono.md` as targeting
**< 5 °/s per axis**, backed by flight heritage plus microgravity and drop-tower test
campaigns. **That number is now in doubt**: search snippets of the sibling NRCSD ICD
(NR-SRD-029) give "less than two (2) deg/sec/axis" verbatim, and the NRCSD-E document itself
403s to automated retrieval so the "-E" variant could not be confirmed either way. If the
real target is 2 °/s, the bar VOLLEY has to clear is 2.5x harder than the pre-declared A7
band assumes. **This must be checked by hand in a browser before A7 runs**, see
`OPEN_PROBLEMS.md` E16. VOLLEY's tip-off is a model output with no
multibody model behind it, A7 is specified and unrun. Claiming a gentler release than a
spring is not yet supported by anything.

**Deployment velocity accuracy is VOLLEY's genuine differentiator**, and it is also the least
validated part. The 0.027 m/s (3σ) dispersion rests on assumed sensor noise (E7), and the
servo headroom argument behind it is stated against a bank sag figure that A8 has just shown
is the wrong quantity. The claim may well hold; it has not been earned yet.

**Interface non-modification is a real advantage over the CSD family**, which uses a tab
interface rather than the CDS rails, and over any concept that bolts an armature to the
customer satellite, a trade this project already made and documented (B6).

## Against transfer vehicles

Not the same market. ION and Vigoride change orbits (altitude, plane, phase) with
propulsion, carrying satellites to a destination. VOLLEY imparts one impulse along the host's
velocity vector and cannot change plane meaningfully (`astro.py` puts the plane-change
ceiling at 0.15°).

Where VOLLEY competes is cost and simplicity for the specific job of *spreading a
constellation in one plane*: no propulsion on the satellites, no propulsion on the deployer,
one shot each. The comparison that matters is against **differential drag**, which is free
and needs no hardware at all, `astro.py` puts 30° of phasing at 25 days by drag against
1.4 days at 10 m/s. Planet Labs has flown differential-drag phasing on a 12-satellite
constellation, which is exactly the comparison case, and **that flown result should replace
the modelled 25-day baseline in the paper** (`RELATED_WORK.md`).

## Prior art VOLLEY must distinguish itself from

Electromagnetic launch is not new, and reviewers will ask. The paper already cites Inductrack
(Post & Ryutov, LLNL) (Halbach array on the moving element, passive track circuits) and the
NASA MagLifter launch-assist work sits in the same lineage. What is not established anywhere
in the literature this project has read is a magazine-fed, *reusable-sled*, programmable-Δv
deployer for unmodified CubeSats. That is the novelty claim, and it is a systems claim rather
than a physics one.

## The honest summary

| | Status |
|---|---|
| Concept occupies a genuinely unserved regime | **yes** |
| Mass per satellite competitive with fielded dispensers | **yes**, with P10 outstanding |
| Programmable velocity, no satellite modification | **yes**, and unique |
| Delivers the velocity it advertises | **yes, since 2026-07-29**: it now advertises the 16.39 m/s the CAD geometry gives |
| Gentler tip-off than a spring | **unproven**: A7 not run |
| Dispersion better than a spring | **unproven**: rests on assumed sensor noise (E7) |
| Anything built or measured | **no** |
| Closest fielded competitor identified and compared | **yes**: Dhruva DSOD, flown on PSLV-C53/C55 |

Against a P-POD, VOLLEY is a hundred times more complex and delivers ten times the velocity,
programmably. Against an OTV it is far cheaper and far less capable. Both of those are
defensible positions. Neither is defensible until the machine hits a number it can prove.
