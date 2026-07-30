# Provenance

Publishing under a personal name requires knowing exactly what stands behind each
claim. This file records that. It is deliberately unflattering.

## Summary

**Every calculation, script, figure, and document in this repository is a model output.**
Nothing here has been measured. No value has been re-derived by hand or checked against a
second method unless this file says so explicitly.

There is no hardware, no finite-element analysis, and no third-party review anywhere in
this project. The CAD is first-pass geometry with no structural analysis behind it.

## What is model output and unverified

All of the following:

- Every calculation in `analysis/` and `legacy/`
- The coilgun-to-linear-motor trade analysis and its supporting numbers
- All performance figures: thrust constant, exit velocity, efficiency, dispersion
- All astrodynamics: lifetime multipliers, seeding rates, conjunction screening
- All mass, thermal, structural, and electrical budgets
- Every figure and diagram
- The IEEE paper, all verification reports, all research summaries
- The literature review and all citation formatting

## Where a genuine cross-check exists

Only two results have independent corroboration, and both are internal:

1. **Halbach field model.** The analytic decaying-wave model agrees with magpylib's
   cuboid superposition to three digits (0.351 T single-array) and within ~1 % on the
   double-sided peak. Caveat: both methods assume ironless geometry, so this validates
   the wave model but is not confirmation by a different physical method.
2. **Orbital decay.** Orbit-averaged Gauss integration agrees with an independent
   Cowell RK4 propagation to 99.4 % on 30-day semi-major-axis decay.

Everything else is single-sourced.

## Errors made and corrected during the work

Recorded because they calibrate how much to trust the rest:

1. Regenerative braking was claimed to arrest the sled. False, braking force is bounded
   by the same thrust constant as acceleration and would need more track than exists.
   Led to the eddy-brake design.
2. Abort was claimed to be available "anytime before release." False, the commit point
   is ~45 % of stroke.
3. The efficiency chain credited 55 % regeneration while the arrest architecture
   dissipates that energy in the brake. Double-counting; efficiency corrected 40 % to 32 %.
4. Two sign errors in the Halbach array convention, caught by empirically probing a
   single array rather than asserting the convention.
5. A retention gate pin was sized at margin 0.5 (inadequate); resized to two D6 pins,
   margin 1.2.
6. **Found while building this repo:** the paper's conjunction minimum (45.3 km) and
   peak current (323 A) both belong to a superseded operating point. See
   `OPEN_PROBLEMS.md` P1 and P2.

## Source material

Three earlier working documents, a feasibility PDF, a consolidated report, and a
strategy document, were checked against the analysis rather than trusted. They were
**sources of claims to check, not sources of truth**, and several of their numbers were
found to be wrong or unattributable. They are not included in this repository.

## How to cite this work honestly

This is a design study at TRL 2-3 with no experimental validation. Any publication or
presentation should say so.
