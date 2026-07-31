# Change log / audit record

Every change made to this repository after the initial export is recorded here, so that
each edit can be traced to a cause and a source of truth. This file is deliberately
exhaustive: it exists to be audited later.

Read alongside `docs/PROVENANCE.md` (what stands behind each claim), `OPEN_PROBLEMS.md` (the defect
list these changes close) and `docs/DECISION_LOG.md` (why design choices were made).

---

## 2026-07-31 (second pass): the payload ladder, the market case, and the bank as the real constraint

Four pieces of work that share one finding: **the bank, not the winding, is what limits this
machine**, and three separate lines of enquiry arrived at it independently.

| ID | Item | Detail |
|---|---|---|
| PL-01 | **`analysis/payload_family.py`, and the packing counts corrected downward** | `PAYLOAD_CLASSES.md` carried four hand-typed tables whose counts were raw volumetric bounds, published alongside a note that realistic packing is 40–60 % of them and then quoted unadjusted. PocketQube 1P appeared as **546 per load and 0.14 kg per satellite**. The script calibrates packing efficiency against the one configuration laid out in CAD — the 3U case, where a volume ratio predicts 21 and the magazine holds 12 — and applies the same 56.2 % to every class: **326 and 0.236 kg**. `KILL_CRITERIA.md` threat 1 still closes, by 2–5x rather than 6x. The ladder now runs from chipsats to 12U, and classes beyond what a twelve-shot escapement and thermal case support are flagged rather than tabulated as available. |
| PL-02 | **A payload-class subsection in the paper** | Velocity is flat across the family because the sled is most of the moving mass; deployer mass per satellite moves by a factor of thirty. That is the answer to the cold-gas comparison and it turns on payload class, not on any machine parameter. Its three qualifications are in the section rather than beneath it. |
| MK-01 | **`docs/MARKET.md`** | Kept out of the paper deliberately. The number it turns on is not a forecast: of the 4,800-odd nanosatellites catalogued as of January 2026, about **222 carry propulsion**. The other 92 % did not decline propulsion because they had no use for orbital control. The CubeSat market projections are third-party research and the file tabulates five firms disagreeing — 15.6 to 18.3 % CAGR, USD 1.65 to 1.98 B, same market, same year — rather than picking one. Section 5 is where VOLLEY loses. Two sourced sentences and two references into the paper's introduction. |
| LV-01 | **`analysis/velocity_levers.py`, and the ranking inverts** | The lever table was hand-computed on 2026-07-28, before anything modelled bank ESR. The new column is the **highest bank ESR at which each lever's shot still completes**, bisected on the real integrator because the ceiling is set at the sagged voltage, not at 96 V. Two-layer stator draws **597 A and needs 39 mohm**; raised sheet current **749 A and 31 mohm**; as drawn, 347 A and 66 mohm. A single commercial string is 116–185. **No row in the table clears it.** |
| LV-02 | **PII-3 gated behind PII-7, in the entry criterion rather than in prose** | The two levers with the best electromagnetic case are the two that make the bank hardest to buy. `PHASE_II.md` now says PII-3 may not be reviewed before PII-7 closes. |
| LV-03 | **A modelling error in the old table, found by generating it** | The two-layer rows were reported at 42 A/mm² because nothing told the model the winding got thicker. It runs at 21, the same as today. The 2026-07-28 prose had this right and the arithmetic did not. |
| PI1-01 | **PII-1 re-modelled, and it compounds with regeneration** | Regeneration takes a fixed ~296 J over 240 mm of stator whatever speed the sled enters at, so the spring moves energy to the payload and regeneration takes its slice of what remains. Together: efficiency **21.2 to 31.6 %**, brake duty **1291 to 711 J**. Past what the superseded 4.86 kg design claimed, on a sled twice the mass. **It still defers**, and the file now states why the risk is not comparable to regeneration's. |
| LIT-01 | **The pulsed-power cluster, 2 entries to 29** | PII-7's entry criterion names this gap. Filled by database search rather than reference harvesting, and marked as a **different provenance** inside its own section: where the search did not return volume, issue or pagination, the fields are marked unverified rather than filled in plausibly. Two findings already sharpen P26 — end of life for these parts is a **two-fold ESR increase**, and −40 °C can **double ESR without shortening life**. |

**What authorised it.** PL-01 and LV-01/LV-03 are error corrections: published numbers that
disagreed with their own stated method. MK-01, PL-02 and LIT-01 add documentation and change no
baseline value. PI1-01 quantifies a deferred item and leaves it deferred. Nothing here needed an
amendment.

---

## 2026-07-31: the sled's energy stops being a write-off

A11 asked a question the record had closed without answering. The 2025 arrest decision
established that motor braking cannot *stop* the sled, which is true; five documents and one
docstring had turned that into "the sled's energy is not recovered", which does not follow and
was never argued. Braking regeneratively over the 240 mm the closed envelope allows past the
release point returns 296.6 J, 23.0 % of the sled's 1291 J.

| ID | Item | Detail |
|---|---|---|
| RG-01 | **Bands declared before the sweep, in `6606567`** | Eight of eight held. The one that mattered was "no interior optimum below the winding's rating": the braking pulse is 15.6 ms over 240 mm of stator against the shot's 157 ms over 1300 mm, so copper during regeneration is **15 J against the shot's 828**, and recovery rises monotonically with force to the rating. The intuition that resistive loss defeats regenerative braking is an intuition about long duty cycles. |
| RG-02 | **`motor_model.regen_brake()`, integrating from the shot's own end state** | Exit velocity and post-shot bank voltage are read from `shot()`, never typed, so this cannot be quoted against a stale operating point (P19). Charging solves `R I^2 + Vc I - P = 0`, the mirror of the discharge solve, so the ESR is paid in both directions rather than credited on the way back. `copper_coeff(length)` makes the energised-copper length a parameter, because it is the one modelling choice that moves the answer: the pessimistic 1.30 m convention gives 235.9 J and 20.68 % rather than 296.6 J and 21.16 %, and both sit inside the declared efficiency band. |
| RG-03 | **`sizing.py` follows on all four loss terms** | Brake duty 1291 to **952 J**, winding heat 828 to **843 J**, converter 97 to **113 J**, bank ESR 86 to **94 J**. `energy_closure()` now closes on the *net* draw, 2583 J accounted against 2584.6 J, with the sled's energy split three ways instead of dumped in one. Campaign heat 28.0 to **24.4 kJ**, bulk rise 2.1 to 1.8 K, fin transient 4.0 to 3.0 K. `_check_operating_point()` gained seven regen rows so the two scripts cannot fork. |
| RG-04 | **Exit velocity unchanged, and asserted rather than hoped** | 16.537 m/s. Regeneration acts after release, so it cannot reach back through it; `motor_model.__main__` raises if it does. That was band 6 and it is the one whose failure would have meant a modelling defect rather than a result. |
| RG-05 | **The old claim corrected in place, not deleted** | `DECISION_LOG.md`'s 2025 entry keeps its text and gains an amendment underneath it; `PROJECT_NOTES.md` keeps the line struck through; `RESULTS.md`, `README.md`, `SUMMARY.md`, `wiki/Home.md` and the Pages site each say what they used to say and why it changed. P25 exists because a retraction once reached four artifacts and none of the places asserting it. |
| RG-06 | **Distinguished from the 55 % claim this project already retracted** | A reader who remembers that correction will assume this is it returning. It is less than half the size, it is integrated against stator that has to be built, the copper it burns is subtracted, the brake still absorbs 952 J, and it has a run sheet. `RESULTS.md` says so at the point of the old retraction. |
| RG-07 | **P28 opened: the regen stator and the fin do not both fit** | 240 mm plus a 300 mm fin against a 339 mm arrest section. Thermally trivial, mechanically not: arrest in the remaining ~99 mm needs the eddy coefficient up 1.8x, which puts peak deceleration at 186 g against the 200 g cap protecting the magnet bonds. Logged rather than fixed by shortening `fin_mass` in a script, which is the hand-edit `validation/README.md` forbids. |
| RG-08 | **Paper, figures and baseline follow** | Abstract, prior-art comparison row, architecture, results, thermal and conclusion. `F08_brake.png` now draws both arrest stages from `regen_brake()` rather than a second copy of the physics. `docs/BASELINE.md` goes from 20 to **23 values**, gross and net draw now distinguished. The thermal section's stale 160 J ESR and 28.9 kJ campaign, which the 2026-07-30 propagation missed, are corrected in the same pass. |

**What authorised it.** Two different things, and only one needed authorising. The *analysis* is
an error correction, which `docs/BASELINE.md` admits into Phase I: a published claim was wider
than its evidence. The *design change* is an improvement, which the same rule puts in Phase II,
so it went through `docs/programme/ADOPTION.md` **Amendment 3** with the argument against it
recorded alongside the argument for. The amendment is gated on the bands declared in `6606567`:
had the run missed them, it lapsed.

---

## 2026-07-30 (propagation): the bank's own resistance enters the model

A8-R, the pulse simulation re-run at the current operating point, failed its energy-closure
band at 97.0 %. The gap was bank ESR dissipation, which the circuit deck carried and no
analysis script did. Propagated in the order the standing rule requires: scripts, then
figures, then paper.

| ID | Item | Detail |
|---|---|---|
| ESR-01 | **`motor_model.py` gains `R_ESR = 0.012` and a terminal-voltage current solve** | The load draws its power at the bank terminal, which sits `I*R` below the cell voltage, so the current is not `P/Vc`. Solving `R I^2 - Vc I + P = 0` gives it, the energy leaving the capacitor becomes `Vc*I` rather than `P`, and `I^2 R` is integrated into a new `Q_esr` output. **11 of 179 result fields moved, all electrical or thermal.** Energy drawn 2795.6 to **2881.2 J**, peak current 330.3 to **346.8 A**, sag 5.19 to **5.35 %**, efficiency 19.56 to **18.98 %**, campaign 28.9 to 28.0 kJ. |
| ESR-02 | **Exit velocity, acceleration, stroke time, dispersion, payload family, mass and cost are unchanged** | Checked rather than assumed. The commanded force and the moving mass are untouched, so the mechanical integration cannot move; anything else would have meant the change was wrong. `v_exit` holds at 16.537 m/s and the 3σ dispersion at 0.027 m/s. |
| ESR-03 | **A five-percent disagreement that had been recorded twice and explained wrongly** | A8 and A8-R both put the analytic model about 5 % below ngspice on peak current and attributed it to forward-Euler against trapezoidal integration. It was the missing ESR. Corrected, the model gives **346.77 A against ngspice's 346.8, agreeing to 0.01 %**, energy to 0.04 % and sag to 0.004 points. The number that sets the SiC device rating now has two independent methods behind it instead of one and an excuse. |
| ESR-04 | **`sizing.py` follows, and `energy_closure()` carries the term on both sides** | `E_DRAWN`, `SAG_FRAC` and a new `Q_ESR` constant track `motor_model`; `_check_operating_point()` gained a `Q_ESR` row so the two cannot fork. `thermal_campaign()`'s literal `Q_esr = 160 J`, flagged as unsourced during the P2 review and never sourced since, becomes the computed **85.6 J**: the placeholder was 1.9x high. |
| ESR-05 | **A closing energy budget was hiding the loss, and now says so** | The ledger read 100.0 % closure while omitting a real 86 J term, because the draw it balanced against came from the same model that omitted it. `docs/RESULTS.md` and the Pages site now state that closure tests arithmetic consistency and not physical completeness. This repository had been quoting it as evidence of both. |
| ESR-06 | **A retraction inside the entry that made the claim** | P24 first stated that the correction pushes the 6.0 F bank under its required capacitance, computed by raising energy while holding sag fixed. Energy and sag are the same physical quantity seen twice: evaluated consistently at 2881 J and 5.35 %, required capacitance is **6.00 F** and the bank was always correctly sized. Withdrawn in place. |
| ESR-07 | **Paper, front pages and generated artifacts follow the scripts** | `paper/paper.tex` abstract, results and conclusion; `README.md`, `SUMMARY.md`, `docs/RESULTS.md`, `docs/index.html`, `wiki/Home.md`, `docs/PRIOR_ART.md`, the profile README and the generated CV. `docs/BASELINE.md` regenerated. The energy pie charts gain an ESR slice. |
| ESR-08 | **E17 stays open, on the provenance rather than the modelling** | The 12 mΩ has no current source: it reaches this repository through a superseded computation note, and no cell datasheet has been checked against it. The modelling gap is closed; the sourcing gap is not, and the code comment says so at the constant. |

