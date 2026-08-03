# Inventory

Complete index of the work. Read alongside `PROVENANCE.md`.

**Baseline:** nothing in this list has been validated by hardware, FEA, or third-party
review. Every entry is a model output or a design decision, and several superseded
entries are kept only so the record of what changed stays legible.

---

## A. Calculations

| # | Item | Where it lives now |
|---|---|---|
| A1 | Recoil examples from earlier feasibility doc (ISS 420 t; 500 kg OTV) | superseded |
| A2 | Separation-speed equation check (FS = ½Mv² + ½M₁V²) | superseded |
| A3 | Δa from 1.5 m/s at 400 km | superseded |
| A4 | Hohmann 350 to 500 km; single-impulse ellipse correction | superseded |
| A5 | Constellation drift per 10 m/s; de-orbit Δv | `analysis/astro.py` |
| A6 | Coilgun single-stage efficiency literature check (1-2 %) | paper Sec. II |
| A7 | g-load vs barrel length | paper Sec. III-B |
| A8 | Energy budget & capacitor mass at 50-100 m/s | superseded |
| A9 | CMG momentum sizing vs line-of-action offset | superseded |
| A10 | Second-document checks (200 kg recoil, 30 m/s apogee, supercap, pulse power) | verification only |
| A11 | Tumble-rate plausibility to 780 °/s falsified | see E13 |
| A12 | Payload-limited velocity ceiling v=√(2aL) | paper Eq. 1 |
| A13 | Coilgun vs LSM energy-per-shot comparison | paper Table I |
| A14 | Magazine packing, feed forces, CoM shift, cadence | paper Sec. III-C |
| A15 | Stage-as-momentum-sink: Δv/shot, torque, RCS propellant, cant, slew | paper Sec. IX |
| A16 | Flywheel vs reaction wheel vs RCS (redundancy proof) | design decision D9 |
| A17 | Envelope/stroke limits; ironless vs iron stator mass | paper Sec. III-B |
| A18 | C1 orbital lifetime (Gauss orbit-averaged) | `analysis/astro.py` |
| A19 | C2 drift seeding vs differential drag | `analysis/astro.py` |
| A20 | C3 Halbach field + shot ODE + Monte Carlo | superseded by A28/A29 |
| A21 | C4 eddy-brake sizing | `legacy/c3_c4_em.py` |
| A22 | C5 conjunction screening (v1 bugged to v2 staggered) | `analysis/astro.py` |
| A23 | C6, C10 host attitude, tip-off, rollups, error map, payload family | `analysis/` |
| A24 | magpylib field verification (two sign errors caught by probing) | `analysis/verify_field.py` |
| A25 | Sled-arrest force mismatch, earlier regen claim falsified | design decision D8 |
| A26 | Abort commit point recomputed (~45 %) | paper Sec. III-D |
| A27 | Efficiency bookkeeping error found (40 % to 32 %; now 20 % at the CAD-derived sled mass) | paper Sec. V-A |
| A28 | Winding-resolved thrust constant Kt = 11.03 N per kA/m | `analysis/motor_model.py` |
| A29 | Closed-loop servo Monte Carlo (3σ = 0.027 m/s) | `analysis/motor_model.py` |
| A30 | Solid mass properties (76.5 kg dry, sled 9.445 kg CAD-derived) | `analysis/mass_properties.py`, parametric 4.86 kg superseded 2026-07-29 |
| A31 | Cowell RK4 cross-validation (99.4 %) | `analysis/astro.py` |
| A32 | Solar-activity UQ, x1.62 multiplier | `analysis/astro.py`, **invariance falsified by GMAT, see P16**; BC half is the same tautology |
| A33 | Refined conjunction at final velocity | `analysis/astro.py`, see P1 |
| A34 | Strategy-doc verification (recoil, propellant, capacitor, trim tables) | verification only |
| A35 | Mechanical/thermal/electrical sizing anchors | `analysis/sizing.py` |
| A36 | Retention-gate resize (margin 0.5 to two D6 pins, 1.2) | `analysis/sizing.py` |
| A37 | **Recurring hardware cost, parametric BOM**: all prices assumed, no quotations | `analysis/cost.py`, corrects the paper's claim that magnets dominate |

## B. Design decisions and when they changed

Reasoning is recorded in `docs/DECISION_LOG.md`.

