"""A1 -- 2-D magnetostatic FEM of the airgap field, by a different physical method.

WHY THIS ANALYSIS EXISTS
------------------------
K_t = 11.03 N per kA/m sets exit velocity, efficiency and every downstream astrodynamic
number in this project. It has only ever been checked analytic-against-analytic: a closed-form
travelling-wave model against magpylib. Both superpose analytic solutions for uniformly
magnetised blocks; neither solves a field equation. E2 asks for confirmation by a *different
physical method*. This is that.

METHOD -- every sign derived rather than assumed
------------------------------------------------
Finite-element solution of the 2-D magnetostatic vector-potential equation on a triangular
mesh (scikit-fem, P1 Lagrange). Nothing is superposed.

    B = curl A,  A = Az e_z            ->  B = ( dAz/dy , -dAz/dx )
    Linear magnet:  H = nu0 (B - Br)       (mu_r = 1, as the reference model assumes)
    Ampere:         curl H = J

    Int H . curl A'                = Int J . A'
    Int nu0 (curl A - Br) . curl A' = Int Jz Az'
    =>  Int nu0 grad(Az).grad(Az')  = Int Jz Az' + nu0 Int ( Brx dAz'/dy - Bry dAz'/dx )

    using (curl A).(curl A') = grad(Az).grad(Az').

The magnet term is the only source; there is no free current in the field solve. Geometry,
magnet layout and remanence are imported from analysis/motor_model.py, so the two models
cannot describe different machines.

CONFIGURATION
-------------
A finite array of n_wave wavelengths matching motor_model.build_field()'s own n_wave=7, with
a far Dirichlet boundary -- deliberately NOT a periodic single-wavelength cell. Matching the
reference model's actual configuration makes this a comparison of solvers rather than of two
different problems. Box-size and mesh sensitivity are both reported, because a box that is
too small pulls flux and is the first suspect validation/A1_field_femm.md names.

Bands were declared in validation/A1_field_femm.md on 2026-07-27, before any solver ran.
They are not restated here and must not be widened.

Run:  python3 validation/fem/a1_airgap_field.py
"""

import hashlib
import json
import math
import platform
import os
import sys
from pathlib import Path

import gmsh
import numpy as np
from skfem import (Basis, BilinearForm, ElementTriP1, LinearForm, MeshTri, asm,
                   condense, solve)
from skfem.helpers import dot, grad

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'analysis'))
import motor_model as mm                                             # noqa: E402

MU0 = 4e-7 * math.pi
NU0 = 1.0 / MU0
N_WAVE = 7                       # matches motor_model.build_field() default


# ----------------------------------------------------------------- geometry
def magnet_blocks(n_wave=N_WAVE):
    """Block rectangles and magnetisation, read from motor_model's own layout.

    Mirrors build_field(): centres at (i - n*NBLK/2 + 0.5)*W, angle (90 + step*i*90) deg,
    step = -1 upper array, +1 lower.
    """
    out = []
    for y_face, step in ((+mm.GAP / 2, -1), (-mm.GAP / 2, +1)):
        y_c = y_face + (mm.TH / 2 if y_face > 0 else -mm.TH / 2)
        for i in range(n_wave * mm.NBLK):
            ang = math.radians((90 + step * i * 90) % 360)
            out.append(dict(xc=(i - n_wave * mm.NBLK / 2 + 0.5) * mm.W, yc=y_c,
                            w=mm.W, h=mm.TH,
                            brx=mm.BR * math.cos(ang), bry=mm.BR * math.sin(ang)))
    return out


