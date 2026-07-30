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

## Result

*To be written after the run. The bands above are committed first.*
