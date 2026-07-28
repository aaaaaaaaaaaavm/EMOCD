# Validation report — 2026-07-28

Every headline claim in this repository, and what independently checking it produced.

Four things were actually run: the analysis scripts were re-executed from a clean copy,
GMAT R2022a propagated the orbits, ngspice simulated the pulse chain, and the Gen3 sled
geometry was measured against material densities. Three planned analyses were **not** run
and are listed as such — nothing here is inferred from an analysis that did not happen.

**Two findings change numbers the project publishes.** Both are at the bottom of this file
and in `OPEN_PROBLEMS.md`.

---

## 1. Does the repository reproduce itself?

**Validated.** All five scripts in `analysis/` were copied to a clean directory, run with
an empty `results/`, and their output compared field by field against the committed JSON.

| | |
|---|---|
| Values compared | **173** |
| Identical | **173** |
| Differing | **0** |

Every number in `analysis/results/*.json` — and therefore every headline figure — is
regenerable from the committed scripts today. This is the claim `D12` makes, and it holds.

---

## 2. Astrodynamics — GMAT R2022a (A5)

GMAT was installed and run headless: MSISE90 atmosphere, 20×20 gravity, Luna and Sun as
point masses, SRP on, RK89. Independently implemented force models, not a second pass of
the same code.

### The ×1.80 lifetime multiplier — **holds**

| Solar activity | GMAT baseline | GMAT boosted | Multiplier | vs ×1.80 | Band ±5 % |
|---|---|---|---|---|---|
| High (F10.7 250) | 144.5 d | 250.0 d | **1.7302** | −3.88 % | pass |
| Mean (F10.7 150) | — | — | **1.7750** | −1.39 % | pass |
| Low (F10.7 70) | still propagating | | | | |

**Invariance across activity: 2.55 % spread, inside the ≤5 % band.** The claim that the
multiplier is invariant — the thing the paper actually defends — survives an independent
propagator.

### Absolute lifetimes — **not confirmed, as expected**

GMAT decays faster than `astro.py` at high and mean activity: 144.5 days against 190 at high
activity. The bounded 30-day window measured the same thing independently — fitted rates of
−0.1618 km/day (GMAT) against −0.1216 (`astro.py`), a factor of **1.33**. The two agree with
each other: 190 ÷ 1.33 ≈ 143 days.

E6 said absolute lifetimes carry severalfold uncertainty and that only the ratio is
defensible. That is now demonstrated rather than asserted.

**Early indication from the unfinished low-activity run: GMAT is at 4.1 years and still at
401 km, where `astro.py` predicts 2.61 years total.** At low activity GMAT appears to decay
*slower*, the opposite direction to the other two levels. If that holds, the invariance
spread will widen. The run is unfinished and this is not yet a result.

Detail: [`validation/results/A5_astro.json`](validation/results/A5_astro.json).

---

## 3. Pulse-power chain — ngspice (A8)

The mechanical ODE was rebuilt in analogue-computer form so SPICE integrates it with a
different scheme (trapezoidal) than `motor_model.py` (forward Euler, dt = 1e-4), while the
electrical side is a real circuit: 6 F bank, 96 V, series ESR, load drawing P/V at the
terminal.

| Quantity | `motor_model.py` | ngspice | Deviation | Band | |
|---|---|---|---|---|---|
| Exit velocity | 20.372 m/s | 20.366 | −0.03 % | ±10 % | pass |
| Pulse duration | 127.7 ms | 127.66 | −0.03 % | ±10 % | pass |
| Peak current | 391.7 A | **415.2 A** | +5.98 % | ±10 % | pass |
| Bank sag | 4.88 % | 5.06 % | +0.18 pts | ±1.5 pts | pass |
| Energy drawn | 2634 J | 2729 J | +3.59 % | ±5 % | pass |

Two different integrators landing within 0.03 % on exit velocity is a real check of the
shot model's arithmetic. All five declared bands met — **and two findings fell out anyway.**

Detail: [`validation/results/A8_pulse.json`](validation/results/A8_pulse.json), netlist at
[`validation/spice/emocd_shot.cir`](validation/spice/emocd_shot.cir).

---

## 4. Sled mass — measured from the Gen3 CAD (A4, partial)

Exact solid volumes from the OpenCASCADE kernel, multiplied by material densities. The
magnet density (7500 kg/m³) is the repo's own, from `sizing.py`.

