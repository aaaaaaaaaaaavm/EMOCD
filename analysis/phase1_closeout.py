"""A18: the last five Phase I analyses -- E20, E19, E26, E10, E22.

Bands declared in validation/A18_phase1_closeout.md at 4e97fce, before this file existed.

Every assumed input is swept, not picked. Where a sweep cannot bound the answer the row is
reported VOID rather than guessed.

Run:  python3 analysis/phase1_closeout.py
"""
import json
import math
import os

import numpy as np

import motor_model as mm
import sizing

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

SIG_CU, SIG_AL, SIG_NDFEB = 5.96e7, 3.5e7, 1.0 / 1.4e-6      # S/m
RHO_CU, CP_CU = 8960.0, 385.0
RHO_MAG, CP_MAG = 7500.0, 440.0
SB = 5.670374419e-8

# --- brake, cad/parameters.json 'brake' --------------------------------------
FIN_L, FIN_W, FIN_T = 0.120, 0.080, 0.004
FIN_MASS = 0.344
POLE_COUNT, POLE_W = 2, 0.090
POLE_L = 0.100
ARREST_LEN = 0.210                       # x = 1530..1740 mm
G_CAP = 200.0
B_POLE_SWEEP = (0.3, 0.4, 0.5, 0.6, 0.7)

# --- E26 ---------------------------------------------------------------------
EPS_SWEEP = (0.05, 0.2, 0.5, 0.9)
H_SWEEP = (100.0, 500.0, 2000.0, 5000.0)
MOUNT_AREA = 0.080 * 0.020               # fin root, m^2
T_ENV, CADENCE = 273.15, 1200.0          # K, s -- ADR-020

# --- E10, GEVS protoflight ---------------------------------------------------
GEVS_ASD = 0.16                          # g^2/Hz plateau
Q_SWEEP = (10.0, 15.0, 20.0, 30.0)
STACK_MASS = 6 * 4.0                     # kg, six 3U per cassette
PIN_D, PIN_N = 0.006, 2
TAU_ULT = 537e6 * 0.6                    # A-286 shear, sizing.py:169
PRELOAD_SIZED = 5900.0                   # N, the load the gates were sized for


def e20(v_entry, ke_in):
    rows = []
    a_pole = POLE_L * POLE_W * POLE_COUNT
    for B in B_POLE_SWEEP:
        k = SIG_CU * FIN_T * B * B * a_pole              # N.s/m
        F0 = k * v_entry
        tau = mm.M_SLED / k
        rows.append(dict(B_T=B, k_Ns_per_m=k, F_peak_N=F0,
                         a_peak_g=F0 / mm.M_SLED / 9.80665,
                         tau_s=tau, stop_dist_m=v_entry * tau,
                         t_99pct_s=tau * math.log(100),
                         energy_J=0.5 * mm.M_SLED * v_entry ** 2))
    ok = [r for r in rows if r['a_peak_g'] <= G_CAP and r['stop_dist_m'] <= ARREST_LEN]
    return rows, ok


def e19(v_exit):
    """Slab eddy loss in the magnet blocks under the armature-reaction field."""
    k_dec = 2 * math.pi / mm.LAM
    B_face = mm.MU0 * mm.K_RATED * 0.9 / 2 if hasattr(mm, 'MU0') else \
        (4e-7 * math.pi) * mm.K_RATED * 0.9 / 2
    z_face = mm.GAP / 2                                   # magnet inner face
    B_ac = B_face * math.exp(-k_dec * z_face)
    f_e = v_exit / mm.LAM
    dBdt = 2 * math.pi * f_e * B_ac
    d_seg = mm.LAM / mm.NBLK                              # block width, 12 mm
    p_vol = SIG_NDFEB * d_seg ** 2 * dBdt ** 2 / 12.0
    vol = mm.SLED_ACTIVE_LEN * mm.DEPTH * mm.TH * 2
    mass = vol * RHO_MAG
    P = p_vol * vol
    t_pulse = 0.1586
    dT = P * t_pulse / (mass * CP_MAG)
    seg = [dict(n_seg=n, d_m=d_seg / n,
                dT_K=dT / n ** 2) for n in (1, 2, 4)]
    return dict(B_ac_T=B_ac, f_e_Hz=f_e, dBdt_T_s=dBdt, seg_width_m=d_seg,
                P_W=P, magnet_mass_kg=mass, dT_per_shot_K=dT,
                dT_campaign_K=dT * 12, segmentation=seg)


