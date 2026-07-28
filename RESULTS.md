# Results, in charts

Everything here is drawn by GitHub from text — no image files. Every value traces to a
field in `analysis/results/*.json`, named under each chart, and nothing has been rounded
in a direction that flatters it.

**These are model outputs.** Nothing in this file has been measured, and only two results
carry an independent cross-check. See [`PROVENANCE.md`](PROVENANCE.md).

---

## Where the energy goes

2630 J leaves the capacitor bank per shot. 830 J of it ends up as payload kinetic energy —
that is the 32 % figure, and it is electrical-to-payload with **no regeneration credit**,
because the sled's 1008 J is dissipated in the eddy brake by design.

```mermaid
pie showData
    title Energy per shot (J) — sizing.py energy_closure
    "Sled KE, dissipated in the brake" : 1008
    "Payload KE, the useful output" : 830
    "Copper loss" : 672
    "Converter loss" : 97
    "Auxiliary" : 26
```

Accounted 2633 J against 2630 J drawn — 100.1 % closure, which is the arithmetic check that
the budget has no missing term. Source: `analysis/results/sizing.json` → `energy_closure`.

An earlier version of this project claimed 52 % efficiency by crediting 55 % of the sled's
energy back as regeneration. That was double-counting: the arrest architecture throws that
energy away. The correction to 32 % is recorded as A25/A27 in
[`INVENTORY.md`](INVENTORY.md).

---

## Why the conjunction claim was reframed

This is the most instructive chart in the repository. It plots the 30-day minimum
satellite-to-stage approach distance against ejection velocity.

```mermaid
xychart-beta
    title "Minimum approach vs ejection velocity — the quantity is not robust"
    x-axis "Ejection velocity (m/s)" [20.00, 20.37, 20.50, 20.65, 21.00]
    y-axis "Minimum approach (km)" 0 --> 70
    line [37.5, 4.6, 56.1, 45.3, 63.4]
```

A ±2.5 % change in velocity moves the answer by more than an order of magnitude, from
4.6 km to 63.4 km. It is a near-resonant beat sample, not a design property. The paper
originally quoted a single figure — 45.3 km — as a safety result. It now rests on the
**8.1-day phase realignment period**, which is robust, plus mandatory per-shot collision
avoidance and host-stage disposal before first realignment.

Source: the P1 sweep table in [`OPEN_PROBLEMS.md`](OPEN_PROBLEMS.md), computed by
`analysis/astro.py` `conjunction()`. `validation/A6_conjunction_cara.md` specifies the
quantitative replacement — probability of collision, which integrates over the covariance
instead of sampling one geometry.

---

## Payload family

Exit velocity is force-limited, so heavier classes go slower at lower acceleration. Only
the 3U case is designed; 6U and 12U are arithmetic from the same thrust constant, with no
mechanism or cassette behind them (`OPEN_PROBLEMS.md` E9).

```mermaid
xychart-beta
    title "Exit velocity by payload class (m/s)"
    x-axis ["1U", "3U", "6U", "12U"]
    y-axis "Exit velocity (m/s)" 0 --> 30
    bar [24.4, 20.4, 16.9, 14.8]
```

```mermaid
xychart-beta
    title "Acceleration on the satellite (g) — 25 g qualification limit"
    x-axis ["1U", "3U", "6U", "12U"]
    y-axis "Acceleration (g)" 0 --> 25
    bar [23.4, 16.3, 11.2, 8.5]
```

The 1U case at 23.4 g sits close to the 25 g limit that standard qualification testing
assumes — the ceiling is the payload's tolerance, not the motor. Source:
`analysis/results/motor_results.json` → `family`.

---

## Seeding: the actual value proposition

Time to spread a constellation 30° apart, by ejection velocity, against the
differential-drag baseline.

```mermaid
xychart-beta
    title "Days to 30 degrees of phase separation"
    x-axis ["EMOCD 10 m/s", "EMOCD 5 m/s", "EMOCD 2 m/s", "Differential drag"]
    y-axis "Days" 0 --> 28
    bar [1.4, 2.8, 6.9, 25.0]
```

Source: `analysis/results/astro_results.json` → `seeding_days`. **Caveat worth reading:**
the 25-day comparator is a model output of `astro.py`, not a measurement. Foster et al.
published *flown* differential-drag phasing results for 12 Planet Labs CubeSats at 510 km;
replacing the modelled baseline with the measured one is the cheapest credibility
improvement available to this project (`docs/RELATED_WORK.md`).

---

## Stray field falloff

Sets the magnetic keep-out for satellites still in the cassettes.

```mermaid
xychart-beta
    title "Stray field behind the array back face (mT)"
    x-axis "Distance (mm)" [10, 20, 50]
    y-axis "Field (mT)" 0 --> 25
    line [22.7, 4.3, 0.4]
```

Source: `analysis/results/field_verification.json` → `stray_field`. The 20 mm and 50 mm
values were wrong in the published paper (4.7 and 1.0 mT) and were corrected against the
script — P3, logged in [`CHANGELOG.md`](CHANGELOG.md) as P2-03. Far-field values are small
differences of large numbers and remain the least trustworthy row here.

---

## The sled mass conflict, and how it gets settled

Two estimates of the same part disagree by 54 %, and the headline exit velocity hangs off
which one is right.

```mermaid
xychart-beta
    title "Sled mass estimates (kg) against the A4 decision thresholds"
    x-axis ["Parametric (scripts)", "A4 lower bound", "A4 upper bound", "CAD geometry"]
    y-axis "Mass (kg)" 0 --> 8
    bar [4.86, 5.35, 6.80, 7.50]
```

The two middle bars are **not measurements** — they are the decision rule declared in
[`validation/A4_sled_structural.md`](validation/A4_sled_structural.md) before the analysis
runs:

