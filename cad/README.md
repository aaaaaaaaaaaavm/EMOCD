# CAD

Fusion 360 CAD for EMOCD, across nine documents (Track, Stator, Sled, Payload_3U,
Magazine_Cassette, Brake, Interface_ESPA, Enclosure, Assembly).

## What is authoritative here

- **`parameters.json` is the geometry source of truth.** Every dimension lives here, not
  in Fusion (Fusion user parameters are document-scoped and drift silently across the nine
  documents). Change a value here, then regenerate the affected document from script.
- CAD is authoritative for **geometry, fit, and interference only.**
- `analysis/*.py` remains authoritative for **mass and performance.** Fusion-computed
  masses are proxies (solid-copper stator, solid-aluminium CubeSats, steel standing in for
  NdFeB) and are deliberately excluded from `parameters.json`.

## Status (2026-07-23)

First-pass CAD, **no structural or magnetic FEA behind it.** Several values are flagged
`PROVISIONAL_PENDING_FEA` in `parameters.json`. The sled chassis mass (P5), the resulting
exit velocity (P8), the ESPA envelope overrun (P9), and the incomplete mass rollup (P10)
are open — see `../OPEN_PROBLEMS.md`.

## Contents

- `parameters.json` — the 9-group geometry parameter set
- `step/` — STEP exports of every document (durable, diffable-by-metadata; `.f3d` is not)
- `renders/` — exterior, interior, exploded, and firing-sequence PNG renders

The 2-D magnetic cross-section and its FEMM run sheet live in `../analysis/femm/`.
