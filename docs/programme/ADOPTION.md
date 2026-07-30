# Programme adoption record

| | |
|---|---|
| Governing document | `ENGINEERING_PROGRAMME.md`, Engineering Programme Dossier **v1.0** |
| Review instructions | `TECHNICAL_REVIEW_BOARD.md`, TRB Prompt **v1.0** |
| Adopted | **2026-07-29** |
| Current phase | **Phase I** |
| Frozen baseline | [`BASELINE.md`](../../BASELINE.md) |

Both documents are committed **verbatim as issued**. They are not edited in place. Where
practice departs from them, the departure is recorded here with its authorisation, the same
way this project records every other discrepancy rather than quietly resolving it.

---

## Amendment 1: repositories 2-4 created in Phase I

**Dossier §3 says:** Repository 2 (IEEE Companion), Repository 3 (Thesis Companion) and
Repository 4+ (Independent Research) are *Future*, and §4 requires explicit approval before
any is created.

**What was done instead:** all four repositories were created on 2026-07-29.

**Authorisation:** explicit, from the programme author, on 2026-07-29. §4's four-part test was
applied rather than skipped:

| §4 criterion | Assessment |
|---|---|
| Independent engineering project | **Met for `EMOCD-lab`.** Not met for the paper and thesis companions, which are derived. |
| Value outside EMOCD | **Met for `EMOCD-lab`**: it is where linear-motor and CubeSat-dynamics work would live beyond this deployer. |
| Keeping it inside would reduce clarity | **Met for all three.** University submission material pollutes a portfolio; a post-publication reproducibility package has a different audience; and Phase II redesign inside the flagship would directly threaten the baseline stability §2 requires. |
| Explicit approval | **Given.** |

**The reasoning that decided it**, recorded because it is the part worth auditing later: the
statement of intent in `WHY.md` names a tendency to re-question foundations and
spiral into redesign. A Phase II track kept *inside* the flagship is a soft boundary, one
`git checkout` from becoming an edit to the frozen baseline. `EMOCD-lab` makes that boundary
hard. The separation is a control against a known failure mode, not a filing preference.

**The risk this amendment creates, and its mitigation.** §4's warning, *"never create new
repositories merely because work can be modularised"*, is aimed at exactly the failure this
could cause: duplicated content diverging across repositories. This project has already
produced two such forks, the operating point between `motor_model.py` and `sizing.py` and the
figures against the analysis, both now mechanically guarded.

The mitigation is that **the two derived repositories are generated, never hand-maintained**
(`tools/export_companion.py`). If that tool is ever bypassed to hand-edit a companion, this
amendment has failed and the companions should be deleted and regenerated rather than
reconciled.

---

## Amendment 2: Phase II promotion gate defined

**Dossier §9 says** the programme remains open to questioning every assumption while
deliverables stay bound to scope. **It does not say how work leaves Phase II.**

Without a route back, Phase II is not a research track but a graveyard: a place ideas are
filed to be safely forgotten. The gate is defined in [`../PHASE_II.md`](../PHASE_II.md):
items are reviewed **only at baseline boundaries**, each against an entry criterion **written
at the time it was deferred**, the same discipline as declaring acceptance bands before a run,
and for the same reason. A criterion written after the fact is written by someone who already
knows what they want the answer to be.

**Authorisation:** programme author, 2026-07-29.

---

## What has *not* been amended

The parts of the dossier that constrain rather than enable are unchanged and binding:

- **§2**: Phase I deliverables develop against a frozen baseline; fundamental redesigns defer.
- **§4**: the flagship is a deliverable and its stability is a design requirement. It is not
  split or substantially reorganised.
- **§5**: *finished engineering before better engineering.* The hardest line in the document
  to hold, and the reason the baseline exists.
- **§7**: every feature needs a path toward validation.

## How to record the next amendment

Add a numbered section: what the dossier says, what was done instead, who authorised it, the
reasoning, and the risk it creates with its mitigation. **Do not edit the dossier.** A
governing document that quietly changes to match practice is not governing anything.
