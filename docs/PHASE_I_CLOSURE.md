# Closing Phase I: every open item, and what each one actually needs

**Written 2026-08-05.** `OPEN_PROBLEMS.md` carries 34 P-items and 27 E-items. This file says,
for each, what would close it and who or what has to do the closing — because a list of 61
entries with no disposition is a list nobody can act on.

**Phase I cannot end with an empty register, and pretending otherwise would be the dishonest
version of this document.** Some items close only against hardware that does not exist. One
cannot close in Phase I at all. The useful question is not "is it empty" but **"is every item
either closed, or open for a stated reason with a named next step"**.

---

## 0. The first finding: the register does not distinguish fixed from live

Fifteen entries are marked RESOLVED. Forty-four are not. **But eight of those forty-four contain
their own correction** — P16, P22, P25, P26, P30, P31 and others describe a defect that was found,
corrected and propagated, and then remain in the register as the historical record.

That is deliberate and right: this project publishes defects rather than deleting them, and a
corrected entry is evidence. **What is wrong is that nothing marks which is which**, so the
headline "34 numbered problems" counts live engineering debt and published history in one number.
A reader cannot tell a live threat from a closed one without reading all 61 entries.

**The first act of closing Phase I is therefore bookkeeping, not analysis:** give every entry an
explicit status line — `LIVE`, `CORRECTED, RETAINED AS RECORD`, or `CLOSED` — and derive the
counts from it. Nothing else in this file can be trusted until that is done, including the
dispositions below.

---

## 1. Disposition summary

| Disposition | Count | Meaning |
|---|---:|---|
| **A. Closable here, by analysis** | 13 | This environment has the tools. Bands first, then run |
| **B. Bookkeeping** | 9 | Closes by writing, not computing |
| **C. Needs a decision from the owner** | 7 | Analysis cannot resolve these; a choice must be made |
| **D. Needs hardware or an external party** | 9 | Measurement, a vendor quote, or a host data exchange |
| **E. Blocked** | 3 | Network policy or missing external data |
| **F. Cannot close in Phase I** | 1 | E4 |
| **Already resolved** | 15 | Marked RESOLVED |

Toolchain confirmed present in this environment: `getdp`, `ccx` (CalculiX), `ngspice`, `gmsh`,
`skfem`, `magpylib`, `scipy`, `pdflatex`. **GMAT is not installed.** That is a wider toolchain
than the repository's own notes assume, and it is why category A is as large as it is.

---

## 2. Category A — closable here, by analysis

Every one of these gets a run sheet with **bands declared and committed before the script exists**,
the discipline `validation/README.md` exists to enforce. Ordered by value.

| # | Item | Closes | Tool | Expected |
|---|---|---|---|---|
| A-1 | **Tip-off at release (A7)** | E7, KILL_CRITERIA §4 | numpy 6-DOF rigid body | Payload CoM sits 70 mm off the thrust line. Band is 2 °/s per P30. **Likely FAIL** |
| A-2 | **Gen4 finite-stator force** | **P32**, E27 | magpylib | Opens the Gen4 export gate. HIGH |
| A-3 | **Ripple vs track modes** | E23 | numpy | 6th harmonic sweeps 0→2048 Hz; track first mode is 109 Hz, so it **crosses** |
| A-4 | **A8 rerun at the corrected point** | A8's self-declared staleness | ngspice | Deck exists at `validation/spice/` |
| A-5 | **Brake force-time profile** | E20, feeds E26 | numpy | The brake has no force-time curve anywhere |
| A-6 | **Magnet eddy heating** | E19 | analytic + magpylib | |
| A-7 | **Brake-fin campaign transient** | E26 | thermal network | Currently only an adiabatic bound (85 K) |
| A-8 | **3-D field and end effects** | E1's remaining half, E2 | gmsh + getdp | Heaviest; a coarse end-effect check is an acceptable outcome |
| A-9 | **Far-field stray, properly** | **P3, P21**, and A14's band 5 | 3-D from A-8 | A14 showed the 2-D model's far field is edge-effect dominated |
| A-10 | **Launch restraint** | E10 | ccx | Needs loads defined first |
| A-11 | **Parasitic eddy drag on the track** | E22 | analytic | |
| A-12 | **The four absent physical effects** | P18 | mixed | Scope each, then close or convert to E-items |
| A-13 | **Payload magnetic environment** | **P34** | 3-D from A-8 | Blocked behind A-8/A-9: the extent of the 61 mT region needs a trustworthy far field |

## 3. Category B — bookkeeping

Closes by writing. No computation needed.

| Item | What it needs |
|---|---|
| **P19** | Every validation predating the current operating point — now largely false; A10, A11, A12, A13, A14 all post-date it. Re-audit and mark |
| **P20** | A1's array-surface reference is mis-specified in the run sheet. Fix the sheet |
| **P23** | Stroke time stale in six places. Sweep and correct |
| **P25** | A retracted claim stayed live for a day. Closed in substance; needs marking |
| **P27** | A numerical guard hid a failure. Fixed in `shot()`; needs marking |
| **P30** | Band chosen at the easier comparator. Corrected; retain as record |
| **P7** | Brake sits past the release point — Gen4's 22 mm gap resolves it geometrically. Record against P32 |
| **P14** | Gen3 CAD defects. Audit each against Gen4 and close or carry |
| **E16** | Three references flagged verify-before-submission. Verify them |