**What authorised it.** `docs/BASELINE.md`'s change-control rule admits error correction as a
Phase I change. This is one: the model was missing a term that exists in the hardware.

---

## 2026-07-23: reproduction check, paper corrections, repo hygiene

Worked in four phases, with a review at each boundary. Environment: macOS
(arm64), Python 3.9.6 in a local `.venv`, `numpy 2.0.2`, `magpylib 5.0.1`. PDF rebuilt
with `tectonic 0.16.9` (no system TeX was present).

### Phase 1: Reproduction verification (no files changed)

Ran all five scripts in `analysis/` from a clean `.venv` and regenerated
`analysis/results/*.json`. Compared every output against the README headline table and
every value quoted in `paper/paper.tex`. Result: all script numbers reproduce; the paper
disagreed with the scripts in the places already listed as P1, P4, plus one additional
current-density value. No file was edited in this phase. The full comparison
table is kept in the working notes.

### Phase 2: Paper corrections (`paper/paper.tex`)

Rule applied throughout: **the scripts are the source of truth. Where the paper and a
script disagreed, the paper was changed to match the script; no script was edited to
match the paper.**

| ID | Location (section) | Cause | Removed to Added | Source of truth |
|---|---|---|---|---|
| P2-01 | V-C Deployment Safety | **P1.** Quoted conjunction minimum belongs to a superseded operating point AND is not a robust quantity (swings 4.6 to 63 km over ±2.5% ejection velocity). | Removed the "45.3 km minimum / 52 km median / 5.8 km sat-sat / 347 km pre-disposal" framing. Added a reframing around the robust **8.1-day phase realignment**, an explicit statement that the minimum is a near-resonant beat sample (varies "below 5 km to above 60 km"), **mandatory per-shot COLA**, and **host-stage disposal before first realignment** as the mitigation. | `analysis/astro.py` (`conjunction()` to 8.1 d); velocity sweep from `OPEN_PROBLEMS.md` P1 table (4.6-63.4 km). 5.8 km and 347 km were **not traceable** to any current script output and were dropped rather than reconstructed. |
| P2-02 | V-A Launch Performance | **P2.** Peak current belongs to the superseded 130 kA/m point. | `323 A` to `392 A` | `analysis/motor_model.py` `shot()` to `I_peak = 391.7 A` |
| P2-03 | IV-A Field Model **and** XIII EMC | **P3.** Far-field stray values at 20/50 mm did not reproduce (10 mm did). | `4.7 mT` to `4.3 mT` (20 mm); `1.0 mT` to `0.4 mT` (50 mm), both occurrences | `analysis/verify_field.py` to `stray_field {20mm: 4.3, 50mm: 0.4}` |
| P2-04 | III-F Arrest **and** XI Thermal | **P4.** Fin rise stated as 37 K "per shot"; that is the 12-shot campaign-adiabatic total. Per-shot is 3.0 K. | `37 K per shot` to `3.0 K per shot`; 37 K recast as the campaign-adiabatic bound relieved by inter-shot radiation, both occurrences | `analysis/sizing.py` `thermal_campaign()` to `fin_adiabatic_dT_K = 3.0` (x12 = 36.5 ≈ 37 K) |
| P2-05 | IV-B Thrust Constant | Additional discrepancy found in Phase 1: copper current density. Paper's 23 A/mm² is the density at the 140 kA/m *rating*; the script emits the *commanded operating* density. | `140 kA/m (23 A/mm² …)` to `140 kA/m and commanding 126 kA/m (21 A/mm² …)`, corrects the density to the emitted value and removes the 140 kA/m ↔ 23 A/mm² arithmetic inconsistency | `analysis/motor_model.py` `shot()` to `J_Amm2 = 21.0`; `K_nom = 126 kA/m` (`sizing.py` `magnet_temperature`) |
| P2-06 | preamble | **Build bug, not a claim.** `\graphicspath{{figs3/}}` pointed at a directory absent from the repo; the shipped `.tex` could not compile from a clean checkout (figures are in `paper/figures/`). | `\graphicspath{{figs3/}}` to `\graphicspath{{figures/}}` | Repo layout (`paper/figures/`) |

**Not changed, a Phase-1 false flag, corrected here for the record.** The thermal
prose lists "160 J in the supercapacitor ESR." This was initially reported as
unsourced. On reading `analysis/sizing.py` it is the `Q_esr=160` default in
`thermal_campaign()`, consistent with the 23.6 kJ campaign total and with
`energy_closure()` (ESR loss is internal to the cells, additional to the 2630 J
delivered at the bank terminals). **The value is correct; no edit was made.**

#### Figure

| ID | Artifact | Cause | Action | Source of truth |
|---|---|---|---|---|
| P2-07 | `paper/figures/F06_conj.png` | The committed plot was generated by `legacy/make_figs.py` at `dv = 25.0 m/s` (an operating point matching neither the rated 20.37 m/s nor the superseded 20.65 m/s) and headlined a hard "fleet minimum = X km" annotation, contradicting the reframed P2-01 prose. | Regenerated at the rated 20.37 m/s driven by `analysis/astro.py`'s own `propagate()`/`boosted_elements()`; reframed to show the range beat and the 8.1-day realignment, with no single-minimum headline. Only the PNG artifact changed; the generator lives in the working scratchpad, matching the repo convention (committed PNGs, no in-repo figure generators). | `analysis/astro.py` (realign 8.06 d ≈ 8.1 d) |

#### Build

| ID | Action | Detail |
|---|---|---|
| P2-08 | Rebuilt the PDF | `tectonic 0.16.9` compiled `paper.tex` to PDF (749 KB, no errors; only cosmetic underfull-hbox warnings). Written to the canonical `paper/VOLLEY_IEEE_Conference.pdf` (see P3-04). |

### Phase 3: Repository hygiene

| ID | File | Cause | Removed to Added |
|---|---|---|---|
| P3-01 | `analysis/astro.py` (docstring) | The docstring claimed "conjunction min (12 shots) 45.3 km", a stale comment its own code contradicts (computes 4.6 km). Comment only; no computed value changed. | `45.3 km sat-stage, resolved at 0.25 s` to `4.6 km min / 12.3 km median at 20.37 m/s -- fragile`; realignment line annotated as the robust quantity |
| P3-02 | `README.md` | (a) Reproduce command omitted `sizing.py`. (b) "Known issues" described P1, P4 as unresolved. | (a) Added `sizing.py` to the run chain. (b) Rewrote to state the four were corrected 2026-07-23, pointing to this log and `OPEN_PROBLEMS.md`. |
| P3-03 | `docs/PROJECT_NOTES.md` | Ground-rule 3 and the work queue described P1, P4 as open. | Updated both to past tense with a pointer to this log; next open items are E1/E3/E4. |
| P3-04 | `.gitignore`, `paper/` | `.venv/` and the transient `paper.pdf` were not ignored; two PDFs of the same document existed (one stale). | Added `.venv/`, `venv/`, `*.toc`, `*.bbl`, `*.blg`, `paper.pdf` to `.gitignore`. Refreshed `paper/VOLLEY_IEEE_Conference.pdf` with the corrected build (P2-08) and removed the transient `paper.pdf`. |
| P3-05 | `OPEN_PROBLEMS.md` | P1, P4 were still listed as open defects. | Added a top-of-section RESOLVED status block and a per-item "RESOLVED 2026-07-23, see CHANGELOG.md" line. The original defect descriptions are retained in full for the audit trail. |
| P3-06 | `CITATION.cff` | No machine-readable citation metadata existed. | Added a CITATION.cff (author, affiliation, title, TRL/design-study caveat). |
| P3-07 | `LICENSE`, `CITATION.cff` | Owner chose **MIT** (2026-07-23), aware it interacts with the unresolved patent/disclosure question (`OPEN_PROBLEMS.md` E14) and that it only takes effect on sharing. MIT chosen over Apache-2.0 to avoid an explicit patent grant. | Added MIT `LICENSE` (© 2026 Adityavardhan Mishra); set `CITATION.cff` `license: MIT`. |

**Scripts verified to run standalone** from a clean checkout: all five write to
`analysis/results/` via `os.makedirs('results', exist_ok=True)` and require only
`numpy` + `magpylib` (matplotlib/scipy pulled transitively). Run from `analysis/`.
No CI, tests, or other tooling was added.

### Phase 4: Git and GitHub (completed 2026-07-23)

`git init` with a repo-local identity (Adityavardhan Mishra
<adityavardhanmishr@gmail.com>). History was built as four logically separable commits:

1. `Baseline: VOLLEY design-study repo as exported`, 47 files, pre-audit state (original
   paper with the P1, P4 defects intact, so the corrections show as real diffs).
2. `fix(paper): correct P1-P4 and current density against the scripts`, 3 files
   (paper.tex, regenerated F06, rebuilt PDF).
3. `chore(repo): license, citation, audit log, gitignore, doc sync`, 8 files.
4. `docs: add status badges to README`.

Pushed to **https://github.com/aaaaaaaaaaaavm/EMOCD**, created **PRIVATE** and confirmed
private via API (`"private": true`), the analysis scripts disclose the design operating
point and no provisional patent is filed (`OPEN_PROBLEMS.md` E14). **Visibility remains
the owner's decision.**

Repository presentation: set description; added 15
topics (cubesat, electromagnetic-launch, halbach-array, linear-synchronous-motor,
astrodynamics...); disabled wiki and projects, kept issues; added honest static README
badges (MIT license, Python 3.9+, TRL 2-3, "model only, unverified"). No CI or fake
status badges were added. Added `docs/CONTRIBUTING.md` (provenance-first: scripts are the
source of truth, mark verification status, no reconstruction) and a GitHub issue template
for reporting reproduction discrepancies, both matching the repo's existing P-item
discipline. Tagged **v0.1.0** (annotated) and published a matching GitHub release, with
notes stating the design-study / unverified status up front.

---

## 2026-07-23: CAD integration (9 Fusion 360 documents)

Since the paper corrections above, the Fusion 360 CAD was completed (nine documents: Track, Stator, Sled, Payload_3U, Magazine_Cassette, Brake,
Interface_ESPA, **Enclosure (new)**, Assembly). This entry records the import of the
durable CAD artifacts and reconciles the repository's now-stale claims.

**Guardrail honoured: no number in `analysis/*.py` or `paper/paper.tex` was changed.** The
CAD is authoritative for **geometry and fit only**; the scripts remain authoritative for
**mass and performance** until FEA closes the open items. File-size report was reviewed
before committing; nothing approached 50 MB, so Git LFS was not used.

### Artifacts imported

| ID | Path | What | Source | Size |
|---|---|---|---|---|
| CAD-01 | `cad/step/*.step` (9) | STEP exports of all nine documents (8 parts + `EMOCD_Assembly`) | `~/Desktop/EMOCD_figs` | 1.8 MB total (largest: Assembly 1.3 MB) |
| CAD-02 | `cad/renders/*.png` (8) | Render set: `exterior_closed`, `exterior_aft_mounting`, `interior_open`, `exploded_view`, `seq1_stowed`...`seq4_braking` | `~/Desktop/EMOCD_figs` | 1.0 MB total |
| CAD-03 | `cad/parameters.json` | Geometry source of truth, 9 groups incl. the new `enclosure`; ESPA rebuilt as Ø460 ring flange / Ø400 bolt circle / 24 holes / hub / 4 gussets; brake as 15 mm tapered pole plates; envelope recorded as 1839x 530x 940 mm | CAD export (`files.zip`) | 12 KB |
| CAD-04 | `analysis/femm/emocd_cross_section.dxf` | 2-D magnetic cross-section (one wavelength, layers `MAG_*`/`BELT`) for FEMM analysis A1 | CAD export | 1.5 KB |
| CAD-05 | `analysis/femm/FEMM_RUN_SHEET.md` | Run sheet for the FEMM airgap-field check (A1, closes half of E1); distinct from and supersedes the older `docs/FEMM_Run_Sheet.md` | CAD export | 3.1 KB |

All CAD artifacts are **unverified by FEA or hardware** (`cad/parameters.json` itself
carries `PROVISIONAL_PENDING_FEA` flags and an incomplete final-verification note).

### Documentation reconciled (before to after)

