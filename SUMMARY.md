# VOLLEY: one page

**Adityavardhan Mishra** · Dept. of Mechanical Engineering, Symbiosis Institute of
Technology, Symbiosis International (Deemed University), Pune
· [adityavardhanmishr@gmail.com](mailto:adityavardhanmishr@gmail.com)
· [full repository](https://github.com/aaaaaaaaaaaavm/VOLLEY)

---

## The idea

Rideshare CubeSats inherit the orbit of whoever paid for the launch. Spring deployers release
them at **1-2 m/s**, which is far too little to change that orbit; orbital transfer vehicles
can change it, but they cost hundreds of m/s of propulsion and a spacecraft to carry it.
Between those sits an unserved regime.

**VOLLEY is a magazine-fed linear synchronous motor** that mounts on a rideshare upper stage
and ejects **unmodified** 3U CubeSats, no armature, no plating, no electrical interface on
the customer satellite, at a **velocity programmable per satellite**. Twelve satellites feed
from two transverse cassettes onto a reusable permanent-magnet sled running a 1.5 m ironless
double-sided Halbach track, arrested by a contactless eddy brake and powered from a
supercapacitor bank.

One shot buys a propulsion-less satellite **1.62x its orbital lifetime**, or seeds 30° of
constellation phase spacing in **1.4-6.9 days** against roughly 25 for differential drag.

## The numbers, with their caveats attached

| | | |
|---|---|---|
| Exit velocity, 3U | **16.5 m/s at 10.7 g** | Eight times a spring. The ceiling is the payload's g-limit, not the machine: 25.3 m/s at the 25 g cap, see [`VELOCITY_CEILING.md`](docs/VELOCITY_CEILING.md). From a sled mass *measured* in CAD (9.445 kg), not estimated, the earlier 4.86 kg parametric estimate gave 20.4 m/s |
| Velocity dispersion | **0.027 m/s (3σ)** | Closed-loop, at a 16.2 m/s setpoint. Rests on *assumed* sensor noise (E7), the differentiator, and the least validated part |
| Thrust constant | **11.22 N per kA/m** | Winding-resolved, and **confirmed 2026-07-29 by a meshed magnetostatic FEM to 0.07 %**, a PDE solve, not another superposition |
| Energy per shot | **2.88 kJ gross, 2.58 kJ net**, 21.2 % electrical-to-payload | Under one watt-hour. 296 J of the sled's 1291 J comes back through 240 mm of regen stator ([A11](validation/A11_regen_braking.md), adopted 2026-07-31); the brake still takes 952 J |
| System mass | **76.9 kg dry**, 124.9 kg loaded | **6.4 kg of deployer per 3U satellite**, the same class as canisterized dispensers at ~2 kg/U |
| Recurring hardware | ~₹1.35 M per unit, ₹112 k per satellite | **Every price assumed, no quotations.** Useful part: avionics + energy storage are ~42 % of cost and the magnet set only ~5 %, which holds even at 2x price errors |
| Envelope | 1839 mm closed | **Exceeds the ESPA-Grande class by ~44 %.** Open packaging problem (P9) |

> **Open as of 2026-07-30:** the supercapacitor bank is modelled at an ESR no commercial cell
> of that capacitance achieves, and the shot does not close at a realistic value (**P26**). The
> velocity and dispersion figures are unaffected, the bank sizing is. Not quietly re-sized.

**Maturity: TRL 2-3. Nothing has been built, fired, or measured.** **Eight of ten** specified
validations have been run, each against an acceptance band declared *before* the run — and the
results are mixed on purpose:

| | |
|---|---|
| **A5 FAILED** | an independent propagator falsified an invariance claim that was in the paper's own abstract (P16) |
| **A12** | found the inter-array force feeding the structural FEA **37 % high** — and that the explanation first written for it was backwards |
| **A6** | returned three rows **void**: the quantity they tested does not exist at these separations |
| A1, A4, A8, A10, A11 | passed, partially or fully, with every miss logged as a numbered defect |

**A7 (tip-off) and A9 (decay against flown CubeSats) are outstanding.** A9 is the only analysis
anywhere in this project that compares the model against something that actually happened, and
it is blocked by network policy rather than by difficulty.

## Where it sits against what flies

| | Δv | Programmable | Satellite mods | Status |
|---|---|---|---|---|
| Spring deployers, P-POD, ISIPOD, **Dhruva DSOD** | 1-2 m/s | no | none | flown, thousands deployed |
| **VOLLEY** | 16.5 m/s | **yes** | **none** | design study |
| Transfer vehicles, ION, Vigoride | 100s m/s | yes | mounting | flown, commercial |

Dhruva Space's DSOD is the closest comparator and it already flies, space-qualified on
PSLV-C53 and C55, non-pyrotechnic release, and instrumented to *measure* ejection velocity on
orbit. What it cannot do is exceed 2 m/s or vary velocity per satellite. That gap is the
entire argument for this machine, and it is narrower than "electromagnetic beats springs".

## Host integration, worked against real vehicles

The interface asks four things of any host: mass and control authority, a 150-300 W recharge
feed, a serial command link, and an authorized firing window.

- **ISRO's POEM** is the flown precedent, a spent PS4 operated as a three-axis-stabilized
  hosted platform, retired by controlled reentry. Its zero-debris closeout is the regulatory
  template.
- **Skyroot's Vikram-1** carries a restartable Orbit Adjustment Module stage-tested through
  more than a thousand pulses. A loaded VOLLEY is **34 %** of the published 350 kg LEO
  capacity, falling to **22 %** and **13 %** on the announced 550 kg and 900 kg variants, so
  early flights are dedicated demonstrations and later ones ordinary manifest items.

Recoil is the satellite's momentum only, **66.1 N·s** per shot, nulled by a few grams of cold
gas.

## What makes this repository worth opening

Every defect found in this work is published, numbered, and tracked, including the ones that
damage its own claims. Acceptance bands are declared in writing **before** each analysis runs,
so a failure cannot be rationalised afterwards. Four errors were found in the paper by
rebuilding its analysis from scratch. An independent propagator (GMAT) then **falsified a
claim in the paper's own abstract**, and that is recorded as P16 rather than quietly dropped.
The scripts are authoritative over the paper, never the reverse.

**[`docs/PROGRAMME.md`](docs/PROGRAMME.md)**: the four repositories of this programme
**[`docs/BASELINE.md`](docs/BASELINE.md)**: what is frozen, and what may move it
**[`docs/ROADMAP.md`](docs/ROADMAP.md)**: what happens next, and when
**[`docs/HISTORY.md`](docs/HISTORY.md)**: the project since 2021, and how this git history was built
**[`docs/QUALIFICATION_PLAN.md`](docs/QUALIFICATION_PLAN.md)**: the test campaign, specified
**[`OPEN_PROBLEMS.md`](OPEN_PROBLEMS.md)**: every known defect
**[`docs/VALIDATION_REPORT.md`](docs/VALIDATION_REPORT.md)**: every claim, independently checked where possible
**[`docs/PROVENANCE.md`](docs/PROVENANCE.md)**: read this before citing anything