## 4. Category C — needs a decision from you

**Analysis cannot close these.** Each is a choice with consequences, and each is currently
blocking work downstream.

| Item | The decision | What it blocks |
|---|---|---|
| **P9** | Target host class. The envelope is 1839 mm against ESPA Grande's ~1270 mm, 44 % over | A kill-criterion item. PII-4 |
| **P28** | 240 mm of regen stator and a 300 mm fin do not both fit the 339 mm arrest section | The regen credit and the brake layout |
| **P29** | Is the stator segmented or not? The paper says yes; the model charges copper for all 1.3 m | Copper loss, efficiency, **and P33's inductance**, which scales with energised length |
| **P10** | Enclosure, radiator and packaged avionics are absent from the mass rollup | Kill criterion 1, which is already crossed at 3U |
| **P31** | Inter-shot cadence: 10–20 s or 1200 s | **Being closed now** as ADR-020 at 1200 s |
| **E9** | Are 6U/12U variants in scope? | Product definition |
| **E14/E15** | Patent posture and sponsorship | Programme, not engineering |

## 5. Category D — needs hardware or an external party

| Item | What closes it |
|---|---|
| **E3** | Vendor datasheets against the parametric masses. No hardware needed, only sourcing |
| **E5** | Host stage properties — a data exchange with a host provider. Paper §VII already names this as the single exchange that converts the analysis from parametric to specific |
| **E11** | T-4 thermal vacuum, ASTM E595 |
| **E12** | **T-6.** A14 scoped it; only measurement closes it |
| **P26** | Bank ESR — a purchasable bank, or PII-7's four parallel strings accepted on paper |
| **P34** | T-6 measures the payload field. A-13 bounds it first |
| **B-1…B-4** | Benchtop programme. B-1 is a Halbach pair on a gaussmeter and is the cheapest first measured number in the project |
| **T-1…T-8** | Qualification campaign |
| **E4** | See category F |

## 6. Category E — blocked

| Item | Why |
|---|---|
| **A9 / E6** | Decay against flown CubeSats. `celestrak.org:443` returns 403 at CONNECT under this environment's network policy — re-tested, not assumed. Space-Track needs an account. The candidate NORAD shortlist is already in the run sheet, so this is an afternoon on any unrestricted machine |
| **P16** | The invariance falsification stands; closing the remainder needs A9 |
| **E18** | Conjunction covariance is invented. Needs a real CDM, which needs an operator relationship |

## 7. Category F — cannot close in Phase I

**E4: nothing has been built or measured at any scale.** This is not a defect to be worked off;
it is the honest description of a TRL 2–3 design study, and it should be stated as a **standing
caveat** rather than carried as an open item that might one day be ticked. Every number in this
repository is a model output. Phase I ends with that still true.

---

## 8. Validations: stated versus run

| | Status |
|---|---|
| A1 field, A4 structural, A5 astro, A6 conjunction, A8 pulse, A10 ESR, A11 regen, A12 attraction, A13 attitude, **A14 EMI** | **RUN** — 10 of 12 |
| **A7** separation and tip-off | **specified, never run.** Runnable here as A-1 |
| **A9** decay against flown objects | **specified, blocked.** Not runnable here |
| A2, A3 | never specified. A1 closed only the 2-D half of E1 |
| **A15** POEM campaign | new; script generated here, **GMAT run is external** |

**Two failed** (A5 invariance, A13 attitude), **two partial** (A1 field, A14 EMI), **one returned
three void rows** (A6), **one found a published number 37 % high** (A12).

### Stated and never run, outside `validation/`

- **T-1 … T-8**, the entire qualification plan. Specified 2026-07-29, none run, all need hardware.
- **B-1 … B-4**, the benchtop programme. B-1 has a bill of materials and a purchase order and has
  not been ordered. **It is the cheapest path to the first measured number in this project.**
- **`docs/FEMM_Run_Sheet.md`** — superseded, retained, and correctly marked as unable to function
  as a test.

---

## 9. What Phase I closure actually looks like

1. **Mark every register entry** `LIVE` / `CORRECTED, RETAINED` / `CLOSED`, and derive the counts
   from that. Section 0. Nothing else is meaningful first.
2. **Run category A** — thirteen analyses, bands first, several expected to fail.
3. **Decide category C** — seven choices, all yours. P29 is the highest-leverage one because it
   moves copper loss, efficiency and inductance together.
4. **Convert category D into a plan with dates**, and order B-1.
5. **State categories E and F as permanent caveats**, not as debt.

**A realistic Phase I close leaves E4 open, categories D and E open with named owners, and
categories A, B and C closed.** That is a defensible end state. An empty register would not be.