| ID | File | Cause | Removed to Added |
|---|---|---|---|
| CAD-06 | `README.md` status line | "No hardware, no CAD, no FEA" is now false | to "CAD complete across 9 Fusion 360 documents with STEP exports committed (`cad/`); FEA and hardware still outstanding" |
| CAD-07 | `README.md` headline table | CAD sled mass (7.50 kg) implies a lower exit velocity than the 20.37 m/s headline, but the chassis is a first-pass 6 mm design with no FEA | Added a ⚠ note: figures assume the 4.86 kg parametric sled and are pending CAD structural reconciliation (P8; provisional ~17.88 m/s). **Computed numbers left unchanged.** |
| CAD-08 | `README.md` layout | New folders undocumented | Added `cad/` and `analysis/femm/` entries |
| CAD-09 | `OPEN_PROBLEMS.md` | P5, P10 absent | Added a "CAD reconciliation" P-section: **P5** sled mass 7.50 vs 4.86 kg; **P6** RESOLVED (CDS corner rails); **P7** brake past the 1500 mm release point; **P8** provisional 17.88 m/s pending FEA; **P9** envelope 1839 mm, ~44% over ESPA Grande; **P10** enclosure/radiator/avionics absent from `mass_properties.py`. Noted launch-lock geometry now exists (advances E10) and CDS corner rails modelled. |

---

## 2026-07-27: archived paper build, live CAD link

| ID | Item | Detail |
|---|---|---|
| ARC-01 | `paper/archive/EMOCD_submission_uncorrected.pdf` | Added an earlier compile of the paper, predating the 2026-07-23 corrections. It still carries the P1, P4 values (323 A peak current, 23 A/mm² at 140 kA/m, 37 K per-shot fin rise, 45.3 km conjunction minimum). Filed under `paper/archive/` with a README stating the deltas, so it cannot be mistaken for the current build. The canonical PDF remains `paper/VOLLEY_IEEE_Conference.pdf`. |
| ARC-02 | `cad/README.md` | Added the Fusion 360 web-view link (https://a360.co/4vSG6cb) under a "Live model" heading, noting that the committed STEP files and `parameters.json` (not the live model) are what the repository stands behind. |
| OP-01 | `OPEN_PROBLEMS.md` | Review pass. **P11 added (NEW):** the archived build still carries all four P1, P4 values and its filename says *submission*, if that is the version of record, P1, P4 are fixed only in this repo and need a corrigendum, not a commit. Flagged UNCONFIRMED pending an answer. |
| OP-02 | `OPEN_PROBLEMS.md` | **E3** retitled and rewritten: the "no CAD" half is closed by `cad/`, but masses are still parametric and unchecked against vendor data, and Fusion masses are proxies (solid copper / solid aluminium / steel for NdFeB) that cannot substitute. Points at P5, P8, P10. |
| OP-03 | `OPEN_PROBLEMS.md` | **E1** updated: the magnetostatic package now exists (`analysis/femm/`, superseding `docs/FEMM_Run_Sheet.md`) but has not been run; A1 closes the 2-D half only. **E2** names the two specified-but-unexecuted analyses (A1, A4). **E10** notes the launch-lock blocks now exist as CAD geometry. |
| OP-04 | `OPEN_PROBLEMS.md`, `CHANGELOG.md` | **E14** rewritten: the repository is public, so the disclosure decision is spent; what remains is the post-disclosure grace-period question and an explicit close-out if no filing is wanted. The stale "repo visibility stays private" open decision corrected to match. |
| OP-05 | `README.md`, `docs/INVENTORY.md`, `wiki/Home.md` | Open-problem summaries synced: P11 added, E1 noted as written-but-unrun, E14 reworded from "unresolved decision" to "disclosure already happened". |

---

## 2026-07-27: validation plan

| ID | Item | Detail |
|---|---|---|
| VAL-01 | `validation/` (new) | Cross-check plan: **A1** airgap field (FEMM), **A4** sled chassis structural (CalculiX/Code_Aster), **A5** lifetime and seeding (Orekit/GMAT), **A6** conjunction probability (NASA CARA), **A7** separation and tip-off (Project Chrono). Each names the P/E item it closes, its inputs from already-committed files, and its output JSON. **Nothing has been run**: this is a specification. |
| VAL-02 | `validation/README.md` | Sets the governing rule: the acceptance band is declared before the analysis runs, and every band traces to a current value in `analysis/results/*.json`. A missed band opens a P-item; it does not get widened. Licence note: GPL solvers stay external to this MIT repo. |
| VAL-03 | `validation/A4_sled_structural.md` | Highest-leverage item. Frames P5 as "what is the lightest chassis that holds the airgap to ±0.05 mm under 3.68 kN" rather than "what does the sled weigh", and fixes the decision rule in advance: ≤5.35 kg the parametric model stands; 5.35-6.80 kg both estimates are wrong and the scripts move; ≥6.80 kg **17.88 m/s becomes the headline** and the paper changes. |
| VAL-04 | `analysis/femm/FEMM_RUN_SHEET.md` | **Stale comparison targets corrected.** Run 3 told the operator to compare stray field against 22.7 / 4.7 / 1.0 mT, the 4.7 and 1.0 are pre-P3 values. Now 22.7 / 4.3 / 0.4 mT per `analysis/results/field_verification.json`. A run sheet carrying superseded targets is worse than none: it would have "confirmed" the wrong numbers. |
| VAL-05 | `docs/FEMM_Run_Sheet.md` | Marked **SUPERSEDED** at the top. Its ⟨B⟩ ≈ 0.62 T winding-gap target predates the winding-resolved model, which computes 0.552 T, so the sheet can no longer function as a test (this is what E1 flagged). Kept for the record. |
| VAL-06 | `docs/RELATED_WORK.md` (new) | Comparator literature and tooling, **explicitly marked as not retrieved and not read**, leads under the E16 rule, not citations. Flags Foster et al. (differential-drag phasing, flown Planet Labs results) as the one worth chasing first, since the paper's 25-day baseline is currently a model output rather than a measurement. |
| VAL-07 | `OPEN_PROBLEMS.md`, `README.md`, `docs/PROJECT_NOTES.md`, `wiki/Home.md` | Cross-references wired: P1 to A6, P5/P8 to A4, E1/E2 to A1, E6 to A5, E7 to A7, E16 to `docs/RELATED_WORK.md`. Layout sections updated for `validation/`. |

---

## 2026-07-27: repository-wide consistency sweep

Swept every committed `.md`, `.tex` and `.json` for values superseded by A27 (efficiency),
A28 (winding-resolved Kt), A29 (servo Monte Carlo), A30 (mass properties) and the P1, P4
corrections. Files that quote old values *deliberately*, `CHANGELOG.md`,
`OPEN_PROBLEMS.md`, `docs/PROVENANCE.md`, `paper/archive/`, `legacy/`, were left alone.

| ID | Item | Detail |
|---|---|---|
| FIX-01 | `docs/EMOCD_Computation_Results_C1-C10.md` | **Marked SUPERSEDED with an old to current mapping table.** It was presented as current computation notes while quoting a 4 kg sled at K = 45 kA/m: 22.4 m/s at 19.7 g, 463 A peak, 3σ 0.054 m/s to ±0.19 km, ⟨B⟩ 0.62 T. Worse, its efficiency line (52 %, crediting 55 % of sled KE as regeneration) is the **falsified** double-count that A25/A27 corrected to 32 %. Nothing deleted; the header states each delta and why. |
| FIX-02 | `docs/INVENTORY.md` | D5 flagged superseded; D8 repointed from `docs/FEMM_Run_Sheet.md` (superseded) to `analysis/femm/FEMM_RUN_SHEET.md` (current) with the band in `validation/A1_field_femm.md`. |
| FIX-03 | `.github/ISSUE_TEMPLATE/reproduction_discrepancy.md` | The worked example cited "paper/paper.tex Sec. V-A to 323 A", a defect fixed in P2-02, so the template implied the paper still carried it. Replaced with a neutral placeholder. |
| FIX-04 | `OPEN_PROBLEMS.md` | **P12 added.** The paper's Limitations section still says masses are "not detailed CAD", and the paper claims an ESPA-Grande-class envelope that P9 contradicts by ~44 %. Prose, not computed values; deliberately **not** edited in `paper.tex`, see the item for why (PDF/source drift, and P11 is unresolved). |
| FIX-05 | `docs/INVENTORY.md`, `wiki/Home.md` | Summaries synced for P11 and P12. |

**Checked and found consistent** (no action): the paper's field values against
`field_verification.json` (0.351 / 0.694 / 0.702 T, 22.7 / 4.3 / 0.4 mT, 0.55 T winding
mean); the paper's mechanical values against `sizing.json` (3.7 kN inter-array, 33 MPa,
9.5 kN arrest, 0.76 kN roller pair, 0.64 kN abort latch, 0.12 MPa bond, 109 Hz first
mode); the README and wiki headline tables against `motor_results.json` and
`astro_results.json`; every file path referenced in the docs.

---

## 2026-07-27: validation plan, second pass

| ID | Item | Detail |
|---|---|---|
| VAL-08 | `validation/A8_pulse_spice.md` (new) | Pulse-power chain under ngspice/PySpice. Bands: 391.7 A ±10 %, 4.88 % sag ±1.5 pts, 2634 J drawn ±5 %, 672 J copper ±15 %, 127.7 ms ±10 %, energy closure 98-102 %. Cheapest analysis in the plan (no geometry, no mesh, no licence) and it attacks three headline-adjacent numbers at once. |
| VAL-09 | `OPEN_PROBLEMS.md` **E17** (new) | The pulse-power chain has never left the analytic model. The 392 A peak, the 4.9 % sag, and the 672 J copper loss all rest on lumped R and ideal switching; no commutation overshoot has been computed, and the `Q_esr = 160 J` default has no second number against it. |
| VAL-10 | `OPEN_PROBLEMS.md` **E18** (new) | Conjunction covariance is invented. Any Pc result inherits it, so no Pc figure may be quoted except as conditional on its assumption until a real covariance is used. |
| VAL-11 | `validation/A5_astro_orekit.md` | Second leg added: reproduce the **measured** decay of 3-5 non-manoeuvring 3U CubeSats from CelesTrak / Space-Track TLE histories, band 15 % on time-to-decay. Two models agreeing is weaker than a model reproducing a flown decay. The 15 % follows published guidance that lifetime prediction tops out near 10 % of residual life. |
| VAL-12 | `validation/A6_conjunction_cara.md` | Covariance input changed from "documented assumption" to **Space-Track CDMs preferred**, assumption as explicit fallback. |
| VAL-13 | `validation/README.md`, `docs/INVENTORY.md`, `OPEN_PROBLEMS.md` E2/E6 | A8 added to the plan table; E-range updated to E1, E18; E2 and E6 cross-referenced to the new legs. |

**Checked, no item raised:** the paper already cites Inductrack (Post & Ryutov, IEEE Trans.
Appl. Supercond. 2000) in both the related-work section and the bibliography, so the
architectural prior art is covered and no E-item was needed for it.

---

## 2026-07-27: GMAT toolkit for A5 (and the A6 ephemeris input)

| ID | Item | Detail |
|---|---|---|
| GM-01 | `validation/gmat/` (new) | Script templates, a builder, and a parser for analysis A5. `emocd_lifetime.script.tmpl` propagates a baseline 450 km circular orbit against the boosted ellipse to a 120 km perigee under MSISE90 / 20x20 gravity / RK89, one script per solar-activity level. `emocd_fleet.script.tmpl` propagates the 12-shot fleet plus host stage for 30 days and writes one CCSDS OEM per object. **Nothing has been run.** |
| GM-02 | `validation/gmat/build_scripts.py` | Fills the templates from `analysis/results/astro_results.json` and **imports `boosted_elements()` and `_kepE()` from `analysis/astro.py`** rather than reimplementing them, so the orbit definition cannot fork between the two codes. Asserts the generated orbit equals `astro.py`'s exactly. Runs with no GMAT installed. Verified: a = 6864.790 km, e = 0.005339269, perigee back at the 450 km injection altitude. |
| GM-03 | `validation/gmat/parse_reports.py` | GMAT `ReportFile` to `validation/results/A5_astro.json`, applying the bands already declared in `validation/A5_astro_orekit.md` (multiplier ±5 %, invariance spread ≤5 %) with an explicit verdict. Exits non-zero on a miss, and the failure text says to open a P-item rather than edit `astro.py`. Absolute lifetimes are recorded but never judged (E6). |
| GM-04 | `validation/gmat/README.md` | Install and headless invocation, with the warning to **verify the run flags against the installed User Guide** rather than assume them, and to record the working command in the results JSON. Documents one real modelling gap: `astro.py` scales density 0.5/1.0/2.5 while GMAT takes F10.7 = 70/150/250, which are not equivalent, it affects the absolutes, not the ratio the band is on. |
| GM-05 | `validation/A6_conjunction_cara.md` | Ephemeris input changed from "export from `astro.py`" to the GMAT-generated OEMs, which replaces Kepler + secular J2 with a real integrator for the conjunction geometry. |
| GM-06 | `validation/A5_astro_orekit.md`, `validation/README.md`, `OPEN_PROBLEMS.md` E2/E6, `.gitignore` | GMAT named as the primary implementation with Orekit as substitute; A5 status now "toolkit built, not run"; `validation/gmat/output/` ignored as regenerable. |

