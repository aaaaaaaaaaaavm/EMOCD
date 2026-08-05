# Architecture Decision Records

Required by the Engineering Programme Dossier and the TRB prompt. One file per decision, in a
fixed shape, so a decision can be audited without reading a narrative.

**[`../DECISION_LOG.md`](../DECISION_LOG.md) is not superseded.** It is the readable history
and remains the better document for understanding *how the project got here*. These records are
the structured view: what was decided, what else was considered, what it costs, and how it gets
validated. Where an ADR has a Context section, that prose usually came from the decision log.

## Template

```
# ADR-NNN, title

Status · Date · Phase
## Context, the forces at play, including what was not known
## Decision, what was decided, stated flatly
## Alternatives, what else was considered, and why it lost
## Consequences, what this costs, including the bad parts
## Validation, how we would find out this was wrong
```

**The Consequences and Validation sections are the ones that matter.** A record listing only
benefits is advocacy, not a decision record, and one with no validation path violates dossier
§7, every feature needs a path toward validation.

## Index

| ADR | Decision | Status | Phase |
|---|---|---|---|
| [001](001-electromagnetic-deployment.md) | Electromagnetic deployment instead of a spring | Accepted | Concept |
| [002](002-host-is-a-spent-upper-stage.md) | Host is a spent upper stage, not a free-flyer | Accepted | Concept |
| [003](003-linear-synchronous-motor.md) | Linear synchronous motor, not a coilgun | Accepted | **Load-bearing** |
| [004](004-ironless-stator.md) | Ironless stator | Accepted | I |
| [005](005-eddy-brake-not-regeneration.md) | Eddy-current brake; sled energy is dissipated | Accepted | I |
| [006](006-magnets-ride-the-sled.md) | Magnets ride the sled; the CubeSat is unmodified | Accepted | **Load-bearing** |
| [007](007-dual-transverse-cassettes.md) | Dual transverse cassettes | Accepted | I |
| [008](008-retention-gate.md) | Retention gate separates preload from release | Accepted | I |
| [009](009-coast-and-trim.md) | Coast-and-trim release zone | Accepted | I |
| [010](010-host-agnostic-interface.md) | Host-agnostic four-item interface | Accepted | I |
| [011](011-publish-publicly.md) | Publish publicly, defects included | Accepted | I |
| [012](012-adopt-measured-sled-mass.md) | Adopt the measured 9.445 kg sled | Accepted | I |
| [013](013-drop-invariance-claim.md) | Drop the lifetime-ratio invariance claim | Accepted | I |
| [014](014-fleet-setpoint-below-ceiling.md) | Fleet setpoint at 98.2 % of the open-loop ceiling | Accepted | I |
| [015](015-derive-not-paste.md) | Derive coupled values; never paste them | Accepted | I |
| [016](016-reconstructed-history.md) | Reconstruct git history with labelled dates | Accepted | I |
| [017](017-four-repositories.md) | Four repositories, two of them generated | Accepted | I |
| [018](018-programme-name.md) | VOLLEY is the programme name; EMOCD_ remains the part prefix | Accepted | Programme |
| [019](019-gen4-open-assembly-before-export.md) | Keep Gen4 open assembly separate from the Phase I baseline | Accepted | Gen4 transition |
| [020](020-inter-shot-cadence.md) | The inter-shot cadence is 1200 s, closing P31 | Accepted | Load-bearing |

Every decision in `DECISION_LOG.md` appears above. ADRs 012-018 record decisions that were
never written down anywhere before.
