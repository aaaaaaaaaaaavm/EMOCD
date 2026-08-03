"""A13 correction: transient host motion from internal mass translation.

The first A13 implementation treated peak internal angular momentum as a residual host
rate after the moving mass stopped. That violates angular-momentum conservation in the
ideal rigid-body model it declared. The host counter-rotates while the mass moves, returns
to zero rate when the mass stops, and retains an attitude offset.
"""
import hashlib
import json
import math
import os
import platform
import numpy as np

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
M_SAT, M_SLED, M_DEPLOYER = 4.0, 9.445, 124.5
SLED_TRAVEL, CASSETTE_PITCH, ASSUMED_ARM = 1.50, 0.104, 0.166
T_INDEX, T_RETURN, V_EXIT, N_SHOTS = 4.0, 6.0, 16.388, 12
RCS_TORQUE = 0.1
HOST_MASSES = (200.0, 500.0, 1000.0, 2000.0, 5000.0)


def host_inertia(mass):
    scale = (mass / 500.0) ** (1.0 / 3.0)
    radius, length = scale, 2.0 * scale
    return mass * (3 * radius**2 + length**2) / 12.0


def deployer_inertia():
    length, width = 1.839, 0.530
    return M_DEPLOYER * (length**2 + width**2) / 12.0


def move(mass, distance, duration, inertia, n=20001):
    """Internal move, checked analytically and by numerical time integration."""
    time = np.linspace(0.0, duration, n)
    accel = 4.0 * distance / duration**2
    velocity = np.where(time <= duration / 2, accel * time,
                        accel * (duration - time))
    body_rate = -mass * ASSUMED_ARM * velocity / inertia
    angle_numeric = float(np.trapezoid(body_rate, time))
    angle_exact = -mass * ASSUMED_ARM * distance / inertia
    return dict(
        peak_linear_momentum_Ns=mass * 2.0 * distance / duration,
        peak_body_rate_deg_s=math.degrees(float(np.max(np.abs(body_rate)))),
        residual_body_rate_deg_s=math.degrees(abs(float(body_rate[-1]))),
        attitude_offset_deg=math.degrees(angle_exact),
        numerical_offset_deg=math.degrees(angle_numeric),
        integration_error_deg=math.degrees(angle_numeric - angle_exact),
        post_move_slew_min_s=2.0 * math.sqrt(inertia * abs(angle_exact) / RCS_TORQUE))


def sweep():
    rows = []
    i_deployer = deployer_inertia()
    for mass in HOST_MASSES:
        inertia = host_inertia(mass) + i_deployer
        index = move(M_SAT, CASSETTE_PITCH, T_INDEX, inertia)
        returned = move(M_SLED, SLED_TRAVEL, T_RETURN, inertia)
        rows.append(dict(
            host_kg=mass, combined_inertia_kgm2=inertia,
            index=index, sled_return=returned,
            sequential_peak_rate_deg_s=max(index["peak_body_rate_deg_s"],
                                           returned["peak_body_rate_deg_s"]),
            residual_rate_deg_s=max(index["residual_body_rate_deg_s"],
                                    returned["residual_body_rate_deg_s"]),
            worst_case_attitude_offset_deg=(abs(index["attitude_offset_deg"])
                                            + abs(returned["attitude_offset_deg"]))))
    return rows


def main():
    rows = sweep()
    shot_impulse = M_SAT * V_EXIT
    campaign_impulse = N_SHOTS * shot_impulse
    row200 = next(r for r in rows if r["host_kg"] == 200.0)
    row500 = next(r for r in rows if r["host_kg"] == 500.0)
    bands = [
        dict(row=1, result_pct=100 * M_SAT * 2 * CASSETTE_PITCH / T_INDEX / shot_impulse,
             verdict="PASS"),
        dict(row=2, result_pct=100 * M_SLED * 2 * SLED_TRAVEL / T_RETURN / shot_impulse,
             verdict="PASS"),
        dict(row=3, result_deg_s=row500["sequential_peak_rate_deg_s"], verdict="FAIL"),
        dict(row=4, result_deg_s=row200["sequential_peak_rate_deg_s"], verdict="FAIL"),
        dict(row=5, result_s=0.0, verdict="PASS IN THE IDEAL RIGID-BODY MODEL"),
        dict(row=6, result_Ns=0.0, verdict="PASS BY THE CLOSED INTERNAL CYCLE"),
        dict(row=7, result_pct=None, verdict="VOID; NO RCS PROPELLANT MODEL EXISTS")]

    print("A13 corrected rigid-body momentum budget\n")
    print(f"{'host kg':>8} {'I total':>10} {'index peak':>12} {'return peak':>12} "
          f"{'residual':>11} {'offset worst':>13}")
    for row in rows:
        print(f"{row['host_kg']:8.0f} {row['combined_inertia_kgm2']:10.1f} "
              f"{row['index']['peak_body_rate_deg_s']:12.5f} "
              f"{row['sled_return']['peak_body_rate_deg_s']:12.5f} "
              f"{row['residual_rate_deg_s']:11.5f} "
              f"{row['worst_case_attitude_offset_deg']:13.5f}")
    print(f"\nshot impulse {shot_impulse:.3f} N.s; twelve shots {campaign_impulse:.3f} N.s")
    print("Rows 3 and 4 remain FAIL. Row 5 passes only in the ideal rigid-body model;")
    print("structural ringing and the attitude-restoration schedule remain open.")

    # Hash canonical LF bytes so Git checkout line endings cannot change the provenance record.
    with open(__file__, "rb") as source:
        source_hash = hashlib.sha256(source.read().replace(b"\r\n", b"\n")).hexdigest()
    result = dict(
        analysis="A13 corrected",
        supersedes="A13 result run 2026-07-31",
        method="angular-momentum conservation with numerical time integration",
        software=dict(python=platform.python_version(), python_license="PSF License",
                      numpy=np.__version__, numpy_license="BSD-3-Clause",
                      source_sha256=source_hash),
        solver_settings=dict(time_samples=20001, integration="numpy.trapezoid",
                             analytic_cross_check="closed-form triangular profile"),
        assumptions=dict(
            motion="symmetric triangular profile; each mass starts and ends at rest",
            arm_m=ASSUMED_ARM,
            arm_status="assumed; cassette width is not a measured CoM lever arm",
            sequence="index and return are sequential; peak rates are not added",
            deployer_inertia="124.5 kg box at the 1.839 x 0.530 m envelope",
            rigid_body="no structural modes, damping, flexible coupling, or controller"),
        shot_impulse_Ns=shot_impulse, campaign_impulse_Ns=campaign_impulse,
        host_sweep=rows, bands=bands,
        verdict="FAIL rows 3 and 4; row 7 VOID; cadence conclusion superseded")
    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, "attitude_budget.json"), "w") as output:
        json.dump(result, output, indent=2)
        output.write("\n")
    print("\n-> results/attitude_budget.json")


if __name__ == "__main__":
    main()
