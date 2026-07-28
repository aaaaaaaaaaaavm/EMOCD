"""
EMOCD analysis A4 -- chassis plate under inter-array attraction.

Extracts one 488x140x6 chassis plate from cad/step/gen3/EMOCD_Sled_Gen3.step, meshes it
with quadratic tets, and writes two CalculiX decks that BRACKET the real support condition:

    pinned  -- webs restrain out-of-plane only   (lower bound on stiffness)
    clamped -- webs restrain all three DOF       (upper bound on stiffness)

The truth is between them. Reporting one number would be a choice dressed as a result.

Loads and geometry come from the repo, not from this file:
    120 kPa Maxwell pressure, 3.67 kN per array   analysis/results/sizing.json inter_array
    magnet footprint 340 x 90 mm                  cad/parameters.json sled
    web lines at |y| = 48..54 mm from centreline  cad/parameters.json sled chassis_web_y_*
Units: mm, N, MPa, tonne.
"""
import gmsh, os, sys

E_TI, NU_TI, RHO_TI = 113800.0, 0.342, 4.43e-9      # Ti-6Al-4V, MPa / - / tonne per mm^3
P_MAXWELL = 0.120                                    # MPa == 120 kPa (sizing.py inter_array)
MAG_LEN, MAG_WID = 340.0, 90.0
WEB_IN, WEB_OUT = 48.0, 54.0
HERE = os.path.dirname(os.path.abspath(__file__))

gmsh.initialize(); gmsh.option.setNumber('General.Terminal', 0)
gmsh.model.occ.importShapes(os.path.join(HERE, '..', '..', 'cad', 'step', 'gen3',
                                         'EMOCD_Sled_Gen3.step'))
gmsh.model.occ.synchronize()
keep = None
for dim, tag in gmsh.model.getEntities(3):
    b = gmsh.model.getBoundingBox(dim, tag)
    if sorted(round(b[i+3]-b[i], 1) for i in range(3)) == [6.0, 140.0, 488.0] and keep is None:
        keep, BB = tag, b
    else:
        gmsh.model.occ.remove([(dim, tag)], recursive=True)
gmsh.model.occ.synchronize()
gmsh.option.setNumber('Mesh.CharacteristicLengthMax', 6.0)
gmsh.option.setNumber('Mesh.CharacteristicLengthMin', 2.0)
gmsh.option.setNumber('Mesh.ElementOrder', 2)
gmsh.model.mesh.generate(3)

ntags, ncoord, _ = gmsh.model.mesh.getNodes()
xyz = {int(t): ncoord[3*i:3*i+3] for i, t in enumerate(ntags)}
etypes, etags, enodes = gmsh.model.mesh.getElements(3)
tets = []
for et, tg, nd in zip(etypes, etags, enodes):
    if et == 11:
        # gmsh tet10 edge order is {0,1},{1,2},{2,0},{3,0},{3,2},{3,1}; CalculiX C3D10 wants
        # 5=(1,2) 6=(2,3) 7=(1,3) 8=(1,4) 9=(2,4) 10=(3,4). The last two are therefore
        # swapped relative to gmsh -- get this wrong and ccx reports a nonpositive jacobian
        # on every element, which is what happened on the first run.
        ORDER = [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]
        tets = [(int(tg[i]), [int(nd[10*i+j]) for j in ORDER]) for i in range(len(tg))]
gmsh.finalize()

ycen = (BB[1] + BB[4]) / 2.0                        # plate is offset in y; work from its centre
zlo, zhi = BB[2], BB[5]
xlo = BB[0]
mag_x0 = BB[3] - MAG_LEN                            # array runs to the muzzle end of the plate
sel = lambda n, ax, lo, hi: lo - 1e-6 <= xyz[n][ax] <= hi + 1e-6

loaded = [n for n in xyz if abs(xyz[n][2] - zlo) < 1e-6
          and sel(n, 0, mag_x0, BB[3]) and sel(n, 1, ycen - MAG_WID/2, ycen + MAG_WID/2)]
webs = [n for n in xyz if WEB_IN - 1e-6 <= abs(xyz[n][1] - ycen) <= WEB_OUT + 1e-6]
area = MAG_LEN * MAG_WID
force = P_MAXWELL * area
print('plate  x %.0f..%.0f  y %.0f..%.0f  z %.0f..%.0f  (centreline y=%.1f)'
      % (BB[0], BB[3], BB[1], BB[4], BB[2], BB[5], ycen))
print('load   %.0f N over %.0f x %.0f mm on the z=%.0f face, %d nodes'
      % (force, MAG_LEN, MAG_WID, zlo, len(loaded)))
print('webs   %d nodes at |y - centre| = %.0f..%.0f' % (len(webs), WEB_IN, WEB_OUT))
if not loaded or not webs:
    sys.exit('node selection failed')

for case, dofs in (('pinned', '3,3'), ('clamped', '1,3')):
    with open(os.path.join(HERE, 'plate_%s.inp' % case), 'w') as f:
        f.write('** EMOCD A4 -- chassis plate, %s webs\n*NODE, NSET=Nall\n' % case)
        for n, c in sorted(xyz.items()):
            f.write('%d, %.6f, %.6f, %.6f\n' % (n, c[0], c[1], c[2]))
        f.write('*ELEMENT, TYPE=C3D10, ELSET=Eall\n')
        for t, nd in tets:
            f.write('%d, %s\n' % (t, ', '.join(str(x) for x in nd)))
        f.write('*NSET, NSET=Nweb\n' + '\n'.join(', '.join(str(n) for n in webs[i:i+8])
                                                 for i in range(0, len(webs), 8)) + '\n')
        f.write('*NSET, NSET=Nload\n' + '\n'.join(', '.join(str(n) for n in loaded[i:i+8])
                                                  for i in range(0, len(loaded), 8)) + '\n')
        f.write('*MATERIAL, NAME=Ti6Al4V\n*ELASTIC\n%.1f, %.3f\n*DENSITY\n%.3e\n'
                % (E_TI, NU_TI, RHO_TI))
        f.write('*SOLID SECTION, ELSET=Eall, MATERIAL=Ti6Al4V\n')
        f.write('*BOUNDARY\nNweb, %s\n' % dofs)
        f.write('*STEP\n*STATIC\n*CLOAD\nNload, 3, %.6f\n' % (-force / len(loaded)))
        f.write('*NODE PRINT, NSET=Nall\nU\n*EL PRINT, ELSET=Eall\nS\n*END STEP\n')
    print('wrote plate_%s.inp' % case)
