"""
VOLLEY | Every lever that has been proposed for recovering exit velocity, priced against the
current model rather than against the one they were first costed on.

`docs/DESIGN_OPTIONS_exit_velocity.md` computed these on 2026-07-28. Three things have
happened since, and all three change the answer:

  1. **The bank has a series resistance** (P24, A8-R). Every row that raises current now
     costs terminal voltage as well as copper.
  2. **A10 found a hard ESR ceiling.** A source of EMF V behind resistance R cannot deliver
     more than V^2/4R into any load, so raising peak current LOWERS the resistance the bank
     is allowed to have. At the rated point the ceiling is 65 mohm; a single commercial
     string is 116-185 (P26). Any lever that raises current makes that worse, and the old
     table could not show it because no script modelled ESR.
  3. **Regeneration returns about a quarter of the sled's energy** (A11), so efficiency is
     now quoted net of recovery and the levers that add sled mass are penalised slightly
     less than they were.

The ESR ceiling column is the point of this script. It is computed by bisection on the real
integrator: raise R_ESR until shot() raises BankLimitError, and report the last value that
completes. That is a property of the lever, not of the bank, and it is what decides whether
a lever can be built at all rather than how well it performs.

Provenance: model output. No new physics -- every row drives motor_model.py with modified
inputs, the same way the original exploration did.
"""
import contextlib
import json
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

# (label, sled kg, Kt N per A/m, K_lim A/m, accel zone m, winding thickness m, note)
# The winding thickness matters and is easy to miss: shot() derives current density from it,
# so a two-layer stator that does NOT declare a thicker winding is reported at twice the
# current density it actually runs at. The 2026-07-28 exploration got this right in prose
# ("J = 21 A/mm^2, the same copper loading as today") and it has to be in the inputs here.
# Kt is recomputed from the field model wherever the magnetic geometry changes; the values
# here are the ones docs/DESIGN_OPTIONS_exit_velocity.md derived that way in 2026-07-28.
LEVERS = [
    ("Superseded 4.86 kg assumption", 4.86, 11.22e-3, 140e3, 1.30, 0.010, "the number the paper used to carry"),
    ("As drawn (the baseline)", 9.445, 11.22e-3, 140e3, 1.30, 0.010, "P15, measured from the Gen3 solids"),
    ("Pocket 40 % of the titanium", 7.50, 11.22e-3, 140e3, 1.30, 0.010, "no such chassis has been designed"),
    ("Pocket 60 % (aggressive)", 6.53, 11.22e-3, 140e3, 1.30, 0.010, "unsupported: A4 passed the as-drawn plate"),
    ("Magnets 8 to 6 mm", 8.53, 9.30e-3, 140e3, 1.30, 0.010, "moves backwards"),
    ("Magnets 8 to 5 mm", 8.07, 8.16e-3, 140e3, 1.30, 0.010, "moves backwards further"),
    ("Raise sheet current to 213 kA/m", 9.445, 11.22e-3, 213e3, 1.30, 0.010, "52 % thermal overload"),
    ("Lengthen the stroke to 1.97 m", 9.445, 11.22e-3, 140e3, 1.97, 0.010, "+673 mm of envelope (P9)"),
    ("Two-layer stator (G3-D4)", 9.445, 7.46e-3, 280e3, 1.30, 0.020, "gap 12 to 22 mm, current doubles"),
    ("Two-layer + 40 % pocketing", 7.50, 7.46e-3, 280e3, 1.30, 0.020, "the only row that met the old target"),
]

ESR_CEILING_MAX = 0.30          # ohm, bisection bracket; nothing plausible sits above this


@contextlib.contextmanager
def _patched(sled, accel, esr, wind=None):
    """Drive motor_model with modified constants and put them back.

    The alternative is a second copy of the integrator, which is how figures and analyses
    drift apart in this project (P19, and the reason paper/make_figures.py imports rather
    than reimplements).
    """
    old = (mm.M_SLED, mm.ACCEL_ZONE, mm.R_ESR, mm.WIND_THICK)
    mm.M_SLED, mm.ACCEL_ZONE, mm.R_ESR = sled, accel, esr
    if wind is not None:
        mm.WIND_THICK = wind
    try:
        yield
    finally:
        mm.M_SLED, mm.ACCEL_ZONE, mm.R_ESR, mm.WIND_THICK = old


