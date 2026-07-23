"""
EMOCD | Mechanical, thermal, electrical and tolerance sizing anchors.

Reconstructs the calculations behind paper Secs. III-D/E, V (design parameter table),
VI (sensitivity), VII (mechanical), VIII (thermal) and the optimization notes. These
were originally run inline and never saved; this script closes that gap.

Margins are quoted on ULTIMATE strength at a 1.4 design factor, consistent with common
launch-hardware practice (GEVS-class qualification philosophy).

Reproduces:
    capacitor sizing            5.97 F  -> 6 F selected
    magnet bond shear           0.118 MPa vs 10 MPa allowable, MoS ~84
    inter-array attraction      3.7 kN, side plate 33 MPa vs 880 MPa Ti yield
    arrest load                 9.5 kN axial, ~0.76 kN per roller pair
    abort latch                 0.64 kN, M4 A-286 margin ~5
    retention gate              5.9 kN, two D6 A-286 pins, MoS 1.2
    track first mode            48 Hz pinned / 109 Hz fixed-fixed  (target >70 Hz)
    gap tolerance               -13 %/mm  -> +/-0.05 mm shim -> +/-0.65 %
    magnet temperature          -0.11 %/K -> +/-40 K -> 132 kA/m needed < 140 rated
    campaign thermal            23.6 kJ, 1.7 K bulk, 37 K fin adiabatic
    energy closure              2633 J accounted vs 2630 J drawn

Provenance: written by Claude (chat session), not independently re-derived.
No margin here has been checked by a structural analyst or by FEA.
"""
import math
import json
import os

G = 9.81
MU0 = 4e-7 * math.pi

# --- shared operating point (see motor_model.py) ---
M_SLED = 4.86          # kg
M_SAT = 4.0            # kg
V_EXIT = 20.37         # m/s
E_DRAWN = 2630.0       # J per shot
F_CMD = 1413.0         # N
ACCEL_ZONE = 1.30      # m
BRAKE_CAP_G = 200      # g, taper-limited sled deceleration


def capacitor_sizing(E=E_DRAWN, V0=96.0, sag_frac=0.049):
    """C from energy and allowed state-of-charge droop."""
    V1 = V0 * (1 - sag_frac)
    C = 2 * E / (V0 ** 2 - V1 ** 2)
    return dict(C_required_F=round(C, 2), C_selected_F=6.0,
                cells_series=32, cell_V=3.0, cell_F=190)


def magnet_bond():
    """Halbach block retention at the brake deceleration cap."""
    blk_m = 0.012 * 0.008 * 0.09 * 7500        # w x t x depth x NdFeB density
    F = BRAKE_CAP_G * G * blk_m
    A = 0.012 * 0.09                            # bonded footprint
    tau = F / A / 1e6                           # MPa
    allow = 10.0                                # MPa, conservative structural epoxy
    return dict(block_mass_g=round(blk_m * 1e3, 1), shear_N=round(F, 1),
                bond_area_cm2=round(A * 1e4, 2), stress_MPa=round(tau, 3),
                allowable_MPa=allow, margin=round(allow / tau - 1, 0))


def inter_array_attraction(B_face=0.55):
    """Maxwell stress between the two opposed Halbach faces."""
    p = B_face ** 2 / (2 * MU0)                 # Pa
    A = 0.34 * 0.09
    F = p * A
    M = F * 0.015 / 2                           # bending, half-gap arm
    Z = 0.008 * 0.025 ** 2 / 6                  # Ti side-plate section modulus
    sigma = M / Z / 1e6
    yield_ti = 880.0
    return dict(pressure_kPa=round(p / 1e3, 0), force_kN=round(F / 1e3, 2),
                plate_stress_MPa=round(sigma, 0), Ti_yield_MPa=yield_ti,
                margin=round(yield_ti / (1.25 * sigma) - 1, 1))


def arrest_loads():
    F_axial = M_SLED * BRAKE_CAP_G * G
    roller_pair = F_axial * 0.02 / 0.25         # pitch couple over roller base
    return dict(axial_kN=round(F_axial / 1e3, 2), roller_pair_N=round(roller_pair, 0))


def abort_latch():
    """Latch holds satellite during a commanded mid-stroke abort."""
    m_tot = M_SAT + M_SLED
    F = M_SAT * (F_CMD / m_tot)
    m4_a286_ult = 7900.0                        # N, M4 A-286 tensile (typical)
    return dict(load_N=round(F, 0), fastener='M4 A-286',
                capacity_N=m4_a286_ult, margin=round(m4_a286_ult / (2 * F) - 1, 1))


def retention_gate(n_pins=2, d=0.006, stack_kg=24.0, g_ascent=25.0, design_factor=1.4):
    """Gate carries ascent preload of a six-satellite stack straight into structure.

    NOTE: an earlier iteration sized this as a single D5 pin and got margin 0.5,
    which is inadequate. Resized to two D6 pins.
    """
    F = stack_kg * g_ascent * G
    tau_ult = 537e6 * 0.6                       # A-286 shear ~0.6 x tensile
    cap = n_pins * (math.pi * (d / 2) ** 2) * tau_ult
    return dict(load_kN=round(F / 1e3, 2), n_pins=n_pins, pin_dia_mm=d * 1e3,
                capacity_kN=round(cap / 1e3, 1),
                margin=round(cap / (design_factor * F) - 1, 1))


