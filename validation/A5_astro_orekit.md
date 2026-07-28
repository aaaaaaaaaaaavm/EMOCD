# A5 — Orbital lifetime and seeding (Orekit or GMAT)

**Closes:** `OPEN_PROBLEMS.md` E6 (absolute lifetimes uncertain), and converts the
×1.80 multiplier from self-checked to independently checked.

`astro.py` already cross-validates orbit-averaged Gauss against its own Cowell RK4 to
99.4 %. That is one code, two integrators, one atmosphere model — it catches integration
error, not modelling error. Orekit and GMAT are different codebases with independently
implemented force models, which is the check that is actually missing.

## Inputs

- Operating point: 450 km, 51.6°, ejection Δv per `analysis/results/astro_results.json`
- Ballistic coefficients: as used in `astro.py` (3U payload, host stage)
- Atmosphere: NRLMSISE-00 (Orekit `NRLMSISE00`, GMAT `MSISE90`/`NRLMSISE00`) at the same
  solar activity levels as the script's low/mean/high cases

## Acceptance band (declared 2026-07-27, before running)

| Quantity | Reference | Band |
|---|---|---|
| Lifetime multiplier, boosted vs unboosted | **×1.80** | ±5 % |
| Multiplier invariance across low/mean/high activity | invariant | spread ≤ 5 % |
| Seeding to 30°, 10 m/s | 1.4 days | ±20 % |
| Seeding to 30°, 5 m/s | 2.8 days | ±20 % |
| Seeding to 30°, 2 m/s | 6.9 days | ±20 % |

**Absolute lifetimes are explicitly not a pass/fail criterion.** The script's 2.61 /
1.30 / 0.52 yr base cases swing severalfold across the solar cycle and are not a defended
claim (E6). If Orekit's absolutes differ by a factor of two, that is expected and does not
falsify anything. The *ratio* is the claim, and the ratio is what the band applies to.

The ±20 % on seeding is wide on purpose: those numbers depend on the along-track drift
model and the definition of "phased", which will not match between codes exactly.

## Implementation: GMAT (primary), Orekit (alternative)

The toolkit lives in `validation/gmat/`. `build_scripts.py` fills two templates from
`analysis/results/astro_results.json` and **imports `boosted_elements()` and `_kepE()`
from `analysis/astro.py`** rather than reimplementing them, so the orbit definition cannot
fork between the two codes. It runs with no GMAT installed; `parse_reports.py` turns the
GMAT output into `validation/results/A5_astro.json` with an explicit pass/fail per band.

```bash
cd validation/gmat
python3 build_scripts.py                       # writes output/*.script
<gmat-console-binary> -r output/emocd_lifetime_mean.script
python3 parse_reports.py --invocation '<the command that worked>'
```

Force models are recorded in the results JSON, not left implicit in the script: MSISE90
atmosphere, 20×20 gravity, RK89, Luna and Sun as point masses, SRP on.

One modelling gap is documented rather than papered over: `astro.py` scales *density* by
0.5 / 1.0 / 2.5, GMAT takes *solar flux* (F10.7 = 70 / 150 / 250 here), and the two are not
equivalent. That affects absolute lifetimes, which are not the claim. The invariance band
applies to the spread of the multiplier, which should survive either parameterisation — and
if it does not, that is a genuine finding about the ×1.80.

Orekit remains a valid substitute for the same bands; nothing above depends on GMAT beyond
the script syntax.

## Second leg: check against flown decay, not just another model

Orekit agreeing with `astro.py` means two models agree. Reproducing a **measured** decay is
a stronger claim and the data is free: CelesTrak and Space-Track publish TLE histories and
reentry records for 3U CubeSats at 450–500 km with estimable ballistic coefficients.

Procedure: pick 3–5 non-manoeuvring 3U objects with clean TLE histories from deployment to
decay, estimate BC from the observed decay, and run the same integration `astro.py` uses.

| Quantity | Band |
|---|---|
| Predicted vs observed time-to-decay | within 15 % over the last year of life |

Published guidance puts lifetime prediction at roughly **10 % of residual lifetime** at
best, driven by density uncertainty, so 15 % is the honest band and anything tighter would
be luck. This leg validates the propagation machinery in absolute terms; the ratio band
above remains the claim EMOCD actually defends (E6).

## If the multiplier band is missed

The ×1.80 appears in the abstract, the README headline table, and the paper's central
value proposition. A miss is a paper-level correction, not a footnote. Record the
discrepancy, open a P-item, and do not adjust `astro.py` until the cause is understood —
force-model differences (drag coefficient convention, atmosphere epoch, third-body terms)
are the first thing to check, not the last.

## Output

`validation/results/A5_astro.json` — multiplier per activity level, seeding days per Δv,
absolute lifetimes for reference only, plus `tool`, `version`, `atmosphere_model`,
`force_models`, `integrator`, `epoch`.
