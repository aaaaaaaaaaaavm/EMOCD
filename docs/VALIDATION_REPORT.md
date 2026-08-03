> **Numerical audit correction, 2026-08-03.** The current operating point is 11.03 N per
> kA/m, 16.388 m/s, 10.53 g, 291.4 J recovered, 934.7 J to the brake, and 20.99% net
> efficiency. A13's former residual-rate/cadence conclusion is superseded, A6's 3.7e-8
> result is only a fixed-shape sensitivity, and the corrected brake-fin transient is 7 K
> per shot. Values below that describe earlier audit states are retained as history.
>
> **Gen4 boundary, 2026-08-03.** None of these results validates the provisional
> `EMOCD_Gen4_Open v7` geometry. Its final 148.5 mm of acceleration occurs under partial
> Halbach/stator overlap, and no position-dependent force result exists. The Phase I / Gen3
> values remain the only rated point; see `GEN4_STATUS.md`, P32 and E27.

# Validation report: 2026-07-28

Every headline claim in this repository, and what independently checking it produced.

Four things were actually run: the analysis scripts were re-executed from a clean copy,
GMAT R2022a propagated the orbits, ngspice simulated the pulse chain, and the Gen3 sled
geometry was measured against material densities. Three planned analyses were **not** run
and are listed as such, nothing here is inferred from an analysis that did not happen.

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

Every number in `analysis/results/*.json` (and therefore every headline figure) is
regenerable from the committed scripts today. This is the claim `D12` makes, and it holds.

---

## 2. Astrodynamics: GMAT R2022a (A5)

GMAT was installed and run headless: MSISE90 atmosphere, 20x20 gravity, Luna and Sun as
point masses, SRP on, RK89. Independently implemented force models, not a second pass of
the same code.

### The x1.80 multiplier holds at two activity levels. **Its invariance does not.**

All three runs are complete.

| Solar activity | GMAT baseline | GMAT boosted | Multiplier | vs x1.80 | Band ±5 % |
|---|---|---|---|---|---|
| High (F10.7 250) | 144.5 d | 250.0 d | **1.7302** | −3.88 % | pass |
| Mean (F10.7 150) | 429.9 d | 763.1 d | **1.7750** | −1.39 % | pass |
| **Low (F10.7 70)** | **2359.1 d** | **4892.3 d** | **2.0739** | **+15.21 %** | **FAIL** |

**Invariance spread across the three: 18.48 % against a ≤5 % band. A5's verdict is FAIL.**

An earlier version of this section reported 2.55 % and called the invariance confirmed. That
was computed from the two levels that had finished at the time, and it was wrong, recorded
here rather than quietly replaced.

### Why the two codes disagree, tested rather than guessed

`astro.py` models solar activity as a **uniform multiplicative scale on density**. Sweep
that scale over a factor of forty and the multiplier does not move:

| density scale | 0.25 | 0.5 | 1.0 | 2.5 | 5.0 | 10.0 |
|---|---|---|---|---|---|---|
| multiplier | 1.7992 | 1.7991 | 1.7989 | 1.7982 | 1.7971 | 1.7968 |

Constant to 0.1 % across 40x. **That is not a physical result, it is arithmetic.** A
uniform density factor divides both lifetimes by the same number, so the ratio survives by
construction of the model. The invariance was never tested by the sweep that claims to
demonstrate it.

MSIS changes the *shape* of the density-altitude profile as F10.7 varies, not just its
magnitude. The boosted orbit carries apogee about 37 km higher than the baseline, so the two
orbits sample the profile differently and the ratio moves: 1.73 at high activity, 2.07 at
low.

**What survives:** the x1.80 point value at mean and high activity, comfortably. **What does
not:** the claim that it is invariant across solar activity, which is stated in the paper's
abstract and which the paper's own Limitations section nominates as "the defensible result".
Recorded as P16.

### Absolute lifetimes: **not confirmed, as expected**

GMAT decays faster than `astro.py` at high and mean activity: 144.5 days against 190 at high
activity. The bounded 30-day window measured the same thing independently, fitted rates of
−0.1618 km/day (GMAT) against −0.1216 (`astro.py`), a factor of **1.33**. The two agree with
each other: 190 ÷ 1.33 ≈ 143 days.

E6 said absolute lifetimes carry severalfold uncertainty and that only the ratio is
defensible. That is now demonstrated rather than asserted.

The disagreement changes sign with activity, which is the same story from another angle:

| | `astro.py` | GMAT | |
|---|---|---|---|
| Low activity | 2.61 yr | **6.46 yr** | GMAT 2.5x longer |
| Mean | 1.30 yr | 1.18 yr | GMAT 9 % shorter |
| High | 0.52 yr | 0.40 yr | GMAT 23 % shorter |

