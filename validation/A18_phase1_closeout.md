# A18: the five remaining Phase I analyses

**Closes:** **E20** (brake force-time), **E19** (magnet eddy heating), **E26** (fin campaign
transient), **E10** (launch restraint, analysis half), **E22** (conductive-structure standoff).

> ## RUN 2026-08-06. Verdict **E19, E26, E22 PASS · E20 PASSES ONLY IN A NARROW WINDOW · E10 FAILS**
>
> Bands committed at **`4e97fce`**, before `analysis/phase1_closeout.py` existed. None widened.

## Result, 2026-08-06

### E20 — the brake works, in a 0.4–0.5 T window and nowhere else

| Pole field | k (N·s/m) | Peak force | Peak decel | Stop distance | 99 % arrest |
|---:|---:|---:|---:|---:|---:|
| 0.3 T | 386 | 5.4 kN | 58.7 g | **344 mm** — overruns | 112.6 ms |
| **0.4 T** | 687 | 9.7 kN | 104.3 g | 193.5 mm | 63.4 ms |
| **0.5 T** | 1073 | 15.1 kN | 162.9 g | 123.9 mm | 40.5 ms |
| 0.6 T | 1545 | 21.7 kN | **234.6 g** — over cap | 86.0 mm | 28.2 ms |
| 0.7 T | 2103 | 29.6 kN | **319.4 g** — over cap | 63.2 mm | 20.7 ms |

Bands 1 and 2 hold **only for 0.4–0.5 T**. Below that the sled runs out of the 210 mm arrest
envelope; above it, deceleration exceeds the 200 g cap `sizing.py` sizes the magnet bond to.
Band 3 self-consistency: energy absorbed matches `regen.KE_to_brake` to **0.005 %**.

**E20 asked for a force-time profile and the answer is that the pole field is a specification,
not a free parameter.** Nothing in `cad/parameters.json` states it. E20's own first-order guess
of ~6 kN average over 8–20 ms lands at the low-field end; the real peak at 0.5 T is **15.1 kN**,
2.5× that, and 11× the 1389 N acceleration force.

### E19 — benign, by a factor of 400

Armature-reaction field at the magnet face 36.1 mT at 341 Hz gives dB/dt = 77.4 T/s, eddy power
**25.2 W** in 3.67 kg of NdFeB over a 158.6 ms pulse: **0.0025 K per shot, 0.030 K per campaign**
against a 1 K band. **Segmentation is not needed** — the trade `docs/CROSS_INDUSTRY.md` names is
real for steady-state rotating machines and irrelevant to a 159 ms pulse at this frequency.

### E26 — at 1200 s the fin never accumulates

**All sixteen (ε, h) pairs fully decay between shots**, so peak temperature is always one shot's
rise: **34.1 °C** against a 150 °C band, identical in the best and worst cases. The sweep did not
need to discriminate because even bare copper at the lowest contact conductance clears 934.7 J in
1200 s. **This is a result about the cadence, not the fin**: ADR-020 is what closes E26, and at
the paper's former 10–20 s it would not have.

### E10 — FAIL. The retention gates were sized against the wrong load case

| Q | g_rms | 3σ | Load | vs the 5.9 kN sized for | MoS |
|---:|---:|---:|---:|---:|---:|
| 10 | 16.6 | 49.7 | **11.7 kN** | 1.98× | 0.56 |
| 15 | 20.3 | 60.8 | **14.3 kN** | 2.43× | 0.27 |
| 20 | 23.4 | 70.2 | **16.5 kN** | 2.80× | 0.10 |
| 30 | 28.7 | 86.0 | **20.2 kN** | 3.43× | **−0.10** |

**Band 9 fails at every Q.** Miles' equation on the GEVS protoflight spectrum at the 109 Hz track
mode gives 11.7–20.2 kN through the retention pins, against the **5.9 kN they were sized for**.
Band 10 fails at Q = 30, where the two D6 A-286 pins are past their 18.2 kN shear capacity.

**The pins are not necessarily undersized; the load case was.** 5.9 kN is a quasi-static figure.
Random vibration through a lightly-damped 109 Hz mode is a different problem, and the margin the
design claims — MoS 1.2 — becomes **0.10 at Q = 20 and negative at Q = 30**.

`docs/QUALIFICATION_PLAN.md` already calls T-1 *"the single most likely qualification failure"*.
**It is now a predicted failure rather than a ranked risk.** Logged as **P37**.

### E22 — the rule is 20 mm

| Standoff | Field | Drag | % of thrust |
|---:|---:|---:|---:|
| 5 mm | 43.7 mT | 200.9 N | **14.5 %** |
| 10 mm | 22.7 mT | 54.3 N | 3.9 % |
| **20 mm** | 6.1 mT | 4.0 N | **0.285 %** |
| 30 mm | 1.7 mT | 0.3 N | 0.021 % |

**Rule: no conductive structure within 20 mm of the array back face**, at which parasitic eddy
drag is under 1 % of thrust. At 5 mm it would cost 14.5 % of thrust and heat the structure.

**Band 12 is reported, not passed.** The track longerons reach z = 20 mm against an array back
face at z = 14 mm — 6 mm axially — but they sit at y = 67–90 mm, outside the array's ±45 mm
half-width, so they are laterally clear rather than axially. **Establishing that properly needs a
3-D minimum-distance check against every conductive part**, which this analysis does not perform.
The rule now exists; applying it to the whole assembly is a CAD task.

---

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
