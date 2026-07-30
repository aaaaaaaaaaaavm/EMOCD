# ADR-018: VOLLEY as the programme name, EMOCD_ retained as the part prefix

**Status:** Accepted · **Date:** 2026-07-30 · **Phase:** I

## Context
`EMOCD` was doing two jobs at once: naming the programme and describing the machine. It fails at
the first. It cannot be said aloud, it carries no memory hook, and a reader meeting it cold has to
decode five letters before learning anything. The description it encodes, *electromagnetic orbital
CubeSat deployer*, is accurate and worth keeping as a subtitle.

The name appeared 946 times across 117 files, so the change is not free, and this was the cheapest
moment to make it: the paper is written but unsubmitted, and GitHub redirects renamed repository
paths, so nothing already published breaks.

## Decision
**VOLLEY** is the programme name. *An electromagnetic orbital CubeSat deployer* is the subtitle.
The paper reads `VOLLEY: A Linear-Motor Electromagnetic Deployment System...`.

The rename is applied in two tiers.

**Tier 1, renamed.** Prose, titles, headings, `CITATION.cff`, the Pages site, tool defaults, and the
configuration designations `EMOCD-A` and `EMOCD-F`, which become `VOLLEY-A` and `VOLLEY-F`. Those
name operating modes, not hardware.

**Tier 2, left alone.** The 30 `cad/**/EMOCD_*.step` and `.stl` files keep their names, and so do
`legacy/` and `paper/archive/`. `EMOCD_` becomes the **part-number prefix**.

## Alternatives
- **Rename everything, CAD included.** Rejected. `analysis/mass_properties.py` reads those paths, so
  the rename would have to move files and edit the script that measures the sled, in the same pass
  that must demonstrably not move a number. It also rewrites the provenance of three CAD generations
  to no reader benefit.
- **Keep EMOCD.** Rejected, but it was the honest default: zero cost, zero risk. What decided against
  it is that the name is the first thing a reviewer or a recruiter meets, and an unpronounceable
  acronym spends attention before it earns any.
- **Rename the GitHub repositories in the same pass.** Rejected as a sequencing hazard rather than a
  bad idea. Renaming the repositories invalidates the working environment's access to them, so the
  content change lands first and the repository rename follows by hand.

## Consequences
Part numbers now outlive the name on the cover, which is ordinary practice and is why this is
recorded rather than left to look like an oversight. Anyone reading `EMOCD_Sled_Gen3.step` inside a
repository called VOLLEY should find this file and stop wondering.

All four repositories were renamed on 2026-07-30, so the URLs now read `aaaaaaaaaaaavm/VOLLEY`.
GitHub redirects the old paths, so links published before the rename keep working.

## Validation
No numeric output moved: `tools/make_baseline.py --check` holds at 20 values and all six analysis
scripts reproduce their committed JSON. Every relative link in the repository resolves. The paper
rebuilds with zero undefined references.
