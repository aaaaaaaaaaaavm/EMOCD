# A8: Pulse-power chain (ngspice / PySpice)

**Closes:** `OPEN_PROBLEMS.md` **E17**.

The supercapacitor bank, the SiC bridge, and the winding are currently modelled
analytically inside `motor_model.py` and `sizing.py`, lumped R, ideal switching, no
device dynamics. A circuit simulation is a genuinely different method and costs an
afternoon, not a lab. It is the cheapest independent check in this directory.

## Inputs (all committed)

- Bank: **6.0 F selected** (5.97 F required), **32 cells in series**, 3.0 V / 190 F per
  cell, `analysis/results/sizing.json` `capacitor`
- Rail 96 V, series resistance 12 mΩ, per `sizing.py`
- Winding and drive as used in `motor_model.py` `shot()`
- Shot profile: force command 1413 N, 127.7 ms pulse

## Acceptance band (declared 2026-07-27, before running)

Reference values from `analysis/results/motor_results.json` and `sizing.json` as committed
at `40e09f9`.

| Quantity | Reference | Band |
|---|---|---|
| Peak current | 391.7 A | ±10 % |
| Bank sag over the shot | 4.88 % | ±1.5 percentage points |
| Energy drawn from the bank | 2634 J | ±5 % |
| Copper loss per shot | 672 J | ±15 % |
| Pulse duration to release | 127.7 ms | ±10 % |
| Energy closure | 100.1 % accounted | 98-102 % |

The copper-loss band is loosest because the analytic model uses a single temperature and
the simulation will not.

## A8-R2: bands declared 2026-08-05, before re-running

**Third declaration, and the reason is P19 again.** A8's original bands were set at the 20.37 m/s
point. A8-R's were set at 16.537 m/s. The 2026-08-03 quadrature correction moved the operating
point a third time, to 16.388 m/s, and `validation/README.md` has been carrying A8 as
"superseded by the quadrature correction and not rerun" ever since.

**The deck is also stale.** `validation/spice/emocd_shot.cir` hardcodes `F=1413.448`, the
pre-quadrature commanded force; the current value is **1389.255 N**. Its `Pcu=5263` happens to
still be right. Both are updated from `motor_results.json` before this runs.

Rewriting the earlier bands to fit the new numbers would destroy the only thing a declared band
is worth, so they are left where they are and these are new.

| Quantity | Reference | Band | Why this width |
|---|---|---|---|
| Peak current | 338.816 A | ±10 % | unchanged from A8-R; the quantity has not become harder to predict |
| Bank sag over the shot | 5.296 % | ±1.5 percentage points | unchanged |
| Energy drawn from the bank | 2850.9 J | ±5 % | unchanged |
| Copper loss per shot | 834.7 J | ±15 % | loosest, because the analytic model uses a single temperature |
| Pulse duration to release | 158.6 ms | ±10 % | unchanged |
| Energy closure | 100 % accounted | 98–102 % | unchanged |

**What this tests.** ngspice integrates the same shot through an independent circuit
formulation — node voltages carrying mechanical state — rather than `motor_model.shot()`'s
Python loop. A disagreement is either a modelling fork or an integrator artefact, and both are
worth knowing. It is *not* an independent physical method: the constants come from
`motor_model.py`.

### A8-R2 result, 2026-08-05: **six of six bands PASS**

ngspice ran the updated deck. Bands were committed at `1e15b0a`, before the deck was touched.

| Quantity | Band reference | ngspice | Deviation | Verdict |
|---|---:|---:|---:|---|
| Peak current | 338.816 A ±10 % | **338.80 A** | 0.005 % | **PASS** |
| Bank sag | 5.296 % ±1.5 pp | **5.294 %** | 0.002 pp | **PASS** |
| Energy drawn | 2850.9 J ±5 % | **2849.7 J** | 0.04 % | **PASS** |
| Copper loss | 834.7 J ±15 % | **834.7 J** | 0.00 % | **PASS** |
| Pulse duration | 158.6 ms ±10 % | **158.63 ms** | 0.02 % | **PASS** |
| Energy closure | 98–102 % | **100.02 %** | — | **PASS** |

Exit velocity comes out at **16.391 m/s** against the model's 16.388, a 0.016 % agreement.

**What this is worth, stated honestly.** The agreement is very close because it should be: the
deck takes `F`, `Pcu`, `m`, `eta` and `R_esr` from `motor_model.py` rather than deriving them, so
this tests the **integration**, not the physics. Copper loss agrees to 0.00 % by construction —
the deck carries it as a constant. What is genuinely tested is that an independent circuit
formulation, with node voltages carrying mechanical state and a real ESR in the loop, reaches the
same exit velocity, peak current and bank sag as a Python loop. It does.

**A8 is no longer stale.** `validation/README.md` had carried it as superseded by the quadrature
correction and not rerun since 2026-08-03. It is now current at 16.388 m/s.

## A8-R: re-run at the current operating point, bands declared 2026-07-30 before running

