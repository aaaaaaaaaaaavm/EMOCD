# Open problems, known errors, and the fix list

Two categories: **P-items are errors in the currently published paper** and should be
fixed first. **E-items are genuinely unsolved engineering.**

Last reviewed 2026-07-30.

---

## P: Errors found while building this repo (paper does not match its own scripts)

> **STATUS (2026-07-23): P1, P4 all RESOLVED in `paper/paper.tex`.** Fixes, causes and
> before/after values are logged in `CHANGELOG.md` (entries P2-01, P2-04). The items are
> kept in full below for the audit record. Two related defects found in the process were
> also fixed: the F06 conjunction figure was regenerated at the rated velocity, and a
> stale `astro.py` docstring value was corrected, both logged in `CHANGELOG.md`.

### P1. Conjunction minimum is wrong AND not a robust quantity: HIGH PRIORITY
**RESOLVED 2026-07-23, see CHANGELOG.md P2-01.**
The paper states a 30-day minimum satellite-to-stage approach of **45.3 km**. That
figure was computed at **20.65 m/s**, the superseded operating point. At the paper's
own rated velocity of **20.37 m/s**, `analysis/astro.py` gives **4.6 km**.

Worse, the quantity is fragile. Sweeping ejection velocity:

| Î”v (m/s) | min approach (km) |
|---|---|
| 20.00 | 37.5 |
| 20.37 (rated) | **4.6** |
| 20.50 | 56.1 |
| 20.65 (paper's value) | 45.3 |
| 21.00 | 63.4 |

This is a near-resonant beat sample, not a design property. A ±2.5 % velocity change
moves it by more than an order of magnitude.

**Follow-up:** `validation/A6_conjunction_cara.md` specifies the quantitative version,
probability of collision via NASA's CARA tools, which integrates over the covariance
instead of sampling one geometry. The test is whether Pc stays stable across the velocity
sweep that moves minimum distance by an order of magnitude.

> **A6 ran 2026-07-31 in a reduced form and P1 stays open.** Without GMAT, CARA or
> Space-Track there is no real covariance, so a 2-D Pc was computed against `astro.py`'s own
> propagator with an assumed one. **The stability test came back void**: at 14 to 63 km miss
> distances against a hundreds-of-metres covariance, Pc underflows double precision, and a
> spread of zeros is not a number.
>
> **What the run found instead is better than what it was looking for.** Pc has a maximum over
> covariance scale — a covariance wide enough to reach a 14.5 km miss is too diffuse to put
> probability inside a 5 m disc — and that maximum is **3.7e-8, some 2700x below the 1e-4
> anyone would act on, for any covariance whatsoever.** So Pc is not *robust* where distance is
> fragile; it is **irrelevant**, bounded far below any action threshold.
>
> **This does not close P1**, because a bound is not a probability. It does say the paper's
> current position — the 9.9-day realignment period plus mandatory per-shot COLA, and no
> minimum-distance claim — is the right one, and is now supported rather than merely honest.

**Fix:** stop quoting a specific minimum distance as a safety result. Reframe around
what IS robust: the ~8.1-day phase realignment period, and the mitigation of disposing
of the host stage before the first realignment. State plainly that per-shot COLA is
mandatory because the approach geometry is sensitive to exact ejection velocity.

### P2. Peak current is stale: MEDIUM PRIORITY
**RESOLVED 2026-07-23, see CHANGELOG.md P2-02.**
Paper says **323 A**. That belongs to the superseded 130 kA/m point. At the rated
140 kA/m, `motor_model.py` gives **392 A**. Fix the paper, and check that the SiC
device derating discussion still holds at the higher current (it should, 96 V rail,
1200 V devices, but the current rating of the bridge and busbars needs restating).

### P3. Far-field stray values don't reproduce exactly: LOW PRIORITY
**RESOLVED 2026-07-23, see CHANGELOG.md P2-03.**
Paper quotes 22.7 / 4.7 / 1.0 mT at 10 / 20 / 50 mm. `verify_field.py` reproduces
22.7 mT at 10 mm exactly but gives 4.3 and 0.4 mT at 20 and 50 mm. Likely sensitivity
to modelled array length (edge effects dominate the far field). The 10 mm value is the
one that sets the keep-out spec, so this is minor, but resolve it before anyone cites
the 20/50 mm numbers.

### P4. Brake fin temperature rise conflates per-shot with per-campaign: MEDIUM PRIORITY
**RESOLVED 2026-07-23, see CHANGELOG.md P2-04.**
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

## P: CAD reconciliation and packaging (found in the 2026-07-23 Fusion 360 CAD build)

> These arose when the parametric design was taken into CAD across nine Fusion documents.
> The CAD is authoritative for **geometry and fit only**; `analysis/*.py` remains
> authoritative for **mass and performance** until FEA closes the open items. All
> geometry values below are traceable to `cad/parameters.json`. **No number in
> `analysis/*.py` or `paper/paper.tex` has been changed** on the strength of the CAD.

### P5. CAD sled mass contradicts the parametric assumption: RESOLVED 2026-07-29
> **RESOLVED.** `motor_model.M_SLED` and `sizing.M_SLED` now carry the CAD-derived **9.445 kg**
> (P15), not the 4.86 kg parametric estimate. A4 ran, the drawn plate passed all three
> structural bands, and the measurement fell in the decision rule's ≥ 6.80 kg branch, so the
> rule resolved this rather than a judgement call. **Caveat carried forward:** 9.445 kg is
> the as-drawn, unpocketed geometry and A4 reports a 17x stress margin, so a rib-stiffened
> chassis would recover mass. Designing one is the open successor to this item
> (`docs/ROADMAP.md`), and it is tracked under E2 rather than here.

Original item follows for the audit trail.

> **UPDATE 2026-07-28, A4 structural leg has RUN (CalculiX).** The as-drawn 6 mm plate
> passes every declared band: 0.0194 mm airgap closure against a 0.025 mm per-plate budget,
> 33.7 MPa against 587 allowable, first mode 3408 Hz against >200. So there is **no
> structural argument for the chassis being lighter than drawn**, a lighter one has to be
> designed (rib-stiffened), not assumed. Combined with P15's CAD-derived 9.445 kg, the decision
> rule's ≥6.80 kg branch stands and the machine as it exists delivers **16.53 m/s**.
The first-pass Fusion sled (6 mm Ti-6Al-4V chassis, stiffness-driven by the ±0.05 mm gap
tolerance under 3.7 kN inter-array attraction — 2.69 kN since A12 — **no structural FEA behind it**) implies a
sled mass of **~7.50 kg**. `analysis/mass_properties.py` assumes **4.86 kg**, which
`motor_model.py` hard-codes as `M_SLED` and which sets the headline exit velocity. Both
are estimates (one CAD-geometric, one parametric-solid) and neither is FEA-verified. Do
not change the scripts until analysis A4 closes the chassis, specified with a
pre-declared decision rule in `validation/A4_sled_structural.md` (CalculiX or
Code_Aster, both free, both read `cad/step/gen3/EMOCD_Sled_Gen3.step`). Source:
`cad/parameters.json` (sled group, `PROVISIONAL_PENDING_FEA`).

### P6. Payload seating / orientation: RESOLVED (by CAD, 2026-07-23)
Resolved via the rail interface: the 3U payload now models the four CubeSat Design
Specification corner rails (8.5 mm, `cad/parameters.json` `payload_3u`), which fix seating
and orientation against the sled cradle. No further action.

### P7. Brake sits past the release point: geometry / ConOps
The eddy brake occupies **x = 1530-1740 mm**, beyond the **1500 mm** satellite release
point, on an 1800 mm longeron. The sled runs on into the brake after the payload departs
consistent with the fire-then-arrest ConOps, but it forces the track and enclosure to
extend past release, which drives the envelope length (see P9). Source:
`cad/parameters.json` (brake, track).

### P8. Exit velocity provisionally 17.88 m/s pending sled structural FEA: RESOLVED 2026-07-29
> **RESOLVED, and not at 17.88 m/s.** That figure came from the 7.50 kg CAD estimate. The
> CAD-derived mass is 9.445 kg, so the rated velocity is **16.537 m/s at 10.7 g**, now
> propagated into `analysis/`, `paper/paper.tex`, the figures and every front page. The
> machine is no longer acceleration-limited: at 10.7 g against a 25 g cap it is
> thrust-and-mass limited, which changes what recovering velocity means (mass or current,
> not stroke).

Original item follows for the audit trail.

If the CAD sled mass (P5) holds, exit velocity falls from the script's **20.37 m/s** to a
provisional **~17.88 m/s** (with acceleration ~12.5 g, efficiency ~24 %, recoil
~71.5 N·s, lifetime multiplier x1.68, all CAD-corrected and provisional). **These values
are NOT propagated into `analysis/*.py` or `paper/paper.tex`**; the scripts stay
authoritative until analysis A4 locks the sled mass (`validation/A4_sled_structural.md`,
which fixes in advance which of the two estimates wins at which mass). Do not hard-swap
20.37 to 17.88 anywhere. Source: 2026-07-23 CAD Master Plan; see README headline note.

### P9. Closed envelope exceeds ESPA Grande by ~44%: packaging / host
The closed installed envelope is **1839x 530x 940 mm** (`cad/parameters.json`). The
1839 mm length exceeds ESPA Grande's ~1270 mm longest-dimension class by ~44%, because
the brake lives past the 1500 mm release point and the enclosure spans it. Owner decision
(cannot be made in code): re-scope the host to POEM / custom accommodation (the paper
already leans host-agnostic), or shorten the track / repackage the brake. This supersedes
the earlier 1825x 516x ~1030 mm figure; the height change (1030 to 940) exceeds what skin
thickness explains and is **flagged for re-verification** in `cad/parameters.json`.

### P10. Enclosure, radiator, and packaged avionics absent from the mass rollup: MEDIUM (NEW)
The ninth document (`EMOCD_Enclosure`) adds 2 mm aluminium skins, a 1600x 200x 3 mm
radiator, and equipment bays for the supercapacitor bank, PPU, sequencer, and IMU. **None
have line items in `analysis/mass_properties.py`**, so the 72.3 kg dry-mass rollup is
incomplete. Add line items once masses are estimated (do not alter existing items without
cause). Source: `cad/parameters.json` (`enclosure.mass_note`).

### P11. The corrections may never have reached the submitted paper: RESOLVED 2026-07-29
> **RESOLVED: nothing has been submitted anywhere.** checked 2026-07-29.
> There is no version of record, so P1, P4 are not loose in any published document and no
> corrigendum is needed. `paper/archive/EMOCD_submission_uncorrected.pdf` is a draft build
> whose filename overstates its status, it was never sent.
>
> **This unblocks the paper edits that were batched behind it.** The reason P12 and P16 were
> left untouched in `paper/paper.tex` was that editing the source without rebuilding the PDF
> would split it from a published record. There is no published record. The paper is a draft,
> the only cost of editing it is that the committed PDF goes stale until it is recompiled,
> and that is a normal state for a draft rather than a defect. **Fix P12 and P16 in
> `paper.tex` and rebuild before anything is submitted.**

Original item follows, kept for the audit trail.


`paper/archive/EMOCD_submission_uncorrected.pdf` is a build of the paper that still
carries all four P1, P4 values (323 A, 23 A/mm² at 140 kA/m, 37 K per shot, 45.3 km
conjunction minimum). Its filename says *submission*. If that is genuinely the version
that went to the conference, then P1, P4 are corrected **only in this repository** and the
version of record is still wrong, which is a different situation from the STATUS block
at the top of this file, and one that a corrigendum, not a git commit, has to fix.
**Confirm which build was submitted.** If it was the uncorrected one, decide between
withdrawing, submitting an erratum, or correcting at the camera-ready stage, and record
the outcome here. If the submitted build was in fact compiled from the corrected
`paper.tex`, delete this item and say so in `CHANGELOG.md`.

### P12. The paper contradicts the CAD in two places: RESOLVED 2026-07-29
> **RESOLVED in `paper/paper.tex`.** The Limitations section no longer says masses derive
> from a parametric model rather than detailed CAD; it states what the CAD solid-volume calculation gives and what
> that costs. The ESPA-Grande envelope is no longer asserted as a capability, the
> requirement statement, the Fig. 2 caption and the accommodation section now record 1839 mm
> against the ~1270 mm class and name it an open packaging problem (P9). The mounting-interface
> statements were true and are unchanged. **The committed PDF still predates these edits**;
> see `paper/README.md`.

Original item follows for the audit trail.

Found while sweeping the repository for stale values. Both are prose claims, not computed
numbers, and neither has been changed in `paper/paper.tex`:

1. **Limitations (Sec. XV) says "Masses derive from a parametric solid model, not detailed
   CAD."** That was true when written and is now false, nine Fusion documents exist in
   `cad/`. The honest replacement is not "CAD exists" but the sharper statement: two mass
   estimates exist, they disagree by 54 %, and neither is FEA-verified (P5, P8).
2. **The paper claims an "ESPA-Grande-class envelope and mass allocation"** (abstract-level
   requirement, the Fig. 2 caption, and again in the accommodation section). The CAD closed
   envelope is 1839 mm against the ~1270 mm class limit, **P9, ~44 % over**. As written,
   the paper asserts a compatibility the geometry does not support.

Item 2 is the serious one: it is a capability claim, not a caveat, and it is the kind of
thing a reviewer with an ESPA user's guide open would catch immediately.

**Why this is not fixed yet.** Editing `paper.tex` without rebuilding the PDF would put the
source and the committed build out of step, and no TeX engine is available in the working
environment. It is also entangled with **P11**: until it is known which build is the
version of record, it is not clear whether this is a camera-ready edit or a corrigendum.
Resolve P11 first, then fix both items in one pass and rebuild.

### P13. The committed STEP set was mixed-generation, with two stubs: RESOLVED 2026-07-28
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

### P14. Gen3 CAD defects not previously tracked: NEW 2026-07-28
From the Gen3 audit in `cad/CHANGELOG_CAD.md`, verified against the exports where possible.
None of these were in this file before.

| ID | Defect | Consequence |
|---|---|---|
| G3-D1 | Cassette height **640 mm** in Gen2 and Gen3 against `parameters.json` `magazine.cassette_height_z = 690` | 50 mm short. Either the CAD or the parameter is wrong; `parameters.json` wins by rule, so the CAD needs correcting |
| G3-D2 | Track is longerons and launch locks only, **no roller channels, guide flanges, or cross-tie outriggers**, all of which `parameters.json` specifies | The 205 mm overall track width exists only as a parameter. The rollers on the sled have nothing modelled to run in |
| G3-D4 | **Stator layer count still open.** Gen1 built two layers (324 conductors), Gen2 and Gen3 one (162) | `parameters.json` flags the decision open. Roughly x2 force for the same sheet current against x2 copper mass, never computed. This sits upstream of Kt and therefore of the headline velocity |
| G3-D5 | Halbach arrays **not re-centred** after the chassis grew 360 to 488 mm | `sled.halbach_array_x_start = 230 mm` is inherited from the shorter chassis. Array position relative to the winding is what Kt depends on |
| G3-D6 | **No payload-on-sled rigid joint** in any generation | `parameters.json` `documents.EMOCD_Assembly` specifies one. Without it the assembly cannot express the payload riding the sled, which is the thing being modelled |

| G3-D12 | **Assembly geometry extends 156 mm aft of the recorded envelope.** `EMOCD_Assembly_Gen3.step` spans x = −188 to 1810 mm; `parameters.json` records the installed envelope as −32 to 1807 mm | Either the assembly parks the sled further aft than the envelope assumed, or the envelope was measured without it. Found on 2026-07-28 while meshing the assembly for `cad/stl/`. It makes P9 worse, not better: 1998 mm against the ~1270 mm ESPA Grande class limit is ~57 % over rather than ~44 %. Measure which component owns the −188 mm face before changing either number |

**Resolved and recorded:** ESPA bolt holes (24x M9 on Ø400 mm BCD) were absent in Gen1 and
Gen2 and are modelled in Gen3, G1-D5 closed.

**Two discrepancies between `cad/CHANGELOG_CAD.md` and its own exports**, found on import
and left in place there with a note rather than edited:

- **The Gen3 brake-placement fix is not in the exports.** G2-D4 says the Gen2 brake sat at
  the local origin and Gen3 moved it to x = 1530 mm. `EMOCD_Brake_Gen2.step` and
  `EMOCD_Brake_Gen3.step` are geometrically identical, 3 bodies each, 79 points each,
  differing only in file name and time stamp, and **both** already place the brake at
  1530-1740 mm. The fix may have been applied to the Fusion document before the Gen2 export
  was taken; either way the export does not show the defect it is said to have.
- Body counts: `EMOCD_Payload_3U_Gen1.step` measures 5 solids where the inventory says 1,
  and `EMOCD_Sled_Gen1b.step` measures 11 where it says ~16.

The sled fix **is** verifiable: Gen2 chassis half-length measures 180 mm (360 mm plate),
Gen3 measures 244 mm (488 mm plate), so G2-D1 is genuinely closed.

### P15. The Gen3 sled as drawn is 9.45 kg, above BOTH existing estimates: RESOLVED 2026-07-29
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
| **Gen3 geometry, CAD solid-volume result** | **9.445 kg** | **16.53 m/s** at 10.7 g, 19.0 % efficiency |

The method reproduces P8 exactly when fed 7.50 kg, it returns 17.87 m/s against P8's stated
17.88, so the discrepancy is in the mass, not the method. Dominated by two chassis plates
(3.63 kg of titanium) and the magnet arrays (3.67 kg of NdFeB).

**What it does not settle.** This is geometry times density, not the structural FEA that A4
specifies. The plates are drawn solid with no lightening pockets, and a real design would
pocket them; the stiffness constraint (airgap held to ±0.05 mm) is still unevaluated. But
A4's pre-declared rule already says a mass at or above 6.80 kg makes 17.88 m/s the headline,
and this is well past that. **Whichever way the FEA goes, the 20.37 m/s headline is not
supported by the geometry that currently exists.**

Do not edit `analysis/*.py` on the strength of this. Run A4, then propagate once.

### P16. The lifetime-multiplier INVARIANCE claim is falsified: HIGH, NEW 2026-07-28
GMAT R2022a, run headless against the bands declared in `validation/A5_astro_orekit.md`
before the run:

| Solar activity | GMAT multiplier | vs x1.80 | Band ±5 % |
|---|---|---|---|
| High (F10.7 250) | 1.7302 | −3.88 % | pass |
| Mean (F10.7 150) | 1.7750 | −1.39 % | pass |
| **Low (F10.7 70)** | **2.0739** | **+15.21 %** | **FAIL** |

Spread across the three: **18.48 %** against a ≤5 % band.

**The mechanism, and it is not subtle.** `analysis/astro.py` represents solar activity as a
uniform multiplicative scale on density (`rho(h, scale)`). Sweeping that scale across a
factor of **forty** moves the multiplier from 1.7992 to 1.7968, 0.1 %. A uniform density
factor divides both lifetimes by the same number, so **the ratio is preserved by
construction**. The sweep that the paper cites as demonstrating invariance cannot, in
principle, do so.

MSIS varies the *shape* of the density-altitude profile with F10.7, not only its magnitude.
The boosted orbit's apogee sits ~37 km above the baseline's, the two sample the profile
differently, and the ratio moves. Corroboration from the same runs: the absolute-lifetime
error changes **sign** across the range, GMAT is 2.5x longer at low activity, 9 % shorter
at mean, 23 % shorter at high. An error that changes sign is a wrong shape, not a
miscalibration.

**What survives:** x1.80 as a point value at mean and high activity, checked independently
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
| `paper/paper.tex` **abstract** | "a ratio shown invariant across ballistic coefficient and a fivefold solar-activity density range" | corrected 2026-07-29, multiplier now quoted at a stated activity level, no invariance claimed |
| `paper/paper.tex` Sec. V-B | "invariant to two decimal places" | corrected 2026-07-29, carries the GMAT three-level result and the mechanism |
| `paper/paper.tex` sensitivity section | "a multiplier invariant across a fivefold density range" | corrected 2026-07-29 |
| `paper/paper.tex` **Limitations** | "the demonstrated invariance of the ratio is the defensible result", the paper leaned on this specific claim | corrected 2026-07-29, no longer offered as the defensible result |
| `README.md`, `wiki/Home.md` headline tables | "x1.80, invariant across BC and solar activity" | corrected 2026-07-28 to "x1.80 at mean activity, invariance falsified, see P16" |
| `docs/RESULTS.md` A5 section and status bar | "GMAT: x1.73 vs x1.80, within band" | corrected 2026-07-28, three-level table, per-activity chart, 40x-sweep chart, status FAIL |
| `docs/index.html` (Pages site) | headline row and GMAT section | corrected 2026-07-28 |
| `docs/VALIDATION_REPORT.md` §2 | "2.55 % spread, inside the ≤5 % band" | corrected 2026-07-28, retraction stated in place |
| `docs/INVENTORY.md` A32 | "Solar-activity UQ, x1.80 invariance" | flagged against P16 |
| `CHANGELOG.md` VAL2-02 | "Invariance spread 2.55 %, inside ≤5 %" | marked SUPERSEDED, text left intact as audit record |
| `paper/figures/F11_uq.png` **caption** | "absolute lifetimes vary fivefold; the x1.8 multiplier does not", a fifth location, missed when this list was written | corrected 2026-07-29, figure now plots `astro.py` against GMAT side by side |

**All documented locations are now corrected.** What is *not* closed:

1. **The BC half has still never been tested against a real atmosphere.** It is proven a
   tautology in `astro.py`, and the paper no longer claims it, but nobody has run GMAT at
   BC 40 and 90 to find out what the true BC dependence is. Until that happens the honest
   position is "unknown", not "invariant".
2. **The GMAT numbers themselves are now stale**, every run was at 20.37 m/s (P19).
3. **The committed PDF predates the correction** (`paper/README.md`).

This item stays open on (1).

**Ballistic-coefficient invariance is not "suspect", it is the identical tautology, proved
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

And the plain sweep across a 5x BC range, 30 to 150 kg/m²: 1.7983 to 1.7992, spread
**0.05 %**.

So the position is worse than "one half falsified, one half untested". **Neither half of the
claim was ever tested by a method capable of falsifying it**, and the half that was
independently checked failed. Closing the BC half needs the same medicine as the solar half,
GMAT runs at BC 40 and 90, because MSIS's response to ballistic coefficient is not a uniform
rescale, for the same profile-shape reason found above.

**Do not edit `analysis/astro.py`.** Its arithmetic is not wrong; its atmosphere
parameterisation cannot express the effect being claimed. The fix is either a variable-shape
atmosphere in the script or dropping the invariance claim and keeping the point value,
that is a judgement, not a patch. Paper edits batch with P11/P12.

### P17. The inter-array attraction feeding the A4 FEA is 37 % high: **RESOLVED 2026-07-31 by A12**
> **Closed by [`validation/A12_inter_array_force.md`](validation/A12_inter_array_force.md), five
> of five declared bands.** A second numerical method — a Maxwell stress tensor integrated over
> the mid-gap plane, sharing only the block model of the magnets — gives **2627.6 N** against
> magpylib's **2686.6 N**, 2.2 % apart. `sizing.py` adopted 2686.6 N under an adoption rule
> declared before the run: attraction 3.68 → **2.69 kN**, plate stress 33 → **24 MPa**, margin
> 20.2 → **28.1**. A4 is not re-run; it was loaded 37 % heavy, so it was conservative and its
> verdict stands.
>
> **The number below was right and the mechanism below is wrong**, which is why the entry is
> corrected in place rather than deleted. See the correction at the end.
`analysis/sizing.py::inter_array_attraction()` computes the force between the two opposed
Halbach faces from a flat-plate Maxwell-stress formula, a uniform pressure
`B_face**2 / (2*mu0)` at a mean face field of 0.55 T over the 340 x 90 mm footprint,
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

Converged (successive deltas halve (-8.3, -4.3, -2.5 N)) and insensitive to the
finite-difference step across four orders of magnitude (1e-5 to 1e-8, identical to 0.1 N).
**The analytic formula is high by 36.7 %.**

~~**The mechanism is understood, which is why this is a defect and not a disagreement.**
Maxwell stress needs the mean of `B**2`; the analytic form uses the square of the mean `B`;
and `mean(B**2) >= mean(B)**2` for any non-uniform field, by Jensen. A Halbach face field is
strongly non-uniform along the wavelength, so the analytic form must overestimate. It does.~~

> **CORRECTED 2026-07-31 by A12. The inequality is right and the conclusion drawn from it is
> the wrong way round.** If `mean(B^2) >= mean(B)^2`, a one-point form evaluated at the *true*
> mean field **under**estimates. Jensen cannot be why the analytic value is high.
>
> A12 decomposed it against M2's own field statistics on the stress plane:
>
> | | Force | |
> |---|---|---|
> | Analytic, `B_face = 0.550 T` assumed | 3683 N | as published |
> | Same one-point form at the **actual** mean, 0.4127 T | 2073 N | **x1.776 from the assumed field** |
> | Full integral, `mean(B_y^2)` | 2628 N | **x1.267 back the other way, from Jensen** |
>
> Net x1.402 against an observed x1.402. **The cause is the input, not the formula:** 0.55 T is
> not the mean normal field on the plane where the stress acts. The flat-plate form's own Jensen
> error is 27 % and in the *safe* direction; it was fed a field 0.33x too high, which swamps it.
>
> **A right number with a wrong explanation attached is worse than an open question**, because
> it survives review and then misleads whoever picks it up next. That is why this is struck
> through and left visible rather than quietly rewritten.

**What this does and does not damage.** The real force is *lower*, so A4's structural
results are conservative, not wrong: 0.0194 mm airgap closure and 33.7 MPa were computed
against a load 37 % heavier than the field model supports, and all three bands still passed.
No A4 conclusion reverses. What is damaged is the claim that A4's inputs were checked, they
were not, and this is the first time anyone looked.

**Reproduce:** `python3 validation/magpylib/check_inter_array_force.py` (no new dependency;
magpylib 5.2.3 is already in `requirements.txt`).

**Procedural note, stated rather than hidden.** This was computed *before* an acceptance band
was declared for it, which inverts this project's own rule. It is therefore logged as a
discrepancy, not as a validated result. Proper closure needs a run sheet with a band declared
in advance, and a decision about whether `sizing.py` adopts a corrected formula, which would
move `plate_stress_MPa`, ~~the retention-gate sizing,~~ and the A4 load together. **Do not edit
`sizing.py` on the strength of this entry.**

> **Done 2026-07-31.** A12 declared the bands and the adoption rule first, then ran. The
> retention gate is struck above because it does not depend on this: `retention_gate()` is sized
> from a 24 kg ascent stack at 25 g. This entry was wrong about its own blast radius.

### P18. Four physical effects are absent from the model, not merely unvalidated: MEDIUM, NEW 2026-07-29
Distinct from the E-items, which record analyses not yet run. These are terms that no script
contains, found by reading `sizing.py` and `motor_model.py` rather than the prose. Each is
carried as an E-item below (E19-E22); this entry exists so they are visible from the P-list,
because "the model does not contain this term" is a different class of gap from "this
analysis has not been run".

### Advanced or resolved by the CAD build (not full closures)
- **Launch restraint now exists as geometry.** The breech launch-lock blocks are modelled
  (`cad/parameters.json` `track`: `launch_lock` at x = 30-50 mm, 2 off). This advances
  **E10** (previously "concept-level"), the lock is drawn, though still not analysed.
- **Payload interface now models CDS corner rails** (see P6), giving the rail contact
  faces the interface-control drawing needs.

---

### P19. Every validation run predates the operating point they validate: HIGH, NEW 2026-07-29
Adopting the CAD-derived 9.445 kg sled moved the rated velocity from 20.37 to 16.537 m/s. The
three analyses that have actually been run were all executed at the **old** point, so none of
them currently validates the design as it stands:

| Analysis | Run at | Still valid? |
|---|---|---|
| **A5** GMAT lifetime | dv = 20.37 m/s | **No.** Both baseline and boosted orbits change; the multiplier the scripts now give is x1.62, not x1.80. The *falsification* of the invariance claim (P16) survives, because that is about the shape of the model and not the velocity, but the numbers do not. |
| **A8** ngspice pulse chain | F = 1413.4 N, m = 8.86 kg, 2630 J | **Re-run 2026-07-30 as A8-R** against fresh bands, at 16.537 m/s. Five of six met; the closure row failed and produced P24. This half of the item is closed. |
| **A4** CalculiX chassis | 3672 N Maxwell attraction | **Yes, structurally.** The load is magnetostatic and does not depend on sled mass or velocity. **37 % heavy**, corrected to 2686.6 N by A12 — so A4 is conservative and is deliberately not re-run. |

**What this costs.** The validation table on the front pages says four of nine analyses have
run (A1 added 2026-07-29, and A1 alone is at the current operating point). Strictly, three have run *against a superseded design*. That is not the same claim, and
the difference is exactly the kind a reviewer notices.

**A8 is done.** A5 remains, and is days of wall time for the low-activity leg.
Neither should be re-run until the sled mass is settled, or the same staleness recurs; that
argues for closing the rib-stiffened-chassis question (P5, E2) **first**.

**Do not quietly restate the old results as if they still applied.** Every place the repo
quotes A5 or A8 numbers now needs the velocity they were obtained at stated alongside.

### P20. The A1 run sheet's array-surface reference is mis-specified: LOW, NEW 2026-07-29
A1 ran and missed two of its seven declared bands. **One of the two is a defect in the run
sheet, not in the model.**

`validation/A1_field_femm.md` declares the array-surface band against
`analytic_B0_surface_T` = 0.7714 T. That is the fundamental amplitude of a **single** array's
ideal Halbach wave at its own surface. But any measurement at that plane in a **double-sided**
machine inevitably includes the opposing array, whose contribution there is
`B0·exp(-k·GAP)` = 0.160 T. The correct double-sided reference is **0.9317 T**.

The FEM's fundamental at that plane is **0.9312 T, a ratio of 0.9994 against the correct
value.** Measured as a raw peak it reads 1.4641 T, because the plane sits on the magnet face
where block-corner harmonics dominate and the field is formally singular at the corners; a raw
peak there is mesh-dependent and is not the same quantity as a fundamental amplitude either.

**So the row failed as declared, and the model is right.** Both statements are true and both
are recorded. The band is **not** widened, `validation/A1_field_femm.md` is left exactly as
written on 2026-07-27, because a run sheet edited after seeing results is worth nothing. The
correction belongs in the *next* run sheet.

**Fix:** when A2 (3-D) is specified, declare the array-surface band against the double-sided
value and against the **fundamental**, not a raw peak. Two references need naming, not one.

### P21. Stray field at 50 mm: 2-D cannot test the far field: LOW, NEW 2026-07-29
The second A1 band miss. FEM gives 0.93 mT against a 0.4 mT reference, ratio **2.32** against
a factor-2 band.

**Cause identified, and it is geometric.** The FEM is 2-D: the array is infinitely long out of
plane. The real array is **90 mm deep**. At 10 and 20 mm behind the back face the observation
distance is small against that depth and the two agree (ratios 1.16 and 1.14, both inside
band). At 50 mm the distance is comparable to the depth, a finite source falls off faster than
an infinite one, and the 2-D model necessarily overestimates.

This is **converged, not noise**: the value sits at 0.93 mT across box sizes 0.5-0.8 m and
across mesh refinements from 32 k to 141 k elements.

**Consequence:** a 2-D method cannot validate this row, by construction. `A1_field_femm.md`
already says A1 "does not close 3-D end effects", this is that limitation showing up in the
one row most sensitive to it. The magpylib reference, which models finite 90 mm blocks
exactly, is the more trustworthy number here and the FEM is not evidence against it.

**Do not** change `verify_field.py`. The row needs A2, a 3-D solve.

### P22. The novelty claim was wrong, and its replacement rests on abstracts: HIGH, NEW 2026-07-30
A literature check found **published work on this exact concept that the paper did not cite.**
Full record in [`docs/PRIOR_ART.md`](docs/PRIOR_ART.md).

**What was wrong.** §I asserted *"no published deployment system operates in the tens of m/s."*
Feng, Yang & Wu (*Int. J. Aerospace Eng.* 2025, art. 3000765) analyse an on-orbit multi-stage
induction coilgun regulating a 20 kg CubeSat to **321.56 m/s**, with a reachable-domain analysis
serving the same purpose as this paper's lifetime and phasing argument. It was published
**2025-11-12, eight months before this repository went public.** The sentence was false as written.

**What it was changed to.** The regime is unserved *by flown hardware*, which is what the
comparator table always actually showed. The contribution is re-scoped to the narrower and more
defensible claim: a **programmable velocity delivered to an unmodified satellite inside its own
qualification envelope.** Both qualifiers carry weight, and against Feng they carry more than they
did against a spring:

| | Why it holds |
|---|---|
| Unmodified satellite | An induction coilgun accelerates a *conductive armature*, attached to the customer satellite, or a sabot needing its own separation. ADR-006 forbids the first |
| Inside the g-limit | 321.56 m/s at 10.7 g requires a **493 m track**; over 1.5 m it is **3515 g**. Not a secondary payload |

The g-limit argument is not new (ADR-003 made it in mid-2025) but it was an assertion and is now
arithmetic against a published number.

**The declared band, and what happened to it.** Before the full texts were obtained, this was
written down: *if Feng et al. report closed-loop per-satellite velocity regulation at dispersion
comparable to this design's 0.027 m/s 3σ, "programmable" stops being a differentiator; if they
report a track length making 321 m/s survivable for a standard CubeSat, §I needs rewriting rather
than adjusting.*

**All five papers were then supplied and read on 2026-07-30. Neither trigger fired, and three of
this entry's own conclusions turned out to be wrong.** Corrections in
[`docs/PRIOR_ART.md`](docs/PRIOR_ART.md); the material ones:

| Claimed from the abstract | After reading |
|---|---|
| "321.56 m/s at 10.7 g would need a 493 m track", a hypothetical | Their **actual** barrel is 3.9 m to **1352 g** mean, ~3060 g peak from their own >600 kN. The fact is far more decisive than the hypothesis |
| ADR-003's unsourced "1-2 % coilgun efficiency", removed *pending Einat* | **False.** Feng reports **14.9-19.9 %**, comparable to this design's own 20 %. Einat cannot settle it, a **2.5 g** projectile. Argument withdrawn as wrong, not deferred |
| *Aerospace* 12(6) 466 "has experimental verification" | True but narrower: a **32.8 mm/s transport mechanism**, not an ejection |

**Feng quotes no dispersion figure at all**, and controls velocity by charging-voltage selection
(10 to 16 kV to 230 to 321.56 m/s). So the dispersion differentiator survives, but as a claim about
*absent evidence*, not about impossibility, and it is written that way now. Feng is also
**simulation-only**, so on maturity this project and theirs are peers rather than this one being
behind.

**Why it stays open.** The claim corrections have landed, but two things are unfinished:

1. **The reachable-domain method should probably be adopted.** Feng's 3-D reachable-set envelope
   answers "which orbits does one shot make available" directly, where this project reports a scalar
   lifetime multiplier. That is a better astrodynamic product and it is the strongest thing to take
   from this literature. Not yet done, Phase II candidate.
2. **E24**, below: Xu et al. model attitude disturbance from the transfer mechanism itself. This
   project has nothing on disturbance from magazine indexing between shots.

**The maturity gap is real and remains.** The Harbin group built and measured a prototype. This
project has measured nothing. `docs/BENCHTOP_TESTS.md` already specified the answer as **B-1** and
**B-2**; what was added on 2026-07-30 is that their bands are now **derived** from an error budget
rather than chosen, by `validation/bench/bench_predict.py`. See E4.

### P23. The stroke time is stale in six places, and A8's band was set at the old one: MEDIUM, NEW 2026-07-30
Found while building the shot animation, which draws its time axis from `motor_model.shot()`
and came out at **157.3 ms** against the **127.7 ms** printed everywhere else.

127.7 ms is the superseded figure. Under constant acceleration the stroke time is `2s/v`:

| Operating point | 2s/v over the 1.30 m accel zone |
|---|---|
| 20.370 m/s, the pre-P15 point | 127.6 ms |
| 16.537 m/s, current | 157.2 ms |

So it belongs to the 4.86 kg parametric sled and survived the P8/P15 propagation in six
places: `README.md` twice, this file's E23 entry, `validation/A8_pulse_spice.md` twice, the
`CHANGELOG` record of A8's bands, and `docs/VALIDATION_REPORT.md`.

**The part that matters is not the typo.** `validation/A8_pulse_spice.md` declared a band of
**127.7 ms +/-10 %**, so 114.9 to 140.5 ms, and `VALIDATION_REPORT.md` records A8 passing it at
127.66 ms. At the current operating point the value is 157.3 ms, which is **23 % above the band
centre and outside the band entirely**. A8's recorded pass is a pass against a superseded
target.

This is the concrete instance of what P19 says in general. It is not a new failure: A8 ran
correctly against the operating point that existed when it ran. But "A8 passed" cannot be
quoted without saying which operating point it passed at, and until it is re-run the row in
`VALIDATION_REPORT.md` overstates what is known.

**Done:** the four prose occurrences corrected to 157.3 ms.

**Closed 2026-07-30 by A8-R.** The original band and its recorded result are left exactly as they
were, marked as belonging to the superseded point, because rewriting a declared band after the
fact to fit a new number is the one move that would make the whole validation record worthless.
Fresh bands were written and committed before the deck was touched, and the re-run passes the
pulse-duration row at 157.26 ms against 157.3. It failed a different row, which is P24.

### P24. No script carries a bank ESR, and the placeholder standing in for it is a factor of two high: HIGH, NEW 2026-07-30
Found by A8-R, the re-run of the pulse-power simulation at the current operating point
(`validation/A8_pulse_spice.md`). Five of six bands passed. Energy closure failed at **97.0 %**
against a declared 98-102 %.

The simulated draw exceeds the analytic accounting by **86.6 J**. That gap is bank ESR
dissipation, which the circuit deck models and the analytic ledger has no term for:

| | |
|---|---|
| I^2 dt over the shot, integrated by ngspice | 7126.2 A^2 s |
| Bank ESR, per `sizing.py` | 0.012 ohm |
| Product | **85.5 J**, against an 86.6 J gap, agreeing to 98.7 % |

**The ledger is internally consistent and still understates the bank.** `energy_closure()` has no
ESR term, and the `E_DRAWN = 2795.6 J` it closes against comes from `motor_model.py`, which has no
ESR either. Both sides of the equation omit the same term, so the closure reads 100.0 % while the
real draw is about **2881 J**, 3 % higher.

**What moves if the term is carried:**

1. **`thermal_campaign()` carries `Q_esr = 160 J`** as a literal default. Against 85.5 J that is
   1.9x high, and the twelve-shot campaign falls from 28.9 to 28.0 kJ. It was flagged as unsourced
   during the P2 review and has had no second number against it until now.
2. **The per-shot energy headline, 2.80 kJ**, is the analytic draw and appears on the front pages.
   It becomes 2.88 kJ, and electrical-to-payload efficiency falls from 19.6 to about 19.0 %.
3. **Quoted bank sag, 5.19 %**, is the charge depletion with no ESR in the loop. The true figure is
   the 5.35 % A8-R measured.

### Retracted, same day it was written: the claim that the bank goes undersized

This entry first stated that `capacitor_sizing()` at the true draw wants **6.18 F** against the
6.0 F selected, and that the bank was therefore chosen against a draw omitting a loss it causes.
**That is wrong, and the error is in how it was computed.** The 6.18 F came from raising the
energy to 2881 J while holding `SAG_FRAC` at 5.19 %. The two are not independent: the ESR
dissipation is drawn out of the same capacitor, so a higher draw *is* the higher sag. Evaluated
consistently, at 2881 J and 5.35 %,

```
C = 2E / (V0^2 - V1^2) = 2(2881) / (96^2 - 90.864^2) = 6.00 F
```

against 6.0 F selected. **The bank is correctly sized and always was.** The sizing function is not
implicated, and the propagation below is a constant change rather than a design decision.

The mechanism is worth naming because it is a general trap in this repository: `capacitor_sizing()`
takes `E` and `sag_frac` as separate arguments, and its own docstring warns that `sag_frac` is the
droop the shot integration reaches rather than a target. Feeding it a new energy with a stale sag
violates that, and the function has no way to notice.

### Propagated 2026-07-30, in the same pass that wrote this entry

`motor_model.py` gained `R_ESR = 0.012` and now solves `R I^2 - Vc I + P = 0` for the current the
load draws at the bank **terminal** rather than at the capacitor, integrating `Vc*I` out of the
bank and `I^2 R` into a new `Q_esr` output. `sizing.py` follows: `E_DRAWN` 2795.6 to 2881.2 J,
`SAG_FRAC` 5.19 to 5.35 %, `energy_closure()` carries the term on both sides, and
`thermal_campaign()`'s literal 160 J becomes the computed 85.6 J.

Eleven result fields moved, all electrical or thermal. **Exit velocity, acceleration, stroke time,
dispersion, the payload family, mass and cost are unchanged**, which is the expected signature of
an electrical-only correction and was checked rather than assumed.

The correction also closed a disagreement nobody had attributed. A8 and A8-R both recorded peak
current about 5 % above the analytic model and put it down to the integrator. It was the ESR:
corrected, the model gives 346.77 A against ngspice's 346.8.

**This is a simulation result, not a measurement.** It gives a placeholder its first independent
number, which is what E17 asked for, and it is still one model checking another.

> **Superseded in part, 2026-07-30 by A10.** Everything above is arithmetically correct and
> still describes what the model does. What it assumed is not: **12 mohm is not purchasable at
> this bank capacitance**, and at a realistic value the shot does not close at all. The 86 J
> figure is therefore the ESR loss of a bank nobody can build. See **P26**.

### P25. A retracted claim stayed live in the paper, the wiki and two docs for a day: MEDIUM, NEW 2026-07-30
P22 withdrew ADR-003's assertion that coilgun efficiency is "1-2 % in the literature", after
Feng et al. were found reporting **14.9-19.9 %** for a multi-stage on-orbit CubeSat launcher.
The withdrawal was recorded in `docs/adr/003`, `docs/PRIOR_ART.md`, `docs/RELATED_WORK.md` and
the changelog.

**It was not propagated to the places that actually assert it.** Four survived:

| Where | What it said |
|---|---|
| `paper/paper.tex` Table I | *Electrical to payload efficiency: coilgun 1-2 %, this work 19 %* |
| `paper/paper.tex` §II and §III | the same figure, once as background and once as a listed cost of the coilgun |
| `wiki/Home.md` | "1-2 % single-stage efficiency" in the locked-decisions list |
| `docs/PROJECT_NOTES.md` | the same, in the locked-decisions list |

**Table I is the one that matters.** It is the architecture trade, and that row claimed an
order-of-magnitude efficiency advantage that the prior art says does not exist. Corrected, the
row reads 14.9-19.9 % against 19 %, which discriminates not at all. The decision survives on the
rows that always carried it: no armature on the customer satellite, closed-loop velocity control,
and an abort path to 45 % of stroke.

**Found by reading the wiki page after publishing it**, not by any check. That is the finding.
The retraction was logged in four places and propagated to none, and nothing in the repository
notices when a ledger entry and an artifact disagree, because the mechanical guards
(`make_baseline.py --check`, `_check_operating_point()`, `check_links.py`) all compare artifacts
to *scripts*. A claim withdrawn in prose has no such guard.

**Half the general case is now fixed**, 2026-07-30. The same blindness had already shipped a
stale PDF: `paper.tex` was corrected twice and the published PDF went on printing the retracted
figure for five hours until it was found by hand.
[`tools/check_artifacts.py`](tools/check_artifacts.py) closes that half by comparing each built
artifact to the sources it was built from, using the commit each was last changed in rather than
file mtimes, which git does not preserve and which a fresh clone destroys. Verified against the
actual failure: at commit `c406da4` it reports the PDF **5.1 hours behind** its own source.

**The other half stays open and is the harder one.** A claim withdrawn in prose still has no
guard. Catching that needs a list of load-bearing claims and where each is asserted, which is
`docs/PROVENANCE.md`'s job and would roughly double it. What is now true is that the *mechanical*
half of this defect cannot recur silently.

### P26. The supercapacitor bank cannot source the shot: HIGH, NEW 2026-07-30
P24 recorded that the 12 mohm bank ESR had no source. Looking for one found that the value is
not merely unsourced, it is **not attainable from the cells the design specifies**, and that the
shot does not close without it. Full run: [`validation/A10_bank_esr.md`](validation/A10_bank_esr.md).

**The physics.** For an EDLC, ESR times capacitance is roughly constant within a cell
technology: both are set by the same electrode area and separator. Two Eaton 3.0 V cells thirty
times apart bracket it, and series stacking preserves the product because R scales with N and C
with 1/N.

| Cell | C | ESR | ESR x C |
|---|---|---|---|
| TV1860-3R0107-R | 100 F | 11 mohm | 1.10 s |
| XL60-3R0308T-R | 3000 F | 0.23 mohm | 0.69 s |
| **This bank, as modelled** | **5.94 F** | **12 mohm** | **0.071 s** |

The bank as modelled is an order of magnitude better than either commercial cell. At a realistic
product it is **116 to 185 mohm**.

**The consequence is not a worse efficiency. It is no shot at all.** A source of EMF V behind
series resistance R cannot deliver more than `V^2/4R` into any load. At the rated point the
shot needs 30.0 kW at peak velocity. A10 swept the integrator and found the design completes up
to **65 mohm and fails from 70**, against the 116 to 185 mohm the cells actually give.

| | |
|---|---|
| Hard ceiling on bank ESR | **65 mohm** |
| A single string of 32 x 190 F cells | **116 to 185 mohm** |
| Margin | **none: short by 1.8x to 2.8x** |

**Nothing else in the design is implicated.** Exit velocity, stroke time and dispersion do not
move anywhere in the sweep, because the commanded force is constant and the mechanical
integration never sees the bank until the bank fails to source it. K_t, the magnets, the
winding and the control loop are untouched. This is a pulse-power defect and it is contained
there.

**Not propagated, and that is deliberate.** The baseline still reads 16.537 m/s at 2.88 kJ,
which assumes a 12 mohm bank that cannot be bought. `docs/BASELINE.md`'s change-control rule
admits error correction; what is needed here is a **sizing decision**, and taking one on the
strength of two datasheet points would be exactly the reasoning this repository logs defects
about. Options costed as **PII-7**.

**The gap that let this through, and it is on the record already.**
[`docs/LITERATURE.md`](docs/LITERATURE.md) has 136 entries across nine clusters, and its
pulsed-power-and-capacitors cluster has **two**. The file names that cluster as the sample's
blind spot in its own words. The one area nobody filled is the one that turned out to carry a
defect big enough to stop the machine.

**What is still soft.** Both cell figures come from distributor listings of manufacturer data,
not from the manufacturer PDFs, which are unreachable from the environment this was written in.
A third mid-range point was not obtained. If space-qualified cells behave differently the
numbers move, though the ceiling at 65 mohm does not: that is set by this design's own power
demand and is independent of any datasheet.

### P27. A numerical guard hid the failure it was written next to: MEDIUM, NEW 2026-07-30
Found by A10 on its first run, before it found anything about the bank.

`shot()` solves `R I^2 - Vc I + P = 0` for the current drawn at the bank terminal. When the
discriminant went negative it fell back to `I = P/Vc`, the current the load would draw with no
ESR at all. That branch was added on 2026-07-30 in the same commit as the ESR term itself,
as an ordinary numerical guard.

**A negative discriminant is not a numerical edge case. It is the bank being unable to source
the demanded power**, which is precisely the condition A10 exists to detect. The fallback
converted it into a completed run with a working machine in it, at every resistance tested.

The tell was visible in the output and nearly missed: **peak current fell from 630 A at 70 mohm
to 331 A at 183 mohm.** Demanded power was fixed, so current cannot fall as resistance rises.

**Fixed:** the branch raises `BankLimitError`, naming the power demanded, the `V^2/4R` ceiling,
and the point in the stroke where it was hit. The baseline is unaffected, because at 12 mohm the
discriminant never goes negative.

**The general lesson, which is why this is a numbered defect and not a commit message.** Every
other guard in this repository fails loudly: `_check_operating_point()` exits, `make_baseline.py
--check` exits, `bench_predict.py` raises on geometry drift. This one substituted a plausible
value and continued. A guard that degrades silently is worse than no guard, because it converts
a detectable failure into a credible wrong answer.

### P28. The regen stator and the eddy fin do not both fit the arrest section: MEDIUM, NEW 2026-07-31
Opened by A11 in the act of adopting regenerative braking, and recorded rather than designed
around.

The closed envelope is 1839 mm and release is at 1500 mm, so the arrest section is **339 mm**.
A11 assumes 240 mm of it carries regenerative stator. The eddy fin as sized in `sizing.py` is
**300 mm** long (0.86 kg of 4 mm copper). **240 + 300 > 339.** Both live in the same airgap, so
they cannot overlap.

**The thermal half is not the problem.** Regeneration cuts the fin's duty from 1291 to 952 J, a
26 % reduction, and the fin's adiabatic rise falls from 4.0 to 3.0 K. A fin a third of the
length would still hold its transient.

**The mechanical half is unresolved, and it is tighter than it looks.** Eddy force is
proportional to velocity, so distance to arrest is linear in the velocity removed:
`x = (m/c)*(v0 - v1)`. At the first-order coefficient `paper/make_figures.py` uses,
`c = 670 N*s/m`, the sled needs **186 mm** to fall from 14.2 to 1.0 m/s, and only about 99 mm
would remain. Closing that means **c rising to roughly 1210 N*s/m, a factor of 1.8**, which puts
peak deceleration at **186 g against the 200 g taper cap** — inside it, with 7 % to spare, on a
cap that exists to protect the bonded magnet interfaces. That is not a comfortable margin, and
it is the reason this is a numbered defect and not a note.

**Regeneration is what makes the repartition even arguable.** Without it the sled enters the
brake at 16.5 m/s and the same 99 mm would need `c = 1440`, putting peak deceleration past the
cap outright. The 240 mm of regenerative stator pays part of its own packaging cost.

**Why this is logged instead of fixed.** The obvious fix is to shorten `fin_mass` in
`thermal_campaign()` until the numbers fit. `validation/README.md`'s conventions forbid exactly
that: *"do not hand-edit a script to match an FEA result, record the discrepancy first, decide
second."* The same applies to hand-editing one to match a packaging wish. `sizing.py` keeps the
300 mm fin and carries a comment saying it does not fit.

**What would close it.** A repartitioned arrest-section layout with the fin resized on eddy
authority rather than on heat, checked against the 200 g deceleration cap and the ring-spring
handover below 1.5 m/s. It is mechanical design, and it is the reason A11 says plainly that it
answers the electromagnetic question only.

### P29. The paper says the winding is segmented; the model charges copper for all 1.3 m: MEDIUM, NEW 2026-07-31
Found while pricing a longer track, and it is a question about the machine as built rather than
about any proposal.

`paper/paper.tex` §VII states, under redundancy: *"the winding is segmented so a shorted coil
degrades thrust rather than ending the campaign."* `motor_model.shot()` computes copper loss as
`RHO_CU * J^2 * vol_cu` with `vol_cu = ACCEL_ZONE * DEPTH * WIND_THICK * FILL`, that is, **the
whole 1.30 m winding carrying full current density for the entire 157 ms stroke**.

Those are not consistent with each other. A segmented long-stator machine energises the section
under the mover — roughly the sled's 340 mm active length — and switches segments as it passes.

**What it is worth.** Energising 340 mm rather than 1300 mm takes copper loss from **827.9 J to
about 217 J**, and electrical-to-payload efficiency from 21.2 % to roughly **24.4 %**, with no
design change whatsoever. It also drops peak current from 347 to about 296 A, which raises the
A10 bank ESR ceiling from 66 to about 79 mohm — relevant to P26, though not enough to reach a
single commercial string at 116.

**Three possibilities and this repository cannot currently distinguish them.**

1. The winding is segmented for *fault tolerance* but driven as one, in which case the model is
   right and the paper's sentence is about failure modes only. Then nothing is wrong and the
   distinction needs stating, because a reader will assume block commutation.
2. The winding is block-commutated and the model is deliberately conservative. Then the
   conservatism is real engineering judgement and **it is written down nowhere**, which is the
   same defect class as the 12 mohm ESR (E17): a value with no provenance.
3. It is simply inconsistent, and `Q_copper` is overstated by a factor of about 3.8.

**Why this is logged rather than fixed.** Changing `vol_cu` moves a baseline number, and which
way it should move depends on a design decision nobody has recorded. Guessing in either direction
would put an unsourced value into the baseline, which is exactly what P24 and E17 exist to stop.
`cad/parameters.json` `groups.stator` records conductor counts and belt geometry but says nothing
about drive segmentation, so the CAD cannot settle it either.

**What would close it.** A recorded decision on how many stator segments exist and how many are
energised at once, then `motor_model.py` computing `vol_cu` from that rather than from
`ACCEL_ZONE`, with the paper's redundancy sentence and the drive description made to agree.
Both numbers then follow from one stated fact instead of two unstated ones.

### P30. An acceptance band was set at the easier of two available comparators: MEDIUM, NEW 2026-07-31
**A defect in how a band was chosen, not in a number.** This repository has no other entry of that
kind, which is the reason to write it down.

`validation/A7_separation_chrono.md` declared its tip-off band as **≤ 5 °/s/axis**, citing the
NanoRacks NRCSD-E interface document. Three other files — E7 above, `docs/KILL_CRITERIA.md` §4 and
PII-1's entry criterion in `docs/PHASE_II.md` — carried a standing flag that this "conflicts" with
a sibling NRCSD ICD quoting 2 °/s, and that the conflict had to be resolved before the band meant
anything. PII-1, the best available velocity lever, was gated on it.

**There is no conflict. They are two different deployers and both numbers are right:**

| | Tip-off target | |
|---|---|---|
| **NRCSD**, internal, ISS airlock | **< 2 °/s/axis** | flown hundreds of times |
| **NRCSD-E**, external, Cygnus-mounted | < 5 °/s/axis | *"additional testing and analysis are being completed... to refine and verify this value"* — its own publisher |

**What that leaves is worse than the flag it replaces.** The band was set at the looser of the two
comparators, taken from the document whose publisher describes the figure as provisional, with
nothing recorded about the tighter flown number existing. Nobody chose the easy number on purpose;
it is what happens when a band cites one source and no one asks what else the source set contains.
**That is the failure mode acceptance bands exist to prevent, occurring inside the band-setting
step itself.**

**Fixed 2026-07-31.** A7's band is now **2 °/s/axis** with NRCSD-E retained as a secondary
reference and labelled provisional. **A7 has never run**, so this is a band tightened before
results rather than after — the distinction the whole validation record depends on, and the sheet
states it above the table. The cost is real: A7 is now **2.5x harder to pass**, on a release path
with no multibody model behind it and a payload centre of mass 70 mm off the thrust line.

**The general rule this implies**, added to `validation/README.md`: *when a band cites an external
document, record which document, which revision, and whether a tighter comparator exists in the
same family.* One line, and it would have caught this.

### P31. The repository carries two different inter-shot cadences and reconciles neither: MEDIUM, NEW 2026-07-31
Found while costing A13's failure, and it decides whether that failure matters.

| Where | Interval | For what |
|---|---|---|
| `paper/paper.tex` §III-C | **10–20 s** | described as "set by supercapacitor recharge, at a 150–300 W allocation" |
| `analysis/astro.py` `conjunction(spacing_s=1200.0)` | **1200 s** | the spacing the 30-day conjunction analysis actually models |

**Twenty seconds and twenty minutes, in the same repository, for the same event.** They are not
necessarily contradictory — a machine able to fire every 18 s may still be *operated* every
20 minutes — but **nothing anywhere states which is the ConOps**, and two published analyses
depend on different ones. The conjunction geometry, the realignment period and the whole safety
case are computed at 1200 s. The thermal case is argued at 10–20 s.

**The recharge claim is also wrong, which A13 established separately.** The mechanical chain
between shots — index, sled return, attitude settling — has a floor of **18.1 s** at a 6.9 s
return, against a recharge of 8.6 s at 300 W and 17.2 s at 150 W. **Attitude settling binds at
both allocations.** The paper's sentence has been corrected; this entry is about the second
number, which the correction does not touch.

**Why it matters for A13.** At 1200 s the 8.2 s settling is 0.7 % of the interval and A13's band 5
tested against the wrong quantity. At the 18.1 s floor it is 45 % of it. **The same failure is
either irrelevant or dominant depending on a number nobody has written down.**

**What would close it:** state the ConOps cadence once, in one place, with the reason — and make
`astro.py`'s `spacing_s` default read from it rather than carry an independent literal. If the
answer is 1200 s, A13's bands 3–5 should be re-declared against it and re-run; **that is a band
change and belongs declared and dated, not quietly applied to an existing failure.**

> **Not all of these weigh the same.** Three of the entries below are threats to whether the
> machine has a reason to exist rather than engineering work, and they are hard to see in a
> numbered list. [`docs/KILL_CRITERIA.md`](docs/KILL_CRITERIA.md) separates them, with the value
> at which each becomes fatal.

## E: Unsolved engineering

### E1. Three-dimensional field closure: 2-D HALF CLOSED 2026-07-29 by A1
> **A1 has run.** A meshed 2-D magnetostatic FEM (scikit-fem P1, 141 k elements, gmsh) gives
> **K_t = 11.228 N per kA/m against the model's 11.22 (a ratio of 1.0007**) with force
> ripple 1.25 % against 1.26 %. Midgap peak and winding mean both land at ratio 1.001.
> **The thrust band, the one that matters, is met.**
>
> What remains open is the 3-D half: end effects on a 340 mm array of finite 90 mm depth.
> P21 is that limitation showing up directly, the 2-D model overestimates far field because
> it has infinite depth. That needs A2.
`motor_model.py` resolves the winding in 2-D. End effects of a few percent on Kt remain
uncomputed. This is the declared close-out task for the electromagnetic model. The
magnetostatic package now exists, `analysis/femm/emocd_cross_section.dxf` plus
`analysis/femm/FEMM_RUN_SHEET.md` (analysis A1), which supersedes the older
`docs/FEMM_Run_Sheet.md`; the acceptance band in that older sheet predates the
winding-resolved model and should not be used. **Nothing has been run.** A1 closes the
2-D half; the 3-D end effects still need a 3-D solver (Elmer or GetDP are the free
options). Acceptance band declared in `validation/A1_field_femm.md`.

### E2. No FEA confirmation of anything: PARTIALLY CLOSED
> **Two FEA results now exist.** A4 (CalculiX, structural) ran 2026-07-28. **A1 (magnetostatic)
> ran 2026-07-29** and is the one that matters most: K_t had only ever been checked
> analytic-against-analytic, a closed-form wave model against magpylib, both superposing
> analytic solutions for uniform blocks, neither solving a field equation. A1 solves the PDE on
> a mesh and agrees to 0.07 %.
>
> Still open: no FEA of the track, the brake, or the cassette structure; and no 3-D
> electromagnetic solve (E1).
The field cross-check is analytic-vs-analytic (both magpylib and the wave model assume
ironless geometry, where superposition is exact). That is a genuine check of the wave
model but is NOT independent confirmation from a different physical method. Two analyses
are specified and neither has been executed: **A1** magnetostatic (E1 above) and **A4**
sled-chassis structural, which is what P5 and P8 are waiting on. Both, plus A5, A8, are
written up with pre-declared acceptance bands in `validation/`, and A5's GMAT toolkit is
built (`validation/gmat/`) though not yet run. A8 (pulse-power, E17) is
the cheapest of them and needs no CAD, no mesh, and no licence.

### E3. Masses are parametric and unchecked against vendor data
CAD now exists (`cad/`, nine documents), so the "no CAD" half of this item is closed,
but the mass problem is not. `mass_properties.py` still uses primitive solids with
shell/fill factors, and no component mass is checked against a vendor datasheet;
estimate spread perhaps ±15 %. Fusion-computed masses are **not** a substitute: they use
solid-copper stator, solid-aluminium CubeSats, and steel standing in for NdFeB, which is
why they are deliberately excluded from `cad/parameters.json`. The sled mass (4.86 kg)
propagates directly into the headline velocity (see P5 and P8) and the enclosure,
radiator, and avionics are still missing from the rollup entirely (P10).

### E4. No hardware at any level
> **A protocol now exists, 2026-07-29.** `docs/BENCHTOP_TESTS.md` specifies four sub-scale
> experiments, cheapest first, each closing a named claim with its acceptance band declared
> in advance: a Halbach pair on a gaussmeter (B-1), single-coil thrust against
> K<sub>t</sub> (B-2), capacitor discharge against the pulse model (B-3), and a drop-test
> brake coupon against the plate-drag law (B-4). **B-1 costs roughly the price of two magnets
> and would give this project its first measured number.** Full-scale qualification is
> specified separately in `docs/QUALIFICATION_PLAN.md`. None of it is run, this item stays
> open until something is measured.
>
> **Strengthened 2026-07-30, and the reason is competitive.** The Harbin group
> (`docs/PRIOR_ART.md`) has **built and measured a prototype**; this project has not, and that
> difference is visible to any reviewer. B-1 and B-2's bands were declared before any test but
> *chosen* rather than derived. `validation/bench/bench_predict.py` now derives them, importing
> `verify_field.py` and `motor_model.py` with a guard against geometry drift. Measurement error
> comes out at **4.4 % for B-1's field rows and 13.5 % for B-2's thrust**, against bands of ±15 %
> and ±20 %. The bands do not move, they must also cover model error, which is the thing under
> test, but a failure is now interpretable, because the rig can no longer be blamed for it.
> Two procedural traps were found in the process and are documented in `BENCHTOP_TESTS.md`: a
> two-block bench pair built poles-facing reads **exactly zero field**, and B-2's load cell must
> be sized to the smallest force in the sweep rather than the largest.
TRL 2-3. Nothing has been built, fired, or measured. The velocity, dispersion, and
tip-off claims are all model outputs.

### E5. Host stage properties unavailable
Recoil budgets are parametric across 300-900 kg host classes because no candidate
stage publishes its mass and control authority. Cannot be closed from public data.

### E6. Absolute orbital lifetimes are uncertain
Static exponential atmosphere at mean solar activity. Absolute lifetimes swing
severalfold across the solar cycle. The x1.80 ratio was believed invariant and defensible;
**P16 has since falsified the invariance**: GMAT gives 1.73 / 1.78 / 2.07 across low to high
activity. The point value at mean and high activity survives; the invariance does not. `validation/A5_astro_orekit.md` specifies an independent
re-run under GMAT (toolkit built in `validation/gmat/`, Orekit an equally valid
substitute) (different codebases, independently implemented force models) with the band on the ratio and explicitly not on the absolutes. It now also
carries a second leg: reproduce the **measured** decay of 3-5 non-manoeuvring 3U CubeSats
from CelesTrak / Space-Track TLE histories, band 15 % on time-to-decay. Two models
agreeing is weaker than a model reproducing a flown decay, and the flight data is free.

### E7. Velocity dispersion rests on assumed sensor noise
The 0.027 m/s (3σ) result is a closed-loop simulation using an assumed 8 mm/s sensor
sigma and assumed tolerance distributions. No sensor has been selected or characterised.
The separation side of this is specified in `validation/A7_separation_chrono.md`, whose
tip-off band is taken from a flown deployer rather than chosen. **Tightened 2026-07-31 from
5 to 2 °/s/axis**: the band cited NRCSD-E, the external Cygnus deployer, whose 5 °/s its own
publisher calls provisional, while the internal NRCSD that has flown hundreds of times specifies
**< 2 °/s/axis**. Two deployers, not a contradiction, and the band had been set at the easier of
them. See **P30**.

### E8. Brake energy is thrown away
~1.0 kJ per shot dissipated in the fin. Whether any of it is worth recovering (and what
that would cost in mass and complexity) has not been examined since the efficiency
correction.

### E9. 6U/12U variants are force-limited, not designed
The payload family table is arithmetic from the same thrust constant. No mechanism,
cassette, or structural design exists for larger classes.

### E10. Launch restraint is drawn but not analysed
Retention gate pin sizing exists (two D6 A-286, margin 1.2) and the breech launch-lock
blocks are now modelled in CAD (`cad/parameters.json` `track`: `launch_lock`, x = 30-50
mm, 2 off). The rest, escapement caging, cam lock, tolerance stack-up under vibration,
is drawn or described, not analysed.

### E11. No contamination or outgassing analysis
> **ADR-004 gains external support 2026-07-29:** coreless construction lowers outgassing and
> vacuum-rated ironless linear motors are catalogue products, so this architecture converges
> with fielded vacuum practice. Does not close the item, T-4 tests *this* material set.
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

### E14. Patent / disclosure: the disclosure has now happened
Concept and results are public (LinkedIn, and this repository, which is now a **public**
repo carrying the scripts and therefore the operating point). No provisional application
was filed first, so this is done and cannot be undone. What remains is not a decision but
a consequence to be handled: any patent route now runs on whatever post-disclosure grace
period applies in each jurisdiction, India and the US have one, most of Europe does not
counted from the earliest public disclosure, not from today. **If a filing is still
wanted, establish that earliest date and take advice quickly.** If it is not, close this
item out explicitly so it stops reading as pending.

### E15. Sponsorship not secured
The build is the declared next step and is unfunded.

### E16. Reference hygiene
Three references in `paper/paper.tex` were flagged verify-before-submission and have
not been fully verified: eddy-damper heritage [15], Yudintsev separation dynamics [17],
and the vibro-impact deployment paper [18]. `docs/RELATED_WORK.md` adds a further list of
comparator sources and tooling, **none of it retrieved and read either**, and it carries
the same rule: fetch before citing. The differential-drag comparator (Foster et al. flown
Planet Labs results) is the one worth chasing first, since the paper's 25-day baseline is
currently a model output rather than a measurement.

### E17. The pulse-power chain: PARTIALLY CLOSED 2026-07-28 by A8, with two findings
**A8 has been run** (ngspice 42, `validation/spice/emocd_shot.cir`). All five declared bands
were met, exit velocity and pulse duration agree to 0.03 % across two different integrators,
peak current +5.98 %, sag +0.18 points, energy +3.59 %. Two findings came out of it anyway:

1. **Quoted sag is state-of-charge, not terminal voltage.** `motor_model.py` models no ESR
   at all; it reports the capacitor's charge depletion, 4.88 %. With a 12 mohm ESR the
   terminal droops to 86.16 V, a **10.25 % total sag**. The servo-headroom argument behind
   the 0.027 m/s dispersion claim is stated against the smaller number.
2. **The `Q_esr = 160 J` default does not reconcile with 12 mohm.** Integral of I^2 dt over
   the shot is 8008 A^2 s, giving 96 J at 12 mohm. The two agree only at about 20 mohm. This
   item asked for a second number against the 160 J; here it is.

The 12 mohm itself appears only in `docs/EMOCD_Computation_Results_C1-C10.md`, which is
superseded. **Datasheets have since been checked against it and it does not survive**: a bank of
this capacitance built from commercial cells is 116 to 185 mohm, and the shot does not close
above 65. See **P26**. This item is no longer about provenance; the number was not merely
unsourced, it was unattainable.

> **Re-run 2026-07-30 (A8-R), then corrected.** Five of six bands met; the pulse-duration row
> that P23 is about passes at 0.03 %. Energy closure failed at 97.0 %, and the cause was the
> gap this item names: 7126.2 A^2 s at 12 mohm is **85.5 J of ESR dissipation per shot** the
> analytic ledger had no term for. That is the second number against `Q_esr = 160 J` this item
> asked for, and it is 1.9x lower.
>
> **`motor_model.py` now carries `R_ESR` and solves for the current at the bank terminal**
> rather than at the capacitor, so the loss is integrated rather than assumed. P24 records the
> propagation. Two things fell out that are worth more than the correction itself:
>
> - **The 5.98 % peak-current deviation this item recorded was the ESR, not the integrator.**
>   Corrected, the analytic model gives 346.77 A against ngspice's 346.8, agreeing to 0.01 %
>   where it previously disagreed by 5 %. Two independent methods now agree on the number that
>   sets the device rating.
> - **The energy budget closed at 100.0 % while missing a real 86 J term**, because the draw it
>   balanced against came from the same model that omitted the loss. Closure tests arithmetic
>   consistency, not physical completeness, and this file had been quoting it as if it tested
>   both.
>
> The sag finding above stands and is unaffected: the quoted figure is still charge depletion,
> and the terminal dip is still additional.

Original item follows.

### E17 (as originally written). The pulse-power chain has never left the analytic model
The supercapacitor bank, the SiC bridge, and the winding exist only as lumped resistances
and ideal switching inside `motor_model.py` and `sizing.py`. Three numbers depend on that
model and nothing else: the **392 A peak current** (which sets the device rating and the
paper's derating discussion), the **4.9 % bank sag** (which underwrites the servo headroom
behind the 0.027 m/s dispersion claim), and the **672 J copper loss** (which carries the
32 % efficiency figure). No transient overshoot at commutation has been computed, and the
`Q_esr = 160 J` default in `sizing.py`, flagged as unsourced during the P2 review before
being traced to the script's own default, has no second number against it.

Specified as **A8** in `validation/A8_pulse_spice.md` (ngspice or PySpice, both free).
This is the least expensive analysis in the plan: no geometry, no mesh, no licence, and it
attacks three headline-adjacent numbers at once.

### E18. Conjunction covariance is invented: NEW 2026-07-27
Any probability-of-collision result (A6) inherits whatever covariance it is given, and no
covariance exists for a satellite that has never flown. Space-Track **Conjunction Data
Messages** carry real post-deployment covariances for comparable objects and are the
defensible source; `validation/A6_conjunction_cara.md` now names them as the preferred
input, with an explicitly documented assumption as the fallback. Until that is done, no Pc
figure from this project should be quoted as anything but conditional on its assumption.

### E19. Eddy-current heating inside the magnet blocks is not modelled: NEW 2026-07-29
> **Cross-industry review 2026-07-29** (`docs/CROSS_INDUSTRY.md`): this is a named, well-studied
> loss mechanism in PM machines, and **magnet segmentation is the standard mitigation, which
> reduces thrust and mechanical robustness.** That is a design option this project did not
> previously have. Item stays open: the literature is steady-state rotating machines, and
> nobody has computed the 157 ms pulsed case here.
`sizing.py::magnet_temperature()` models exactly one thermal effect on the magnets:
reversible remanence drift with ambient temperature, `alpha = -0.11 %/K`. NdFeB is a
conductor (roughly 1.4-1.6 uOhm*m, some 80-90x copper's resistivity but far from an
insulator), and the blocks sweep past the winding at up to 20 m/s through the field's
spatial harmonics, the belt winding's own 6th-harmonic ripple, slot-like content, and
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

### E20. The brake's force-time profile does not exist: NEW 2026-07-29
`sizing.py` asserts a 200 g deceleration **cap**, used to size the magnet bond. No script
anywhere simulates the arrest: there is no force against velocity, no force against
position, no peak, and no duration. `legacy/c3_c4_em.py` sizes the brake by energy, not by
transient.

A first-order estimate from the sled's own kinetic energy across the 210 mm arrest zone
puts the **average** force near 6 kN over roughly 8-20 ms, some 4x the 1413 N
acceleration force, over a tenth of the duration, and with a peak that nothing bounds. The
host therefore sees two oppositely-signed impulses of very different shape per shot, not
one smooth push, and a 12-shot campaign is 24 load reversals through the ESPA bolted
interface.

E5 covers the *magnitude* of the recoil budget across host mass classes. Nothing covers its
*shape*, and A4 is a static analysis that cannot. This is a fatigue and control-bandwidth
question, and it is the natural companion to A7.

### E21. No vacuum tribology anywhere: SUBSTANTIALLY RETIRED BY CITATION 2026-07-29
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

### E22. Parasitic eddy drag on the track structure is not in the thrust model: REFRAMED 2026-07-29
> **Reframed as a design rule rather than an analysis** (`docs/CROSS_INDUSTRY.md`): vendor
> ironless motors keep conductive structure out of the magnet track's field. Specify a minimum
> standoff and check the CAD against it, cheaper than the computation this item implied.
The eddy brake works because a moving Halbach field drags on a nearby stationary conductor.
That is also the geometry of the entire 1.3 m acceleration zone wherever aluminium or
titanium structure (longerons, guide rails, enclosure skins) sits within reach of the
field. `verify_field.py` puts the stray field at 22.7 mT at 10 mm behind the array and
4.3 mT at 20 mm, which is not negligible at plausible standoffs.

`motor_model.thrust_constant()` computes Kt purely as the Lorentz force against winding
current. It carries no term for eddy coupling into any other conductor. So the model
accounts for eddy drag exactly where it is wanted (the brake) and nowhere it might be
unwanted, and the sign is unfavourable: any such drag subtracts from delivered thrust and
adds heat to the track.

Not quantified here, it depends on the track-to-array standoff and the conductivity of
whatever is actually there, and the standoff is not a single number in `cad/parameters.json`.
The check is cheap once that geometry is pinned, and it belongs with A1.

### E23. Force-ripple harmonics sweep the track's own structural modes every shot: NEW 2026-07-29
> **The cogging half retires; the sweep half does not.** Ironless construction has zero cogging
> by design, so the largest ripple source in an iron-core machine is absent. But E23 is about
> the *electrical* ripple chirping through the modes, and industrial stages run at constant
> velocity and do not chirp. **No citation found addresses this**: it appears genuinely
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

So both modes are crossed inside the first 4-50 ms of a 158.6 ms stroke, twelve times per
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

### E24. Attitude disturbance from magazine indexing is not modelled: NEW 2026-07-30
Found by reading a competitor's problem statement rather than by examining this design, which is
worth stating plainly: Xu et al. (*Aerospace* 11(5) 394, 2024) build a **cost model for attitude
disturbance caused by moving CubeSats around inside the deployer**, and optimise their transfer
paths against it, because a shifting centre of mass degrades platform pointing and therefore release
accuracy.

**This project models the recoil of the shot and nothing about the indexing between shots.**
`analysis/sizing.py` gives 66.1 N·s per ejection and the host nulls it with cold gas. But twelve
satellites feed from two transverse cassettes, so between every pair of shots a mass of order a few
kilograms translates across the structure, and:

- the centre of mass moves, so the host's attitude reference sees a disturbance torque that is
  **not** the shot recoil and is not in any budget here;
- the sled returns to the breech, a second mass motion, also unmodelled;
- the dispersion claim (0.027 m/s 3σ) assumes the track is where the model says it is at trigger
  time. If indexing leaves residual attitude rate or structural motion that has not damped out, the
  release direction carries an error the velocity servo cannot see, because it measures position
  along the track and not the track's own orientation.

**Why it is probably small, and why that is not an answer.** The indexed mass is a few kg against a
124.9 kg loaded system on a host of hundreds to thousands of kg, and the campaign has time between
shots, nothing here suggests a feasibility problem. But P16 was also "probably fine" until an
independent propagator was pointed at it. The quantity that matters is **residual attitude rate at
trigger, and the settling time to reach it**, and neither number exists anywhere in this repository.

**What would close it:** a rigid-body momentum budget for one index cycle, then the settling time
against the campaign's inter-shot interval. Cheap (it is bookkeeping, not a new solver) and it
belongs with the recoil analysis in `sizing.py` rather than with the motor model. Explicitly *not*
claimed to be negligible until that is done.

> ## Done 2026-07-31 as A13. **Verdict FAIL, and this entry was worried about the wrong mass.**
>
> **Indexing is negligible**, exactly as the paragraph above guessed: 0.208 N·s, **0.31 % of the
> shot impulse**, 0.007 °/s at a 500 kg host.
>
> **The sled return is not, and it appears nowhere in this entry or anywhere else.** 9.445 kg
> travelling 1.5 m back to the breech is **4.723 N·s, 7.14 % of the shot, 23x the indexing
> momentum** — the largest unbudgeted term in the host interaction by a wide margin.
>
> | Band | Result | |
> |---|---|---|
> | peak rate below 0.05 °/s at a 500 kg host | **0.161 °/s** | **FAIL, 3.2x over** |
> | peak rate below 0.2 °/s at 200 kg | **0.740 °/s** | **FAIL, 3.7x over** |
> | settle to 0.01 °/s in under 2 s at 0.1 N·m | **8.2 s** | **FAIL, 4x over** |
>
> Four of seven bands; the three that failed are the three that mattered. **Nothing inside the
> 10–20 s cadence passes** — the bands are only met at a 30 s sled return, which does not fit.
>
> **The velocity servo cannot see this.** It measures position along the track, not the track's
> orientation, so residual attitude rate at trigger is a pointing error the 0.027 m/s dispersion
> figure neither includes nor can detect.
>
> **Why this entry missed it is worth keeping.** E24 came from reading Xu et al., whose deployer
> moves satellites and does not return a sled — so the competitor's problem was the indexing, and
> this design's problem is in a place their paper never had to look. **Reading someone else's
> problem statement finds their gaps, not yours.**
>
> Full working, the three fixes and what each costs: [`validation/A13_indexing_disturbance.md`](validation/A13_indexing_disturbance.md).

### E25. A13 now leaves attitude restoration and structural settling open: CORRECTED 2026-08-03

The corrected rigid-body budget does not leave a residual angular rate after an internal mass
starts and stops. It leaves a transient rate and an attitude offset. At the assumed 166 mm
lever arm, the 500 kg example reaches about 0.136 deg/s during sled return and finishes about
0.42 deg from its initial attitude. The 200 kg example reaches about 0.443 deg/s and 1.37 deg.

The declared transient-rate rows remain FAIL. The ideal residual-rate row passes, but that does
not establish structural settling. No controller, thruster geometry, wheel/RCS authority,
flexible-body mode, damping ratio, or firing schedule closes the attitude offset before the next
trigger. The previous 8.2 s rate-null and 18.1 s cadence floor are superseded. P31's 10--20 s
versus 1200 s cadence contradiction remains unresolved.

### E26. Brake-fin transient temperature across a campaign is not modelled: NEW 2026-08-03

The thermal calculation previously used a 300 x 80 x 4 mm copper fin. The Gen3 STEP and the
validation mass table specify 120 x 80 x 4 mm, 0.344 kg. Correcting that input raises the
adiabatic increment from about 3 K to about 7 K per shot and the twelve-shot no-cooling bound
to about 85 K.

The former statement that each transient decays before the next 10--20 s shot had no transient
conduction or radiation model behind it and is removed. A thermal network, contact conductance,
surface properties, and the resolved P31 cadence are required. The 0.32 m2 radiator number remains
an assumed 130 W steady rejection case, not a demonstrated campaign transient.