**Scope note.** GMAT closes E6 and feeds A6. It does nothing for P5/P8 or E4, it validates
the consequences of a Δv, not the Δv itself, so A4 remains the highest-leverage analysis
in `validation/`.

---

## 2026-07-28: CAD generations imported, mixed/stubbed STEP set replaced

Source: `EMOCD_figs.zip` (three Fusion generations plus a 543-line `CHANGELOG_CAD.md`
auditing all three by direct Fusion API read). Body counts below were **measured on import**
with `grep -c MANIFOLD_SOLID_BREP`, not copied from the source changelog.

| ID | Item | Detail |
|---|---|---|
| CAD2-01 | `cad/step/` | **The committed set was replaced wholesale.** It matched no single generation and two files were stubs: the stator STEP held **1 solid** where Gen3 holds 162 conductors, and the ESPA interface held **1** where Gen3 holds 6 plus bolt holes. Others were mid-generation (sled 12, track 6, payload 5, assembly 225). Anyone opening the committed stator to check the winding layout would have found a block. Logged as **P13**, marked resolved by this import. |
| CAD2-02 | `cad/step/gen3/` | Current generation: 9 component files plus `EMOCD_Gen3.step`, the monolithic single-file model (395 solids, all nine sub-systems). Stator 162, sled 16, cassette 24, assembly 227. |
| CAD2-03 | `cad/step/gen2/`, `cad/step/gen1/` | Heritage, superseded, kept for the record as `legacy/` already is. Gen1 includes the pre-split `EMOCD_Deployer_Assembly_Gen1.step` and a second sled revision (`Sled_Gen1b`). ~11 MB across all three generations; no LFS needed. |
| CAD2-04 | `cad/CHANGELOG_CAD.md` | Imported verbatim, with a repository verification note added at the top recording what was checked against the exports on import. Nothing in the body was edited. |
| CAD2-05 | `OPEN_PROBLEMS.md` **P14** (new) | Five Gen3 defects that were never tracked here: cassette height 640 mm vs the 690 mm spec (G3-D1); track has no roller channels or guide flanges though `parameters.json` specifies them (G3-D2); stator layer count still open, Gen1 built two layers, Gen2/Gen3 one, and the x2 force vs x2 copper trade is uncomputed (G3-D4); Halbach arrays not re-centred after the chassis grew 360 to 488 mm (G3-D5); no payload-on-sled rigid joint in any generation (G3-D6). ESPA bolt holes recorded as **resolved** in Gen3 (G1-D5). |
| CAD2-06 | Verification findings | **Sled length fix confirmed:** Gen2 chassis half-length measures 180 mm (360 mm plate), Gen3 measures 244 mm (488 mm plate). **Brake placement fix not visible in the exports:** `EMOCD_Brake_Gen2.step` and `_Gen3.step` are geometrically identical (3 bodies and 79 points each, differing only in file name and time stamp) and *both* already place the brake at x = 1530-1740 mm, so the G2-D4 defect is not present in the file said to have it. Minor count deltas: Gen1 payload measures 5 solids where the inventory says 1; `Sled_Gen1b` measures 11 where it says ~16. |
| CAD2-07 | `cad/README.md` | Rewritten: three generations with status, what is authoritative, the six before-use rules, and the stub finding stated plainly rather than quietly fixed. |
| CAD2-08 | `validation/A4_sled_structural.md`, `A7_separation_chrono.md`, `validation/README.md`, `OPEN_PROBLEMS.md` P5 | Inputs repointed to `cad/step/gen3/*`. A4 gains an explicit note that Gen3 is the dimensionally corrected sled, meshing Gen2 would size a chassis that no longer exists. |
| CAD2-09 | `README.md`, `docs/INVENTORY.md` (C6, new C8), `docs/PROJECT_NOTES.md`, `wiki/Home.md` | Summaries synced to three generations with Gen3 current. |

The CAD-01 row in the 2026-07-23 block above described the set committed that day and is
left as written; this block supersedes it.

---

## 2026-07-28: visual pass: renders on the front page, STL viewer, Pages site

The repository had **no images anywhere**: eight 1920x1080 CAD renders and twelve result
figures were committed and shown on no page. Fixed across three surfaces, adding no claim
the repository does not already support and keeping every caveat intact.

| ID | Item | Detail |
|---|---|---|
| VIS-01 | `cad/stl/` (new) | GitHub renders `.stl` natively and does **not** render STEP, so the Gen3 assembly and sled were meshed with `gmsh` (OCC STEP reader) into browser-viewable binary STLs: assembly 50,692 triangles / 2.5 MB at a 40 mm mesh, sled 23,332 / 1.1 MB at 8 mm. `cad/stl/README.md` carries the regeneration command and states plainly that these are derived, non-authoritative meshes. |
| VIS-02 | Mesh verification | Each STL was bounding-box checked against its STEP source on generation. Sled matches exactly at 616x 172x 140 mm; assembly measures 1995 mm in X against a 1998 mm point-cloud bound on the STEP, the 3 mm being spline control points outside their own surface. |
| VIS-03 | `OPEN_PROBLEMS.md` **P14 / G3-D12** (new) | Found while meshing: the Gen3 assembly spans x = −188 to 1810 mm where `parameters.json` records −32 to 1807 mm. 156 mm of geometry sits aft of the recorded envelope, which makes the ESPA overrun ~57 % rather than ~44 %. |
| VIS-04 | `README.md` | Hero render above the badges; a 2x2 render gallery; a Mermaid ConOps flow (feed to gate to accelerate to coast/trim to release to brake to recover); two result figures beside the reproduce section; a validation-status table putting "nothing has been run" on the front page rather than three directories down; links to the spinnable STLs. |
| VIS-05 | `wiki/Home.md` | Same hero, gallery and ConOps diagram, with absolute `raw.githubusercontent.com` image URLs, since wiki pages cannot resolve repo-relative paths. |
| VIS-06 | `docs/index.html`, `docs/.nojekyll` (new) | A single self-contained landing page, dark/light aware, responsive, no framework, no build step and **no CI**, which keeps the "no CI by design" rule in `docs/CONTRIBUTING.md`. Assets are referenced from `../cad/renders/` and `../paper/figures/` so nothing is duplicated. Serves from `main` to `/docs` once Pages is enabled. |
| VIS-08 | `docs/index.html`, **defect fixed same day** | The site referenced its images as `../cad/renders/…`. Pages deploying from `main` to `/docs` publishes **only the contents of `docs/`** as the site root, so every `../` path pointed above the published root and all nine images plus the paper link would have 404'd on the live site while working fine locally. Switched to absolute `raw.githubusercontent.com` URLs, the same approach `wiki/Home.md` already used and for the same reason. |
| VIS-07 | Duplicate render found | `interior_open.png` and `seq1_stowed.png` are **byte-identical** (same MD5). The firing sequence is therefore three distinct frames, not four, and no gallery presents it as four. Worth regenerating a real stowed frame when the CAD is next opened. |

Every number on the new surfaces is copied from `analysis/results/*.json` or the existing
README table, and the P5/P8 caveat travels with the headline figures onto each one. A
prettier page must not become a more confident one.

---

## 2026-07-28: GMAT actually run, and native charts everywhere

| ID | Item | Detail |
|---|---|---|
| A5-01 | **GMAT R2022a installed and run headless** | `GmatConsole` on Linux, no missing libraries. Two script bugs fixed on the way: GMAT rejects any script containing non-ASCII characters with an error that does not name the line (an em dash in a comment), and it resolves relative `ReportFile` paths against `bin/../output`, not the working directory. `build_scripts.py` now guards the first and emits absolute paths for the second. |
| A5-02 | **Bounded 30-day leg** | Fitted decay rate −0.1618 km/day (GMAT) vs −0.1216 km/day (`astro.py`), GMAT decays **1.33x faster**. Expected: static exponential atmosphere vs MSISE90 at F10.7 = 150. Reported SMA is osculating with 12.2 km peak-to-peak short-period variation, several times the decay across the window, so the comparison is a least-squares rate over 31 daily samples, **not** a difference of endpoints. New template `emocd_sma_window.script.tmpl`. |
| A5-03 | **Full decay, high activity, the x1.80 claim holds** | Baseline 144.51 days, boosted 250.03 days, multiplier **1.7302**, deviation **−3.88 %** against the ±5 % band declared before the run. An independently implemented force model reproduces the headline astrodynamics claim. The absolute baseline lifetime does *not* agree (144.5 days vs 190), exactly the 1.33x rate difference, and exactly what E6 says to expect. Mean and low activity still propagating. |
| A5-04 | Parser hardened | `parse_reports.py` read a decay file GMAT was still writing, treated the partial decay as final, and emitted a confident `FAIL`. It now requires the 120 km floor (or the 40-year cap) to have been reached before reporting a multiplier, and distinguishes "not run" from "in progress". Also handles GMAT re-emitting headers mid-file. |
| VIS-09 | `docs/RESULTS.md` (new) | Chart hub, everything drawn by GitHub from text: energy budget (Mermaid `pie`), conjunction fragility, payload family, seeding, stray field, sled-mass decision thresholds, validation dependency graph, and the GMAT comparison. Each chart names the JSON field behind it. |
| VIS-10 | `README.md`, `wiki/Home.md`, `docs/index.html`, `validation/README.md` | Energy pie and conjunction fragility inlined on README and wiki; the Pages site gets pure CSS/HTML bar charts (no images, no JS); validation status tables updated to show A5 as run. |

**No number was invented.** Charts for unrun analyses show an explicit "specified" state; no
placeholder curves, no "expected" lines. The one genuinely new result (GMAT) was produced
by running the tool, not by estimating what it would have said.

---

## 2026-07-28: validation run against every claim

Four analyses actually executed; three could not be. Full account in
[`docs/VALIDATION_REPORT.md`](docs/VALIDATION_REPORT.md).

| ID | Item | Detail |
|---|---|---|
| VAL2-01 | **Reproducibility, passes** | All five `analysis/` scripts re-run from a clean copy with an empty `results/`, output compared field by field against the committed JSON: **173 values, 173 identical, 0 differing.** The reproducibility claim (D12) holds today. |
| VAL2-02 | **A5 GMAT, the x1.80 claim holds**: ⚠️ **SUPERSEDED 2026-07-28 by A5-01 below: the low-activity run finished and the invariance claim FAILS. The entry is left unedited because it is the audit record of what was believed with two levels of three in hand.** | Mean activity 1.7750 (−1.39 %), high activity 1.7302 (−3.88 %), both inside the ±5 % band declared before the run. **Invariance spread 2.55 %**, inside ≤5 %. An independently implemented force model reproduces the claim the paper actually defends. Low activity still propagating, and early state (4.1 years elapsed, still at 401 km, against `astro.py`'s 2.61-year total) suggests GMAT decays *slower* there, opposite to the other two levels. Not a result until it finishes. |
| VAL2-03 | **A5, absolute lifetimes do not agree, as E6 predicted** | GMAT 144.5 days against `astro.py`'s 190 at high activity. The bounded 30-day window measured the same 1.33x rate difference independently, and 190 ÷ 1.33 ≈ 143 reconciles the two. |
| VAL2-04 | **A8 ngspice, all bands met, two findings** | Exit velocity and pulse duration agree to 0.03 % across two different integrators. **Finding:** `motor_model.py` reports capacitor state-of-charge sag (4.88 %) and models no ESR; terminal voltage droops to 86.16 V, a 10.25 % total sag, and the dispersion claim's headroom argument is stated against the smaller figure. **Finding:** ∫I²dt = 8008 A²s gives 96 J of ESR loss at 12 mohm against the `Q_esr = 160 J` default, consistent only at ~20 mohm. E17 updated; original text kept. |
| VAL2-05 | **P15 (new, HIGH), the sled is heavier than either estimate** | Exact OCC solid volumes from `EMOCD_Sled_Gen3.step` times material densities give **9.445 kg**, against 4.86 kg parametric and the 7.50 kg quoted in P5. Exit velocity falls to **16.53 m/s**. The method reproduces P8's 17.88 m/s exactly when fed 7.50 kg, so the discrepancy is in the mass, not the method. Not the structural FEA A4 specifies (plates are drawn solid, pocketing would reduce it) but past A4's own 6.80 kg threshold either way. |
| VAL2-06 | Tooling committed | `validation/spice/emocd_shot.cir` (A8 netlist), `validation/results/A5_astro.json`, `validation/results/A8_pulse.json`. |

**Not run, and recorded as not run:** A1 (FEMM is Windows-only; no magnetostatic solver was
set up, so Kt = 11.22 N per kA/m remains single-method), A4's structural half, A6 (needs a
covariance that does not exist, E18), A7 (Project Chrono unavailable here). Nothing in this
block is inferred from an analysis that did not happen.

