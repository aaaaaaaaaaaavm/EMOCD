# Inventory

Complete index of the work, with provenance. Produced by walking the full chat
transcript. Read alongside `PROVENANCE.md`.

Markings: `[ME]` owner-originated · `[YOU]` AI-generated, unverified by owner ·
`[BOTH]` jointly worked or owner-corrected.

**Baseline:** the overwhelming majority is `[YOU]`. The owner directed, chose, rejected
and caught framing errors, but did not independently re-derive or re-run any
calculation. No hardware, no CAD, no FEA, no third-party review exists.

---

## A. Calculations

| # | Item | Where it lives now | Prov. |
|---|---|---|---|
| A1 | Recoil examples from uploaded feasibility doc (ISS 420 t; 500 kg OTV) | superseded | [YOU] |
| A2 | Separation-speed equation check (FS = ½Mv² + ½M₁V²) | superseded | [YOU] |
| A3 | Δa from 1.5 m/s at 400 km | superseded | [YOU] |
| A4 | Hohmann 350→500 km; single-impulse ellipse correction | superseded | [YOU] |
| A5 | Constellation drift per 10 m/s; de-orbit Δv | `analysis/astro.py` | [YOU] |
| A6 | Coilgun single-stage efficiency literature check (1–2 %) | paper Sec. II | [YOU] |
| A7 | g-load vs barrel length | paper Sec. III-B | [YOU] |
| A8 | Energy budget & capacitor mass at 50–100 m/s | superseded | [YOU] |
| A9 | CMG momentum sizing vs line-of-action offset | superseded | [YOU] |
| A10 | Second-document checks (200 kg recoil, 30 m/s apogee, supercap, pulse power) | verification only | [YOU] |
| A11 | Tumble-rate plausibility → 780 °/s falsified | see E13 | [YOU] |
| A12 | Payload-limited velocity ceiling v=√(2aL) | paper Eq. 1 | [YOU] |
| A13 | Coilgun vs LSM energy-per-shot comparison | paper Table I | [YOU] |
| A14 | Magazine packing, feed forces, CoM shift, cadence | paper Sec. III-C | [YOU] |
| A15 | Stage-as-momentum-sink: Δv/shot, torque, RCS propellant, cant, slew | paper Sec. IX | [BOTH] |
| A16 | Flywheel vs reaction wheel vs RCS (redundancy proof) | design decision D9 | [BOTH] |
| A17 | Envelope/stroke limits; ironless vs iron stator mass | paper Sec. III-B | [YOU] |
| A18 | C1 orbital lifetime (Gauss orbit-averaged) | `analysis/astro.py` | [YOU] |
| A19 | C2 drift seeding vs differential drag | `analysis/astro.py` | [YOU] |
| A20 | C3 Halbach field + shot ODE + Monte Carlo | superseded by A28/A29 | [YOU] |
| A21 | C4 eddy-brake sizing | `legacy/c3_c4_em.py` | [YOU] |
| A22 | C5 conjunction screening (v1 bugged → v2 staggered) | `analysis/astro.py` | [YOU] |
| A23 | C6–C10 host attitude, tip-off, rollups, error map, payload family | `analysis/` | [YOU] |
| A24 | magpylib field verification (two sign errors caught by probing) | `analysis/verify_field.py` | [YOU] |
| A25 | Sled-arrest force mismatch — earlier regen claim falsified | design decision D8 | [YOU] |
| A26 | Abort commit point recomputed (~45 %) | paper Sec. III-D | [YOU] |
| A27 | Efficiency bookkeeping error found (40 % → 32 %) | paper Sec. V-A | [YOU] |
| A28 | Winding-resolved thrust constant Kt = 11.22 N per kA/m | `analysis/motor_model.py` | [YOU] |
| A29 | Closed-loop servo Monte Carlo (3σ = 0.027 m/s) | `analysis/motor_model.py` | [YOU] |
| A30 | Parametric solid mass properties (72.3 kg dry, sled 4.86 kg) | `analysis/mass_properties.py` | [YOU] |
| A31 | Cowell RK4 cross-validation (99.4 %) | `analysis/astro.py` | [YOU] |
| A32 | Solar-activity UQ, ×1.80 invariance | `analysis/astro.py` | [YOU] |
| A33 | Refined conjunction at final velocity | `analysis/astro.py` — see P1 | [YOU] |
| A34 | Strategy-doc verification (recoil, propellant, capacitor, trim tables) | verification only | [YOU] |
| A35 | Mechanical/thermal/electrical sizing anchors | `analysis/sizing.py` | [YOU] |
| A36 | Retention-gate resize (margin 0.5 → two D6 pins, 1.2) | `analysis/sizing.py` | [YOU] |
| A37 | LinkedIn character counts (measured after guessing) | n/a | [BOTH] |

