"""A14: EMI scoping against the bands declared in validation/A14_emi_scoping.md.

The bands were committed at c274473, before this file existed. Do not widen them here.

WHAT THIS COMPUTES
------------------
Two coupling paths, at the three payload stations `cad/parameters.json` actually puts the
satellite at, plus the comms question and the coilgun comparator that the 2021 architecture
decision rested on.

REFERENCE PLANES -- the easy thing to get wrong
-----------------------------------------------
`motor_model` works in a convention where **y is the gap-normal direction**; `cad/parameters.json`
calls the same axis z. They are the same axis and this file uses the CAD naming.

The two fields do NOT share a reference plane and must not be given one:

- the **armature-reaction (AC)** field is produced by the winding, which straddles z = 0, so its
  decay is measured from z = 0;
- the **static Halbach** field is produced by the arrays, whose back face is at z = 14 mm, which
  is why `verify_field.py` probes at `GAP/2 + TH + d`.

Both are therefore evaluated at absolute stations z = 20, 70, 120 mm and the decay is applied
from each field's own source plane. Quoting one at the other's standoff would be wrong by a
factor of e^(k*14mm) = 6.2.

METHOD
------
The AC field uses the same harmonic decomposition of the belt winding that
`analysis/drive_electrical.py` uses for the inductance, so the two cannot fork. Harmonic n of a
sheet current of amplitude K_n produces a field of amplitude mu0*K_n/2 at the sheet, decaying as
exp(-n*k*z) into free space.

The static field is taken from magpylib via `motor_model.build_field()`, which is what
`verify_field.py` and A1 use.

LIMITATIONS
-----------
- The victim loop is a declared 10 cm^2 area at a declared station; it is a stand-in for a
  payload PCB, not a model of one.
- Free space. No shielding, no enclosure, no payload structure. That makes every EMF here an
  upper bound, which is the useful direction.
- Band 8's ratio uses the same crude infinite-wire model for BOTH machines so the comparison is
  symmetric. VOLLEY's three-phase fields largely cancel at distance, so that model OVERstates
  VOLLEY and the true ratio is larger than reported. The absolute VOLLEY figure is the
  harmonic-decay one, not the wire one.
- Nothing here is measured. E12 closes on T-6.

Run:  python3 validation/emi/emi_scoping.py
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'analysis'))

import motor_model as mm                                    # noqa: E402
import drive_electrical as de                               # noqa: E402

RESULTS = os.path.join(ROOT, 'validation', 'results')
ANALYSIS_RESULTS = os.path.join(ROOT, 'analysis', 'results')
MU0 = 4e-7 * math.pi
C_LIGHT = 2.99792458e8

# --- declared in A14, not chosen here ----------------------------------------
A_LOOP = 1e-3                       # m^2, the declared 10 cm^2 victim loop
STATIONS = {                        # CAD z, absolute from the thrust line
    'payload_near_face': 0.020,
    'payload_com': 0.070,
    'payload_far_face': 0.120}
ARRAY_BACK_FACE = mm.GAP / 2 + mm.TH                        # z = 0.014 m
STRUCT_LEN = 1.839                  # m, KILL_CRITERIA section 2
T_RISE_SIC = (20e-9, 50e-9)
BANDS_RF = dict(UHF=400e6, GPS_L1=1575.42e6, S_band=2200e6)
B_EARTH = 45e-6                     # T
MAG_FULL_SCALE = 100e-6             # T, class figure -- see A14's comparator table
V_ANALOG, V_DIGITAL = 50e-3, 400e-3

# --- Feng et al. coilgun comparator, per stage (ADR-003) ---------------------
CG_E_TOTAL, CG_V, CG_STAGES, CG_L = 6.91e6, 16e3, 3, 30e-6


def ac_field_at(z, K_amp):
    """Armature-reaction field amplitude at height z above the winding plane."""
    k = 2 * math.pi / mm.LAM
    orders, amps = de.sheet_harmonics()
    return sum(MU0 * (K_amp * a) / 2 * math.exp(-n * k * z)
               for n, a in zip(orders, amps))


def static_field_at(z, nx=240):
    """Peak static Halbach field at height z, via the same magpylib model A1 uses."""
    field = mm.build_field()
    xs = np.linspace(0, mm.LAM, nx, endpoint=False)
    pts = np.stack([xs, np.full(nx, z), np.zeros(nx)], axis=1)
    return float(np.linalg.norm(field.getB(pts), axis=1).max())


def wire_emf(current, freq, r, area=A_LOOP):
    """Infinite-wire coupling, used ONLY for the symmetric band-8 ratio."""
    B = MU0 * current / (2 * math.pi * r)
    return area * B * 2 * math.pi * freq, B


def main():
    with open(os.path.join(ANALYSIS_RESULTS, 'drive_electrical.json'),
              encoding='utf-8') as f:
        d = json.load(f)

    I_m = d['phase_current_peak_A']
    f_e = d['commutation_Hz']
    L_s = d['phase_inductance_H']
    K_amp = mm.K_RATED * 0.9
    ripple20 = d['ripple']['20000']
    ripple40 = d['ripple']['40000']

    # --- coupling at each payload station ------------------------------------
    stations = {}
    for name, z in STATIONS.items():
        B_ac = ac_field_at(z, K_amp)
        B_static = static_field_at(z)
        emf_comm = A_LOOP * B_ac * 2 * math.pi * f_e
        # triangular ripple: dB/dt = dB / (half switching period)
        emf_pwm = {}
        for tag, rip, f_sw in (('20kHz', ripple20, 20e3), ('40kHz', ripple40, 40e3)):
            dB = B_ac * (rip['pp_A'] / I_m)
            emf_pwm[tag] = A_LOOP * dB * 2 * f_sw
        stations[name] = dict(
            z_m=z, behind_array_back_face_mm=(z - ARRAY_BACK_FACE) * 1e3,
            B_ac_T=B_ac, B_static_T=B_static,
            B_static_mT=B_static * 1e3,
            static_x_earth=B_static / B_EARTH,
            static_x_magnetometer_fullscale=B_static / MAG_FULL_SCALE,
            emf_commutation_V=emf_comm, emf_pwm_V=emf_pwm)

    # --- comms ---------------------------------------------------------------
    knees = sorted(1 / (math.pi * t) for t in T_RISE_SIC)
    comms = {}
    for name, f_band in BANDS_RF.items():
        margins = [40 * math.log10(f_band / kn) for kn in knees]
        comms[name] = dict(f_Hz=f_band, knee_lo_Hz=knees[0], knee_hi_Hz=knees[1],
                           margin_dB_min=min(margins), margin_dB_max=max(margins))
    rad_eff = {int(f): (STRUCT_LEN / (C_LIGHT / f)) ** 2 for f in (20e3, 40e3)}

    # --- band 8: the comparator the 2021 decision rested on -------------------
    E_stage = CG_E_TOTAL / CG_STAGES
    C_stage = 2 * E_stage / CG_V ** 2
    I_cg = CG_V * math.sqrt(C_stage / CG_L)
    t_quarter = (math.pi / 2) * math.sqrt(CG_L * C_stage)
    f_cg = 1 / (4 * t_quarter)
    r_cmp = 0.30
    emf_cg, B_cg = wire_emf(I_cg, f_cg, r_cmp)
    emf_v, B_v = wire_emf(I_m, f_e, r_cmp)
    ratio = emf_cg / emf_v

    near = stations['payload_near_face']
    worst_emf = max(near['emf_commutation_V'], *near['emf_pwm_V'].values())

    verdicts = [
        dict(band=1, question='EMF from commutation, 10 cm2 loop at the nearest face',
             limit_V=V_ANALOG, result_V=near['emf_commutation_V'],
             verdict='PASS' if near['emf_commutation_V'] < V_ANALOG else 'FAIL'),
        dict(band=2, question='EMF from 20 kHz PWM ripple, same loop and station',
             limit_V=V_ANALOG, result_V=near['emf_pwm_V']['20kHz'],
             verdict='PASS' if near['emf_pwm_V']['20kHz'] < V_ANALOG else 'FAIL'),
        dict(band=3, question='Worst of the above against the digital threshold',
             limit_V=V_DIGITAL, result_V=worst_emf,
             verdict='PASS' if worst_emf < V_DIGITAL else 'FAIL'),
        dict(band=4, question='Static field at the nearest face vs magnetometer full scale',
             limit_T=MAG_FULL_SCALE, result_T=near['B_static_T'],
             verdict='PASS' if near['B_static_T'] <= MAG_FULL_SCALE else 'FAIL'),
        dict(band=5, question='Static field at CoM and far face, multiples of Earth',
             verdict='VOID; no materials list exists for a magnetisation threshold',
             com_x_earth=stations['payload_com']['static_x_earth'],
             far_x_earth=stations['payload_far_face']['static_x_earth']),
        dict(band=6, question='Spectral margin below the SiC knee at every comms band',
             limit_dB=40, result_dB=min(c['margin_dB_min'] for c in comms.values()),
             verdict='PASS' if min(c['margin_dB_min'] for c in comms.values()) > 40 else 'FAIL'),
        dict(band=7, question='Radiation efficiency of the structure at the fundamental',
             limit=1e-6, result=max(rad_eff.values()),
             verdict='PASS' if max(rad_eff.values()) < 1e-6 else 'FAIL'),
        dict(band=8, question='Coilgun-to-VOLLEY induced-EMF ratio at equal geometry',
             limit=100.0, result=ratio, verdict='PASS' if ratio > 100 else 'FAIL'),
    ]

    res = dict(
        analysis='A14', method='scoping calculation from analysis/results/, no measurement',
        bands_declared_commit='c274473',
        inputs=dict(phase_current_peak_A=I_m, phase_inductance_H=L_s,
                    commutation_Hz=f_e, K_amplitude_A_per_m=K_amp,
                    loop_area_m2=A_LOOP, array_back_face_z_m=ARRAY_BACK_FACE),
        stations=stations, comms=comms, radiation_efficiency=rad_eff,
        coilgun=dict(stage_capacitance_F=C_stage, stage_peak_current_A=I_cg,
                     equivalent_Hz=f_cg, comparison_radius_m=r_cmp,
                     B_coilgun_T=B_cg, B_volley_T=B_v,
                     emf_coilgun_V=emf_cg, emf_volley_V=emf_v, ratio=ratio),
        bands=verdicts)

    print("A14 EMI scoping -- bands declared at c274473\n")
    print(f"{'station':<20}{'behind':>8}{'B_ac':>12}{'B_static':>12}{'EMF comm':>11}{'EMF 20k':>10}")
    for name, s in stations.items():
        print(f"{name:<20}{s['behind_array_back_face_mm']:7.0f}mm"
              f"{s['B_ac_T']*1e3:10.4f}mT{s['B_static_mT']:10.3f}mT"
              f"{s['emf_commutation_V']*1e3:9.3f}mV{s['emf_pwm_V']['20kHz']*1e3:8.3f}mV")
    print()
    for name, s in stations.items():
        print(f"  {name:<20} static = {s['static_x_earth']:8.1f}x Earth, "
              f"{s['static_x_magnetometer_fullscale']:8.1f}x magnetometer full scale")
    print()
    print(f"  SiC knee {knees[0]/1e6:.1f}-{knees[1]/1e6:.1f} MHz")
    for name, c in comms.items():
        print(f"    {name:<8}{c['f_Hz']/1e6:8.1f} MHz  {c['margin_dB_min']:.0f}-{c['margin_dB_max']:.0f} dB below")
    print(f"  radiation efficiency 20/40 kHz: "
          f"{rad_eff[20000]:.2e} / {rad_eff[40000]:.2e}")
    print()
    print(f"  coilgun stage: {I_cg/1e3:.0f} kA, {f_cg:.0f} Hz equivalent")
    print(f"  at r = {r_cmp} m: coilgun {emf_cg*1e3:.1f} mV vs VOLLEY {emf_v*1e3:.3f} mV"
          f"  -> ratio {ratio:.0f}x")
    print("\n  VERDICTS")
    for b in verdicts:
        print(f"    band {b['band']}: {b['verdict']:<12} {b['question']}")

    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, 'A14_emi.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=2)
        f.write('\n')
    print(f"\nwrote {path}")


if __name__ == '__main__':
    main()
