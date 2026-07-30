# A10: what the shot does at a realistic bank ESR

**Closes:** nothing. **Opens:** whether the pulse-power chain closes at all.

`motor_model.py` carries `R_ESR = 0.012` for the supercapacitor bank. P24 recorded that the
figure has no source. Chasing that source turned up something worse than a missing citation.

## The argument, before any simulation

For electric double-layer capacitors the product of ESR and capacitance is roughly constant
within a cell technology, because both are set by the same electrode area and separator. Two
Eaton cells thirty times apart in capacitance bracket it:

| Cell | C | ESR | ESR x C |
|---|---|---|---|
| Eaton TV1860-3R0107-R, 3.0 V | 100 F | 11 mohm | 1.10 s |
| Eaton XL60-3R0308T-R, 3.0 V | 3000 F | 0.23 mohm | 0.69 s |

The bank is 32 cells of 190 F in series: 5.94 F, 96 V. Series stacking preserves the product,
because R scales with N and C scales with 1/N. So the bank should land at

```
ESR = (ESR x C) / C = 0.69/5.94 to 1.10/5.94 = 116 to 185 mohm
```

**The modelled 12 mohm implies ESR x C = 0.071 s, an order of magnitude better than either
commercial cell.** Both figures above are quoted at 3.0 V from distributor listings of the
manufacturer data. Neither has been confirmed against the manufacturer PDF, because
eaton.com is unreachable from this environment; that limitation is recorded rather than
worked around.

**The AC/DC distinction cuts the wrong way.** Vinatech define DC ESR from the voltage drop
10 ms into discharge and AC ESR from a 1 kHz impedance sweep; for EDLCs the DC figure is the
larger. A 157 ms pulse is a DC event. If any figure above is an AC one, the real number is
higher, not lower.

## The ceiling this implies, derived rather than simulated

A source of EMF `V` behind series resistance `R` cannot deliver more than `V^2/4R` into any
load, at any impedance. At the rated point the shot needs, at peak velocity:

```
P = F*v/eta_conv + P_cu + P_aux = 1413.4*16.537/0.95 + 827.9/0.1573 + 200 = 30.0 kW
```

Setting `V^2/4R = P` with V = 96 V gives **R_max = 76.8 mohm**, and that is the theoretical
limit at matched load, where half the energy burns in the ESR. Anything approaching it is
useless in practice.

**So the prediction is not that the shot is inefficient. It is that the shot does not exist.**

## Bands, declared 2026-07-30 before running

`motor_model.shot()` solves `R I^2 - Vc I + P = 0` for the terminal current. That quadratic
has no real root when `Vc^2 < 4 R P`, which is the same statement as the ceiling above. The
sweep runs at 12, 30, 60, 90, 115, 150 and 183 mohm.

| # | Quantity | Prediction | Accept if |
|---|---|---|---|
| 1 | Shot completes at 12 mohm | yes | completes, v_exit within 0.1 % of 16.537 |
| 2 | Shot completes at 115 and 183 mohm | **no** | integration fails, or terminal falls below the 40 V floor |
| 3 | Highest ESR at which the shot still completes | **60 to 77 mohm** | within that range |
| 4 | ESR loss at 115 mohm, if it ran | 820 J | within +/-15 % of `I^2 dt * R` |
| 5 | Exit velocity at 12 mohm vs 60 mohm | unchanged | commanded force is constant, so velocity must not move until the bank fails to source it |
| 6 | Bank capable of the rated shot at a commercial ESR | **no** | any result showing otherwise falsifies this whole entry |

**Falsification:** row 3 landing above 100 mohm would mean the ceiling argument is wrong and
the design closes on ordinary cells. Row 5 moving would mean the model couples velocity to
bank resistance somewhere it should not, which would be a defect in the model rather than in
the design.

**What this analysis cannot settle.** Whether a different cell technology, a different bank
topology, or a different rated point rescues the design. That is a sizing decision and it is
deliberately not taken here. This run establishes only whether the bank as specified can
source the shot as specified.

## Result, run 2026-07-30

**The first run was invalid, and the reason is worth more than the run.**

`shot()` carried a guard: when the quadratic had no real root it fell back to `I = P/Vb`,
the current the load would draw with no ESR at all. So the sweep completed at every
resistance and reported plausible numbers. The tell was that **peak current fell from 630 A
to 331 A as resistance rose**, which cannot happen at fixed demanded power.

That guard was written on 2026-07-30 in the same commit that added the ESR term. It converted
"this bank cannot source the shot" into a finished run with a working machine in it. It now
raises `BankLimitError` naming the power demanded, the ceiling, and where in the stroke it was
hit. **A10 was built to test the bank and the first thing it caught was the instrument.**

### The sweep, with the failure exposed

| ESR mohm | v_exit | I_peak A | E drawn J | Q_esr J | min terminal V | |
|---|---|---|---|---|---|---|
| 12 | 16.537 | 346.8 | 2881 | 86 | 86.7 | as modelled |
| 30 | 16.537 | 379.7 | 3038 | 242 | 79.2 | |
| 50 | 16.537 | 441.9 | 3282 | 486 | 68.0 | |
| 60 | 16.537 | 505.8 | 3465 | 669 | 59.4 | |
| **65** | 16.537 | 579.7 | 3597 | 802 | 51.9 | **last value that completes** |
| 70 | | | | | | **bank limit** |
| 115 | | | | | | bank limit, realistic low |
| 183 | | | | | | bank limit, realistic high |

### Against the declared bands

| # | Prediction | Result | |
|---|---|---|---|
| 1 | completes at 12 mohm, v_exit within 0.1 % | 16.537 m/s | **pass** |
| 2 | does not complete at 115 and 183 mohm | raises at both | **pass** |
| 3 | ceiling between 60 and 77 mohm | **65 mohm** | **pass** |
| 4 | ESR loss at 115 mohm within 15 % of I^2dt*R | unmeasurable: the shot does not run | **void** |
| 5 | v_exit unchanged until the bank fails | unchanged to three decimals throughout | **pass** |
| 6 | bank not capable at a commercial ESR | not capable | **pass** |

Five of six. Row 4 is recorded void rather than passed: it assumed a number that only exists
if the shot runs, and it does not. Writing bands in advance is what makes that visible instead
of quietly reinterpreting the row.

The measured 65 mohm sits below the 76.8 mohm derived from `V^2/4R`, and the reason is that
the derivation used 96 V while the bank has already sagged to about 90 V by the time peak
power is demanded. Recomputing the ceiling at the sagged voltage gives 28.9 kW against 30.0 kW
required, which is the failure the integrator reports.

### What this establishes

**A single series string of 190 F cells cannot fire this shot.** Its ESR is 116 to 185 mohm
against a hard ceiling of 65 mohm, and the ceiling is a limit on deliverable power, not an
efficiency target. Nothing about the winding, the magnets or the control loop is implicated.

**What it does not establish** is what to build instead. That is a sizing decision and it is
not taken here. The options are costed in `docs/PHASE_II.md` PII-7.
