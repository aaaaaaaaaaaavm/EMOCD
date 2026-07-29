# Benchtop tests — the cheapest route to a measured number

**E4 says it plainly: nothing in this project has been built, fired, or measured.** Every
number in this repository is a model output, and two of them are cross-checked only against
another model. That is the one gap no amount of further analysis closes.

This document exists because closing it does not require a lab. Four experiments are listed,
cheapest first. **The first one costs about the price of two magnets and would give this
project its first measured number.** Each closes a *specific named claim*, and each has its
acceptance band declared here — before the test — in the same discipline `validation/` uses
for the analyses.

None of these have been run. If you run one, record the result against the band as declared,
including if it fails.

---

## B-1 — Halbach pair field profile

**Closes:** the field model behind everything (**A24**, **E1**), and the keep-out in **P3**.
**Cost:** low — two to four N45SH blocks, a Hall probe, printed spacers.
**Time:** an afternoon.

### Method

Build a two-block opposed pair at the design gap (12 mm) using non-magnetic printed spacers,
clamped in a non-conductive fixture. Traverse a Hall probe on the centreline and behind the
back face. **A single-wavelength four-block array is better** if the budget stretches, because
the four-block case is what `verify_field.py` actually models.

Measure: peak field in the gap; field at 10, 20 and 50 mm behind the back face.

### Bands, declared now

| Quantity | Model says | Accept if |
|---|---|---|
| Peak gap field | 0.703 T analytic double-peak | within **±15 %** |
| Winding mean \|B\| | 0.552 T | within **±15 %** |
| Stray at 10 mm | 22.7 mT | within **±20 %** |
| Stray at 20 mm | 4.3 mT | within **±40 %** |
| Stray at 50 mm | 0.4 mT | **order of magnitude only** |

The far-field bands widen deliberately. Those values are small differences of large numbers,
`RESULTS.md` already calls them the least trustworthy row in the repository, and they were
wrong in the published paper once (P3). **A 50 mm reading that lands within a factor of two is
a pass; the model does not deserve better than that.**

### Why this one first

Every headline number descends from the field model, and the field model has only ever been
checked analytic-against-analytic — a wave model against magpylib, which is two implementations
of the same physics. A gaussmeter is a different *kind* of evidence entirely.

---

## B-2 — Single-coil thrust constant

**Closes:** the analytic-only status of **K<sub>t</sub> = 11.22 N per kA/m** — the number every
headline is downstream of. Partially closes **E1**.
**Cost:** moderate — B-1's magnets, wound coil, load cell, bench supply.
**Time:** a few days including winding.

### Method

Mount the Halbach pair from B-1 on a load cell. Wind a single-phase coil to the design
geometry (10 mm thick, 60 % fill) and energise at a **known, low** sheet current — a few
kA/m, DC or low duty, far below the 140 kA/m rating. Measure force against current at several
positions through one wavelength (48 mm).

Force scales linearly with sheet current, so a low-current measurement extrapolates. **Do not
attempt rated current on a bench** — 330 A into an unrestrained coil next to a magnet array is
a genuine hazard, and the linearity is the whole point.

### Bands, declared now

| Quantity | Model says | Accept if |
|---|---|---|
| Thrust per unit sheet current | 11.22 N per kA/m | within **±20 %** |
| Force ripple over one wavelength | ±1.26 % | within **±2 pts**, i.e. under ±3.3 % |
| Linearity of force vs current | linear | R² > 0.98 over the swept range |

±20 % is wide, and deliberately so: a single coil is not a three-phase belt winding, and the
scaling from one to the other is itself part of the model being tested. **A result outside
±20 % means the model is wrong, not the test.**

### The trap

`motor_model.py` carries a warning worth repeating here: an early version held the field
fixed while commutating current and produced near-zero mean thrust. The field must translate
*with* the sled. On a bench the equivalent error is measuring at one position and calling it
the mean — **sweep the wavelength.**

---

## B-3 — Capacitor discharge into a resistive load

**Closes:** the two open **E17** findings — no script defines a bank ESR, and the quoted sag
is state-of-charge rather than the terminal voltage the drive sees. Gives **A8** a measured
anchor.
**Cost:** moderate — the bank is the expensive part; a sub-scale bank at lower voltage tests
the same physics.
**Time:** days.

### Method

Discharge a supercapacitor bank into a resistive load sized to draw a comparable current
profile. Instrument terminal voltage and current directly. Compare measured ESR against the
12 mΩ assumed in the A8 netlist, and measured terminal droop against the 5.19 %
state-of-charge sag.

### Bands, declared now

| Quantity | Model says | Accept if |
|---|---|---|
| Bank ESR | 12 mΩ assumed | measured value **recorded**; no pass/fail — this is a measurement, not a check |
| SoC sag at equivalent energy | 5.19 % | within **±1.5 pts** |
| Terminal droop | 10.25 % total per A8 | within **±3 pts** |

**ESR gets no band on purpose.** No current script defines one; A8's finding was that
∫I²dt = 8008 A²s implies ~20 mΩ against the 12 mΩ assumed. Declaring a band around a number
the project has not committed to would be inventing a target to hit.

---

## B-4 — Eddy-brake coupon, drop test

**Closes:** the first measured point on **E20**, which records that no force-time profile for
the arrest exists anywhere in the scripts — only a 200 g cap used for bond sizing.
**Cost:** low — a copper plate, a magnet carriage, a vertical rail, a high-speed phone camera.
**Time:** an afternoon.

### Method

Drop a magnet carriage down a vertical rail past a copper fin and track position against time
from video. Differentiate twice for deceleration, or fit the exponential the first-order plate
drag law predicts.

### Bands, declared now

| Quantity | Model says | Accept if |
|---|---|---|
| Drag coefficient form | F ∝ v (first-order plate drag) | linear fit **R² > 0.95** over the velocity range |
| Drag constant | σ·t·B²·A from `legacy/c3_c4_em.py` | within **a factor of 2** |

A factor of two is honest for a first-order law with no correction for finite plate width,
edge effects or skin depth. **The form matters more than the constant** — if force is not
proportional to velocity, the brake model is wrong in a way no amount of coefficient tuning
fixes.

---

## What these four together would change

Right now `PROVENANCE.md` can say of every number that it is a model output. After B-1 alone
that stops being true, and after all four the project has measured anchors on the field, the
thrust constant, the pulse chain and the brake — the four subsystems the whole machine
consists of.

**None of it qualifies anything.** These are sub-scale, ambient, single-article experiments,
and `docs/QUALIFICATION_PLAN.md` is what qualification actually requires. But the difference
between a design study with no measurements and one with four is not a matter of degree — it
is the difference between a proposal and an experiment.

Record results in `validation/results/` alongside the analysis outputs, in the same format,
**including failures.** A benchtop result that contradicts the model is worth more than one
that confirms it, and this repository's whole method is built on saying so before the run
rather than after.