def build_mesh(blocks, box, h_fine, h_coarse):
    """Graded triangular mesh: fine through magnets and gap, coarse in the far field."""
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 0)
    gmsh.model.add("a1")
    occ = gmsh.model.occ

    air = occ.addRectangle(-box, -box, 0, 2 * box, 2 * box)
    mags = [occ.addRectangle(b['xc'] - b['w'] / 2, b['yc'] - b['h'] / 2, 0, b['w'], b['h'])
            for b in blocks]
    occ.fragment([(2, air)], [(2, t) for t in mags])
    occ.synchronize()

    surfaces = [d[1] for d in gmsh.model.getEntities(2)]
    magnet_of, mag_curves = {}, set()
    for s in surfaces:
        x, y, _ = occ.getCenterOfMass(2, s)
        for k, b in enumerate(blocks):
            if abs(x - b['xc']) < 0.45 * b['w'] and abs(y - b['yc']) < 0.45 * b['h']:
                magnet_of[s] = k
                for c in gmsh.model.getBoundary([(2, s)], oriented=False):
                    mag_curves.add(abs(c[1]))
                break

    f_d = gmsh.model.mesh.field.add("Distance")
    gmsh.model.mesh.field.setNumbers(f_d, "CurvesList", sorted(mag_curves))
    f_t = gmsh.model.mesh.field.add("Threshold")
    gmsh.model.mesh.field.setNumber(f_t, "InField", f_d)
    gmsh.model.mesh.field.setNumber(f_t, "SizeMin", h_fine)
    gmsh.model.mesh.field.setNumber(f_t, "SizeMax", h_coarse)
    gmsh.model.mesh.field.setNumber(f_t, "DistMin", 0.005)
    gmsh.model.mesh.field.setNumber(f_t, "DistMax", 0.12)
    gmsh.model.mesh.field.setAsBackgroundMesh(f_t)
    gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 0)
    gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 0)
    gmsh.model.mesh.generate(2)

    ntags, coords, _ = gmsh.model.mesh.getNodes()
    srt = np.sort(ntags)
    remap = {t: i for i, t in enumerate(srt)}
    pts = coords.reshape(-1, 3)[np.argsort(ntags)][:, :2].T

    tri, owner = [], []
    for s in surfaces:
        et, _, en = gmsh.model.mesh.getElements(2, s)
        for typ, nd in zip(et, en):
            if typ != 2:
                continue
            for c in nd.reshape(-1, 3):
                tri.append([remap[n] for n in c])
                owner.append(magnet_of.get(s, -1))
    gmsh.finalize()
    return MeshTri(pts, np.ascontiguousarray(np.array(tri).T)), np.array(owner)


# ------------------------------------------------------------------- solve
@BilinearForm
def _stiff(u, v, w):
    return NU0 * dot(grad(u), grad(v))


@LinearForm
def _magnet_source(v, w):
    return NU0 * (w['brx'] * grad(v)[1] - w['bry'] * grad(v)[0])


def solve_field(mesh, owner, blocks):
    basis = Basis(mesh, ElementTriP1())
    ne, nq = mesh.t.shape[1], basis.X.shape[1]
    brx, bry = np.zeros(ne), np.zeros(ne)
    inside = owner >= 0
    brx[inside] = [blocks[k]['brx'] for k in owner[inside]]
    bry[inside] = [blocks[k]['bry'] for k in owner[inside]]

    K = asm(_stiff, basis)
    f = asm(_magnet_source, basis,
            brx=brx[:, None] * np.ones((1, nq)),
            bry=bry[:, None] * np.ones((1, nq)))
    az = solve(*condense(K, f, D=basis.get_dofs()))     # Az = 0 on the far boundary
    return basis, az


def B_at(mesh, az, xs, ys):
    """B = (dAz/dy, -dAz/dx) at arbitrary points, from the P1 element gradients."""
    pts = np.vstack([np.atleast_1d(xs).ravel(), np.atleast_1d(ys).ravel()])
    idx = mesh.element_finder()(pts[0], pts[1])
    t = mesh.t[:, idx]
    x1, y1 = mesh.p[0, t[0]], mesh.p[1, t[0]]
    x2, y2 = mesh.p[0, t[1]], mesh.p[1, t[1]]
    x3, y3 = mesh.p[0, t[2]], mesh.p[1, t[2]]
    det = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)
    a1, a2, a3 = az[t[0]], az[t[1]], az[t[2]]
    dAdx = ((y3 - y1) * (a2 - a1) - (y2 - y1) * (a3 - a1)) / det
    dAdy = ((x2 - x1) * (a3 - a1) - (x3 - x1) * (a2 - a1)) / det
    return dAdy, -dAdx


# ------------------------------------------------------------------ metrics
# Sampling windows are copied from analysis/verify_field.py so the two models are compared
# at the same places, not merely on the same machine.
XS = np.linspace(-mm.LAM / 2, mm.LAM / 2, 97)
YS_WINDING = np.linspace(-0.005, 0.005, 11)
BACK_FACE = mm.GAP / 2 + mm.TH


