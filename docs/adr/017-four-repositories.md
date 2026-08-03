# ADR-017: Four repositories, two of them generated

**Status:** Accepted · **Date:** 2026-07-29 · **Phase:** I

## Context
The programme has four deliverables: the flagship engineering record, the IEEE paper, the
thesis, and a continuing research track. Dossier §3 designates repositories 2-4 as *Future*; §4 requires
explicit approval and warns *"never create new repositories merely because work can be
modularised."*

## Decision
Create all four now. **`VOLLEY-paper` and `VOLLEY-thesis` are generated** by
`tools/export_companion.py` and never hand-edited. `VOLLEY-lab` is Phase II and
hand-maintained. Recorded as an authorised amendment in `docs/programme/ADOPTION.md`.

## Alternatives
- **Flagship only, defer the rest.** The dossier as written. Rejected because it leaves
  redesign work with nowhere to go except the flagship itself. A Phase II track inside the
  flagship is a soft boundary, one `git checkout` from an edit to the frozen baseline, and
  §2 requires that baseline to hold for the duration of Phase I.
- **Four hand-maintained repositories.** Rejected as the failure §4 warns about. `16.388 m/s`
  appears in nine places in the flagship alone; four hand-maintained copies would diverge, and
  this project has already produced two such forks (ADR-015).
- **Branches instead of repositories.** Rejected for Phase II on the same soft-boundary
  argument.

## Consequences
Gains a hard wall between frozen and free. Costs: three repositories that will look sparse
until they have content, which is why each carries a README stating its role so sparseness
reads as structure rather than abandonment.

**The mitigation is mechanical, not behavioural.** If `export_companion.py` is ever bypassed
to hand-edit a companion, the mechanism is dead, and the correct response is to delete and
regenerate, never to reconcile.

## Validation
The exported paper companion was verified to reproduce standalone: run from a clean copy it
returns `v_exit = 16.388`, matching the flagship. The cross-link header is emitted from one
source, so it cannot drift between the four.