A model whose error changes sign across its input range is not off by a calibration factor,
it has the wrong shape.

Detail: [`validation/results/A5_astro.json`](../validation/results/A5_astro.json).

---

## 3. Pulse-power chain: ngspice (A8)

The mechanical ODE was rebuilt in analogue-computer form so SPICE integrates it with a
different scheme (trapezoidal) than `motor_model.py` (forward Euler, dt = 1e-4), while the
electrical side is a real circuit: 6 F bank, 96 V, series ESR, load drawing P/V at the
terminal.

| Quantity | `motor_model.py` | ngspice | Deviation | Band | |
|---|---|---|---|---|---|
| Exit velocity | 20.372 m/s | 20.366 | −0.03 % | ±10 % | pass |
| Pulse duration | 127.7 ms | 127.66 | −0.03 % | ±10 % | pass **at the superseded operating point**, see P23. The current value is 157.3 ms, outside this band |
| Peak current | 391.7 A | **415.2 A** | +5.98 % | ±10 % | pass |
| Bank sag | 4.88 % | 5.06 % | +0.18 pts | ±1.5 pts | pass |
| Energy drawn | 2634 J | 2729 J | +3.59 % | ±5 % | pass |

Two different integrators landing within 0.03 % on exit velocity is a real check of the
shot model's arithmetic. All five declared bands met, **and two findings fell out anyway.**

### A8-R: re-run at the current operating point, 2026-07-30

The table above belongs to the 20.37 m/s point. The deck was re-run at 16.537 m/s against bands
declared fresh and committed before the deck was touched.

| Quantity | Reference | ngspice | Deviation | Band | |
|---|---|---|---|---|---|
| Peak current | 330.3 A | 346.8 A | +5.0 % | ±10 % | pass |
| Pulse duration | 157.3 ms | 157.26 | −0.03 % | ±10 % | **pass**, and this closes the P23 row |
| Energy drawn | 2796 J | 2880 J | +3.0 % | ±5 % | pass |
| Bank sag | 5.19 % | 5.35 % | +0.2 pts | ±1.5 pts | pass |
| Copper loss | 828 J | 827.7 J | −0.04 % | ±15 % | pass, but not independent: `Pcu` is a constant in the deck |
| Energy closure | 100.0 % | **97.0 %** | −3.0 pts | 98-102 % | **fail** |

**Five of six.** The closure failure is bank ESR dissipation, 85.5 J per shot, which the circuit
models and the analytic ledger had no term for at all. Logged as **P24** and corrected the same
day: `motor_model.py` now integrates the term.

**What the correction did to this table is the point of running A8 at all.** Re-evaluated against
the corrected model, the two methods agree far more closely than the run recorded:

| Quantity | Corrected model | ngspice | Deviation |
|---|---|---|---|
| Peak current | 346.77 A | 346.8 A | **0.01 %** (was 5.0 %) |
| Energy drawn | 2881.2 J | 2880 J | **0.04 %** (was 3.0 %) |
| Bank sag | 5.354 % | 5.35 % | **0.004 pts** (was 0.2 pts) |

The 5 % peak-current deviation had been recorded twice, in A8 and again in A8-R, and attributed
both times to the difference between a forward-Euler and a trapezoidal integrator. It was not the
integrator. It was a missing physical term, and it took a second method to expose it.

Detail: [`validation/results/A8_pulse.json`](../validation/results/A8_pulse.json), netlist at
[`validation/spice/emocd_shot.cir`](../validation/spice/emocd_shot.cir).

---

## 3b. Bank ESR: the shot does not close on commercial cells (A10)

Run 2026-07-30 against bands committed beforehand. Not a cross-check of a number: a test of
whether the pulse-power chain closes at all.

For an EDLC, ESR times capacitance is roughly constant within a technology. Two Eaton 3.0 V
cells thirty times apart give 0.69 and 1.10 s. The bank as modelled, 5.94 F at 12 mΩ, implies
**0.071 s**, an order of magnitude better than either. At a realistic product the bank is
**116 to 185 mΩ**.

A source of EMF V behind resistance R cannot deliver more than V²/4R. The shot needs 30.0 kW at
peak velocity.

| | |
|---|---|
| Highest bank ESR at which the shot completes | **65 mΩ** |
| A single string of 32 × 190 F cells | **116 to 185 mΩ** |
| Margin | **none** |

**Exit velocity, stroke time and dispersion do not move anywhere in the sweep.** The commanded
force is constant, so the mechanical integration never sees the bank until the bank fails to
source it. This defect is contained in the pulse chain.

