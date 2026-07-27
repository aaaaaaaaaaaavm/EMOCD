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

**P-POD Mk III Rev E User Guide** (Cal Poly) and the **NanoRacks NRCSD-E Interface
Definition Document.**
Why they matter: the paper's premise is "spring deployers impart 1–2 m/s". These are the
primary sources for that, and the NRCSD-E document additionally quotes a tip-off target of
< 5 °/s/axis, used as the acceptance band in `validation/A7_separation_chrono.md`.

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

**pyleecan** (github.com/Eomys/pyleecan, Apache-2.0) — couples to FEMM and GMSH; useful if
A1 turns into a parameter sweep rather than a single run.

## Astrodynamics tooling

**Orekit** (Apache-2.0, Java with Python bindings) and **GMAT** (NASA, open source) — the
independent force-model implementations behind `validation/A5_astro_orekit.md`.

**NASA CARA Analysis Tools** (github.com/nasa/CARA_Analysis_Tools, MATLAB) — probability
of collision, covariance realism. Behind `validation/A6_conjunction_cara.md`.

A 2026 preprint backtesting lifetime prediction against 934 non-maneuvering satellites
that deorbited between 1961 and 2024 (arXiv 2601.02453) appeared in the same search. If it
is what the abstract suggests, it is a ready-made benchmark for E6 — but only the
search-result summary was seen, so it is a lead and nothing more.

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
