# EMOCD — Electromagnetic Orbital CubeSat Deployer

A magazine-fed electromagnetic deployer that ejects unmodified CubeSats from a host
stage at programmable velocity, aimed at the unserved regime between spring deployers
(~2 m/s) and propulsive orbital transfer vehicles (hundreds of m/s).

**Status: design study, TRL 2–3. No hardware, no CAD, no FEA.**
**Read `PROVENANCE.md` before citing anything here.**

## The idea

CubeSats flown as rideshare secondaries inherit the primary customer's orbit. The
spring that ejects them adds 1–2 m/s — enough to drift clear, not enough to change an
orbit. A satellite with no propulsion of its own is stuck there for life.

EMOCD replaces the spring with an ironless double-sided Halbach linear synchronous
motor driving a reusable magnetic sled along a 1.5 m track. Twelve 3U CubeSats feed
from two transverse cassettes and are fired one at a time. The satellite is never
modified — the magnets ride the sled, not the payload.

## Headline results (all model outputs, not measurements)

| Quantity | Value | Source |
|---|---|---|
| Thrust constant | 11.22 N per kA/m, ±1.26 % ripple | `analysis/motor_model.py` |
| Exit velocity, 3U | 20.37 m/s at 16.3 g | `analysis/motor_model.py` |
| Electrical→payload efficiency | 32 % (2.63 kJ drawn, 830 J delivered) | `analysis/motor_model.py` |
| Closed-loop dispersion | 0.027 m/s (3σ) → ±0.10 km apogee | `analysis/motor_model.py` |
| Orbital lifetime multiplier | ×1.80, invariant across BC and solar activity | `analysis/astro.py` |
| Constellation seeding | 30° in 1.4–6.9 days vs 25 days by differential drag | `analysis/astro.py` |
| Dry / loaded mass | 72.3 kg / 120.3 kg | `analysis/mass_properties.py` |
| Recoil per shot | 81.5 N·s | `analysis/astro.py` |
| Track first mode | 109 Hz fixed-fixed (target >70) | `analysis/sizing.py` |
| Energy closure | 100.1 % accounted | `analysis/sizing.py` |

Two results have independent cross-checks: the Halbach field model (analytic vs
magpylib, agreeing to three digits) and orbital decay (orbit-averaged vs Cowell RK4,
99.4 %). Everything else is single-sourced.

## Reproducing

```bash
pip install -r requirements.txt
cd analysis
python3 verify_field.py && python3 mass_properties.py && python3 motor_model.py && python3 sizing.py && python3 astro.py
```

Results land in `analysis/results/*.json`.

## Repository layout

- `analysis/` — current scripts; these reproduce the numbers above
- `legacy/` — superseded scripts, kept for history, **do not cite**
- `paper/` — IEEE conference paper (LaTeX source, figures, PDF)
- `docs/` — computation notes, FEMM run sheet
- `CLAUDE.md` — context for AI-assisted development sessions
- `INVENTORY.md` — complete indexed catalogue of every calculation, decision and artifact
- `docs/DECISION_LOG.md` — why each design change happened, including two self-corrections
- `PROVENANCE.md` — what came from where, and what was never verified
- `OPEN_PROBLEMS.md` — known errors in the paper, and unsolved engineering

## Known issues

The published paper previously contained four numbers its own scripts did not reproduce
(conjunction minimum, peak current, far-field stray values, brake fin temperature rise),
all found by reconstructing the analysis from scratch. **All four were corrected in
`paper/paper.tex` on 2026-07-23 to match the scripts**, and the conjunction claim was
additionally reframed because that minimum is not a robust quantity. Full record with
cause, before/after, and references is in `CHANGELOG.md`; the original defects remain
documented in `OPEN_PROBLEMS.md` P1–P4 for the audit trail.

## Author

Adityavardhan Mishra — Department of Mechanical Engineering, Symbiosis Institute of
Technology, Symbiosis International (Deemed University), Pune. Project begun April 2021.
