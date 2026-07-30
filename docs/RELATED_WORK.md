# Literature review

Dossier §6: the literature review exists to identify **better ideas, competing approaches,
hidden assumptions, previous failures, and engineering tradeoffs**, and to preserve the
analyses so accumulated knowledge is not lost. This file is that record. It is not a
bibliography; the paper has one.

## How to read an entry

Each source below carries the same five fields, so a reader can judge it without reading the
source:

| | |
|---|---|
| **Claim** | what the source establishes |
| **Method** | how, and therefore how much weight it carries |
| **VOLLEY takes** | what this project adopts from it |
| **VOLLEY differs** | where this project does not follow it, and why |
| **Status** | `verified` (retrieved and read · `confirmed`) existence and content confirmed but not read in full · `lead`, identified from search only |

> ### Verification discipline (E16)
>
> **A `lead` may not support a number in `paper/paper.tex`.** Retrieve and read first. Three
> references already in the paper carry this flag, and they are the reason the rule exists.
>
> Status is recorded per source rather than per file, because the earlier blanket statement
> ("none of this has been retrieved") became untrue as items were checked, and a blanket
> statement that is wrong is worse than no statement.

---

## The wider landscape

[`LITERATURE.md`](LITERATURE.md) maps 136 works around this project, harvested from the reference
lists of the five papers read in full. It is a reading list with provenance attached, not a review,
and the `lead` rule above applies to all of it: nothing there may support a number in the paper.

One entry deserves promotion out of it. Zhao, Yue, Yang and Zhu, "A High Thrust Density Voice Coil
Actuator With a New Structure of Double Magnetic Circuits for CubeSat Deployers", *IEEE Trans. Ind.
Electron.* 69 (2022) 13305, is cited by **all three** Harbin papers. It is the actuator underneath
their deployer line, it is a linear machine rather than a coilgun, and it is the nearest published
neighbour to this design's topology that has turned up so far. It has not been read.

## Direct competitors: added 2026-07-30

> **This section did not exist until 2026-07-30, and its absence was the defect.** A review with
> no competitor section had 7 citations and none of the five works below, one of which is the
> closest published work to this project. Full analysis in [`PRIOR_ART.md`](PRIOR_ART.md); the
> claim corrections it forced are logged as **P22** in `OPEN_PROBLEMS.md`. All five were read in
> full on 2026-07-30, and doing so **changed three conclusions drawn from their abstracts**, those
> reversals are tabulated in `PRIOR_ART.md`.

