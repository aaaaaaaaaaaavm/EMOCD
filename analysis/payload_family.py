"""
VOLLEY | What the machine does across payload classes, from PocketQubes to 12U.

`docs/PAYLOAD_CLASSES.md` used to be four hand-typed tables. This script generates them,
for the reason every other generated artifact here exists: a table typed once is a table
that silently disagrees with the scripts the first time an input moves (P16, P19).

Two questions, and only the second one matters:

  1. Does a lighter payload go faster? Barely. The sled is 9.445 kg and the payload is
     0.005 to 12 kg, so removing the entire payload buys 19 % of velocity. Exit velocity
     is a property of the sled and the stroke, not of the customer.
  2. How much deployer does each customer pay for? This is the whole commercial argument,
     it moves by a factor of thirty across the ladder, and it is what decides whether
     VOLLEY beats a cold-gas module (docs/KILL_CRITERIA.md threat 1).

THE PACKING MODEL, WHICH IS THE ONE THING WORTH ARGUING WITH
------------------------------------------------------------
A raw volume ratio says the magazine holds 21 3U satellites. It holds 12. The difference
is septa, follower plates, the escapement, the gate and the drive bay, none of which a
volume ratio knows about.

So the model is calibrated rather than asserted: PACK_EFF is set so the 3U case returns
the twelve the machine is actually laid out for, and the same efficiency is applied to
every other class. That converts `docs/PAYLOAD_CLASSES.md`'s old caveat -- "realistic
packing is likely 40 to 60 %" -- from a hedge into a number anchored on the one
configuration that has been drawn in CAD.

It is still a volumetric argument. **No cassette, cradle or gate exists for any class
except 3U**, and the feed engages CubeSat corner rails, which PocketQubes and TubeSats do
not have. The counts below say how much room there is, not that anything has been designed
to use it.

Provenance: model output, not independently re-derived. Payload masses are typical flight
masses from published form-factor specifications, not qualification maxima.
"""
import json
import math
import os

import motor_model as mm

# Outputs go next to this script, not next to whoever ran it. Every script here used to
# write to a cwd-relative "results/", so running one from the repository root created a
# SECOND, silently stale copy of its JSON at the root -- which is exactly what happened on
# 2026-07-30 and left a results/sizing.json carrying a superseded inter-array force. A
# duplicate that nothing regenerates is the defect class this repository logs twice
# already (P16, P19).
RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

G = 9.81
G_QUAL = 25.0                   # g, CubeSat Design Specification design cap (docs/VELOCITY_CEILING.md)

# --- magazine geometry, from cad/parameters.json groups.magazine ----------------
CASSETTES = 2
CASSETTE_LEN_X = 380.5          # mm
CASSETTE_WID_Y = 166.0          # mm
DRIVE_BAY_X = 30.0              # mm, leadscrew and follower drive, not available to payload
SATS_PER_CASSETTE = 6
PITCH_Z = 104.0                 # mm

# Usable bay: the stack height the six slots occupy, across the cassette section less the
# drive bay. This is the gross volume the packing efficiency is then applied to.
BAY_MM3 = (CASSETTES * (CASSETTE_LEN_X - DRIVE_BAY_X) * CASSETTE_WID_Y
           * SATS_PER_CASSETTE * PITCH_Z)

DEPLOYER_DRY_KG = 76.5          # mass_properties.json. Several packaging line items remain
#                                 parametric rather than measured, so every kg-per-satellite
#                                 figure remains provisional.


# (tag, mass kg, bounding box mm, note)
# Bounding boxes are the packing envelope, so cylinders are boxed: a TubeSat stows in the
# square prism around it, not in its own volume.
CLASSES = [
    ("ChipSat / femtosat", 0.005, (35, 35, 2.5),
     "Sprite class. Volumetric only -- see mechanism_limited"),
    ("PocketQube 1P", 0.25, (50, 50, 50), "PocketQube standard, 1P"),
    ("ThinSat", 0.28, (114, 114, 25.4), "ThinSat published envelope"),
    ("PocketQube 3P", 0.75, (50, 50, 150), "PocketQube standard, 3P"),
    ("TubeSat", 0.75, (88, 88, 127), "Boxed from the 88 mm cylinder"),
    ("1U CubeSat", 1.33, (100, 100, 100), "Typical flight mass, CDS allows 2 kg"),
    ("3U CubeSat", 4.00, (340, 100, 100), "The reference payload, and the only one laid out"),
    ("6U CubeSat", 8.00, (340, 200, 100), "Arithmetic only, no cassette exists"),
    ("12U CubeSat", 12.00, (340, 200, 200), "Arithmetic only, no cassette exists"),
]

