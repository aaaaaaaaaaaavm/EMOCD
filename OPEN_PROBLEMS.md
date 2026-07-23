# Open problems, known errors, and the fix list

Two categories: **P-items are errors in the currently published paper** and should be
fixed first. **E-items are genuinely unsolved engineering.**

---

## P — Errors found while building this repo (paper does not match its own scripts)

### P1. Conjunction minimum is wrong AND not a robust quantity — HIGH PRIORITY
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

**Fix:** stop quoting a specific minimum distance as a safety result. Reframe around
what IS robust: the ~8.1-day phase realignment period, and the mitigation of disposing
of the host stage before the first realignment. State plainly that per-shot COLA is
mandatory because the approach geometry is sensitive to exact ejection velocity.

### P2. Peak current is stale — MEDIUM PRIORITY
Paper says **323 A**. That belongs to the superseded 130 kA/m point. At the rated
140 kA/m, `motor_model.py` gives **392 A**. Fix the paper, and check that the SiC
device derating discussion still holds at the higher current (it should — 96 V rail,
1200 V devices — but the current rating of the bridge and busbars needs restating).

### P3. Far-field stray values don't reproduce exactly — LOW PRIORITY
Paper quotes 22.7 / 4.7 / 1.0 mT at 10 / 20 / 50 mm. `verify_field.py` reproduces
22.7 mT at 10 mm exactly but gives 4.3 and 0.4 mT at 20 and 50 mm. Likely sensitivity
to modelled array length (edge effects dominate the far field). The 10 mm value is the
one that sets the keep-out spec, so this is minor — but resolve it before anyone cites
the 20/50 mm numbers.

### P4. Brake fin temperature rise conflates per-shot with per-campaign — MEDIUM PRIORITY
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

## E — Unsolved engineering

### E1. Three-dimensional field closure
`motor_model.py` resolves the winding in 2-D. End effects of a few percent on Kt remain
uncomputed. This is the declared close-out task for the electromagnetic model. FEMM run
sheet is in `docs/FEMM_Run_Sheet.md`; note the acceptance band there predates the
winding-resolved model and should be updated to the current Kt.

### E2. No FEA confirmation of anything
The field cross-check is analytic-vs-analytic (both magpylib and the wave model assume
ironless geometry, where superposition is exact). That is a genuine check of the wave
model but is NOT independent confirmation from a different physical method.

### E3. No CAD; all masses parametric
`mass_properties.py` uses primitive solids with shell/fill factors. No component mass
is checked against a vendor datasheet. Estimate spread perhaps ±15 %. The sled mass
(4.86 kg) propagates directly into the headline velocity, so CAD will move the
performance numbers.

### E4. No hardware at any level
TRL 2–3. Nothing has been built, fired, or measured. The velocity, dispersion, and
tip-off claims are all model outputs.

### E5. Host stage properties unavailable
Recoil budgets are parametric across 300–900 kg host classes because no candidate
stage publishes its mass and control authority. Cannot be closed from public data.

### E6. Absolute orbital lifetimes are uncertain
Static exponential atmosphere at mean solar activity. Absolute lifetimes swing
severalfold across the solar cycle. The ×1.80 ratio is invariant and is the defensible
claim; absolute years are not.

### E7. Velocity dispersion rests on assumed sensor noise
The 0.027 m/s (3σ) result is a closed-loop simulation using an assumed 8 mm/s sensor
sigma and assumed tolerance distributions. No sensor has been selected or characterised.

### E8. Brake energy is thrown away
~1.0 kJ per shot dissipated in the fin. Whether any of it is worth recovering (and what
that would cost in mass and complexity) has not been examined since the efficiency
correction.

### E9. 6U/12U variants are force-limited, not designed
The payload family table is arithmetic from the same thrust constant. No mechanism,
cassette, or structural design exists for larger classes.

### E10. Launch restraint is concept-level
Retention gate pin sizing exists (two D6 A-286, margin 1.2). The rest — escapement
caging, cam lock, tolerance stack-up under vibration — is described, not analysed.

### E11. No contamination or outgassing analysis
Materials were selected against E595 limits by rule, not by analysis. No contamination
budget for customer optics exists.

### E12. EMC beyond stray field
Static magnetic keep-out is computed. Induced currents from switching transients in
adjacent payloads are discussed but not calculated.

### E13. Two numbers in source documents were never traced
- The "780 deg/s" tumble rate from an uploaded third-party document. Falsified as
  implausible (would require a ~7.6 m line-of-action offset on a 1 m vehicle) but its
  origin was never found.
- The "1,000+ G hardening" figure, whose context (ground-launch guns) does not apply
  to this design.

### E14. Patent / disclosure question unresolved
Concept and results are now public (LinkedIn, and this repo). No provisional
application was filed first. Detailed mechanism design and operating point were
deliberately withheld from public posts — but publishing this repository discloses the
scripts and therefore the operating point. **Decide whether that is acceptable before
making the repo public.** This is a real, irreversible consequence.

### E15. Sponsorship not secured
The build is the declared next step and is unfunded.

### E16. Reference hygiene
Three references in `paper/paper.tex` were flagged verify-before-submission and have
not been fully verified: eddy-damper heritage [15], Yudintsev separation dynamics [17],
and the vibro-impact deployment paper [18].