**No script or paper value was changed.** The standing rule applies: record the discrepancy,
run the analysis, then propagate once.

---

## 2026-07-28: exit-velocity options, and where this sits against what flies

| ID | Item | Detail |
|---|---|---|
| OPT-01 | `docs/DESIGN_OPTIONS_exit_velocity.md` (new) | Every lever for recovering 20.37 m/s at the measured 9.445 kg sled, computed by driving `motor_model.py` with modified inputs, the repo's own field model and integrator, no new physics. **Marked exploration, not a result.** Mass reduction alone tops out at 18.68 m/s with 60 % of the titanium pocketed. **Thinning the magnets moves backwards** (6 mm gives 15.68 m/s) because the Halbach field decays as e^(-ky) faster than the mass comes off. Raising sheet current to 213 kA/m works at J = 31.9 A/mm² against 21 today. Lengthening the stroke to 1.97 m works and adds 673 mm to an envelope already 44 % over ESPA. |
| OPT-02 | Two-layer stator costed for the first time | Doubling the winding widens the magnetic gap 12 to 22 mm and drops Kt from 11.22 to 7.46 N per kA/m, but sheet current doubles at unchanged current density: **20.61 m/s at 7.50 kg, J still 21 A/mm²**. The stator does not ride the sled, so its copper costs dry mass (P10), not velocity. Costs: copper loss doubles, peak current ~580 A against 392, which collides with the A8 ESR finding. This is the first time G3-D4's open decision has had its electromagnetic consequence computed. |
| OPT-03 | Reconciliation hypothesis for P5 vs P15 | Pocketing 40 % of the titanium gives 7.50 kg and 17.88 m/s, **exactly** P5's and P8's figures. The 7.50 kg may never have been the as-drawn mass but an estimate with lightening assumed, in which case P15 and P5 are the same design before and after pocketing. Flagged as an inference to check against the CAD Master Plan, not as a finding. |
| LAND-01 | `docs/LANDSCAPE.md` (new) | Comparison against fielded deployers (P-POD, ISIPOD, NRCSD, CSD, EXOpod) and transfer vehicles (ION, Vigoride). VOLLEY carries **6.0 kg of deployer per 3U satellite** against roughly 2 kg per U for canisterized dispensers, the same mass class, which is the genuinely favourable result. Against that: tip-off and dispersion advantages are **unproven** (A7 unrun, E7 assumed sensor noise), springs need no power at all, and the machine does not currently deliver the velocity it advertises. Competitor figures are marked unverified under the E16 rule. |

No script or paper value changed.

---

## 2026-07-28: A4 structural run, and the front pages corrected to match

| ID | Item | Detail |
|---|---|---|
| A4-01 | **A4 structural leg RUN** (CalculiX ccx 2.21) | Quadratic-tet FE of one 488x140x6 chassis plate taken straight from `cad/step/gen3/EMOCD_Sled_Gen3.step` (29,312 nodes, 143,930 C3D10) under the 3672 N Maxwell attraction from `sizing.json`. Support bracketed pinned vs clamped because the real web joint is between. **All three declared bands pass: 0.0194 mm airgap closure against a 0.025 mm per-plate budget (78 %), 33.7 MPa against 587 allowable (17x margin), first mode 3408 Hz against >200.** |
| A4-02 | What A4 did *not* settle | It answers "does the drawn chassis meet the constraint" (yes) rather than "what is the lightest chassis that does". Uniform thinning is nearly worthless, deflection goes as 1/t³, budget spent at ~5.5 mm for 0.30 kg, moving exit velocity 16.53 to ~16.7 m/s. Real reduction needs a rib-stiffened redesign that nothing has evaluated, so the 60 % pocketing row in `docs/DESIGN_OPTIONS_exit_velocity.md` is **unsupported**. The decision rule's ≥6.80 kg branch stands. |
| A4-03 | Deck bug worth recording | First run failed with `nonpositive jacobian` on every element: gmsh's tet10 edge order is `{0,1},{1,2},{2,0},{3,0},{3,2},{3,1}` and CalculiX C3D10 wants nodes 9 and 10 the other way round. `build_deck.py` carries the mapping and a comment so the next person does not lose an hour to it. |
| A4-04 | `validation/fea/` (new) | `build_deck.py` regenerates both decks from the STEP; results in `validation/results/A4_sled_structural.json` with mesh, material, load, bands, and five stated idealisations. Run artifacts gitignored. |
| DOC-01 | **README, wiki and the Pages site now lead with the real number** | All three previously headlined 20.37 m/s with a caveat about a provisional 17.88, while `docs/VALIDATION_REPORT.md` said 16.5. A reader finding that gap themselves reads it as overclaiming; the front page saying it first reads as rigour. Each now carries the three-row mass/velocity table and the sentence "treat 20.37 m/s as an upper bound the current geometry does not support". The computed values are still left exactly as the scripts produce them. |

The standing rule held throughout: **no script or paper value was changed.** Discrepancy
recorded, analysis run, and the propagation into `analysis/*.py` still waits on a decision
about the chassis and the stator layer count.

---

## 2026-07-28: A5 completes, and falsifies the claim the paper calls its defensible one

| ID | Item | Detail |
|---|---|---|
| A5-01 | **A5 GMAT complete, verdict `FAIL`** | The low-activity leg finished: baseline 2359.1 d, boosted 4892.4 d, **multiplier 2.0739, +15.21 % against x1.80**, outside the ±5 % band. With high (1.7302) and mean (1.7750), the **invariance spread is 18.48 % against a ≤5 % band declared before the run.** The point value survives at mean and high activity; the *invariance* does not. `validation/results/A5_astro.json` regenerated and carries the FAIL. |
| A5-02 | **Mechanism identified and tested, not guessed** | `astro.py` models solar activity as a uniform multiplicative scale on density. Sweeping that scale over **40x** (0.25 to 10.0) moves the multiplier only 1.7992 to 1.7968, constant to 0.1 %. A uniform density factor divides both lifetimes by the same number, so **the ratio is invariant by construction of the model, not as a physical result.** MSIS changes the shape of the density, altitude profile with F10.7, the boosted orbit's apogee sits ~37 km higher, and the ratio then moves 1.73 to 2.07. Reproducible from `analysis/astro.py` `lifetime()` unedited. |
| A5-03 | **`OPEN_PROBLEMS.md` P16 (new, HIGH)** | Records the falsification, the 40x sweep table as evidence, and every location the claim appears, including the **abstract** of `paper/paper.tex` ("invariant across ballistic coefficient and a fivefold solar-activity density range"), Sec. V-B ("invariant to two decimal places") and Limitations, which calls the invariance "the defensible result". E6 updated: it warned the absolutes were weak, and now has to say the ratio is weaker than advertised too. |
| A5-04 | **Absolute-lifetime error changes sign** | GMAT is **2.5x longer** than `astro.py` at low activity, **9 % shorter** at mean, **23 % shorter** at high. E6 predicted absolute disagreement; it did not predict a sign change across the range. Same profile-shape effect, seen from the other side. |
| A5-05 | **Correction to my own text in `docs/VALIDATION_REPORT.md`** | Section 2 read "Invariance across activity: 2.55 % spread, inside the ≤5 % band" and "the claim the paper actually defends survives an independent propagator". Both were computed from two levels before the third finished, and both were wrong. Replaced with the three-level result and the mechanism, and the retraction is stated in place rather than quietly overwritten. |
| DOC-02 | Front pages corrected | `README.md` and `wiki/Home.md` headline rows now read "x1.80 at mean activity, **invariance falsified, see P16**" instead of "invariant across BC and solar activity"; README's validation summary rewritten around the four run analyses. `docs/RESULTS.md` A5 section replaced with the three-level table, a per-activity chart and the 40x-sweep chart; its status bar moved from `████████░░` "within band" to `██████████` **FAIL**. `docs/INVENTORY.md` A32 flagged against P16. |
| A5-06 | **`paper/paper.tex` deliberately not edited** | Four locations are affected (abstract, Sec. V-B, sensitivity, Limitations). Same reasoning as P12: no TeX engine is available here, editing without rebuilding splits the source from the committed PDF, and it is entangled with **P11**: which this makes urgent, because if the submitted build is the uncorrected one, the paper of record carries P1, P4 *and* a falsified abstract claim. Batched for one pass. |

Standing rule held: **no value in `analysis/` was changed.** The parser's own instruction on
a failed band is explicit (*"open a P-item; do not edit `analysis/astro.py`"*) and that is
what happened.

---

## 2026-07-29: review sweep: two falsifications, one new lever, four missing model terms

Three independent reviews of the repository, each verified against the code rather than the
prose before anything was written down. Every number below was recomputed here.