# The escapement, the gate and the campaign thermal case were all sized for twelve shots.
# Anything asking for materially more is a different machine, not a bigger magazine, and
# is flagged rather than quietly tabulated.
MECHANISM_SHOT_LIMIT = 200


def _pack_efficiency(ref_tag="3U CubeSat", ref_count=12):
    """Calibrate the volumetric model against the one configuration that has been drawn."""
    for tag, _m, box, _n in CLASSES:
        if tag == ref_tag:
            gross = BAY_MM3 / (box[0] * box[1] * box[2])
            return ref_count / gross
    raise SystemExit(f"reference class {ref_tag} not in CLASSES")


def family(Kt=None, F_cmd=None):
    if Kt is None or F_cmd is None:
        Kt, _ripple = mm.thrust_constant()
        F_cmd = 0.9 * Kt * mm.K_RATED
    eff = _pack_efficiency()
    rows = []
    for tag, m_sat, box, note in CLASSES:
        a = min(F_cmd / (m_sat + mm.M_SLED), G_QUAL * G)
        v = math.sqrt(2 * a * mm.ACCEL_ZONE)
        n = int(BAY_MM3 / (box[0] * box[1] * box[2]) * eff)
        rows.append(dict(
            tag=tag, mass_kg=m_sat, box_mm=list(box),
            a_g=round(a / G, 1), v_exit=round(v, 1),
            n_per_load=n,
            kg_per_satellite=round(DEPLOYER_DRY_KG / n, 3) if n else None,
            mechanism_limited=bool(n > MECHANISM_SHOT_LIMIT),
            note=note))
    return dict(pack_efficiency=round(eff, 3), bay_mm3=round(BAY_MM3),
                deployer_dry_kg=DEPLOYER_DRY_KG, F_cmd=round(F_cmd, 1),
                mechanism_shot_limit=MECHANISM_SHOT_LIMIT, classes=rows)


def sled_scaling(lengths=(340, 240, 150), m_sat=4.0):
    """What a shorter magnet array buys, which is nothing.

    Array length sets thrust and sled mass together: a shorter array is a lighter sled AND
    a weaker motor. Kt scales with active length; sled mass is taken as the magnet mass,
    which scales with length, plus the chassis, which is treated as a fixed overhead plus a
    length term. That split is crude and is the reason this returns a trend rather than a
    design -- a genuinely minimal sled for a 0.25 kg payload has not been drawn and would
    not look like a scaled copy of this one.
    """
    Kt, _ = mm.thrust_constant()
    mag_per_mm = 3.67 / 340.0                 # mass_properties: sled Halbach magnets
    # Everything that is not magnet -- chassis, rollers, latch, backstop -- carried as a
    # length term over the array plus 148 mm of end structure that does not shrink.
    struct_per_mm = (mm.M_SLED - 3.67) / (340.0 + 148.0)
    out = []
    for L in lengths:
        kt = Kt * L / 340.0
        sled = mag_per_mm * L + struct_per_mm * (L + 148.0)
        F = 0.9 * kt * mm.K_RATED
        a = min(F / (m_sat + sled), G_QUAL * G)
        out.append(dict(array_mm=L, Kt_N_per_kA=round(kt * 1e3, 2),
                        sled_kg=round(sled, 2), F_N=round(F, 0),
                        a_g=round(a / G, 1),
                        v_exit=round(math.sqrt(2 * a * mm.ACCEL_ZONE), 1)))
    return out


DOC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   '..', 'docs', 'PAYLOAD_CLASSES.md')
START, END = "<!-- PAYLOAD-TABLES-START -->", "<!-- PAYLOAD-TABLES-END -->"


