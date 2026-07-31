"""
VOLLEY | Winding-resolved thrust constant, shot simulation, closed-loop dispersion.

This is the script behind the paper's headline performance numbers. It supersedes
the earlier lumped surface-current model (see legacy/c3_c4_em.py), which assumed an
effective airgap field of 0.62 T and produced 22.4 m/s. That model omitted the
one-half traveling-wave factor inherent to synchronous extraction; this one resolves
the three-phase belt winding directly against the verified field.

Reproduces (paper Secs. IV-B, V-A):
    thrust constant Kt          11.22 N per kA/m
    force ripple                +/-1.26 % (6th harmonic)
    exit velocity (3U)          16.54 m/s at 10.7 g
    pulse duration              157 ms
    bank SoC sag                5.2 %
    energy drawn                2.80 kJ
    payload KE                  547 J  -> 20 % electrical-to-payload
    copper heat                 828 J/shot
    closed-loop dispersion      0.026 m/s (3 sigma) at a 16.2 m/s setpoint

IMPORTANT: the sled field must TRANSLATE with the sled (np.roll on the field array).
An early version held the field fixed while commutating the current, which produced
a near-zero mean thrust. If Kt comes out ~0, check that first.

Provenance: model output, not independently re-derived.

Efficiency is electrical-to-payload. It used to be quoted with the note that the sled's
kinetic energy "is dissipated in the arrest brake by design and is NOT recovered". The
first half was right and the second half was never argued: the 2025 decision established
that the motor cannot ARREST the sled, not that none of its energy can be taken back.
A11 asked the second question and regen_brake() below answers it -- about a quarter of
the sled's energy returns to the bank inside the existing envelope, and the eddy brake is
still required for the rest. The original caution came from a real error (a 2021 draft
credited 55 % regeneration, giving 40 %, corrected to 32 %), and crediting nothing was the
safe response to it rather than the correct one.
"""
import numpy as np
import magpylib as magpy
import math
import json
import os

# Outputs go next to this script, not next to whoever ran it. Every script here used to
# write to a cwd-relative "results/", so running one from the repository root created a
# SECOND, silently stale copy of its JSON at the root -- which is exactly what happened on
# 2026-07-30 and left a results/sizing.json carrying a superseded inter-array force. A
# duplicate that nothing regenerates is the defect class this repository logs twice
# already (P16, P19).
RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

# --- geometry / materials -----------------------------------------------------
LAM, NBLK, TH, GAP, DEPTH, BR = 0.048, 4, 0.008, 0.012, 0.09, 1.32
W = LAM / NBLK
SLED_ACTIVE_LEN = 0.34          # m, magnet array length along track
WIND_THICK = 0.010              # m, winding radial thickness
FILL = 0.60                     # copper fill factor
K_RATED = 140e3                 # A/m sheet current (pulse rating)
RHO_CU = 1.7e-8                 # ohm-m

# --- operating point ----------------------------------------------------------
M_SAT = 4.0                     # kg, 3U reference payload
M_SLED = 9.445                  # kg, measured from cad/step/gen3/EMOCD_Sled_Gen3.step
#                                 (P15). Superseded the 4.86 kg parametric estimate in
#                                 mass_properties.py on 2026-07-29, under the decision
#                                 rule declared in validation/A4_sled_structural.md
#                                 before A4 ran: at >= 6.80 kg the CAD mass wins and the
#                                 paper changes materially. A4 has since run and the
#                                 as-drawn plate passes all three bands, so nothing
#                                 structural forces a lighter chassis. This is the
#                                 as-drawn, unpocketed geometry -- a rib-stiffened
#                                 redesign could recover mass, and none has been
#                                 evaluated (P5, P8, E2).
ACCEL_ZONE = 1.30               # m
TRACK = 1.50                    # m (accel + 0.20 m coast-trim)
V_FLEET = 16.2                  # m/s, closed-loop fleet setpoint.
#                                 The servo has authority only below the open-loop
#                                 ceiling; above it, Kc saturates at K_RATED and the
#                                 Monte Carlo measures shortfall rather than dispersion.
#                                 Set at 98.2 % of the ceiling -- the same fraction the
#                                 superseded 20.0 m/s setpoint held against the old
#                                 20.37 m/s ceiling -- so the headroom argument behind
#                                 the dispersion claim is unchanged, not re-tuned.
C_BANK, V0 = 6.0, 96.0          # F, V
R_ESR = 0.012                   # ohm, bank equivalent series resistance.
#                                 The value the SPICE deck at validation/spice/ uses. It has
#                                 no current source: it reaches this repository through
#                                 docs/EMOCD_Computation_Results_C1-C10.md, which is
#                                 superseded, and no cell datasheet has been checked against
#                                 it. E17 stays open on that basis. What it is here for is
#                                 that omitting the term entirely was worse: A8-R found the
#                                 shot drawing 3 % more from the bank than this model
#                                 accounted for, and 12 mohm reproduces the gap to 1.3 %.
CONV_EFF = 0.95                 # power converter
P_AUX = 200.0                   # W


