# STL meshes: derived, not authoritative

GitHub renders `.stl` in an interactive viewer and does **not** render STEP, so these two
meshes exist purely so the geometry can be spun in a browser. Click either file above.

**These are derived artifacts.** `../step/gen3/*.step` is the master geometry and
`../parameters.json` is the source of truth for every dimension. A mesh is a faceted
approximation, never measure anything off it.

| File | Source | Mesh size | Triangles | Bounding box |
|---|---|---|---|---|
| `EMOCD_Assembly_Gen3.stl` | `../step/gen3/EMOCD_Assembly_Gen3.step` | 40 mm max | 50,692 | 1995x 530x 940 mm |
| `EMOCD_Sled_Gen3.stl` | `../step/gen3/EMOCD_Sled_Gen3.step` | 8 mm max | 23,332 | 616x 172x 140 mm |

Regenerate with:

```python
import gmsh
gmsh.initialize()
gmsh.option.setNumber('Mesh.CharacteristicLengthMax', 40)   # 8 for the sled
gmsh.option.setNumber('Mesh.CharacteristicLengthMin', 10)   # 2 for the sled
gmsh.option.setNumber('Mesh.Binary', 1)
gmsh.merge('../step/gen3/EMOCD_Assembly_Gen3.step')
gmsh.model.mesh.generate(2)
gmsh.write('EMOCD_Assembly_Gen3.stl')
gmsh.finalize()
```

`pip install gmsh` (its OCC reader handles STEP). On a headless Linux box it also needs
`libglu1-mesa libxft2 libxinerama1 libxcursor1 libfontconfig1`.

Each mesh was checked against its STEP source by bounding box on generation. The sled
matches exactly at 616x 172x 140 mm. The assembly measures 1995 mm in X against a
point-cloud bound of 1998 mm on the STEP, the 3 mm is spline control points lying outside
the surface they define, which is expected and harmless.

**One thing the assembly mesh exposes:** its X range is −188 to 1810 mm, where
`parameters.json` records the installed envelope as −32 to 1807 mm. Something sits 156 mm
further aft than the recorded envelope. See `../../OPEN_PROBLEMS.md` P14.
