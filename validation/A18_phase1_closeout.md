# A18: the five remaining Phase I analyses

**Closes:** **E20** (brake force-time), **E19** (magnet eddy heating), **E26** (fin campaign
transient), **E10** (launch restraint, analysis half), **E22** (conductive-structure standoff).

> ## BANDS DECLARED 2026-08-06. NOT YET RUN.
>
> Committed before `analysis/phase1_closeout.py` existed. `git log` is the evidence.

Five items grouped into one sheet because they share inputs and none is large enough to earn its
own. Each keeps its own bands and its own verdict.

## Assumed inputs, swept rather than picked

Every one of these needs a number the repository does not have. Following A14 band 5 and A17's
Q sweep: **swept, and where a sweep cannot bound the answer the row is VOID, not guessed.**

| Quantity | Sweep | Why it is not in the repo |
|---|---|---|
| Eddy-brake pole field | 0.3 – 0.7 T | `cad/parameters.json` gives pole geometry, never a field |
| Fin emissivity | 0.05 (bare Cu) – 0.9 (coated) | no surface finish specified |
| Mount contact conductance | 100 – 5000 W/m²K | no joint design |
| Structural Q under random vibration | 10 – 30 | **P36** already records that no Q exists anywhere |
| NdFeB resistivity | 1.4 µΩ·m | published range, narrow enough not to sweep |

## Acceptance bands

### E20 — brake force-time profile

Velocity-proportional eddy drag `F = k·v`, `k = σ·t·B²·A_pole`, integrated across the arrest zone
from the post-regeneration entry speed of 14.068 m/s (`motor_results.regen.v_end`).

| # | Question | Band |
|---|---|---|
| 1 | Peak deceleration at brake entry | **≤ 200 g**, the cap `sizing.py` asserts and sizes the magnet bond to |
| 2 | Stopping distance | **≤ 210 mm**, the brake envelope x = 1530–1740 mm |
| 3 | Energy absorbed vs `regen.KE_to_brake` | **within 2 %** of 934.7 J — self-consistency, not a new result |
| 4 | Arrest duration | **report**; E20 estimates 8–20 ms with nothing bounding the peak |

### E19 — eddy heating inside the magnet blocks

Slab eddy loss `P/V = σ·d²·(dB/dt)²/12` under the armature-reaction field the blocks see at the
commutation frequency, over the 158.6 ms pulse.

| # | Question | Band |
|---|---|---|
| 5 | Magnet temperature rise per shot | **< 1 K** — above this it competes with the ±0.11 %/K remanence drift `sizing.magnet_temperature()` already carries |
| 6 | Whether segmentation is needed | **report** the trade `docs/CROSS_INDUSTRY.md` names |

### E26 — brake-fin transient across a campaign

Lumped fin capacity with radiation and conduction, twelve shots at the **1200 s ADR-020 cadence**,
from the 7.1 K per-shot adiabatic step.

| # | Question | Band |
|---|---|---|
| 7 | Peak fin temperature over twelve shots, worst case in the sweep | **< 150 °C** |
| 8 | Whether the transient decays between shots at 1200 s | **report per (ε, h) pair**; the claim E26 removed for having no model behind it |

### E10 — launch restraint, analysis half only

Miles' equation on the GEVS protoflight spectrum (14.1 g_rms, 20–2000 Hz) against the retention
gate's stated 5.9 kN through two D6 A-286 pins at MoS 1.2 (`sizing.py:166`).

| # | Question | Band |
|---|---|---|
| 9 | 3σ random-vibration load on the retention pins | **≤ 5.9 kN**, the load the pins were sized for |
| 10 | Margin of safety at the swept Q | **≥ 0** |

**T-1 closes the test half. This closes only the analysis half**, and band 9 is expected to be
the hard one — the pins were sized against a quasi-static load, not a random-vibration one.

### E22 — conductive-structure standoff

E22 is already reframed as a design rule. Produce the drag-versus-standoff curve so the rule has
a number, then check the CAD.

| # | Question | Band |
|---|---|---|
| 11 | Standoff at which parasitic eddy drag falls below **1 % of thrust** | **report** — this is the rule |
| 12 | Whether `cad/parameters.json`'s track geometry clears it | **pass/fail against the rule** |

## If bands 1, 7 or 9 fail

Band 1 failing means the brake as drawn exceeds its own deceleration cap and the magnet bond is
undersized. Band 7 failing means the fin needs active cooling or a larger radiator. **Band 9
failing is the most likely and the most consequential**: it would mean the retention gates were
sized against the wrong load case, and T-1 — already flagged in `docs/QUALIFICATION_PLAN.md` as
*"the single most likely qualification failure"* — becomes a predicted failure rather than a risk.
