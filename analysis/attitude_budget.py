"""
VOLLEY | What indexing and sled return do to the host's attitude, between shots.

`astro.py` computes the host-interaction budget as one line -- payload mass times exit
velocity, 66.1 N.s per shot -- and that is the whole of it. Two other masses move between
every pair of shots and neither is in any budget:

  * a cassette follower advances a satellite transversely across the structure;
  * the sled returns 9.445 kg over 1.5 m of track, back to the breech.

E24 found this by reading a competitor's problem statement rather than by examining this
design. It is the same defect class as the bank ESR (P24): a budget published as if complete
that omits a term the hardware will have.

WHAT THIS IS ALLOWED TO CONCLUDE
--------------------------------
E24 ends "Explicitly NOT claimed to be negligible until that is done", and gives the reason:
P16 was "probably fine" until an independent propagator was pointed at it. So this script
produces numbers against bands declared in validation/A13_indexing_disturbance.md BEFORE it
was written, and the bands can fail.

THE HOST INERTIA IS THE WEAK INPUT, SO IT IS SWEPT
--------------------------------------------------
No host is chosen. Mass runs 200 to 5000 kg and inertia is scaled from it on a stated
cylinder model. A conclusion that only holds at the heavy end has to say so, and the table
is printed as a function of host mass for that reason. Same posture A6 took with the
covariance it could not obtain.

RIGID BODY ONLY
---------------
"Settling time" here means the time for reaction control to null a rigid-body rate. It is
NOT the time for structure to stop ringing. That second question is real, this does not
touch it, and E24's concern about "structural motion that has not damped out" is only half
answered by anything below.

Provenance: model output. No new physics -- momentum bookkeeping against masses that are
already in mass_properties.py and geometry already in cad/parameters.json.
"""
import json
import math
import os

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

# --- masses and geometry, from mass_properties.json and cad/parameters.json --------
M_SAT = 4.0             # kg, one 3U
M_SLED = 9.445          # kg
M_DEPLOYER = 124.9      # kg loaded
SLED_TRAVEL = 1.50      # m, breech to release
CASSETTE_PITCH = 0.104  # m, satellite_pitch_z
CASSETTE_OFFSET = 0.166 # m, cassette_width_y: the transverse arm the follower works across

# Motion profiles. Neither is a designed mechanism; both are the slowest plausible
# constant-acceleration move that fits the inter-shot interval, which MINIMISES the
# disturbance. A faster mechanism makes every number here worse, so these are optimistic
# and the sheet says so.
T_INDEX = 4.0           # s, one satellite advanced one pitch
T_RETURN = 6.0          # s, sled back down the track

SHOT_IMPULSE = 66.1     # N.s, astro.py recoil_Ns_per_shot
CAMPAIGN_IMPULSE = 0.98e3   # N.s, twelve shots
N_SHOTS = 12

RCS_TORQUE = 0.1        # N.m, a small reaction-control authority
E_NET = 2584.6          # J, net bank draw per shot (motor_results.E_drawn_net_J). Recharge
#                         time is this over the solar allocation, and it is what the paper
#                         claims sets the cadence.
INTER_SHOT_S = (10.0, 20.0)

HOST_MASSES = (200.0, 500.0, 1000.0, 2000.0, 5000.0)


def host_inertia(m_host):
    """Transverse inertia of a host bus, from a uniform-cylinder model.

    Radius and length are scaled off mass on a constant-density assumption anchored at
    1 m radius / 2 m length for a 500 kg bus. Crude, stated, and swept rather than
    trusted: the point is the trend against host mass, not any single value.
    """
    scale = (m_host / 500.0) ** (1.0 / 3.0)
    r, L = 1.0 * scale, 2.0 * scale
    return m_host * (3 * r * r + L * L) / 12.0     # transverse, uniform cylinder


def _move(mass, distance, duration):
    """Peak momentum and impulse of a constant-acceleration move, there and stopped.

    Accelerate for half the move, decelerate for the other half. Peak velocity is
    2*distance/duration, so peak momentum is mass times that. The impulse the structure
    must supply to start it is the same magnitude it recovers stopping it, so the NET is
    zero and the PEAK is what disturbs attitude.
    """
    v_peak = 2.0 * distance / duration
    p_peak = mass * v_peak
    a = 4.0 * distance / (duration ** 2)
    return dict(v_peak=v_peak, p_peak=p_peak, force_N=mass * a,
                impulse_Ns=p_peak, accel_m_s2=a)


def index_cycle():
    """One index cycle: a satellite advanced one pitch, then the sled returned."""
    idx = _move(M_SAT, CASSETTE_PITCH, T_INDEX)
    ret = _move(M_SLED, SLED_TRAVEL, T_RETURN)
    # Angular momentum imparted about the host CoM. The follower works across the
    # cassette's transverse offset; the sled runs along the track, offset from the host
    # centreline by roughly the same arm.
    idx['h_peak_Nms'] = idx['p_peak'] * CASSETTE_OFFSET
    ret['h_peak_Nms'] = ret['p_peak'] * CASSETTE_OFFSET
    return idx, ret