| ID | Item | Detail |
|---|---|---|
| REV-01 | **P16 extended, the BC half of the abstract is the same tautology** | The abstract claims the ratio is invariant across ballistic coefficient **and** solar activity. In `lifetime()` the drag term is `ft = -0.5 * rho(h, scale) * v**2 / BC`, so `scale` and `1/BC` are the **same multiplicative slot**. Reciprocal test: BC=61/scale=2.0 gives 1.7987 and BC=30.5/scale=1.0 gives **1.7987**; BC=122/scale=1.0 gives 1.7991 and BC=61/scale=0.5 gives **1.7991**. Plain BC sweep 30 to 150 kg/m²: spread **0.05 %**. So the position is not "one half falsified, one half untested", **neither half was ever tested by a method that could fail**, and the half that was independently checked did fail. |
| REV-02 | **P17 (new, HIGH), the A4 load input is 37 % high** | `sizing.py::inter_array_attraction()` gives 3672 N from a flat-plate Maxwell-stress formula; that number was the applied load in the CalculiX run. `magpylib.getFT()` on the repo's own `build_field()` geometry converges to **2686.6 N** (mesh (14,14,14), deltas −8.3/−4.3/−2.5 N, step-size independent 1e-5 to 1e-8). Mechanism: Maxwell stress needs mean(B²), the formula uses mean(B)², and mean(B²) ≥ mean(B)² by Jensen, so the analytic form must overestimate a non-uniform Halbach face. **A4's conclusions do not reverse** (the real load is lighter, margins widen); what fails is the claim that A4's inputs were checked. |
| REV-03 | `validation/magpylib/check_inter_array_force.py` (new) | Reproduces P17 in one command, no new dependency, magpylib 5.2.3 is already in `requirements.txt`. Documents the 3672 vs 3680 N provenance (`build_deck.py` multiplied the rounded 120.0 kPa by the footprint). |
| REV-04 | **Momentum-transfer release costed, a lever absent from the options table** | Every option costed so far accelerates sled and payload as one rigid mass. They need not separate at the same speed. A momentum-conserving spring push recovers the full headline shortfall for **41.8 J against a 2630 J shot (1.6 %)**, and brake duty *falls* 1291 to 1050 J. The binding constraint is the payload's 25 g qualification limit, not energy: at 25 g the kick is **15.6 ms over 42.7 mm of relative stroke at 981 N**, an ordinary spring, not a shock event. Against the stroke-lengthening row, which needs **673 mm** more envelope on a machine already 44 % over ESPA, this needs **43 mm** of guided rail. Written up as **exploration, not a result**; the tip-off objection is real and makes A7 load-bearing. |
| REV-05 | Mission-value framing added to the re-scope option | A **23 % velocity shortfall costs 9.7 % of the lifetime multiplier**, x1.624 at the as-drawn 16.54 m/s against x1.799 at 20.37. The re-scope case had been argued only in m/s, where it looks like a collapse. |
| REV-06 | **E19, E22 (new), four terms no script contains** | Distinct from "analysis not yet run". **E19** eddy-current heating *inside* the NdFeB blocks (`magnet_temperature()` models only reversible Br drift; the risk is irreversible knee-point demagnetisation, and it grows with the current-density option). **E20** the brake's force, time profile does not exist anywhere, only a 200 g cap used for bond sizing; a first-order estimate puts the average near 6 kN over 8-20 ms, ~4x the acceleration force, 24 load reversals per campaign through the ESPA joint. **E21** no vacuum tribology anywhere in the repo, four rollers at ~763 N per pair, reused twelve times, cold welding and galling unaddressed. **E22** parasitic eddy drag on track structure during acceleration; `thrust_constant()` models eddy coupling only where it is wanted. P18 added so these are visible from the P-list. |
| REV-07 | **Dhruva Space added to `docs/LANDSCAPE.md`** | The closest fielded comparator is Indian and was absent. DSOD family space-qualified on PSLV-C55 (22 Apr 2023), non-pyrotechnic HDRM, **< 2 m/s**, and (pointedly) **onboard telemetry for ejection-velocity measurement**, which is the quantity VOLLEY claims as its differentiator and currently has only as a model output. Deployer unit mass could not be retrieved (403), so no mass comparison is made; marked unverified under E16. |
| REV-08 | **A7's pre-declared acceptance band may be mis-sourced** | `validation/A7_separation_chrono.md` declares ≤5 °/s citing NRCSD-E. Snippets of the sibling NRCSD ICD (NR-SRD-029) give "less than two (2) deg/sec/axis" verbatim; the NRCSD-E PDF 403s so the variant is unconfirmed. **Flagged, not asserted**: but a band declared before a run is no protection if the band itself misquotes its source. To be checked by hand before A7 runs. |
| REV-09 | Two "blocked" verdicts corrected as overstated | **A1:** FEMM 4.2 runs under Wine (documented by the FEMM project; `py2femm` automates it), and Elmer / GetDP+Gmsh are native-Linux meshed FEM, a not-yet, not a cannot. **A7:** `pychrono` ships on conda-forge, not PyPI, so `pip install pychrono` fails by design; linux-64 is supported. Both corrected in `docs/VALIDATION_REPORT.md`. Recorded against them: for an *ironless* geometry magpylib's analytic superposition is essentially exact and already 3-D, so the weak link was never the field model, it was the closed-form expressions on top of it, which is exactly what P17 caught. **Radia is not worth pursuing** for A1; same solver family, no independence gained. |
| REV-10 | References upgraded from lead to verified | Foster et al. **both companion preprints are open-access** (arXiv 1806.01218, 1509.03270), so the highest-value modelled to measured swap has no paywall. Shambaugh, arXiv 2601.02453 (Jan 2026), verified: backtests lifetime prediction against **934 non-manoeuvring decayed satellites, 1961-2024**, reporting 12.4 % median error under fully predictive conditions. That supplies the accuracy band **E6 never had**: GMAT and `astro.py` differing 9-23 % on absolutes is near the state-of-the-art floor, not evidence either is broken, and it independently corroborates P16's mechanism by naming solar-cycle forecast error as dominant after ballistic coefficient. |
| REV-11 | A6 tooling risk removed | The 2-D Pc algorithm is a published closed-form integral, ~50 lines against the already-installed `scipy`, applied to the OEM ephemerides `validation/gmat/` already emits. No MATLAB, no Octave port. E18's covariance problem is untouched either way. |

**No value in `analysis/`, `cad/` or `paper/` was changed.** P17 in particular is logged as a
discrepancy rather than a correction, and it carries an explicit instruction not to edit
`sizing.py` on the strength of it, adopting a corrected formula would move the plate stress,
the retention-gate sizing and the A4 load together, and that is a propagation decision, not a
patch.

**Stated plainly because it inverts this project's own rule:** the P17 force was computed
*before* an acceptance band was declared for it. That is the wrong order, it is recorded as
such in the P-item, and proper closure still needs a run sheet with a band fixed in advance.

---

## 2026-07-29 (later): P11 resolved, and one review finding that was missed

| ID | Item | Detail |
|---|---|---|
| REV-12 | P11 RESOLVED, nothing has been submitted | Checked. There is no version of record, so P1, P4 are not loose in any published document and no corrigendum or erratum is needed. `paper/archive/EMOCD_submission_uncorrected.pdf` is a draft whose filename overstates its status. |
| REV-13 | **The paper edits are no longer blocked** | P12 and P16 were held out of `paper/paper.tex` because editing the source without rebuilding would split it from a published record. With nothing published, the only cost is a stale committed PDF until recompilation, a normal state for a draft. **Both should now be fixed in the source and the PDF rebuilt before any submission.** |
| REV-14 | **E23 (new), a review finding not covered by E19, E22** | `track_first_mode()` gives 48 Hz pinned / 109 Hz fixed and checks them only against a static launch-band target. The shot's own excitation sweeps from zero as `f = n·v/λ`, so every shot chirps through both modes: the 6th harmonic crosses 48 Hz at 3.7 ms and 0.7 mm of travel, and 109 Hz at 8.3 ms and 3.6 mm; the fundamental crosses 109 Hz at 49.8 ms. Twelve times per campaign, in the first millimetres of stroke. Probably benign (the sweep rate is ~2190 Hz/s, so transit is sub-millisecond) but that argument needs the structure's Q, and **no damping figure appears anywhere in the repository**. |

---

## 2026-07-29 (propagation): the first time a script value has moved

P11 resolved (nothing has ever been submitted) which removed the reason `paper/paper.tex`
was frozen. The measured sled mass was then propagated in the order the standing rule
requires: **scripts, then figures, then paper.**

| ID | Item | Detail |
|---|---|---|
| PROP-01 | **`analysis/` adopts the measured 9.445 kg sled** | Authorised by the rule in `validation/A4_sled_structural.md` declared *before* A4 ran: at ≥ 6.80 kg the headline changes and the paper changes materially. A4 has since run, all three structural bands pass, and P15 measured 9.445 kg from the Gen3 STEP solids. **55 of 179 result fields moved.** Exit velocity 20.372 to **16.537 m/s**, acceleration 16.26 to **10.72 g**, efficiency 31.5 to **19.6 %**, energy 2634 to 2796 J, copper loss 672 to 828 J, peak current 392 to 330 A, pulse 128 to 157 ms, multiplier x1.80 to **x1.62**, recoil 81.5 to 66.1 N·s, realignment 8.1 to 9.9 d, dry mass 72.3 to 76.9 kg. |
| PROP-02 | **The closed-loop Monte Carlo had silently saturated** | Its 20.0 m/s setpoint now sits above the open-loop ceiling, so `Kc` pinned at `K_RATED` and the run reported a 0.267 m/s "dispersion" that was really a 2.27 m/s shortfall. The setpoint moved to **16.2 m/s (98.2 % of the ceiling, the same fraction 20.0 held against the old 20.37**) so the headroom argument is unchanged rather than re-tuned to taste. Dispersion returns at 0.027 m/s. A guard now raises if the servo ever fails to reach its setpoint again. |
| PROP-03 | **Loss terms were pasted literals** | `sizing.py` hard-coded 672 J copper and 26 J auxiliary, so energy closure fell to 94.2 % on the first run after the change. They now derive from the operating point; closure is back to **100.0 %**. |
| PROP-04 | **Capacitor sizing quoted a droop the bank no longer meets** | 5.97 F was computed against a 4.9 % sag target; at 2795.6 J, holding 4.9 % needs **6.35 F**, which the selected 6 F bank does not provide. It sags 5.19 % instead. The function now derives from the sag actually reached, returns 6.0 F against 6 F selected, and reports the 6.35 F alternative rather than hiding it. |
| PROP-05 | **A fork guard, because the operating point was duplicated** | `M_SLED`, `V_EXIT`, `E_DRAWN`, `F_CMD` lived in both `motor_model.py` and `sizing.py`. `sizing.py` now asserts agreement against `motor_model`'s own JSON on six quantities and exits with a diagnostic if they drift. `mass_properties.py` keeps the parametric sled breakdown and carries the 4.59 kg measurement delta as its own line, so system dry mass no longer understates. |
| PROP-06 | **`paper/make_figures.py` (new)** | The committed figures had **no generator in the repository**: `legacy/make_figs.py` is at a superseded point and reimplements the physics instead of importing it, so the figures could not follow the operating point. All ten now regenerate from `analysis/`, with trace accessors added to the analysis modules (`shot(trace=True)`, `thrust_constant(profile=True)`, `conjunction(trace=True)`) rather than the physics copied into figure code. |
| PROP-07 | **F11 reframed, F09 given both bands** | F11's caption asserted the falsified invariance; it now plots `astro.py` against GMAT side by side, which shows P16 directly, the script series is flat across the whole activity range while GMAT moves 2.07 / 1.78 / 1.73. F09 draws both the 5 °/s line the paper cites and the 2 °/s wording in the sibling NRCSD ICD, since which applies is unresolved. |
| PROP-08 | **`paper/paper.tex` follows the scripts** | Abstract, results, family table, comparison and sensitivity tables, mechanical, thermal, cost and conclusion. Sec. III is *rewritten*, not renumbered: the design used to be acceleration-limited and is now thrust-and-mass limited with more than half its qualification margin unused, which changes what recovering velocity means. Sec. V-B drops the invariance claim and explains the defect. Limitations no longer offers that invariance as the defensible result. |
| PROP-09 | **P12 closed** | The ESPA-Grande envelope is no longer asserted as a capability, 1839 mm against ~1270 mm is stated and named an open packaging problem (P9). "Masses derive from a parametric solid model, not detailed CAD" is replaced by what the CAD measured. |
| PROP-10 | **A pre-existing build defect fixed** | `\ref{sec:opt}` pointed at a section that has never existed and would have rendered as "Sec. ??". The length trade it promised is now stated inline from `sizing.py`'s own sweep. |
| PROP-11 | **P19 (new, HIGH)** | Every validation run predates the operating point it validates. A5 and A8 were propagated at 20.37 m/s; A4 survives because its load is magnetostatic and velocity-independent. "Three of eight analyses have run" is really "three have run against a design that has since moved". |
| PROP-12 | **P5, P8, P15 closed; each keeps its original text** | P5 carries a caveat forward: 9.445 kg is the as-drawn, unpocketed geometry and A4 reports a 17x stress margin, so a rib-stiffened chassis would recover mass and nobody has designed one. That successor question moves to E2 and the roadmap. |
| PROP-13 | **`docs/ROADMAP.md`, `SUMMARY.md` (new); contact details** | Nineteen numbered defects only read as rigour if there is also a plan for closing them; without one a reader cannot tell mid-flight from abandoned. A1 is sequenced first because Kt is checked only analytic-against-analytic and everything is downstream of it. Dates are assumed from a standard Indian final-year calendar and the header says so. Contact details previously existed only in `CITATION.cff`. |
| PROP-14 | **Host-integration work surfaced** | The POEM and Vikram-1 analysis was at line 245 of the LaTeX, the most India-specific engineering in the project, invisible from the front page. Now in `README.md` and `SUMMARY.md`. |

**The committed PDF is knowingly stale.** No TeX engine is available in this environment, so
`paper.tex` was revised without recompiling. `paper/README.md` declares the divergence and
says how to rebuild; a silent split between source and PDF would be worse than either being
wrong alone.

---

## 2026-07-29 (blockers and gaps): three blockers cleared, three gaps closed

Re-checking the standing blockers found three of four had changed status. The environment,
not the problem, had been the obstacle.

