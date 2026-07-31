# Programme adoption record

| | |
|---|---|
| Governing document | `ENGINEERING_PROGRAMME.md`, Engineering Programme Dossier **v1.0** |
| Review instructions | `TECHNICAL_REVIEW_BOARD.md`, TRB Prompt **v1.0** |
| Adopted | **2026-07-29** |
| Current phase | **Phase I** |
| Frozen baseline | [`BASELINE.md`](../BASELINE.md) |

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
| Independent engineering project | **Met for `VOLLEY-lab`.** Not met for the paper and thesis companions, which are derived. |
| Value outside VOLLEY | **Met for `VOLLEY-lab`**: it is where linear-motor and CubeSat-dynamics work would live beyond this deployer. |
| Keeping it inside would reduce clarity | **Met for all three.** University submission material pollutes a portfolio; a post-publication reproducibility package has a different audience; and Phase II redesign inside the flagship would directly threaten the baseline stability §2 requires. |
| Explicit approval | **Given.** |

**The reasoning that decided it**, recorded because it is the part worth auditing later: §2
requires the Phase I baseline to hold for the duration of Phase I, and a Phase II track kept
*inside* the flagship is a soft boundary, one `git checkout` from becoming an edit to that
baseline. `VOLLEY-lab` makes the boundary hard. The separation exists to protect the freeze,
not as a filing preference.

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

## Amendment 3: regenerative recovery adopted into the Phase I baseline

**The dossier and [`../BASELINE.md`](../BASELINE.md) say** that Phase I deliverables develop
against a frozen baseline (§2), that the baseline moves only for an error correction, a
validation outcome against a pre-declared band, or a defect that makes a deliverable wrong, and
that **performance improvement is Phase II** — §5, *finished engineering before better
engineering*, which the adoption record calls "the hardest line in the document to hold".

**What was done instead:** regenerative braking was added to the Phase I design and its credit
taken into the baseline numbers.

**Authorisation:** programme author, 2026-07-31, explicitly and after the rule was put in front
of them.

### The two halves, because only one of them needed authorising

| | Route |
|---|---|
| **The analysis** ([`../../validation/A11_regen_braking.md`](../../validation/A11_regen_braking.md)) | **Error correction, no amendment needed.** `DECISION_LOG.md`, `RESULTS.md`, `SUMMARY.md`, `README.md` and `motor_model.py`'s docstring all assert that the sled's energy is not recoverable. The 2025 decision argued only that the motor cannot *arrest* the sled. The published claim is wider than its evidence, which is the defect class this repository logs as P-items |
| **The design change** | **Improvement. This amendment.** Adding a regen stator section downstream of release makes the machine better, not correct. Nothing in Phase I is wrong without it |

### The reasoning that decided it, and the argument against

**For.** The sled carries 44.8 % of every shot into the brake, the largest single loss in the
machine. A11 puts about a quarter of it back inside the existing envelope, at the existing
sheet-current rating, with peak current below the shot's own. A deployer whose thesis defence
includes "44.8 % is thrown away" when 23.6 % of it is retrievable with no envelope change is a
design that has to be defended rather than presented.

**Against, recorded because it is the stronger procedural argument.** This is exactly the
reasoning §5 exists to refuse. Every deferred item in [`../PHASE_II.md`](../PHASE_II.md) had a
sponsor who thought it was worth the exception, and PII-1 recovers the entire velocity shortfall
for 1.5 % of shot energy — a better return than this one — and still defers. **The honest
alternative was to open PII-11 and leave it there.**

The author chose adoption. That choice is recorded here rather than absorbed into a commit
message, so that a reader who disagrees can see precisely what was traded and by whom.

### The risk this creates, and its mitigation

**The risk is precedent, not physics.** The improvement/correction boundary is what the baseline
is made of, and `BASELINE.md` says so in terms: *"If that distinction ever bends toward whichever
is easier, the baseline has stopped meaning anything."* This is the first time it has been
crossed by authorisation rather than by type, and the second time is always easier than the
first.

Four things bound it:

1. **Scope.** This amendment authorises one item. It does not reopen PII-1 through PII-10, and
   it is not a general licence to promote improvements. Any further promotion needs its own
   numbered amendment with its own argument, and the argument may not be "Amendment 3".
2. **The bands gate the change.** A11's acceptance bands were committed in `6606567`, before the
   sweep. **If the run misses them, the design change does not happen** and this amendment
   lapses. An authorised change that is also allowed to move its own target is not a change
   control, it is a formality.
3. **`v_exit` must not move.** Regeneration acts after release. If 16.537 m/s changes by so much
   as a rounding digit, the model has coupled the loss ledger to the performance claim and the
   change is reverted rather than explained.
4. **The packaging question stays open.** The 240 mm of stator is assumed to fit the arrest
   section; no fin or ring-spring layout has been drawn against it. That stays a Phase I defect,
   recorded as one. Adopting the electromagnetic result does not adopt a mechanical design
   nobody has done.

---

## What has *not* been amended

The parts of the dossier that constrain rather than enable are unchanged and binding:

- **§2**: Phase I deliverables develop against a frozen baseline; fundamental redesigns defer.
- **§4**: the flagship is a deliverable and its stability is a design requirement. It is not
  split or substantially reorganised.
- **§5**: *finished engineering before better engineering.* The hardest line in the document
  to hold, and the reason the baseline exists. **Amendment 3 is a scoped, recorded departure
  from it and the only one.** Everything else deferred stays deferred.
- **§7**: every feature needs a path toward validation.

## How to record the next amendment

Add a numbered section: what the dossier says, what was done instead, who authorised it, the
reasoning, and the risk it creates with its mitigation. **Do not edit the dossier.** A
governing document that quietly changes to match practice is not governing anything.
