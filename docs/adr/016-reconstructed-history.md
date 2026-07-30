# ADR-016: Reconstruct the git history with labelled dates

**Status:** Accepted · **Date:** 2026-07-29 · **Phase:** I

## Context
The project began 22 March 2021; the repository was created 23 July 2026. The commit graph
showed one week of work on a five-year project, and three CAD generations appeared in a single
import commit.

## Decision
Reconstruct commits at documented design periods, and **label the reconstruction in three
places**: `HISTORY.md`, the commit messages, and git's own metadata, author dates carry the
design periods, committer dates all read 2026-07-29.

## Alternatives
- **Backdate silently.** Rejected. GitHub exposes repository creation and push times, so it is
  detectable; and in a repository whose entire argument is auditability, an unlabelled
  fabricated timeline would discredit everything else in it.
- **Tags and a timeline document only, no commit reconstruction.** Safest, and rejected as
  insufficiently informative, the commit graph would still show one week.
- **Leave it.** Rejected: the five-year span is real and invisible.

## Consequences
The span is visible and the reconstruction is undeniable from `git log --format='%ad | %cd'`.
**Four of six milestone dates are approximate** and say so, `cad/CHANGELOG_CAD.md` states
Gen1's build history was never reconstructed, so inventing precision it disclaims would have
been the exact failure this project logs against itself.

Gen1's placement after the motor decision is **inferred from the artifacts**: its files
contain a stator, which a coilgun has not, and `HISTORY.md` says so and defers to the CAD
changelog if the inference is wrong.

## Validation
Tree hash byte-identical before and after (`1435acc`), and 37 commits preserved. Content did
not change, only history.