**Five of six declared rows passed; one is recorded void** because it assumed a loss figure that
only exists if the shot runs. Detail: [`validation/A10_bank_esr.md`](../validation/A10_bank_esr.md),
defect **P26**, options costed as PII-7.

**A10 caught its own instrument first.** The integrator had a fallback that silently substituted
a no-ESR current when the bank could not source the load, which produced completed runs at every
resistance with peak current *falling* as resistance rose. Logged separately as **P27**.

---

## 4. Sled mass: computed from Gen3 CAD solid volumes (A4, partial)

Exact solid volumes from the OpenCASCADE kernel, multiplied by material densities. The
magnet density (7500 kg/m³) is the repo's own, from `sizing.py`.

| Body | n | cm³ each | Material | kg |
|---|---|---|---|---|
| Chassis plate 488x140x6 | 2 | 409.9 | Ti-6Al-4V | 3.632 |
| Halbach array 340x90x8 | 2 | 244.8 | NdFeB | 3.672 |
| Backstop 8x140x100 | 1 | 112.0 | Ti-6Al-4V | 0.496 |
| Chassis web 488x6x28 | 2 | 82.0 | Ti-6Al-4V | 0.727 |
| Brake fin 120x80x4 | 1 | 38.4 | Copper | 0.344 |
| Roller arm 40x16x20 | 4 | 12.8 | Ti-6Al-4V | 0.227 |
| Roller Ø30x16 | 4 | 11.3 | 440C steel | 0.348 |
| **Total as drawn** | | | | **9.445** |

**The method reproduces the existing claim exactly.** Fed 7.50 kg, the shot model returns
17.87 m/s, the 17.88 m/s that P8 states. Fed the CAD-derived 9.445 kg, it returns **16.53 m/s
at 10.7 g and 19.6 % efficiency**.

What this is not: it is not the structural FEA A4 specifies. It measures the sled *as
drawn*, with solid plates and no lightening pockets. A real design would pocket them. The
stiffness question (the lightest chassis that holds the airgap to ±0.05 mm) remains open.

---

## 4b. Sled chassis structural: CalculiX (A4)

Quadratic-tet FE of one 488x140x6 mm chassis plate lifted straight out of the Gen3 STEP,
29,312 nodes, loaded with the 3672 N Maxwell attraction over the 340x90 mm magnet footprint
from `sizing.json`. Support at the web lines is bracketed, pinned (lower bound on
stiffness) and clamped (upper bound), because the real joint is between the two and
reporting one number would be a choice dressed as a result.

| Band, declared before the run | Result | |
|---|---|---|
| Airgap closure ≤ 0.025 mm per plate | **0.0194 mm** pinned, 0.0160 clamped | pass, 78 % of budget |
| Von Mises ≤ 587 MPa | **33.7 MPa** | pass, **17x margin** |
| First mode > 200 Hz | **3408 Hz** | pass, 17x |

**The chassis as drawn is sound.** It is nowhere near strength-limited and comfortably
inside the deflection budget.

> **The load itself was never checked, and it is 37 % high, P17, found 2026-07-29.**
> The 3672 N comes from a flat-plate Maxwell-stress formula in `sizing.py`: a uniform
> `B²/2μ₀` at a 0.55 T mean face field over the footprint. Recomputing the same force with
> `magpylib.getFT()`, which meshes the blocks and integrates the field gradient in 3-D on the
> repo's own array geometry, converges to **2686.6 N**: deltas halving cleanly through a
> (14,14,14) mesh and independent of the finite-difference step from 1e-5 to 1e-8. The reason
> is structural: Maxwell stress needs mean(B²), the formula uses mean(B)², and
> mean(B²) ≥ mean(B)² for any non-uniform field, so the analytic form must overestimate a
> Halbach face. **This does not reverse anything above**: the real load is lighter, so every
> band passed with more margin than reported, not less. What it does mean is that A4's input
> was taken on trust, which is the one thing this report is supposed to stop.
> Reproduce: `python3 validation/magpylib/check_inter_array_force.py`.

**And that is why the velocity problem does not go away.** A4 was supposed to decide whether
the sled could be lighter. The answer it gives is that the drawn plate already meets the
constraint, so nothing structural forces it to be heavier, but equally, nothing here makes
it lighter. Uniform thinning is nearly worthless: deflection scales as 1/t³, so the budget
is spent at about 5.5 mm, which saves 0.30 kg of 9.445 and moves exit velocity from 16.53 to
roughly 16.7 m/s. Genuine reduction needs a rib-stiffened redesign, section depth enters as
the square, and **no analysis anywhere has evaluated one.** The 60 % pocketing row in
`docs/DESIGN_OPTIONS_exit_velocity.md` is unsupported until someone does.

