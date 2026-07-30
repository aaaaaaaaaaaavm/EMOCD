# ADR-002: Host is a spent upper stage, not a free-flyer

**Status:** Accepted · **Date:** 2023 · **Phase:** Concept

## Context
The original concept was a dedicated free-flying deployer. Learning of ISRO's POEM, a spent
PSLV fourth stage operated as a stabilised platform, reframed the problem.

## Decision
Host the deployer on a spent upper stage or hosted platform. Do not build a free-flyer.

## Alternatives
- **Dedicated free-flyer.** Rejected: it must carry its own attitude control, power and recoil
  management, which is most of a spacecraft.
- **Bolt to the primary payload.** Rejected: makes the deployer the primary's problem.

## Consequences
This is what turns the concept from a mission into a payload. The stage already supplies
attitude control, power and enough mass to absorb recoil. The cost is a dependency on host
properties that are frequently not public, E5, and the reason the recoil table is parametric.

## Validation
Host integration is worked against POEM and Skyroot's Vikram-1 in the paper. The single
missing input is stage mass and control authority; obtaining it converts the analysis from
parametric to specific.