| # | Decision |
|---|---|
| B1 | Core concept: EM launcher on a rideshare placing sats in own orbits |
| B2 | Original dual option: maglev rail *or* coilgun |
| B3 | Reluctance to induction coilgun |
| B4 | **Coilgun to linear synchronous motor** (mid-2025) |
| B5 | Ironless vs iron-core stator |
| B6 | Reusable sled vs armature on customer satellite |
| B7 | Dual transverse cassettes vs revolver / 2-DOF / tandem |
| B8 | Eddy brake + ring spring replaces regen-only arrest |
| B9 | No CMG/flywheel in attached mode |
| B10 | Fixed cant instead of gimballed barrel |
| B11 | Aft ESPA port, barrel parallel, fire forward |
| B12 | Fire-last ConOps |
| B13 | Retention gate separating preload from release path |
| B14 | Three-inhibit no-fire chain |
| B15 | Coast-and-trim release zone |
| B16 | Materials rules (non-conductive on field, non-magnetic near track, E595) |
| B17 | POEM as host and flight-demo path |
| B18 | VOLLEY-A / VOLLEY-F variant split |
| B19 | Scope narrowed to 3U baseline claim |
| B20 | Rated sheet current 130 to 140 kA/m |
| B21 | Paper reframed host-specific to host-agnostic |
| B22 | Value proposition to propulsion-less niche + drift seeding |
| B23 | Publish publicly |

## C. Diagrams and CAD

| # | Item | Status |
|---|---|---|
| C1 | System block diagram | `paper/figures/D01_block.png` |
| C2 | Plan-view layout | `paper/figures/D02_layout.png` |
| C3 | Figure set v1 (11 figures) | superseded, `legacy/make_figs.py` |
| C4 | Figure set v2 at final numbers | `paper/figures/` |
| C5 | Concept illustration | `legacy/concept.py` |
| C6 | **CAD assembly** | `cad/`, 9 Fusion 360 documents in 3 generations; Gen3 current, plus a monolithic `EMOCD_Gen3.step` |
| C7 | **FEMM / FEA field maps** | does not exist, run sheet only |
| C8 | CAD generation history and defect audit | `cad/CHANGELOG_CAD.md` |

## D. Documents

| # | Item | Status |
|---|---|---|
| D1 | Verification report, feasibility PDF | not in repo |
| D2 | Verification report, consolidated docx | not in repo |
| D3 | Verification of strategy document | not in repo |
| D4 | Launch-ecosystem research report | not in repo |
| D5 | Computation results C1, C10 | `docs/`, **superseded**, old operating point |
| D6 | PBL-2 skeleton (19 pp, Annexure format) | not in repo |
| D7 | Figure pack | `paper/figures/` |
| D8 | FEMM run sheet | `analysis/femm/FEMM_RUN_SHEET.md` (current); `docs/FEMM_Run_Sheet.md` superseded; band in `validation/A1_field_femm.md` |
| D9 | IEEE showcase paper (5 pp, text-only) | superseded |
| D10 | IEEE conference paper (10 pp) | `paper/` |
| D11 | LaTeX source | `paper/paper.tex` |
| D12 | Reproducibility package | this repo |
| D13 | Analysis scripts | `analysis/` + `legacy/` |
| D14 | LinkedIn announcement post | not in repo |
| D15 | **Qualification and environmental test plan** | `docs/QUALIFICATION_PLAN.md`, specified, none run |
| D16 | **Benchtop test protocol** (4 sub-scale experiments, bands declared) | `docs/BENCHTOP_TESTS.md`, specified, none run |
| D17 | **Project history and milestone tags** | `HISTORY.md`, records that the git history below 2026-07-23 was reconstructed |

## E. Open problems

Full detail in `OPEN_PROBLEMS.md`. Summary: P1, P4 are errors in the published paper
(conjunction minimum, peak current, stray far-field, fin temperature), corrected in
`paper.tex`, though P11 asks whether those corrections reached the submitted build.
P5, P10 come out of the CAD build, and P12 records two places where the paper's prose
contradicts it, including an ESPA-Grande envelope claim the CAD does not support. E1, E18 are unsolved engineering, of which the
load-bearing ones are 3-D field closure, the absence of FEA and hardware, and the
patent position now that disclosure has happened.

## F. External sources

30 sources cited across the work; 21 were fetched and read directly ("verified"), the
remainder cited without retrieval and **should be re-checked before publication**. Full
list with verification status is in the paper bibliography and `PROVENANCE.md`. Three
references (eddy-damper heritage, Yudintsev, vibro-impact deployment) remain explicitly
unverified, see `OPEN_PROBLEMS.md` E16.