| Outcome | Consequence |
|---|---|
| ≤ 5.35 kg | Parametric model stands. 20.37 m/s holds, P5 and P8 close |
| 5.35 – 6.80 kg | Neither estimate right. Scripts move, then the paper |
| ≥ 6.80 kg | **17.88 m/s becomes the headline** and the paper changes materially |

Fixing the thresholds in advance is the point. After the run, the temptation will be to
pick whichever threshold preserves 20.37 m/s.

---

## Validation status

```mermaid
flowchart LR
    subgraph SPEC["Specified, not run"]
        A1["A1 · FEMM<br/>airgap field"]
        A4["A4 · CalculiX<br/>sled chassis"]
        A6["A6 · NASA CARA<br/>conjunction Pc"]
        A7["A7 · Chrono<br/>separation, tip-off"]
        A8["A8 · ngspice<br/>pulse power"]
    end
    subgraph RUN["Run - GMAT R2022a"]
        A5["A5 · GMAT<br/>lifetime, seeding"]
    end
    A1 --> E1["E1 · 3-D field closure"]
    A1 --> E2["E2 · no FEA of anything"]
    A4 --> P5["P5 · sled mass"]
    A4 --> P8["P8 · exit velocity"]
    A5 --> E6["E6 · absolute lifetimes"]
    A6 --> P1["P1 · conjunction claim"]
    A7 --> E7["E7 · dispersion assumptions"]
    A8 --> E17["E17 · pulse chain unmodelled"]
```

Six analyses, each with its acceptance band declared before the run. Progress so far:

| Analysis | Status |
|---|---|
| A1 airgap field | `░░░░░░░░░░` specified |
| A4 sled chassis | `███░░░░░░░` mass measured (**9.45 kg**, P15); stiffness not run |
| A5 lifetime & seeding | `████████░░` **GMAT: ×1.73 vs ×1.80, within band** (high activity); mean/low running |
| A6 conjunction Pc | `░░░░░░░░░░` specified |
| A7 separation & tip-off | `░░░░░░░░░░` specified |
| A8 pulse-power chain | `██████████` **run — ngspice, all bands met, 2 findings** |

## GMAT cross-check (A5) — first real validation output

GMAT R2022a was installed and run headless. This is the first number in this project
produced by something other than its own scripts.

### Decay rate over a bounded 30-day window

```mermaid
xychart-beta
    title "Baseline orbit semi-major axis, GMAT vs astro.py (km)"
    x-axis "Days from epoch" [0, 5, 10, 15, 20, 25, 30]
    y-axis "Semi-major axis (km)" 6810 --> 6832
    line [6828.14, 6823.25, 6815.45, 6817.31, 6825.00, 6819.62, 6812.58]
    line [6828.14, 6827.54, 6826.95, 6826.34, 6825.73, 6825.11, 6824.49]
```

First line GMAT, second `astro.py`. The GMAT curve wanders because **reported SMA is
osculating** — short-period J2 and lunisolar terms run 12.2 km peak to peak here, several
times the decay over the whole window. `astro.py` integrates mean elements, so its curve is
smooth. Differencing the endpoints of the two would be meaningless; the honest comparison is
the fitted rate:

| | Decay rate | Method |
|---|---|---|
| GMAT | **−0.1618 km/day** | least squares over 31 daily samples, residual RMS 4.24 km |
| `astro.py` | **−0.1216 km/day** | 30-day Cowell integration, `cowell_sma_after()` |
| Ratio | **1.33×** | GMAT decays faster |

**A 33 % difference in absolute decay rate is not a failure**, and E6 says so in advance:
`astro.py` uses a static exponential atmosphere at "mean activity" while GMAT uses MSISE90
at F10.7 = 150, and those are not the same thing. The claim this project defends is the
ratio between boosted and unboosted lifetimes, not the years.

An internal consistency check fell out of it: a 1.33× faster decay predicts the
high-activity case reaching 120 km at 190 / 1.33 ≈ 143 days. GMAT's full run gives
**144.5 days**. The bounded window and the full decay agree with each other.

### Full decay runs — the ×1.80 claim, checked

High solar activity (F10.7 = 250), propagated to the 120 km floor:

```mermaid
xychart-beta
    title "Lifetime multiplier: does the boost buy 1.8x? (high activity)"
    x-axis ["astro.py claim", "GMAT R2022a", "band lower", "band upper"]
    y-axis "Multiplier" 1.5 --> 2.0
    bar [1.80, 1.73, 1.71, 1.89]
```

| | Baseline | Boosted | Multiplier |
|---|---|---|---|
| GMAT R2022a, MSISE90 | 144.5 days | 250.0 days | **1.7302** |
| `astro.py` | 190 days (0.52 yr) | — | 1.80 |
| | | Deviation | **−3.88 %** |

**Inside the ±5 % band declared before the run.** An independently implemented force model —
different atmosphere, 20×20 gravity, lunisolar third bodies, SRP, RK89 — reproduces the
project's headline astrodynamics claim to within 4 %.

Note what did *not* agree: the absolute baseline lifetime, 144.5 days against 190. That is
the 1.33× rate difference again, and E6 predicted it in advance. The ratio survives what the
absolutes do not, which is the entire argument for quoting the ratio.

Mean and low activity are still propagating (2.6 years of orbit at low activity takes a
while). Live verdict, force models and run metadata:
[`validation/results/A5_astro.json`](validation/results/A5_astro.json).

> **The parser earned its keep here.** Its first run read a decay file GMAT was still
> writing, took the partial decay as final, and produced a confident `FAIL`. It now refuses
> to report a multiplier unless the run actually reached the 120 km floor. A validation
> harness that reports a failure it cannot substantiate is worse than no harness.