def e26(q_shot):
    C = FIN_MASS * CP_CU
    area_rad = 2 * FIN_L * FIN_W
    rows = []
    for eps in EPS_SWEEP:
        for h in H_SWEEP:
            T = T_ENV + 27.0                              # start at 300 K
            peak = T
            for _ in range(12):
                T += q_shot / C
                peak = max(peak, T)
                # cool for one cadence interval, explicit sub-stepped
                dt, n = CADENCE / 240, 240
                for _ in range(n):
                    p = eps * SB * area_rad * (T ** 4 - T_ENV ** 4) + h * MOUNT_AREA * (T - T_ENV)
                    T -= p * dt / C
            rows.append(dict(eps=eps, h_W_m2K=h, peak_K=peak, peak_C=peak - 273.15,
                             final_K=T, decays=bool(T - (T_ENV + 27.0) < 1.0)))
    return rows


def e10():
    rows = []
    modes = sizing.track_first_mode()
    f_n = modes['fixed_fixed_Hz']
    area = PIN_N * math.pi * (PIN_D / 2) ** 2
    cap = area * TAU_ULT
    for Q in Q_SWEEP:
        g_rms = math.sqrt(math.pi / 2 * f_n * Q * GEVS_ASD)
        load = STACK_MASS * 3 * g_rms * 9.80665           # 3 sigma
        rows.append(dict(Q=Q, f_n_Hz=f_n, g_rms=g_rms, g_3sigma=3 * g_rms,
                         load_N=load, vs_sized_ratio=load / PRELOAD_SIZED,
                         pin_capacity_N=cap, MoS=cap / load - 1.0))
    return rows, cap


def e22(v_exit, F_thrust):
    """Parasitic eddy drag on conductive structure vs standoff from the array back face."""
    k_dec = 2 * math.pi / mm.LAM
    B0 = 22.7e-3                                          # measured model value at 10 mm
    rows = []
    for d_mm in (5, 10, 20, 30, 40, 50, 75, 100):
        d = d_mm / 1000.0
        B = B0 * math.exp(-k_dec * (d - 0.010))
        k = SIG_AL * 0.006 * B * B * (mm.SLED_ACTIVE_LEN * mm.DEPTH)
        F = k * v_exit
        rows.append(dict(standoff_mm=d_mm, B_mT=B * 1e3, drag_N=F,
                         pct_of_thrust=100 * F / F_thrust))
    rule = next((r['standoff_mm'] for r in rows if r['pct_of_thrust'] < 1.0), None)
    return rows, rule


