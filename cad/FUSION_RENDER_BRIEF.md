# Render brief for the Fusion assistant

Paste the block below into the Fusion 360 assistant with the VOLLEY assembly open. It is kept
here rather than in a chat window so the render set can be reproduced, and so that when the
geometry changes the brief changes with it.

**Why the enclosure comes off.** The current render set leads with the machine closed, which
shows a box. The interesting object is the track, the stator belts, the Halbach sled and the
two cassettes. Every hero image below is enclosure-off; the closed view survives only as a
single packaging shot, because the ESPA envelope overrun (P9) is a real constraint a reader
should see.

---

## The prompt

```
You are rendering an engineering assembly for a public technical repository, not a product
advertisement. Priorities in order: read the geometry clearly, look consistent across the set,
look good. Never let a lighting or composition choice hide a mechanism.

ASSEMBLY AND COORDINATE FRAME
This is VOLLEY, a magazine-fed electromagnetic CubeSat deployer. The frame, from
cad/parameters.json, is:
  x = firing axis, positive toward the muzzle, origin x=0 at the ESPA flange aft mating face
  y = lateral, +y port, -y starboard
  z = vertical, z=0 at the stator mid-plane
Overall installed envelope is 1839 x 530 x 940 mm. The track longerons run 1800 mm. The
acceleration zone ends at x=1300, release is at x=1500, the eddy brake occupies x=1530 to 1740.

VISIBILITY, APPLIED TO EVERY SHOT UNLESS SAID OTHERWISE
  HIDE: the outer enclosure panels, and any skin or shroud that occludes the track.
  SHOW: track longerons and guide rails, stator belts, the sled with its Halbach arrays,
        both magazine cassettes, the eddy brake poles, the ESPA ring flange.
  Keep the two cassettes populated with CubeSats. An empty magazine reads as an unfinished
  model rather than a deliberate view.

MATERIALS
  Track and structure: bead-blasted or anodised aluminium, matte. No chrome, no mirror finish.
  Stator belts: copper, distinctly warmer than the structure so the winding reads at a glance.
  Halbach magnets: dark nickel-plated, near-black, slightly glossy. They should read as the
    densest object in the frame, because they are.
  CubeSats: neutral mid-grey anodised, deliberately plain. They are cargo, not the subject.
  ESPA flange: same aluminium as the structure.
  Avoid colour-coding phases in the renders. The A/B/C belt colours belong on the 2D drawings,
  not here, where they read as decoration.

LIGHTING AND BACKGROUND
  Three-point studio: key high and forward at roughly 40 degrees off the firing axis, fill at
  about one third key intensity from the opposite side, and a rim light behind to separate the
  track from the background.
  Background: flat neutral, either near-white (RGB about 245) or near-black (about 25). Pick ONE
  and use it for the whole set. No gradients, no floor reflections, no environment imagery.
  No depth of field. Blurring the far end of a 1.8 m track hides the brake, which is a
  component, not bokeh.

OUTPUT
  1920 x 1080 minimum, PNG, no watermark, no dimension annotations, no Fusion UI.
  Same background, same materials, same lighting rig across all seven. If one shot needs a
  different setup to work, the set is inconsistent and the shot is wrong.

THE SEVEN SHOTS

1. hero_open.png
   Three-quarter view from the muzzle end, camera roughly 30 degrees above the stator plane and
   35 degrees off-axis, whole machine in frame with a small margin. This is the lead image on
   every page. The track, both cassettes and the sled must all be legible in one look.

2. track_stator.png
   Near-side elevation along -y, orthographic or a long lens to keep the 1800 mm track from
   converging. Enclosure and near cassette hidden so the stator belts run uninterrupted from
   x=0 to x=1296. This shot exists to show that the stator is ironless and continuous.

3. sled_detail.png
   Close on the sled alone at mid-stroke, roughly x=650, three-quarter from above. The 12 mm
   airgap between the opposed Halbach arrays is the subject: frame so that gap is near the
   centre and clearly a gap. Include the four rollers and the guide rails they run in.

4. magazine_feed.png
   Looking down the -x direction from the muzzle toward the breech, both cassettes visible
   flanking the track, one satellite part-way onto the sled cradle. Shows the transverse feed,
   which is the part of the architecture people misread most often.

5. brake.png
   Close on x=1530 to 1740, the two tapered pole plates and the ring spring stop. Light so the
   entry taper is visible in profile, because that taper is the 200 g deceleration limiter and
   is the whole reason the brake looks the way it does.

6. espa_interface.png
   Aft three-quarter on the ring flange: 460 mm outer diameter, 400 mm bolt circle, 24 holes,
   four gussets. Frame so the bolt pattern is countable.

7. envelope_closed.png
   The ONLY enclosure-on shot. Plain side elevation, orthographic, whole machine. This one
   exists to show the 1839 mm closed length honestly against the ESPA Grande class limit of
   about 1270 mm. Do not flatter it with an angle that foreshortens the length.

WHAT NOT TO DO
  No motion blur, lens flare, sparks, exhaust, or starfield backgrounds.
  No cutaway sections unless asked: they need a defined cut plane and a stated reason.
  Do not hide the roller channels or guide rails to tidy the silhouette. They are flagged in
  cad/parameters.json as an open CAD defect (G3-D2) and a render that omits them would be
  showing a machine that does not exist.
```

---

## After the renders come back

Drop them into `cad/renders/` **using the existing filenames** where they correspond, because
`README.md`, `wiki/Home.md` and `docs/index.html` all reference them by absolute
`raw.githubusercontent.com` URL. Replacing in place updates every surface at once. New
filenames mean editing four files and are only worth it when the shot is genuinely new.

| New shot | Replaces |
|---|---|
| `hero_open.png` | `interior_open.png` |
| `sled_detail.png` | `seq2_midstroke.png` |
| `envelope_closed.png` | `exterior_closed.png` |
| `espa_interface.png` | `exterior_aft_mounting.png` |
| `track_stator.png`, `magazine_feed.png`, `brake.png` | new, need link edits |

**A new CAD generation is not a picture change.** `analysis/mass_properties.py` reads the STEP
solids and the sled mass sets the exit velocity. If the geometry moved at all, re-run it and
follow the propagation rule before quoting any number, exactly as P15 was handled. Add the
generation to `cad/CHANGELOG_CAD.md` in the existing format.
