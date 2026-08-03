# CHANGELOG_CAD: EMOCD_figs
**VOLLEY, an electromagnetic orbital CubeSat deployer**
CAD Generation History, Design Rationale, and Audit Record

**Author:** Adityavardhan Mishra · Symbiosis Institute of Technology, Pune
**PRN:** 23070125054
**Last updated:** 2026-08-03

Read alongside:
- `EMOCD-main/CHANGELOG.md`, analysis and paper change history
- `EMOCD-main/OPEN_PROBLEMS.md`, full defect and open-problem list
- `EMOCD-main/PROVENANCE.md`, what stands behind each claim
- `EMOCD-main/cad/parameters.json`, single source of truth for all dimensions

**Governing rule:** `cad/parameters.json` is the single source of truth for
all dimensions. Fusion 360 is authoritative for geometry and fit only.
`analysis/*.py` is authoritative for mass and performance until FEA closes
the open items. No number in the scripts or the paper is changed on the
strength of CAD geometry alone. Nothing is ever deleted from this file,
superseded content is marked SUPERSEDED in place.

---

## 2026-08-03: PROVISIONAL GEN4 OPEN ASSEMBLY, NOT EXPORTED

`EMOCD_Gen4_Open v7` exists in Fusion 360 as a working open-mechanism configuration. It is
not present in the committed STEP, STL or render set. The repository's Gen3 exports remain the
Phase I CAD record.

The active configuration uses the 488 mm sled at s = 300 mm stowed and s = 1200 mm release.
The brake fin enters the x = 1530-1740 mm brake envelope at s = 1222 mm and clears it at
s = 1552 mm. The 340 mm Halbach array reaches the finite stator edge at s = 1051.5 mm, so the
final 148.5 mm of acceleration is under partial overlap. This prevents a Gen4 performance
claim until the position-dependent electromagnetic calculation is complete.

The primary assembly stays open for explanatory views. The enclosure is retained separately
for envelope checks. `Gen4_Operational_Export` excludes the audit sled, linked source sled,
duplicate brake, construction diagnostic, enclosure check and released-payload reference.
No export has been made from that selection. Full state and gate: `docs/GEN4_STATUS.md` and
ADR-019.

---
> **Repository verification note (added on import, 2026-07-28).** This file is imported
> verbatim; nothing in it has been edited. Two checks were run against the STEP exports
> themselves when they were committed, and both results are recorded in `OPEN_PROBLEMS.md`
> rather than changed here:
>
> - **Sled length fix confirmed.** Gen2 chassis half-length measures 180 mm (360 mm plate);
> Gen3 measures 244 mm (488 mm plate). G2-D1 is genuinely fixed in the export.
> - **Brake placement fix not visible in the exports.** Gen2 and Gen3 brake STEPs are
> geometrically identical (3 bodies each, 79 points each, differing only in file name and
> time stamp), and *both* already place the brake at x = 1530-1740 mm. The G2-D4 claim
> that Gen2 sat at the local origin does not hold for `EMOCD_Brake_Gen2.step`.
> - Minor body-count deltas: `EMOCD_Payload_3U_Gen1.step` measures 5 solids where the table
> below says 1; `EMOCD_Sled_Gen1b.step` measures 11 where the table says ~16.
>
> Body counts elsewhere match. Measured with `grep -c MANIFOLD_SOLID_BREP`.


## PART I: SYSTEM DESCRIPTION AND DESIGN RATIONALE

This section records *why* each major architectural decision was made,
reconstructed from `EMOCD-main/docs/DECISION_LOG.md`, the analysis scripts,
and the IEEE conference paper. Without this context a dimension is just a
number; with it, a dimension is a consequence.

---

### R1. Why this machine exists: the gap it fills

The project began on 22 March 2021. CubeSats flown as rideshare secondaries
inherit the primary customer's orbit. The spring that ejects them adds 1-2
m/s, enough to drift clear of the host vehicle, not enough to change the
orbit. A satellite with no onboard propulsion is stranded in whatever orbit
the primary customer bought, for life.

The regime between spring deployers (~2 m/s) and propulsive orbital transfer
vehicles (hundreds of m/s) is unoccupied. VOLLEY fills it: a system that can
deliver 3U CubeSats at 10-35 m/s without modifying the satellite at all.

The no-modification constraint is not optional, it is what makes the machine
commercially viable. Any system requiring a ferromagnetic or conducting
armature on the customer satellite forces the customer to redesign hardware,
re-qualify, and accept liability for armature interference with their payload.
No rideshare operator accepts those terms for a secondary slot. VOLLEY routes
around this completely: the magnets ride the sled, the sled stays on the
deployer, and the satellite receives a standard push at the pocket wall,
exactly as a spring deployer gives it.

---

### R2. Why a linear synchronous motor, not a coilgun

The first concept (ARDE/INSARM 2021) was built around a coilgun. The switch
to a linear synchronous motor in mid-2025 is the pivotal decision in the
project's history.

Exit velocity is bounded by v = √(2aL). The payload's structural
qualification caps acceleration: for a 3U CubeSat qualified to NASA GEVS, the
peak quasi-static deployment ceiling is roughly 25-30 g. Over any stroke that
fits a secondary-payload envelope, that ceiling produces a maximum exit
velocity of 26-35 m/s, regardless of what the launcher is. A coilgun capable
of 1 km/s is worthless because the satellite cannot survive 1 km/s.

With that ceiling in place, the coilgun's only advantage is unreachable while
every one of its costs is present:

- **1-2% electrical-to-kinetic efficiency**: fundamental, not a maturity
  problem (Sandia-lineage literature across decades of coilgun development).
- **Microsecond pulse timing** against the suck-back effect at the coil
  midpoint. The firing decision is irrevocable once the pulse starts.
- **A ferromagnetic or conducting armature bolted to the customer's
  satellite**, the commercial dealbreaker from R1.
- **No abort capability after firing starts**: the three-inhibit safety
  chain is only meaningful if the shot can be called off.

A linear synchronous motor gives up nothing in the reachable envelope and
inverts every cost:

- **32% electrical-to-payload efficiency** at the rated operating point
  (analysis A27, corrected from an earlier 40% figure that double-counted
  sled kinetic energy as regeneration; this was a project error, documented
  in PROVENANCE.md error 3 and OPEN_PROBLEMS.md).