Idealisations, stated because they bound the result: one plate rather than the assembled
box; web attachment as two support lines; load applied as equal nodal forces (total exact,
local distribution approximate); bonded magnets not modelled, which is conservative; static
attraction only, no launch or arrest loads.

## 5. Not run, and why

| Analysis | Status |
|---|---|
| **A1** airgap field, magnetostatic FEA | **RUN 2026-07-29, thrust band met at ratio 1.001.** See section 5. |
| **A4** sled structural | **Run**: see section 4b. Mass computed from CAD solids, stiffness/stress/modal computed. What remains is the optimisation question: the lightest chassis meeting the constraint, which needs a rib-stiffened study. |
| **A6** conjunction P<sub>c</sub> | **Not run.** Needs a covariance that does not exist for an unflown satellite (E18), and the CARA tools are MATLAB. |
| **A7** separation and tip-off | **Not run.** Recorded here as "Project Chrono is not installable", **that verdict is now in doubt**: `pychrono` ships on conda-forge rather than PyPI and lists linux-64, so a failed `pip install` is the likely cause. Retry before treating A7 as blocked. Tip-off remains a model output with no multibody model behind it, and the acceptance band it would be judged against may itself be mis-sourced (`docs/LANDSCAPE.md`). |
| Thermal, contamination, EMC, host stage | Unchanged, E5, E11, E12 stand. |
| Anything at all in hardware | **Nothing has been built, fired, or measured.** E4 stands, and no amount of this changes TRL 2-3. |

---

## Findings

### F1: The Gen3 sled as drawn is 9.45 kg, above both existing estimates, **HIGH**

`mass_properties.py` assumes 4.86 kg. P5 quotes the CAD at ~7.50 kg. Measuring the Gen3
solids gives **9.445 kg**, which drives exit velocity to **16.53 m/s**: below the 17.88 m/s
that P8 already flags as provisional.

A4's pre-declared decision rule says a mass at or above 6.80 kg means "17.88 m/s becomes the
headline and the paper changes materially". The CAD result lands well beyond that
threshold. It does not settle the design question, pocketed plates would weigh less, and
the stiffness constraint is unevaluated, but **whichever way the FEA goes, 20.37 m/s is not
supported by the geometry that currently exists.** Recorded as P15.

### F2: Quoted bank sag is state-of-charge, not terminal voltage, **MEDIUM**

`motor_model.py` computes sag as the capacitor's charge depletion (4.88 %) and models no
ESR. With the 12 mΩ ESR the terminal voltage droops to 86.16 V at end of stroke: a **10.25 %
total sag**, more than double the published figure. The servo-headroom argument behind the
0.027 m/s dispersion claim is stated against the smaller number. Recorded under E17.

Related: ∫I² dt over the shot is 8008 A²s. At 12 mΩ that is 96 J of ESR loss, against the
`Q_esr = 160 J` default in `sizing.py`. The two are consistent only at ~20 mΩ. E17 noted that
160 J had no second number against it; this is the second number.

*(The 12 mΩ itself appears only in `docs/EMOCD_Computation_Results_C1-C10.md`, which is
superseded. No current script defines a bank ESR at all, which is part of the problem.)*

---

## 5. Airgap field: 2-D magnetostatic FEM (A1)

**The most important validation this project has run**, because K<sub>t</sub> = 11.22 N per
kA/m sets exit velocity, efficiency and every downstream astrodynamic number, and until now
it had only ever been checked *analytic against analytic*. The closed-form travelling-wave
model and magpylib both superpose analytic solutions for uniformly magnetised blocks. Neither
solves a field equation.

A1 does. Vector-potential magnetostatics on a triangular mesh (scikit-fem P1, gmsh),
**141 k elements**, 0.6 mm airgap mesh, Az = 0 on a 500 mm box. Geometry and magnetisation
imported from `motor_model.py` so the two cannot describe different machines; sampling windows
copied from `verify_field.py` so they are compared at the same places.

| Quantity | FEM | Reference | Ratio | Band | |
|---|---|---|---|---|---|
| Midgap peak | 0.6947 T | 0.6942 | **1.001** | ±5 % | pass |
| Winding mean \|B\| | 0.5523 T | 0.5518 | **1.001** | ±5 % | pass |
| **Thrust at 140 kA/m** | **1571.9 N** | **1570.8** | **1.001** | **±10 %** | **pass** |
| Stray at 10 mm | 26.3 mT | 22.7 | 1.160 | factor 1.5 | pass |
| Stray at 20 mm | 4.91 mT | 4.3 | 1.142 | factor 1.5 | pass |
| Array-surface peak | 1.4641 T | 0.7714 | 1.898 | ±5 % | **miss, P20** |
| Stray at 50 mm | 0.929 mT | 0.4 | 2.322 | factor 2 | **miss, P21** |

