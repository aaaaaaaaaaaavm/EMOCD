# VOLLEY: Computation Results C1, C10

> **SUPERSEDED (marked 2026-07-27). Do not cite any number in this file.** It records the
> C1, C10 computations at an operating point that no longer exists, a 4 kg sled at
> K = 45 kA/m, and it predates both the winding-resolved motor model (A28) and the
> efficiency correction (A27). Current values live in `analysis/results/*.json` and the
> README headline table. Kept for the audit trail, as the P-items are.
>
> | Quantity | This file | Current | Why it moved |
> |---|---|---|---|
> | Exit velocity, 3U | 22.4 m/s at 19.7 g | **20.37 m/s at 16.3 g** | winding-resolved Kt (A28), 4.86 kg sled |
> | Sled mass | 4 kg | **4.86 kg** parametric (7.50 kg in CAD, P5) | `mass_properties.py` |
> | Winding mean field | ⟨B⟩ ≈ 0.62 T | **0.552 T** | winding-resolved model |
> | Peak current | 463 A | **392 A** | rated point moved to 140 kA/m |
> | Closed-loop 3σ | 0.054 m/s to ±0.19 km | **0.027 m/s to ±0.10 km** | servo Monte Carlo (A29) |
> | Efficiency | 52 %, crediting 55 % regen | **32 %, no regen credit** | see below |
>
> **The efficiency line is not merely stale, it is the falsified claim.** Crediting 55 %
> of the sled's kinetic energy as regeneration was double-counting: the arrest
> architecture dissipates that energy in the eddy brake by design. Recorded as A25/A27 in
> `INVENTORY.md` and in `docs/DECISION_LOG.md`. The C10 payload-family table below is
> superseded by the family table in `analysis/results/motor_results.json`.

All values computed numerically (Python). SI units. Baseline configuration: ironless double-sided Halbach LSM, 4 kg reusable sled, 1.5 m track (1.3 m acceleration zone + 0.2 m coast-trim zone), 12x 3U/4 kg manifest, PS4/POEM host at ~450 km, 51.6°.

---

## C1: Orbital lifetime gain (the value-proposition number)

Method: per-revolution orbit-averaged decay (Gauss tangential equations, quadrature over eccentric anomaly), static exponential atmosphere (Vallado Table 8-4 class, mean activity). **Model limitation: absolute lifetimes swing ~3-10x with solar cycle; the *ratio* is the robust result** (density-scale factors largely cancel).

| Fire alt (km) | Δv (m/s) | Apogee (km) | Lifetime ratio vs circular |
|---|---|---|---|
| 350 | 15 / 25 | 403 / 438 | **1.62-1.68x / 2.15-2.21x** |
| 400 | 15 / 25 | 453 / 489 | **1.59-1.61x / 2.09-2.11x** |
| 450 | 15 / 25 | 504 / 540 | **1.55-1.56x / 2.01-2.03x** |
| 500 | 15 / 25 | 554 / 591 | **1.54x / 1.99x** |

(Sweep over BC = 40/61/90 kg·m⁻²; ratio nearly invariant to BC and altitude.)
**Headline: one 25 m/s shot ≈ 2.0x orbital lifetime, robust across altitude, ballistic coefficient, and drag-model uncertainty.** Absolute example (BC=61): 450 km circular 1.30 yr to 450x540 km 2.64 yr.

## C2: Drift seeding vs differential drag (the killer-app number)

Along-track drift at 450-500 km per ejection-velocity split between adjacent satellites:

| Δ(Δv) between sats | Δa | Drift rate | Time to 30° spacing |
|---|---|---|---|
| 2 m/s | 3.6 km | 518 km/day (4.3°/day) | **6.9 days** |
| 5 m/s | 8.9 km | 1,296 km/day (10.9°/day) | **2.8 days** |
| 10 m/s | 17.9 km | 2,592 km/day (21.7°/day) | **1.4 days** |

Comparison anchor: Foster et al. (JSR 2018) phase propulsion-less constellations by differential drag over campaign timescales of weeks, months. **VOLLEY seeds equivalent relative motion in days with single-digit m/s splits; hybrid ConOps = VOLLEY seeds, drag trims/freezes.**

