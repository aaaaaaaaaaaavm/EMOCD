# Benchtop tests: the cheapest route to a measured number

**E4 says it plainly: nothing in this project has been built, fired, or measured.** Every
number in this repository is a model output, and two of them are cross-checked only against
another model. That is the one gap no amount of further analysis closes.

This document exists because closing it does not require a lab. Four experiments are listed,
cheapest first. **The first one costs about the price of two magnets and would give this
project its first measured number.** Each closes a *specific named claim*, and each has its
acceptance band declared here (before the test) in the same discipline `validation/` uses
for the analyses.

None of these have been run. If you run one, record the result against the band as declared,
including if it fails.

---

## The bands are now derived, not chosen: added 2026-07-30

The bands below were declared before any test, which is the important part. But they were
*chosen* (±15 %, ±20 %) rather than traced to an error budget, and a band with no derivation
cannot be defended if a reading lands just outside it.

[`validation/bench/bench_predict.py`](../validation/bench/bench_predict.py) now derives them. It
**imports** `verify_field.py` and `motor_model.py` rather than reimplementing the geometry, and
carries a guard that fails loudly if its local field build ever drifts from
`verify_field.make_array`, the same idea as `_check_operating_point()` in `sizing.py`. It
perturbs what a bench build actually gets wrong (gap ±0.5 mm, Br ±3 %, block thickness ±0.1 mm),
re-solves, and reports the spread. Output: `validation/results/bench_predictions.json`.

| B-1 row | Model | Measurement error, RSS | Band declared |
|---|---|---|---|
| Peak gap field | 0.694 T *(magpylib; 0.703 T analytic)* | **4.4 %** | ±15 % |
| Winding mean \|B\| | 0.552 T | **4.5 %** | ±15 % |
| Stray at 10 mm | 22.7 mT | **3.7 %** | ±20 % |
| Stray at 20 mm | 4.3 mT | **4.2 %** | ±40 % |
| Stray at 50 mm | 0.4 mT | **3.3 %** | order of magnitude |
| **B-2** thrust per kA/m | 11.218 N | **13.5 %** | ±20 % |

**The bands are three to ten times wider than the measurement error, and that is correct.** A
declared band has to cover *model* error, which is the thing under test and cannot be budgeted
from the model itself. What the budget establishes is the other half: **the rig is not the limiting
factor.** A reading outside ±15 % cannot be blamed on shim stack or magnet grade, because those
together account for 4.5 %. That is what makes a failure interpretable, and it is the reason to
derive the budget even when it does not move the number.

Two things the derivation turned up that the procedures did not say:

### For a two-block bench pair, the blocks face the same way

B-1 below says "a two-block **opposed** pair", which is ambiguous in the one way that matters:

| Two-block arrangement | Mean \|B_y\| at midgap |
|---|---|
| Polarizations facing each other across the gap | **0.00000 T**: cancels exactly |
| Polarizations both the same direction | **0.329 T** |

Built the first way the rig reads **zero field and zero force**, which looks like a falsified model
rather than a reversed magnet. `verify_field.py` probes for the correct convention automatically on
the four-block array, so this trap exists only on the bench. **The pair also attracts hard across
12 mm**, assemble with a captive non-magnetic spacer, shimming outward from a closed stack, never
inward by hand.

### B-2's load cell should be sized to the smallest force, not the largest

At low sheet current the force is small, and a load cell specified at 0.5 % of *full scale*
contributes error inversely with the reading. Sizing the cell to the largest expected force makes
the smallest reading the least trustworthy, the opposite of what B-2 needs, since low current is
where it is meant to operate. **Choose the cell for the lowest force in the sweep**, and if one
cell cannot span the range, sweep current over a narrower band and rely on the linearity check.

### One term in the budget is understated, and it is recorded rather than fixed

For the three stray rows the probe sits a fixed distance behind the **back face**, so changing block
thickness moves the reference plane as well as the source. The budget's `thickness` term captures
only the source movement. The affected contributions are 0.8-1.8 % against an RSS of 3.3-4.2 %, so
it does not change any conclusion, but it is a known-incomplete term and is flagged in the script
rather than left to be discovered.

