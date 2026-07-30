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

## A8-R: re-run at the current operating point, bands declared 2026-07-30 before running

The bands above were set against the 20.37 m/s point and the 4.86 kg parametric sled. P15 moved
the sled to a measured 9.445 kg, and P24 established that the recorded pass sits outside the band
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
| Pulse duration to release | 157.3 ms | +/-10 % | The band that P24 is about. 141.6 to 173.0 ms |
| Energy closure | 100.0 % accounted | 98-102 % | Unchanged |

**What changes in the deck, and nothing else:** the sled mass 8.86 to 13.445 kg, and the two
measurement windows from 127.7 ms to 157.3 ms. Force, copper loss, bank and ESR are unchanged,
because none of them depends on the sled mass. If anything else needs changing to make the
numbers agree, that is a finding and gets recorded as one.

**Falsification:** any row outside its band. The interesting failure would be pulse duration,
because that is the row the old band failed, and passing it now is the whole point of re-running.

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
