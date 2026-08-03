# Gen4 open-assembly status

**Recorded 2026-08-03.** This is a CAD configuration record, not a new operating
point. `EMOCD_Gen4_Open v7` exists in Fusion 360 but has not yet been exported into
this repository. The committed STEP, STL, renders, analyses, paper, and frozen
baseline remain the Phase I / Gen3 record unless a file says otherwise.

## Why this record exists

The Phase I model accelerates through a uniform 1.30 m active stator and releases at
1500 mm. The revised open assembly uses the actual 488 mm sled geometry and gives the
brake a physical interaction interval without extending the track or presenting an
enclosure as the primary public model. Those choices change the geometry that the
motor model must solve. They do not establish a new velocity, energy, thermal, orbit,
or efficiency result.

## Provisional geometry read from `EMOCD_Gen4_Open v7`

Coordinate convention: x is the firing axis and positive x is toward the muzzle. The
sled joint reports `sled_origin_x_mm = slideValue_mm`.

| Item | Value | Status |
|---|---:|---|
| Active sled | 488 mm chassis local x = -180 to +308 mm | Editable local Gen4 copy |
| Halbach arrays | local x = -96 to +244 mm; 340 mm long | Active sled geometry |
| Payload backstop | local x = -308 to -300 mm | Stowed clearance datum |
| Brake fin | local x = +188 to +308 mm | Active sled geometry |
| Track | x = 0 to 1800 mm | Existing source geometry |
| Active stator | x = 0.5 to 1295.5 mm | Existing source geometry |
| Brake envelope | x = 1530 to 1740 mm | Existing source geometry |
| Stowed sled station | s = 300 mm | Backstop clears aft enclosure skin by 24 mm in the envelope check |
| Acceleration end / release | s = 1200 mm | Provisional; 900 mm acceleration stroke |
| Brake entry | s = 1222 mm | Fin forward face reaches x = 1530 mm |
| Arrest-end joint limit | s = 1552 mm | Fin trailing edge clears x = 1740 mm |

The Halbach array is fully over the finite stator from s = 300 to 1051.5 mm. The final
148.5 mm of the acceleration stroke therefore occurs with partial overlap. At the
provisional release station, 191.5 mm of the 340 mm array remains over the stator.
A constant-thrust 1.30 m calculation cannot describe this configuration.

The 12-payload stowed manifest is complete in the working assembly: six port and six
starboard 3U payload occurrences. The previous missing sixth starboard occurrence is
resolved in CAD. It has not been independently checked as a mass, mechanism, or
interference closure.

## What the configuration does and does not resolve

The 900 mm release station is 22 mm before brake-fin entry. The fin then occupies the
brake interval over 330 mm of sled travel, from s = 1222 to 1552 mm. This resolves the
specific release-into-brake overlap seen at the former 1500 mm station without adding
track length.

It does not close the electromagnetic, braking, thermal, or guidance problem:

- A finite-stator, position-dependent motor calculation is required before quoting a
  Gen4 exit velocity, acceleration, electrical energy, or efficiency.
- The Phase I regenerative-stator assumption is not placed in this configuration.
  P28 remains open; no regeneration credit may be carried into a Gen4 result unless
  the hardware is laid out and re-analysed.
- Roller comparisons used excluded diagnostic construction geometry. They are not a
  clearance pass, and the roller-span discrepancy remains open.
- Hidden reference occurrences and envelope-check geometry are not evidence of
  exclusion from mass or interference work. Later work must name its occurrence
  selection explicitly.

## Provenance and export gate

`Gen4_Operational_Export` is a named Fusion selection containing the active sled,
one active brake, stator, track, ESPA interface, two cassettes, and twelve stowed
payloads. It excludes the 360 mm audit sled, the linked source sled, duplicate brake,
construction diagnostic, enclosure-check occurrence, and released-payload reference.
No STEP, STL, or render export has been made from this selection.

The export gate is deliberately closed until the finite-stator result is recorded and
the export selection is checked against the final intended shot and stowed states.

## Relationship to the Phase I baseline

`docs/BASELINE.md`, the paper, current validation results, and the headline values in
the repository remain a frozen Phase I record. The Gen4 configuration is a successor
under analysis, not a silent revision of that record. Once the finite-stator model has
run, every affected result and validation will be classified before one controlled
propagation pass updates public values.
