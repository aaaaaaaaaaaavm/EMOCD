# CAD

Fusion 360 CAD for VOLLEY, across nine documents (Track, Stator, Sled, Payload_3U,
Magazine_Cassette, Brake, Interface_ESPA, Enclosure, Assembly), in **three generations**.

Full generation history, per-file body counts, and the defect list are in
[`CHANGELOG_CAD.md`](CHANGELOG_CAD.md).

## Generations

| Folder | What it is | Status |
|---|---|---|
| `step/gen3/` | Parameter-reconciled revision, plus `EMOCD_Gen3.step`, a monolithic single-file model (395 solids) holding all nine sub-systems. The renders in `renders/` came from it | **CURRENT.** Open problems P5, P12 are indexed against it |
| `step/gen2/` | First structured revision. Mechanism-level detail arrives: single-layer stator, sled Halbach arrays and rollers, magazine escapement and D6 pins, brake ring spring | SUPERSEDED, carries a 360 mm sled chassis where the spec says 488 mm |
| `step/gen1/` | The original CAD, 2021-2025. Structural envelope rather than mechanism model; the geometry `parameters.json` was reverse-engineered from. Includes the pre-split single-file `EMOCD_Deployer_Assembly_Gen1.step` and a second sled revision, `Sled_Gen1b` | SUPERSEDED, heritage only |

Use Gen3 unless you specifically need a heritage comparison.

## What is authoritative here

- **`parameters.json` is the geometry source of truth.** Every dimension lives here, not
  in Fusion (Fusion user parameters are document-scoped and drift silently across the nine
  documents). Change a value here, then regenerate the affected document from script. If
  the CAD and `parameters.json` disagree, `parameters.json` wins and the CAD is wrong.
- CAD is authoritative for **geometry, fit, and interference only.**
- `analysis/*.py` remains authoritative for **mass and performance.** Fusion-computed
  masses are proxies (solid-copper stator, solid-aluminium CubeSats, steel standing in for
  NdFeB) and are deliberately excluded from `parameters.json`. **Never quote a
  Fusion-computed mass.**

## Status (2026-07-28)

First-pass CAD, **no structural or magnetic FEA behind any of it.** Several values are
flagged `PROVISIONAL_PENDING_FEA` in `parameters.json`. Open: the sled chassis mass (P5),
the resulting exit velocity (P8), the ESPA envelope overrun (P9), the incomplete mass
rollup (P10), and the CAD-side geometry defects P14, see `../OPEN_PROBLEMS.md`.

**What changed on 2026-07-28.** The previously committed `step/*.step` set was a
mixed-generation snapshot matching no single generation, and two of its files were stubs:
the stator export contained **one solid** rather than 162 conductors, and the ESPA
interface contained **one solid** rather than a flange ring, hub plate, and four gussets.
It was replaced wholesale by the three audited generations. See `CHANGELOG.md` (CAD2 block)
and `OPEN_PROBLEMS.md` P13.

## Before using any file

1. **Gen3 unless you need heritage.** Gen1 and Gen2 carry known dimensional and mechanism
   defects, listed per file in `CHANGELOG_CAD.md`.
2. **Cross-check every dimension against `parameters.json`** before quoting it.
3. **No Fusion masses.** Mass authority is `analysis/mass_properties.py`, and even that is
   incomplete (P10).
4. **The sled mass conflict is resolved (2026-07-29).** The scripts now carry the measured 9.445 kg and the headline is 16.54 m/s. Historical note follows: 20.37 m/s assumed a 4.86 kg sled; the Gen3
   geometry implies ~7.50 kg and a provisional 17.88 m/s. Quote neither without the
   conflict (P5, P8). `validation/A4_sled_structural.md` is the analysis that settles it.
5. **The ESPA envelope claim is not supported.** 1839 mm installed against a ~1270 mm class
   limit, ~44 % over (P9), and the paper still asserts compatibility (P12).
6. **The stator layer count is an open design decision.** Gen1 built two layers, Gen2 and
   Gen3 one, and `parameters.json` flags it open. The electromagnetic consequence, roughly
   x2 force for the same current against x2 copper mass and winding complexity, has never
   been computed (P14).

## Contents

- `parameters.json`, the 9-group geometry parameter set, source of truth
- `CHANGELOG_CAD.md`, generation history, per-file inventories, defect IDs (G1-D*, G2-D*,
  G3-D*), and the cross-generation comparison
- `step/gen1/`, `step/gen2/`, `step/gen3/`, STEP exports (`.f3d` is not diffable, so STEP
  is what gets committed)
- `renders/`, exterior, interior, exploded, and firing-sequence PNGs, from the Gen3
  monolithic model

The 2-D magnetic cross-section and its FEMM run sheet live in `../analysis/femm/`.