The bands above were set against the 20.37 m/s point and the 4.86 kg parametric sled. P15 moved
the sled to a measured 9.445 kg, and P23 established that the recorded pass sits outside the band
the current model would produce. Re-running needs fresh bands, and rewriting the old ones to fit
the new number would destroy the only thing that makes a declared band worth anything.

**These are written down before the circuit deck is touched.** Reference values from
`analysis/results/motor_results.json` and `sizing.json` as committed at `3ddd56e`.

| Quantity | Reference | Band | Why this width |
|---|---|---|---|
| Peak current | 330.3 A | +/-10 % | Same as before; the quantity has not become harder to predict |
| Bank sag over the shot | 5.19 % | +/-1.5 percentage points | Unchanged, absolute rather than relative because the number is small |
| Energy drawn from the bank | 2796 J | +/-5 % | Unchanged |
| Copper loss per shot | 828 J | +/-15 % | Still the loosest: the analytic model uses one temperature and the simulation does not |
| Pulse duration to release | 157.3 ms | +/-10 % | The band that P23 is about. 141.6 to 173.0 ms |
| Energy closure | 100.0 % accounted | 98-102 % | Unchanged |

**What changes in the deck, and nothing else:** the sled mass 8.86 to 13.445 kg, and the two
measurement windows from 127.7 ms to 157.3 ms. Force, copper loss, bank and ESR are unchanged,
because none of them depends on the sled mass. If anything else needs changing to make the
numbers agree, that is a finding and gets recorded as one.

**Falsification:** any row outside its band. The interesting failure would be pulse duration,
because that is the row the old band failed, and passing it now is the whole point of re-running.

## A8-R result, run 2026-07-30

ngspice 44, deck `validation/spice/emocd_shot.cir`. Three parameters changed and nothing else:
sled mass 8.86 to 13.445 kg, and the two measurement windows to 157.3 ms.

| Quantity | Simulated | Reference | Delta | Band | Verdict |
|---|---|---|---|---|---|
| Peak current | 346.8 A | 330.3 A | +5.0 % | +/-10 % | pass |
| Pulse duration to release | 157.26 ms | 157.3 ms | -0.03 % | +/-10 % | **pass** |
| Energy drawn from the bank | 2880 J | 2796 J | +3.0 % | +/-5 % | pass |
| Bank sag over the shot | 5.35 % | 5.19 % | +0.2 pts | +/-1.5 pts | pass |
| Copper loss per shot | 827.7 J | 828 J | -0.04 % | +/-15 % | pass, but see below |
| Energy closure | 97.0 % | 100 % | -3.0 pts | 98-102 % | **FAIL** |

Five of six pass. The pulse-duration row, which is what P23 is about, now passes at 0.03 %.

**The copper-loss row is not an independent check and should not be read as one.** The deck
carries `Pcu` as a constant computed by `motor_model.py`, so the simulation returns `Pcu` times
the shot duration by construction. It confirms the integration window, nothing more. Left in the
table because removing a row after seeing the result is exactly the move these bands exist to
prevent.

### The closure failure, and what caused it

The simulated draw exceeds the analytic accounting by **86.6 J**, 3 % of the shot.

That gap is **bank ESR dissipation**, which the circuit models and the analytic ledger omits:

```
I^2 dt over the shot   7126.2 A^2 s      (ngspice, integrated)
x ESR                  0.012 ohm
= ESR loss                85.5 J          against an 86.6 J gap, agreeing to 98.7 %
```

With that term included the closure is **100.0 %** and the row passes.

This is the open half of **E17**, and `sizing.py` says so in a comment at the point where it
matters: `thermal_campaign()` carries a literal `Q_esr=160` J placeholder with the note that no
script models a bank ESR at all, and `energy_closure()` omits the term entirely.

A lumped energy ledger cannot see this term, because it has no state variable to attach it to; a
circuit solve can, because it integrates the current it is already carrying. That is the reason
A8 was specified. The placeholder it lands on was carrying **160 J against 85.5 J from the
solve**, nearly a factor of two high.

**85.5 J is a simulation result, not a measurement.** It is a second independent number against a
placeholder that previously had none, which is what E17 asked for, and it is still one model
checking another. Nothing in this repository has been measured. Logged as **P24**.

## What this can find that the analytic model cannot

- **Transient current overshoot** at commutation, which sets the real device rating rather
  than the steady peak. The paper's SiC derating discussion assumes the 392 A figure.
- **Bank sag under the actual current waveform** rather than an averaged draw, the 4.9 %
  number feeds the servo headroom argument behind the 0.027 m/s dispersion claim.
- **ESR heating distribution.** `sizing.py` carries a `Q_esr = 160 J` default that P2's
  Phase-1 review initially flagged as unsourced; a circuit model puts a second number
  against it.

## If a band is missed

Peak current and sag both propagate: current into the device rating and the paper's power
electronics section, sag into the closed-loop dispersion. Record first, open a P-item, and
do not adjust `sizing.py` before the cause is understood, switching model, ESR at
temperature, and winding inductance are the three suspects.

## Output

`validation/results/A8_pulse.json`, the six quantities above with their ratios to
reference, plus `simulator`, `version`, `switching_model`, `esr_assumption`,
`timestep`, `netlist_path`.