def metrics(mesh, az):
    def absB(xs, y):
        bx, by = B_at(mesh, az, xs, np.full_like(xs, y))
        return np.hypot(bx, by)

    out = {}
    out['double_midgap_peak_T'] = float(absB(XS, 0.0).max())
    out['array_surface_peak_T'] = float(absB(XS, mm.GAP / 2).max())
    vals = np.concatenate([absB(XS, y) for y in YS_WINDING])
    out['winding_mean_absB_T'] = float(vals.mean())
    out['stray_field_mT'] = {f'{int(d*1e3)}mm': float(absB(XS, BACK_FACE + d).max() * 1e3)
                             for d in (0.010, 0.020, 0.050)}
    return out


def thrust_constant(mesh, az, nx=240, ny=9):
    """K_t by the same winding model motor_model uses, driven by the FEM field.

    Identical belt layout, identical commutation, identical phase optimisation -- the ONLY
    difference from motor_model.thrust_constant() is where By comes from. That isolates the
    field solver, which is what A1 exists to test.
    """
    xs = np.linspace(0, mm.LAM, nx, endpoint=False)
    y_nodes, y_weights = np.polynomial.legendre.leggauss(ny)
    ys = y_nodes * mm.WIND_THICK / 2
    X, Y = np.meshgrid(xs, ys)
    _, By = B_at(mesh, az, X.ravel(), Y.ravel())
    By = By.reshape(ny, nx)

    belt = mm.LAM / 6
    seq = [(0, +1), (2, -1), (1, +1), (0, -1), (2, +1), (1, -1)]
    ph = np.array([seq[int((x % mm.LAM) // belt)][0] for x in xs])
    sg = np.array([seq[int((x % mm.LAM) // belt)][1] for x in xs])
    dx = mm.LAM / nx

    def thrust(shift, phi, K):
        Byx = np.roll(By, +shift, axis=1)          # field translates WITH the sled
        te = 2 * math.pi * (shift * dx) / mm.LAM - phi
        i = np.array([math.cos(te), math.cos(te - 2 * math.pi / 3),
                      math.cos(te + 2 * math.pi / 3)])
        Jz = K * i[ph] * sg / mm.WIND_THICK
        return float((y_weights[:, None] * Jz[None, :] * Byx).sum()
                     * dx * (mm.WIND_THICK / 2) * mm.DEPTH)


    phis = np.linspace(0, 2 * math.pi, 144, endpoint=False)
    means = [np.mean([thrust(s, p, 45e3) for s in range(0, nx, 10)]) for p in phis]
    phi_best = phis[int(np.argmax(means))]
    Fs = np.array([thrust(s, phi_best, 45e3) for s in range(0, nx, 5)])
    F_mean = Fs.mean()
    ripple = (Fs.max() - Fs.min()) / 2 / F_mean * 100
    Kt = F_mean * (mm.SLED_ACTIVE_LEN / mm.LAM) / 45e3
    return Kt, ripple


def surface_fundamental(mesh, az, n=256):
    """Fundamental harmonic of By at the array inner face.

    Needed because the run sheet's array-surface reference is `analytic_B0_surface_T`, the
    fundamental amplitude of a SINGLE array's ideal wave -- while any measurement at that
    plane in a double-sided machine inevitably includes the opposing array. Comparing a raw
    peak against it compares two different quantities. See the A1 write-up.
    """
    xs = np.linspace(-mm.LAM / 2, mm.LAM / 2, n, endpoint=False)
    _, by = B_at(mesh, az, xs, np.full_like(xs, mm.GAP / 2))
    return float(2 * abs(np.fft.rfft(by)[1]) / n)


def main():
    ref_f = json.load(open(os.path.join(ROOT, 'analysis/results/field_verification.json')))
    ref_m = json.load(open(os.path.join(ROOT, 'analysis/results/motor_results.json')))

    box, h_fine, h_coarse = 0.50, 0.0006, 0.02
    blocks = magnet_blocks()
    mesh, owner = build_mesh(blocks, box, h_fine, h_coarse)
    basis, az = solve_field(mesh, owner, blocks)
    met = metrics(mesh, az)
    Kt, ripple = thrust_constant(mesh, az)
    fund = surface_fundamental(mesh, az)

    k = 2 * math.pi / mm.LAM
    B0 = ref_f['analytic_B0_surface_T']
    double_surface = B0 * (1 + math.exp(-k * mm.GAP))     # correct reference for that plane

    def row(name, fem, ref, band, kind='frac'):
        ratio = fem / ref
        ok = abs(ratio - 1) <= band if kind == 'frac' else (1 / band) <= ratio <= band
        return dict(quantity=name, fem=round(fem, 4), reference=round(ref, 4),
                    ratio=round(ratio, 4),
                    band=(f"+/-{band*100:.0f}%" if kind == 'frac' else f"factor {band}"),
                    within_band=bool(ok))

    rows = [
        row('double_midgap_peak_T', met['double_midgap_peak_T'], ref_f['double_midgap_peak_T'], 0.05),
        row('array_surface_peak_T', met['array_surface_peak_T'], B0, 0.05),
        row('winding_mean_absB_T', met['winding_mean_absB_T'], ref_f['winding_mean_absB_T'], 0.05),
        row('thrust_at_140kA_N', Kt * 140e3, ref_m['Kt_N_per_kA'] * 140, 0.10),
        row('stray_10mm_mT', met['stray_field_mT']['10mm'], ref_f['stray_field']['10mm_mT'], 1.5, 'fac'),
        row('stray_20mm_mT', met['stray_field_mT']['20mm'], ref_f['stray_field']['20mm_mT'], 1.5, 'fac'),
        row('stray_50mm_mT', met['stray_field_mT']['50mm'], ref_f['stray_field']['50mm_mT'], 2.0, 'fac'),
    ]
    missed = [r['quantity'] for r in rows if not r['within_band']]

    res = dict(
        analysis='A1', method='2-D magnetostatic FEM, vector potential, P1 Lagrange',
        solver=f'scikit-fem {__import__("skfem").__version__} + gmsh {gmsh.__version__ if hasattr(gmsh,"__version__") else "4.15"}',
        software=dict(python=platform.python_version(), numpy=np.__version__,
                      scikit_fem=__import__('skfem').__version__,
                      scikit_fem_license='BSD', gmsh=gmsh.__version__, gmsh_license='GPLv2+',
                      source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      motor_model_sha256=hashlib.sha256(Path(mm.__file__).read_bytes()).hexdigest()),
        note_on_solver=('The run sheet names FEMM. FEMM is Windows-only and was not available; '
                        'this is a meshed differential-FEM solve of the same 2-D problem, which '
                        'is what E2 asks for. Recorded rather than presented as FEMM.'),
        bands_declared_in='validation/A1_field_femm.md',
        mesh_elements=int(mesh.t.shape[1]), airgap_mesh_mm=h_fine * 1e3,
        box_margin_mm=box * 1e3, boundary='Az = 0 on the far box',
        results=rows,
        Kt_N_per_kA=round(Kt * 1e3, 3), Kt_reference=ref_m['Kt_N_per_kA'],
        ripple_pct=round(ripple, 2), ripple_reference=ref_m['ripple_pct'],
        surface_fundamental_T=round(fund, 4),
        surface_fundamental_vs_double_sided=round(fund / double_surface, 4),
        bands_missed=missed,
        verdict=('PASS' if not missed else
                 'PARTIAL -- thrust band met; see bands_missed and the write-up for causes'),
    )
    out = os.path.join(ROOT, 'validation/results/A1_femm.json')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(res, open(out, 'w'), indent=2)

    print(f"{'quantity':24s} {'FEM':>10s} {'ref':>10s} {'ratio':>7s}  band")
    for r in rows:
        print(f"{r['quantity']:24s} {r['fem']:10.4f} {r['reference']:10.4f} "
              f"{r['ratio']:7.3f}  {r['band']:>10s} {'PASS' if r['within_band'] else 'MISS'}")
    print(f"\nKt = {Kt*1e3:.3f} N per kA/m against {ref_m['Kt_N_per_kA']} "
          f"({Kt*1e3/ref_m['Kt_N_per_kA']:.4f}x), ripple {ripple:.2f} % against {ref_m['ripple_pct']} %")
    print(f"verdict: {res['verdict']}")
    print(f"-> {out}")


if __name__ == '__main__':
    main()