| ID | Item | Detail |
|---|---|---|
| BLK-01 | Git history tidied | `git-filter-repo` installs from PyPI, so the rewrite that was previously blocked ran. A stray working-notes file was dropped from the three commits carrying it, and one commit message reworded. Verified: 37 commits preserved and the **tree hash byte-identical before and after** (`1435acc`), so no content moved, only history. Force-pushed with `--force-with-lease` against the recorded prior head. |
| BLK-02 | **PDF rebuilt** | TeX Live 2023 installs from apt (`texlive-latex-base`, `-latex-recommended`, `-fonts-recommended`; `-latex-extra` is unnecessary and pulls a broken dependency set). `pdflatex` run twice: **10 pages, zero undefined references, zero missing figures.** Verified the build came from corrected source, the PDF reads 16.5 m/s, states the ESPA envelope as unmet, and its only mentions of 20.4 m/s and of invariance are the explicit historical ones. `paper/README.md`'s stale-PDF notice removed, which is what it existed for. |
| BLK-03 | **Wiki push still blocked** | The wiki remote now *clones* (it holds a 1-line placeholder against the repo's 227-line `wiki/Home.md`) but pushing returns `403`. Reads permitted, writes denied. Reported, not worked around. |
| BLK-04 | **`xychart-beta` confirmed rendering** | No chart work needed. |
| BLK-05 | **Tag pushes blocked** | Six annotated tags created locally; `refs/tags/*` pushes return `403` while `refs/heads/*` succeed. The remote's pre-existing `v0.1.0` now points at a commit the rewrite removed and cannot be updated from here. |
| GAP-01 | **`analysis/cost.py` (new), and it contradicts the paper** | Parametric BOM driven by `mass_properties.py`'s own part list, imported rather than re-entered. **Every price is an assumption and the file says so in its first paragraph.** The paper claimed recurring hardware "is dominated by the magnet set and the SiC drive". It is not: **avionics 23.7 %, supercapacitors 17.8 %, SiC 13.3 %, NdFeB 4.8 %.** Doubling the magnet price still leaves it under a tenth of the total, so the ordering survives the price uncertainty even though the ₹1.35 M total does not. **This machine is an avionics and energy-storage cost problem, not a magnetics one**, the opposite of where the design effort has gone. Paper corrected and rebuilt. |
| GAP-02 | **`docs/QUALIFICATION_PLAN.md` (new)** | Eight tests, T-1 to T-8, against GEVS and the CubeSat Design Specification, each naming the item it closes and its pass criteria. Two have no spring-deployer counterpart: T-6 measures static field at the payload envelope, and T-7 instruments a mass simulator to test whether "unmodified CubeSat" is true. Flags T-1 as the most likely failure, the track's first mode is 48 Hz pinned and 109 Hz fixed against a 70-100 Hz convention, and the as-built joint is between the two. |
| GAP-03 | **`docs/BENCHTOP_TESTS.md` (new)** | Four sub-scale experiments, cheapest first, **bands declared in advance** as `validation/` does. B-1 (Halbach pair on a gaussmeter) costs about two magnets and would be this project's first measured number. Bands are deliberately wide where the model deserves no better (±40 % at 20 mm stray field, order-of-magnitude at 50 mm) and B-3's ESR row carries **no** band, because declaring one around a number no script commits to would be inventing a target. |
| GAP-04 | **`validation/A9_tle_decay.md` + `validation/tle/fit_decay.py` (new)** | Decay rate against element-set histories of real decayed 3U CubeSats, **the only analysis specified anywhere that compares the model against something that happened** rather than against another model. **Specified, not run:** CelesTrak and Space-Track return 403 on CONNECT under this environment's network policy. Script committed unrun; its offline half is verified (`model_rate` returns −121.6 m/day at 450 km, matching A5's independently measured −0.1216 km/day). Band set at ±40 % on the median because Shambaugh's backtest puts state-of-the-art at 12.4 %, holding a static exponential atmosphere tighter than that would guarantee a meaningless failure. |
| GAP-05 | Limitation recorded rather than hidden | `fit_decay.py`'s `model_rate` runs at mean activity regardless of what each object's decay window experienced, because `cowell_sma_after()` takes no density scale. An object that decayed near solar maximum will look like a model failure when it is partly an activity mismatch. Documented in the function's own docstring. |

---

## 2026-07-29 (governance): the Engineering Programme adopted, four repositories stood up

The Engineering Programme Dossier v1.0 and TRB Prompt v1.0 now govern this project. A review
against both found six gaps; all are closed here. **This entry adds documents and zero
engineering**, right once, because the dossier asks for exactly this before new concepts, but
it must not become the pattern. The next work is A1.

| ID | Item | Detail |
|---|---|---|
| GOV-01 | **Governing documents committed verbatim** | `docs/programme/`. They existed only as uploads; a repository whose authoritative record lacks the document governing it has a hole exactly where this project claims strength. |
| GOV-02 | **Two amendments recorded, not buried** | `docs/programme/ADOPTION.md`. §3 designates repos 2-4 *Future* and we created them; §9 defines no Phase II promotion route and we added one. Both carry authorisation, reasoning, and the risk they create. **The dossier itself is not edited**: a governing document that quietly changes to match practice is not governing anything. |
| GOV-03 | **`docs/BASELINE.md`, generated, not typed** | `tools/make_baseline.py` reads 20 values from `analysis/results/*.json`. A hand-typed baseline is a set of numbers that can silently disagree with the scripts, which is the defect class this repo logs twice (P16, P19). `git diff --exit-code BASELINE.md` after regeneration is now a real check. |
| GOV-04 | **The change-control rule** | What may move the baseline: error correction, a validation outcome against a pre-declared band, a defect that makes a deliverable wrong. What may not: anything motivated by *better* rather than *correct*. **The boundary is by type, not convenience**: the momentum-transfer release is the most interesting idea here and defers; P17 is tedious and does not. |
| GOV-05 | **Seventeen ADRs at the time** | `docs/adr/`. `DECISION_LOG.md` is not superseded, its prose became the Context sections. 012-017 record decisions never written down anywhere, including the three second-order effects of the sled-mass change that were not obvious at the time. |
| GOV-06 | **`docs/PHASE_II.md`, the gate** | Items reviewed **only at baseline boundaries**, each against an entry criterion **written when it was deferred**. Same discipline as declaring acceptance bands before a run: a criterion written afterwards is written by someone who already knows what they want the answer to be. |
| GOV-07 | **`docs/MANUFACTURING.md`, and a finding** | Three budgets were being conflated: 1.000 mm clearance, A4's 0.025 mm deflection band, and the 0.050 mm shim *setting* spec. **The build stack had never been computed.** RSS of seven contributors is 0.101 mm; with A4's deflection bias the total is 0.121 mm to **1.58 % thrust spread against the 0.65 % claimed, 2.4x.** Not a contact risk (12 % of clearance) but the paper's open-loop spread counted the shim and not the parts. **Not propagated**: the contributors are assumptions. Ranking is the deliverable: track straightness and plate flatness dominate, and tightening the shim is nearly worthless. |
| GOV-08 | **Halbach assembly named as the largest manufacturability unknown** | 2.69 kN closing on brittle sinter, magnetisation order undecided, and absent from cost, schedule and the qualification plan. |
| GOV-10 | **`docs/CROSS_INDUSTRY.md`, sourced, not asserted** | **E21 substantially retires by citation** (ESA Space Tribology Handbook; MoS₂; twelve cycles is trivial). **E19 characterised**: segmentation is the standard mitigation and it costs thrust, a design option this project lacked. **E11** gains external support for ADR-004. It cuts both ways: E23's cogging half retires, but its *sweep* half appears genuinely unusual, industrial stages do not chirp through their velocity range in 157 ms. **E20 was not searched and says so** rather than padding with a plausible citation. |
| GOV-11 | **Four repositories, two generated** | `tools/export_companion.py`. The paper companion was verified to reproduce standalone, `v_exit = 16.537`, matching the flagship. §4's divergence warning is answered mechanically, not behaviourally: if a companion is ever hand-edited, delete and regenerate rather than reconcile. |
| GOV-12 | **Linkage prepared where it could not be pushed** | `bootstrap_repos.sh`, `seed_issues.sh` (14 issues, the roadmap and open HIGH defects, not all 42), `setup_project.sh`. **Found while testing: Issues are disabled on the repository** (API returns 410), a settings flag, now handled by the bootstrap. |
| GOV-13 | **Validation chain positioned honestly** | Dossier §7's eight rungs added to `docs/ROADMAP.md`. The project is at **Simulation, one rung of eight**. **Repeatability has no rung, nothing has been run twice by anyone.** Manufacturability opened today but holds analysis *about* manufacturing, not manufacturing evidence. |
| GOV-14 | **Literature review restructured** | `RELATED_WORK.md` was a leads list; it now carries five fields per source, claim, method, what VOLLEY takes, where it differs, verification status. Status is per-source, because the old blanket "none of this has been read" became untrue and a blanket statement that is wrong is worse than none. |
| GOV-15 | `PROJECT_NOTES.md` de-staled | It claimed 32 % efficiency and listed P5/P8 as open, both wrong since the propagation. Now defers to `docs/BASELINE.md`, `docs/ROADMAP.md` and `PHASE_II.md` rather than competing with them. |

**No value in `analysis/` changed.** `analysis/results/cost.json` is the only file added there,
and every existing result field is untouched, verified, because this is governance work and a
moved number would mean something went wrong.

---

## 2026-07-29 (companions): the three repositories exist; content still to be pushed

| ID | Item | Detail |
|---|---|---|
| REPO-01 | `VOLLEY-paper`, `VOLLEY-thesis`, `VOLLEY-lab` created | Created 2026-07-29. All three public, `main` default, currently empty. Repository creation is not possible from the working environment at all, the GitHub App returns `403 Resource not accessible by integration`, because **GitHub Apps cannot create repositories on a personal account**; that endpoint needs a user token, not an installation token. No permission setting changes it. |
| REPO-02 | **Content generated and verified, not yet pushed** | 84 files to `VOLLEY-paper`, 148 to `VOLLEY-thesis`, 3 to `VOLLEY-lab`. The paper companion was verified to **reproduce standalone**: run from a clean copy it returns `v_exit = 16.537`, matching the flagship. |
| REPO-03 | **Why the push did not happen here** | The environment's git proxy serves only `aaaaaaaaaaaavm/emocd`; `git ls-remote` fails against all three companions. Extending session scope needs `add_repo`, which required an approval the environment could not grant. Reported rather than worked around. `tools/bootstrap_repos.sh` covers it in one command from any machine with `gh`. |
| REPO-04 | **Three stale counts fixed from the A1 propagation** | A1 moved the tally 3-of-8 to 4-of-9 and three places did not follow. `SUMMARY.md` had become **self-contradictory**: "four of nine ... and all three predate the current operating point", which was introduced in the same edit that added A1. A1 *is* at the current point; A5 and A8 are not. `README.md` and P19 carried the same stale framing. |
| REPO-05 | `docs/PROGRAMME.md` and `docs/HISTORY.md` narrowed | Both described the companions as prepared-but-unpushed in general terms. They now state precisely what exists, what is empty, and which specific things remain blocked: tags and releases, descriptions and topics, the programme board, and the Issues toggle. |

**Still outstanding, all of it one command each:** `bootstrap_repos.sh` (fills the three
companions), `publish_releases.sh` (six milestone tags and releases), `setup_project.sh` (the
programme board), and the Issues toggle in repository settings.

---

## 2026-07-30: prior art found, two claims retracted, one ADR argument found false

The most consequential entry in this log. A literature check found **published work on this exact
concept that the paper did not cite**, and reading it retracted two claims and falsified an argument
this design's central decision was partly resting on. Full record in `docs/PRIOR_ART.md`, tracked as
**P22**.

