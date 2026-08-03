"""Generate docs/BASELINE.md from analysis/results/*.json.

The frozen Phase I baseline must not be a hand-typed table. Every number in a hand-typed
table is a number that can silently disagree with the scripts -- which is the exact defect
class this repository logs (P16, P19) and mechanically guards against elsewhere
(sizing.py's _check_operating_point, paper/make_figures.py).

Run after any authorised baseline change:  python3 tools/make_baseline.py
"""
import argparse
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, 'analysis', 'results')


def load(name):
    with open(os.path.join(R, name), encoding='utf-8') as f:
        return json.load(f)


def value_rows(text):
    """Just the engineering values, without the provenance stamp.

    The commit hash in the header changes on every commit, so a plain diff of this file
    always reports a change and is therefore useless as a drift detector -- which would have
    quietly defeated the check this file documents.
    """
    return [ln for ln in text.splitlines() if ln.startswith('| ') and '`' in ln]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true',
                    help='compare values against the committed file; exit 1 on drift')
    args = ap.parse_args()
    m, a, s = load('motor_results.json'), load('astro_results.json'), load('sizing.json')
    mp, c = load('mass_properties.json'), load('cost.json')
    sh = m['shot']
    commit = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT,
                            capture_output=True, text=True).stdout.strip()

    rows = [
        ("Thrust constant", f"{m['Kt_N_per_kA']} N per kA/m, ±{m['ripple_pct']} % ripple", "motor_results.Kt_N_per_kA"),
        ("Exit velocity, 3U", f"{sh['v_exit']:.3f} m/s", "motor_results.shot.v_exit"),
        ("Payload acceleration", f"{sh['a_g']:.2f} g", "motor_results.shot.a_g"),
        ("Pulse duration", f"{sh['t_ms']:.1f} ms", "motor_results.shot.t_ms"),
        ("Peak current", f"{sh['I_peak']:.0f} A", "motor_results.shot.I_peak"),
        ("Bank sag", f"{sh['sag_pct']:.2f} %", "motor_results.shot.sag_pct"),
        ("Energy drawn per shot, gross", f"{sh['E_drawn']:.0f} J", "motor_results.shot.E_drawn"),
        ("Energy recovered per shot", f"{m['regen']['E_recovered']:.0f} J ({m['regen']['frac_recovered_pct']:.1f} % of sled KE)", "motor_results.regen.E_recovered"),
        ("Energy drawn per shot, net", f"{m['E_drawn_net_J']:.0f} J", "motor_results.E_drawn_net_J"),
        ("Sled energy to the brake", f"{m['regen']['KE_to_brake']:.0f} J", "motor_results.regen.KE_to_brake"),
        ("Copper loss per shot", f"{sh['Q_copper'] + m['regen']['Q_copper']:.0f} J (shot + regen)", "motor_results.shot.Q_copper"),
        ("Payload kinetic energy", f"{sh['KE_payload']:.0f} J", "motor_results.shot.KE_payload"),
        ("Electrical-to-payload efficiency", f"{m['eff_net_pct']:.1f} % (net of regeneration)", "motor_results.eff_net_pct"),
        ("Closed-loop dispersion", f"{m['closed_loop_3sigma']} m/s (3σ)", "motor_results.closed_loop_3sigma"),
        ("Fleet setpoint", f"{m['v_fleet_setpoint']} m/s", "motor_results.v_fleet_setpoint"),
        ("Sled mass", f"{mp['sled_kg']} kg (computed from CAD solid volumes)", "mass_properties.sled_kg"),
        ("Dry / loaded mass", f"{mp['dry_kg']} / {mp['loaded_kg']} kg", "mass_properties.dry_kg"),
        ("Lifetime multiplier, mean activity", f"x{a['lifetime']['mean']['multiplier']}", "astro_results.lifetime.mean"),
        ("Recoil per shot", f"{a['recoil_Ns_per_shot']} N·s", "astro_results.recoil_Ns_per_shot"),
        ("Phase realignment period", f"{a['conjunction']['realign_days']} days", "astro_results.conjunction.realign_days"),
        ("Energy closure", f"{s['energy_closure']['closure_pct']} %", "sizing.energy_closure.closure_pct"),
        ("Track first mode", f"{s['track_mode']['fixed_fixed_Hz']} Hz fixed-fixed", "sizing.track_mode.fixed_fixed_Hz"),
        ("Recurring hardware cost", f"₹{c['total_INR']:,} per unit (all prices assumed)", "cost.total_INR"),
    ]

    body = HEADER.format(commit=commit)
    body += "\n".join(f"| {n} | **{v}** | `{src}` |" for n, v, src in rows)
    body += FOOTER

    path = os.path.join(ROOT, 'docs', 'BASELINE.md')
    if args.check:
        if not os.path.exists(path):
            raise SystemExit("docs/BASELINE.md missing -- run without --check to generate it.")
        with open(path, encoding='utf-8') as f:
            old = value_rows(f.read())
        new = value_rows(body)
        drift = [(o, n) for o, n in zip(old, new) if o != n]
        if drift or len(old) != len(new):
            print("BASELINE DRIFT -- the scripts have moved and the baseline has not.")
            for o, n in drift:
                print(f"  committed: {o}\n  scripts  : {n}")
            raise SystemExit(1)
        print(f"baseline holds: {len(new)} values match the scripts")
        return

    with open(path, 'w', encoding='utf-8') as f:

        f.write(body)
    print(f"docs/BASELINE.md written from analysis/results/ at {commit} ({len(rows)} values)")