- **Continuous proportional thrust** with a servo loop that can close on
  position/velocity. Mid-stroke abort is available up to ~45% of stroke
  (~13.5 m/s), the true commit point, corrected from the original claim of
  "anytime before release" (A26).
- **The reusable sled carries the magnets.** The satellite is never modified.
- **Velocity is programmable** by the servo loop, enabling the 0.027 m/s
  (3σ) closed-loop dispersion (A29).

Verified outcome: factor-of-16 efficiency advantage over the coilgun it
replaced, at the same exit velocity.

---

### R3. Why an ironless stator

The first linear-motor layout used an iron-core double-sided stator. Computed
mass: ~65 kg laminations + 32 kg copper, nearly the entire mass budget for
a secondary-payload system.

Beyond mass: an iron-core design creates a sustained ~3.7 kN attraction force
between the Halbach arrays on the sled and the iron stator at all times, not
just during a shot. The sled rollers and guide rails would have to be
designed against this as a permanent preload, feeding back into sled mass,
rail mass, and track stiffness.

Going ironless eliminates both problems. The stator becomes a few kilograms
of copper belt winding. The inter-array attraction still exists (it is what
the sled gap shim tolerance of ±0.05 mm controls, per `parameters.json`
`sled.gap_shim_tolerance`) but acts on the sled chassis, not a fixed iron
core, and only appears when the sled is on the track.

Secondary benefit: the ironless geometry makes the field problem linear and
analytic superposition exact. This is what made the independent magpylib
cross-check a genuine verification rather than two models sharing the same
assumption. The agreement to three digits (0.351 T single-array) is a real
corroboration of the wave model and is one of only two results in the project
with independent corroboration (`EMOCD-main/PROVENANCE.md`).

---

### R4. Why a Halbach array on the sled, not conventional magnets

A Halbach array concentrates the magnetic field on one side and cancels it
on the other. For a double-sided arrangement driving an ironless winding:

**First:** the airgap field is stronger for a given magnet volume than an
alternating-pole arrangement, raising thrust constant Kt directly. The
winding-resolved model gives Kt = 11.22 N per kA/m (A28).

**Second:** the near-zero field on the back side of each array substantially
reduces stray field on the enclosure, magazine cassettes, and customer
satellite sitting in the cassette. This is what allows the silicon-steel
septum in the magazine cassette to be 1 mm rather than a mass-consuming
thick plate. The septum is present in every generation of the Magazine
Cassette CAD as a consequence of this decision.

The sign convention in the Halbach array was one of the first errors found:
two sign errors in the analytic model, caught only by empirically probing a
simulated single array with magpylib (A24) rather than asserting the phase
convention was correct. `verify_field.py` exists because of this error.

---

### R5. Why the eddy-current brake, not regenerative arrest

The original arrest design credited regenerative braking, the same motor
would reverse and recover ~55% of the sled's kinetic energy back into the
supercapacitor bank. This was wrong.

Braking force is bounded by the same thrust constant as acceleration force.
Working backwards from the required arrest distance, motor-only braking at
rated current needs 1.2-2.6 m of track, more than exists. The correct
efficiency, once the false regeneration credit was removed, fell from 40% to
32% (A27). This was the most consequential error in the project because it
propagated into the paper's headline efficiency figure.

The eddy-current brake that replaced it is better suited to the application:

- Force is proportional to velocity, highest force appears earliest in the
  arrest stroke when velocity is highest. Right profile for rapid arrest.
- Contactless. The sled fin passes through the pole-plate field without
  touching anything. No wear, no single-point failure from contact
  degradation over 12 shots per campaign.
- Flight heritage in the eddy-current damper class (solar arrays, antenna
  booms, attitude control mechanisms).

The brake authority turned out to be so large relative to the requirement
that the design constraint inverted: rather than sizing pole plates up for
sufficient force, the pole entry is *tapered* to cap peak deceleration near
200 g and protect the sintered NdFeB magnet bonds from shock. The 30 mm
taper entry length in `parameters.json` `brake.pole_taper_entry_length` is
a direct consequence of this inversion. This taper geometry is present in
every generation of the Brake CAD.

---

### R6. Why dual transverse cassettes

Four magazine architectures were compared and three were eliminated:

**Revolver drum:** ~40% volume waste at cylinder-to-rectangle corners.
Requires a rotary actuator and makes the drum a structural element that must
react magazine preload.

**2-DOF conveying platform:** requires a motor cell under every storage
position. Random access is pointless, deployment order is fixed at
integration and cannot change on orbit.

**Tandem in-tube stack:** geometrically impossible. The sled must return from
muzzle to breech between shots. A tandem stack in that volume blocks the
return path.

**Dual transverse cassettes (adopted):** cassettes flank the track laterally,
loading from the side. Sled return path remains clear. Magazine preload is
reacted by the cassette frame, not the track. The alternating port, starboard
feed pattern keeps lateral centre-of-mass asymmetry to one satellite pitch
at most, bounding the off-axis ejection force component that drives tip-off
torque. This is why `parameters.json` `magazine.satellites_per_cassette = 6`
and the assembly carries exactly two cassette instances.

---

### R7. Why the retention gate is separated from the release mechanism

During ascent, the satellite stack is held against launch vibration by a gate
that preloads the stack into the aft backstop. The key decision: this preload
path runs through structure, directly through the gate frame and cassette
shell, and never through the escapement mechanism that eventually releases
the satellite.

This was directly motivated by the NanoRacks ball-lock anomaly: ascent
preload ran *through* the release mechanism, and jack-screw torque above
0.11 N·m drove it toward seizure. VOLLEY routes that load away from the
release path entirely. The escapement is caged during ascent and sees launch
loads never. This makes the NanoRacks failure mode geometrically impossible.

Consequence in the CAD: the gate frame is a dedicated structural body in the
Magazine Cassette. The two D6 A-286 shear pins (`parameters.json`
`magazine.gate_pin_material = "A-286"`, `gate_pin_count = 2`) at x = 110 mm
and x = 290 mm carry the 5,900 N ascent preload at a margin of 1.2 (A36).
These pins appear in the Magazine Cassette from Gen2 onward, they are
absent in Gen1, which is one of Gen1's documented defects.

---

### R8. Why the coast-and-trim release zone and the x = 1500 mm release point

If the satellite were released at peak motor force, the tip-off torque would
be dominated by the gradient of the Halbach force field over the satellite's
length. A rough calculation puts the leading term above 30°/s against a
requirement of less than 5°/s derived from NRCSD-E flown deployer
performance.

