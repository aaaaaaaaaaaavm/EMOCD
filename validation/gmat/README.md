# GMAT toolkit (analysis A5, and the ephemeris input for A6)

Generates GMAT mission scripts from the values already committed in `analysis/`, runs
them headless, and parses the output into `validation/results/A5_astro.json` against the
bands declared in `../A5_astro_orekit.md`.

**Nothing here has been run.** These are inputs and a parser; there is no result yet.

## Why GMAT

`analysis/astro.py` uses a static exponential atmosphere, J2-only secular propagation, and
its own RK4 Cowell integrator. Its "cross-check" is that script checking itself. GMAT
brings independently implemented force models — MSISE-class atmosphere, spherical-harmonic
gravity, RK89 — and is the external propagator `astro.py`'s own docstring says it has never
been checked against.

It closes **E6** and feeds **A6**. It does nothing for P5/P8 or E4: it validates the
consequences of a Δv, never the Δv itself.

## Install and invocation

GMAT is a NASA open-source release (Apache-2.0). Download the binary for your platform;
do **not** vendor it into this repository — commit inputs and outputs only.

```bash
python3 build_scripts.py            # fills the templates; works with no GMAT installed
<gmat-console-binary> -r output/emocd_lifetime_mean.script
python3 parse_reports.py            # -> ../results/A5_astro.json
```

**Verify the headless flags against the User Guide shipped with your GMAT build before
relying on them.** The console executable and its run/exit switches have changed across
releases, and the wrong flag silently opens the GUI instead of running the mission. Record
the exact command that worked in `../results/A5_astro.json` (`invocation` field).

Pin the version: GMAT's force-model defaults have moved between releases, so a result
without a version string is not reproducible.

## Files

| File | What it is |
|---|---|
| `emocd_lifetime.script.tmpl` | Baseline vs boosted orbit, propagated to 120 km perigee or a 40-year cap. One filled script per solar-activity level |
| `emocd_fleet.script.tmpl` | 12 shots at 1200 s spacing plus the host stage, 30 days, one CCSDS OEM per object — the A6 input |
| `build_scripts.py` | Fills both templates. Imports `boosted_elements()` and `_kepE()` from `analysis/astro.py` so the orbit definition cannot fork |
| `parse_reports.py` | GMAT `ReportFile` / OEM → `../results/A5_astro.json`, with pass/fail against the declared bands |

Placeholders are `@@NAME@@`, not `{NAME}` — GMAT's `Propagate` syntax uses braces.

## Rules

1. **GMAT output never edits `analysis/*.py`.** A disagreement opens a P-item; the scripts
   stay authoritative until the cause is understood. This is ground rule 3 in
   `docs/PROJECT_NOTES.md`.
2. **The bands are already declared** in `../A5_astro_orekit.md`. Do not restate or widen
   them here after seeing output.
3. **Absolute lifetimes will differ** from `astro.py`'s 2.61 / 1.30 / 0.52 yr, possibly by a
   factor of two, because an exponential table is not MSIS. That is expected and is not a
   failure. E6 defends the ×1.80 ratio, not the years.

## Known modelling gap between the two codes

`astro.py` scales *density* by 0.5 / 1.0 / 2.5 for low / mean / high activity. GMAT takes
*solar flux* (F10.7, F10.7A, Kp) instead, and the relationship between the two is neither
linear nor one-to-one. The filled scripts use F10.7 = 70 / 150 / 250 as the conventional
low / mean / high proxies, which is **not** equivalent to the density scaling.

This matters for the absolute lifetimes and not for the claim: the invariance band is on
the *spread of the multiplier* across activity levels, which should hold under either
parameterisation. If it does not, that is a real finding about the ×1.80 and belongs in a
P-item.

> **Outcome (2026-07-28): it did not hold, and the P-item is `OPEN_PROBLEMS.md` P16.**
> Spread 18.48 % against the ≤5 % band. The paragraph above is left exactly as written
> before the run — it is the record of what was expected, and the fact that the failure mode
> it names in advance is the one that occurred is the reason the run sheet was written first.


