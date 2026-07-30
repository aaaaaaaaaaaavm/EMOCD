# ADR-006: Magnets ride the sled; the CubeSat is never modified

**Status:** Accepted · **Date:** 2025 · **Phase:** Load-bearing

## Context
An electromagnetic launcher needs something on the moving body to push against. The obvious
choice is to put it on the payload.

## Decision
A **reusable** sled carries the Halbach array. The customer satellite is unmodified, no
armature, no plating, no electrical interface, and sits in a cradle on standard CDS rails.

## Alternatives
- **Armature on the customer satellite.** Rejected. It is simpler and lighter, and it destroys
  the product: every customer would need to modify their spacecraft and requalify it. The
  entire commercial argument rests on not asking that.
- **Consumable sled per shot.** Rejected on mass: twelve sleds is most of the mass budget.

## Consequences
**This is the decision the whole value proposition rests on.** It costs a reusable mechanism
that must survive twelve arrests per campaign, a magazine feed, and a sled mass that directly
subtracts from exit velocity, the 9.445 kg measured sled is why the headline is 16.5 m/s and
not 20.4 (ADR-012). It also creates a magnetic keep-out constraint for satellites still in
the cassettes.

## Validation
Stray field measured against `verify_field.py`, B-1 and qualification test T-6. Reuse life
is E21 (vacuum tribology, entirely unanalysed) and T-8.
