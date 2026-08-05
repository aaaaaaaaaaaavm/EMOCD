"""Winding inductance, phase current, and what the inverter actually has to synthesise.

WHY THIS EXISTS
---------------
`paper.tex` Sec. on the drive states that the 20-40 kHz switching frequency is "high enough
that the current ripple is filtered by the winding inductance". Nothing in this repository
computes that inductance. There is no henry anywhere in `analysis/`, and until this script
there was no phase current either: `motor_model.shot()` integrates in SHEET current (A/m)
and its `I_peak` is the DC-link current drawn from the bank, not the current in a conductor.

That gap is wider than one missing number. A sheet-current model is turns-invariant by
construction -- the same 126 kA/m can be wound as many turns at low current or few turns at
high current -- so the winding inductance is genuinely undetermined by the model. L scales as
N^2, phase current as 1/N, and the stored field energy is invariant.

WHAT CLOSES IT
--------------
The bus does. The inverter has to synthesise the phase voltage the machine demands at rated
speed, and it has 96 V (90.9 V after the 5.3 % sag) to do it with. That fixes the turns count,
and therefore fixes L, the phase current and the resistance, without any new assumption about
how the coils are wound.

The algebra collapses because every term in the required phase voltage scales as 1/I_m:

    V_req * I_m = (2/3) * sqrt((P_mech + P_cu)^2 + (2 w W_field)^2)

with every quantity on the right already fixed by the shot. So I_m follows from the available
voltage alone, and L, R and the ripple follow from I_m.

METHOD FOR THE FIELD ENERGY
---------------------------
The armature-reaction energy is computed from the *same* belt-winding distribution
`motor_model.thrust_constant()` integrates against, not from a sinusoidal idealisation. The
distribution is Fourier-decomposed over one wavelength; each spatial harmonic n radiates a
field decaying as exp(-n k |y|) into free space on both sides (the machine is ironless and
NdFeB is magnetically close to air), giving energy per unit sheet area

    u_n = mu0 * K_n^2 / (8 n k)

and higher harmonics contribute less because they decay faster. Summing over harmonics is
what distinguishes this from a one-line sinusoidal estimate.

LIMITATIONS
-----------
- Two-dimensional. End-turn inductance is not included and is not small for a short machine;
  this is a LOWER bound on L, so the ripple below is an UPPER bound.
- The energised length is the full 1.30 m acceleration zone, matching how `motor_model`
  computes copper loss. A segmented stator energising only the active section would cut both
  L and R roughly in proportion. That decision is open as P29.
- Ripple uses the worst-case two-level expression dI_pp = V_dc / (4 L f_sw) at a modulation
  duty of one half. Space-vector modulation does somewhat better.
- Nothing here is measured.

Run:  python3 analysis/drive_electrical.py
"""
import json
import math
import os

import numpy as np

import motor_model as mm

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

F_SW = (20e3, 40e3)          # Hz, the switching range paper.tex specifies
SQRT3 = math.sqrt(3.0)
MU0 = 4e-7 * math.pi


