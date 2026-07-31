# A11: how much of the sled's energy the motor can take back

**Closes:** nothing. **Opens:** whether the 2025 arrest decision was read wider than it argued.

The sled leaves the release point with **1291 J**, which is **44.8 % of the 2881 J shot**, and
every joule of it is currently dissipated in the eddy-current brake. That is the single largest
loss in the machine, larger than copper (828 J) and larger than the payload itself (547 J).

## What the record actually decided, and what was read into it

`cad/CHANGELOG_CAD.md` R5 rejected regenerative arrest in 2025 on a sound argument: braking
force is bounded by the same thrust constant that bounds acceleration, so the motor cannot
*stop* the sled in the track available, and something else has to. That is correct and A11 does
not touch it.

What followed it is not the same statement. `DECISION_LOG.md`, `RESULTS.md`, `SUMMARY.md`,
`README.md` and `motor_model.py`'s own docstring all now carry a flat "no regeneration credit",
and the docstring goes further: the sled's kinetic energy "is dissipated in the arrest brake by
design and is **NOT** recovered". **Cannot stop the sled** and **cannot recover any of its
energy** are different claims, and only the first one was ever argued.

The reason nobody caught it is worth recording: the 2021 draft credited **55 %** of sled kinetic
energy as regeneration, that was a double-count, and correcting it dropped the headline
efficiency from 40 % to 32 %. After an error that size in that direction, the safe position was
to credit nothing. Safe is not the same as right, and this run asks the question the retraction
skipped.

---

## The argument, before any simulation

Braking regeneratively over a distance `s` at constant force `F`, starting at `v0` with sled
mass `m`:

```
mechanical work extracted   W   = F*s                       (while the sled is still moving)
time under braking          t   = m*(v0 - v1)/F,   v1 = sqrt(v0^2 - 2*F*s/m)
copper burned doing it      Qcu = k * F^2 * t
energy returned to the bank Erec = (W - Qcu)*CONV_EFF - P_AUX*t
```

`k` follows from the same two lines `shot()` uses. Sheet current for a commanded force is
`K = F/(0.9*Kt)`, current density is `J = 0.9*K/(WIND_THICK*FILL)`, so `J = F/(Kt*t_w*f)` and

```
k = RHO_CU * vol_cu / (Kt * WIND_THICK * FILL)^2
```

**`vol_cu` is the copper of the energised section, and that is the one modelling choice in this
run that changes the answer.** The regenerative section is *added stator downstream of the
release point*; it is not the acceleration winding, which the sled has already left. So its
copper volume is `s * DEPTH * WIND_THICK * FILL`, giving `k = 4.86e-4 W/N²` at `s = 0.240 m`,
where the accelerating winding's own 1.30 m gives `2.63e-3`. The pessimistic reading, that
whichever converter drives the regen section energises the full 1.30 m of installed winding, is
carried as a declared sensitivity below rather than argued away.

### Two constraints, and they are what make the answer small

1. **`K <= K_RATED`.** The winding has one sheet-current rating and it does not care about the
   sign of the force. So `F <= 0.9*Kt*K_RATED = 1413.7 N`, the same force that accelerated the
   sled. This is the 2025 argument, stated as an inequality.
2. **`s = 0.240 m`.** The closed envelope is 1839 mm and release is at 1500 mm, leaving 339 mm
   of arrest section. Allowing roughly 100 mm for the eddy fin and the ring-spring stack leaves
   about 240 mm for winding **without growing P9's 44 % envelope overrun**.

Constraint 2 is a packaging assumption, not a layout anybody has drawn, and it is stated as one.
The distance sweep below exists so a reader can see exactly how much rides on it.

### What that gives

At the rating, over 240 mm: `W = 339 J`, `t = 15.6 ms`, `Qcu = 15 J`, and about **305 J returns
to the bank, 23.6 % of the sled's energy**. The sled still arrives at the brake with 952 J.

**Copper is not the limit here and that is the surprise.** The braking pulse is 15.6 ms against
the shot's 157 ms, and it energises 240 mm of stator against 1300 mm, so the loss is 15 J
against the shot's 828. Within the rating, recovery therefore *rises monotonically with force*:
there is no interior optimum to find, the answer is "brake as hard as the winding allows". The
copper penalty that would produce an optimum only appears if the rating is lifted, and that is
what row 7 tests.

---

## Bands, declared 2026-07-31 before running

The sweep is over braking force multiplier (0.25 to 3.81 x rated, the last being the force that
would stop the sled inside 240 mm) and over regen section length (0.10 to 1.00 m at the rating).

| # | Quantity | Prediction | Accept if |
|---|---|---|---|
| 1 | Energy returned to the bank, rated force, 240 mm | **305 J** | 280 to 330 J |
| 2 | That, as a fraction of the sled's 1291 J | **23.6 %** | 21 to 26 % |
| 3 | Copper burned during regen at the rated point | **15 J** | below 30 J, and below 100 J under the pessimistic 1.30 m convention |
| 4 | Electrical-to-payload efficiency after the credit | **21.2 %** | 20.5 to 21.5 %, under **either** copper convention |
| 5 | Sled energy still arriving at the brake | **952 J** | 900 to 1000 J. **The eddy brake stays in the design** |
| 6 | Exit velocity | **unchanged, 16.537** | identical to three decimals: regen acts after release and must not reach back through it |
| 7 | Optimum braking force within the rating | **at the rating, no interior optimum** | recovery increases monotonically to `K_RATED` |
| 8 | Peak bank current during regen | **~244 A** | below the shot's 346.8 A, so the drive is not re-rated |

**Falsification.** Row 7 landing on an interior optimum would mean copper dominates over 240 mm
and this is worth a fraction of the claim. Row 5 coming back below 300 J would mean the motor
*can* very nearly arrest the sled, which would make the 2025 decision wrong rather than narrow,
and R5 would have to be reopened rather than supplemented. Row 6 moving at all is a model
defect, not a result: it would mean regen is coupled to the acceleration integration somewhere
it should not be.

**What this run cannot settle.** Whether 240 mm of stator can be packaged into the arrest section
alongside a working eddy brake. The energy side of that repartition looks easy, the fin's duty
falls 26 % so a shorter fin still holds its transient rise, but the eddy coefficient would have
to roughly triple to arrest the sled in the remaining length, and no fin has been designed to
that. **A11 answers the electromagnetic question only**; the mechanical one is recorded as an
open item, not assumed away.

**What it also cannot settle** is whether recovery is worth its mass. The regen section is added
stator and added converter, against a mass rollup that already excludes the enclosure, radiator
and avionics (P10). 305 J per shot is 3.7 kJ over a twelve-shot campaign, and that is an energy
argument, not a mass one.
