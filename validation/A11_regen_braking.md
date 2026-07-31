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

---

## Result, run 2026-07-31

`motor_model.regen_brake()` integrates the sled alone from the shot's own end state: its exit
velocity and the bank voltage the shot left behind, both read from `shot()` rather than typed,
so this cannot be quoted against a stale operating point. Charging is solved through the same
ESR the discharge uses, in the other direction.

### Braking force, over the 240 mm the envelope allows

| F / rated | F, N | Mechanical extracted | Copper | Bank ESR | **To the cells** | % of sled KE | Peak A | v leaving |
|---|---|---|---|---|---|---|---|---|
| 0.25 | 353 | 84.8 | 0.9 | 0.6 | 76.2 | 5.9 | 58 | 15.98 |
| 0.50 | 707 | 169.7 | 3.7 | 2.2 | 152.5 | 11.8 | 116 | 15.41 |
| 0.75 | 1060 | 254.5 | 8.4 | 4.8 | 225.9 | 17.5 | 171 | 14.82 |
| **1.00, the rating** | **1413** | **339.3** | **15.2** | **8.2** | **296.6** | **23.0** | **225** | **14.20** |
| *1.25* | *1767* | *424.2* | *24.2* | *12.1* | *364.7* | *28.2* | *277* | *13.55* |
| *1.50* | *2120* | *509.1* | *35.7* | *16.4* | *430.0* | *33.3* | *327* | *12.87* |
| *2.00* | *2827* | *678.7* | *66.8* | *25.8* | *551.9* | *42.7* | *422* | *11.39* |
| *3.00* | *4240* | *1018.3* | *173.9* | *43.5* | *754.3* | *58.4* | *593* | *7.61* |
| *3.81* | *5385* | *1291.9* | *409.2* | *51.2* | *812.6* | *62.9* | *714* | *0.00* |

**Rows below the rule are the design. Rows above it are italicised because they are not
available**: they need sheet current beyond `K_RATED`, which is the 2025 argument restated. They
are reported because the shape matters. Recovery is still climbing at 3.81x rated, where the sled
stops dead inside 240 mm, so **the thing standing between this machine and full regenerative
arrest is the winding rating, not the physics of copper loss**. That is a Phase II question with
a converter current limit in front of it (714 A against the shot's 347 A), and it is not asked
here.

### Distance, at the rating

| Regen section | Extracted | Copper | To the cells | % of sled KE | Still to the brake |
|---|---|---|---|---|---|
| 100 mm | 141.5 | 2.5 | 127.0 | 9.8 | 1149.9 |
| 200 mm | 282.9 | 10.4 | 249.3 | 19.3 | 1008.5 |
| **240 mm, the envelope** | **339.3** | **15.2** | **296.6** | **23.0** | **952.1** |
| 400 mm | 565.5 | 44.8 | 477.1 | 36.9 | 726.0 |
| 500 mm | 706.9 | 73.2 | 581.1 | 45.0 | 584.5 |
| 730 mm | 1032.0 | 180.2 | 781.5 | 60.5 | 259.5 |
| 1000 mm | 1291.5 | 447.4 | 806.7 | 62.5 | 0.0 |

Distance is the strong lever and the envelope is what denies it. At 1000 mm the sled stops
without a brake at all and gives back 62.5 %; the machine is 44 % over ESPA Grande already (P9),
so that row is a fact about free-flyers, not about this deployer. It is the same conclusion
PII-8 reached from the acceleration side, arrived at independently from the braking side.

### Against the declared bands

| # | Prediction | Result | |
|---|---|---|---|
| 1 | 305 J to the bank, accept 280 to 330 | **296.6 J** | **pass** |
| 2 | 23.6 % of sled KE, accept 21 to 26 | **23.0 %** | **pass** |
| 3 | copper below 30 J, below 100 J pessimistic | **15.2 J**, 82.2 J pessimistic | **pass** |
| 4 | efficiency 20.5 to 21.5 % under either convention | **21.16 %**, 20.68 % pessimistic | **pass** |
| 5 | 900 to 1000 J still to the brake | **952.1 J** | **pass** |
| 6 | v_exit identical to three decimals | 16.537, asserted in `__main__` | **pass** |
| 7 | no interior optimum below the rating | monotone to 3.81x, let alone to 1.0x | **pass** |
| 8 | peak current below the shot's 346.8 A | **225.3 A** | **pass** |

**Eight of eight.** The prediction that mattered most was row 7, and it held for a reason worth
stating plainly: the braking pulse is 15.6 ms against the shot's 157 ms and energises 240 mm of
stator against 1300 mm, so copper during regeneration is **15 J against the shot's 828**. The
intuition that regenerative braking is defeated by resistive loss is an intuition about long
duty cycles, and this is not one.

### What changed downstream

| | Before | After |
|---|---|---|
| Net bank draw per shot | 2881.2 J | **2584.6 J** |
| Electrical-to-payload efficiency | 18.98 % | **21.16 %** |
| Energy to the eddy brake per shot | 1291.4 J | **952.1 J** |
| Winding heat per shot | 827.9 J | 843.1 J |
| Twelve-shot campaign heat | 28.0 kJ | **24.4 kJ** |
| Fin adiabatic rise per shot | 4.0 K | 3.0 K |
| Exit velocity | 16.537 m/s | **16.537 m/s** |

`energy_closure()` closes at 100 % on the net draw, with the sled's energy now split three ways
rather than dumped in one.

### The defect this opens

**240 mm of regen stator and a 300 mm eddy fin do not both fit a 339 mm arrest section.** The
thermal side of a repartition is easy, the fin's duty falls 26 % and its transient rise with it,
but no layout has been drawn and the eddy coefficient would have to rise sharply to arrest the
sled in what is left. Logged as **P28** rather than resolved here by shortening the fin in a
script, which would be exactly the "hand-edit to match" this repository's validation conventions
forbid.

### What A11 does not do

It does not reverse the 2025 arrest decision. The eddy brake still absorbs 952 J of every shot,
73.7 % of what it absorbed before, and the ring spring still catches the residual. R5 was right
about arrest and is now supplemented rather than contradicted: **the motor cannot stop the sled,
and it can take back about a quarter of the sled's energy on the way past.** Both statements are
true and only the first one was ever in the record.