def sheet_harmonics(nx=2400):
    """Amplitudes of the spatial harmonics of the belt winding's sheet current.

    Rebuilds the same six-sector phase/sign pattern `motor_model.thrust_constant` uses, at
    unit sheet-current amplitude, and returns (harmonic order, amplitude) pairs.
    """
    xs = np.linspace(0, mm.LAM, nx, endpoint=False)
    belt = mm.LAM / 6
    seq = [(0, +1), (2, -1), (1, +1), (0, -1), (2, +1), (1, -1)]
    ph = np.array([seq[int((x % mm.LAM) // belt)][0] for x in xs])
    sg = np.array([seq[int((x % mm.LAM) // belt)][1] for x in xs])
    i = np.array([1.0, math.cos(-2 * math.pi / 3), math.cos(2 * math.pi / 3)])
    k_of_x = i[ph] * sg                          # unit-amplitude sheet current vs position

    spec = np.fft.rfft(k_of_x) / nx
    orders, amps = [], []
    for n in range(1, 25):
        a = 2.0 * abs(spec[n])
        if a > 1e-6:
            orders.append(n)
            amps.append(a)
    return np.array(orders), np.array(amps)


def field_energy(K_amp, length, depth=None):
    """Armature-reaction magnetic energy, summed over the winding's spatial harmonics."""
    depth = mm.DEPTH if depth is None else depth
    k = 2 * math.pi / mm.LAM
    orders, amps = sheet_harmonics()
    u = sum(MU0 * (K_amp * a) ** 2 / (8 * n * k) for n, a in zip(orders, amps))
    return u * length * depth, dict(zip(orders.tolist(), amps.tolist()))


def solve(sag_pct=None):
    """Close the drive design against the bus voltage and report the electrical point."""
    with open(os.path.join(RESULTS, 'motor_results.json'), encoding='utf-8') as f:
        m = json.load(f)
    shot = m['shot']

    v_exit = shot['v_exit']
    F = shot['F_cmd']
    t_pulse = shot['t_ms'] / 1000.0
    P_cu = shot['Q_copper'] / t_pulse                  # W, mean ohmic dissipation
    P_mech = F * v_exit                                # W, at exit, the worst case
    sag = shot['sag_pct'] if sag_pct is None else sag_pct
    V_bus = mm.V0 * (1 - sag / 100.0)
    V_avail = V_bus / SQRT3                            # peak phase, space-vector limit

    K_amp = mm.K_RATED * 0.9
    W_field, harmonics = field_energy(K_amp, mm.ACCEL_ZONE)

    f_e = v_exit / mm.LAM                              # commutation fundamental
    w_e = 2 * math.pi * f_e

    # V_req * I_m is invariant under the turns count; see the module docstring.
    VA = (2.0 / 3.0) * math.hypot(P_mech + P_cu, 2 * w_e * W_field)
    I_m = VA / V_avail

    L_s = 4 * W_field / (3 * I_m ** 2)
    R_ph = 2 * P_cu / (3 * I_m ** 2)
    E_m = 2 * P_mech / (3 * I_m)
    tau = L_s / R_ph

    ripple = {}
    for f_sw in F_SW:
        pp = mm.V0 / (4 * L_s * f_sw)
        rms = pp / (2 * SQRT3)
        ripple[int(f_sw)] = dict(
            pp_A=pp, pct_of_peak=100 * pp / I_m, rms_A=rms,
            extra_copper_W=3 * rms ** 2 * R_ph,
            extra_copper_J=3 * rms ** 2 * R_ph * t_pulse)

    return dict(
        method='armature-reaction field energy, harmonic sum; turns closed on the bus voltage',
        inputs=dict(v_exit=v_exit, F_cmd=F, P_mech_W=P_mech, P_copper_W=P_cu,
                    sag_pct=sag, V_bus_sagged=V_bus, V_phase_available_peak=V_avail,
                    K_amplitude_A_per_m=K_amp, energised_length_m=mm.ACCEL_ZONE),
        field_energy_J=W_field,
        sheet_harmonics={str(k): v for k, v in harmonics.items()},
        commutation_Hz=f_e,
        phase_current_peak_A=I_m,
        phase_inductance_H=L_s,
        phase_resistance_ohm=R_ph,
        back_emf_peak_V=E_m,
        resistive_drop_V=I_m * R_ph,
        reactive_drop_V=w_e * L_s * I_m,
        electrical_tau_s=tau,
        modulation_index_at_exit=1.0,
        didt_commutation_A_per_s=w_e * I_m,
        didt_pwm_A_per_s=mm.V0 / L_s,
        ripple=ripple,
        copper_loss_J=shot['Q_copper'])


def main():
    r = solve()
    print("Drive electrical design point (closed on the bus, not assumed)\n")
    print(f"  armature field energy      {r['field_energy_J']:.3f} J")
    print(f"  commutation fundamental    {r['commutation_Hz']:.1f} Hz")
    print(f"  available peak phase V     {r['inputs']['V_phase_available_peak']:.2f} V"
          f"  (bus {r['inputs']['V_bus_sagged']:.1f} V after sag)")
    print(f"  peak phase current         {r['phase_current_peak_A']:.1f} A")
    print(f"  phase inductance           {r['phase_inductance_H']*1e6:.2f} uH")
    print(f"  phase resistance           {r['phase_resistance_ohm']*1e3:.2f} mohm")
    print(f"  electrical time constant   {r['electrical_tau_s']*1e3:.3f} ms")
    print(f"  back-EMF / IR / wLI        {r['back_emf_peak_V']:.2f} / "
          f"{r['resistive_drop_V']:.2f} / {r['reactive_drop_V']:.2f} V")
    print(f"  modulation index at exit   {r['modulation_index_at_exit']:.2f}")
    print()
    for f_sw, d in sorted(r['ripple'].items()):
        print(f"  ripple at {f_sw/1000:.0f} kHz  {d['pp_A']:6.1f} A pp "
              f"({d['pct_of_peak']:.1f} % of peak), adds {d['extra_copper_J']:.2f} J "
              f"of {r['copper_loss_J']:.1f} J")
    print()
    print(f"  dI/dt commutation          {r['didt_commutation_A_per_s']:.3e} A/s")
    print(f"  dI/dt PWM (V/L)            {r['didt_pwm_A_per_s']:.3e} A/s")

    path = os.path.join(RESULTS, 'drive_electrical.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(r, f, indent=2)
        f.write('\n')
    print(f"\nwrote {path}")


if __name__ == '__main__':
    main()
