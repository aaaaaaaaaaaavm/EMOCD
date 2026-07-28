# A7 — Separation and tip-off (Project Chrono)

**Relates to:** `OPEN_PROBLEMS.md` E7 (dispersion rests on assumed sensor noise) and the
tip-off claims in the paper, which are model outputs with no multibody model behind them.

Unlike A1 and A4, this one has a **measured benchmark to compare against** — spring
deployers have flown thousands of times and their tip-off performance is published.

## Inputs

- Geometry and masses: `cad/step/gen3/EMOCD_Sled_Gen3.step`,
  `cad/step/gen3/EMOCD_Payload_3U_Gen3.step`,
  `cad/parameters.json` (payload CDS corner rails, sled cradle, release at x = 1500 mm)
- Release conditions: exit velocity 20.37 m/s at 16.3 g (or the A4 outcome, if A4 has run)
- Contact: rail-on-cradle friction, coefficient stated as an assumption

## Acceptance band (declared 2026-07-27, before running)

| Quantity | Criterion | Basis |
|---|---|---|
| Tip-off rate, any axis | **≤ 5 °/s** | NRCSD-E interface document quotes < 5 °/s/axis as its target — the number EMOCD has to beat, or at least match, to claim a benign release |
| Re-contact after release | none, through 2 m of separation | fire-then-arrest ConOps assumes clean departure |
| Lateral velocity component | ≤ 2 % of axial | otherwise the ±0.10 km apogee placement claim is optimistic |

Beating a flown spring deployer on tip-off is a *claim EMOCD makes implicitly* by
positioning itself as a controlled alternative. Putting a flown number in the band makes
that claim falsifiable rather than rhetorical.

## If tip-off exceeds the band

That is not necessarily fatal — but it changes the pitch. A deployer that delivers precise
Δv with worse attitude disturbance than a spring is a different product from one that
improves both, and the paper currently implies the latter. Record it, open an E-item, and
adjust the framing before the next submission.

## Output

`validation/results/A7_separation.json` — tip-off rates per axis, lateral/axial velocity
ratio, minimum separation distance over the departure window, plus `tool`, `version`,
`friction_assumption`, `contact_model`, `timestep`.
