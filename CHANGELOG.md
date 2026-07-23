# Change log / audit record

Every change made to this repository after the initial export is recorded here, so that
each edit can be traced to a cause and a source of truth. This file is deliberately
exhaustive: it exists to be audited later.

Read alongside `PROVENANCE.md` (who originated what), `OPEN_PROBLEMS.md` (the defect
list these changes close) and `docs/DECISION_LOG.md` (why design choices were made).

## Provenance markings (same convention as PROVENANCE.md / INVENTORY.md)

- `[ME]`   — directed, decided, or supplied by the project owner (Adityavardhan Mishra)
- `[YOU]`  — executed / drafted by the AI assistant (Claude), not independently re-verified
- `[BOTH]` — owner directed and set the rule/judgment; AI executed the edit

**Standing caveat.** Every edit below was executed by the AI assistant under the owner's
direction. The owner set the rules (scripts are the source of truth; fix the paper, not
the scripts; keep the repo private) and the P1 reframing judgment. The owner has **not**
independently re-derived any number. No change here has been checked by hardware, FEA, or
third-party review.

---

## Session 2026-07-23 — reproduction check, paper corrections, repo hygiene

Worked in four phases, stopping for owner review at each boundary. Environment: macOS
(arm64), Python 3.9.6 in a local `.venv`, `numpy 2.0.2`, `magpylib 5.0.1`. PDF rebuilt
with `tectonic 0.16.9` (no system TeX was present).

### Phase 1 — Reproduction verification (no files changed)

Ran all five scripts in `analysis/` from a clean `.venv` and regenerated
`analysis/results/*.json`. Compared every output against the README headline table and
every value quoted in `paper/paper.tex`. Result: all script numbers reproduce; the paper
disagreed with the scripts in the places already listed as P1–P4, plus one additional
current-density value. No file was edited in this phase. Full comparison table was
delivered to the owner in-session.

### Phase 2 — Paper corrections (`paper/paper.tex`)

Rule applied throughout: **the scripts are the source of truth. Where the paper and a
script disagreed, the paper was changed to match the script; no script was edited to
match the paper.**

| ID | Location (section) | Cause | Removed → Added | Source of truth | Prov. |
|---|---|---|---|---|---|
| P2-01 | V-C Deployment Safety | **P1.** Quoted conjunction minimum belongs to a superseded operating point AND is not a robust quantity (swings 4.6→63 km over ±2.5% ejection velocity). | Removed the "45.3 km minimum / 52 km median / 5.8 km sat-sat / 347 km pre-disposal" framing. Added a reframing around the robust **8.1-day phase realignment**, an explicit statement that the minimum is a near-resonant beat sample (varies "below 5 km to above 60 km"), **mandatory per-shot COLA**, and **host-stage disposal before first realignment** as the mitigation. | `analysis/astro.py` (`conjunction()` → 8.1 d); velocity sweep from `OPEN_PROBLEMS.md` P1 table (4.6–63.4 km). 5.8 km and 347 km were **not traceable** to any current script output and were dropped rather than reconstructed. | [BOTH] |
| P2-02 | V-A Launch Performance | **P2.** Peak current belongs to the superseded 130 kA/m point. | `323 A` → `392 A` | `analysis/motor_model.py` `shot()` → `I_peak = 391.7 A` | [BOTH] |
| P2-03 | IV-A Field Model **and** XIII EMC | **P3.** Far-field stray values at 20/50 mm did not reproduce (10 mm did). | `4.7 mT` → `4.3 mT` (20 mm); `1.0 mT` → `0.4 mT` (50 mm), both occurrences | `analysis/verify_field.py` → `stray_field {20mm: 4.3, 50mm: 0.4}` | [BOTH] |
| P2-04 | III-F Arrest **and** XI Thermal | **P4.** Fin rise stated as 37 K "per shot"; that is the 12-shot campaign-adiabatic total. Per-shot is 3.0 K. | `37 K per shot` → `3.0 K per shot`; 37 K recast as the campaign-adiabatic bound relieved by inter-shot radiation, both occurrences | `analysis/sizing.py` `thermal_campaign()` → `fin_adiabatic_dT_K = 3.0` (×12 = 36.5 ≈ 37 K) | [BOTH] |
| P2-05 | IV-B Thrust Constant | Additional discrepancy found in Phase 1: copper current density. Paper's 23 A/mm² is the density at the 140 kA/m *rating*; the script emits the *commanded operating* density. | `140 kA/m (23 A/mm² …)` → `140 kA/m and commanding 126 kA/m (21 A/mm² …)` — corrects the density to the emitted value and removes the 140 kA/m ↔ 23 A/mm² arithmetic inconsistency | `analysis/motor_model.py` `shot()` → `J_Amm2 = 21.0`; `K_nom = 126 kA/m` (`sizing.py` `magnet_temperature`) | [BOTH] |
| P2-06 | preamble | **Build bug, not a claim.** `\graphicspath{{figs3/}}` pointed at a directory absent from the repo; the shipped `.tex` could not compile from a clean checkout (figures are in `paper/figures/`). | `\graphicspath{{figs3/}}` → `\graphicspath{{figures/}}` | Repo layout (`paper/figures/`) | [YOU] |