The coast-and-trim zone reduces this: after main acceleration the servo
drives to target velocity and coasts with near-zero force. Release happens
in this coast phase, when electromagnetic force on the satellite is
negligible. The release point at x = 1,500 mm in `parameters.json`
`track.release_point` is the start of this zone. The track runs to 1,800 mm
and the brake occupies x = 1,530-1,740 mm, both beyond the release point,
the sled runs on into the brake *after* the payload departs.

This layout also defines the abort logic: up to ~45% of stroke (~13.5 m/s)
the servo can decelerate the sled and return it to home within the available
track length. Past that the shot is committed. The three-inhibit no-fire
chain must be green before the trigger fires precisely because mid-stroke
abort is a contingency, not a load-bearing safety feature.

---

### R9. Why the ESPA interface and host-agnostic framing

The original design was written around ISRO POEM as a specific host.
Reframing to host-agnostic happened in 2026-07: the deployer is now
specified against a generic four-item interface, a secondary-payload mount
(ESPA-class bolt pattern), a 150-300 W electrical allotment, an attitude
reference able to absorb 81.5 N·s per shot, and a disposal path for the
host stage.

The ESPA Grande ring flange (Ø460 mm OD, Ø400 mm bolt circle, 24x M9 bolts,
25 mm thick) in `parameters.json` `interface_espa` is the reference
interface because it is the most widely flown secondary-payload standard in
the mass class VOLLEY targets.

**Open conflict P9 (unresolved as of Gen3):** the closed installed envelope
is 1,839x 530x 940 mm. ESPA Grande's longest-dimension class limit is
~1,270 mm. VOLLEY exceeds it by ~44% because the brake lives past the 1,500
mm release point and the enclosure spans it. This cannot be resolved in CAD
without a ConOps decision. The paper claims ESPA-Grande-class compatibility
that claim is contradicted by the CAD. This is documented as P12 in
`OPEN_PROBLEMS.md`.

---

### R10. Why the enclosure is the ninth document and why mass is incomplete

The enclosure is the last of the nine documents to be built. It represents
the flight unit as seen from outside: 2 mm aluminium skins, muzzle panel
with a 160x160 mm aperture, aft horseshoe cutout for the ESPA flange,
1,600x200x3 mm radiator at z = 707 mm, and four equipment bays (96 V / 6 F
supercapacitor bank, SiC inverter, avionics sequencer, IMU).

Its mass is absent from `analysis/mass_properties.py`. The 72.3 kg
dry-mass figure in the paper and README is therefore incomplete (open
problem P10). The mass was deferred to avoid adding plausible-sounding
numbers without methodology. The correct fix is to estimate each bay's mass
from geometry and material density, flag it `ESTIMATED_PENDING_VENDOR`, and
add it to `mass_properties.py`.

---

## PART II: GENERATION CHANGE LOG

---

## GEN 1: OG CAD

**Date range:** 2021-2025 (exact build history not reconstructed)
**Fusion hub folder:** `OG CAD` to renamed `Gen1` on 2026-07-28
**STEP exports:** 11 files in `EMOCD_figs/Gen1/`
**Status:** SUPERSEDED. Retained as design heritage and geometric ancestor
reference only. Do not cite Gen1 dimensions without cross-checking against
`cad/parameters.json`.

### What Gen1 is