---

## B-1: Halbach pair field profile

**Closes:** the field model behind everything (**A24**, **E1**), and the keep-out in **P3**.
**Cost:** low, two to four N45SH blocks, a Hall probe, printed spacers.
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
checked analytic-against-analytic, a wave model against magpylib, which is two implementations
of the same physics. A gaussmeter is a different *kind* of evidence entirely.

---

### B-1 bill of materials

Written 2026-07-30 so B-1 stops being a procedure and becomes a purchase order. **Every price
below is an estimate, not a quotation.** `analysis/cost.py` carries the same caveat for the
machine itself and it applies with more force here, where the quantities are ones and twos.

**The magnets are not one part number, and this is the thing most likely to go wrong.** A
Halbach wavelength needs four blocks magnetised in four different directions. In practice that
is two part numbers, each ordered four times per side:

| | Block | Magnetisation | Qty for a double-sided pair |
|---|---|---|---|
| Type A | 12 x 8 x 90 mm N45SH | through the **8 mm** thickness | 4 |
| Type B | 12 x 8 x 90 mm N45SH | along the **12 mm** length | 4 |

Dimensions are from `cad/parameters.json`: wavelength 48 mm over four blocks gives 12 mm each,
magnet thickness 8 mm, array depth 90 mm. Each block is 8.64 cm3, about 65 g; eight of them
about 520 g.

**Specify the magnetisation direction explicitly on the order, with a sketch.** A supplier
given "12 x 8 x 90, N45SH" will magnetise through the largest face by default, which gives four
identical blocks and no Halbach array.

| Item | Spec | Qty | Est. INR | Source |
|---|---|---|---|---|
| N45SH block, magnetised through thickness | 12 x 8 x 90 mm | 4 | 2,000-4,000 | Magnaplast Technologies (Pune) or Meena Magnetic; both list custom NdFeB blocks |
| N45SH block, magnetised along length | 12 x 8 x 90 mm | 4 | 2,000-4,000 | as above, same order |
| Digital teslameter with transverse Hall probe | **1 T minimum range**, 2 % or better | 1 | 15,000-45,000 | Permanent Magnets Ltd (TM-901EXP class), or an imported PCE unit |
| Aluminium plate for the fixture | 200 x 150 x 10 mm, 2 off | 2 | 1,500 | any local stockist |
| Non-magnetic fasteners | A4 / 316 stainless M6 | 10 | 500 | local |
| Printed spacers | PETG or nylon, 12.0 mm nominal plus a shim set | set | 500 | own printer |
| Feeler gauges | 0.05 to 1.00 mm | 1 set | 700 | local |
| **Total** | | | **22,000-52,000** | |

The teslameter dominates and is the only line worth shopping hard. **1 T range is the binding
requirement**: the model predicts 0.694 T at midgap, so a 200 mT instrument, which is what most
cheap "gauss meters" are, saturates and reads nothing useful. If a lab at SIT has one, borrowing
it removes two thirds of the cost.

### The safety item, quantified

The two arrays attract. Over one wavelength at the design gap, Maxwell stress on
48 x 90 mm at 0.694 T gives roughly

```
F = B^2 A / 2 mu_0 = 0.694^2 x 0.0043 / (2 x 4pi x 10^-7) = 828 N
```

**About 84 kgf, across a 12 mm gap, on brittle sintered NdFeB.** That is not a handling
inconvenience, it is the hazard in this experiment. Nothing else on the bench stores that much
energy.

- Build the fixture so the gap is **set by a captive spacer that cannot be removed while the
  magnets are mounted**, and shim outward from a closed stack. Never approach the gap from open.
- Keep fingers out of the plane of the gap during assembly.
- The 37 % overestimate in P17 applies to the flat-plate formula used above, so the real figure
  is likely nearer 600 N. **Design the fixture for 828 N anyway**: the error is in the
  conservative direction and the cost of over-building an aluminium bracket is nothing.

### What a result buys