| Body | n | cm³ each | Material | kg |
|---|---|---|---|---|
| Chassis plate 488×140×6 | 2 | 409.9 | Ti-6Al-4V | 3.632 |
| Halbach array 340×90×8 | 2 | 244.8 | NdFeB | 3.672 |
| Backstop 8×140×100 | 1 | 112.0 | Ti-6Al-4V | 0.496 |
| Chassis web 488×6×28 | 2 | 82.0 | Ti-6Al-4V | 0.727 |
| Brake fin 120×80×4 | 1 | 38.4 | Copper | 0.344 |
| Roller arm 40×16×20 | 4 | 12.8 | Ti-6Al-4V | 0.227 |
| Roller Ø30×16 | 4 | 11.3 | 440C steel | 0.348 |
| **Total as drawn** | | | | **9.445** |

**The method reproduces the existing claim exactly.** Fed 7.50 kg, the shot model returns
17.87 m/s — the 17.88 m/s that P8 states. Fed the measured 9.445 kg, it returns **16.53 m/s
at 10.7 g and 19.6 % efficiency**.

What this is not: it is not the structural FEA A4 specifies. It measures the sled *as
drawn*, with solid plates and no lightening pockets. A real design would pocket them. The
stiffness question — the lightest chassis that holds the airgap to ±0.05 mm — remains open.

---

## 5. Not run, and why

| Analysis | Status |
|---|---|
| **A1** airgap field, magnetostatic FEA | **Not run.** FEMM is Windows-only and no open-source magnetostatic solver was set up here. The field remains checked only analytic-vs-analytic (wave model vs magpylib), which E2 already says is not confirmation by a different physical method. **K<sub>t</sub> = 11.22 N per kA/m is therefore still single-method.** |
| **A4** sled structural | **Partially run** — mass measured (above), stiffness and stress not. CalculiX is installed; the analysis was not performed. |
| **A6** conjunction P<sub>c</sub> | **Not run.** Needs a covariance that does not exist for an unflown satellite (E18), and the CARA tools are MATLAB. |
| **A7** separation and tip-off | **Not run.** Project Chrono is not installable here. Tip-off remains a model output with no multibody model behind it. |
| Thermal, contamination, EMC, host stage | Unchanged — E5, E11, E12 stand. |
| Anything at all in hardware | **Nothing has been built, fired, or measured.** E4 stands, and no amount of this changes TRL 2–3. |

---

## Findings

### F1 — The Gen3 sled as drawn is 9.45 kg, above both existing estimates — **HIGH**

`mass_properties.py` assumes 4.86 kg. P5 quotes the CAD at ~7.50 kg. Measuring the Gen3
solids gives **9.445 kg**, which drives exit velocity to **16.53 m/s** — below the 17.88 m/s
that P8 already flags as provisional.

A4's pre-declared decision rule says a mass at or above 6.80 kg means "17.88 m/s becomes the
headline and the paper changes materially". The measurement lands well beyond that
threshold. It does not settle the design question — pocketed plates would weigh less, and
the stiffness constraint is unevaluated — but **whichever way the FEA goes, 20.37 m/s is not
supported by the geometry that currently exists.** Recorded as P15.

### F2 — Quoted bank sag is state-of-charge, not terminal voltage — **MEDIUM**

`motor_model.py` computes sag as the capacitor's charge depletion (4.88 %) and models no
ESR. With the 12 mΩ ESR the terminal voltage droops to 86.16 V at end of stroke: a **10.25 %
total sag**, more than double the published figure. The servo-headroom argument behind the
0.027 m/s dispersion claim is stated against the smaller number. Recorded under E17.

Related: ∫I² dt over the shot is 8008 A²s. At 12 mΩ that is 96 J of ESR loss, against the
`Q_esr = 160 J` default in `sizing.py`. The two are consistent only at ~20 mΩ. E17 noted that
160 J had no second number against it; this is the second number.

*(The 12 mΩ itself appears only in `docs/EMOCD_Computation_Results_C1-C10.md`, which is
superseded. No current script defines a bank ESR at all — which is part of the problem.)*

---

## What this changes

The astrodynamics claim is in better shape than it was this morning: the ×1.80 multiplier
and its invariance now have an independent propagator behind them, and the absolutes are
demonstrably the weak part, exactly as E6 predicted.

The performance claim is in worse shape. The headline 20.37 m/s rests on a 4.86 kg sled that
the drawn geometry does not support, and the electrical margin is quoted against a voltage
the drive never sees.

Neither of those is a reason to change a script today. Both are reasons to run A4 properly
and to put an ESR in the shot model — and, per the standing rule, to fix the paper only
after the analysis lands, not before.