HEADER = """# Phase I frozen baseline

> **Generated by `tools/make_baseline.py` from `analysis/results/*.json`. Do not hand-edit.**
> Every value below is read from the scripts at generation time, so this file cannot silently
> disagree with them. Regenerate after any authorised baseline change.
>
> Flagship commit at generation: `{commit}` · Phase **I** · governed by
> [`docs/programme/ENGINEERING_PROGRAMME.md`](programme/ENGINEERING_PROGRAMME.md)

This is the engineering baseline the Phase I deliverables (portfolio, IEEE paper, thesis)
are developed against. Dossier §2 requires it to be stable. The change-control rule below is
what makes "stable" mean something.

**These are model outputs.** Nothing here has been measured. See
[`PROVENANCE.md`](PROVENANCE.md) before citing any of it.

## The baseline

| Quantity | Value | Source field |
|---|---|---|
"""

FOOTER = """

## Change control

### What may move the baseline during Phase I

1. **Error correction.** A value that is wrong. P17, the inter-array attraction being 37 %
   high, qualifies, and stays Phase I even though correcting it moves three coupled numbers.
2. **A validation outcome against a band declared before its run.** This is how the baseline
   last moved: `validation/A4_sled_structural.md` fixed the consequence of each sled-mass
   outcome *before* the analysis ran, the CAD result landed in the ≥ 6.80 kg branch, and the
   scripts followed the rule rather than a preference.
3. **A defect that makes a Phase I deliverable wrong.** A paper that states something the
   scripts contradict is a defect regardless of which is right.

### What may not

Performance improvement. Architecture change. Anything whose motivation is *better* rather
than *correct*. These go to [`docs/PHASE_II.md`](PHASE_II.md) with an entry criterion,
and are reviewed at the next baseline boundary.

**The boundary is by type, not by convenience.** The momentum-transfer release in
`docs/DESIGN_OPTIONS_exit_velocity.md` recovers the entire velocity shortfall for 1.6 % of
shot energy and is the most interesting idea in this repository. It defers. P17 is tedious,
touches three coupled numbers, and improves nothing anyone will notice. It does not defer.
If that distinction ever bends toward whichever is easier, the baseline has stopped meaning
anything.

### Every baseline change must

- **Name its trigger**, which P-item, E-item or validation outcome forced it.
- **State which validations it invalidates.** This is the P19 lesson: moving the sled mass
  silently invalidated A5 and A8, both of which had been run at the old operating point. That
  was discovered afterwards. It should have been declared as a consequence at the time.
- **Propagate in order: scripts, then figures, then paper.** Never the reverse. The scripts are
  authoritative; `paper/make_figures.py` and `tools/make_baseline.py` regenerate from them.
- **Be recorded** in `CHANGELOG.md` and as an ADR under `docs/adr/`.

## Verifying this file

```bash
python3 tools/make_baseline.py    # regenerates; a clean diff means the baseline holds
git diff --exit-code docs/BASELINE.md  # non-zero means the scripts have moved and the record has not
```

That second command is the useful one. If it ever fails unexpectedly, something changed a
script value without going through change control.
"""

if __name__ == '__main__':
    main()
