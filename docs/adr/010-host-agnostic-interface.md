# ADR-010: Host-agnostic four-item interface

**Status:** Accepted · **Date:** 2026-07 · **Phase:** I

## Context
The paper was written host-specific, around POEM. That made it read as an ISRO proposal rather
than a deployer design.

## Decision
Specify the interface generically, mass and control authority, a 150-300 W recharge feed, a
serial command link, an authorised firing window, and treat POEM and Vikram-1 as worked
examples.

## Alternatives
- **Stay host-specific.** Rejected: ties the concept's fate to one vehicle.
- **Fully abstract, no examples.** Rejected: unfalsifiable, and loses the most concrete
  engineering in the paper.

## Consequences
Widens the addressable host set and makes the work legible to any launch provider. Costs
specificity: the recoil table stays parametric because the OAM's mass and control authority
are not public (E5).

## Validation
The interface is exercised against two real vehicles in the paper. One data exchange,
stage mass, thruster impulse budget, coast duration, converts it from parametric to specific.
