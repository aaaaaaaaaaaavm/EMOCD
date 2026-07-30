# ADR-007: Dual transverse cassettes

**Status:** Accepted · **Date:** 2025 · **Phase:** I

## Context
Twelve 3U satellites must be fed onto one track without shifting the centre of mass enough to
upset the host's attitude control.

## Decision
Two transverse cassettes of six, feeding alternately.

## Alternatives
- **Revolver magazine.** Rejected: rotating mass and a harder indexing mechanism.
- **Tandem in-line magazine.** Rejected: the CoM shift as it empties is monotonic and large.
- **2-DOF feed.** Rejected as mechanism complexity for no gain.

## Consequences
Alternating feed keeps the CoM shift roughly symmetric. It costs two escapements instead of
one, and it sets the enclosure width. G3-D1 records a 50 mm discrepancy between the drawn
cassette height and `parameters.json`.

## Validation
Feed forces and cadence are in the paper; the escapement is drawn but unanalysed (E10).
