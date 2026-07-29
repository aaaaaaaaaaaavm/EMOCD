# Related work and comparator sources

Candidate literature and tooling for the validation plan in `../validation/`, and for the
comparator claims in the paper.

**Verification status of this list: NONE OF IT HAS BEEN RETRIEVED AND READ.** Every entry
below was identified from search results on 2026-07-27 and is recorded as a lead. The
repository's standing rule applies (`OPEN_PROBLEMS.md` E16): fetch and read before
anything here enters `paper/paper.tex` or is relied on for a number. Three references
already in the paper are flagged for exactly this reason.

## Comparator claims — highest priority

**Foster et al., "Constellation Phasing with Differential Drag on Planet Labs
Satellites," *Journal of Spacecraft and Rockets* (2018).** Companion preprints: arXiv
1806.01218, arXiv 1509.03270.
Why it matters: the paper's seeding claim is stated against a differential-drag baseline
of 25 days, which is currently a model output of `astro.py`. Foster et al. report phasing
of the Flock 2p constellation — 12 CubeSats at 510 km SSO — with on-orbit results. A
measured baseline is far stronger than a modelled one, and 12 satellites at ~500 km is
close enough to the EMOCD case to be a fair comparison. **Replacing the modelled
comparator with the flown one is the cheapest credibility improvement available to the
paper.**
**No paywall applies** (confirmed 2026-07-29): both companion preprints are open-access on
arXiv, so E16's "fetch and read before citing" requirement can be discharged for this
reference at zero cost. The 2018 preprint matches the *JSR* 55(2) pp. 473-483 content
(DOI 10.2514/1.A33927); the 2015 one is the AAS conference version.

**P-POD Mk III Rev E User Guide** (Cal Poly) and the **NanoRacks NRCSD-E Interface
Definition Document.**
Why they matter: the paper's premise is "spring deployers impart 1–2 m/s". These are the
primary sources for that, and the NRCSD-E document additionally quotes a tip-off target of
< 5 °/s/axis, used as the acceptance band in `validation/A7_separation_chrono.md`.

> **The 5 °/s figure needs checking by hand, and it is not a small point.** Search snippets
> of the sibling NRCSD ICD (NR-SRD-029, public domain) give **"the target tip-off rate of
> the NRCSD is less than two (2) deg/sec/axis"** verbatim. The NRCSD-E document itself
> returns 403 to automated retrieval, so whether the "-E" mechanical variant carries the
> same figure could not be confirmed either way — **this is flagged, not asserted.** If the
> real target is 2 °/s, a pre-declared acceptance band is 2.5x looser than the source it
> cites, which is the one kind of error this project's band-before-run discipline cannot
> catch by itself. Check in a browser at
> `nanoracks.com/wp-content/uploads/Nanoracks-External-Cygnus-Deployer-E-NRCSD-IDD.pdf`
> **before A7 runs.**

## Motor and electromagnetics

**"Electromagnetic Analysis and Experimental Validation of an Ironless Tubular Permanent
Magnet Synchronous Linear Motor," *Symmetry* 17(9), 2025** (doi:10.3390/sym17091480).
The closest published analog to the EMOCD topology, and it reports analytic vs FEA vs
*experimental* agreement on thrust constant. If that agreement level holds up on reading,
it justifies the ±10 % thrust band in `validation/A1_field_femm.md` and gives the paper a
precedent for the analytic-model approach.

**"A multi-stage 130 m/s reluctance linear electromagnetic launcher," *Scientific
Reports* (2022).**
A real, built comparator for the coilgun side of the Table I trade, which currently rests
on a literature efficiency range rather than a specific machine.

**FEMM under Wine is a live path, and the "Windows-only" blocker is softer than recorded.**
FEMM 4.2 is free of charge and source-available (Aladdin Free Public License — not OSI-open,
but cost is what blocks here). Running it under Wine on Linux is documented by the FEMM
project itself (`femm.info/wiki/linuxsupport`), and `py2femm` (GitHub) automates Lua-script
generation through Wine. `analysis/femm/emocd_cross_section.dxf` and
`analysis/femm/FEMM_RUN_SHEET.md` are already written and specific, so no modelling work is
needed — only the install, plus an X11 display or Xvfb, since the run sheet is GUI-driven.

**Elmer FEM** (LGPL, native Linux, 2-D magnetostatic solver) and **GetDP + Gmsh** (Onelab,
ships a `Magnetostatics.pro` template, imports the existing DXF directly) are the fallbacks.
Both are meshed differential-FEM rather than integral superposition, which is the bar E2
actually sets, and GetDP handles 3-D natively — so it is also the natural route to A2's end
effects rather than a detour.

**Radia** (pip-installable, purpose-built for Halbach and undulator arrays) is real and
tempting, but it is a boundary-integral / dipole-superposition solver in the same family as
magpylib. For this ironless geometry it would land on essentially the same answer and inherit
the same "not independent by method" critique. **Do not spend time on it for A1.**

> **Caveat against over-reading this.** The premise that magpylib is a weak check deserves
> qualification: for an **ironless** design with no permeable material, analytic superposition
> is essentially exact and already handles 3-D finite blocks, which 2-D FEMM does not. The
> weak link is not the field model — it is the closed-form expressions built on top of it,
> which is precisely what P17 demonstrated when `magpylib.getFT()` found the inter-array
> attraction formula 37 % high.

**pyleecan** (github.com/Eomys/pyleecan, Apache-2.0) — couples to FEMM and GMSH; useful if
A1 turns into a parameter sweep rather than a single run.