## C3: Electromagnetic shot model (the missing-evidence simulation)

Halbach: Br=1.30 T (N45SH), 8 mm magnets, λ=48 mm, 4 segments/λ to B₀=0.760 T surface; two-sided effective ⟨B⟩≈0.62 T across a 12 mm winding gap. Active area 0.061 m² (both faces, 0.34x0.09 m) at K=45 kA/m (adiabatic pulse) to **F_max = 1,717 N**.

Shot ODE (supercap bank 6 F / 96 V / 12 mΩ, force-command 90% F_max, drive η=0.82):
- **Exit velocity 22.4 m/s at 19.7 g on the satellite** (limit 25 g), pulse 125 ms
- Peak current 463 A; **bank sag 96 to 91.6 V (4.6%)**: comfortably inside servo headroom
- Energy drawn 2.47 kJ; payload KE 1.00 kJ; sled KE 1.00 kJ; regen credit (55% of sled KE) to **net 1.92 kJ/shot, 52% end-to-end efficiency**
- Coil adiabatic ΔT = 0.02 K/shot at 6 A/mm², thermally negligible per shot
- Monte Carlo (B ±3%σ-scaled, mass, ESR, force ripple; N=4000): open-loop 3σ = 0.47 m/s (2.1%); **closed-loop (encoder servo + coast-trim) 3σ = 0.054 m/s (0.24%)**

## C4: Eddy-current brake

F = σ·t·B²·A·v (first-order plate drag), Cu fin 4 mm, B=0.85 T:
- Authority is abundant: even 80 cm² pole to 30 kN peak at 22.4 m/s, stop in ~6 cm. **Design is therefore taper-limited, not authority-limited: taper pole entry to cap sled decel ≈200 g (protects sintered NdFeB bonding), stop in ~15-25 cm.**
- Fin (0.86 kg Cu) absorbs ~1.0 kJ/shot to **ΔT = 3.0 K/shot**; radiates between shots. Contactless to cycle life not a limiter.
- Ring-spring catches residual ≤1.5 m/s (≈4.5 J, trivial).

## C5: Conjunction screening (30 days, Kepler + secular J2, 5 s sampling)

Scenario: 12 prograde 25 m/s shots, 20 min apart, from 450 km/51.6° stage. Period difference 55.7 s/orbit to **along-track phase realignment ≈101 orbits ≈ 6.6 days**.
- Min satellite, stage distance (excluding 1 h post-release): **61.9 km** (median 69.4 km)
- Min satellite, satellite distance: **5.8 km**
- With stage disposal at day 2 (before first realignment): min pre-disposal approach **347.5 km**
**Safety case: time-staggered firing + prompt stage disposal keeps all approaches in the tens-to-hundreds of km. Screening-level (5 s sampling bounds, does not resolve, sub-km events); full COLA per shot remains a mission product.**

## C6: PS4/POEM attitude budget (parametric; PS4 mass stated as class range, not spec)

Per shot J = 4 kg x 22.4 m/s = 89.6 N·s (satellite momentum only, sled momentum recovered through brake):

| PS4-class mass | ΔV/shot | 12-shot cumulative |
|---|---|---|
| 900 kg | 100 mm/s | 1.19 m/s |
| 1,100 kg | 81 mm/s | 0.98 m/s |
| 1,300 kg | 69 mm/s | 0.83 m/s |

Torque null via He cold-gas (10 N class, 1.2 m arm, Isp≈160 s): residual thrust-line arm 5-15 cm to **2.4-7.1 g of helium per shot; 29-86 g for the whole campaign.** Cumulative translation folds into disposal targeting.

## C7: Tip-off error budget (3U, I_t = 0.042 kg·m²)

| Contributor | ΔL (mN·m·s) | Rate |
|---|---|---|
| Residual trim force 10 N x 5 mm CoM x 20 ms | 1.00 | 1.36 °/s |
| Rail-clearance couple in coast (2 N x 10 mm x 50 ms) | 1.00 | 1.36 °/s |
| Guide spring-back at release (estimate) | 0.80 | 1.09 °/s |
| Sled rate residual (0.05 °/s servo) | 0.04 | 0.05 °/s |
| **Worst-case sum** | | **3.9 °/s** |