**K<sub>t</sub> = 11.228 N per kA/m against 11.22, and ripple 1.25 % against 1.26 %.** An
independently implemented method (a meshed PDE solve rather than superposition) reproduces
the number every headline in this project descends from, to **0.07 %**.

### Both misses have identified causes, and neither is a model error

**P20, the run sheet's reference was wrong for that row.** The array-surface band was declared
against `analytic_B0_surface_T` = 0.7714 T, the fundamental of a **single** array's wave. Any
measurement at that plane in a double-sided machine includes the opposing array, worth
`B0·exp(-k·GAP)` = 0.160 T there. Correct reference: **0.9317 T**. The FEM's fundamental is
**0.9312 T, ratio 0.9994.** The row failed as declared and the model is right; both are
recorded, and **the band was not widened**: `A1_field_femm.md` stands exactly as written on
2026-07-27, because a run sheet edited after seeing results is worth nothing.

**P21, 2-D cannot test the far field.** The FEM has infinite depth; the array is 90 mm deep.
At 10 and 20 mm the observation distance is small against that and the two agree. At 50 mm it
is comparable, a finite source falls off faster, and 2-D necessarily overestimates. Converged,
not noise: 0.93 mT across boxes from 0.5 to 0.8 m and meshes from 32 k to 141 k elements. The
magpylib reference models finite blocks exactly and is the better number here.

### What was checked before concluding

The run sheet names air-box size as the first suspect on a miss, so it was tested first.
Box 0.20 to 0.80 m moves midgap by 0.2 %, winding by 1.3 %, **K<sub>t</sub> by 0.07 %**: all
converged. Mesh 32 k to 141 k elements moves K<sub>t</sub> by 0.2 %. The stray rows move with
both, which is why their bands were declared loose and why the 50 mm row needed a physical
explanation rather than a numerical one.

Detail: [`validation/results/A1_femm.json`](../validation/results/A1_femm.json). Script:
[`validation/fem/a1_airgap_field.py`](../validation/fem/a1_airgap_field.py).

> **Note on the solver.** The run sheet names FEMM, which is Windows-only and was not
> available. This is a meshed differential-FEM solve of the same 2-D problem, which is what E2
> actually asks for, recorded as what it is rather than presented as FEMM.

## What this changes

*Updated 2026-07-29, after the propagation.*

**The performance claim has been settled, downward.** The headline 20.37 m/s rested on a
4.86 kg sled the drawn geometry does not support. A4 ran, the plate passed all three
structural bands, and the CAD-derived 9.445 kg fell in the decision rule's ≥ 6.80 kg branch, so
`analysis/` moved to **16.537 m/s at 10.7 g**, and the paper and figures followed. This is
the first script value this project has changed, and it was authorised by a rule written
before the analysis that triggered it.

**The astrodynamics claim is half-confirmed and half-broken, and the broken half is worse
than first recorded.** The x1.80 multiplier of the day stood up at mean and high solar
activity under an independently implemented propagator. Its *invariance* did not, and the
ballistic-coefficient half of the same claim is the identical tautology, since `scale` and
`1/BC` occupy the same multiplicative slot in the drag term. Neither half was ever tested by
a method that could fail. The paper nominated that invariance as its defensible result; it no
longer does.

**Three things remain open and are now scheduled rather than merely noted** (`ROADMAP.md`):

1. **A5 still predates the operating point it validates** (P19), having been propagated at
   20.37 m/s. A8 was in the same position and was re-run on 2026-07-30 against fresh bands.
   A4 survives, its load being magnetostatic and velocity-independent, but it is separately
   37 % high (P17). A5 is days of wall time and should not be redone before the chassis
   question is settled, or the staleness simply recurs.
2. **The lightest chassis has never been designed.** A4 answers "does the drawn plate meet
   the constraint" (yes, with 17x stress margin) and not "what is the lightest one that
   does". Until someone evaluates a rib-stiffened redesign, 9.445 kg is the honest number and
   the pocketing rows in `docs/DESIGN_OPTIONS_exit_velocity.md` are unsupported.
3. **The electrical margin is still quoted against a voltage the drive never sees**, and no
   current script defines a bank ESR at all (E17).

The standing rule held throughout: the discrepancy was recorded, the analysis was run, and
only then did anything propagate, once, in the order scripts to figures to paper.
