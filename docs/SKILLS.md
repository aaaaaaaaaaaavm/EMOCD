# Skills, and the file that proves each one

**Adityavardhan Mishra** · BTech Mechanical Engineering, Symbiosis Institute of Technology, Pune
(2023-2027) · [adityavardhanmishr@gmail.com](mailto:adityavardhanmishr@gmail.com) ·
[linkedin.com/in/adityavardhanmishra](https://www.linkedin.com/in/adityavardhanmishra/)

An unevidenced skills list is worth nothing, so this one carries the evidence inline. **Every row
points at a file in this repository that you can open and run.** Where a claim rests on something
outside the repository, the row says so and says what the evidence actually is.

The caveats at the bottom are part of the page, not a disclaimer appended to it. Read them with
the rest.

---

## Electromagnetics and finite-element analysis

| Claim | Evidence | Strength |
|---|---|---|
| 2-D magnetostatic FEM, written from the weak form | [`validation/fem/a1_airgap_field.py`](../validation/fem/a1_airgap_field.py), scikit-fem, gmsh meshing at 141 k elements, vector-potential formulation with a remanence source term | **Strong.** Confirmed the winding-resolved thrust constant to **0.07 %**: an independent PDE solve, not a second superposition |
| Analytic field modelling, and knowing its limits | [`analysis/verify_field.py`](../analysis/verify_field.py), Halbach wave model against magpylib, with an automatic probe for the polarity convention rather than an assumption | **Strong.** Also found where 2-D *cannot* work: P21, where infinite depth overestimates far field |
| Error-budget discipline | [`validation/bench/bench_predict.py`](../validation/bench/bench_predict.py), derives bench acceptance bands by perturbing gap, remanence and thickness and re-solving; carries a guard that fails loudly if its geometry drifts from `verify_field.py` | **Strong.** Found two unit/definition errors by requiring reproduction of published values |
| Knowing when a cross-check is not one | P17 in [`OPEN_PROBLEMS.md`](../OPEN_PROBLEMS.md), magpylib's `getFT()` converges 37 % from the analytic force; diagnosed as a Jensen-inequality artefact, `mean(B²)` vs `mean(B)²` | **Strong.** The diagnosis is the skill, not the discrepancy |

## Structural, thermal and multiphysics

| Claim | Evidence | Strength |
|---|---|---|
| Structural FEA from a real STEP file | [`validation/fea/build_deck.py`](../validation/fea/build_deck.py), CalculiX deck built against `cad/step/gen3/EMOCD_Sled_Gen3.step` | Moderate, ran, passed three declared bands |
| Tolerance stack-up and its consequences | [`docs/MANUFACTURING.md`](MANUFACTURING.md), airgap stack RSS 0.101 mm against a declared 0.05 mm shim spec, giving **1.58 % thrust spread against the 0.65 % claimed** | **Strong.** A 2.4x error found in the project's own published figure |
| Thermal budgeting, per-shot vs per-campaign | P4 in [`OPEN_PROBLEMS.md`](../OPEN_PROBLEMS.md), the paper's 37 K "per shot" was the 12-shot adiabatic total; per shot is 3.0 K | Moderate. Found by rebuilding the arithmetic |
| Swept-excitation resonance reasoning | E23 in [`OPEN_PROBLEMS.md`](../OPEN_PROBLEMS.md), force-ripple harmonics cross both track modes inside the first 4-50 ms of every shot; a static frequency check does not settle it | Moderate, *identified, not closed.* No Q or damping figure exists anywhere in the repository, and the entry says so |

## Astrodynamics

| Claim | Evidence | Strength |
|---|---|---|
| Orbit propagation and lifetime modelling | [`analysis/astro.py`](../analysis/astro.py), orbit-averaged decay cross-checked against Cowell RK4 to 99.4 % | Moderate |
| Independent-tool validation, including when it goes against you | [`validation/gmat/`](../validation/gmat/), GMAT R2022a **falsified a claim in the paper's own abstract** (P16). The lifetime-ratio invariance claim was a tautology: `scale` and `1/BC` occupy the same multiplicative slot | **Strong, and the best single item here.** The claim was retracted, not defended |
| Reading a competitor's method and conceding it is better | [`docs/PRIOR_ART.md`](PRIOR_ART.md), Feng et al.'s 3-D reachable-domain envelope answers "which orbits does one shot make available" directly, where this project reports a scalar. Recorded as something to adopt | **Strong.** Judgement, not technique |

## Power electronics and pulsed power

| Claim | Evidence | Strength |
|---|---|---|
| Circuit simulation of a supercapacitor pulse chain | [`validation/spice/`](../validation/spice/), ngspice against the analytical discharge model | **Strong.** Ran twice, at both operating points. The second run found a loss term the analytic model was missing entirely (P24), and the two methods now agree on peak current to 0.01 % |
| ECU calibration and reverse engineering | **Outside this repository.** Powertronic's map files are an obfuscated binary; format reverse-engineered and a dual-map editor built (TronicLabs) | Moderate, no artefact here. Verifiable by demonstration |

## Cost and manufacturing engineering

| Claim | Evidence | Strength |
|---|---|---|
| Parametric BOM that contradicted the paper | [`analysis/cost.py`](../analysis/cost.py), avionics 23.7 %, supercapacitors 17.8 %, SiC 13.3 %, **NdFeB only 4.8 %.** The paper had claimed magnets dominate | **Strong.** Conclusion holds even at 2x price errors, which is stated because every price is assumed and none is quoted |
| Qualification planning | [`docs/QUALIFICATION_PLAN.md`](QUALIFICATION_PLAN.md), [`docs/BENCHTOP_TESTS.md`](BENCHTOP_TESTS.md), four benchtop tests cheapest-first, each closing a named claim against a band declared in advance | Moderate, **specified, not run.** That is the honest status |

## Software and tooling

| Claim | Evidence | Strength |
|---|---|---|
| Python numerical work | Six scripts in [`analysis/`](../analysis/), numpy/scipy, reproducible from a clean checkout, JSON outputs | **Strong.** Reproduced `v_exit = 16.388` from a clean copy |
| Refusing to duplicate a source of truth | [`paper/make_figures.py`](../paper/make_figures.py) imports the analysis rather than reimplementing it; [`tools/export_companion.py`](../tools/export_companion.py) generates the companion repos so they cannot drift; `_check_operating_point()` in `sizing.py` exits with a diagnostic if two modules disagree | **Strong.** Each guard exists because that exact divergence had already happened |
| Regression guarding | [`tools/make_baseline.py`](../tools/make_baseline.py) `--check` compares 20 frozen values against live script output; [`check_links.py`](../tools/check_links.py) every link and the shared repo table; [`check_artifacts.py`](../tools/check_artifacts.py) every built artifact against its source, by commit time rather than mtime so it survives a clone | **Strong.** Each was verified against a real failure rather than assumed to work: the baseline check against injected drift, the artifact check against the commit where a stale PDF actually shipped |
| Applied AI systems | **Outside this repository.** RAG retrieval pipeline, vector store and role-based dashboards shipped for a telecom CRM at Avisys | Moderate, no artefact here |

## Engineering process: the part that is actually unusual

This is the strongest section, and it is the one most people cannot evidence at all.

| Claim | Evidence |
|---|---|
| **Acceptance bands declared before the analysis runs** | Every file in [`validation/`](../validation/) states its band before its result. A failure therefore cannot be rationalised afterwards |
| **Defects published, including the ones that damage the work** | 27 P-items and 24 E-items in [`OPEN_PROBLEMS.md`](../OPEN_PROBLEMS.md). Two retracted claims in the paper's own abstract. An ADR argument found false and withdrawn |
| **Decisions recorded with alternatives and consequences** | 18 records in [`docs/adr/`](adr/), including [ADR-003](adr/003-linear-synchronous-motor.md), which carries its own amendment showing what it got wrong |
| **A single source of truth, enforced** | Scripts are authoritative over the paper, never the reverse. Four errors were found in the paper by rebuilding its analysis from scratch |
| **Provenance stated per claim** | [`PROVENANCE.md`](PROVENANCE.md) and the per-source `verified`/`confirmed`/`lead` status in [`docs/RELATED_WORK.md`](RELATED_WORK.md), a `lead` may not support a number in the paper |
| **Changing your mind in public** | [`CHANGELOG.md`](../CHANGELOG.md) logs every reversal with its cause, including three conclusions I drew from abstracts and then had to retract on reading the full papers |

## A second electromagnetic launch study, in a different g-regime

**Electromagnetic Launch System for Vertical Silo-Based Deployment**, sole-authored feasibility
study, IEEE format, 12 references. Not part of this repository; listed because it is the same
architecture solved for a different payload.

| | |
|---|---|
| Concept | Magazine-fed electromagnetic launch: belt-feed indexing, pulsed coilgun ejection, ignition deferred to 20 m altitude so no thermal event occurs inside the structure |
| Scale | 500 kg booster class, 50 m/s exit, **2.50-4.17 MJ per launch** across a sourced 15-25 % efficiency band, **10.6-15.0 cycles/min** on a 1 MW supply, *corrected; the paper prints 18.5* |
| Method | First-order energy, ballistic and g-load analysis. Names its own next step: ANSYS structural validation plus a subscale coilgun efficiency test |

### Two defects in it, found 2026-08-05 and recorded here because it has no defect log of its own

**Two of Table III's four rate-of-fire rows do not follow from its own caption.** The caption
fixes `t_index = 1.5 s` and the text gives `t_cycle = E_input/P + t_index`, `ROF = 60/t_cycle`.
Applying that:

| Generator | η | t_recharge | ROF as specified | Printed |
|---|---|---:|---:|---:|
| 500 kW | 15 % | 8.34 s | 6.10 | 6.1 |
| 500 kW | 25 % | 5.00 s | **9.23** | **8.6**, which implies t_index = 1.98 s |
| 1 MW | 15 % | 4.17 s | 10.58 | 10.6 |
| 1 MW | 25 % | 2.50 s | **15.00** | **18.5**, which implies t_index = 0.74 s |

The 18.5 propagates into the abstract ("10-18 launches per minute") and the conclusion
("10.6-18.5 rounds per minute"), so the headline cadence claim is high by 23 %. The 8.6 is wrong
in the conservative direction and had not been noticed at all. Neither error touches the energy
analysis, which is the paper's substance; both are in the number a reader quotes.

**The abstract claims an analysis the paper does not contain.** It states that "key engineering
challenges — g-load tolerance, **electromagnetic coupling**, and pulsed power thermal management
— are identified and analyzed." Section IX lists six challenges and electromagnetic coupling is
not among them, nor does it appear anywhere in the body.

That is the same gap this repository carries as **E12**, and the pair is worth stating plainly:
**two electromagnetic launch studies, and neither contains an EMI calculation.** One dropped an
architecture partly on electromagnetic grounds without computing them
([`HISTORY.md`](HISTORY.md#why-the-coilgun-was-actually-dropped)); the other lists the analysis in
its abstract without performing it. Nothing about that is fatal to either paper, and it is the
strongest available argument for closing E12 rather than carrying it.

**The reason it belongs next to VOLLEY.** It selects a **coilgun**; VOLLEY
[rejects one](adr/003-linear-synchronous-motor.md). That is the same trade resolved in opposite
directions, and the thing that decides it is the payload:

```
s_min = v² / (2·n·g)          the same equation sizes both machines

silo    50 m/s, 15 m rail  ->  8.5 g   against a 10–15 g propellant grain
VOLLEY   16.5 m/s, 1.5 m    -> 10.7 g   against a  ~14 g CubeSat
Feng    321.6 m/s, 3.9 m   -> 1352 g   against a  ~14 g CubeSat
```

Two designs sized by what the payload tolerates, and a published third that was not. Getting the
same trade right twice, in regimes that demand opposite answers, is a better signal than getting it
right once.

**It also settles something in this repository.** ADR-003 asserted coilgun efficiency of "1-2 % in
the literature" with no source, and [`PRIOR_ART.md`](PRIOR_ART.md) found that false. The silo paper
carries the properly-referenced survey that should have been cited all along: **5-6 %** sub-kilogram,
**14.5 %** at 0.45 kg single-stage, **15 % measured** at 100 kg (Hanwha), **20-25 % simulated** at
1000 kg. The correct figure was sitting in my own other paper.

## Design studies: coursework

Listed as coursework, with the course named, because that is what they are. None is peer-reviewed.

| Study | What it covers |
|---|---|
| **Hydrogen, ammonia dual-fuel SI engine with plasma-assisted combustion** | Ammonia as a carbon-free carrier, hydrogen as combustion enhancer, load-dependent blend ratio, plasma ignition to overcome ammonia's low flame speed. The most substantial of these |
| **Dry-sump two-stroke with direct injection and catalytic converter** | Separates lubrication from the crankcase and injects after exhaust-port closure, attacking two-stroke scavenging losses at the source |
| **IC Engine & E-Mobility project file** | SI/CI fuel-injection systems compared (TBI, MPFI, GDI, inline/distributor, unit injector, CRDI) plus hybrid architecture |
| **FocusLens** | Prototype Android lensometer using the phone camera and calibrated optics; image processing and curvature-based diopter estimation. Independent project |
| **Adaptive transmission** | Hydraulically controlled chain/belt drive modulating RPM through tension variation; torque and power simulated in Fusion 360 and ANSYS. Independent project |
| **Two-stage gear-train supercharger** | **Completed**: previous final-year project, closed out in third year. 1:5 RPM multiplication within cleared gear-stress margins, letting a standard high-torque DC motor replace an ultra-high-speed unit. Metal-fabricated, FMEA completed |

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

## What this page will not pretend

**1. Nothing here has been built, fired, or measured.** This is a design study at TRL 2-3. Every
number is a model output, and the two strongest results are cross-checks between models rather
than against hardware. Four of nine specified validations have run; one of those predates the
current operating point and needs re-running (P19). If you are looking for evidence that I can
make hardware work, this repository does not contain it, what it contains is evidence about how
I handle analysis, uncertainty, and being wrong.

**2. The most persuasive items here are failures.** GMAT falsifying the abstract, the cost model
contradicting the paper, the tolerance stack coming out 2.4x worse than claimed, the ADR argument
found false, my own three retracted conclusions. That is deliberate: anyone can show you work that
went well. What is hard to fake is a record of catching yourself.

**3. This page is held to the same rule as the paper.** A claim here has to be checkable against
the artifact it names, not against a summary of it. Anything peer-reviewed says so and names the
venue; anything coursework says so and names the course; anything unsubmitted is called a
manuscript. Two manuscripts here are written and unsubmitted, and both are described that way.