def esr_ceiling(sled, Kt, K_lim, accel, wind, lo=0.001, hi=ESR_CEILING_MAX, tol=1e-4):
    """Highest bank ESR at which this lever's shot still completes.

    Bisection on the integrator itself rather than on the V^2/4R algebra, because the bank
    sags during the stroke and the ceiling is set at the sagged voltage, not at 96 V. A10
    found the difference: 65 mohm measured against 76.8 mohm derived at V0.
    """
    def completes(r):
        with _patched(sled, accel, r, wind):
            try:
                mm.shot(Kt, K_lim=K_lim, dt=1e-4)     # the step A10 used. A10 swept discrete
                #     values and bracketed the baseline between 65 (completes) and 70 (fails);
                #     bisecting lands at 66, inside that bracket rather than against it.
                return True
            except mm.BankLimitError:
                return False
    if not completes(lo):
        return None                       # fails even at a near-ideal bank
    if completes(hi):
        return hi
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if completes(mid):
            lo = mid
        else:
            hi = mid
    return lo


def levers():
    rows = []
    for label, sled, Kt, K_lim, accel, wind, note in LEVERS:
        with _patched(sled, accel, mm.R_ESR, wind):
            s = mm.shot(Kt, K_lim=K_lim)
            rg = mm.regen_brake(Kt, s['v_exit'], mm.V0 * (1 - s['sag_pct'] / 100),
                                K_lim=K_lim)
        net = s['E_drawn'] - rg['E_recovered']
        ceiling = esr_ceiling(sled, Kt, K_lim, accel, wind)
        rows.append(dict(
            lever=label, sled_kg=sled, Kt_N_per_kA=round(Kt * 1e3, 2),
            K_kA=K_lim / 1e3, accel_m=accel,
            v_exit=round(s['v_exit'], 2), a_g=round(s['a_g'], 1),
            J_Amm2=round(s['J_Amm2'], 1), I_peak=round(s['I_peak'], 0),
            eff_net_pct=round(s['KE_payload'] / net * 100, 1),
            E_net_J=round(net, 0),
            esr_ceiling_mohm=round(ceiling * 1e3, 0) if ceiling else None,
            note=note))
    return rows


DOC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   '..', 'docs', 'DESIGN_OPTIONS_exit_velocity.md')
START, END = "<!-- LEVER-TABLE-START -->", "<!-- LEVER-TABLE-END -->"

# A single commercial string of 32 x 190 F cells, from A10's ESR x C argument.
STRING_ESR_LO, STRING_ESR_HI = 116, 185     # mohm


def doc_table(rows):
    out = ["| Lever | Sled | K<sub>t</sub> | K | Stroke | Exit velocity | J | Peak A | Efficiency | Bank ESR ceiling |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        c = f"{r['esr_ceiling_mohm']:.0f} mohm" if r['esr_ceiling_mohm'] else "**does not close**"
        if r['esr_ceiling_mohm'] and r['esr_ceiling_mohm'] < 30:
            c = f"**{c}**"
        out.append(f"| {r['lever']} | {r['sled_kg']:.2f} kg | {r['Kt_N_per_kA']:.2f} | "
                   f"{r['K_kA']:.0f} | {r['accel_m']:.2f} m | **{r['v_exit']:.2f} m/s** | "
                   f"{r['J_Amm2']:.1f} | {r['I_peak']:.0f} | {r['eff_net_pct']:.1f} % | {c} |")
    return "\n".join(out)


def write_doc(rows):
    with open(DOC, encoding='utf-8') as fh:
        text = fh.read()
    i, j = text.find(START), text.find(END)
    if i < 0 or j < 0:
        raise SystemExit(f"{DOC} is missing the {START} / {END} markers.")
    new = text[:i + len(START)] + "\n\n" + doc_table(rows) + "\n\n" + text[j:]
    if new != text:
        with open(DOC, 'w', encoding='utf-8') as fh:
            fh.write(new)
        print("-> docs/DESIGN_OPTIONS_exit_velocity.md table rewritten")
    else:
        print("docs/DESIGN_OPTIONS_exit_velocity.md table already current")


if __name__ == '__main__':
    rows = levers()
    print(f"{'lever':34s} {'v':>7s} {'J':>6s} {'I pk':>6s} {'eff':>6s} {'ESR ceil':>9s}")
    for r in rows:
        c = f"{r['esr_ceiling_mohm']:.0f}" if r['esr_ceiling_mohm'] else "none"
        print(f"{r['lever']:34s} {r['v_exit']:7.2f} {r['J_Amm2']:6.1f} {r['I_peak']:6.0f} "
              f"{r['eff_net_pct']:5.1f}% {c:>9s}")
    print(f"\nA single commercial string of 32 x 190 F cells is {STRING_ESR_LO}-{STRING_ESR_HI} "
          f"mohm (A10).\nNo row above clears it, which is P26 restated: the bank, not the "
          f"winding, is the binding\nconstraint on every one of these levers.")

    os.makedirs(RESULTS, exist_ok=True)
    json.dump(dict(levers=rows, string_esr_mohm=[STRING_ESR_LO, STRING_ESR_HI]),
              open(os.path.join(RESULTS, 'velocity_levers.json'), 'w'), indent=2)
    print("\n-> results/velocity_levers.json")
    write_doc(rows)