**Not changed — a Phase-1 false flag, corrected here for the record.** The thermal
prose lists "160 J in the supercapacitor ESR." This was initially reported as
unsourced. On reading `analysis/sizing.py` it is the `Q_esr=160` default in
`thermal_campaign()`, consistent with the 23.6 kJ campaign total and with
`energy_closure()` (ESR loss is internal to the cells, additional to the 2630 J
delivered at the bank terminals). **The value is correct; no edit was made.**

#### Figure

| ID | Artifact | Cause | Action | Source of truth | Prov. |
|---|---|---|---|---|---|
| P2-07 | `paper/figures/F06_conj.png` | The committed plot was generated by `legacy/make_figs.py` at `dv = 25.0 m/s` — an operating point matching neither the rated 20.37 m/s nor the superseded 20.65 m/s — and headlined a hard "fleet minimum = X km" annotation, contradicting the reframed P2-01 prose. | Regenerated at the rated 20.37 m/s driven by `analysis/astro.py`'s own `propagate()`/`boosted_elements()`; reframed to show the range beat and the 8.1-day realignment, with no single-minimum headline. Only the PNG artifact changed; the generator lives in the working scratchpad, matching the repo convention (committed PNGs, no in-repo figure generators). | `analysis/astro.py` (realign 8.06 d ≈ 8.1 d) | [YOU] |

#### Build

| ID | Action | Detail | Prov. |
|---|---|---|---|
| P2-08 | Rebuilt the PDF | `tectonic 0.16.9` compiled `paper.tex` → PDF (749 KB, no errors; only cosmetic underfull-hbox warnings). Written to the canonical `paper/EMOCD_IEEE_Conference.pdf` (see P3-04). | [YOU] |

### Phase 3 — Repository hygiene

