# 2D drawing brief for the AutoCAD assistant

Paste the block below into the AutoCAD assistant. Kept here so the drawing set is versioned
alongside the geometry it describes, and so a dimension change in
[`parameters.json`](parameters.json) has one obvious place to propagate to.

**Read this first.** `cad/parameters.json` is the single source of truth for VOLLEY geometry,
and it carries its own warning: Fusion user parameters are document-scoped and drift silently
across the nine documents. **Every dimension in every drawing must trace to a key in that file.**
If a dimension is needed that is not there, it does not exist yet and must be added there first.

Three parameter groups are marked provisional or open, and the drawings must not present them
as settled. They are called out per-sheet below.

---

## The prompt

```
Produce a 2D engineering drawing set for VOLLEY, a magazine-fed electromagnetic CubeSat
deployer. These are working engineering drawings for a public technical repository, read by
examiners and engineers. Clarity and correctness over presentation.

CONVENTIONS, APPLIED THROUGHOUT
  Projection: FIRST ANGLE. State it in the title block with the truncated-cone symbol.
  Units: millimetres. Do not annotate units on each dimension; state "ALL DIMENSIONS IN MM"
    once in the notes.
  Sheets: ISO A3 for detail parts, ISO A2 for assembly and interface sheets.
  Line weights: visible 0.5 mm, hidden 0.25 mm dashed, centre 0.25 mm chain, dimension and
    leader 0.18 mm, section cut 0.7 mm.
  Text: 3.5 mm for dimensions, 5 mm for view labels, 7 mm for the drawing title.
  Scales: state on every view. Prefer 1:5 for the full machine, 1:2 for sub-assemblies, 1:1
    for interface detail. Never leave a view unscaled or marked NTS.

COORDINATE FRAME, from cad/parameters.json
  x = firing axis, positive toward the muzzle, origin x=0 at the ESPA flange aft mating face
  y = lateral, +y port, -y starboard
  z = vertical, z=0 at the stator mid-plane
  Datum A = ESPA flange aft mating face (the x=0 plane)
  Datum B = stator mid-plane (z=0)
  Datum C = machine centreline (y=0)
  Every geometric tolerance references these three in this order.

TOLERANCING
  General tolerance note: linear +/-0.5 unless otherwise stated, angular +/-0.5 degrees.
  Apply ISO 1101 geometric tolerancing ONLY where a function demands it. The functional ones,
  and they are the point of the whole set:
    - Airgap-critical faces: the stator belt envelope and the Halbach array inner faces.
      Parallelism 0.05 to datum B. The airgap stack budget is 0.05 mm shim setting, and the
      as-built RSS is 0.101 mm (see docs/MANUFACTURING.md). Call out both.
    - Track longeron straightness over 1800 mm: 0.2. Track straightness and plate flatness
      dominate the airgap error budget; tightening the shim is nearly worthless by comparison.
    - ESPA flange face flatness 0.1 to datum A, bolt circle true position 0.2 MMC.
    - CubeSat corner-rail contact faces: flatness 0.1, per the CubeSat Design Specification
      rail interface.
  Surface finish: Ra 3.2 general machined, Ra 1.6 on airgap-critical and bearing faces.

THE SHEETS

SHEET 1 - GENERAL ARRANGEMENT (A2, 1:5)
  Three orthographic views plus an isometric. Envelope 1839 x 530 x 940 closed.
  Dimension only: overall envelope, ESPA flange position, acceleration zone end x=1300,
  release point x=1500, brake span x=1530 to 1740, track longeron length 1800.
  ADD THIS NOTE, it is a live open problem:
    "ENVELOPE LENGTH 1839 EXCEEDS ESPA GRANDE CLASS (~1270) BY ~44%. OPEN, SEE P9."

SHEET 2 - TRACK (A3, 1:5, detail 1:1)
  Two longerons, length 1800, z from -45 to +20, overall width 205.
  Roller channels: y 67 to 90, half-height 22. Guide rails: y 68 to 88, z contact 15, outer 22,
  two per side. Launch locks: x 30 to 50, y 68 to 78, half-height 14, two off.
  Detail view at 1:1 on the guide-rail cross-section, which is where the roller runs.
  NOTE: "ROLLER CHANNELS AND GUIDE FLANGES ARE FLAGGED INCOMPLETE IN THE SOURCE MODEL
  (G3-D2). DIMENSIONS SHOWN ARE THE INTENDED SECTION, NOT AS-MODELLED."

SHEET 3 - STATOR (A3, 1:5, detail 2:1)
  Ironless single-layer three-phase, 162 conductors, 54 per phase.
  Belt pitch 8.0, belt width 7.0, insulation gap 1.0, thickness in z 10.0, z from -5 to +5.
  Active width in y 90, pole pitch 24, wavelength 48, active span x 0 to 1296.
  Detail at 2:1 over one 48 mm wavelength showing the belt sequence A+ C- B+ A- C+ B-.
  Colour or hatch the three phases distinctly on the detail and key them in the notes.
  TWO NOTES, both required:
    "END TURNS NOT SHOWN. CORRECT FOR FIELD AND FORCE, WRONG FOR PACKAGING: REAL RACETRACK
     ENDS WRAP BEYOND THE 90 ACTIVE DEPTH AND ARE NOT IN THE ENVELOPE."
    "SINGLE VERSUS TWO-LAYER WINDING IS AN OPEN ELECTROMAGNETIC DECISION. SINGLE AS DRAWN."

SHEET 4 - SLED (A3, 1:2, detail 1:1)
  488 x 140 x 140. Halbach arrays x 230 to 570, length 340, width in y 90, z inner 6 outer 14,
  magnet thickness 8, airgap per side 1.0.
  Chassis plate 6.0, web 6.0, web y 48 to 54, backstop 8.0.
  Four rollers, diameter 30, width 16, base span 300, x offset from centre 125, y 70 to 86.
  Detail at 1:1 on the airgap stack: magnet face, airgap, stator belt, airgap, opposing magnet.
  This is the single most important detail in the set and everything downstream depends on it.
  TWO NOTES:
    "CHASSIS IS PROVISIONAL, STIFFNESS-DRIVEN, NO STRUCTURAL FEA AT THE TIME OF DRAWING
     (P5, P8). AS-DRAWN UNPOCKETED GEOMETRY."
    "HALBACH ARRAY X-POSITION INHERITED FROM A SHORTER CHASSIS AND NOT RE-CENTRED (P14).
     POSITION RELATIVE TO THE WINDING SETS THE THRUST CONSTANT."

SHEET 5 - MAGAZINE CASSETTE (A3, 1:5)
  One document, two instances. The second is a 180-degree ROTATION about z through x=210.25,
  NOT a mirror. Say so in the notes; it matters for the part count.
  380.5 x 166 x 690, six satellites per cassette, pitch in z 104.
  Drive bay 30, leadscrew at x=200, follower plate 6.0 with three ribs.
  Gate frame z 46 to 626, two A-286 pins diameter 6 at x=110 and 290.
  Septum 1.0 silicon steel, x 25 to 375, z 26 to 646.
  NOTE: "GATE PINS CARRY 5900 N ASCENT PRELOAD DIRECTLY INTO STRUCTURE, BYPASSING THE RELEASE
  MECHANISM. THIS IS DELIBERATE, SEE ADR-008."
  NOTE: "SHELL DRAWN AS CLOSED 4.0 PANELS. OPEN FRAME IS AN UNMADE DECISION WORTH ~4.8 KG."

SHEET 6 - ESPA INTERFACE (A2, 1:2, detail 1:1)  ** CONTROLLED INTERFACE **
  Flange OD 460, bolt circle 400, 24 holes diameter 9, flange thickness 25.
  Hub plate diameter 300, thickness 15. Four gussets, thickness 12, inner radius 50, outer 220.
  x from -25 to 0. Flange protrudes through the aft skin.
  Full geometric tolerancing: flatness 0.1 on the mating face to datum A, true position 0.2 MMC
  on the bolt circle, perpendicularity 0.1 of the hub axis to datum A.
  Bolt hole detail at 1:1 with edge distances.

SHEET 7 - PAYLOAD INTERFACE (A3, 1:1)  ** CONTROLLED INTERFACE **
  3U envelope 340.5 x 100 x 100, four corner rails 8.5 square, per the CubeSat Design
  Specification rail interface.
  Show the cradle contact faces and the retention gate engagement.
  Dimension the clearance envelope around the satellite through the full stroke.
  NOTE: "SATELLITE IS NEVER MODIFIED. NO ARMATURE, NO PLATING, NO ELECTRICAL INTERFACE."

SHEET 8 - BRAKE (A3, 1:2)
  x 1530 to 1740, two pole plates 15 thick, width in y 90, entry taper 30 long, ring spring stop.
  NOTE: "POLES LIGHTENED FROM SOLID BLOCKS ON STRUCTURAL REASONING ONLY. MAGNETIC SIZING
  AGAINST REQUIRED POLE AREA NOT YET DONE."
  NOTE: "TAPERED ENTRY IS THE 200 g DECELERATION LIMITER PROTECTING THE SINTERED NDFEB BOND."

TITLE BLOCK, EVERY SHEET
  Title, drawing number VOL-DRW-0nn, sheet n of 8, scale, first-angle symbol,
  designer A. MISHRA, date, revision, material, general tolerance note, and:
  "GEOMETRY PER cad/parameters.json. THAT FILE IS AUTHORITATIVE; THIS DRAWING IS DERIVED."
  "DESIGN STUDY, TRL 2-3. NOT FOR MANUFACTURE."

WHAT NOT TO DO
  Do not invent a dimension. If something is needed that is not listed above, flag it as
  MISSING FROM SOURCE rather than scaling it off a view or estimating it.
  Do not silently round. 380.5 and 340.5 are real values, not typos.
  Do not omit the open-problem notes to make the drawings look finished. Those notes are the
  reason this set is worth publishing.
```

---

## After the drawings come back

Commit to `cad/drawings/` as both DWG and PDF, add them to `cad/CHANGELOG_CAD.md`, and add the
PDF set to `tools/export_companion.py`'s thesis manifest so the examiner's copy carries them.

**Cross-check before committing.** Every dimension on every sheet against `parameters.json`. A
drawing that disagrees with the parameter file is the same class of defect as a paper that
disagrees with its scripts, and this repository logs four of those.
