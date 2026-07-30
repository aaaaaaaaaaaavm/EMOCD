# ADR-001: Electromagnetic deployment instead of a spring

**Status:** Accepted · **Date:** 2021-03-22 · **Phase:** Concept

## Context
Rideshare CubeSat secondaries inherit the primary customer's orbit. The spring that ejects
them imparts 1-2 m/s, enough to clear the stage, far too little to change an orbit. A
satellite with no propulsion is stuck where the primary paid to go. The observation came from
watching a Rocket Lab Photon deploy CubeSats on 22 March 2021.

## Decision
Pursue an electromagnetic deployer delivering a **programmable** ejection velocity an order of
magnitude above a spring.

## Alternatives
- **Spring, accept the limitation.** Flight-proven, needs no power, and is what everyone uses.
  Rejected because it forecloses the entire capability being sought.
- **Give the satellite propulsion.** Solves the problem at the customer's expense, mass,
  cost, and a propulsion system on a 3U. Rejected: it moves the burden to the party least able
  to carry it.
- **Orbital transfer vehicle.** Works, and flies commercially. Rejected as a different product
  at a different price point; it does not serve the customer who cannot afford one.

## Consequences
Buys a regime nothing currently serves. Costs everything a spring does not need: power,
energy storage, thermal management, a sequencer, and a far harder qualification argument. It
also means competing against hardware with thousands of flight units behind it
(`docs/LANDSCAPE.md`).

## Validation
The value proposition rests on the astrodynamic effect being real: `analysis/astro.py`, A5,
and A9. The premise that spring deployers impart 1-2 m/s is cited to P-POD and NRCSD
documentation and is verifiable.
