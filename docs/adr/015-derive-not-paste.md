# ADR-015: Derive coupled values; never paste them

**Status:** Accepted · **Date:** 2026-07-29 · **Phase:** I

## Context
Adopting the measured sled mass (ADR-012) broke three things that had nothing to do with mass,
because each held a pasted copy of a value that moved:

- `sizing.py` hard-coded 672 J copper loss and 26 J auxiliary. Energy closure fell to 94.2 %.
- The capacitor sizing quoted 5.97 F against a 4.9 % sag target the bank no longer met, at
  2795.6 J, holding 4.9 % needs 6.35 F, which a 6 F bank does not provide.
- The operating point existed independently in `motor_model.py` and `sizing.py`.

## Decision
Coupled values are **derived at run time or guarded**, never pasted. Where duplication is
unavoidable, a check fails loudly on drift.

## Alternatives
- **Keep literals, update carefully.** Rejected: this is what produced the defect. Care is not
  a mechanism.
- **Single module for all constants.** Rejected for now: it would make `sizing.py` require
  magpylib and re-integrate a shot to compute anything. The guard achieves the same protection
  at a fraction of the coupling.

## Consequences
`sizing.py::_check_operating_point()` asserts six quantities against `motor_model`'s own JSON
and exits with a diagnostic on drift. Loss terms derive from the operating point; closure is
back to 100.0 %. Capacitor sizing derives from the sag actually reached and *reports* the
6.35 F alternative rather than hiding it.

**This is the same pattern applied four times now:** `make_figures.py` (figures from analysis),
`make_baseline.py` (baseline from JSON), `export_companion.py` (companions from flagship), and
this guard. Every one exists because a hand-maintained copy diverged.

## Validation
Deliberately forking `V_EXIT` makes `sizing.py` exit with the diagnostic, tested. Energy
closure at 100.0 % is itself an arithmetic check that no loss term is missing.