Gen1 is the original set of Fusion 360 documents built to establish the
physical envelope and structural concept of VOLLEY. It is the first complete
3D realisation of the system and is the geometric source from which
`EMOCD-main/cad/parameters.json` was reverse-engineered by direct read of
the live Fusion model on 2026-07-23 (`parameters.json` `_PROVENANCE`
section, method: "Rebuilt by reading the nine-document Autodesk Fusion model
directly").

Gen1 is therefore the **geometric ancestor** of the entire parameter set.
However, it does not faithfully represent the current design in several
areas: it reflects design decisions that were later reversed, and several
sub-systems were built as structural proxies rather than detailed mechanism
models.

### Gen1 file inventory (verified by direct Fusion API read, 2026-07-28)

| File | STEP size | Bodies read | Key geometry | Notes |
|---|---|---|---|---|
| `EMOCD_Track_Gen1.step` | 47,302 bytes | 8 | Longerons 1800x20x65 mm; 4x GuideRail 1800x8x22 mm; 2x LaunchLock 20x10x28 mm | Longeron length correct at 1800 mm. Longeron web only 20 mm wide, no outrigger structure, roller channels, or cross-tie frames present |
| `EMOCD_Stator_Gen1.step` | 1,954,907 bytes | 324 | Conductors 7x90x10 mm each | **Two-layer winding**: Belt_Top and Belt_Bottom groups, 162 conductors per layer = 324 total. Contradicts `parameters.json` `stator.layer_count_decision: "OPEN — single vs two-layer … Single layer as drawn."` Gen1 implemented two layers; this was unresolved at build time. The large STEP file size (1.95 MB vs ~9 KB for the repo export) reflects the full 324-body geometry |
| `EMOCD_Sled_Gen1.step` | 30,359 bytes | 5 | Chassis plates 488x140x6 mm; webs 488x6x140 mm; backstop 8x140x140 mm | **Chassis structural box only.** No Halbach arrays, no rollers, no brake fin. This is a structural proxy, geometry and fit only. The 488x140 mm footprint and 6 mm chassis plate thickness are correct per spec |
| `EMOCD_Sled_Gen1b.step` | 50,130 bytes | ~16 | Chassis + partial sled detail | **Duplicate sled document**: a later revision of the Gen1 sled with more detail than `Sled_Gen1` but less than Gen2. Included rollers and additional bodies not in `Sled_Gen1`. Named `Gen1b` to disambiguate. Not in `EMOCD-main/cad/step/` |
| `EMOCD_Magazine_Cassette_Gen1.step` | 89,234 bytes | 16 | Shell 380.5x166x690 mm; septum 350x1x620 mm; follower plate 380.5x158x6 mm; gate frame 10x580x140 mm; 6x divider plates | Shell dimensions correct. Silicon-steel septum present at 1 mm. **Missing: D6 shear pins, escapement fingers, SMA pin puller.** Includes 6x internal satellite divider plates (340x126x2 mm) that are not in `parameters.json`, these appear to be an early non-parametric approach to satellite slot separation, later superseded by the escapement mechanism |
| `EMOCD_Brake_Gen1.step` | 22,915 bytes | 4 | Poles: BrakePole_Top_Main 180x90x15 mm, BrakePole_Top_Taper 30x90x15 mm (x2 for bottom) | Pole plate thickness 15 mm correct. Taper entry 30 mm correct. **Missing ring spring stop** (`parameters.json` `brake.ring_spring_stop = true`). **Modelled at x = 0 (local origin)**: not placed at assembly x = 1530 mm |
| `EMOCD_Interface_ESPA_Gen1.step` | 77,997 bytes | 6 | Flange ring 25x460x460 mm; hub plate 15x300x300 mm; 4x gussets | Flange OD 460 mm, thickness 25 mm, and hub plate 300 mm diameter all correct. **Bolt holes absent**: 24x M9 on Ø400 mm BCD not modelled |
| `EMOCD_Enclosure_Gen1.step` | 72,627 bytes | 11 | Skins: 1839x530x2 mm (top, bottom, sides); aft horseshoe 2 mm; muzzle panel 2 mm; radiator 1600x200x3 mm; 4x equipment bays | **Most complete Gen1 document.** All dimensions match `parameters.json` precisely. All four equipment bays present (supercap bank, PPU/SiC, avionics sequencer, IMU). Radiator, muzzle aperture panel, and aft horseshoe cutout all present |
| `EMOCD_Payload_3U_Gen1.step` | 30,613 bytes | 1 | 340.5x100x100 mm solid | Correct dimensions per `parameters.json` `payload_3u`. Solid aluminium proxy, real 3U flight mass is 4 kg, not Fusion-computed value |
| `EMOCD_Assembly_Gen1.step` | 229,550 bytes | | Full 9-document assembly | Post-split assembly referencing all component documents. **Zero joints**: all occurrences grounded, no kinematic definition. No sled slider joint, no payload joints |
| `EMOCD_Deployer_Assembly_Gen1.step` | 246,874 bytes | | Legacy single-file assembly | **SUPERSEDED single-file model** built before the nine-document split. Carried unsaved modifications at time of audit (2026-07-23 CAD Master Plan). Not present in `EMOCD-main/cad/step/`, the only Gen1 file with no repo counterpart. Retained for heritage only. Must not be edited |

### Gen1 known defects

The following defects were identified by direct Fusion API read on 2026-07-28
and by comparison against `cad/parameters.json`. This is the complete list,
nothing is inferred or estimated.

| ID | File | Defect | Consequence | Fixed in |
|---|---|---|---|---|
| G1-D1 | Sled | Missing Halbach arrays, rollers, brake fin | Sled is structural proxy only, no electromagnetic or dynamic geometry | Gen2 |
| G1-D2 | Stator | 324 bodies (two-layer) vs single-layer repo spec | Contradicts `parameters.json` `stator.layer_count_decision` which states single-layer as drawn | Gen2 |
| G1-D3 | Magazine | Missing D6 shear pins, escapement fingers, SMA pin puller | Gate release mechanism incomplete | Gen2 |
| G1-D4 | Brake | Missing ring spring stop | Arrest mechanism incomplete, only eddy poles present | Gen2 |
| G1-D5 | Interface ESPA | Bolt holes absent | 24x M9 on Ø400 mm BCD not modelled | Not resolved in Gen2 or Gen
| G1-D5 | Interface ESPA | Bolt holes absent | 24x M9 on Ø400 mm BCD not modelled | Not resolved in Gen2 or Gen3, bolt holes remain absent across all generations. Open geometry gap |
| G1-D6 | Assembly | Zero joints, static pile of grounded occurrences | No kinematic definition. No sled slider, no payload cradle joint | Gen3 assembly partially, 8 components grounded, sled slider added via as-built joint |
| G1-D7 | Deployer_Assembly_v1 | Open with unsaved modifications at time of 2026-07-23 audit | Risk of incorrect geometry being committed if saved | Closed without saving on 2026-07-23. Not touched since |
| G1-D8 | Track | Longeron web only 20 mm wide vs 205 mm overall width spec | No roller channels, no outrigger structure, no cross-tie frames | Gen2 added frame ties and outrigger posts. Gen3 extended further |
| G1-D9 | Sled | Chassis plate parameters not parametrically driven | Face offsets applied via direct edit did not persist across timeline recompute | Addressed in Gen3 by sketch geometry remapping |
| G1-D10 | Brake | Placed at local origin (x = 0) not at assembly x = 1530 mm | Brake appears at breech end in assembly, incorrect position relative to release point at x = 1500 mm | Gen3, brake moved to x_start = 1530 mm |
| G1-D11 | Magazine | 6x internal divider plates present but not in parameters.json | Non-parametric satellite separation approach, superseded by escapement mechanism | Gen2, dividers removed, escapement fingers and gate mechanism added |

---

## GEN 2: First Structured Revision

**Date range:** 2025-2026-07 (built iteratively; exact commit dates not
reconstructed)
**Fusion hub folder:** `Fresh` to renamed `Gen2` on 2026-07-28
**STEP exports:** 9 files in `EMOCD_figs/Gen2/`
**Status:** SUPERSEDED by Gen3. Retained as intermediate reference showing
the transition from structural proxy models to mechanism-level detail.

### What Gen2 is

Gen2 is the first structured revision of the VOLLEY CAD, built after the
coilgun-to-LSM decision was finalised and after `cad/parameters.json` was
established as the governing source of truth. All nine documents were built
as separate Fusion files from the outset, each corresponding to one row in
`parameters.json` `documents`.

Gen2 corrected the major structural proxy issues in Gen1, sled mechanism
completeness, stator layer count, magazine mechanism detail, brake ring
spring stop. It is the first generation that can be called a mechanism-level
model rather than a structural envelope. The `_FRESH` suffix used during
build was informal, it meant "freshly built from parameters" as opposed to
the legacy organic Gen1 geometry. Renamed `_Gen2` on 2026-07-28.

Gen2 did not resolve all defects. Several parameter mismatches carried
forward from Gen1 (longeron overall width, brake local-origin placement,
sled sketch parametric driving) and were only corrected in Gen3. The
assembly in Gen2 still had zero joints, carrying G1-D6 forward.

### Gen2 file inventory (verified by direct Fusion API read, 2026-07-28)

| File | STEP size | Bodies read | Key geometry | Notes |
|---|---|---|---|---|
| `EMOCD_Track_Gen2.step` | 35,670 bytes | 4 | Longerons 1800x45x65 mm; 2x launch locks | Longerons at correct 1800 mm length. Width grown to 45 mm (vs 20 mm in Gen1), wider web section. No roller channels or guide flanges yet. File is smaller than Gen1 Track despite more detail, different sketch approach |
| `EMOCD_Stator_Gen2.step` | 967,482 bytes | 162 | Conductors 7x90x10 mm | **Single-layer, 162 conductors**: corrects G1-D2. Belt sequence A+/C−/B+/A−/C+/B− with phase labelling per conductor. STEP file approximately halved in size vs Gen1 (967 KB vs 1.95 MB) reflecting the single-layer correction |
| `EMOCD_Sled_Gen2.step` | 80,554 bytes | 16 | Chassis plates 360x110x6 mm; Halbach arrays upper/lower 340x90x8 mm; 4x rollers 30x16x30 mm (Ø30 mm); 4x roller arms; brake fin 120x80x4 mm | **Mechanism-level sled**: corrects G1-D1. Halbach arrays, rollers, roller arms, and brake fin all present. **However:** chassis length is 360 mm (should be 488 mm per parameters.json) and width is 110 mm (should be 140 mm). These dimensional errors were identified in the Gen2-to-Gen3 audit and corrected in Gen3. Roller diameter already correct at 30 mm |
| `EMOCD_Magazine_Cassette_Gen2.step` | 132,249 bytes | 24 | Shell 380.5x140x640 mm; septum 350x1x620 mm; follower plate + leadscrew; escapement fingers x2; gate frame + D6 pins x2; SMA pin puller; follower motor | **Full mechanism model**: corrects G1-D3 and G1-D11. D6 shear pins present, escapement fingers present, SMA pin puller present, follower motor present. Gate frame and retention mechanism complete. Divider plates from Gen1 removed. Cassette height 640 mm vs 690 mm in parameters.json, 50 mm short |
| `EMOCD_Brake_Gen2.step` | 20,143 bytes | 3 | Pole upper 170x90x30 mm; pole lower 170x90x30 mm; ring spring stop 30x90x92 mm | **Ring spring stop added**: corrects G1-D4. Both poles present with taper geometry. Brake placed at local origin, G1-D10 not yet corrected |
| `EMOCD_Interface_ESPA_Gen2.step` | 73,434 bytes | 6 | Flange ring 25x460x460 mm; hub plate 15x300x300 mm; 4x gussets | Same as Gen1 interface geometry. Bolt holes still absent, G1-D5 not corrected. Gusset geometry refined |
| `EMOCD_Enclosure_Gen2.step` | 77,268 bytes | 11 | Skins 1835x2 mm; radiator 1600x200x3 mm; 4x equipment bays | Enclosure present and correct. All dimensions consistent with parameters.json. 4 equipment bays (supercap, PPU, avionics, IMU) all present. Essentially identical to Gen1 Enclosure in content |
| `EMOCD_Payload_3U_Gen2.step` | 9,273 bytes | 1 | 340.5x100x100 mm | Correct dimensions. File size much smaller than Gen1 (9 KB vs 30 KB), simplified solid proxy. Same geometry, leaner model |
| `EMOCD_Assembly_Gen2.step` | 1,433,428 bytes | 21 occurrences | Full assembly: track, stator, sled, 2x cassettes, brake x2, 12x payload, enclosure, ESPA | Assembly references v2/v4 versions of component documents (not the v1 files audited above, newer saved versions in hub). 12 payloads present (6 per cassette). **Zero joints**: G1-D6 not corrected in Gen2. All occurrences ungrounded at this stage |

### What Gen2 corrected vs Gen1

| Defect ID | Defect | Resolution in Gen2 |
|---|---|---|
| G1-D1 | Sled missing Halbach arrays, rollers, brake fin | Fixed, all mechanism bodies present in Gen2 Sled (16 bodies) |
| G1-D2 | Stator two-layer (324 bodies) | Fixed, single-layer 162 conductors with phase labelling |
| G1-D3 | Magazine missing pins, escapement, SMA puller | Fixed, all mechanism bodies present (24 bodies total) |
| G1-D4 | Brake missing ring spring stop | Fixed, ring spring stop body present |
| G1-D11 | Magazine non-parametric divider plates | Fixed, dividers removed, replaced by escapement mechanism |

### Gen2 defects carried forward to Gen3

| ID | File | Defect | Evidence |
|---|---|---|---|
| G2-D1 | Sled | Chassis length 360 mm vs 488 mm spec | Verified by Fusion API read: chassis_plate_upper 360x110x6 mm |
| G2-D2 | Sled | Chassis width 110 mm vs 140 mm spec | Verified by Fusion API read: chassis_plate_upper 360x110x6 mm |
| G2-D3 | Magazine | Cassette height 640 mm vs 690 mm spec | Verified by Fusion API read: Shell_Front 380.5x4x640 mm |
| G2-D4 | Brake | Placed at local origin, not x = 1530 mm assembly position | Verified by Fusion API read: brake_yoke x_start = 30 mm not 1530 mm |
| G2-D5 | Interface ESPA | Bolt holes absent | Not modelled in any generation |
| G2-D6 | Assembly | Zero joints, no kinematic definition | Verified by Fusion API read: root.joints.count = 0 |
| G2-D7 | Track | No roller channels or guide flange geometry | Track is longerons and launch locks only |

---

## GEN 3: Parameter-Reconciled Revision

**Date range:** 2026-07 (built during the 2026-07-23 CAD build session and
subsequent corrections applied 2026-07-28)
**Fusion hub folder:** `Even more fresh` to renamed `Gen3` on 2026-07-28
**STEP exports:** 10 files in `EMOCD_figs/Gen3/` (9 component files + 1
monolithic single-file model `EMOCD_Gen3.step`)
**Status:** CURRENT. This is the generation against which open problems P5, P12 are indexed. All geometry values carry status from `parameters.json`.

### What Gen3 is

Gen3 is the parameter-reconciled revision of the VOLLEY CAD. It was built
during the 2026-07-23 CAD build session documented in the `EMOCD_CAD_Master_Plan.md`
working document, which performed a live read of the Fusion hub via the
Fusion MCP and rebuilt the parameter set from the actual geometry. This is
the build that produced the current `cad/parameters.json`.

Gen3 introduced two things that did not exist in any earlier generation:

1. **The `EMOCD_Gen3.step` monolithic model** (2,520,630 bytes), a
   single Fusion document (`EMOCD_Gen3`, previously named `VOLLEY but really
   detailed`) that contains all nine sub-systems as components within one
   assembly file. This is the most detailed single-file representation of
   the system and is the model used for the CAD renders in `EMOCD-main/cad/renders/`.

2. **The first assembly with joint definitions**, the Gen3 assembly has 8
   structural components grounded (`isGrounded = True`: Track, Stator, both
   Cassettes, both Brake instances, Interface ESPA, Enclosure) and a sled
   slider as-built joint defining X-axis travel with limits 0-1740 mm. Gen1
   and Gen2 assemblies had zero joints.

Gen3 also corrected all dimensional defects identified in Gen2 (sled length,
sled width, brake position) and corrected the user parameters in the
monolithic model that were previously not propagating to geometry.

### Gen3 file inventory (verified by direct Fusion API read, 2026-07-28)

| File | STEP size | Bodies read | Key geometry | Notes |
|---|---|---|---|---|
| `EMOCD_Track_Gen3.step` | 35,241 bytes | 4 | Longerons 1800x45x65 mm; 2x launch locks | Longerons at correct 1800 mm length. Same structure as Gen2 Track. No roller channels, G2-D7 not resolved |
| `EMOCD_Stator_Gen3.step` | 967,476 bytes | 162 | Conductors 7x90x10 mm | Single-layer 162 conductors with phase labelling, same as Gen2. Correct per spec. File size within 6 bytes of Gen2 Stator (967,476 vs 967,482), effectively identical geometry |
| `EMOCD_Sled_Gen3.step` | 80,874 bytes | 16 | Chassis plates 488x140x6 mm; Halbach arrays 340x90x8 mm; 4x rollers Ø30x16 mm; roller arms; brake fin | **Dimensional corrections applied**: corrects G2-D1 and G2-D2. Chassis length 488 mm (was 360 mm in Gen2) and width 140 mm (was 110 mm in Gen2) now match `parameters.json` `sled.overall_length` and `sled.overall_width`. Achieved by remapping sketch point geometry and forcing design.computeAll(). Roller diameter 30 mm correct throughout Gen2 and Gen3 |
| `EMOCD_Magazine_Cassette_Gen3.step` | 131,320 bytes | 24 | Shell 380.5x140x640 mm; full mechanism | Same mechanism completeness as Gen2 (24 bodies). Cassette height still 640 mm (G2-D3 not resolved in Gen3. File 929 bytes smaller than Gen2) minor geometry refinement |
| `EMOCD_Brake_Gen3.step` | 20,136 bytes | 3 | Poles with taper; ring spring stop | **Brake position corrected**: corrects G2-D4. Brake placed at x_start = 1530 mm (was at local origin in Gen1 and Gen2). Verified by Fusion API read: brake_yoke minPoint.x = 153.0 cm. Ring spring stop present, taper geometry correct |
| `EMOCD_Interface_ESPA_Gen3.step` | 73,428 bytes | 6 | Flange ring Ø460 mm OD, 25 mm thick; hub plate Ø300 mm, 15 mm thick; 4x gussets; 24 bolt holes | **Bolt holes added**: partially corrects G1-D5. 24 bolt holes on Ø400 mm BCD modelled by sketch + cut extrude in the Gen3 session on 2026-07-28. This is the first generation with bolt holes present. Gussets at 0/90/180/270 deg |
| `EMOCD_Enclosure_Gen3.step` | 78,457 bytes | 11 | Skins 1839x530x2 mm; radiator 1600x200x3 mm; muzzle aperture; aft horseshoe cutout; 4x equipment bays | Full enclosure with all features. 1,231 bytes larger than Gen2, minor geometry refinement. All dimensions consistent with `parameters.json` |
| `EMOCD_Payload_3U_Gen3.step` | 9,267 bytes | 1 | 340.5x100x100 mm | Correct dimensions. 6 bytes smaller than Gen2, effectively identical |
| `EMOCD_Assembly_Gen3.step` | 1,433,418 bytes | 21 occurrences | Full assembly with joints | **First assembly with kinematic joints**: corrects G1-D6 / G2-D6. 8 structural components grounded, sled slider as-built joint with X-axis limits 0-1740 mm. 12 payloads (6 per cassette), 2x cassette instances, 2x brake instances. File 10 bytes smaller than Gen2 Assembly, effectively identical geometry, the joint definitions are not reflected in STEP size |
| `EMOCD_Gen3.step` | 2,520,630 bytes | 9 sub-components, all bodies | Monolithic single-file assembly with all 9 sub-systems | **Unique to Gen3.** The `VOLLEY but really detailed` document renamed `EMOCD_Gen3`. Contains Track (43 bodies), Stator (170 bodies including 162 conductors + spine + brackets), Sled (76 bodies including 56 Halbach magnets + chassis + 8 rollers + brake fin + detent latches), Payload (12 bodies, 12 CubeSat instances), Cassette_P (18 bodies), Cassette_S (18 bodies, corrected from 16 in earlier state by adding interface_pad_S5_0 and S5_1), Brake (8 bodies), Avionics (39 bodies including 32 supercap cells), Interface (9 bodies including bolt holes and gussets), Enclosure (7 bodies: 6 skins + radiator). Most complete single representation of VOLLEY in any generation |

### What Gen3 corrected vs Gen2

| Defect ID | Defect | Resolution in Gen3 |
|---|---|---|
| G2-D1 | Sled chassis length 360 mm | Fixed, 488 mm, verified by Fusion API read |
| G2-D2 | Sled chassis width 110 mm | Fixed, 140 mm, verified by Fusion API read |
| G2-D4 | Brake at local origin | Fixed, brake x_start = 1530 mm, verified by Fusion API read |
| G2-D6 | Assembly zero joints | Fixed, 8 components grounded, sled slider joint X-axis 0-1740 mm |
| G1-D5 | ESPA bolt holes absent | Fixed in Gen3 Interface ESPA, 24 holes on Ø400 mm BCD now modelled |

### Gen3 defects and open problems remaining

The following defects were identified by direct Fusion API read on 2026-07-28
and by comparison against `cad/parameters.json` and `OPEN_PROBLEMS.md`.
These are unresolved as of the last audit.

| ID | File | Defect | Evidence | Repo reference |
|---|---|---|---|---|
| G3-D1 | Magazine (all gens) | Cassette height 640 mm vs 690 mm spec | Verified: Shell_Front 380.5x4x640 mm in Gen2 and Gen3. 50 mm short | `parameters.json` `magazine.cassette_height_z = 690` |
| G3-D2 | Track (all gens) | No roller channels, guide flanges, or cross-tie outrigger structure | Track is longerons + launch locks only. `parameters.json` specifies roller_channel_y_inner/outer and guide_rail geometry | `parameters.json` track group |
| G3-D3 | Sled (monolithic Gen3) | Chassis width reached 139.8 mm not exact 140 mm | Residual rounding from sequential face-offset operations. Within 0.2 mm of spec | `parameters.json` `sled.overall_width = 140` |
| G3-D4 | Stator (all gens) | Layer count decision still open | Single-layer as built, but `parameters.json` explicitly flags `layer_count_decision: OPEN`. Two-layer may be the correct electromagnetic design | `parameters.json` `stator.layer_count_decision` |
| G3-D5 | Sled (all gens) | Halbach arrays not repositioned after sled length correction | After chassis extended 360 to 488 mm, Halbach array start position not re-centred on the new chassis length | `parameters.json` `sled.halbach_array_x_start = 230 mm` |
| G3-D6 | Assembly (all gens) | No payload-on-sled rigid joint | `parameters.json` `documents.EMOCD_Assembly` specifies `payload_on_sled_rigid` joint. Not present in any generation | `parameters.json` documents section |
| G3-D7 | All gens | Masses absent from `mass_properties.py` for enclosure, radiator, avionics | 72.3 kg dry mass figure is incomplete | Open problem P10 |
| G3-D8 | All gens | CAD sled mass ~7.50 kg vs parametric 4.86 kg | Exit velocity provisional at 17.88 m/s pending structural FEA (ANSYS A4) | Open problems P5, P8 |
| G3-D9 | All gens | Installed envelope 1839 mm exceeds ESPA Grande ~1270 mm limit by ~44% | Brake must live past 1500 mm release point, forcing total length | Open problem P9 |
| G3-D10 | All gens | Paper claims ESPA-Grande-class compatibility contradicted by CAD | P12 in OPEN_PROBLEMS.md, not yet corrected in paper.tex | Open problem P12 |
| G3-D11 | All gens | Whether P1, P4 paper corrections reached the submitted build is unconfirmed | `paper/archive/EMOCD_submission_uncorrected.pdf` still carries incorrect values | Open problem P11 |

---

## PART III: CROSS-GENERATION COMPARISON SUMMARY

This table shows the state of each sub-system across all three generations,
verified by direct Fusion API read of the live Fusion documents on 2026-07-28.

| Sub-system | Gen1 | Gen2 | Gen3 |
|---|---|---|---|
| **Track** | 8 bodies. Longerons 1800 mm ✅. Width 20 mm ❌ (no outrigger). | 4 bodies. Longerons 1800x45 mm. Slightly wider but still no outrigger ❌. | 4 bodies. Same as Gen2. Outrigger gap not closed ❌. |
| **Stator** | 324 bodies. Two-layer ❌. 7x90x10 mm conductors ✅. | 162 bodies. Single-layer ✅. Phase-labelled ✅. | 162 bodies. Identical to Gen2 ✅. Monolithic model adds spine + brackets. |
| **Sled** | 5 bodies. Chassis only ❌. Length 488 mm ✅, width 140 mm ✅, plate 6 mm ✅. No Halbach, rollers, fin ❌. | 16 bodies. Halbach ✅, rollers Ø30 mm ✅, fin ✅. But length 360 mm ❌, width 110 mm ❌. | 16 bodies. Length 488 mm ✅, width ~140 mm ✅. All mechanism bodies ✅. Brake fin present ✅. |
| **Magazine Cassette** | 16 bodies. Shell correct ✅. Septum ✅. No pins, escapement, SMA ❌. Has non-spec dividers ❌. | 24 bodies. D6 pins ✅. Escapement ✅. SMA puller
| **Magazine Cassette** | 16 bodies. Shell correct ✅, septum ✅. No D6 pins ❌, no escapement ❌, no SMA puller ❌. Non-spec divider plates ❌. | 24 bodies. D6 pins ✅, escapement ✅, SMA puller ✅, follower motor ✅. Dividers removed ✅. Height 640 mm vs 690 mm spec ❌. | 24 bodies. Same mechanism completeness as Gen2 ✅. Height still 640 mm ❌. |
| **Brake** | 4 bodies. Pole thickness 15 mm ✅, taper 30 mm ✅. No ring spring stop ❌. At local origin ❌. | 3 bodies. Ring spring stop added ✅. Still at local origin ❌. | 3 bodies. Ring spring stop ✅. Placed at x = 1530 mm ✅. |
| **Interface ESPA** | 6 bodies. Ø460 mm OD ✅, 25 mm thick ✅, hub plate ✅, 4x gussets ✅. No bolt holes ❌. | 6 bodies. Same geometry as Gen1. Bolt holes still absent ❌. | 6 bodies + bolt holes. 24x M9 on Ø400 mm BCD added ✅. First generation with complete interface geometry. |
| **Enclosure** | 11 bodies. All skins ✅, radiator ✅, muzzle aperture ✅, aft horseshoe ✅, 4x equipment bays ✅. Most complete Gen1 document. | 11 bodies. Effectively identical to Gen1 Enclosure ✅. | 11 bodies (component file). Monolithic model separately adds enclosure skins + radiator ✅. |
| **Payload 3U** | 1 body. 340.5x100x100 mm ✅. | 1 body. 340.5x100x100 mm ✅. Smaller STEP (9 KB vs 30 KB). | 1 body. 340.5x100x100 mm ✅. 12 instances in assembly ✅. |
| **Assembly** | 11 files including legacy monolith. Zero joints ❌. References split docs ✅. | 9 files. Zero joints ❌. 21 occurrences ✅ (12 payloads, 2 cassettes, 2 brake instances). | 10 files including monolithic EMOCD_Gen3. 8 components grounded ✅. Sled slider joint X-axis 0-1740 mm ✅. No payload-on-sled rigid joint ❌. |
| **Monolithic model** | EMOCD_Deployer_Assembly_v1 (legacy, unsaved mods, not in repo) ❌ | None | EMOCD_Gen3.step (2.52 MB) ✅, all 9 sub-systems in one file, most detailed representation in any generation. Stator has 170 bodies (162 conductors + spine + 7 brackets). Cassette S-side corrected from 16 to 18 bodies. |

---

## PART IV: OPEN PROBLEMS INDEXED TO CAD

The following open problems from `EMOCD-main/OPEN_PROBLEMS.md` have direct
CAD consequences. They are reproduced here for completeness so this file can
be read standalone. Described in full in `OPEN_PROBLEMS.md`.

| Problem | Description | CAD consequence | Status |\n|---|---|---|---|\n| **P5** | CAD sled mass ~7.50 kg vs parametric assumption 4.86 kg | Exit velocity provisional at 17.88 m/s, not 20.37 m/s. No number in `analysis/*.py` changed. Sled chassis flagged `PROVISIONAL_PENDING_FEA` in `parameters.json` | Open. Requires ANSYS structural FEA (validation A4) |\n| **P7** | Brake occupies x = 1530-1740 mm, beyond x = 1500 mm release point | Track and enclosure must extend past release, directly drives the 1839 mm total length and therefore P9 | Open. ConOps decision required |\n| **P8** | Exit velocity provisionally 17.88 m/s if CAD sled mass holds | All downstream numbers (acceleration, efficiency, recoil, lifetime multiplier) shift. Not propagated into scripts or paper pending FEA | Open. Waiting on P5 resolution |\n| **P9** | Installed envelope 1839 mm exceeds ESPA Grande ~1270 mm limit by ~44% | Machine cannot fit ESPA Grande as claimed. Host claim must be re-scoped or track repackaged | Open. Owner decision, cannot be resolved in code |\n| **P10** | Enclosure, radiator, avionics absent from `mass_properties.py` | 72.3 kg dry-mass rollup is incomplete by an unknown amount | Open. Needs bay-by-bay mass estimation, then addition to `mass_properties.py` |\n| **P11** | Whether P1, P4 corrections reached the submitted paper build is unconfirmed | `paper/archive/EMOCD_submission_uncorrected.pdf` still carries all four incorrect values. If this is the version of record, a corrigendum is needed, not a git commit | Open. Must confirm which build was submitted |\n| **P12** | Paper claims ESPA-Grande-class envelope; CAD contradicts this by ~44% | Two places in paper.tex assert compatibility the geometry does not support. One is an abstract-level capability claim; the other is in the limitations section | Open. Entangled with P11, resolve P11 first, then fix paper.tex in one pass |\n| **E1** | 3-D field end effects on Kt uncomputed | FEMM cross-section DXF and run sheet exist (`analysis/femm/`) but nothing has been run. A few percent on Kt unaccounted | Open. FEMM package written, not executed |\n| **E2** | No FEA of any structural component | Sled, track, brake poles, cassette shell all first-pass geometry with no structural analysis behind them | Open. Validations A1 and A4 specified in `validation/` with pre-declared acceptance bands |\n| **E3** | Enclosure, radiator, and avionics masses missing from rollup | Directly feeds P10 | Open |\n| **E10** | Launch restraint drawn but not analysed | Retention gate pin sizing exists (two D6 A-286, margin 1.2, A36) and launch-lock blocks are in Track CAD but escapement caging, cam lock, and tolerance stack-up under vibration not analysed | Open, CAD advances this item from concept to drawn, not to analysed |\n\n---\n\n## PART V, FILE NAMING CONVENTION\n\nAll files across all generations follow the pattern:\n\n```\nEMOCD_[SubSystem]_[Generation].step\n```\n\nWhere `[SubSystem]` is one of:\n`Track`, `Stator`, `Sled`, `Magazine_Cassette`, `Brake`, `Interface_ESPA`,\n`Enclosure`, `Payload_3U`, `Assembly`\n\nAnd `[Generation]` is `Gen1`, `Gen2`, or `Gen3`.\n\nSpecial cases:\n- `EMOCD_Deployer_Assembly_Gen1.step` (legacy single-file model, Gen1 only,\n no repo counterpart. Superseded.\n- `EMOCD_Sled_Gen1b.step`) duplicate sled document from Gen1, later revision\n than `Sled_Gen1`. Suffix `b` added to disambiguate.\n- `EMOCD_Gen3.step`, monolithic single-file model, Gen3 only. Contains all\n nine sub-systems in one Fusion document. The most detailed and complete\n representation of VOLLEY in any generation.\n\n### Folder rename history\n\n| Original folder name | Renamed to | Date | Reason |\n|---|---|---|---|\n| `OG CAD` | `Gen1` | 2026-07-28 | Align with generation naming convention |\n| `Fresh` | `Gen2` | 2026-07-28 | `_FRESH` suffix meant \"built from parameters\", formalised as Gen2 |\n| `Even more fresh` | `Gen3` | 2026-07-28 | Formalised as Gen3 |\n\n---\n\n## PART VI, WHAT TO CHECK BEFORE USING ANY FILE\n\nBefore citing or using any geometry from `EMOCD_figs`:\n\n1. **Use Gen3 files unless you specifically need a heritage comparison.**\n Gen1 and Gen2 contain known dimensional and mechanism defects.\n\n2. **Cross-check every dimension against `cad/parameters.json`.**\n `parameters.json` is the source of truth, not the Fusion model. If they\n disagree, `parameters.json` wins and the CAD needs correcting.\n\n3. **Do not quote Fusion-computed masses.** The Fusion models use solid copper\n for the stator, solid aluminium for CubeSats, and steel standing in for\n NdFeB. None of these are the correct material densities. Mass authority\n is `analysis/mass_properties.py` only, and even that is incomplete (P10).\n\n4. **The sled mass conflict is unresolved (P5/P8).** The headline exit\n velocity of 20.37 m/s assumes a 4.86 kg sled. The Gen3 CAD sled geometry\n implies ~7.50 kg, which gives a provisional 17.88 m/s. Do not use either\n number without noting this conflict until ANSYS structural FEA (A4)\n resolves it.\n\n5. **The ESPA envelope claim is not supported by the CAD (P9/P12).** The\n installed length of 1839 mm exceeds ESPA Grande's ~1270 mm limit by ~44%.\n Do not present VOLLEY as ESPA-Grande-compatible without noting this open\n problem.\n\n6. **The stator layer count is still an open design decision.** Gen1 built\n two layers; Gen2 and Gen3 built one layer; `parameters.json` explicitly\n flags the decision as open. The electromagnetic consequence (roughly x2\n on force for the same current, but also x2 on copper mass and winding\n complexity) has not been computed for the two-layer case.\n\n---\n\n*End of CHANGELOG_CAD. Append new entries below this line.*\n```