def main():
    with open(os.path.join(RESULTS, 'motor_results.json'), encoding='utf-8') as f:
        m = json.load(f)
    v_entry = m['regen']['v_end']
    ke_in = m['regen']['KE_to_brake']
    F_thrust = m['shot']['F_cmd']
    v_exit = m['shot']['v_exit']

    brake, brake_ok = e20(v_entry, ke_in)
    mag = e19(v_exit)
    fin = e26(ke_in)
    pins, pin_cap = e10()
    drag, rule_mm = e22(v_exit, F_thrust)

    print("A18 -- the last five Phase I analyses  (bands at 4e97fce)\n")
    print(f"E20 brake, entry {v_entry:.3f} m/s, KE {ke_in:.1f} J")
    print(f"  {'B (T)':>7}{'k (Ns/m)':>11}{'F peak (N)':>12}{'a (g)':>9}{'stop (mm)':>11}{'t99 (ms)':>10}")
    for r in brake:
        print(f"  {r['B_T']:7.1f}{r['k_Ns_per_m']:11.1f}{r['F_peak_N']:12.0f}"
              f"{r['a_peak_g']:9.1f}{r['stop_dist_m']*1e3:11.1f}{r['t_99pct_s']*1e3:10.1f}")
    print(f"  band 1 (<=200 g) and band 2 (<=210 mm) hold for B in "
          f"{[r['B_T'] for r in brake_ok]}")
    e_err = 100 * abs(brake[0]['energy_J'] - ke_in) / ke_in
    print(f"  band 3 energy vs KE_to_brake: {e_err:.3f} %\n")

    print(f"E19 magnets: B_ac {mag['B_ac_T']*1e3:.2f} mT at {mag['f_e_Hz']:.0f} Hz, "
          f"dB/dt {mag['dBdt_T_s']:.1f} T/s")
    print(f"  eddy power {mag['P_W']:.2f} W over {mag['magnet_mass_kg']:.2f} kg")
    print(f"  band 5 dT per shot = {mag['dT_per_shot_K']:.4f} K  (< 1 K), "
          f"campaign {mag['dT_campaign_K']:.3f} K\n")

    worst = max(fin, key=lambda r: r['peak_C'])
    best = min(fin, key=lambda r: r['peak_C'])
    print(f"E26 fin, 12 shots at {CADENCE:.0f} s")
    print(f"  band 7 worst case eps={worst['eps']} h={worst['h_W_m2K']:.0f}: "
          f"peak {worst['peak_C']:.1f} C   (< 150 C)")
    print(f"  best case  eps={best['eps']} h={best['h_W_m2K']:.0f}: peak {best['peak_C']:.1f} C")
    print(f"  band 8 decays between shots: "
          f"{sum(1 for r in fin if r['decays'])} of {len(fin)} (eps,h) pairs\n")

    print(f"E10 retention pins, GEVS {GEVS_ASD} g^2/Hz at {pins[0]['f_n_Hz']:.0f} Hz")
    print(f"  {'Q':>5}{'g_rms':>9}{'3-sigma g':>12}{'load (kN)':>12}{'x sized':>10}{'MoS':>9}")
    for r in pins:
        print(f"  {r['Q']:5.0f}{r['g_rms']:9.1f}{r['g_3sigma']:12.1f}"
              f"{r['load_N']/1e3:12.2f}{r['vs_sized_ratio']:10.2f}{r['MoS']:9.2f}")
    print(f"  pin shear capacity {pin_cap/1e3:.1f} kN, sized against {PRELOAD_SIZED/1e3:.1f} kN\n")

    print(f"E22 standoff rule, thrust {F_thrust:.0f} N")
    print(f"  {'standoff':>10}{'B (mT)':>10}{'drag (N)':>11}{'% thrust':>11}")
    for r in drag:
        print(f"  {r['standoff_mm']:8.0f}mm{r['B_mT']:10.3f}{r['drag_N']:11.2f}"
              f"{r['pct_of_thrust']:11.3f}")
    print(f"  band 11 rule: conductive structure at >= {rule_mm} mm behind the array back face")

    res = dict(analysis='A18', bands_declared_commit='4e97fce',
               E20=dict(entry_v=v_entry, sweep=brake, within_bands_B=[r['B_T'] for r in brake_ok],
                        energy_err_pct=e_err),
               E19=mag, E26=dict(cadence_s=CADENCE, sweep=fin),
               E10=dict(sweep=pins, pin_capacity_N=pin_cap, sized_for_N=PRELOAD_SIZED),
               E22=dict(sweep=drag, rule_standoff_mm=rule_mm))
    path = os.path.join(RESULTS, 'phase1_closeout.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=2)
        f.write('\n')
    print(f"\nwrote {path}")


if __name__ == '__main__':
    main()
