# EMOCD-lab: Phase II

<!-- PROGRAMME-HEADER-START -->
| Repository | Role | You are here |
|---|---|---|
| [EMOCD](https://github.com/aaaaaaaaaaaavm/EMOCD) | Flagship, authoritative engineering record, portfolio | |
| [EMOCD-paper](https://github.com/aaaaaaaaaaaavm/EMOCD-paper) | IEEE companion, manuscript and reproducibility package *(generated)* | |
| [EMOCD-thesis](https://github.com/aaaaaaaaaaaavm/EMOCD-thesis) | Thesis companion, university submission *(generated)* | |
| **[EMOCD-lab](https://github.com/aaaaaaaaaaaavm/EMOCD-lab)** | Phase II, research, redesign, deliberately unstable | |
<!-- PROGRAMME-HEADER-END -->

> ## This repository makes no promises
>
> No frozen baseline. No stability requirement. Numbers here may be wrong, half-finished, or
> abandoned mid-thought. **Nothing in this repository should be cited.**
>
> The engineering record is the [flagship](https://github.com/aaaaaaaaaaaavm/EMOCD). If
> anything here disagrees with it, the flagship is right.

## Why this exists

The [flagship](https://github.com/aaaaaaaaaaaavm/EMOCD) is a Phase I deliverable and its
stability is a design requirement. This repository is the pressure valve that lets it stay
frozen.

The reasoning is in the flagship's
[`WHY.md`](https://github.com/aaaaaaaaaaaavm/EMOCD/blob/main/WHY.md): the stated
failure mode is spiralling into redesign. A Phase II track kept *inside* the flagship is a soft
boundary, one `git checkout` from becoming an edit to the frozen baseline. This is a hard wall
instead of a line on the floor.

**Redesign freely here. Do not touch the baseline there.**

## What belongs here

Anything that would make the design **better** rather than **correct**. The deferred list and
each item's entry criterion live in the flagship's
[`docs/PHASE_II.md`](https://github.com/aaaaaaaaaaaavm/EMOCD/blob/main/docs/PHASE_II.md):

| | |
|---|---|
| PII-1 | Momentum-transfer release, recovers the full velocity shortfall for 1.6 % of shot energy |
| PII-2 | Rib-stiffened chassis, A4 leaves a 17x stress margin unspent |
| PII-3 | Two-layer stator (G3-D4), sits upstream of K<sub>t</sub> |
| PII-4 | Envelope repackaging (P9), currently 44 % over ESPA Grande |
| PII-5 | Variable-shape atmosphere, the root cause behind P16 |

Also: anything from dossier §8's cross-industry list that turns into real work, and any idea
that does not yet have a home.

## What does not belong here

**Error corrections.** If something in the flagship is *wrong*, fix it in the flagship. The
distinction is the whole of the change-control rule in
[`BASELINE.md`](https://github.com/aaaaaaaaaaaavm/EMOCD/blob/main/BASELINE.md), and it is by
type, not by convenience. P17 is tedious and belongs upstream; the momentum-transfer release
is fascinating and belongs here.

## How work gets out

Only at a **baseline boundary**: the next opens after thesis submission, and only by meeting
the entry criterion written when the item was deferred. Not by seeming promising.

That rule exists for the same reason acceptance bands are declared before runs: a criterion
written afterwards is written by someone who already knows what they want the answer to be.
