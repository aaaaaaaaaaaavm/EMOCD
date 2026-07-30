# Manufacturability

The Engineering Programme Dossier names manufacturability three times, in the Phase I focus
list, in the philosophy (*"manufacturability over elegance"*), and in the validation chain.
Until 2026-07-29 this repository contained none. This document opens it.

**Status: analysis only.** Nothing has been quoted, no vendor has been approached, and no part
has been made. Every price and process tolerance below is an **assumption**, marked as such
under E16, exactly like `analysis/cost.py`.

---

## 1. The airgap tolerance stack: the finding

`sizing.py` declares a single `gap_shim_tolerance = 0.05 mm` against a thrust sensitivity of
**13.1 %/mm**, and reports a resulting spread of ±0.65 %. **That figure counts only the shim.
It does not count the parts.**

Three separate budgets were being conflated. Separated:

| # | Budget | Value | Status |
|---|---|---|---|
| 1 | Physical clearance per side | **1.000 mm** | `parameters.json` `sled.airgap_per_side` |
| 2 | A4 deflection band per plate | 0.025 mm | measured 0.0194, **78 % used** |
| 3 | Shim **setting** spec | ±0.050 mm | to ±0.66 % thrust |
| 4 | **Build stack** | **never computed** | below |

### The build stack

| Contributor | Assumed (mm) | Note |
|---|---|---|
| Track straightness over 1.8 m | 0.060 | **Dominant.** A 1.8 m extruded/machined Al assembly |
| Ti plate flatness over 488 mm | 0.050 | Post-machining, pre-shim |
| Roller / rail radial clearance | 0.040 | Bearing fit plus rail form |
| Magnet block thickness tolerance | 0.030 | Sintered NdFeB, ground faces |
| Chassis web height tolerance | 0.030 | |
| Bond line thickness variation | 0.020 | Adhesive under 12 blocks |
| Shim setting | 0.020 | The only term currently counted |
| **RSS** | **0.101** | to **1.33 % thrust** |

Combined with A4's deflection bias (0.0194 mm, always closing) the total gap error is
**0.121 mm, 2.4x the ±0.65 % currently claimed, giving ±1.58 % thrust spread.**

### What this does and does not mean

**It is not a contact risk.** 0.121 mm against 1.000 mm of clearance is 12 %; nothing touches.

**It is a claims problem.** ±1.58 % thrust spread propagates into the open-loop velocity
spread, which the paper states as ±2.1 % RSS from manufacturing terms. That figure was built
from magnet grade, gap, resistance and ESR, **with the gap term taken as the ±0.05 mm shim
rather than the real stack.** The closed-loop servo collapses delivered dispersion regardless
(ADR-014), so the headline 0.027 m/s survives. But the open-loop number is optimistic and
should be restated once these contributors are replaced with real ones.

**The individual values above are assumed.** The useful output is the ranking: **track
straightness and plate flatness dominate**, and no amount of shim precision fixes either.
Tightening the shim spec is the intuitive move and it is nearly worthless.

> **Not propagated.** Per `BASELINE.md` change control this is a discrepancy, not yet a
> correction, the contributors are assumptions, and replacing a real number with an assumed
> one is not an improvement. Closure needs a real tolerance study against quoted process
> capability. **Do not edit `sizing.py` on the strength of this section.**

## 2. Halbach assembly: the hazardous operation

`analysis/cost.py` puts the magnet set at only ~5 % of recurring cost. **It is far more than
5 % of the risk.**

