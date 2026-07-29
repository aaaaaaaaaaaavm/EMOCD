# EMOCD — one page

**Adityavardhan Mishra** · Dept. of Mechanical Engineering, Symbiosis Institute of
Technology, Symbiosis International (Deemed University), Pune
· [adityavardhanmishr@gmail.com](mailto:adityavardhanmishr@gmail.com)
· [full repository](https://github.com/aaaaaaaaaaaavm/EMOCD)

---

## The idea

Rideshare CubeSats inherit the orbit of whoever paid for the launch. Spring deployers release
them at **1–2 m/s**, which is far too little to change that orbit; orbital transfer vehicles
can change it, but they cost hundreds of m/s of propulsion and a spacecraft to carry it.
Between those sits an unserved regime.

**EMOCD is a magazine-fed linear synchronous motor** that mounts on a rideshare upper stage
and ejects **unmodified** 3U CubeSats — no armature, no plating, no electrical interface on
the customer satellite — at a **velocity programmable per satellite**. Twelve satellites feed
from two transverse cassettes onto a reusable permanent-magnet sled running a 1.5 m ironless
double-sided Halbach track, arrested by a contactless eddy brake and powered from a
supercapacitor bank.

One shot buys a propulsion-less satellite **1.62× its orbital lifetime**, or seeds 30° of
constellation phase spacing in **1.4–6.9 days** against roughly 25 for differential drag.

## The numbers, with their caveats attached

| | | |
|---|---|---|
| Exit velocity, 3U | **16.5 m/s at 10.7 g** | Eight times a spring. From a sled mass *measured* in CAD (9.445 kg), not estimated — the earlier 4.86 kg parametric estimate gave 20.4 m/s |
| Velocity dispersion | **0.027 m/s (3σ)** | Closed-loop, at a 16.2 m/s setpoint. Rests on *assumed* sensor noise (E7) — the differentiator, and the least validated part |
| Thrust constant | **11.22 N per kA/m** | Winding-resolved. Checked only analytic-against-analytic; a second physical method is the top roadmap item |
| Energy per shot | **2.80 kJ**, 20 % electrical-to-payload | Under one watt-hour. No regeneration credit — the sled's energy is dissipated by design |
| System mass | **76.9 kg dry**, 124.9 kg loaded | **6.4 kg of deployer per 3U satellite**, the same class as canisterized dispensers at ~2 kg/U |
| Envelope | 1839 mm closed | **Exceeds the ESPA-Grande class by ~44 %.** Open packaging problem (P9) |

**Maturity: TRL 2–3. Nothing has been built, fired, or measured.** Three of eight specified
validations have been run, each against an acceptance band declared *before* the run — and
all three predate the current operating point, which is itself logged as a defect (P19).

## Where it sits against what flies

| | Δv | Programmable | Satellite mods | Status |
|---|---|---|---|---|
| Spring deployers — P-POD, ISIPOD, **Dhruva DSOD** | 1–2 m/s | no | none | flown, thousands deployed |
| **EMOCD** | 16.5 m/s | **yes** | **none** | design study |
| Transfer vehicles — ION, Vigoride | 100s m/s | yes | mounting | flown, commercial |

Dhruva Space's DSOD is the closest comparator and it already flies — space-qualified on
PSLV-C53 and C55, non-pyrotechnic release, and instrumented to *measure* ejection velocity on
orbit. What it cannot do is exceed 2 m/s or vary velocity per satellite. That gap is the
entire argument for this machine, and it is narrower than "electromagnetic beats springs".

## Host integration, worked against real vehicles

The interface asks four things of any host: mass and control authority, a 150–300 W recharge
feed, a serial command link, and an authorized firing window.

- **ISRO's POEM** is the flown precedent — a spent PS4 operated as a three-axis-stabilized
  hosted platform, retired by controlled reentry. Its zero-debris closeout is the regulatory
  template.
- **Skyroot's Vikram-1** carries a restartable Orbit Adjustment Module stage-tested through
  more than a thousand pulses. A loaded EMOCD is **34 %** of the published 350 kg LEO
  capacity, falling to **22 %** and **13 %** on the announced 550 kg and 900 kg variants — so
  early flights are dedicated demonstrations and later ones ordinary manifest items.

Recoil is the satellite's momentum only, **66.1 N·s** per shot, nulled by a few grams of cold
gas.

## What makes this repository worth opening

Every defect found in this work is published, numbered, and tracked — including the ones that
damage its own claims. Acceptance bands are declared in writing **before** each analysis runs,
so a failure cannot be rationalised afterwards. Four errors were found in the paper by
rebuilding its analysis from scratch. An independent propagator (GMAT) then **falsified a
claim in the paper's own abstract**, and that is recorded as P16 rather than quietly dropped.
The scripts are authoritative over the paper, never the reverse.

**→ [`ROADMAP.md`](ROADMAP.md)** — what happens next, and when
**→ [`OPEN_PROBLEMS.md`](OPEN_PROBLEMS.md)** — every known defect
**→ [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md)** — every claim, independently checked where possible
**→ [`PROVENANCE.md`](PROVENANCE.md)** — read this before citing anything