## B. Design decisions and when they changed

Reasoning is recorded in `docs/DECISION_LOG.md`.

| # | Decision | Prov. |
|---|---|---|
| B1 | Core concept: EM launcher on a rideshare placing sats in own orbits | [ME] |
| B2 | Original dual option: maglev rail *or* coilgun | [ME] |
| B3 | Reluctance → induction coilgun | [YOU] |
| B4 | **Coilgun → linear synchronous motor** (mid-2025) | [BOTH] |
| B5 | Ironless vs iron-core stator | [YOU] |
| B6 | Reusable sled vs armature on customer satellite | [YOU] |
| B7 | Dual transverse cassettes vs revolver / 2-DOF / tandem | [YOU] |
| B8 | Eddy brake + ring spring replaces regen-only arrest | [YOU] |
| B9 | No CMG/flywheel in attached mode | [BOTH] |
| B10 | Fixed cant instead of gimballed barrel | [YOU] |
| B11 | Aft ESPA port, barrel parallel, fire forward | [YOU] |
| B12 | Fire-last ConOps | [YOU] |
| B13 | Retention gate separating preload from release path | [YOU] |
| B14 | Three-inhibit no-fire chain | [YOU] |
| B15 | Coast-and-trim release zone | [YOU] |
| B16 | Materials rules (non-conductive on field, non-magnetic near track, E595) | [YOU] |
| B17 | POEM as host and flight-demo path | [ME] |
| B18 | EMOCD-A / EMOCD-F variant split | [BOTH] |
| B19 | Scope narrowed to 3U baseline claim | [YOU] |
| B20 | Rated sheet current 130 → 140 kA/m | [YOU] |
| B21 | Paper reframed host-specific → host-agnostic | [ME] |
| B22 | Value proposition → propulsion-less niche + drift seeding | [YOU] |
| B23 | Publish publicly | [ME] |

## C. Diagrams and CAD

| # | Item | Status | Prov. |
|---|---|---|---|
| C1 | System block diagram | `paper/figures/D01_block.png` | [YOU] |
| C2 | Plan-view layout | `paper/figures/D02_layout.png` | [YOU] |
| C3 | Figure set v1 (11 figures) | superseded, `legacy/make_figs.py` | [YOU] |
| C4 | Figure set v2 at final numbers | `paper/figures/` | [YOU] |
| C5 | Concept illustration (LinkedIn) | `legacy/concept.py` | [YOU] |
| C6 | **CAD assembly** | does not exist — owner to produce | [ME] |
| C7 | **FEMM / FEA field maps** | does not exist — run sheet only | — |

## D. Documents

| # | Item | Status | Prov. |
|---|---|---|---|
| D1 | Verification report, uploaded feasibility PDF | chat only | [YOU] |
| D2 | Verification report, consolidated docx | chat only | [YOU] |
| D3 | Verification of strategy document | chat only | [YOU] |
| D4 | Launch-ecosystem research report | chat only | [YOU] |
| D5 | Computation results C1–C10 | `docs/` | [YOU] |
| D6 | PBL-2 skeleton (19 pp, Annexure format) | not in repo | [YOU] |
| D7 | Figure pack | `paper/figures/` | [YOU] |
| D8 | FEMM run sheet | `docs/` — needs update, see E1 | [YOU] |
| D9 | IEEE showcase paper (5 pp, text-only) | superseded | [YOU] |
| D10 | IEEE conference paper (10 pp) | `paper/` | [YOU] |
| D11 | LaTeX source | `paper/paper.tex` | [YOU] |
| D12 | Reproducibility package | this repo | [YOU] |
| D13 | Analysis scripts | `analysis/` + `legacy/` | [YOU] |
| D14 | LinkedIn post (2,991 chars) | not in repo | [BOTH] |

## E. Open problems

Full detail in `OPEN_PROBLEMS.md`. Summary: P1–P4 are errors in the published paper
(conjunction minimum, peak current, stray far-field, fin temperature). E1–E16 are
unsolved engineering, of which the load-bearing ones are 3-D field closure, absence of
CAD, absence of hardware, and the unresolved patent/disclosure question.

## F. External sources

30 sources cited across the work; 21 were fetched and read in-session ("verified"),
the remainder cited from model knowledge and **should be re-checked before
publication**. Full list with verification status is in the paper bibliography and
`PROVENANCE.md`. Three references (eddy-damper heritage, Yudintsev, vibro-impact
deployment) remain explicitly unverified — see `OPEN_PROBLEMS.md` E16.
