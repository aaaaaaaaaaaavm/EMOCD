# Open problems, known errors, and the fix list

Two categories: **P-items are errors in the currently published paper** and should be
fixed first. **E-items are genuinely unsolved engineering.**

Last reviewed 2026-07-29.

---

## P — Errors found while building this repo (paper does not match its own scripts)

> **STATUS (2026-07-23): P1–P4 all RESOLVED in `paper/paper.tex`.** Fixes, causes and
> before/after values are logged in `CHANGELOG.md` (entries P2-01–P2-04). The items are
> kept in full below for the audit record. Two related defects found in the process were
> also fixed: the F06 conjunction figure was regenerated at the rated velocity, and a
> stale `astro.py` docstring value was corrected — both logged in `CHANGELOG.md`.

### P1. Conjunction minimum is wrong AND not a robust quantity — HIGH PRIORITY
**RESOLVED 2026-07-23 — see CHANGELOG.md P2-01.**
The paper states a 30-day minimum satellite-to-stage approach of **45.3 km**. That
figure was computed at **20.65 m/s**, the superseded operating point. At the paper's
own rated velocity of **20.37 m/s**, `analysis/astro.py` gives **4.6 km**.

Worse, the quantity is fragile. Sweeping ejection velocity:

| Δv (m/s) | min approach (km) |
|---|---|
| 20.00 | 37.5 |
| 20.37 (rated) | **4.6** |
| 20.50 | 56.1 |
| 20.65 (paper's value) | 45.3 |
| 21.00 | 63.4 |

This is a near-resonant beat sample, not a design property. A ±2.5 % velocity change
moves it by more than an order of magnitude.

**Follow-up:** `validation/A6_conjunction_cara.md` specifies the quantitative version —
probability of collision via NASA's CARA tools, which integrates over the covariance
instead of sampling one geometry. The test is whether Pc stays stable across the velocity
sweep that moves minimum distance by an order of magnitude.

**Fix:** stop quoting a specific minimum distance as a safety result. Reframe around
what IS robust: the ~8.1-day phase realignment period, and the mitigation of disposing
of the host stage before the first realignment. State plainly that per-shot COLA is
mandatory because the approach geometry is sensitive to exact ejection velocity.

### P2. Peak current is stale — MEDIUM PRIORITY
**RESOLVED 2026-07-23 — see CHANGELOG.md P2-02.**
Paper says **323 A**. That belongs to the superseded 130 kA/m point. At the rated
140 kA/m, `motor_model.py` gives **392 A**. Fix the paper, and check that the SiC
device derating discussion still holds at the higher current (it should — 96 V rail,
1200 V devices — but the current rating of the bridge and busbars needs restating).

### P3. Far-field stray values don't reproduce exactly — LOW PRIORITY
**RESOLVED 2026-07-23 — see CHANGELOG.md P2-03.**
Paper quotes 22.7 / 4.7 / 1.0 mT at 10 / 20 / 50 mm. `verify_field.py` reproduces
22.7 mT at 10 mm exactly but gives 4.3 and 0.4 mT at 20 and 50 mm. Likely sensitivity
to modelled array length (edge effects dominate the far field). The 10 mm value is the
one that sets the keep-out spec, so this is minor — but resolve it before anyone cites
the 20/50 mm numbers.

### P4. Brake fin temperature rise conflates per-shot with per-campaign — MEDIUM PRIORITY
**RESOLVED 2026-07-23 — see CHANGELOG.md P2-04.**
The paper states the 0.86 kg copper fin sees "an adiabatic 37 K transient rise" **per
shot**, and later refers to "the adiabatic per-shot rises (0.3 K coil, 37 K fin)".

`analysis/sizing.py` gives 1008 J into 0.86 kg of copper = **3.0 K per shot**. The 37 K
figure is the *full 12-shot campaign* total if the fin never radiated between shots
(12 x 1008 J / 331 J/K = 36.5 K).

The design is therefore *less* thermally stressed than the paper claims, but the number
as written is wrong and internally inconsistent.

**Fix:** state 3.0 K per shot, and 37 K as a bounding campaign-adiabatic case that
radiation between shots relieves. Same correction applies to the coil: 0.28 K per shot,
3.3 K campaign.

---

## P — CAD reconciliation and packaging (found in the 2026-07-23 Fusion 360 CAD build)

> These arose when the parametric design was taken into CAD across nine Fusion documents.
> The CAD is authoritative for **geometry and fit only**; `analysis/*.py` remains
> authoritative for **mass and performance** until FEA closes the open items. All
> geometry values below are traceable to `cad/parameters.json`. **No number in
> `analysis/*.py` or `paper/paper.tex` has been changed** on the strength of the CAD.

### P5. CAD sled mass contradicts the parametric assumption — RESOLVED 2026-07-29
> **RESOLVED.** `motor_model.M_SLED` and `sizing.M_SLED` now carry the measured **9.445 kg**
> (P15), not the 4.86 kg parametric estimate. A4 ran, the drawn plate passed all three
> structural bands, and the measurement fell in the decision rule's ≥ 6.80 kg branch, so the
> rule resolved this rather than a judgement call. **Caveat carried forward:** 9.445 kg is
> the as-drawn, unpocketed geometry and A4 reports a 17× stress margin, so a rib-stiffened
> chassis would recover mass. Designing one is the open successor to this item
> (`ROADMAP.md`), and it is tracked under E2 rather than here.

Original item follows for the audit trail.

> **UPDATE 2026-07-28 — A4 structural leg has RUN (CalculiX).** The as-drawn 6 mm plate
> passes every declared band: 0.0194 mm airgap closure against a 0.025 mm per-plate budget,
> 33.7 MPa against 587 allowable, first mode 3408 Hz against >200. So there is **no
> structural argument for the chassis being lighter than drawn** — a lighter one has to be
> designed (rib-stiffened), not assumed. Combined with P15's measured 9.445 kg, the decision
> rule's ≥6.80 kg branch stands and the machine as it exists delivers **16.53 m/s**.
The first-pass Fusion sled (6 mm Ti-6Al-4V chassis, stiffness-driven by the ±0.05 mm gap
tolerance under 3.7 kN inter-array attraction, **no structural FEA behind it**) implies a
sled mass of **~7.50 kg**. `analysis/mass_properties.py` assumes **4.86 kg**, which
`motor_model.py` hard-codes as `M_SLED` and which sets the headline exit velocity. Both
are estimates — one CAD-geometric, one parametric-solid — and neither is FEA-verified. Do
not change the scripts until analysis A4 closes the chassis — specified with a
pre-declared decision rule in `validation/A4_sled_structural.md` (CalculiX or
Code_Aster, both free, both read `cad/step/gen3/EMOCD_Sled_Gen3.step`). Source:
`cad/parameters.json` (sled group, `PROVISIONAL_PENDING_FEA`).

### P6. Payload seating / orientation — RESOLVED (by CAD, 2026-07-23)
Resolved via the rail interface: the 3U payload now models the four CubeSat Design
Specification corner rails (8.5 mm, `cad/parameters.json` `payload_3u`), which fix seating
and orientation against the sled cradle. No further action.

### P7. Brake sits past the release point — geometry / ConOps
The eddy brake occupies **x = 1530–1740 mm**, beyond the **1500 mm** satellite release
point, on an 1800 mm longeron. The sled runs on into the brake after the payload departs
— consistent with the fire-then-arrest ConOps, but it forces the track and enclosure to
extend past release, which drives the envelope length (see P9). Source:
`cad/parameters.json` (brake, track).

### P8. Exit velocity provisionally 17.88 m/s pending sled structural FEA — RESOLVED 2026-07-29
> **RESOLVED, and not at 17.88 m/s.** That figure came from the 7.50 kg CAD estimate. The
> measured mass is 9.445 kg, so the rated velocity is **16.537 m/s at 10.7 g**, now
> propagated into `analysis/`, `paper/paper.tex`, the figures and every front page. The
> machine is no longer acceleration-limited: at 10.7 g against a 25 g cap it is
> thrust-and-mass limited, which changes what recovering velocity means (mass or current,
> not stroke).

Original item follows for the audit trail.

If the CAD sled mass (P5) holds, exit velocity falls from the script's **20.37 m/s** to a
provisional **~17.88 m/s** (with acceleration ~12.5 g, efficiency ~24 %, recoil
~71.5 N·s, lifetime multiplier ×1.68 — all CAD-corrected and provisional). **These values
are NOT propagated into `analysis/*.py` or `paper/paper.tex`**; the scripts stay
authoritative until analysis A4 locks the sled mass (`validation/A4_sled_structural.md`,
which fixes in advance which of the two estimates wins at which mass). Do not hard-swap
20.37 → 17.88 anywhere. Source: 2026-07-23 CAD Master Plan; see README headline note.

### P9. Closed envelope exceeds ESPA Grande by ~44% — packaging / host
The closed installed envelope is **1839 × 530 × 940 mm** (`cad/parameters.json`). The
1839 mm length exceeds ESPA Grande's ~1270 mm longest-dimension class by ~44%, because
the brake lives past the 1500 mm release point and the enclosure spans it. Owner decision
(cannot be made in code): re-scope the host to POEM / custom accommodation (the paper
already leans host-agnostic), or shorten the track / repackage the brake. This supersedes
the earlier 1825 × 516 × ~1030 mm figure; the height change (1030 → 940) exceeds what skin
thickness explains and is **flagged for re-verification** in `cad/parameters.json`.

### P10. Enclosure, radiator, and packaged avionics absent from the mass rollup — MEDIUM (NEW)
The ninth document (`EMOCD_Enclosure`) adds 2 mm aluminium skins, a 1600 × 200 × 3 mm
radiator, and equipment bays for the supercapacitor bank, PPU, sequencer, and IMU. **None
have line items in `analysis/mass_properties.py`**, so the 72.3 kg dry-mass rollup is
incomplete. Add line items once masses are estimated (do not alter existing items without
cause). Source: `cad/parameters.json` (`enclosure.mass_note`).

### P11. The corrections may never have reached the submitted paper — RESOLVED 2026-07-29
> **RESOLVED: nothing has been submitted anywhere.** Confirmed by the author 2026-07-29.
> There is no version of record, so P1–P4 are not loose in any published document and no
> corrigendum is needed. `paper/archive/EMOCD_submission_uncorrected.pdf` is a draft build
> whose filename overstates its status — it was never sent.
>
> **This unblocks the paper edits that were batched behind it.** The reason P12 and P16 were
> left untouched in `paper/paper.tex` was that editing the source without rebuilding the PDF
> would split it from a published record. There is no published record. The paper is a draft,
> the only cost of editing it is that the committed PDF goes stale until it is recompiled,
> and that is a normal state for a draft rather than a defect. **Fix P12 and P16 in
> `paper.tex` and rebuild before anything is submitted.**

Original item follows, kept for the audit trail.


`paper/archive/EMOCD_submission_uncorrected.pdf` is a build of the paper that still
carries all four P1–P4 values (323 A, 23 A/mm² at 140 kA/m, 37 K per shot, 45.3 km
conjunction minimum). Its filename says *submission*. If that is genuinely the version
that went to the conference, then P1–P4 are corrected **only in this repository** and the
version of record is still wrong — which is a different situation from the STATUS block
at the top of this file, and one that a corrigendum, not a git commit, has to fix.
**Confirm which build was submitted.** If it was the uncorrected one, decide between
withdrawing, submitting an erratum, or correcting at the camera-ready stage, and record
the outcome here. If the submitted build was in fact compiled from the corrected
`paper.tex`, delete this item and say so in `CHANGELOG.md`.

### P12. The paper contradicts the CAD in two places — RESOLVED 2026-07-29
> **RESOLVED in `paper/paper.tex`.** The Limitations section no longer says masses derive
> from a parametric model rather than detailed CAD; it states what the CAD measured and what
> that costs. The ESPA-Grande envelope is no longer asserted as a capability — the
> requirement statement, the Fig. 2 caption and the accommodation section now record 1839 mm
> against the ~1270 mm class and name it an open packaging problem (P9). The mounting-interface
> statements were true and are unchanged. **The committed PDF still predates these edits**;
> see `paper/README.md`.

Original item follows for the audit trail.

Found while sweeping the repository for stale values. Both are prose claims, not computed
numbers, and neither has been changed in `paper/paper.tex`:

1. **Limitations (Sec. XV) says "Masses derive from a parametric solid model, not detailed
   CAD."** That was true when written and is now false — nine Fusion documents exist in
   `cad/`. The honest replacement is not "CAD exists" but the sharper statement: two mass
   estimates exist, they disagree by 54 %, and neither is FEA-verified (P5, P8).
2. **The paper claims an "ESPA-Grande-class envelope and mass allocation"** (abstract-level
   requirement, the Fig. 2 caption, and again in the accommodation section). The CAD closed
   envelope is 1839 mm against the ~1270 mm class limit — **P9, ~44 % over**. As written,
   the paper asserts a compatibility the geometry does not support.

Item 2 is the serious one: it is a capability claim, not a caveat, and it is the kind of
thing a reviewer with an ESPA user's guide open would catch immediately.

**Why this is not fixed yet.** Editing `paper.tex` without rebuilding the PDF would put the
source and the committed build out of step, and no TeX engine is available in the working
environment. It is also entangled with **P11** — until it is known which build is the
version of record, it is not clear whether this is a camera-ready edit or a corrigendum.
Resolve P11 first, then fix both items in one pass and rebuild.

### P13. The committed STEP set was mixed-generation, with two stubs — RESOLVED 2026-07-28
Found while importing `EMOCD_figs.zip`. The nine files in `cad/step/` matched no single CAD
generation, and two of them were single solids:

| Document | Was committed | Gen1 | Gen3 |
|---|---|---|---|
| Stator | **1 body** | 324 | 162 conductors |
| Interface_ESPA | **1 body** | 6 | 6 + bolt holes |
| Sled | 12 | 5 | 16 |
| Payload_3U | 5 | 5 | 1 |
| Track | 6 | 8 | 4 |
| Assembly | 225 | 43 | 227 |

The stator export therefore contained no winding at all, while `cad/README.md` claimed
"STEP exports of every document" and the paper's §IV-B rests on a winding-resolved model.
Anyone opening the committed stator to check the conductor layout would have found a block.

**Resolved** by replacing the set with `cad/step/gen1|gen2|gen3/`, the three audited
generations. Body counts measured on import with `grep -c MANIFOLD_SOLID_BREP`, not copied
from the source changelog.

### P14. Gen3 CAD defects not previously tracked — NEW 2026-07-28
From the Gen3 audit in `cad/CHANGELOG_CAD.md`, verified against the exports where possible.
None of these were in this file before.

| ID | Defect | Consequence |
|---|---|---|
| G3-D1 | Cassette height **640 mm** in Gen2 and Gen3 against `parameters.json` `magazine.cassette_height_z = 690` | 50 mm short. Either the CAD or the parameter is wrong; `parameters.json` wins by rule, so the CAD needs correcting |
| G3-D2 | Track is longerons and launch locks only — **no roller channels, guide flanges, or cross-tie outriggers**, all of which `parameters.json` specifies | The 205 mm overall track width exists only as a parameter. The rollers on the sled have nothing modelled to run in |
| G3-D4 | **Stator layer count still open.** Gen1 built two layers (324 conductors), Gen2 and Gen3 one (162) | `parameters.json` flags the decision open. Roughly ×2 force for the same sheet current against ×2 copper mass — never computed. This sits upstream of Kt and therefore of the headline velocity |
| G3-D5 | Halbach arrays **not re-centred** after the chassis grew 360 → 488 mm | `sled.halbach_array_x_start = 230 mm` is inherited from the shorter chassis. Array position relative to the winding is what Kt depends on |
| G3-D6 | **No payload-on-sled rigid joint** in any generation | `parameters.json` `documents.EMOCD_Assembly` specifies one. Without it the assembly cannot express the payload riding the sled, which is the thing being modelled |

| G3-D12 | **Assembly geometry extends 156 mm aft of the recorded envelope.** `EMOCD_Assembly_Gen3.step` spans x = −188 to 1810 mm; `parameters.json` records the installed envelope as −32 to 1807 mm | Either the assembly parks the sled further aft than the envelope assumed, or the envelope was measured without it. Found on 2026-07-28 while meshing the assembly for `cad/stl/`. It makes P9 worse, not better: 1998 mm against the ~1270 mm ESPA Grande class limit is ~57 % over rather than ~44 %. Measure which component owns the −188 mm face before changing either number |

**Resolved and recorded:** ESPA bolt holes (24× M9 on Ø400 mm BCD) were absent in Gen1 and
Gen2 and are modelled in Gen3 — G1-D5 closed.

**Two discrepancies between `cad/CHANGELOG_CAD.md` and its own exports**, found on import
and left in place there with a note rather than edited:

- **The Gen3 brake-placement fix is not in the exports.** G2-D4 says the Gen2 brake sat at
  the local origin and Gen3 moved it to x = 1530 mm. `EMOCD_Brake_Gen2.step` and
  `EMOCD_Brake_Gen3.step` are geometrically identical — 3 bodies each, 79 points each,
  differing only in file name and time stamp — and **both** already place the brake at
  1530–1740 mm. The fix may have been applied to the Fusion document before the Gen2 export
  was taken; either way the export does not show the defect it is said to have.
- Body counts: `EMOCD_Payload_3U_Gen1.step` measures 5 solids where the inventory says 1,
  and `EMOCD_Sled_Gen1b.step` measures 11 where it says ~16.

The sled fix **is** verifiable: Gen2 chassis half-length measures 180 mm (360 mm plate),
Gen3 measures 244 mm (488 mm plate), so G2-D1 is genuinely closed.

### P15. The Gen3 sled as drawn is 9.45 kg, above BOTH existing estimates — RESOLVED 2026-07-29
> **RESOLVED by adoption.** 9.445 kg is now the operating point across `analysis/`, the
> paper and the figures. `mass_properties.py` keeps the parametric breakdown for the record
> and carries the 4.59 kg difference as an explicit reconciliation line, so system dry mass
> (76.9 kg, up from 72.3) no longer understates.

Original item follows for the audit trail.

Measured on 2026-07-28 from `cad/step/gen3/EMOCD_Sled_Gen3.step`: exact solid volumes from
the OpenCASCADE kernel, times material densities (NdFeB 7500 kg/m3 is this repo's own value,
from `sizing.py`).

| Estimate | Sled mass | Exit velocity |
|---|---|---|
| `mass_properties.py` parametric | 4.86 kg | 20.37 m/s |
| P5's CAD figure | 7.50 kg | 17.87 m/s |
| **Gen3 geometry, measured** | **9.445 kg** | **16.53 m/s** at 10.7 g, 19.6 % efficiency |

The method reproduces P8 exactly when fed 7.50 kg — it returns 17.87 m/s against P8's stated
17.88 — so the discrepancy is in the mass, not the method. Dominated by two chassis plates
(3.63 kg of titanium) and the magnet arrays (3.67 kg of NdFeB).

**What it does not settle.** This is geometry times density, not the structural FEA that A4
specifies. The plates are drawn solid with no lightening pockets, and a real design would
pocket them; the stiffness constraint (airgap held to ±0.05 mm) is still unevaluated. But
A4's pre-declared rule already says a mass at or above 6.80 kg makes 17.88 m/s the headline,
and this is well past that. **Whichever way the FEA goes, the 20.37 m/s headline is not
supported by the geometry that currently exists.**

Do not edit `analysis/*.py` on the strength of this. Run A4, then propagate once.

### P16. The lifetime-multiplier INVARIANCE claim is falsified — HIGH, NEW 2026-07-28
GMAT R2022a, run headless against the bands declared in `validation/A5_astro_orekit.md`
before the run:

| Solar activity | GMAT multiplier | vs ×1.80 | Band ±5 % |
|---|---|---|---|
| High (F10.7 250) | 1.7302 | −3.88 % | pass |
| Mean (F10.7 150) | 1.7750 | −1.39 % | pass |
| **Low (F10.7 70)** | **2.0739** | **+15.21 %** | **FAIL** |

Spread across the three: **18.48 %** against a ≤5 % band.

**The mechanism, and it is not subtle.** `analysis/astro.py` represents solar activity as a
uniform multiplicative scale on density (`rho(h, scale)`). Sweeping that scale across a
factor of **forty** moves the multiplier from 1.7992 to 1.7968 — 0.1 %. A uniform density
factor divides both lifetimes by the same number, so **the ratio is preserved by
construction**. The sweep that the paper cites as demonstrating invariance cannot, in
principle, do so.

MSIS varies the *shape* of the density-altitude profile with F10.7, not only its magnitude.
The boosted orbit's apogee sits ~37 km above the baseline's, the two sample the profile
differently, and the ratio moves. Corroboration from the same runs: the absolute-lifetime
error changes **sign** across the range — GMAT is 2.5× longer at low activity, 9 % shorter
at mean, 23 % shorter at high. An error that changes sign is a wrong shape, not a
miscalibration.

**What survives:** ×1.80 as a point value at mean and high activity, checked independently
and comfortably inside band. **What does not:** invariance.

Reproduce the sweep in six lines, no edit to any script:

```python
from analysis.astro import lifetime, boosted_elements, RE
a0 = RE + 450e3
ab, eb = boosted_elements(450e3, 20.37)
for s in (0.25, 0.5, 1.0, 2.5, 5.0, 10.0):
    print(s, lifetime(ab, eb, scale=s) / lifetime(a0, 0.0, scale=s))
```

**Where the claim appears:**

| Location | Text | Status |
|---|---|---|
| `paper/paper.tex` **abstract** | "a ratio shown invariant across ballistic coefficient and a fivefold solar-activity density range" | corrected 2026-07-29 — multiplier now quoted at a stated activity level, no invariance claimed |
| `paper/paper.tex` Sec. V-B | "invariant to two decimal places" | corrected 2026-07-29 — carries the GMAT three-level result and the mechanism |
| `paper/paper.tex` sensitivity section | "a multiplier invariant across a fivefold density range" | corrected 2026-07-29 |
| `paper/paper.tex` **Limitations** | "the demonstrated invariance of the ratio is the defensible result" — the paper leaned on this specific claim | corrected 2026-07-29 — no longer offered as the defensible result |
| `README.md`, `wiki/Home.md` headline tables | "×1.80, invariant across BC and solar activity" | corrected 2026-07-28 → "×1.80 at mean activity — invariance falsified, see P16" |
| `RESULTS.md` A5 section and status bar | "GMAT: ×1.73 vs ×1.80, within band" | corrected 2026-07-28 — three-level table, per-activity chart, 40×-sweep chart, status FAIL |
| `docs/index.html` (Pages site) | headline row and GMAT section | corrected 2026-07-28 |
| `VALIDATION_REPORT.md` §2 | "2.55 % spread, inside the ≤5 % band" | corrected 2026-07-28, retraction stated in place |
| `INVENTORY.md` A32 | "Solar-activity UQ, ×1.80 invariance" | flagged against P16 |
| `CHANGELOG.md` VAL2-02 | "Invariance spread 2.55 %, inside ≤5 %" | marked SUPERSEDED, text left intact as audit record |
| `paper/figures/F11_uq.png` **caption** | "absolute lifetimes vary fivefold; the ×1.8 multiplier does not" — a fifth location, missed when this list was written | corrected 2026-07-29 — figure now plots `astro.py` against GMAT side by side |

**All documented locations are now corrected.** What is *not* closed:

1. **The BC half has still never been tested against a real atmosphere.** It is proven a
   tautology in `astro.py`, and the paper no longer claims it — but nobody has run GMAT at
   BC 40 and 90 to find out what the true BC dependence is. Until that happens the honest
   position is "unknown", not "invariant".
2. **The GMAT numbers themselves are now stale** — every run was at 20.37 m/s (P19).
3. **The committed PDF predates the correction** (`paper/README.md`).

This item stays open on (1).

**Ballistic-coefficient invariance is not "suspect" — it is the identical tautology, proved
2026-07-29.** The abstract's sentence has two halves: invariant across *ballistic
coefficient* **and** across a *fivefold solar-activity density range*. Both rest on the same
construction. In `lifetime()` the drag term is

```python
ft = -0.5 * rho(h, scale) * v ** 2 / BC
```

`scale` and `1/BC` are the **same multiplicative slot**. Scaling one is mathematically
indistinguishable from scaling the other, so a BC sweep is a density sweep wearing a
different label. The reciprocal test confirms it exactly:

| Configuration | Multiplier |
|---|---|
| BC = 61, scale = 2.0 | 1.7987 |
| BC = 30.5, scale = 1.0 | **1.7987** |
| BC = 122, scale = 1.0 | 1.7991 |
| BC = 61, scale = 0.5 | **1.7991** |

And the plain sweep across a 5× BC range, 30 → 150 kg/m²: 1.7983 → 1.7992, spread
**0.05 %**.

So the position is worse than "one half falsified, one half untested". **Neither half of the
claim was ever tested by a method capable of falsifying it**, and the half that was
independently checked failed. Closing the BC half needs the same medicine as the solar half —
GMAT runs at BC 40 and 90 — because MSIS's response to ballistic coefficient is not a uniform
rescale, for the same profile-shape reason found above.

**Do not edit `analysis/astro.py`.** Its arithmetic is not wrong; its atmosphere
parameterisation cannot express the effect being claimed. The fix is either a variable-shape
atmosphere in the script or dropping the invariance claim and keeping the point value —
that is a judgement, not a patch. Paper edits batch with P11/P12.

### P17. The inter-array attraction feeding the A4 FEA is 37 % high — HIGH, NEW 2026-07-29
`analysis/sizing.py::inter_array_attraction()` computes the force between the two opposed
Halbach faces from a flat-plate Maxwell-stress formula — a uniform pressure
`B_face**2 / (2*mu0)` at a mean face field of 0.55 T over the 340 x 90 mm footprint —
giving **3672 N**. That number was the applied load in the CalculiX A4 structural run
(`validation/results/A4_sled_structural.json`), and it had never been checked against
anything.

`magpylib.getFT()` meshes each magnet block and integrates the field gradient in three
dimensions. Driven by the repo's own array geometry (`build_field()`), so the two methods
cannot disagree about the magnets themselves:

| Mesh per block | Force |
|---|---|
| (2,2,2) | 2909.4 N |
| (4,4,4) | 2773.0 N |
| (6,6,6) | 2720.8 N |
| (8,8,8) | 2701.6 N |
| (10,10,10) | 2693.3 N |
| (12,12,12) | 2689.0 N |
| **(14,14,14)** | **2686.6 N** |

Converged — successive deltas halve (-8.3, -4.3, -2.5 N) — and insensitive to the
finite-difference step across four orders of magnitude (1e-5 to 1e-8, identical to 0.1 N).
**The analytic formula is high by 36.7 %.**

**The mechanism is understood, which is why this is a defect and not a disagreement.**
Maxwell stress needs the mean of `B**2`; the analytic form uses the square of the mean `B`;
and `mean(B**2) >= mean(B)**2` for any non-uniform field, by Jensen. A Halbach face field is
strongly non-uniform along the wavelength, so the analytic form must overestimate. It does.

**What this does and does not damage.** The real force is *lower*, so A4's structural
results are conservative, not wrong: 0.0194 mm airgap closure and 33.7 MPa were computed
against a load 37 % heavier than the field model supports, and all three bands still passed.
No A4 conclusion reverses. What is damaged is the claim that A4's inputs were checked — they
were not, and this is the first time anyone looked.

**Reproduce:** `python3 validation/magpylib/check_inter_array_force.py` (no new dependency;
magpylib 5.2.3 is already in `requirements.txt`).

**Procedural note, stated rather than hidden.** This was computed *before* an acceptance band
was declared for it, which inverts this project's own rule. It is therefore logged as a
discrepancy, not as a validated result. Proper closure needs a run sheet with a band declared
in advance, and a decision about whether `sizing.py` adopts a corrected formula — which would
move `plate_stress_MPa`, the retention-gate sizing, and the A4 load together. **Do not edit
`sizing.py` on the strength of this entry.**

### P18. Four physical effects are absent from the model, not merely unvalidated — MEDIUM, NEW 2026-07-29
Distinct from the E-items, which record analyses not yet run. These are terms that no script
contains, found by reading `sizing.py` and `motor_model.py` rather than the prose. Each is
carried as an E-item below (E19-E22); this entry exists so they are visible from the P-list,
because "the model does not contain this term" is a different class of gap from "this
analysis has not been run".

### Advanced or resolved by the CAD build (not full closures)
- **Launch restraint now exists as geometry.** The breech launch-lock blocks are modelled
  (`cad/parameters.json` `track`: `launch_lock` at x = 30–50 mm, 2 off). This advances
  **E10** (previously "concept-level") — the lock is drawn, though still not analysed.
- **Payload interface now models CDS corner rails** (see P6), giving the rail contact
  faces the interface-control drawing needs.

---

### P19. Every validation run predates the operating point they validate — HIGH, NEW 2026-07-29
Adopting the measured 9.445 kg sled moved the rated velocity from 20.37 to 16.537 m/s. The
three analyses that have actually been run were all executed at the **old** point, so none of
them currently validates the design as it stands:

| Analysis | Run at | Still valid? |
|---|---|---|
| **A5** GMAT lifetime | dv = 20.37 m/s | **No.** Both baseline and boosted orbits change; the multiplier the scripts now give is ×1.62, not ×1.80. The *falsification* of the invariance claim (P16) survives, because that is about the shape of the model and not the velocity — but the numbers do not. |
| **A8** ngspice pulse chain | F = 1413.4 N, m = 8.86 kg, 2630 J | **No.** The netlist carries the old mass and energy. Peak current moved 392 → 330 A and pulse duration 128 → 157 ms, which is exactly what that analysis exists to check. |
| **A4** CalculiX chassis | 3672 N Maxwell attraction | **Yes, structurally.** The load is magnetostatic and does not depend on sled mass or velocity. Separately 37 % high — see P17. |

**What this costs.** The validation table on the front pages says four of nine analyses have
run (A1 added 2026-07-29, and A1 alone is at the current operating point). Strictly, three have run *against a superseded design*. That is not the same claim, and
the difference is exactly the kind a reviewer notices.

**Cheapest closure first.** A8 is minutes — the netlist is `validation/spice/emocd_shot.cir`
and only its `.param` line needs the new operating point, though the declared bands must be
re-read before the run rather than after. A5 is days of wall time for the low-activity leg.
Neither should be re-run until the sled mass is settled, or the same staleness recurs; that
argues for closing the rib-stiffened-chassis question (P5, E2) **first**.

**Do not quietly restate the old results as if they still applied.** Every place the repo
quotes A5 or A8 numbers now needs the velocity they were obtained at stated alongside.

### P20. The A1 run sheet's array-surface reference is mis-specified — LOW, NEW 2026-07-29
A1 ran and missed two of its seven declared bands. **One of the two is a defect in the run
sheet, not in the model.**

`validation/A1_field_femm.md` declares the array-surface band against
`analytic_B0_surface_T` = 0.7714 T. That is the fundamental amplitude of a **single** array's
ideal Halbach wave at its own surface. But any measurement at that plane in a **double-sided**
machine inevitably includes the opposing array, whose contribution there is
`B0·exp(-k·GAP)` = 0.160 T. The correct double-sided reference is **0.9317 T**.

The FEM's fundamental at that plane is **0.9312 T — a ratio of 0.9994 against the correct
value.** Measured as a raw peak it reads 1.4641 T, because the plane sits on the magnet face
where block-corner harmonics dominate and the field is formally singular at the corners; a raw
peak there is mesh-dependent and is not the same quantity as a fundamental amplitude either.

**So the row failed as declared, and the model is right.** Both statements are true and both
are recorded. The band is **not** widened — `validation/A1_field_femm.md` is left exactly as
written on 2026-07-27, because a run sheet edited after seeing results is worth nothing. The
correction belongs in the *next* run sheet.

**Fix:** when A2 (3-D) is specified, declare the array-surface band against the double-sided
value and against the **fundamental**, not a raw peak. Two references need naming, not one.

### P21. Stray field at 50 mm: 2-D cannot test the far field — LOW, NEW 2026-07-29
The second A1 band miss. FEM gives 0.93 mT against a 0.4 mT reference, ratio **2.32** against
a factor-2 band.

**Cause identified, and it is geometric.** The FEM is 2-D: the array is infinitely long out of
plane. The real array is **90 mm deep**. At 10 and 20 mm behind the back face the observation
distance is small against that depth and the two agree (ratios 1.16 and 1.14, both inside
band). At 50 mm the distance is comparable to the depth, a finite source falls off faster than
an infinite one, and the 2-D model necessarily overestimates.

This is **converged, not noise**: the value sits at 0.93 mT across box sizes 0.5–0.8 m and
across mesh refinements from 32 k to 141 k elements.

**Consequence:** a 2-D method cannot validate this row, by construction. `A1_field_femm.md`
already says A1 "does not close 3-D end effects" — this is that limitation showing up in the
one row most sensitive to it. The magpylib reference, which models finite 90 mm blocks
exactly, is the more trustworthy number here and the FEM is not evidence against it.

**Do not** change `verify_field.py`. The row needs A2, a 3-D solve.

## E — Unsolved engineering

### E1. Three-dimensional field closure — 2-D HALF CLOSED 2026-07-29 by A1
> **A1 has run.** A meshed 2-D magnetostatic FEM (scikit-fem P1, 141 k elements, gmsh) gives
> **K_t = 11.228 N per kA/m against the model's 11.22 — a ratio of 1.0007** — with force
> ripple 1.25 % against 1.26 %. Midgap peak and winding mean both land at ratio 1.001.
> **The thrust band, the one that matters, is met.**
>
> What remains open is the 3-D half: end effects on a 340 mm array of finite 90 mm depth.
> P21 is that limitation showing up directly — the 2-D model overestimates far field because
> it has infinite depth. That needs A2.
`motor_model.py` resolves the winding in 2-D. End effects of a few percent on Kt remain
uncomputed. This is the declared close-out task for the electromagnetic model. The
magnetostatic package now exists — `analysis/femm/emocd_cross_section.dxf` plus
`analysis/femm/FEMM_RUN_SHEET.md` (analysis A1), which supersedes the older
`docs/FEMM_Run_Sheet.md`; the acceptance band in that older sheet predates the
winding-resolved model and should not be used. **Nothing has been run.** A1 closes the
2-D half; the 3-D end effects still need a 3-D solver (Elmer or GetDP are the free
options). Acceptance band declared in `validation/A1_field_femm.md`.

### E2. No FEA confirmation of anything — PARTIALLY CLOSED
> **Two FEA results now exist.** A4 (CalculiX, structural) ran 2026-07-28. **A1 (magnetostatic)
> ran 2026-07-29** and is the one that matters most: K_t had only ever been checked
> analytic-against-analytic — a closed-form wave model against magpylib, both superposing
> analytic solutions for uniform blocks, neither solving a field equation. A1 solves the PDE on
> a mesh and agrees to 0.07 %.
>
> Still open: no FEA of the track, the brake, or the cassette structure; and no 3-D
> electromagnetic solve (E1).
The field cross-check is analytic-vs-analytic (both magpylib and the wave model assume
ironless geometry, where superposition is exact). That is a genuine check of the wave
model but is NOT independent confirmation from a different physical method. Two analyses
are specified and neither has been executed: **A1** magnetostatic (E1 above) and **A4**
sled-chassis structural, which is what P5 and P8 are waiting on. Both, plus A5–A8, are
written up with pre-declared acceptance bands in `validation/`, and A5's GMAT toolkit is
built (`validation/gmat/`) though not yet run. A8 (pulse-power, E17) is
the cheapest of them and needs no CAD, no mesh, and no licence.

### E3. Masses are parametric and unchecked against vendor data
CAD now exists (`cad/`, nine documents), so the "no CAD" half of this item is closed —
but the mass problem is not. `mass_properties.py` still uses primitive solids with
shell/fill factors, and no component mass is checked against a vendor datasheet;
estimate spread perhaps ±15 %. Fusion-computed masses are **not** a substitute: they use
solid-copper stator, solid-aluminium CubeSats, and steel standing in for NdFeB, which is
why they are deliberately excluded from `cad/parameters.json`. The sled mass (4.86 kg)
propagates directly into the headline velocity — see P5 and P8 — and the enclosure,
radiator, and avionics are still missing from the rollup entirely (P10).

### E4. No hardware at any level
> **A protocol now exists, 2026-07-29.** `docs/BENCHTOP_TESTS.md` specifies four sub-scale
> experiments, cheapest first, each closing a named claim with its acceptance band declared
> in advance: a Halbach pair on a gaussmeter (B-1), single-coil thrust against
> K<sub>t</sub> (B-2), capacitor discharge against the pulse model (B-3), and a drop-test
> brake coupon against the plate-drag law (B-4). **B-1 costs roughly the price of two magnets
> and would give this project its first measured number.** Full-scale qualification is
> specified separately in `docs/QUALIFICATION_PLAN.md`. None of it is run — this item stays
> open until something is measured.
TRL 2–3. Nothing has been built, fired, or measured. The velocity, dispersion, and
tip-off claims are all model outputs.

### E5. Host stage properties unavailable
Recoil budgets are parametric across 300–900 kg host classes because no candidate
stage publishes its mass and control authority. Cannot be closed from public data.

### E6. Absolute orbital lifetimes are uncertain
Static exponential atmosphere at mean solar activity. Absolute lifetimes swing
severalfold across the solar cycle. The ×1.80 ratio was believed invariant and defensible;
**P16 has since falsified the invariance** — GMAT gives 1.73 / 1.78 / 2.07 across low to high
activity. The point value at mean and high activity survives; the invariance does not. `validation/A5_astro_orekit.md` specifies an independent
re-run under GMAT (toolkit built in `validation/gmat/`, Orekit an equally valid
substitute) — different codebases, independently implemented force models — with the band on the ratio and explicitly not on the absolutes. It now also
carries a second leg: reproduce the **measured** decay of 3–5 non-manoeuvring 3U CubeSats
from CelesTrak / Space-Track TLE histories, band 15 % on time-to-decay. Two models
agreeing is weaker than a model reproducing a flown decay, and the flight data is free.

### E7. Velocity dispersion rests on assumed sensor noise
The 0.027 m/s (3σ) result is a closed-loop simulation using an assumed 8 mm/s sensor
sigma and assumed tolerance distributions. No sensor has been selected or characterised.
The separation side of this is specified in `validation/A7_separation_chrono.md`, whose
tip-off band is taken from a flown deployer (NRCSD-E, < 5 °/s/axis) rather than chosen.

### E8. Brake energy is thrown away
~1.0 kJ per shot dissipated in the fin. Whether any of it is worth recovering (and what
that would cost in mass and complexity) has not been examined since the efficiency
correction.

### E9. 6U/12U variants are force-limited, not designed
The payload family table is arithmetic from the same thrust constant. No mechanism,
cassette, or structural design exists for larger classes.

### E10. Launch restraint is drawn but not analysed
Retention gate pin sizing exists (two D6 A-286, margin 1.2) and the breech launch-lock
blocks are now modelled in CAD (`cad/parameters.json` `track`: `launch_lock`, x = 30–50
mm, 2 off). The rest — escapement caging, cam lock, tolerance stack-up under vibration —
is drawn or described, not analysed.

### E11. No contamination or outgassing analysis
> **ADR-004 gains external support 2026-07-29:** coreless construction lowers outgassing and
> vacuum-rated ironless linear motors are catalogue products, so this architecture converges
> with fielded vacuum practice. Does not close the item — T-4 tests *this* material set.
> **Specified 2026-07-29** as T-4 in `docs/QUALIFICATION_PLAN.md`: 8 thermal-vacuum cycles,
> −40 to +60 °C, with ASTM E595 limits (TML ≤ 1.0 %, CVCM ≤ 0.1 %) as pass criteria. The
> materials rule B16 already requires E595-compliant selection; T-4 is where that gets tested
> rather than asserted. Not run.
Materials were selected against E595 limits by rule, not by analysis. No contamination
budget for customer optics exists.

### E12. EMC beyond stray field
> **Specified 2026-07-29** as T-6 in `docs/QUALIFICATION_PLAN.md`: MIL-STD-461 RE102/CE102
> class emissions during a 330 A pulse, plus static field measured at the payload envelope
> against the 22.7 / 4.3 / 0.4 mT model. A customer flying a magnetometer or magnetorquer
> needs that number measured, not modelled. Not run.
Static magnetic keep-out is computed. Induced currents from switching transients in
adjacent payloads are discussed but not calculated.

### E13. Two numbers in source documents were never traced
- The "780 deg/s" tumble rate from a third-party document. Falsified as
  implausible (would require a ~7.6 m line-of-action offset on a 1 m vehicle) but its
  origin was never found.
- The "1,000+ G hardening" figure, whose context (ground-launch guns) does not apply
  to this design.

### E14. Patent / disclosure — the disclosure has now happened
Concept and results are public (LinkedIn, and this repository, which is now a **public**
repo carrying the scripts and therefore the operating point). No provisional application
was filed first, so this is done and cannot be undone. What remains is not a decision but
a consequence to be handled: any patent route now runs on whatever post-disclosure grace
period applies in each jurisdiction — India and the US have one, most of Europe does not
— counted from the earliest public disclosure, not from today. **If a filing is still
wanted, establish that earliest date and take advice quickly.** If it is not, close this
item out explicitly so it stops reading as pending.

### E15. Sponsorship not secured
The build is the declared next step and is unfunded.

### E16. Reference hygiene
Three references in `paper/paper.tex` were flagged verify-before-submission and have
not been fully verified: eddy-damper heritage [15], Yudintsev separation dynamics [17],
and the vibro-impact deployment paper [18]. `docs/RELATED_WORK.md` adds a further list of
comparator sources and tooling — **none of it retrieved and read either**, and it carries
the same rule: fetch before citing. The differential-drag comparator (Foster et al., flown
Planet Labs results) is the one worth chasing first, since the paper's 25-day baseline is
currently a model output rather than a measurement.

### E17. The pulse-power chain — PARTIALLY CLOSED 2026-07-28 by A8, with two findings
**A8 has been run** (ngspice 42, `validation/spice/emocd_shot.cir`). All five declared bands
were met — exit velocity and pulse duration agree to 0.03 % across two different integrators,
peak current +5.98 %, sag +0.18 points, energy +3.59 %. Two findings came out of it anyway:

1. **Quoted sag is state-of-charge, not terminal voltage.** `motor_model.py` models no ESR
   at all; it reports the capacitor's charge depletion, 4.88 %. With a 12 mohm ESR the
   terminal droops to 86.16 V — a **10.25 % total sag**. The servo-headroom argument behind
   the 0.027 m/s dispersion claim is stated against the smaller number.
2. **The `Q_esr = 160 J` default does not reconcile with 12 mohm.** Integral of I^2 dt over
   the shot is 8008 A^2 s, giving 96 J at 12 mohm. The two agree only at about 20 mohm. This
   item asked for a second number against the 160 J; here it is.

The 12 mohm itself appears only in `docs/EMOCD_Computation_Results_C1-C10.md`, which is
superseded — **no current script defines a bank ESR**, which is the underlying gap.

Original item follows.

### E17 (as originally written). The pulse-power chain has never left the analytic model
The supercapacitor bank, the SiC bridge, and the winding exist only as lumped resistances
and ideal switching inside `motor_model.py` and `sizing.py`. Three numbers depend on that
model and nothing else: the **392 A peak current** (which sets the device rating and the
paper's derating discussion), the **4.9 % bank sag** (which underwrites the servo headroom
behind the 0.027 m/s dispersion claim), and the **672 J copper loss** (which carries the
32 % efficiency figure). No transient overshoot at commutation has been computed, and the
`Q_esr = 160 J` default in `sizing.py` — flagged as unsourced during the P2 review before
being traced to the script's own default — has no second number against it.

Specified as **A8** in `validation/A8_pulse_spice.md` (ngspice or PySpice, both free).
This is the least expensive analysis in the plan: no geometry, no mesh, no licence, and it
attacks three headline-adjacent numbers at once.

### E18. Conjunction covariance is invented — NEW 2026-07-27
Any probability-of-collision result (A6) inherits whatever covariance it is given, and no
covariance exists for a satellite that has never flown. Space-Track **Conjunction Data
Messages** carry real post-deployment covariances for comparable objects and are the
defensible source; `validation/A6_conjunction_cara.md` now names them as the preferred
input, with an explicitly documented assumption as the fallback. Until that is done, no Pc
figure from this project should be quoted as anything but conditional on its assumption.

### E19. Eddy-current heating inside the magnet blocks is not modelled — NEW 2026-07-29
> **Cross-industry review 2026-07-29** (`docs/CROSS_INDUSTRY.md`): this is a named, well-studied
> loss mechanism in PM machines, and **magnet segmentation is the standard mitigation — which
> reduces thrust and mechanical robustness.** That is a design option this project did not
> previously have. Item stays open: the literature is steady-state rotating machines, and
> nobody has computed the 157 ms pulsed case here.
`sizing.py::magnet_temperature()` models exactly one thermal effect on the magnets:
reversible remanence drift with ambient temperature, `alpha = -0.11 %/K`. NdFeB is a
conductor (roughly 1.4-1.6 uOhm*m, some 80-90x copper's resistivity but far from an
insulator), and the blocks sweep past the winding at up to 20 m/s through the field's
spatial harmonics — the belt winding's own 6th-harmonic ripple, slot-like content, and
whatever switching harmonics the SiC bridge puts on the current. That drives eddy currents
in the magnet bulk.

This is not the same failure mode as reversible drift. Local heating risks crossing the
knee point and causing **irreversible** demagnetisation, which no amount of cooling
recovers, and it is worst where the field harmonics are strongest rather than where the
bulk temperature sensor would sit.

No number is offered here because nothing in the repo computes one, and inventing an
order of magnitude for a loss that depends on harmonic content the model does not resolve
would be worse than recording the gap. What can be said without computation: this term
grows with current density, so it works directly against the "raise sheet current to
213 kA/m" option in `docs/DESIGN_OPTIONS_exit_velocity.md`, which that document already
calls thermally hard for the winding alone.

### E20. The brake's force-time profile does not exist — NEW 2026-07-29
`sizing.py` asserts a 200 g deceleration **cap**, used to size the magnet bond. No script
anywhere simulates the arrest: there is no force against velocity, no force against
position, no peak, and no duration. `legacy/c3_c4_em.py` sizes the brake by energy, not by
transient.

A first-order estimate from the sled's own kinetic energy across the 210 mm arrest zone
puts the **average** force near 6 kN over roughly 8-20 ms — some 4x the 1413 N
acceleration force, over a tenth of the duration, and with a peak that nothing bounds. The
host therefore sees two oppositely-signed impulses of very different shape per shot, not
one smooth push, and a 12-shot campaign is 24 load reversals through the ESPA bolted
interface.

E5 covers the *magnitude* of the recoil budget across host mass classes. Nothing covers its
*shape*, and A4 is a static analysis that cannot. This is a fatigue and control-bandwidth
question, and it is the natural companion to A7.

### E21. No vacuum tribology anywhere — SUBSTANTIALLY RETIRED BY CITATION 2026-07-29
> **This is solved engineering with a handbook.** The ESA Space Tribology Handbook (Roberts,
> ESTL) covers lubricant and component selection, cold welding, and rolling-element life in
> vacuum; MoS2 is the broadly accepted solid lubricant. **Twelve cycles is a trivial life
> requirement** by space-mechanism standards. The remaining task is a *selection calculation*
> against the 1.48 kN per pair load, not research. See `docs/CROSS_INDUSTRY.md`.
Searching the entire repository for lubrication, tribology, cold welding or galling returns
nothing. The sled runs on four rollers (30 mm dia x 16 mm) carrying roughly 763 N per pair
at arrest (`sizing.py::arrest_loads()`), reused across twelve shots, in vacuum. Repeated
metal-on-metal rolling and sliding contact in vacuum with marginal or no lubrication is a
well-known deployable-mechanism failure class, and the reusable sled is the one part of
this architecture that a single-shot spring deployer does not have to solve.

Distinct from the neighbouring items: E10 covers the launch-restraint escapement, E11
covers outgassing and contamination. Neither covers the roller-to-rail interface, and no
lubricant, coating, or material pair is specified for it in `cad/parameters.json`.

### E22. Parasitic eddy drag on the track structure is not in the thrust model — REFRAMED 2026-07-29
> **Reframed as a design rule rather than an analysis** (`docs/CROSS_INDUSTRY.md`): vendor
> ironless motors keep conductive structure out of the magnet track's field. Specify a minimum
> standoff and check the CAD against it — cheaper than the computation this item implied.
The eddy brake works because a moving Halbach field drags on a nearby stationary conductor.
That is also the geometry of the entire 1.3 m acceleration zone wherever aluminium or
titanium structure — longerons, guide rails, enclosure skins — sits within reach of the
field. `verify_field.py` puts the stray field at 22.7 mT at 10 mm behind the array and
4.3 mT at 20 mm, which is not negligible at plausible standoffs.

`motor_model.thrust_constant()` computes Kt purely as the Lorentz force against winding
current. It carries no term for eddy coupling into any other conductor. So the model
accounts for eddy drag exactly where it is wanted (the brake) and nowhere it might be
unwanted, and the sign is unfavourable: any such drag subtracts from delivered thrust and
adds heat to the track.

Not quantified here — it depends on the track-to-array standoff and the conductivity of
whatever is actually there, and the standoff is not a single number in `cad/parameters.json`.
The check is cheap once that geometry is pinned, and it belongs with A1.

### E23. Force-ripple harmonics sweep the track's own structural modes every shot — NEW 2026-07-29
> **The cogging half retires; the sweep half does not.** Ironless construction has zero cogging
> by design, so the largest ripple source in an iron-core machine is absent. But E23 is about
> the *electrical* ripple chirping through the modes, and industrial stages run at constant
> velocity and do not chirp. **No citation found addresses this** — it appears genuinely
> unusual (`docs/CROSS_INDUSTRY.md`).
`sizing.py::track_first_mode()` reports 48 Hz pinned-pinned and 109 Hz fixed-fixed, and
checks them against a single static target: above 70 Hz to clear the launch primary band.
That is the right check for the launch environment and the wrong one for the shot.

The electrical excitation is not at a fixed frequency. It sweeps from zero upward as
`f = n*v/lambda` with lambda = 48 mm, so every shot chirps through the whole band below the
running frequency. At the as-drawn 9.445 kg sled (a = 105 m/s^2):

| Crossing | Speed | Time from start | Distance into the 1300 mm stroke |
|---|---|---|---|
| 6th harmonic through the 48 Hz pinned mode | 0.38 m/s | 3.7 ms | 0.7 mm |
| 6th harmonic through the 109 Hz fixed mode | 0.87 m/s | 8.3 ms | 3.6 mm |
| fundamental through 109 Hz | 5.23 m/s | 49.8 ms | 130 mm |

So both modes are crossed inside the first 4-50 ms of a 127.7 ms stroke, twelve times per
campaign, and the crossings happen in the first few millimetres of travel where the sled is
still adjacent to the breech and the launch-lock hardware.

**The likely answer is that this is benign, and the point is that nobody has shown it.** The
sweep rate is roughly `a/lambda` ~ 2.2 kHz/s, so transit through any plausible half-power
bandwidth takes on the order of a millisecond, which is far too fast for resonant buildup.
But that argument depends on the structure's Q, and **no Q, damping ratio, or loss factor
appears anywhere in the repository**. A static frequency check against a launch target does
not settle a swept-excitation question; the analysis that would is a chirp or Campbell-style
dwell-time check, and it does not exist.

Cheap to close, and it belongs with A4's dynamic leg rather than with A1.