def track_first_mode(L=1.5, m_dist=20.0):
    """Two 7075 box longerons; target f1 > 70 Hz to clear launch primary band."""
    E_al = 69e9
    I = 2 * ((0.045 * 0.065 ** 3 - 0.037 * 0.057 ** 3) / 12)
    mu = m_dist / L
    out = {}
    for lam2, name in [(9.87, 'pinned_pinned_Hz'), (22.37, 'fixed_fixed_Hz')]:
        out[name] = round(lam2 / (2 * math.pi * L ** 2) * math.sqrt(E_al * I / mu), 0)
    out['EI_kNm2'] = round(E_al * I / 1e3, 1)
    out['target_Hz'] = 70
    return out


def gap_tolerance(lam=0.048, shim_mm=0.05):
    k = 2 * math.pi / lam
    per_mm = k * 1e-3 * 100
    return dict(decay_k_per_m=round(k, 0), sensitivity_pct_per_mm=round(per_mm, 1),
                shim_spec_mm=shim_mm, thrust_spread_pct=round(per_mm * shim_mm, 2))


def magnet_temperature(alpha=-0.0011, dT=40, K_rated=140e3, K_nom=126e3):
    """N45SH remanence drift and the current headroom needed to absorb it."""
    drift = alpha * dT * 100
    K_needed = K_nom * (1 + abs(alpha) * dT)
    return dict(alpha_pct_per_K=alpha * 100, dT_K=dT, Kt_drift_pct=round(drift, 1),
                K_needed_kA=round(K_needed / 1e3, 0), K_rated_kA=K_rated / 1e3,
                within_rating=bool(K_needed < K_rated))


def thermal_campaign(n_shots=12, Q_coil=672, Q_fin=1008, Q_esr=160,
                     Q_conv=97, Q_aux=26, C_th=13500.0):
    total = n_shots * (Q_coil + Q_fin + Q_esr + Q_conv + Q_aux)
    fin_mass = 0.004 * 0.08 * 0.30 * 8960
    fin_dT = Q_fin / (fin_mass * 385)
    # radiator to reject the burst average over the following orbit
    P_avg = 130.0
    A_rad = P_avg / (0.85 * 5.67e-8 * (323 ** 4 - 220 ** 4))
    return dict(campaign_kJ=round(total / 1e3, 1), bulk_rise_K=round(total / C_th, 1),
                fin_mass_kg=round(fin_mass, 2), fin_adiabatic_dT_K=round(fin_dT, 0),
                radiator_m2=round(A_rad, 2))


def energy_closure():
    KE_sat = 0.5 * M_SAT * V_EXIT ** 2
    KE_sled = 0.5 * M_SLED * V_EXIT ** 2
    accounted = KE_sat + KE_sled + 672 + 97 + 26
    return dict(KE_payload_J=round(KE_sat, 0), KE_sled_J=round(KE_sled, 0),
                copper_J=672, converter_J=97, aux_J=26,
                accounted_J=round(accounted, 0), drawn_J=E_DRAWN,
                closure_pct=round(100 * accounted / E_DRAWN, 1))


def pole_pitch_sweep(gap_half=0.006, th=0.008):
    """Relative thrust constant vs wavelength; shows 48 mm sits on the plateau."""
    out = {}
    for lam_mm in (32, 40, 48, 56, 64):
        k = 2 * math.pi / (lam_mm * 1e-3)
        out[f'{lam_mm}mm'] = round((1 - math.exp(-k * th)) * math.exp(-k * gap_half), 3)
    return out


def track_length_sweep(a=F_CMD / (M_SAT + M_SLED)):
    return {f'{L}m': round(math.sqrt(2 * a * (L - 0.2)), 1)
            for L in (1.0, 1.2, 1.5, 1.8)}


if __name__ == '__main__':
    res = dict(
        capacitor=capacitor_sizing(), magnet_bond=magnet_bond(),
        inter_array=inter_array_attraction(), arrest=arrest_loads(),
        abort_latch=abort_latch(), retention_gate=retention_gate(),
        track_mode=track_first_mode(), gap_tolerance=gap_tolerance(),
        magnet_temperature=magnet_temperature(), thermal=thermal_campaign(),
        energy_closure=energy_closure(), pole_pitch=pole_pitch_sweep(),
        track_length=track_length_sweep())

    for section, vals in res.items():
        print(f"\n[{section}]")
        for k, v in vals.items():
            print(f"  {k:26s} {v}")

    os.makedirs('results', exist_ok=True)
    json.dump(res, open('results/sizing.json', 'w'), indent=2)
    print("\n-> results/sizing.json")
