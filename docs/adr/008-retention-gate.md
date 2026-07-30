# ADR-008: Retention gate separates ascent preload from the release path

**Status:** Accepted · **Date:** 2025 · **Phase:** I

## Context
NanoRacks experienced a deployment failure traced to a ball-lock mechanism carrying ascent
preload through the release path.

## Decision
A one-shot retention gate at each cassette exit carries ascent preload **directly into
structure**. The escapement is caged behind it and sees none of that load.

## Alternatives
- **Release mechanism carries preload.** Rejected, this is precisely the failure being
  designed against.
- **Pyrotechnic restraint.** Rejected: shock next to brittle magnets, and non-pyro release is
  already the fielded standard (`docs/LANDSCAPE.md`).

## Consequences
Deliberately borrows a lesson from someone else's failure, which is the cheapest kind of
engineering evidence available. Costs a separate one-shot mechanism per cassette. The gate
carries 5.9 kN through two D6 A-286 pins at a margin of **1.2**: the thinnest margin in the
design, and the reason T-1 vibration is the likeliest qualification failure.

## Validation
`sizing.py` `retention_gate()`. Qualification test T-1.
