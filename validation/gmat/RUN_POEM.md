# Running the A15 POEM campaign in GMAT

The scripts are generated and cross-checked here. **GMAT is not installed in the environment
this repository is developed in**, so the run happens on your machine and the reports come back.
Until they do, `validation/A15_poem_campaign.md` says *generated and cross-checked, not
executed*, and A15 must not be described as a run.

## 1. Regenerate, if anything upstream changed

```bash
python3 validation/gmat/build_poem_campaign.py
```

Reads `analysis/results/motor_results.json` for Δv and imports `analysis/astro.py` for the orbit
definition, so the scripts cannot drift from the operating point. Writes three scripts to
`validation/gmat/output/` and the cross-check to `validation/results/A15_poem_campaign.json`.

It fails loudly on any unfilled `@@PLACEHOLDER@@` rather than emitting a broken script.

## 2. Run each case

```bash
cd validation/gmat/output
GMAT -m -r a15_poem_r1.script      # 450 km / 51.6  -- the case the bands are set against
GMAT -m -r a15_poem_r2.script      # 350 km / 55.2  -- POEM-4-like, UNVERIFIED
GMAT -m -r a15_poem_r3.script      # 350 km /  9.6  -- POEM-3-like, UNVERIFIED
```

`-m` is minimise-the-GUI, `-r` runs and exits. On Windows the binary is `GMAT.exe` in
`GMAT/bin`. Each case propagates one host plus twelve satellites for 90 days.

**Expect a few minutes per case.** RungeKutta89 at 1e-11 accuracy with a 20×20 field, drag and
SRP over 90 days for thirteen objects is not instant.

## 3. What a good run produces

Twelve report files per case, `sat01.txt` … `sat12.txt`, each with hourly rows of

```
UTCGregorian   SMA   ECC   INC   RAAN   Altitude
```

Sanity checks before you send them back — these are the ones that catch a broken run:

| Check | Expected |
|---|---|
| Row count per file | ~2160 (90 days, hourly) |
| SMA at epoch, prograde satellites | 6857.6 km at R1 |
| INC at epoch | within 0.13° of the reference inclination |
| RAAN at 90 days | spread of **13°** (R1), **12.7°** (R2), **21.9°** (R3) |
| Altitude | never negative, and no satellite reentering inside 90 days |

If any file is empty, GMAT could not resolve the report path. It resolves relative paths against
`bin/../output`, not your working directory, which is why the generator writes absolute paths.

## 4. Send the reports back

Paste the files, or the whole `validation/gmat/output/` directory, into the next session. Then:

```bash
python3 validation/gmat/parse_reports.py --analysis A15
```

which applies A15's eight declared bands and writes the verdicts into
`validation/results/A15_poem_campaign.json`. **The bands are in the run sheet and were committed
at `e067da8`, before the template existed.** Do not edit them to match what comes back — a missed
band is a numbered defect, which is the whole point of the directory.

## 5. If a band fails

The consequences were fixed before the run and are written down in A15 §"What happens at each
outcome". In short: bands 1, 3 or 5 failing means suspect the script before the physics; band 2 or
4 failing narrows the deployment claim and needs the paper corrected; band 6 failing re-opens
ADR-020's cadence.

## Known caveats you are running with

- **R2 and R3's orbital elements are unverified.** They are written from recollection of published
  PSLV mission profiles and are marked as such in the script header and the results JSON. Confirm
  or cite them before any of R2/R3 is published. R1 is the traceable case.
- **Satellites are staggered analytically, not fired in sequence.** Each is placed on its
  post-burn orbit with mean anomaly rewound by `n·t_k`, the same device
  `emocd_fleet.script.tmpl` uses. This ignores J2 during a 4 h rewind against a 90 day
  propagation.
- **Case B is not generated yet.** The host-assisted plane change needs a POEM Δv budget, and
  paper §VII records that POEM's mass and control authority are undisclosed (E5). Band 8 is
  declared VOID-able for that reason.