def doc_tables(res):
    """The three tables docs/PAYLOAD_CLASSES.md used to carry by hand."""
    out = ["### Velocity, which barely moves\n",
           "| Payload | Mass | Moving mass with the 9.445 kg sled | Acceleration | Exit velocity |",
           "|---|---|---|---|---|"]
    for r in res['classes']:
        out.append(f"| {r['tag']} | {r['mass_kg']:.3f} kg | "
                   f"{r['mass_kg'] + mm.M_SLED:.2f} kg | {r['a_g']:.1f} g | "
                   f"{r['v_exit']:.1f} m/s |")
    out += ["", "### Deployer mass per customer, which moves by a factor of thirty\n",
            "| Payload | Envelope, mm | Per load | Deployer kg per satellite | |",
            "|---|---|---|---|---|"]
    for r in res['classes']:
        b = r['box_mm']
        flag = "**beyond the mechanism**" if r['mechanism_limited'] else ""
        out.append(f"| {r['tag']} | {b[0]:g} x {b[1]:g} x {b[2]:g} | {r['n_per_load']} | "
                   f"**{r['kg_per_satellite']:.3f}** | {flag} |")
    out += ["", "### Shortening the magnet array, which buys nothing\n",
            "| Array length | K<sub>t</sub> | Sled mass | Force | Acceleration, 3U | Exit velocity |",
            "|---|---|---|---|---|---|"]
    for r in res['sled_scaling']:
        out.append(f"| {r['array_mm']} mm | {r['Kt_N_per_kA']:.2f} | {r['sled_kg']:.2f} kg | "
                   f"{r['F_N']:.0f} N | {r['a_g']:.1f} g | {r['v_exit']:.1f} m/s |")
    return "\n".join(out)


def write_doc(res):
    with open(DOC, encoding='utf-8') as fh:
        text = fh.read()
    i, j = text.find(START), text.find(END)
    if i < 0 or j < 0:
        raise SystemExit(f"{DOC} is missing the {START} / {END} markers.")
    new = text[:i + len(START)] + "\n\n" + doc_tables(res) + "\n\n" + text[j:]
    if new != text:
        with open(DOC, 'w', encoding='utf-8') as fh:
            fh.write(new)
        print("-> docs/PAYLOAD_CLASSES.md tables rewritten")
    else:
        print("docs/PAYLOAD_CLASSES.md tables already current")


if __name__ == '__main__':
    res = family()
    print(f"packing efficiency {res['pack_efficiency']:.3f}, calibrated so 3U returns 12")
    print(f"usable bay {res['bay_mm3']/1e6:.1f} litres, deployer {DEPLOYER_DRY_KG} kg dry\n")
    print(f"{'class':22s} {'kg':>6s} {'a (g)':>6s} {'v (m/s)':>8s} {'n':>7s} {'kg/sat':>8s}")
    for r in res['classes']:
        flag = '  *' if r['mechanism_limited'] else ''
        print(f"{r['tag']:22s} {r['mass_kg']:6.3f} {r['a_g']:6.1f} {r['v_exit']:8.1f} "
              f"{r['n_per_load']:7d} {r['kg_per_satellite']:8.3f}{flag}")
    print(f"\n  * beyond {MECHANISM_SHOT_LIMIT} per load: the escapement, gate cycle life and "
          f"campaign\n    thermal case were sized for twelve. That is a different machine.")

    res['sled_scaling'] = sled_scaling()
    print("\nshortening the magnet array (3U payload):")
    for r in res['sled_scaling']:
        print(f"  {r['array_mm']:3d} mm  Kt {r['Kt_N_per_kA']:5.2f}  sled {r['sled_kg']:5.2f} kg"
              f"  {r['a_g']:4.1f} g  {r['v_exit']:5.1f} m/s")

    os.makedirs(RESULTS, exist_ok=True)
    json.dump(res, open(os.path.join(RESULTS, 'payload_family.json'), 'w'), indent=2)
    print("\n-> results/payload_family.json")
    write_doc(res)
