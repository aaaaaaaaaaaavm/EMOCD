# ADR-019: Keep the Gen4 open assembly separate from the frozen Phase I baseline

**Status:** Accepted · **Date:** 2026-08-03 · **Phase:** Gen4 transition

## Context

The committed Phase I model accelerates through a uniform 1.30 m active stator and
releases at 1500 mm. The reviewed `EMOCD_Gen4_Open v7` assembly instead uses the
488 mm sled at s = 300 mm stowed and s = 1200 mm release. Its 340 mm Halbach array is
fully over the stator for 751.5 mm of that 900 mm stroke. The final 148.5 mm is under
partial overlap; 191.5 mm of the array remains over the stator at release.

The new station keeps release 22 mm ahead of brake-fin entry and gives the fin 330 mm
of travel through the brake. It is a geometry decision, not a performance result.
Replacing the Phase I headline with a shortened-stroke constant-thrust calculation
would only make a new number look derived.

## Decision

Treat `EMOCD_Gen4_Open v7` as a provisional, open public assembly. Keep the enclosure
as a separate envelope-check configuration. Do not export Gen4 STEP, STL, or renders,
and do not quote a Gen4 operating point, until a finite-stator position-dependent
motor calculation has been run and its affected evidence has been classified.

## Alternatives

- **Keep the 1500 mm release station.** Rejected: the brake fin is already inside the
  brake envelope at release.
- **Extend the track and enclosure to retain the 1.30 m stroke.** Rejected for this
  revision: it enlarges the existing packaging problem and turns a CAD correction into
  a host-envelope decision.
- **Use a 900 mm constant-thrust calculation.** Rejected: the finite stator edge is
  encountered before release, so constant thrust is not the stated geometry.

## Consequences

The Phase I baseline remains visible and reproducible. The Gen4 configuration has no
public exit velocity, energy, efficiency, thermal, orbit, or regeneration claim yet.
P32 records the operating-point mismatch, and E27 records the missing finite-stator
force profile. P28 remains open because the Gen4 arrangement does not lay out the
Phase I regeneration section.

The choice retains a shorter track and an open explanatory assembly, but it delays CAD
export until the new geometry has a numerical basis.

## Validation

Implement a position-dependent field and force calculation over the finite stator,
with the Gen4 body bounds and stations as declared inputs. Record the implementation,
tool version, input hash, numerical settings, output hash, and comparison with the
existing infinite-period result where their domains overlap. Then identify every
validation and document that depended on the Phase I operating point before changing
any public number.
