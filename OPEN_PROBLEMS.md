# Open problems, known errors, and the fix list

Two categories: **P-items are errors in the currently published paper** and should be
fixed first. **E-items are genuinely unsolved engineering.**

Last reviewed 2026-07-27.

---

## P — Errors found while building this repo (paper does not match its own scripts)

> **STATUS (2026-07-23): P1–P4 all RESOLVED in `paper/paper.tex`.** Fixes, causes and
> before/after values are logged in `CHANGELOG.md` (entries P2-01–P2-04). The items are
> kept in full below for the audit record. Two related defects found in the process were
> also fixed: the F06 conjunction figure was regenerated at the rated velocity, and a
> stale `astro.py` docstring value was corrected — both logged in `CHANGELOG.md`.

### P1. Conjunction minimum is wrong AND not a robust quantity — HIGH PRIORITY
**RESOLVED 2026-07-23 — see CHANGELOG.md P2-01.**
The paper states a 30-day minimum satellite-to-stage approach of **45.3 km**. That
figure was computed at **20.65 m/s**, the superseded operating point. At the paper's
own rated velocity of **20.37 m/s**, `analysis/astro.py` gives **4.6 km**.

Worse, the quantity is fragile. Sweeping ejection velocity:

| Δv (m/s) | min approach (km) |
|---|---|
| 20.00 | 37.5 |
| 20.37 (rated) | **4.6** |
| 20.50 | 56.1 |
| 20.65 (paper's value) | 45.3 |
| 21.00 | 63.4 |

This is a near-resonant beat sample, not a design property. A ±2.5 % velocity change
moves it by more than an order of magnitude.

**Follow-up:** `validation/A6_conjunction_cara.md` specifies the quantitative version —
probability of collision via NASA's CARA tools, which integrates over the covariance
instead of sampling one geometry. The test is whether Pc stays stable across the velocity
sweep that moves minimum distance by an order of magnitude.

**Fix:** stop quoting a specific minimum distance as a safety result. Reframe around
what IS robust: the ~8.1-day phase realignment period, and the mitigation of disposing
of the host stage before the first realignment. State plainly that per-shot COLA is
mandatory because the approach geometry is sensitive to exact ejection velocity.

### P2. Peak current is stale — MEDIUM PRIORITY
**RESOLVED 2026-07-23 — see CHANGELOG.md P2-02.**
Paper says **323 A**. That belongs to the superseded 130 kA/m point. At the rated
140 kA/m, `motor_model.py` gives **392 A**. Fix the paper, and check that the SiC
device derating discussion still holds at the higher current (it should — 96 V rail,
1200 V devices — but the current rating of the bridge and busbars needs restating).

### P3. Far-field stray values don't reproduce exactly — LOW PRIORITY
**RESOLVED 2026-07-23 — see CHANGELOG.md P2-03.**
Paper quotes 22.7 / 4.7 / 1.0 mT at 10 / 20 / 50 mm. `verify_field.py` reproduces
22.7 mT at 10 mm exactly but gives 4.3 and 0.4 mT at 20 and 50 mm. Likely sensitivity
to modelled array length (edge effects dominate the far field). The 10 mm value is the
one that sets the keep-out spec, so this is minor — but resolve it before anyone cites
the 20/50 mm numbers.

### P4. Brake fin temperature rise conflates per-shot with per-campaign — MEDIUM PRIORITY
**RESOLVED 2026-07-23 — see CHANGELOG.md P2-04.**
The paper states the 0.86 kg copper fin sees "an adiabatic 37 K transient rise" **per
shot**, and later refers to "the adiabatic per-shot rises (0.3 K coil, 37 K fin)".

`analysis/sizing.py` gives 1008 J into 0.86 kg of copper = **3.0 K per shot**. The 37 K
figure is the *full 12-shot campaign* total if the fin never radiated between shots
(12 x 1008 J / 331 J/K = 36.5 K).

The design is therefore *less* thermally stressed than the paper claims, but the number
as written is wrong and internally inconsistent.

**Fix:** state 3.0 K per shot, and 37 K as a bounding campaign-adiabatic case that
radiation between shots relieves. Same correction applies to the coil: 0.28 K per shot,
3.3 K campaign.

---

## P — CAD reconciliation and packaging (found in the 2026-07-23 Fusion 360 CAD build)

> These arose when the parametric design was taken into CAD across nine Fusion documents.
> The CAD is authoritative for **geometry and fit only**; `analysis/*.py` remains
> authoritative for **mass and performance** until FEA closes the open items. All
> geometry values below are traceable to `cad/parameters.json`. **No number in
> `analysis/*.py` or `paper/paper.tex` has been changed** on the strength of the CAD.

### P5. CAD sled mass contradicts the parametric assumption — HIGH PRIORITY
The first-pass Fusion sled (6 mm Ti-6Al-4V chassis, stiffness-driven by the ±0.05 mm gap
tolerance under 3.7 kN inter-array attraction, **no structural FEA behind it**) implies a
sled mass of **~7.50 kg**. `analysis/mass_properties.py` assumes **4.86 kg**, which
`motor_model.py` hard-codes as `M_SLED` and which sets the headline exit velocity. Both
are estimates — one CAD-geometric, one parametric-solid — and neither is FEA-verified. Do
not change the scripts until analysis A4 closes the chassis — specified with a
pre-declared decision rule in `validation/A4_sled_structural.md` (CalculiX or
Code_Aster, both free, both read `cad/step/EMOCD_Sled.step`). Source:
`cad/parameters.json` (sled group, `PROVISIONAL_PENDING_FEA`).

### P6. Payload seating / orientation — RESOLVED (by CAD, 2026-07-23)
Resolved via the rail interface: the 3U payload now models the four CubeSat Design
Specification corner rails (8.5 mm, `cad/parameters.json` `payload_3u`), which fix seating
and orientation against the sled cradle. No further action.

### P7. Brake sits past the release point — geometry / ConOps
The eddy brake occupies **x = 1530–1740 mm**, beyond the **1500 mm** satellite release
point, on an 1800 mm longeron. The sled runs on into the brake after the payload departs
— consistent with the fire-then-arrest ConOps, but it forces the track and enclosure to
extend past release, which drives the envelope length (see P9). Source:
`cad/parameters.json` (brake, track).

### P8. Exit velocity provisionally 17.88 m/s pending sled structural FEA — HIGH PRIORITY
If the CAD sled mass (P5) holds, exit velocity falls from the script's **20.37 m/s** to a
provisional **~17.88 m/s** (with acceleration ~12.5 g, efficiency ~24 %, recoil
~71.5 N·s, lifetime multiplier ×1.68 — all CAD-corrected and provisional). **These values
are NOT propagated into `analysis/*.py` or `paper/paper.tex`**; the scripts stay
authoritative until analysis A4 locks the sled mass (`validation/A4_sled_structural.md`,
which fixes in advance which of the two estimates wins at which mass). Do not hard-swap
20.37 → 17.88 anywhere. Source: 2026-07-23 CAD Master Plan; see README headline note.

### P9. Closed envelope exceeds ESPA Grande by ~44% — packaging / host
The closed installed envelope is **1839 × 530 × 940 mm** (`cad/parameters.json`). The
1839 mm length exceeds ESPA Grande's ~1270 mm longest-dimension class by ~44%, because
the brake lives past the 1500 mm release point and the enclosure spans it. Owner decision
(cannot be made in code): re-scope the host to POEM / custom accommodation (the paper
already leans host-agnostic), or shorten the track / repackage the brake. This supersedes
the earlier 1825 × 516 × ~1030 mm figure; the height change (1030 → 940) exceeds what skin
thickness explains and is **flagged for re-verification** in `cad/parameters.json`.

### P10. Enclosure, radiator, and packaged avionics absent from the mass rollup — MEDIUM (NEW)
The ninth document (`EMOCD_Enclosure`) adds 2 mm aluminium skins, a 1600 × 200 × 3 mm
radiator, and equipment bays for the supercapacitor bank, PPU, sequencer, and IMU. **None
have line items in `analysis/mass_properties.py`**, so the 72.3 kg dry-mass rollup is
incomplete. Add line items once masses are estimated (do not alter existing items without
cause). Source: `cad/parameters.json` (`enclosure.mass_note`).

### P11. The corrections may never have reached the submitted paper — UNCONFIRMED (NEW 2026-07-27)
`paper/archive/EMOCD_submission_uncorrected.pdf` is a build of the paper that still
carries all four P1–P4 values (323 A, 23 A/mm² at 140 kA/m, 37 K per shot, 45.3 km
conjunction minimum). Its filename says *submission*. If that is genuinely the version
that went to the conference, then P1–P4 are corrected **only in this repository** and the
version of record is still wrong — which is a different situation from the STATUS block
at the top of this file, and one that a corrigendum, not a git commit, has to fix.
**Confirm which build was submitted.** If it was the uncorrected one, decide between
withdrawing, submitting an erratum, or correcting at the camera-ready stage, and record
the outcome here. If the submitted build was in fact compiled from the corrected
`paper.tex`, delete this item and say so in `CHANGELOG.md`.

### Advanced or resolved by the CAD build (not full closures)
- **Launch restraint now exists as geometry.** The breech launch-lock blocks are modelled
  (`cad/parameters.json` `track`: `launch_lock` at x = 30–50 mm, 2 off). This advances
  **E10** (previously "concept-level") — the lock is drawn, though still not analysed.
- **Payload interface now models CDS corner rails** (see P6), giving the rail contact
  faces the interface-control drawing needs.

---

## E — Unsolved engineering

### E1. Three-dimensional field closure — half of it is now set up, not run
`motor_model.py` resolves the winding in 2-D. End effects of a few percent on Kt remain
uncomputed. This is the declared close-out task for the electromagnetic model. The
magnetostatic package now exists — `analysis/femm/emocd_cross_section.dxf` plus
`analysis/femm/FEMM_RUN_SHEET.md` (analysis A1), which supersedes the older
`docs/FEMM_Run_Sheet.md`; the acceptance band in that older sheet predates the
winding-resolved model and should not be used. **Nothing has been run.** A1 closes the
2-D half; the 3-D end effects still need a 3-D solver (Elmer or GetDP are the free
options). Acceptance band declared in `validation/A1_field_femm.md`.

### E2. No FEA confirmation of anything
The field cross-check is analytic-vs-analytic (both magpylib and the wave model assume
ironless geometry, where superposition is exact). That is a genuine check of the wave
model but is NOT independent confirmation from a different physical method. Two analyses
are specified and neither has been executed: **A1** magnetostatic (E1 above) and **A4**
sled-chassis structural, which is what P5 and P8 are waiting on. Both, plus A5–A7, are
written up with pre-declared acceptance bands in `validation/`.

### E3. Masses are parametric and unchecked against vendor data
CAD now exists (`cad/`, nine documents), so the "no CAD" half of this item is closed —
but the mass problem is not. `mass_properties.py` still uses primitive solids with
shell/fill factors, and no component mass is checked against a vendor datasheet;
estimate spread perhaps ±15 %. Fusion-computed masses are **not** a substitute: they use
solid-copper stator, solid-aluminium CubeSats, and steel standing in for NdFeB, which is
why they are deliberately excluded from `cad/parameters.json`. The sled mass (4.86 kg)
propagates directly into the headline velocity — see P5 and P8 — and the enclosure,
radiator, and avionics are still missing from the rollup entirely (P10).

### E4. No hardware at any level
TRL 2–3. Nothing has been built, fired, or measured. The velocity, dispersion, and
tip-off claims are all model outputs.

### E5. Host stage properties unavailable
Recoil budgets are parametric across 300–900 kg host classes because no candidate
stage publishes its mass and control authority. Cannot be closed from public data.

### E6. Absolute orbital lifetimes are uncertain
Static exponential atmosphere at mean solar activity. Absolute lifetimes swing
severalfold across the solar cycle. The ×1.80 ratio is invariant and is the defensible
claim; absolute years are not. `validation/A5_astro_orekit.md` specifies an independent
re-run under Orekit or GMAT — different codebases, independently implemented force
models — with the band on the ratio and explicitly not on the absolutes.

### E7. Velocity dispersion rests on assumed sensor noise
The 0.027 m/s (3σ) result is a closed-loop simulation using an assumed 8 mm/s sensor
sigma and assumed tolerance distributions. No sensor has been selected or characterised.
The separation side of this is specified in `validation/A7_separation_chrono.md`, whose
tip-off band is taken from a flown deployer (NRCSD-E, < 5 °/s/axis) rather than chosen.

### E8. Brake energy is thrown away
~1.0 kJ per shot dissipated in the fin. Whether any of it is worth recovering (and what
that would cost in mass and complexity) has not been examined since the efficiency
correction.

### E9. 6U/12U variants are force-limited, not designed
The payload family table is arithmetic from the same thrust constant. No mechanism,
cassette, or structural design exists for larger classes.

### E10. Launch restraint is drawn but not analysed
Retention gate pin sizing exists (two D6 A-286, margin 1.2) and the breech launch-lock
blocks are now modelled in CAD (`cad/parameters.json` `track`: `launch_lock`, x = 30–50
mm, 2 off). The rest — escapement caging, cam lock, tolerance stack-up under vibration —
is drawn or described, not analysed.

### E11. No contamination or outgassing analysis
Materials were selected against E595 limits by rule, not by analysis. No contamination
budget for customer optics exists.

### E12. EMC beyond stray field
Static magnetic keep-out is computed. Induced currents from switching transients in
adjacent payloads are discussed but not calculated.

### E13. Two numbers in source documents were never traced
- The "780 deg/s" tumble rate from a third-party document. Falsified as
  implausible (would require a ~7.6 m line-of-action offset on a 1 m vehicle) but its
  origin was never found.
- The "1,000+ G hardening" figure, whose context (ground-launch guns) does not apply
  to this design.

### E14. Patent / disclosure — the disclosure has now happened
Concept and results are public (LinkedIn, and this repository, which is now a **public**
repo carrying the scripts and therefore the operating point). No provisional application
was filed first, so this is done and cannot be undone. What remains is not a decision but
a consequence to be handled: any patent route now runs on whatever post-disclosure grace
period applies in each jurisdiction — India and the US have one, most of Europe does not
— counted from the earliest public disclosure, not from today. **If a filing is still
wanted, establish that earliest date and take advice quickly.** If it is not, close this
item out explicitly so it stops reading as pending.

### E15. Sponsorship not secured
The build is the declared next step and is unfunded.

### E16. Reference hygiene
Three references in `paper/paper.tex` were flagged verify-before-submission and have
not been fully verified: eddy-damper heritage [15], Yudintsev separation dynamics [17],
and the vibro-impact deployment paper [18]. `docs/RELATED_WORK.md` adds a further list of
comparator sources and tooling — **none of it retrieved and read either**, and it carries
the same rule: fetch before citing. The differential-drag comparator (Foster et al., flown
Planet Labs results) is the one worth chasing first, since the paper's 25-day baseline is
currently a model output rather than a measurement.