| ID | File | Cause | Removed → Added | Prov. |
|---|---|---|---|---|
| P3-01 | `analysis/astro.py` (docstring) | The docstring claimed "conjunction min (12 shots) 45.3 km" — a stale comment its own code contradicts (computes 4.6 km). Comment only; no computed value changed. | `45.3 km sat-stage, resolved at 0.25 s` → `4.6 km min / 12.3 km median at 20.37 m/s -- fragile`; realignment line annotated as the robust quantity | [YOU] |
| P3-02 | `README.md` | (a) Reproduce command omitted `sizing.py`. (b) "Known issues" described P1–P4 as unresolved. | (a) Added `sizing.py` to the run chain. (b) Rewrote to state the four were corrected 2026-07-23, pointing to this log and `OPEN_PROBLEMS.md`. | [BOTH] |
| P3-03 | `CLAUDE.md` | Ground-rule 3 and the work queue described P1–P4 as open. | Updated both to past tense with a pointer to this log; next open items are E1/E3/E4. | [BOTH] |
| P3-04 | `.gitignore`, `paper/` | `.venv/` and the transient `paper.pdf` were not ignored; two PDFs of the same document existed (one stale). | Added `.venv/`, `venv/`, `*.toc`, `*.bbl`, `*.blg`, `paper.pdf` to `.gitignore`. Refreshed `paper/EMOCD_IEEE_Conference.pdf` with the corrected build (P2-08) and removed the transient `paper.pdf`. | [YOU] |
| P3-05 | `OPEN_PROBLEMS.md` | P1–P4 were still listed as open defects. | Added a top-of-section RESOLVED status block and a per-item "RESOLVED 2026-07-23 — see CHANGELOG.md" line. The original defect descriptions are retained in full for the audit trail. | [BOTH] |
| P3-06 | `CITATION.cff` | No machine-readable citation metadata existed. | Added a CITATION.cff (author, affiliation, title, TRL/design-study caveat). | [YOU] |
| P3-07 | `LICENSE`, `CITATION.cff` | Owner chose **MIT** (2026-07-23), aware it interacts with the unresolved patent/disclosure question (`OPEN_PROBLEMS.md` E14) and that it only takes effect on sharing. MIT chosen over Apache-2.0 to avoid an explicit patent grant. | Added MIT `LICENSE` (© 2026 Adityavardhan Mishra); set `CITATION.cff` `license: MIT`. | [ME] |

**Scripts verified to run standalone** from a clean checkout: all five write to
`analysis/results/` via `os.makedirs('results', exist_ok=True)` and require only
`numpy` + `magpylib` (matplotlib/scipy pulled transitively). Run from `analysis/`.
No CI, tests, or other tooling was added.

### Phase 4 — Git and GitHub (completed 2026-07-23)

`git init` with a repo-local identity (Adityavardhan Mishra
<adityavardhanmishr@gmail.com>). History was built as four logically separable commits:

1. `Baseline: EMOCD design-study repo as exported` — 47 files, pre-audit state (original
   paper with the P1–P4 defects intact, so the corrections show as real diffs).
2. `fix(paper): correct P1-P4 and current density against the scripts` — 3 files
   (paper.tex, regenerated F06, rebuilt PDF).
3. `chore(repo): license, citation, audit log, gitignore, doc sync` — 8 files.
4. `docs: add status badges to README`.

Pushed to **https://github.com/aaaaaaaaaaaavm/EMOCD**, created **PRIVATE** and confirmed
private via API (`"private": true`) — the analysis scripts disclose the design operating
point and no provisional patent is filed (`OPEN_PROBLEMS.md` E14). **Visibility remains
the owner's decision.**

Repository presentation (owner-requested professional pass): set description; added 15
topics (cubesat, electromagnetic-launch, halbach-array, linear-synchronous-motor,
astrodynamics, …); disabled wiki and projects, kept issues; added honest static README
badges (MIT license, Python 3.9+, TRL 2–3, "model only, unverified"). No CI or fake
status badges were added.

---

## Open decisions

1. **LICENSE** — RESOLVED 2026-07-23: owner chose **MIT** (P3-07).
2. **Repo visibility** — stays **private** until the owner decides otherwise (E14).

## Known follow-ups not addressed this session

- The two remaining figure generators (`legacy/make_figs.py`, `legacy/c5b_conj.py`) are
  legacy and use `dv = 25.0 m/s`. Only `F06` was regenerated; other figures were not
  audited against the current operating point.
- `OPEN_PROBLEMS.md` E-items (E1 3-D field closure, E3 CAD, E4 hardware, E16 reference
  hygiene, …) remain open engineering, unchanged.
