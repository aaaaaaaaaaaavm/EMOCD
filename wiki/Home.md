# EMOCD — Electromagnetic Orbital CubeSat Deployer

Wiki landing page. Source of truth stays in the repository:
[aaaaaaaaaaaavm/emocd](https://github.com/aaaaaaaaaaaavm/emocd). This page summarises
what exists and points at it; when the two disagree, the repository is right.

**Read [`PROVENANCE.md`](https://github.com/aaaaaaaaaaaavm/emocd/blob/main/PROVENANCE.md)
before citing anything here.** Every quantity on this page is a model output. None of it
has been measured, tested, or reviewed by a third party.

---

## What it is

CubeSats flown as rideshare secondaries inherit the primary customer's orbit. The spring
that ejects them adds 1–2 m/s — enough to drift clear of the stage, not enough to change
an orbit. A satellite with no propulsion of its own stays there for life.

EMOCD replaces the spring with an ironless double-sided Halbach linear synchronous motor
driving a reusable magnetic sled along a 1.5 m track. Twelve 3U CubeSats feed from two
transverse cassettes and fire one at a time. The customer satellite is never modified —
the magnets ride the sled, not the payload.

The target regime is the gap between spring deployers (~2 m/s) and propulsive orbital
transfer vehicles (hundreds of m/s).

## Maturity

| | |
|---|---|
| TRL | 2–3 |
| Analysis | 5 Python scripts, reproducible, outputs committed as JSON |
| CAD | 9 Fusion 360 documents, STEP exports committed ([`cad/`](https://github.com/aaaaaaaaaaaavm/emocd/tree/main/cad)) |
| FEA | none |
| Hardware | none |
| Independent review | none |

## Headline results

All figures are script outputs, not measurements.

| Quantity | Value | Script |
|---|---|---|
| Thrust constant | 11.22 N per kA/m, ±1.26 % ripple | `motor_model.py` |
| Exit velocity, 3U | 20.37 m/s at 16.3 g | `motor_model.py` |
| Electrical→payload efficiency | 32 % (2.63 kJ drawn, 830 J delivered) | `motor_model.py` |
| Closed-loop dispersion | 0.027 m/s (3σ) → ±0.10 km apogee | `motor_model.py` |
| Orbital lifetime multiplier | ×1.80, invariant across BC and solar activity | `astro.py` |
| Constellation seeding | 30° in 1.4–6.9 days vs 25 days by differential drag | `astro.py` |
| Dry / loaded mass | 72.3 kg / 120.3 kg | `mass_properties.py` |
| Recoil per shot | 81.5 N·s | `astro.py` |
| Track first mode | 109 Hz fixed-fixed (target >70) | `sizing.py` |
| Energy closure | 100.1 % accounted | `sizing.py` |

Payload family (`motor_model.py`): 1U 24.4 m/s at 23.4 g · 3U 20.4 m/s at 16.3 g ·
6U 16.9 m/s at 11.2 g · 12U 14.8 m/s at 8.5 g. The 6U and 12U cases are force-limited
consequences of the 3U design, not designed variants (see E9).

> **CAD structural reconciliation is pending (P5/P8).** The table assumes the 4.86 kg
> parametric sled from `mass_properties.py`. The first-pass Fusion sled (6 mm Ti-6Al-4V
> chassis, no structural FEA behind it) comes out heavier — provisionally ~7.50 kg —
> which would drop exit velocity to a provisional ~17.88 m/s and move efficiency, recoil,
> and the lifetime multiplier with it. The numbers above are left as the scripts compute
> them until ANSYS closes the sled mass. Scripts stay authoritative for performance; CAD
> is authoritative for geometry and fit only.

Two results have independent cross-checks: the Halbach airgap field (analytic wave model
vs magpylib, agreeing to three digits) and orbital decay (orbit-averaged Gauss vs Cowell
RK4, 99.4 %). Everything else is single-sourced and correspondingly weaker.

## Design decisions that are locked

These were argued out and should not be silently reopened; reasoning is in
[`docs/DECISION_LOG.md`](https://github.com/aaaaaaaaaaaavm/emocd/blob/main/docs/DECISION_LOG.md).

- **Linear synchronous motor, not a coilgun.** The payload's own g-limit caps exit
  velocity near 26–35 m/s whatever the launcher, which erases the coilgun's only
  advantage while keeping its costs: 1–2 % single-stage efficiency, an armature bolted to
  the customer satellite, and no abort path.
- **Ironless double-sided Halbach stator**, reusable sled carrying the magnets.
- **Eddy-current brake for arrest.** Motor regeneration alone cannot stop the sled —
  braking force is bounded by the same thrust constant as acceleration.
- **Sled kinetic energy is dissipated, not recovered.** The 32 % figure is therefore
  electrical-to-payload, with no regeneration credit.
- **No CMGs or thrusters in attached mode**; the host stage absorbs recoil.
- **Two transverse cassettes of six**, alternating feed to keep the centre of mass
  symmetric.
- **Retention gate carries ascent preload straight into structure**, bypassing the
  release mechanism — this is the NanoRacks ball-lock lesson, and it is deliberate.

## Repository map

| Path | Contents |
|---|---|
| [`analysis/`](https://github.com/aaaaaaaaaaaavm/emocd/tree/main/analysis) | current scripts; these reproduce the numbers above |
| `analysis/femm/` | FEMM magnetostatics package: cross-section DXF + run sheet (analysis A1, not yet run) |
| `analysis/results/` | script outputs as JSON |
| [`cad/`](https://github.com/aaaaaaaaaaaavm/emocd/tree/main/cad) | `parameters.json` (geometry source of truth), `step/` exports, `renders/` |
| [`paper/`](https://github.com/aaaaaaaaaaaavm/emocd/tree/main/paper) | IEEE conference paper — LaTeX source, figures, PDF |
| [`legacy/`](https://github.com/aaaaaaaaaaaavm/emocd/tree/main/legacy) | superseded scripts, kept for history — **do not cite** |
| [`docs/`](https://github.com/aaaaaaaaaaaavm/emocd/tree/main/docs) | computation notes C1–C10, FEMM run sheet, decision log, related work |
| [`validation/`](https://github.com/aaaaaaaaaaaavm/emocd/tree/main/validation) | cross-check plan — FEMM, CalculiX, Orekit, CARA, Chrono — with acceptance bands declared before the runs; nothing run yet |
| [`INVENTORY.md`](https://github.com/aaaaaaaaaaaavm/emocd/blob/main/INVENTORY.md) | indexed catalogue of every calculation, decision, and artifact |
| [`OPEN_PROBLEMS.md`](https://github.com/aaaaaaaaaaaavm/emocd/blob/main/OPEN_PROBLEMS.md) | known paper errors and unsolved engineering |
| [`CHANGELOG.md`](https://github.com/aaaaaaaaaaaavm/emocd/blob/main/CHANGELOG.md) | what changed, when, and why |

## Reproducing the numbers

```bash
pip install -r requirements.txt
cd analysis
python3 verify_field.py       # ~10 s   magpylib cross-check of the airgap field
python3 mass_properties.py    # instant parametric mass rollup
python3 motor_model.py        # ~2 min  Kt, shot sim, 800-run closed-loop Monte Carlo
python3 sizing.py             # instant mechanical, thermal, electrical margins
python3 astro.py              # ~10 min decay integrations, 30-day propagations
```

Results land in `analysis/results/*.json`. Order matters: `mass_properties.py` produces
the 4.86 kg sled mass that `motor_model.py` hard-codes as `M_SLED`. Change the mass model
and you must update that constant, re-run the motor model, then update the paper.

## Known errors and open work

The paper once carried four numbers its own scripts did not reproduce — conjunction
minimum, peak current, far-field stray values, and brake fin temperature rise. All four
were found by rebuilding the analysis from scratch and were corrected in `paper.tex` on
2026-07-23; the conjunction claim was also reframed, because that minimum turns out to be
a near-resonant beat sample rather than a design property (a ±2.5 % velocity change moves
it by an order of magnitude). The defects stay documented as P1–P4 for the audit trail.

Open items now, in rough order of how much they move the design:

- **P5 / P8** — CAD sled mass contradicts the parametric assumption; exit velocity
  provisionally 17.88 m/s pending structural FEA.
- **P9** — closed envelope exceeds the ESPA Grande class limit by roughly 44 %; the host
  claim must be re-scoped or the machine repackaged.
- **P10** — enclosure, radiator, and packaged avionics are missing from the mass rollup.
- **P11** — the archived build in `paper/archive/` still carries the uncorrected P1–P4
  values; whether that is the version that was submitted is unconfirmed.
- **E1** — three-dimensional field closure; the winding is resolved in 2-D, so end
  effects of a few percent on Kt are uncomputed. The FEMM package (A1) is written but
  has not been run.
- **E2 / E4** — no FEA of anything, no hardware at any level.
- **E14** — disclosure has already happened; the patent position needs settling or
  closing out.

Full list with detail: [`OPEN_PROBLEMS.md`](https://github.com/aaaaaaaaaaaavm/emocd/blob/main/OPEN_PROBLEMS.md).

## How to read the verification status

Nothing in this project has been validated by hardware, FEA, or third-party review, and
no number has been hand-checked against a second method except the two cross-checks noted
above. `INVENTORY.md` indexes every calculation and where it now lives; `PROVENANCE.md`
states plainly what stands behind each claim. Anything added here should carry the same
distinction, and a computed number must never be presented as a measured one.

## Citing

Citation metadata is in
[`CITATION.cff`](https://github.com/aaaaaaaaaaaavm/emocd/blob/main/CITATION.cff). The
paper is *EMOCD: A Linear-Motor Electromagnetic Deployment System for Deterministic
CubeSat Orbit Seeding from Small Launch Vehicles*. Licence: MIT.

## Author

Adityavardhan Mishra — Department of Mechanical Engineering, Symbiosis Institute of
Technology, Symbiosis International (Deemed University), Pune. Project begun April 2021.