The first measured number in this project at any scale. Every headline descends from a field
model checked twice against other models and never against a magnet, and
[`../validation/bench/bench_predict.py`](../validation/bench/bench_predict.py) has already
derived the bands, so the reading is interpretable the day it is taken: the rig contributes
4.4 % against a declared 15 %, which means a miss cannot be blamed on the build.

---

## B-2: Single-coil thrust constant

**Closes:** the analytic-only status of **K<sub>t</sub> = 11.03 N per kA/m**: the number every
headline is downstream of. Partially closes **E1**.
**Cost:** moderate, B-1's magnets, wound coil, load cell, bench supply.
**Time:** a few days including winding.

### Method

Mount the Halbach pair from B-1 on a load cell. Wind a single-phase coil to the design
geometry (10 mm thick, 60 % fill) and energise at a **known, low** sheet current, a few
kA/m, DC or low duty, far below the 140 kA/m rating. Measure force against current at several
positions through one wavelength (48 mm).

Force scales linearly with sheet current, so a low-current measurement extrapolates. **Do not
attempt rated current on a bench**, 330 A into an unrestrained coil next to a magnet array is
a genuine hazard, and the linearity is the whole point.

### Bands, declared now

| Quantity | Model says | Accept if |
|---|---|---|
| Thrust per unit sheet current | 11.03 N per kA/m | within **±20 %** |
| Force ripple over one wavelength | ±0.99 % | within **±2 pts**, i.e. under ±3.3 % |
| Linearity of force vs current | linear | R² > 0.98 over the swept range |

±20 % is wide, and deliberately so: a single coil is not a three-phase belt winding, and the
scaling from one to the other is itself part of the model being tested. **A result outside
±20 % means the model is wrong, not the test.**

### The trap

`motor_model.py` carries a warning worth repeating here: an early version held the field
fixed while commutating current and produced near-zero mean thrust. The field must translate
*with* the sled. On a bench the equivalent error is measuring at one position and calling it
the mean, **sweep the wavelength.**

---

## B-3: Capacitor discharge into a resistive load

**Closes:** the two open **E17** findings, no script defines a bank ESR, and the quoted sag
is state-of-charge rather than the terminal voltage the drive sees. Gives **A8** a measured
anchor.
**Cost:** moderate, the bank is the expensive part; a sub-scale bank at lower voltage tests
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
| Bank ESR | 12 mΩ assumed | measured value **recorded**; no pass/fail, this is a measurement, not a check |
| SoC sag at equivalent energy | 5.19 % | within **±1.5 pts** |
| Terminal droop | 10.25 % total per A8 | within **±3 pts** |

**ESR gets no band on purpose.** No current script defines one; A8's finding was that
∫I²dt = 8008 A²s implies ~20 mΩ against the 12 mΩ assumed. Declaring a band around a number
the project has not committed to would be inventing a target to hit.

---

## B-4: Eddy-brake coupon, drop test

**Closes:** the first measured point on **E20**, which records that no force-time profile for
the arrest exists anywhere in the scripts, only a 200 g cap used for bond sizing.
**Cost:** low, a copper plate, a magnet carriage, a vertical rail, a high-speed phone camera.
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
edge effects or skin depth. **The form matters more than the constant**: if force is not
proportional to velocity, the brake model is wrong in a way no amount of coefficient tuning
fixes.

---

## What these four together would change

Right now `PROVENANCE.md` can say of every number that it is a model output. After B-1 alone
that stops being true, and after all four the project has measured anchors on the field, the
thrust constant, the pulse chain and the brake, the four subsystems the whole machine
consists of.

**None of it qualifies anything.** These are sub-scale, ambient, single-article experiments,
and `docs/QUALIFICATION_PLAN.md` is what qualification actually requires. But the difference
between a design study with no measurements and one with four is not a matter of degree, it
is the difference between a proposal and an experiment.

Record results in `validation/results/` alongside the analysis outputs, in the same format,
**including failures.** A benchtop result that contradicts the model is worth more than one
that confirms it, and this repository's whole method is built on saying so before the run
rather than after.