Meets the NRCSD-class ≤5 °/s/axis requirement; near the ≤2 °/s target with RSS combination. The coast-trim release zone is what makes this possible, at full force the first line alone would be ~34 °/s.

## C8: System rollups

- **Battery:** 12 shots x 2.5 kJ = 30 kJ (8.3 Wh) + ~4 h avionics at 60 W = 250 Wh to **~1.7 kg Li-ion**; POEM solar available for recharge in hosted mode.
- **Thermal:** campaign losses ≈23 kJ over 4 h ≈ 2 W average, radiator requirement negligible (<0.05 m²); driven by transient local ΔT, not steady state.
- **Mass:** structure 27 + stator 36 + sled 4 + brake 3 + cassettes 9 + supercap/PPU 12 + thermal 6 + avionics/battery 8 = **~105 kg dry, ~153 kg loaded** (12x4 kg). ESPA Grande allocation 320-465 kg to >2x margin. (Estimates pending CAD; flagged.)

## C9: Velocity error to orbit error (450 km, 22.4 m/s)

| Velocity error | Apogee error |
|---|---|
| 0.1% (0.022 m/s) | 0.08 km |
| 0.25% (0.056 m/s) | 0.20 km |
| 0.5% (0.112 m/s) | 0.40 km |
| 1.0% (0.224 m/s) | 0.80 km |

**At the measured closed-loop 3σ (0.054 m/s): apogee placement/knowledge ≈ ±0.19 km.** Sub-kilometer deterministic orbit placement for a propulsion-less satellite.

## C10: Payload family (F=1,545 N commanded, 4 kg sled, 1.3 m accel zone)

| Payload | Accel on sat | Exit velocity | Limit |
|---|---|---|---|
| 1U (1.3 kg) | 29.7 g | 27.5 m/s | force |
| 3U (4 kg) | 19.7 g | 22.4 m/s | force |
| 6U (8 kg) | 13.1 g | 18.3 m/s | force |
| 12U (12 kg) | 9.8 g | 15.8 m/s | force |

Every class stays under 25-30 g qual loads; heavier payloads trade velocity, not safety. (Interesting inversion vs the old coilgun concept: the system is now force-limited, not g-limited, for everything above 1U.)

---

### The paper's quantitative spine, in one paragraph
A 153 kg ESPA-Grande-class linear-motor deployer ejects twelve unmodified 3U CubeSats at 22.4 m/s (19.7 g, within standard qual), each shot drawing a net 1.92 kJ at 52% efficiency from a 6 F/96 V supercapacitor bank sagging only 4.6%, with closed-loop velocity dispersion of ±0.054 m/s (3σ) mapping to ±0.19 km apogee placement and ≤3.9 °/s worst-case tip-off. Each shot doubles a propulsion-less satellite's orbital lifetime (2.0x, invariant across BC and altitude) or seeds 30° constellation spacing in 1.4-6.9 days versus weeks, months for differential drag. Recoil costs the PS4-class host ~90 N·s per shot (≈0.1 m/s), nulled by 2-7 g of cold gas, with 30-day minimum conjunction distances of 62 km (satellite, stage) and 5.8 km (satellite, satellite) under time-staggered firing, rising to 348 km with day-2 stage disposal.

### Honest caveats to carry into the paper
1. Lifetime absolutes depend on solar activity (static mean-activity model used); ratios are the defensible claim.
2. C3 uses a surface-current motor model and lumped drive efficiency; FEA refinement will move F_max by tens of percent, the design margin (90% command, 25 g cap at 19.7 g) absorbs this.
3. C4's plate-drag formula is first-order; pole-geometry factor <1 expected, irrelevant to the conclusion given 20x authority margin.
4. C5 is screening-level (5 s sampling); per-shot COLA remains an operational product.
5. C6 PS4 mass is a class range, not an ISRO spec; cite as parametric.
6. C8 masses are pre-CAD estimates and labeled as such.
