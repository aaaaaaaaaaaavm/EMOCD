# Skills, and the file that proves each one

**Adityavardhan Mishra** · BTech Mechanical Engineering, Symbiosis Institute of Technology, Pune
(2023–2027) · [adityavardhanmishr@gmail.com](mailto:adityavardhanmishr@gmail.com) ·
[linkedin.com/in/adityavardhanmishra](https://www.linkedin.com/in/adityavardhanmishra/)

An unevidenced skills list is worth nothing, so this one carries the evidence inline. **Every row
points at a file in this repository that you can open and run.** Where a claim rests on something
outside the repository, the row says so and says what the evidence actually is.

Read the two honesty caveats at the bottom before using this as a hiring signal. They are there
because they belong there.

---

## Electromagnetics and finite-element analysis

| Claim | Evidence | Strength |
|---|---|---|
| 2-D magnetostatic FEM, written from the weak form | [`validation/fem/a1_airgap_field.py`](../validation/fem/a1_airgap_field.py) — scikit-fem, gmsh meshing at 141 k elements, vector-potential formulation with a remanence source term | **Strong.** Confirmed the winding-resolved thrust constant to **0.07 %** — an independent PDE solve, not a second superposition |
| Analytic field modelling, and knowing its limits | [`analysis/verify_field.py`](../analysis/verify_field.py) — Halbach wave model against magpylib, with an automatic probe for the polarity convention rather than an assumption | **Strong.** Also found where 2-D *cannot* work: P21, where infinite depth overestimates far field |
| Error-budget discipline | [`validation/bench/bench_predict.py`](../validation/bench/bench_predict.py) — derives bench acceptance bands by perturbing gap, remanence and thickness and re-solving; carries a guard that fails loudly if its geometry drifts from `verify_field.py` | **Strong.** Found two unit/definition errors by requiring reproduction of published values |
| Knowing when a cross-check is not one | P17 in [`OPEN_PROBLEMS.md`](../OPEN_PROBLEMS.md) — magpylib's `getFT()` converges 37 % from the analytic force; diagnosed as a Jensen-inequality artefact, `mean(B²)` vs `mean(B)²` | **Strong.** The diagnosis is the skill, not the discrepancy |

## Structural, thermal and multiphysics

| Claim | Evidence | Strength |
|---|---|---|
| Structural FEA from a real STEP file | [`validation/fea/build_deck.py`](../validation/fea/build_deck.py) — CalculiX deck built against `cad/step/gen3/EMOCD_Sled_Gen3.step` | Moderate — ran, passed three declared bands |
| Tolerance stack-up and its consequences | [`docs/MANUFACTURING.md`](MANUFACTURING.md) — airgap stack RSS 0.101 mm against a declared 0.05 mm shim spec, giving **1.58 % thrust spread against the 0.65 % claimed** | **Strong.** A 2.4× error found in the project's own published figure |
| Thermal budgeting, per-shot vs per-campaign | P4 in [`OPEN_PROBLEMS.md`](../OPEN_PROBLEMS.md) — the paper's 37 K "per shot" was the 12-shot adiabatic total; per shot is 3.0 K | Moderate. Found by rebuilding the arithmetic |
| Swept-excitation resonance reasoning | E23 in [`OPEN_PROBLEMS.md`](../OPEN_PROBLEMS.md) — force-ripple harmonics cross both track modes inside the first 4–50 ms of every shot; a static frequency check does not settle it | Moderate — *identified, not closed.* No Q or damping figure exists anywhere in the repository, and the entry says so |

## Astrodynamics

| Claim | Evidence | Strength |
|---|---|---|
| Orbit propagation and lifetime modelling | [`analysis/astro.py`](../analysis/astro.py) — orbit-averaged decay cross-checked against Cowell RK4 to 99.4 % | Moderate |
| Independent-tool validation, including when it goes against you | [`validation/gmat/`](../validation/gmat/) — GMAT R2022a **falsified a claim in the paper's own abstract** (P16). The lifetime-ratio invariance claim was a tautology: `scale` and `1/BC` occupy the same multiplicative slot | **Strong, and the best single item here.** The claim was retracted, not defended |
| Reading a competitor's method and conceding it is better | [`docs/PRIOR_ART.md`](PRIOR_ART.md) — Feng et al.'s 3-D reachable-domain envelope answers "which orbits does one shot make available" directly, where this project reports a scalar. Recorded as something to adopt | **Strong.** Judgement, not technique |

## Power electronics and pulsed power

| Claim | Evidence | Strength |
|---|---|---|
| Circuit simulation of a supercapacitor pulse chain | [`validation/spice/`](../validation/spice/) — ngspice against the analytical discharge model | Moderate. Ran; two findings, and A8 now predates the current operating point (P19) |
| ECU calibration and reverse engineering | **Outside this repository.** Powertronic's map files are an obfuscated binary; format reverse-engineered and a dual-map editor built (TronicLabs) | Moderate — no artefact here. Verifiable by demonstration |

## Cost and manufacturing engineering

| Claim | Evidence | Strength |
|---|---|---|
| Parametric BOM that contradicted the paper | [`analysis/cost.py`](../analysis/cost.py) — avionics 23.7 %, supercapacitors 17.8 %, SiC 13.3 %, **NdFeB only 4.8 %.** The paper had claimed magnets dominate | **Strong.** Conclusion holds even at 2× price errors, which is stated because every price is assumed and none is quoted |
| Qualification planning | [`docs/QUALIFICATION_PLAN.md`](QUALIFICATION_PLAN.md), [`docs/BENCHTOP_TESTS.md`](BENCHTOP_TESTS.md) — four benchtop tests cheapest-first, each closing a named claim against a band declared in advance | Moderate — **specified, not run.** That is the honest status |

## Software and tooling

| Claim | Evidence | Strength |
|---|---|---|
| Python numerical work | Six scripts in [`analysis/`](../analysis/) — numpy/scipy, reproducible from a clean checkout, JSON outputs | **Strong.** Verified to reproduce `v_exit = 16.537` from a clean copy |
| Refusing to duplicate a source of truth | [`paper/make_figures.py`](../paper/make_figures.py) imports the analysis rather than reimplementing it; [`tools/export_companion.py`](../tools/export_companion.py) generates the companion repos so they cannot drift; `_check_operating_point()` in `sizing.py` exits with a diagnostic if two modules disagree | **Strong.** Each guard exists because that exact divergence had already happened |
| Regression guarding | [`tools/make_baseline.py`](../tools/make_baseline.py) `--check` — compares 20 frozen values against live script output. Its first version was **broken** (the commit-hash header made it always fail); fixed, then verified against injected drift | **Strong.** Testing your own test is the point |
| Applied AI systems | **Outside this repository.** RAG retrieval pipeline, vector store and role-based dashboards shipped for a telecom CRM at Avisys | Moderate — no artefact here |

## Engineering process — the part that is actually unusual

This is the strongest section, and it is the one most people cannot evidence at all.

| Claim | Evidence |
|---|---|
| **Acceptance bands declared before the analysis runs** | Every file in [`validation/`](../validation/) states its band before its result. A failure therefore cannot be rationalised afterwards |
| **Defects published, including the ones that damage the work** | 22 P-items and 24 E-items in [`OPEN_PROBLEMS.md`](../OPEN_PROBLEMS.md). Two retracted claims in the paper's own abstract. An ADR argument found false and withdrawn |
| **Decisions recorded with alternatives and consequences** | 17 records in [`docs/adr/`](adr/), including [ADR-003](adr/003-linear-synchronous-motor.md), which carries its own amendment showing what it got wrong |
| **A single source of truth, enforced** | Scripts are authoritative over the paper, never the reverse. Four errors were found in the paper by rebuilding its analysis from scratch |
| **Provenance stated per claim** | [`PROVENANCE.md`](../PROVENANCE.md) and the per-source `verified`/`confirmed`/`lead` status in [`docs/RELATED_WORK.md`](RELATED_WORK.md) — a `lead` may not support a number in the paper |
| **Changing your mind in public** | [`CHANGELOG.md`](../CHANGELOG.md) logs every reversal with its cause, including three conclusions I drew from abstracts and then had to retract on reading the full papers |

## Formal coursework behind this

BTech Mechanical Engineering, SIT Pune. Directly relevant, from the programme structure:
**Finite Element Methods** · **Computational Fluid Dynamics** · Dynamics of Machines · Strength of
Materials · Heat Transfer · Engineering Thermodynamics · Fundamentals of Machine Design ·
Measurement and Metrology · Engineering Materials and Metallurgy · Composite Materials ·
Manufacturing Technology · Additive Manufacturing · Industrial Automation and Robotics ·
Introduction to Mechatronics · Numerical Methods.

## Tools

**CAD/CAE:** Fusion 360, SolidWorks, AutoCAD, ANSYS
**Open-source simulation:** scikit-fem, gmsh, GetDP, CalculiX, ngspice, GMAT, magpylib
**Programming:** Python (numpy, scipy, matplotlib), MATLAB, C
**Fabrication:** metal fabrication, 3-D printing, CNC, FMEA
**Other:** LaTeX, git, Figma

---

## Two things this page will not pretend

**1. Nothing here has been built, fired, or measured.** This is a design study at TRL 2–3. Every
number is a model output, and the two strongest results are cross-checks between models rather
than against hardware. Four of nine specified validations have run; two of those predate the
current operating point and need re-running (P19). If you are looking for evidence that I can
make hardware work, this repository does not contain it — what it contains is evidence about how
I handle analysis, uncertainty, and being wrong.

**2. The most persuasive items here are failures.** GMAT falsifying the abstract, the cost model
contradicting the paper, the tolerance stack coming out 2.4× worse than claimed, the ADR argument
found false, my own three retracted conclusions. That is deliberate: anyone can show you work that
went well. What is hard to fake is a record of catching yourself.