Each array is 12 blocks of N45SH in alternating orientation, and the two opposed arrays attract
across the gap with **2.69 kN** (P17's corrected 3-D figure; the flat-plate formula says 3.67).
That is roughly 274 kgf trying to close a 12 mm gap, acting on brittle sintered material with
essentially no tensile strength.

Process implications, none of which are in the CAD:

- **Assembly fixture must be non-magnetic and must control the gap throughout closure**, not
  only at the end. There is no intermediate state where the halves are "nearly together" and
  safe.
- **A controlled-approach mechanism is required**, screw-driven or similar. Free approach ends
  in an impact between two brittle arrays.
- **Keep-out during assembly.** 2.69 kN closing on a hand is a serious injury.
- **Magnetisation order.** Magnetise-then-assemble is standard for Halbach arrays but makes
  every handling step hazardous; assemble-then-magnetise needs equipment most shops lack.
  **Not yet decided, and it changes the fixture completely.**
- **Bond cure under load**: the bond line is a stack contributor (§1) and cures while the
  attraction is trying to squeeze it.

**This is the single largest manufacturability unknown in the project**, and it is not
represented in cost, schedule, or the qualification plan beyond T-3's magnet-integrity check.

## 3. Make versus buy

Driven by `analysis/cost.py`, whose sensitivity table is the relevant output:

| Item | Share | Recommendation |
|---|---|---|
| Avionics, sequencer, IMU | 23.7 % | **Buy.** Nothing here is VOLLEY-specific |
| Supercapacitor bank | 17.8 % | **Buy** cells, make the pack, cell selection is commodity, the pack is not |
| SiC bridge + gate drive | 13.3 % | **Buy** the modules, make the busbar |
| Halbach arrays | ~5 % | **Buy magnetised blocks, assemble in-house**: see §2 |
| Ti chassis, track longerons | ~11 % | **Make** (subcontract machining). This is where DFM effort pays |
| Bearings, rails | 5.2 % | **Buy.** Vacuum-rated hybrid ceramics are catalogue items |

**The strategic point:** the project's cost and risk both concentrate in electronics and
assembly process, not in the electromagnetics the design effort has gone into.

## 4. DFM review of the Gen3 parts

| Part | Observation | Action |
|---|---|---|
| Chassis plate 488x140x6 | Drawn **solid**. A4 gives a 17x stress margin, so this is not a structural part, it is a stiffness part carrying dead mass | Pocketing is PII-2. Do not thin uniformly: deflection goes as 1/t³ |
| Track longerons, 1.8 m | Straightness dominates the tolerance stack (§1) | Specify straightness explicitly. It is currently unspecified anywhere |
| Halbach blocks | 12 per array, alternating orientation | Orientation-proof fixturing. A reversed block is invisible on inspection and destroys K<sub>t</sub> |
| Roller channels, guide flanges | **G3-D2: not modelled at all.** The rollers have nothing to run in | Blocking for any real build |
| Halbach array position | **G3-D5: not re-centred** after the chassis grew 360 to 488 mm | Array-to-winding position is what K<sub>t</sub> depends on. **Blocking, and it may invalidate K<sub>t</sub> independently of A1** |

## 5. Process route

```
Buy magnetised N45SH blocks  ──┐
Machine Ti chassis + webs  ────┼──> Bond arrays in controlled-approach fixture ──┐
Machine Al track longerons ────┘         (§2 — hazardous operation)              │
                                                                                 v
Wind stator on formers ──> pot ──> verify per-phase resistance ──> Integrate ──> Shim gap
                                                                                 │
                        Inspect: gap map, K_t on a load cell (B-2) <─────────────┘
```

**Inspection points that do not currently exist:** a gap map along the full 1.3 m stroke rather
than a single measurement, and a K<sub>t</sub> check on the built article. Both are in
`docs/BENCHTOP_TESTS.md` as B-1 and B-2 at sub-scale.

## 6. What would close this

1. **Real tolerance data.** Quote the seven contributors in §1 against actual process
   capability. Until then §1 is structure, not a number.
2. **A decision on magnetisation order** (§2). It changes the fixture, the hazard case and the
   schedule.
3. **G3-D2 and G3-D5** (§4). Both are blocking for a build and G3-D5 may move K<sub>t</sub>.
4. **One quotation**: any line item. `cost.py` currently has zero real prices, and a single
   quote would tell us whether the model is out by 20 % or by 200 %.

## Where this sits in the validation chain

Dossier §7: Concept to Analysis to **Simulation** to Prototype to Experiment to Repeatability to **Manufacturability** to Flight Qualification.

The project sits at Simulation. This document is the **first entry on the manufacturability
rung**, and it is analysis about manufacturing rather than manufacturing evidence. The rung is
opened, not climbed.