## Astrodynamics tooling

**Orekit** (Apache-2.0, Java with Python bindings) and **GMAT** (NASA, open source) — the
independent force-model implementations behind `validation/A5_astro_orekit.md`.

**NASA CARA Analysis Tools** (github.com/nasa/CARA_Analysis_Tools, MATLAB) — probability
of collision, covariance realism. Behind `validation/A6_conjunction_cara.md`.

> **A6 does not actually need MATLAB, and chasing Octave compatibility would be a mistake.**
> The 2-D Pc algorithm the run sheet wants (Foster or Alfano method) is a published
> closed-form integral of a bivariate Gaussian over a disk — roughly 50 lines against
> `scipy`, which is already installed, applied directly to the OEM ephemerides
> `validation/gmat/` already emits. This removes the tooling risk entirely and changes
> nothing about E18: the covariance is still the hard input either way, CDM-derived or
> documented-assumption. Reimplement rather than port.

**Shambaugh, "Validation of Satellite Lifetime Predictions at Leonid Space,"
arXiv 2601.02453 (Jan 2026)** — verified 2026-07-29, title and content confirmed.
Backtests a lifetime-prediction pipeline against **934 non-manoeuvring satellites that
decayed from LEO between 1961 and 2024**, across six solar cycles, with a three-stage
design that progressively removes hindsight bias. Reported 1-year median CRPS accuracy:
**6.0 days (1.6 %) under perfect knowledge, 18.6 days (5.1 %) with estimated ballistic
coefficients and known space weather, 45.5 days (12.4 %) fully predictive**, against a
claimed 4x improvement on ESA's DRAMA/DISCOS.

Why it matters here, and it matters more than it first looks: it supplies the **accuracy
band E6 has never had**. This project has been comparing `astro.py` against GMAT with no
external sense of what agreement is even achievable — and this paper says that under
realistic forecasting, roughly 12 % error on absolute lifetime is state of the art. That
reframes the A5 result: GMAT and `astro.py` differing by 9-23 % on absolutes is close to
the floor set by space-weather forecast error, not evidence that either is broken. It also
independently corroborates P16's mechanism, since it identifies solar-cycle forecast error
as dominating the budget after ballistic coefficient — i.e. exactly the two axes whose
treatment in `astro.py` turned out to be the same multiplicative slot.

## Publication venue

**IEEE International Symposium on Electromagnetic Launch Technology (EML)** — biennial,
run under the IEEE Nuclear & Plasma Sciences Society, and the principal forum for
electromagnetic acceleration of macroscopic objects since 1980. Selected papers are
published as a special issue of **IEEE Transactions on Plasma Science**; earlier symposia
also fed **IEEE Transactions on Magnetics**. This is a closer fit than a general
conference, and more to the point, its reviewers are the people most likely to find a
problem in the thrust-constant derivation — which is the reason to send it there.

## Architectural precedent

**Post & Ryutov (LLNL), "The Inductrack: A Simpler Approach to Magnetic Levitation,"** and
**"The Design of Halbach Arrays for Inductrack Maglev Systems"** (LLNL-CONF-406791).
The closest published ancestor of this architecture: Halbach array on the moving element,
passive circuits in the track. Post's force scaling — of order 40 tonnes per square metre
of Halbach array — is a useful order-of-magnitude anchor for the 120 kPa Maxwell stress in
`sizing.py`, once the difference between levitation and inter-array attraction is stated
explicitly rather than assumed away.

**NASA MagLifter launch-assist sled work** (superconducting-magnet sleds, and a
NASA-sponsored 10-g Inductrack model). Prior art for maglev launch assist, and the obvious
thing a reviewer will ask EMOCD to distinguish itself from.

## Flight data for validating decay

**CelesTrak** and **Space-Track.org** publish TLE histories, decay predictions, and
reentry records. `validation/A5_astro_orekit.md` currently proposes checking `astro.py`
against another propagator — two models agreeing. Checking it instead against the
*measured* decay of real 3U CubeSats at 450–500 km with known ballistic coefficients would
be a stronger claim, and it is free data.

Set expectations first: published guidance puts lifetime-prediction accuracy at roughly
10 % of residual lifetime at best, driven by atmospheric density uncertainty. That is the
realistic band for absolute lifetimes and reinforces why E6 defends the ×1.80 ratio rather
than the years.

Space-Track's **Conjunction Data Messages** are also the obvious source for a defensible
covariance in A6, which currently has to assume one.

## Power electronics

**ngspice** / **PySpice** (both free) would independently check the pulse-power chain —
the 392 A peak, the 4.9 % bank sag across a 6 F / 96 V bank at 12 mΩ, and the SiC bridge
loading. `sizing.py` computes these analytically; a circuit simulation is a genuinely
different method and takes an afternoon, not a lab.

## Structural and multibody

**CalculiX** and **Code_Aster** (both GPL) for A4; **Elmer** (LGPL) and **GetDP** if the
3-D field work (A2) proceeds; **Project Chrono** (BSD-3) for A7.

> **A7's "not installable" verdict is probably a packaging mistake, not a real blocker.**
> `pychrono` ships prebuilt SWIG bindings through **conda-forge, not PyPI** — so
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
- AFIT/AFRL microgravity deployment testing, DTIC AD1055374 — parabolic flight and drop
  tower measurements of P-POD dynamics

These are the empirical tip-off literature that the paper's Yudintsev citation (reference
[17], flagged unverified in E16) currently stands in for.