### Feng, Yang & Wu: on-orbit electromagnetic launcher for CubeSats
*Int. J. Aerospace Eng.* 2025, art. 3000765 · DOI [10.1155/ijae/3000765](https://doi.org/10.1155/ijae/3000765)

| | |
|---|---|
| **Claim** | A **three-stage** induction coilgun (3 x 1300 mm) drives a 20 kg payload to 321.56 m/s at 16 kV, 230 m/s at 10 kV, efficiency 19.9 % falling to 14.9 %, stored energy 2.70 to 6.91 MJ, peak force >600 kN. Then a 3-D reachable-domain envelope by enhanced alpha-shape |
| **Method** | Coupled circuit-electromagnetic-mechanical model validated against nonlinear FEM, plus two-body orbital simulation. **No hardware.** "Experimental results" in the text refers to simulation runs |
| **VOLLEY takes** | The reachable-domain framing, which is a better astrodynamic product than a scalar lifetime multiplier, it answers "which orbits does one shot make available" in three dimensions. **The strongest single thing to take from this literature.** Candidate Phase II item |
| **VOLLEY differs** | Architecture (Halbach LSM vs induction coilgun), and the two differences that matter: their armature is **aluminium coils on the payload**, so the satellite is modified or a sabot is added (ADR-006 forbids the former); and their 3.9 m barrel delivers 321.56 m/s at **1352 g** mean and ~3060 g peak, against ~14 g CubeSat qualification. Their velocity is not available to a standard-qualified CubeSat. Also 6.91 MJ per shot against 2.80 kJ |
| **Status** | `verified`, read 2026-07-30. **Simulation only, no hardware**, so this project and theirs are maturity peers. Publication predates this repository going public by 8 months |

### Xu, Yue, Zhao, Yang, Wu, Pan, Tang & Zhang: CubeSats in-orbit electromagnetic transfer system
*Aerospace* **11**(5) 394, 2024 · DOI [10.3390/aerospace11050394](https://doi.org/10.3390/aerospace11050394)

| | |
|---|---|
| **Claim** | Stacked CubeSats are pushed layer by layer onto a 2-D electromagnetic conveying platform and moved to a release window by a planar two-axis drive; an improved A\* planner coordinates many transfers, with a cost term for **attitude disturbance caused by the transfers themselves** |
| **Method** | Algorithm design and simulation |
| **VOLLEY takes** | The disturbance cost model. This project budgets recoil from the *shot* and has nothing on disturbance from **magazine indexing between shots**: now opened as **E24** |
| **VOLLEY differs** | Theirs moves satellites electromagnetically to *select a release position*; this one uses the electromagnetics to *set the release velocity*. Different function, similar hardware vocabulary |
| **Status** | `verified`, read 2026-07-30 |

### High-volume CubeSat storage device: transport characteristics
*Aerospace* **12**(6) 466, 2025 · DOI [10.3390/aerospace12060466](https://doi.org/10.3390/aerospace12060466)

| | |
|---|---|
| **Claim** | A high-density multi-species CubeSat storage and transport system, with **a prototype built and measured**: pushing speed **32.8 mm/s** during the transport stroke, and collisions observed in both simulation and experiment |
| **Method** | Simulation plus hardware experiment |
| **VOLLEY takes** | The rig itself is the most useful thing here, a template for what a credible bench verification of a transport mechanism looks like. Directly informs B-1 and B-2 in `BENCHTOP_TESTS.md` |
| **VOLLEY differs** | Storage and transport, not ejection. What they measured is a **slow pusher at 32.8 mm/s**, not an electromagnetic launch, the maturity gap against this project is real but narrower than "they have experiment and we do not" suggests |
| **Status** | `verified`, read 2026-07-30. Author list now confirmed from the PDF; the paper bibliography is complete. HIT with Harbin Space Star Data System Technology |

### New deployer for in-orbit release of multiple stacked CubeSats
*Remote Sensing* **14**(17) 4205, 2022 · DOI [10.3390/rs14174205](https://doi.org/10.3390/rs14174205)

| | |
|---|---|
| **Claim** | A large-capacity stacked-CubeSat deployer that replaces compression springs with **electromagnetic actuators** for transport and release |
| **Method** | Design and analysis |
| **VOLLEY takes** | Establishes the stacked/magazine deployer lineage, which is the ancestry of the cassette architecture here whether or not it was known at the time |
| **VOLLEY differs** | Transport and release actuation, not programmable exit velocity |
| **Status** | `verified`, read 2026-07-30. Origin of the Harbin line |

### Einat & Orbach: multi-stage 130 m/s reluctance linear electromagnetic launcher
*Sci. Rep.* **13**, 2023 · DOI [10.1038/s41598-022-27022-z](https://doi.org/10.1038/s41598-022-27022-z)

| | |
|---|---|
| **Claim** | A **built and measured** multi-stage reluctance coilgun reaching 130 m/s (highest reported for a reluctance launcher) on a **2.5 g projectile** (~21 J). Modular stage cascading, stated route to lunar launch. Its survey of the field is the most useful part: Manzoor 36 m/s at 6 J, Deng 340 g at 30 J, Song 21.68 kg to 143 m/s, typical projectiles 2-11 g |
| **Method** | Hardware, measured. The strongest experimental evidence in this section |
| **VOLLEY takes** | Nothing quantitative, and that is the finding. It was expected to settle ADR-003's unsourced "1-2 % coilgun efficiency" claim. **At 2.5 g it cannot**: five orders of magnitude below a 4 kg CubeSat, and Feng reports 14.9-19.9 % at 20 kg, so the claim was false regardless. ADR-003's efficiency argument is **withdrawn** |
| **VOLLEY differs** | Reluctance, ferromagnetic armature, no velocity-regulation claim at the dispersion this application needs |
| **Status** | `verified`, read 2026-07-30 |

---

## Comparator claims: highest priority

### Foster et al.: differential-drag phasing, flown

*"Constellation Phasing with Differential Drag on Planet Labs Satellites,"* **J. Spacecraft
and Rockets 55(2) 2018, 473-483**, DOI 10.2514/1.A33927. Open-access preprints: arXiv
**1806.01218** (matches the JSR content), arXiv **1509.03270** (AAS version).

| | |
|---|---|
| **Claim** | Differential drag phased the Flock 2p constellation (12 CubeSats at 510 km SSO) with measured on-orbit results |
| **Method** | **Flight data.** Not a model. This is the only comparator in this review with that status |
| **VOLLEY takes** | The comparator baseline. The paper's seeding claim is currently stated against 25 days, which is an `astro.py` model output |
| **VOLLEY differs** | Not yet, the swap has not been made |
| **Status** | **confirmed**: DOI, venue, pages and both preprint IDs verified 2026-07-29; no paywall applies. Not yet read in full |

**Why this is the highest-priority item in the review:** it replaces a modelled number with a
measured one, at zero cost, in the claim that carries the value proposition. Nothing else here
offers that.

**P-POD Mk III Rev E User Guide** (Cal Poly) and the **NanoRacks NRCSD-E Interface
Definition Document.**
Why they matter: the paper's premise is "spring deployers impart 1-2 m/s". These are the
primary sources for that, and the NRCSD-E document additionally quotes a tip-off target of
< 5 °/s/axis, used as the acceptance band in `validation/A7_separation_chrono.md`.

> **The 5 °/s figure needs checking by hand, and it is not a small point.** Search snippets
> of the sibling NRCSD ICD (NR-SRD-029, public domain) give **"the target tip-off rate of
> the NRCSD is less than two (2) deg/sec/axis"** verbatim. The NRCSD-E document itself
> returns 403 to automated retrieval, so whether the "-E" mechanical variant carries the
> same figure could not be confirmed either way, **this is flagged, not asserted.** If the
> real target is 2 °/s, a pre-declared acceptance band is 2.5x looser than the source it
> cites, which is the one kind of error this project's band-before-run discipline cannot
> catch by itself. Check in a browser at
> `nanoracks.com/wp-content/uploads/Nanoracks-External-Cygnus-Deployer-E-NRCSD-IDD.pdf`
> **before A7 runs.**

## Cross-industry sources (added 2026-07-29)

Full analysis in [`CROSS_INDUSTRY.md`](CROSS_INDUSTRY.md); recorded here so the literature
record is in one place.

### ESA Space Tribology Handbook

Roberts, ESTL / AEA Technology, [ESA Bulletin 94](https://www.esa.int/esapub/bulletin/bullet94/ROB.pdf).

| | |
|---|---|
| **Claim** | Design guidance for tribology in space mechanisms: lubricant and component selection, cold welding, rolling-element and linear bearings, testing |
| **Method** | Handbook distilled from ESTL's accelerated life testing in thermal-vacuum |
| **VOLLEY takes** | **E21 substantially retires.** MoS₂ is the accepted solid lubricant; twelve cycles is trivial by space-mechanism standards. The task becomes selection, not research |
| **VOLLEY differs** | The 1.48 kN per roller pair must still be checked against bearing ratings, MoS₂ transfer-film behaviour is load-dependent |
| **Status** | **confirmed**: source located and its scope verified 2026-07-29 |

### Magnet eddy-current loss and segmentation

[Zhang et al. *IET Power Electronics* 2021](https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/pel2.12009);
[partial-segmentation study for PMLSMs, UTS OPUS](https://opus.lib.uts.edu.au/bitstream/10453/140691/3/Reduction%20of%20Magnet%20Eddy%20Current%20Loss%20in%20PMSM%20by%20Using%20Partial%20Magnet%20Segment%20Method.pdf).

| | |
|---|---|
| **Claim** | Eddy currents in PM bulk cause heating and risk **irreversible** demagnetisation; segmentation is the standard mitigation and it reduces thrust and mechanical robustness |
| **Method** | FEA plus analytical models, overwhelmingly steady-state rotating machines |
| **VOLLEY takes** | E19 is characterised rather than unexplored, and **segmentation is a design option this project did not previously have** |
| **VOLLEY differs** | **Duty is not comparable.** A 157 ms pulse twelve times per campaign is thermally far gentler in the mean than continuous operation, but the peak drives the knee point, and nobody has computed it here. E19 stays open |
| **Status** | **confirmed** |

### Vacuum-rated ironless linear motors

[Tecnotion](https://www.tecnotion.com/applications/semiconductors/) ·
[Dover Motion](https://dovermotion.com/applications/high-vacuum-positioning-systems/) ·
[Gorman Dynamics](https://www.gormandynamics.com/vacuum-motor-umv)

| | |
|---|---|
| **Claim** | Vacuum-compatible ironless linear motors are catalogue products; coreless construction lowers outgassing and eliminates cogging |
| **Method** | Vendor documentation, **marketing material.** Cited only for what a product category routinely does, never for a performance number |
| **VOLLEY takes** | External support for ADR-004: the ironless choice converges with fielded vacuum practice for a reason this project had not recorded |
| **VOLLEY differs** | **Regime.** Wafer stages run sub-m/s continuous; this runs 16.5 m/s for 157 ms. Zero-cogging retires half of E23; the *sweep* half is untouched, because industrial stages do not chirp through their velocity range |
| **Status** | **confirmed** as vendor claims. Not independent evidence |

## Motor and electromagnetics

**"Electromagnetic Analysis and Experimental Validation of an Ironless Tubular Permanent
Magnet Synchronous Linear Motor," *Symmetry* 17(9), 2025** (doi:10.3390/sym17091480).
The closest published analog to the VOLLEY topology, and it reports analytic vs FEA vs
*experimental* agreement on thrust constant. If that agreement level holds up on reading,
it justifies the ±10 % thrust band in `validation/A1_field_femm.md` and gives the paper a
precedent for the analytic-model approach.

**"A multi-stage 130 m/s reluctance linear electromagnetic launcher," *Scientific
Reports* (2022).**
A real, built comparator for the coilgun side of the Table I trade, which currently rests
on a literature efficiency range rather than a specific machine.

**FEMM under Wine is a live path, and the "Windows-only" blocker is softer than recorded.**
FEMM 4.2 is free of charge and source-available (Aladdin Free Public License, not OSI-open,
but cost is what blocks here). Running it under Wine on Linux is documented by the FEMM
project itself (`femm.info/wiki/linuxsupport`), and `py2femm` (GitHub) automates Lua-script
generation through Wine. `analysis/femm/emocd_cross_section.dxf` and
`analysis/femm/FEMM_RUN_SHEET.md` are already written and specific, so no modelling work is
needed, only the install, plus an X11 display or Xvfb, since the run sheet is GUI-driven.

**Elmer FEM** (LGPL, native Linux, 2-D magnetostatic solver) and **GetDP + Gmsh** (Onelab,
ships a `Magnetostatics.pro` template, imports the existing DXF directly) are the fallbacks.
Both are meshed differential-FEM rather than integral superposition, which is the bar E2
actually sets, and GetDP handles 3-D natively, so it is also the natural route to A2's end
effects rather than a detour.

**Radia** (pip-installable, purpose-built for Halbach and undulator arrays) is real and
tempting, but it is a boundary-integral / dipole-superposition solver in the same family as
magpylib. For this ironless geometry it would land on essentially the same answer and inherit
the same "not independent by method" critique. **Do not spend time on it for A1.**

> **Caveat against over-reading this.** The premise that magpylib is a weak check deserves
> qualification: for an **ironless** design with no permeable material, analytic superposition
> is essentially exact and already handles 3-D finite blocks, which 2-D FEMM does not. The
> weak link is not the field model, it is the closed-form expressions built on top of it,
> which is precisely what P17 demonstrated when `magpylib.getFT()` found the inter-array
> attraction formula 37 % high.

**pyleecan** (github.com/Eomys/pyleecan, Apache-2.0), couples to FEMM and GMSH; useful if
A1 turns into a parameter sweep rather than a single run.

## Astrodynamics tooling

**Orekit** (Apache-2.0, Java with Python bindings) and **GMAT** (NASA, open source), the
independent force-model implementations behind `validation/A5_astro_orekit.md`.

**NASA CARA Analysis Tools** (github.com/nasa/CARA_Analysis_Tools, MATLAB), probability
of collision, covariance realism. Behind `validation/A6_conjunction_cara.md`.

> **A6 does not actually need MATLAB, and chasing Octave compatibility would be a mistake.**
> The 2-D Pc algorithm the run sheet wants (Foster or Alfano method) is a published
> closed-form integral of a bivariate Gaussian over a disk, roughly 50 lines against
> `scipy`, which is already installed, applied directly to the OEM ephemerides
> `validation/gmat/` already emits. This removes the tooling risk entirely and changes
> nothing about E18: the covariance is still the hard input either way, CDM-derived or
> documented-assumption. Reimplement rather than port.

**Shambaugh, "Validation of Satellite Lifetime Predictions at Leonid Space,"
arXiv 2601.02453 (Jan 2026)**, verified 2026-07-29, title and content confirmed.
Backtests a lifetime-prediction pipeline against **934 non-manoeuvring satellites that
decayed from LEO between 1961 and 2024**, across six solar cycles, with a three-stage
design that progressively removes hindsight bias. Reported 1-year median CRPS accuracy:
**6.0 days (1.6 %) under perfect knowledge, 18.6 days (5.1 %) with estimated ballistic
coefficients and known space weather, 45.5 days (12.4 %) fully predictive**, against a
claimed 4x improvement on ESA's DRAMA/DISCOS.

Why it matters here, and it matters more than it first looks: it supplies the **accuracy
band E6 has never had**. This project has been comparing `astro.py` against GMAT with no
external sense of what agreement is even achievable, and this paper says that under
realistic forecasting, roughly 12 % error on absolute lifetime is state of the art. That
reframes the A5 result: GMAT and `astro.py` differing by 9-23 % on absolutes is close to
the floor set by space-weather forecast error, not evidence that either is broken. It also
independently corroborates P16's mechanism, since it identifies solar-cycle forecast error
as dominating the budget after ballistic coefficient, i.e. exactly the two axes whose
treatment in `astro.py` turned out to be the same multiplicative slot.

## Publication venue

**IEEE International Symposium on Electromagnetic Launch Technology (EML)**, biennial,
run under the IEEE Nuclear & Plasma Sciences Society, and the principal forum for
electromagnetic acceleration of macroscopic objects since 1980. Selected papers are
published as a special issue of **IEEE Transactions on Plasma Science**; earlier symposia
also fed **IEEE Transactions on Magnetics**. This is a closer fit than a general
conference, and more to the point, its reviewers are the people most likely to find a
problem in the thrust-constant derivation, which is the reason to send it there.

## Architectural precedent

**Post & Ryutov (LLNL), "The Inductrack: A Simpler Approach to Magnetic Levitation,"** and
**"The Design of Halbach Arrays for Inductrack Maglev Systems"** (LLNL-CONF-406791).
The closest published ancestor of this architecture: Halbach array on the moving element,
passive circuits in the track. Post's force scaling, of order 40 tonnes per square metre
of Halbach array, is a useful order-of-magnitude anchor for the 120 kPa Maxwell stress in
`sizing.py`, once the difference between levitation and inter-array attraction is stated
explicitly rather than assumed away.

**NASA MagLifter launch-assist sled work** (superconducting-magnet sleds, and a
NASA-sponsored 10-g Inductrack model). Prior art for maglev launch assist, and the obvious
thing a reviewer will ask VOLLEY to distinguish itself from.

## Flight data for validating decay

**CelesTrak** and **Space-Track.org** publish TLE histories, decay predictions, and
reentry records. `validation/A5_astro_orekit.md` currently proposes checking `astro.py`
against another propagator, two models agreeing. Checking it instead against the
*measured* decay of real 3U CubeSats at 450-500 km with known ballistic coefficients would
be a stronger claim, and it is free data.

Set expectations first: published guidance puts lifetime-prediction accuracy at roughly
10 % of residual lifetime at best, driven by atmospheric density uncertainty. That is the
realistic band for absolute lifetimes and reinforces why E6 defends the x1.80 ratio rather
than the years.

Space-Track's **Conjunction Data Messages** are also the obvious source for a defensible
covariance in A6, which currently has to assume one.

## Power electronics

**ngspice** / **PySpice** (both free) would independently check the pulse-power chain,
the 392 A peak, the 4.9 % bank sag across a 6 F / 96 V bank at 12 mΩ, and the SiC bridge
loading. `sizing.py` computes these analytically; a circuit simulation is a genuinely
different method and takes an afternoon, not a lab.

## Structural and multibody

**CalculiX** and **Code_Aster** (both GPL) for A4; **Elmer** (LGPL) and **GetDP** if the
3-D field work (A2) proceeds; **Project Chrono** (BSD-3) for A7.

> **A7's "not installable" verdict is probably a packaging mistake, not a real blocker.**
> `pychrono` ships prebuilt SWIG bindings through **conda-forge, not PyPI**: so
> `pip install pychrono` fails reliably, which is the likely cause of the entry in
> `VALIDATION_REPORT.md`. `conda install projectchrono::pychrono -c conda-forge` lists
> **linux-64** as supported. Worth a five-minute retry with miniforge or mamba before A7
> stays open another cycle, particularly now that the momentum-transfer option in
> `docs/DESIGN_OPTIONS_exit_velocity.md` makes separation dynamics load-bearing rather than
> a nice-to-have.

Licence note: keep all of these external. This repository is MIT; commit input decks and
results, never vendored solver source.

## Deployment dynamics literature

- "Modeling of the CubeSat deployment and initial separation angular velocity estimation,"
  *Acta Astronautica* (2020)
- SSC21-S1-08, on validating NRCSD deployment dynamics (USU SmallSat)
- AFIT/AFRL microgravity deployment testing, DTIC AD1055374, parabolic flight and drop
  tower measurements of P-POD dynamics

These are the empirical tip-off literature that the paper's Yudintsev citation (reference
[17], flagged unverified in E16) currently stands in for.
