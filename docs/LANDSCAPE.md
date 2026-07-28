# Where EMOCD sits against what actually flies

An honest comparison of this design study against fielded CubeSat deployers and the
last-mile transfer vehicles at the other end of the market.

> **Source status.** EMOCD's own figures come from `analysis/results/*.json` and are model
> outputs. Competitor figures were collected from vendor and agency material on 2026-07-28
> and are **recorded as leads, not verified** — the same E16 rule that applies to
> `RELATED_WORK.md`. Fetch and read the primary document before any of these numbers enters
> `paper/paper.tex`. Where a figure could not be pinned down, this file says so rather than
> estimating.

## The three families

| | **Spring deployers** | **EMOCD** | **Orbital transfer vehicles** |
|---|---|---|---|
| Examples | P-POD, ISIPOD, NRCSD, CSD, EXOpod | this design study | D-Orbit ION, Momentus Vigoride |
| Δv imparted | **1–2 m/s** | **16.5–20.4 m/s** (model) | hundreds of m/s upward, propulsive |
| Mechanism | compressed spring | linear synchronous motor, reusable sled | chemical or electric propulsion |
| Programmable per satellite | no | **yes** — the distinguishing claim | yes, by manoeuvre |
| Satellite modification | none (CDS rails) | **none** — magnets ride the sled | mounting to the carrier |
| Power required | none | ~2.6 kJ per shot, supercapacitor bank | full propulsion system |
| Maturity | **flight-proven, thousands deployed** | **TRL 2–3, nothing built** | flown, commercially operating |

The gap EMOCD targets is real: nothing fielded delivers a *programmable* 10–30 m/s to an
unmodified CubeSat. Springs cannot, and OTVs solve a different problem at a different price.

## Against the incumbents, honestly

**Mass per satellite is the surprise, and it is not embarrassing.** EMOCD's 72.3 kg dry
carries twelve 3U satellites — **6.0 kg of deployer per satellite**. Planetary Systems'
canisterized dispensers run about 2 kg per U (12 kg for 6U, 24 kg for 12U, 54 kg for 27U),
so a 3U-equivalent slot is in the same 6 kg neighbourhood. A magazine-fed electromagnetic
launcher lands in the same mass class as a canister of springs, per satellite.

Two caveats that cut against EMOCD: the 72.3 kg **excludes** the enclosure, radiator and
avionics (P10, open), and springs need no power, no capacitor bank, no thermal system and no
sequencer.

**Tip-off is where the incumbents are strong and EMOCD is unproven.** The NRCSD-E interface
document targets **< 5 °/s per axis**, and that number is backed by flight heritage plus
microgravity and drop-tower test campaigns. EMOCD's tip-off is a model output with no
multibody model behind it — A7 is specified and unrun. Claiming a gentler release than a
spring is not yet supported by anything.

**Deployment velocity accuracy is EMOCD's genuine differentiator**, and it is also the least
validated part. The 0.027 m/s (3σ) dispersion rests on assumed sensor noise (E7), and the
servo headroom argument behind it is stated against a bank sag figure that A8 has just shown
is the wrong quantity. The claim may well hold; it has not been earned yet.

**Interface non-modification is a real advantage over the CSD family**, which uses a tab
interface rather than the CDS rails, and over any concept that bolts an armature to the
customer satellite — a trade this project already made and documented (B6).

## Against transfer vehicles

Not the same market. ION and Vigoride change orbits — altitude, plane, phase — with
propulsion, carrying satellites to a destination. EMOCD imparts one impulse along the host's
velocity vector and cannot change plane meaningfully (`astro.py` puts the plane-change
ceiling at 0.15°).

Where EMOCD competes is cost and simplicity for the specific job of *spreading a
constellation in one plane*: no propulsion on the satellites, no propulsion on the deployer,
one shot each. The comparison that matters is against **differential drag**, which is free
and needs no hardware at all — `astro.py` puts 30° of phasing at 25 days by drag against
1.4 days at 10 m/s. Planet Labs has flown differential-drag phasing on a 12-satellite
constellation, which is exactly the comparison case, and **that flown result should replace
the modelled 25-day baseline in the paper** (`RELATED_WORK.md`).

## Prior art EMOCD must distinguish itself from

Electromagnetic launch is not new, and reviewers will ask. The paper already cites Inductrack
(Post & Ryutov, LLNL) — Halbach array on the moving element, passive track circuits — and the
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
| Delivers the 20.37 m/s it advertises | **not as drawn** — 16.5 m/s at the measured sled mass (P15) |
| Gentler tip-off than a spring | **unproven** — A7 not run |
| Dispersion better than a spring | **unproven** — rests on assumed sensor noise (E7) |
| Anything built or measured | **no** |

Against a P-POD, EMOCD is a hundred times more complex and delivers ten times the velocity —
programmably. Against an OTV it is far cheaper and far less capable. Both of those are
defensible positions. Neither is defensible until the machine hits a number it can prove.
