# ADR-004: Ironless stator

**Status:** Accepted · **Date:** 2025 · **Phase:** I

## Context
A conventional iron-cored linear motor gives more force per amp but adds cogging, attraction
between stator and magnets, and mass.

## Decision
Ironless: the winding sits in the airgap between two opposed Halbach arrays with no back-iron.

## Alternatives
- **Iron-core stator.** Rejected: heavy, and the cogging torque conflicts directly with a
  dispersion claim measured in centimetres per second.
- **Single-sided array with back-iron.** Rejected: halves the useful field for the same magnet
  mass.

## Consequences
No cogging, and no stator-to-magnet attraction, but a large inter-array attraction between
the two Halbach faces instead (P17), which the chassis must carry. Force per amp is lower, so
the design runs at high sheet current, which is where the copper loss and the 20 % efficiency
come from.

## Validation
A1 (magnetostatic FEA) would close the field model. The attraction was checked in 2026-07 by
3-D force integration and found 37 % below the flat-plate formula in `sizing.py`, P17,
Phase I error correction.
