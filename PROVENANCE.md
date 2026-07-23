# Provenance

Publishing under a personal name requires knowing exactly what stands behind each
claim. This file records that. It is deliberately unflattering.

## Summary

**Essentially every calculation, script, figure, and document in this repository was
produced by an AI assistant (Claude) during a chat session with the project owner.**
The owner directed the work, made the design decisions, supplied the concept and its
history, rejected proposals, and caught framing errors. The owner did **not**
independently re-derive, re-run, or hand-check any calculation.

There is no hardware, no CAD, no finite-element analysis, and no third-party review
anywhere in this project.

## Markings used

- `[ME]`   — stated, decided, or supplied by the project owner
- `[YOU]`  — proposed, derived, or drafted by the AI and not independently verified
- `[BOTH]` — worked out jointly, or where the owner materially shaped or corrected it

## What is owner-originated `[ME]`

- The core concept: an electromagnetic launcher flown on a rideshare that places
  CubeSats into their own orbits (conceived March 2021; presented at ARDE/INSARM 2021
  and India Science Festival 2024)
- The original dual option of "maglev rail or coilgun, whichever is more feasible"
- Identifying ISRO's POEM as host and flight-demonstration path
- Project history, dates, venues, and all biographical content
- Scope decisions: PBL-2 framing, host-agnostic reframing, publishing publicly
- Rejecting the Skyroot-specific framing

## What is AI-generated and unverified `[YOU]`

All of the following. Each was produced by the AI and never checked by a second method
unless explicitly noted:

- Every calculation in `analysis/` and `legacy/`
- The coilgun-to-linear-motor trade analysis and its supporting numbers
- All performance figures: thrust constant, exit velocity, efficiency, dispersion
- All astrodynamics: lifetime multipliers, seeding rates, conjunction screening
- All mass, thermal, structural, and electrical budgets
- Every figure and diagram
- The IEEE paper, the PBL skeleton, all verification reports, all research summaries
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

1. Claimed regenerative braking would arrest the sled. False — braking force is bounded
   by the same thrust constant as acceleration and would need more track than exists.
   Led to the eddy-brake design.
2. Claimed abort was available "anytime before release." False — the commit point is
   ~45 % of stroke.
3. Credited 55 % regeneration in the efficiency chain while the arrest architecture
   dissipates that energy in the brake. Double-counting; efficiency corrected 40 % → 32 %.
4. Two sign errors in the Halbach array convention, caught by empirically probing a
   single array rather than asserting the convention.
5. Sized a retention gate pin at margin 0.5 (inadequate); resized to two D6 pins,
   margin 1.2.
6. Guessed at LinkedIn character limits repeatedly instead of measuring.
7. **Found while building this repo:** the paper's conjunction minimum (45.3 km) and
   peak current (323 A) both belong to a superseded operating point. See
   `OPEN_PROBLEMS.md` P1 and P2.

## Third-party material

Three documents were uploaded by the owner and verified by the AI: an AI-generated
feasibility PDF, an AI-generated consolidated report, and a strategy document. These
were **sources of claims to check, not sources of truth**, and several of their numbers
were found to be wrong or unattributable. They are not included in this repository.

## How to cite this work honestly

This is a design study produced with heavy AI assistance, at TRL 2–3, with no
experimental validation. Any publication or presentation should say so.