| ID | Item | Detail |
|---|---|---|
| ART-01 | **Two independent groups are already here** | Feng, Yang & Wu (NUDT, *IJAE* 2025, art. 3000765) simulate an on-orbit three-stage induction coilgun driving a 20 kg CubeSat to **321.56 m/s** with a 3-D reachable-domain analysis, **published 2025-11-12, eight months before this repository went public.** Separately the Harbin Institute of Technology mechatronics group has three papers (2022, 2024, 2025) on magazine-fed electromagnetic storage, transport and release of stacked CubeSats. The paper had 24 references and none of them. |
| ART-02 | **§I claim retracted** | *"No published deployment system operates in the tens of m/s"* was **false**: Feng operates at hundreds. Now restricted to **flown hardware**, which is what the comparison table always actually showed. Feng's own Table 1 surveys the same 1-2 m/s spring deployers and identifies the same gap, so the gap is real; the word *published* was wrong. |
| ART-03 | Contribution re-scoped in the abstract | From electromagnetic deployment as such to **programmable velocity + unmodified satellite + inside its own qualification envelope**. Narrower and defensible. Both qualifiers do real work against Feng, where against a spring they were nearly free. |
| ART-04 | **ADR-003's efficiency argument was false, and unsourced. Withdrawn.** | It claimed coilgun efficiency is *"1-2 % in the literature"* with no citation. Feng reports **14.9-19.9 %**: the same order as this design's own 20 % electrical-to-payload. Einat & Orbach (*Sci. Rep.* 2023) measure a real multi-stage launcher but at a **2.5 g** projectile, five orders below a CubeSat, so it cannot settle the question either way. The argument is removed rather than re-sourced. It was never load-bearing. |
| ART-05 | ADR-003's second claim softened | *"Cannot command velocity closed-loop"* to a claim about **absent published dispersion evidence**. Feng varies exit velocity 230 to 321.56 m/s by charging voltage (10 to 16 kV) with position/velocity feedback for stage trigger timing. That is genuine velocity selection. They quote **no dispersion figure**, so this design's 0.027 m/s 3σ stands unopposed rather than proven superior. |
| ART-06 | **The decision survives, now on arithmetic instead of assertion** | ADR-003 argued in mid-2025 that a coilgun's velocity advantage is *"erased by the payload's own g-limit."* Against Feng's published 3.9 m barrel: **1352 g mean**, ~3060 g peak from their own >600 kN on 20 kg, against ~14 g CubeSat qualification. Also **6.91 MJ per shot against 2.80 kJ**: 2470x. Not a flaw in their work; they target debris removal with a purpose-built body. It is why this one is not a coilgun. |
| ART-07 | **Three of my own abstract-level conclusions were wrong** | Listed in `PRIOR_ART.md` rather than quietly corrected. The worst: I asserted 321.56 m/s "would need a 493 m track at 10.7 g" as a hypothetical, when their actual barrel length was in their Table 2 all along. The fact is more decisive than my hypothesis was. Also: Feng has **no hardware** (so this project and theirs are maturity peers, not one behind), and *Aerospace* 12(6) 466's experiment measures a **32.8 mm/s transport pusher**, not an ejection, a real maturity gap but narrower than "they have experiment and we don't". |
| ART-08 | **E24 opened**, from a competitor's problem statement | Xu et al. build a cost model for **attitude disturbance caused by moving CubeSats inside the deployer**. This project budgets recoil from the *shot* (66.1 N·s) and has nothing on disturbance from **magazine indexing between shots**: a few kg translating across the structure between every pair of shots, unmodelled, on a design whose dispersion claim assumes the track is where the model says it is at trigger time. |
| ART-09 | Phase II candidate: adopt reachable-domain analysis | Feng's 3-D reachable-set envelope answers "which orbits does one shot make available" directly, where this project reports a scalar lifetime multiplier. The strongest thing to take from this literature. |
| ART-10 | `docs/RELATED_WORK.md` gained the section it should always have had | It had 7 citations and **no competitor section at all**. Its absence was the defect that let ART-02 stand. All five works now carry `verified` status with the file's own five-field format. |

---

## 2026-07-30 (bench): B-1 and B-2 bands derived instead of chosen

Prompted by ART-01: the Harbin group has measured hardware and this project has measured nothing.

| ID | Item | Detail |
|---|---|---|
| BENCH-01 | **I duplicated existing work and then removed it** | `docs/BENCHTOP_TESTS.md` already specified a single-coil thrust measurement as **B-2**, with a better rig than the one I designed, real Halbach pair, design coil geometry, swept over a wavelength. I wrote a competing `BENCH_E4.md` around a simpler two-magnet rig before checking. Deleted; the effort was redirected into strengthening B-1 and B-2. Recorded because the repository logs its own process defects, and "check whether it already exists" is one. |
| BENCH-02 | `validation/bench/bench_predict.py` | Derives the acceptance bands B-1 and B-2 previously asserted. **Imports** `verify_field.py` and `motor_model.py` rather than reimplementing the field geometry, and carries a guard that exits non-zero if its local build ever drifts from `verify_field.make_array`, the same idea as `_check_operating_point()` in `sizing.py`. Perturbs gap ±0.5 mm, Br ±3 %, thickness ±0.1 mm, re-solves, reports RSS. |
| BENCH-03 | The bands do not move, and that is the finding | Measurement error is **4.4 % on B-1's field rows, 13.5 % on B-2's thrust**, against declared bands of ±15 % and ±20 %. The bands must also cover *model* error, which is the thing under test and cannot be budgeted from the model. What the budget establishes is that **the rig is not the limiting factor**: a reading outside ±15 % can no longer be blamed on shim stack or magnet grade. That is what makes a failure interpretable. |
| BENCH-04 | **A two-block bench pair built poles-facing reads exactly zero** | 0.00000 T at midgap, against 0.329 T built correctly. B-1's wording, "a two-block *opposed* pair", is ambiguous in precisely the way that matters, and a zero reading would look like a falsified field model rather than a reversed magnet. Found by hitting it, the first version of the predictor divided by zero. `verify_field.py` probes for the convention automatically on the four-block array, so the trap exists only on the bench. |
| BENCH-05 | B-2's load cell must be sized to the smallest force, not the largest | A cell specified at 0.5 % of full scale contributes error inversely with the reading, so sizing it to the largest expected force makes the lowest-current point the least trustworthy, the opposite of what B-2 needs, since low current is where it is designed to operate. |
| BENCH-06 | One budget term is known-incomplete, and says so | For the stray rows the probe sits a fixed distance behind the **back face**, so block thickness moves the reference plane as well as the source; the budget captures only the source term. Affected contributions are 0.8-1.8 % against an RSS of 3.3-4.2 %, so no conclusion changes. Flagged in the script and the doc rather than left to be found. |
| BENCH-08 | **`.gitignore` has never ignored `paper.pdf`** | Line 17 read `paper.pdf          # transient output; committed PDF is VOLLEY_IEEE_Conference.pdf`. In `.gitignore`, `#` opens a comment **only at the start of a line**, so the pattern was the entire string including the comment text and matched no file. Found because `git add -A` staged `paper/paper.pdf` when the documented intent was that it never be tracked. Comment moved to its own line; `git check-ignore` now confirms the match. The committed `VOLLEY_IEEE_Conference.pdf` has also been refreshed from the corrected `paper.tex` (11 pages, zero undefined references) since the ART-02 rewrite made it stale. |
| BENCH-07 | Two unit and definition errors caught by cross-checking | `motor_model.thrust_constant()` returns N per **A/m**, not per kA/m, a factor of 1000, caught because 0.011 was obviously not 11.22. And `verify_field` computes stray field as the **max of the full 3-vector**, not the mean of the in-plane components; using the latter gave 16.2 mT where the repository publishes 22.7 mT. Both found by requiring the script to reproduce `field_verification.json` rather than merely look plausible. |

---

## 2026-07-29 (toolchain): the validation environment made reproducible

| ID | Item | Detail |
|---|---|---|
| ENV-01 | **`tools/env-setup.sh` added** | Until now `requirements.txt` covered only the analysis layer. Everything under `validation/` needs external solvers, and those were installed ad hoc each time the working environment was rebuilt, which means the validation results were reproducible in principle and awkward in practice. The script installs GetDP, CalculiX, ngspice, gmsh, scikit-fem and a minimal LaTeX set, then **verifies each one and exits non-zero if any is missing**. |
| ENV-02 | Two install failures encoded as comments, not rediscovered | `apt-get update` must run first, a stale container index makes the first `texlive` fetch 404. And `texlive-latex-extra` is deliberately excluded: nothing in `paper/` uses it and it pulls a mesa/ruby chain that fails to configure in a minimal container. Both cost time once; neither should again. |
| ENV-03 | `README.md` cross-check count corrected 2 to 3 | The README still read "Two results have independent cross-checks", naming the magpylib field check and the orbital decay check. A1 (the meshed magnetostatic FEM confirming the thrust constant to 0.07 %) is a third, and a stronger one, since it is a PDE solve rather than another superposition. `SUMMARY.md` already said so; the README contradicted it. Same class of staleness as REPO-04, from the same propagation. |
| ENV-04 | `README.md` and `docs/CONTRIBUTING.md` point at the setup script | Both previously implied `pip install -r requirements.txt` was sufficient to run everything in the repository. It is sufficient for `analysis/` only, and that distinction is now stated where each instruction appears. |

---

## 2026-07-29 (companions live): all four repositories now carry content

| ID | Item | Detail |
|---|---|---|
| REPO-06 | **The three companions are published** | `VOLLEY-paper` at `8c80f78` (84 files), `VOLLEY-thesis` at `fe6756d` (148), `VOLLEY-lab` at `2ebb6a3` (3). The two generated ones were built by `tools/export_companion.py` against flagship `c927df9` and carry that commit in their banner, so a reader can tell exactly which flagship state they are a copy of. |
| REPO-07 | What actually unblocked it | REPO-03 recorded this as blocked on session repository scope. The real cause was narrower and was found by testing rather than assumed: the **GitHub App installation was scoped to `VOLLEY` alone**, because the other three were created after it was installed. Widening the installation's repository access made the scope extension succeed on the first attempt. The earlier diagnosis was correct about the symptom and wrong about the cause. |
| REPO-08 | The paper companion was verified **before** publishing, not after | `analysis/` was run from the clean pushed tree with an empty `results/`, and returned `v_exit = 16.537 m/s`, identical to the flagship. The rest of the tree then diffed byte-identical against the export. For a reproducibility package this is the only check that matters, and it precedes the push rather than trailing it. |
| REPO-09 | Still blocked, retested rather than assumed | `refs/tags/*` still fails (the proxy drops the connection mid-push) and `api.github.com/repos/*` still returns `403 GitHub access is not enabled for this session`. Both were re-tested after the App scope widened, on the chance that fixed them too. It did not, they are proxy behaviour, not permissions. The six tags, their releases, the descriptions and topics, and the programme board all still need `tools/publish_releases.sh` and `tools/setup_project.sh` run from an ordinary machine. |

---

## 2026-07-29 (tags): the six milestones are on GitHub, and the publish path was found broken

| ID | Item | Detail |
|---|---|---|
| TAG-01 | **Six milestone tags pushed** | `v0.0-concept` (2021-03-22) through `v1.0` (2026-07-29), annotated, carrying their design-period tagger dates. Verified against the remote by SHA: all six tag objects on GitHub are the objects built here. Supersedes the "tags cannot be pushed" note in REPO-09 for `refs/heads`-adjacent reasons, the block was the *proxy's* credential path, not GitHub. |
| TAG-02 | **`publish_releases.sh` would have silently created nothing** | Found by actually cloning the repository and running it, rather than reading it. The script pushes tags **if they exist locally**: and they existed only in the environment they were built in. They were never on GitHub, so **no clone has them**. A fresh clone arrives with one tag, `v0.1.0`, pointing at a commit the reconstruction removed. The script would have printed `MISSING locally -- skipped` six times, created zero releases, and exited 0. A defect that reports success is worse than one that fails. |
| TAG-03 | `tools/restore_tags.sh` added | Rebuilds all seven annotated tags (message, tagger date and tagger identity) from data embedded in the script plus commits already in the clone. Every tagged commit is an ancestor of the default branch, so a full clone suffices. **Verified by cloning fresh, running it, and comparing tag objects: all seven reproduce bit-for-bit.** `publish_releases.sh` now invokes it when the tags are absent, so the failure in TAG-02 cannot recur. |
| TAG-04 | Two bugs in that script, both found by testing it | **(a)** The tagger identity was inherited from git config, so in a fresh clone whose config named someone else, every milestone was silently restamped with that identity and the tag objects stopped matching. Now pinned, overridable via `TAGGER_NAME`/`TAGGER_EMAIL`. **(b)** `v0.1.0` was treated like the others and skipped when already present, but a clone always has it, pointing at the wrong commit, so the re-point step would have force-pushed a stale pointer and changed nothing. It is now always rewritten. Neither bug was visible by reading the script. |
| TAG-05 | Identity audit across all four repositories | Every commit author, committer and tag tagger in the flagship history and in all three companions: a single identity, `Adityavardhan Mishra <adityavardhanmishr@gmail.com>`. No stray identity anywhere. |
| TAG-06 | **Still outstanding: the `v0.1.0` re-point and the six Releases** | The re-point needs a force-push, which the working environment declines to perform, and Releases need the REST API, which it intercepts. Both are one `tools/publish_releases.sh` run from an ordinary machine. Reported rather than worked around. |

---

## Open decisions

1. **LICENSE**: RESOLVED 2026-07-23: owner chose **MIT** (P3-07).
2. **Repo visibility**: RESOLVED: the repository is now **public**, which discloses the
   scripts and the operating point. See `OPEN_PROBLEMS.md` E14 for what that costs on the
   patent side.

## Known follow-ups not yet addressed

- The two remaining figure generators (`legacy/make_figs.py`, `legacy/c5b_conj.py`) are
  legacy and use `dv = 25.0 m/s`. Only `F06` was regenerated; other figures were not
  audited against the current operating point.
- `OPEN_PROBLEMS.md` E-items (E1 3-D field closure, E3 CAD, E4 hardware, E16 reference
  hygiene...) remain open engineering, unchanged.