def build_field(n_wave=7):
    def arr(y_face, step):
        mags = []
        for i in range(n_wave * NBLK):
            x = (i - n_wave * NBLK / 2 + 0.5) * W
            ang = (90 + step * i * 90) % 360
            pol = [BR * np.cos(np.radians(ang)), BR * np.sin(np.radians(ang)), 0]
            y_c = y_face + (TH / 2 if y_face > 0 else -TH / 2)
            mags.append(magpy.magnet.Cuboid(polarization=pol,
                                            dimension=(W, TH, DEPTH),
                                            position=(x, y_c, 0)))
        return magpy.Collection(mags)
    return magpy.Collection([arr(+GAP / 2, -1), arr(-GAP / 2, +1)])


def thrust_constant(nx=240, ny=9, profile=False):
    """Direct Lorentz integration of a 3-phase belt winding against the real field."""
    field = build_field()
    xs = np.linspace(0, LAM, nx, endpoint=False)
    ys = np.linspace(-WIND_THICK / 2, WIND_THICK / 2, ny)
    X, Y = np.meshgrid(xs, ys)
    By = field.getB(np.stack([X.ravel(), Y.ravel(), np.zeros(X.size)], 1))[:, 1].reshape(ny, nx)

    belt = LAM / 6
    seq = [(0, +1), (2, -1), (1, +1), (0, -1), (2, +1), (1, -1)]
    ph = np.array([seq[int((x % LAM) // belt)][0] for x in xs])
    sg = np.array([seq[int((x % LAM) // belt)][1] for x in xs])
    dx, dy = LAM / nx, WIND_THICK / ny

    def thrust(shift, phi, K):
        Byx = np.roll(By, +shift, axis=1)          # field translates WITH the sled
        te = 2 * math.pi * (shift * dx) / LAM - phi
        i = np.array([math.cos(te), math.cos(te - 2 * math.pi / 3),
                      math.cos(te + 2 * math.pi / 3)])
        Jz = K * i[ph] * sg / WIND_THICK
        return float((Jz[None, :] * Byx).sum() * dx * dy * DEPTH)

    phis = np.linspace(0, 2 * math.pi, 144, endpoint=False)
    means = [np.mean([thrust(s, p, 45e3) for s in range(0, nx, 10)]) for p in phis]
    phi_best = phis[int(np.argmax(means))]
    Fs = np.array([thrust(s, phi_best, 45e3) for s in range(0, nx, 5)])
    F_mean = Fs.mean()
    ripple = (Fs.max() - Fs.min()) / 2 / F_mean * 100
    Kt = F_mean * (SLED_ACTIVE_LEN / LAM) / 45e3     # N per (A/m)
    if profile:
        # thrust over one wavelength of sled travel, scaled to the rated sheet current
        xs_prof = np.arange(0, nx, 5) * dx
        return Kt, ripple, xs_prof, Fs * (SLED_ACTIVE_LEN / LAM) * (K_RATED * 0.9 / 45e3)
    return Kt, ripple


class BankLimitError(RuntimeError):
    """The supercapacitor bank cannot source the power the shot demands.

    Raised rather than worked around. A bank that cannot deliver the shot is a design
    result, and the caller has to decide what to do about it; silently substituting a
    current the circuit cannot produce is how A10 nearly reported a working machine.
    """


def shot(Kt, K_lim=K_RATED, dt=1e-4, trace=False):
    """Integrate one shot: constant commanded force against bank sag + copper loss.

    trace=True additionally returns the time series (t, x, v, Vc, I) so figures can be
    drawn from this integrator rather than a second copy of it.
    """
    m = M_SAT + M_SLED
    F = 0.9 * Kt * K_lim
    J = (K_lim * 0.9) / WIND_THICK / FILL                     # A/m^2 in copper
    vol_cu = ACCEL_ZONE * DEPTH * WIND_THICK * FILL
    P_cu = RHO_CU * J * J * vol_cu
    x = v = t = E = Q = Q_esr = 0.0
    Vc, Imax = V0, 0.0
    hist = []
    while x < ACCEL_ZONE:
        v += F / m * dt
        x += v * dt
        t += dt
        P = F * v / CONV_EFF + P_cu + P_AUX
        # The load draws P at the bank TERMINAL, which sits R_ESR*I below the cell voltage,
        # so the current is not P/Vc. Solving P = (Vc - I*R)*I for the physical root:
        #     R I^2 - Vc I + P = 0  ->  I = (Vc - sqrt(Vc^2 - 4 R P)) / (2 R)
        # The energy leaving the capacitor is then Vc*I, not P: the difference is I^2*R
        # burned in the ESR, which is the term A8-R found missing.
        Vb = max(Vc, 40)
        disc = Vb * Vb - 4 * R_ESR * P
        if disc <= 0:
            # No real root: a source of EMF Vb behind R cannot deliver more than
            # Vb^2/(4R) into ANY load, and the shot is asking for more. This is a
            # physical impossibility, not a numerical edge case, so it raises.
            #
            # It used to fall back to P/Vb here, which is the current the load would
            # draw with no ESR at all. That silently turned "this bank cannot source
            # the shot" into a completed run with plausible numbers, and it made peak
            # current DECREASE with rising resistance. Found by A10. See P26.
            raise BankLimitError(
                f"bank cannot source {P/1e3:.1f} kW at Vc={Vb:.1f} V through "
                f"R_ESR={R_ESR*1e3:.0f} mohm: ceiling is Vb^2/4R = "
                f"{Vb*Vb/(4*R_ESR)/1e3:.1f} kW, reached at t={t*1e3:.1f} ms, "
                f"v={v:.2f} m/s, x={x*1e3:.0f} mm")
        I = (Vb - math.sqrt(disc)) / (2 * R_ESR)
        Imax = max(Imax, I)
        Vc -= I * dt / C_BANK
        E += Vb * I * dt
        Q += P_cu * dt
        Q_esr += I * I * R_ESR * dt
        if trace:
            hist.append((t, x, v, Vc, I))
    out = dict(F_cmd=F, v_exit=v, a_g=F / m / 9.81, t_ms=t * 1e3, I_peak=Imax,
                sag_pct=(1 - Vc / V0) * 100, E_drawn=E, Q_copper=Q, Q_esr=Q_esr,
                KE_payload=0.5 * M_SAT * v * v,
                eff_pct=0.5 * M_SAT * v * v / E * 100,
                J_Amm2=(K_lim * 0.9) / WIND_THICK / FILL / 1e6)
    if trace:
        out['trace'] = np.array(hist)          # columns: t, x, v, Vc, I
    return out


# --- regenerative braking after release (A11) ----------------------------------
S_REGEN = 0.240                 # m of added stator downstream of the 1500 mm release point.
#                                 The closed envelope is 1839 mm, so the arrest section is
#                                 339 mm; roughly 100 mm of it goes to the eddy fin and the
#                                 ring-spring stack. This is a packaging ASSUMPTION, not a
#                                 layout anyone has drawn -- see A11's "what this run cannot
#                                 settle". regen_brake(s=...) is the sweep handle.


def copper_coeff(length):
    """W per N^2 of braking force, for a stator section of the given energised length.

    Sheet current for a commanded force is K = F/(0.9*Kt) and current density is
    J = 0.9*K/(WIND_THICK*FILL), so J = F/(Kt*WIND_THICK*FILL) and P_cu = RHO_CU*J^2*vol.
    The length passed in is the copper that is ENERGISED, which for regeneration is the
    added section and not the 1.30 m acceleration winding the sled has already left.
    That choice is the one modelling decision in A11 that moves the answer, so it is a
    parameter here rather than a constant.
    """
    def coeff(Kt):
        vol = length * DEPTH * WIND_THICK * FILL
        return RHO_CU * vol / (Kt * WIND_THICK * FILL) ** 2
    return coeff


def regen_brake(Kt, v0, Vc0, s=S_REGEN, K_lim=K_RATED, energised=None, dt=1e-5):
    """Brake the sled regeneratively over s metres of stator, after payload release.

    The sled alone decelerates: the payload is gone, which is why this cannot move
    v_exit. Force is constant at the commanded sheet current, capped at K_lim by the
    same rating that bounds acceleration -- that inequality IS the 2025 arrest argument,
    and it is why the eddy brake survives this.

    Charging mirrors shot()'s discharge: the bank terminal sits R_ESR*I ABOVE the cell
    voltage when current flows in, so delivering P at the terminal means
        R I^2 + Vc I - P = 0  ->  I = (-Vc + sqrt(Vc^2 + 4 R P)) / (2 R)
    and the energy reaching the cell is Vc*I, not P. Omitting that would credit the ESR
    loss twice over: once on the way out, not at all on the way back.
    """
    m = M_SLED                                   # payload already released
    F = 0.9 * Kt * K_lim
    P_cu = copper_coeff(s if energised is None else energised)(Kt) * F * F
    v = v0                                       # from shot(), never a literal
    Vc = Vc0                                     # bank voltage the shot left behind
    x = t = W = Q = Q_esr = E_rec = 0.0
    Imax = 0.0
    while x < s and v > 0:
        dv = F / m * dt
        if dv > v:
            dv = v
        W += F * v * dt
        v -= dv
        x += v * dt
        t += dt
        Q += P_cu * dt
        P_term = (F * v - P_cu) * CONV_EFF - P_AUX
        if P_term > 0:
            I = (-Vc + math.sqrt(Vc * Vc + 4 * R_ESR * P_term)) / (2 * R_ESR)
            Imax = max(Imax, I)
            E_rec += Vc * I * dt
            Q_esr += I * I * R_ESR * dt
            Vc += I * dt / C_BANK
    KE0 = 0.5 * m * v0 * v0
    return dict(s_m=s, F_brake=F, K_kA=K_lim / 1e3, mult_of_rated=K_lim / K_RATED,
                W_mech=W, Q_copper=Q, Q_esr=Q_esr, E_recovered=E_rec,
                Q_converter=(W - Q) * (1 - CONV_EFF), Q_aux=P_AUX * t,
                t_ms=t * 1e3, v_end=v, I_peak=Imax,
                KE_sled_in=KE0, KE_to_brake=0.5 * m * v * v,
                frac_recovered_pct=E_rec / KE0 * 100)


def closed_loop_mc(Kt, n=800, v_target=V_FLEET, seed0=0):
    """Position-scheduled profile + coast-trim correction from photogate measurement."""
    m = M_SAT + M_SLED
    out = []
    for s in range(seed0, seed0 + n):
        r = np.random.default_rng(s)
        Ktf = Kt * (1 + r.normal(0, 0.008))       # magnet grade + gap tolerance
        mf = m * (1 + r.normal(0, 0.0067))        # mass tolerance
        x = v = 0.0
        dt = 2e-4
        while x < ACCEL_ZONE:
            v_plan = v_target * math.sqrt(max(x, 1e-6) / ACCEL_ZONE)
            Kc = min(max((mf * v_target ** 2 / (2 * ACCEL_ZONE)
                          + 3500 * (v_plan - v) * mf) / Ktf, 0), K_RATED)
            v += Ktf * Kc * (1 + r.normal(0, 0.005)) / mf * dt
            x += v * dt
        v_meas = v + r.normal(0, 0.008)           # 8 mm/s sensor sigma
        v += min(max(v_target - v_meas, -0.3), 0.3) + r.normal(0, 0.004)
        out.append(v)
    a = np.array(out)
    return dict(mean=float(a.mean()), sigma3=float(3 * a.std()), samples=a)


def payload_family(Kt, F_cmd):
    fam = {}
    for m_sat, cap, tag in [(1.3, 30, '1U'), (4, 25, '3U'), (8, 25, '6U'), (12, 25, '12U')]:
        a = min(F_cmd / (m_sat + M_SLED), cap * 9.81)
        fam[tag] = dict(v_exit=round(math.sqrt(2 * a * ACCEL_ZONE), 1), a_g=round(a / 9.81, 1))
    return fam


if __name__ == '__main__':
    Kt, ripple = thrust_constant()
    print(f"Kt = {Kt * 1e3:.2f} N per kA/m, ripple +/-{ripple:.2f} %")
    s = shot(Kt)
    for k, v in s.items():
        print(f"  {k:12s} {v:.3f}" if isinstance(v, float) else f"  {k:12s} {v}")
    mc = closed_loop_mc(Kt)
    print(f"closed-loop MC at {V_FLEET} m/s setpoint: "
          f"mean {mc['mean']:.3f} m/s, 3sigma {mc['sigma3']:.4f} m/s")
    if mc['mean'] < V_FLEET - 0.05:
        raise SystemExit(
            f"Servo saturated: mean {mc['mean']:.3f} < setpoint {V_FLEET}. "
            "V_FLEET must sit below the open-loop ceiling or the dispersion figure "
            "is measuring shortfall, not sensing noise.")
    fam = payload_family(Kt, s['F_cmd'])
    print("payload family:", fam)

    # A11. Regeneration runs off the shot's own end state -- exit velocity and the bank
    # voltage the shot left behind -- so it cannot be quoted against a stale operating
    # point, which is the failure P19 records.
    rg = regen_brake(Kt, s['v_exit'], V0 * (1 - s['sag_pct'] / 100))
    rg_pess = regen_brake(Kt, s['v_exit'], V0 * (1 - s['sag_pct'] / 100),
                          energised=ACCEL_ZONE)
    net_draw = s['E_drawn'] - rg['E_recovered']
    print(f"regen over {rg['s_m']*1e3:.0f} mm: {rg['E_recovered']:.1f} J recovered "
          f"({rg['frac_recovered_pct']:.1f} % of sled KE), {rg['KE_to_brake']:.0f} J still "
          f"to the brake, peak {rg['I_peak']:.0f} A")
    print(f"  efficiency {s['eff_pct']:.2f} % -> {s['KE_payload']/net_draw*100:.2f} % "
          f"(pessimistic copper convention: "
          f"{s['KE_payload']/(s['E_drawn']-rg_pess['E_recovered'])*100:.2f} %)")
    if abs(s['v_exit'] - shot(Kt)['v_exit']) > 1e-9:
        raise SystemExit("regen changed v_exit; it acts after release and must not.")

    res = dict(Kt_N_per_kA=round(Kt * 1e3, 2), ripple_pct=round(ripple, 2),
               K_rated_kA=K_RATED / 1e3,
               regen={k: round(v, 3) for k, v in rg.items()},
               regen_copper_pessimistic_J=round(rg_pess['Q_copper'], 1),
               regen_E_recovered_pessimistic_J=round(rg_pess['E_recovered'], 1),
               E_drawn_net_J=round(net_draw, 1),
               eff_net_pct=round(s['KE_payload'] / net_draw * 100, 2),
               shot={k: round(v, 3) for k, v in s.items()},
               v_fleet_setpoint=V_FLEET,
               closed_loop_mean=round(mc['mean'], 3),
               closed_loop_3sigma=round(mc['sigma3'], 4), family=fam)
    os.makedirs(RESULTS, exist_ok=True)
    json.dump(res, open(os.path.join(RESULTS, 'motor_results.json'), 'w'), indent=2)
    print("\n-> results/motor_results.json")