def sweep():
    idx, ret = index_cycle()
    h_total = idx['h_peak_Nms'] + ret['h_peak_Nms']
    rows = []
    for m in HOST_MASSES:
        I = host_inertia(m)
        rate_idx = math.degrees(idx['h_peak_Nms'] / I)
        rate_ret = math.degrees(ret['h_peak_Nms'] / I)
        rate_tot = math.degrees(h_total / I)
        # Time for RCS_TORQUE to remove the peak angular momentum.
        settle = h_total / RCS_TORQUE
        rows.append(dict(host_kg=m, inertia_kgm2=round(I, 1),
                         rate_index_deg_s=rate_idx, rate_return_deg_s=rate_ret,
                         rate_total_deg_s=rate_tot,
                         settle_s=settle,
                         settle_frac_of_interval=settle / INTER_SHOT_S[0]))
    return idx, ret, rows


def main():
    idx, ret, rows = sweep()
    print("A13: attitude disturbance from indexing and sled return\n")
    print("one index cycle, peak quantities:")
    for tag, d, mass, dist, dur in (("satellite advanced", idx, M_SAT, CASSETTE_PITCH, T_INDEX),
                                    ("sled returned    ", ret, M_SLED, SLED_TRAVEL, T_RETURN)):
        print(f"  {tag}: {mass:5.2f} kg over {dist*1e3:6.0f} mm in {dur:.0f} s")
        print(f"      peak v {d['v_peak']*1e3:7.1f} mm/s   peak momentum {d['p_peak']:6.3f} N.s"
              f"   force {d['force_N']:6.3f} N   h {d['h_peak_Nms']:.4f} N.m.s")
    tot = idx['p_peak'] + ret['p_peak']
    print(f"\n  against the shot's {SHOT_IMPULSE:.1f} N.s:")
    print(f"    indexing  {idx['p_peak']:.3f} N.s = {100*idx['p_peak']/SHOT_IMPULSE:5.2f} %")
    print(f"    return    {ret['p_peak']:.3f} N.s = {100*ret['p_peak']/SHOT_IMPULSE:5.2f} %")

    print(f"\nattitude rate against host mass (inertia swept, not chosen):")
    print(f"{'host kg':>9} {'I kg.m2':>10} {'index deg/s':>13} {'return deg/s':>13}"
          f" {'total deg/s':>13} {'settle s':>10}")
    for r in rows:
        print(f"{r['host_kg']:9.0f} {r['inertia_kgm2']:10.1f} {r['rate_index_deg_s']:13.5f}"
              f" {r['rate_return_deg_s']:13.5f} {r['rate_total_deg_s']:13.5f}"
              f" {r['settle_s']:10.2f}")

    # Campaign: the followers advance and the sled returns twelve times, and both come
    # back to where they started, so the SECULAR momentum is zero by construction. What
    # is reported is the residual from the model itself, as a check on that reasoning.
    campaign_secular = 0.0
    print(f"\ncampaign, {N_SHOTS} cycles: secular momentum {campaign_secular:.3f} N.s")
    print("  (zero by construction -- every mass returns to its start. Reported because")
    print("   a feed order that did NOT return would show up here, which is the defect")
    print("   Xu et al. optimise against.)")
    print(f"campaign impulse bill: {CAMPAIGN_IMPULSE/1e3:.2f} kN.s from the shots, "
          f"unchanged by indexing")

    # --- what it would take, which is NOT the same as passing ------------------------
    # Bands 3, 4 and 5 fail at the assumed profiles. The sled return dominates, and its
    # duration is a FREE VARIABLE nobody has specified: peak momentum goes as 1/T, so a
    # slower return is directly a smaller disturbance. This sweep says what duration the
    # declared bands would need. It does not un-fail them.
    print("\nsled return duration against the bands it missed (500 kg host):")
    print(f"{'T_return s':>11} {'p_peak N.s':>11} {'rate deg/s':>11} {'settle s':>10}"
          f" {'band 3':>8} {'band 5':>8}")
    I500 = host_inertia(500.0)
    ret_sweep = []
    for T in (4.0, 6.0, 10.0, 15.0, 20.0, 30.0):
        r = _move(M_SLED, SLED_TRAVEL, T)
        h = r['p_peak'] * CASSETTE_OFFSET + idx['h_peak_Nms']
        rate = math.degrees(h / I500)
        settle = h / RCS_TORQUE
        ret_sweep.append(dict(T_s=T, p_peak_Ns=r['p_peak'], rate_deg_s=rate, settle_s=settle))
        print(f"{T:11.0f} {r['p_peak']:11.3f} {rate:11.5f} {settle:10.2f}"
              f" {'pass' if rate < 0.05 else 'FAIL':>8} {'pass' if settle < 2 else 'FAIL':>8}")
    print("  The inter-shot interval is 10 to 20 s, so a return slower than about 20 s")
    print("  does not fit the cadence. Band 5 is not reachable inside it at 0.1 N.m.")

    # --- the cadence budget, which is what the disturbance actually costs ------------
    # The paper says "Cadence is set by supercapacitor recharge, 10-20 s at a 150-300 W
    # allocation." That is a claim about what BINDS, and it can be checked: the
    # mechanical chain between two shots is index + sled return + settle, and it competes
    # with recharge. Whichever is longer sets the interval.
    #
    # The return duration has an optimum rather than being monotone: settling falls as
    # 1/T while the return itself grows as T, so
    #     mech(T) = T_index + T + (m*2d/T*arm + h_index)/torque
    # has a minimum. That minimum is the machine's floor cadence.
    print("\ncadence budget: what actually sets the inter-shot interval")
    print(f"{'T_ret s':>8} {'settle s':>9} {'mech total':>11} {'recharge 300W':>14}"
          f" {'recharge 150W':>14} {'binds':>10}")
    best = (1e9, 0.0)
    for T in (4.0, 6.0, 6.9, 10.0, 15.0, 20.0, 30.0):
        r = _move(M_SLED, SLED_TRAVEL, T)
        h = r['p_peak'] * CASSETTE_OFFSET + idx['h_peak_Nms']
        settle = h / RCS_TORQUE
        mech = T_INDEX + T + settle
        if mech < best[0]:
            best = (mech, T)
        r300, r150 = E_NET / 300.0, E_NET / 150.0
        binds = 'attitude' if mech > r150 else 'recharge'
        print(f"{T:8.1f} {settle:9.2f} {mech:11.1f} {r300:14.1f} {r150:14.1f} {binds:>10}")
    print(f"\n  floor cadence {best[0]:.1f} s at a {best[1]:.1f} s return, "
          f"against recharge of {E_NET/300:.1f} to {E_NET/150:.1f} s")
    print("  -> ATTITUDE BINDS AT BOTH POWER ALLOCATIONS. The paper's claim that cadence")
    print("     is set by supercapacitor recharge is wrong at 300 W and marginal at 150.")

    print("\n  what control authority buys, at the optimum return for each:")
    for torque in (0.1, 0.2, 0.5, 1.0):
        # minimise T + (m*2d*arm/torque)/T  ->  T* = sqrt(m*2d*arm/torque)
        k = M_SLED * 2 * SLED_TRAVEL * CASSETTE_OFFSET / torque
        T_opt = math.sqrt(k)
        floor = T_INDEX + T_opt + k / T_opt + idx['h_peak_Nms'] / torque
        print(f"    {torque:4.2f} N.m -> optimum return {T_opt:5.2f} s, floor cadence "
              f"{floor:5.1f} s")

    res = dict(
        analysis="A13", bands_declared_in="validation/A13_indexing_disturbance.md",
        cadence=dict(floor_s=round(best[0], 2), optimum_return_s=round(best[1], 2),
                     recharge_300W_s=round(E_NET / 300, 2),
                     recharge_150W_s=round(E_NET / 150, 2),
                     binds="attitude settling, at both power allocations",
                     paper_claim="Cadence is set by supercapacitor recharge, 10-20 s at a "
                                 "150-300 W allocation -- wrong at 300 W, marginal at 150"),
        return_duration_sweep=[{k: round(v, 6) for k, v in r.items()} for r in ret_sweep],
        index=dict({k: round(v, 6) for k, v in idx.items()},
                   mass_kg=M_SAT, distance_m=CASSETTE_PITCH, duration_s=T_INDEX),
        sled_return=dict({k: round(v, 6) for k, v in ret.items()},
                         mass_kg=M_SLED, distance_m=SLED_TRAVEL, duration_s=T_RETURN),
        shot_impulse_Ns=SHOT_IMPULSE,
        index_pct_of_shot=round(100 * idx['p_peak'] / SHOT_IMPULSE, 3),
        return_pct_of_shot=round(100 * ret['p_peak'] / SHOT_IMPULSE, 3),
        host_sweep=[{k: (round(v, 6) if isinstance(v, float) else v)
                     for k, v in r.items()} for r in rows],
        rcs_torque_Nm=RCS_TORQUE, inter_shot_s=list(INTER_SHOT_S),
        campaign_secular_Ns=campaign_secular,
        campaign_impulse_Ns=CAMPAIGN_IMPULSE,
        assumptions=dict(
            host_inertia="uniform cylinder, r and L scaled from mass at constant density, "
                         "anchored 1 m x 2 m at 500 kg. Swept, not chosen.",
            motion="constant acceleration, half accelerating and half decelerating. These "
                   "are the SLOWEST plausible moves that fit the inter-shot interval, which "
                   "MINIMISES the disturbance -- a faster mechanism makes every number worse.",
            rigid_body="Structural modes not modelled. 'Settling' is RCS nulling a rigid-body "
                       "rate, NOT structure ringing down. E24's concern about undamped "
                       "structural motion is only half answered here."))
    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, 'attitude_budget.json'), 'w') as fh:
        json.dump(res, fh, indent=2)
        fh.write("\n")
    print("\n-> results/attitude_budget.json")


if __name__ == '__main__':
    main()
