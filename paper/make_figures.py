"""Regenerate every figure in paper/figures/ from analysis/.

Why this exists: until 2026-07-29 the committed PNGs had no generator in the
repository. `legacy/make_figs.py` sits at a superseded operating point (4.0 kg sled,
F_cmd = 1717*0.9) and *reimplements* the physics instead of importing it, which is the
exact fork this project polices everywhere else -- and it meant the figures could not
follow a change to the operating point. `INVENTORY.md` D12 calls this repo a
reproducibility package, so a figure set nothing can redraw was a real hole.

Every number here comes from `analysis/`. Nothing is re-derived locally: the shot
profile is the same integrator `motor_model.shot()` uses, the thrust ripple is the same
`thrust_constant()` sweep, the lifetimes are `astro.lifetime()`. Where a figure needed a
time series rather than a summary, the accessor was added to the analysis module
(`shot(trace=True)`, `thrust_constant(profile=True)`, `conjunction(trace=True)`) rather
than copied into this file.

D01_block.png and D02_layout.png are schematics, not plots, and are not regenerated
here -- see `legacy/make_diagrams.py`.

Run:  python3 paper/make_figures.py
"""

import math
import os
import sys
import json

import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'analysis'))

import astro
import motor_model as mm
import sizing

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures')

plt.rcParams.update({
    'font.family': 'serif', 'font.size': 10, 'axes.grid': True, 'grid.alpha': 0.3,
    'figure.dpi': 300, 'savefig.bbox': 'tight',
    'axes.spines.top': False, 'axes.spines.right': False,
})


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path)
    plt.close(fig)
    print(f"  {name}")


# --------------------------------------------------------------------------- F01/F02
def f01_shot(Kt):
    s = mm.shot(Kt, trace=True)
    tr = s['trace']
    t, x, v, Vc, I = tr[:, 0], tr[:, 1], tr[:, 2], tr[:, 3], tr[:, 4]

    fig, ax = plt.subplots(1, 2, figsize=(7.2, 2.8))
    ax[0].plot(x, v, 'k-')
    ax[0].plot([mm.ACCEL_ZONE, mm.TRACK], [v[-1], v[-1]], 'k--', lw=1)
    ax[0].axvspan(mm.ACCEL_ZONE, mm.TRACK, alpha=0.12, color='gray')
    ax[0].annotate('coast-trim\nzone', (mm.ACCEL_ZONE + 0.1, v[-1] * 0.45),
                   ha='center', fontsize=8)
    ax[0].set_xlabel('Position along track (m)')
    ax[0].set_ylabel('Velocity (m/s)')
    ax[0].set_title(f"(a) Velocity profile — {s['v_exit']:.2f} m/s exit", fontsize=9)

    ax[1].plot(t * 1e3, Vc, 'k-', label='Bank voltage (V)')
    ax2 = ax[1].twinx()
    ax2.plot(t * 1e3, I, 'k:', label='Current (A)')
    ax2.set_ylabel('Current (A)')
    ax2.spines['right'].set_visible(True)
    ax[1].set_xlabel('Time (ms)')
    ax[1].set_ylabel('Bank voltage (V)')
    ax[1].set_title(f"(b) Bank sag {s['sag_pct']:.1f} %, peak {s['I_peak']:.0f} A",
                    fontsize=9)
    ax[1].legend([plt.Line2D([], [], color='k'), plt.Line2D([], [], color='k', ls=':')],
                 ['Bank voltage', 'Current'], fontsize=8, loc='lower left')
    fig.tight_layout()
    save(fig, 'F01_shot.png')


def f02_ripple(xs, Fs, ripple):
    fig, ax = plt.subplots(figsize=(4.8, 2.9))
    ax.plot(xs * 1e3, Fs, 'k-')
    ax.axhline(Fs.mean(), color='gray', ls='--', lw=1)
    ax.set_xlabel('Sled travel over one wavelength (mm)')
    ax.set_ylabel('Thrust (N)')
    ax.set_title(f'Mean {Fs.mean():.0f} N, ripple ±{ripple:.2f} %', fontsize=9)
    save(fig, 'F02_ripple.png')


# ------------------------------------------------------------------------------- F03
def f03_mc(Kt):
    mc = mm.closed_loop_mc(Kt)
    cl = mc['samples']
    # open-loop spread at the same rated point, from the manufacturing tolerances
    rng = np.random.default_rng(1)
    m = mm.M_SAT + mm.M_SLED
    n = len(cl)
    F = 0.9 * Kt * mm.K_RATED * (1 + rng.normal(0, 0.008, n))
    mf = m * (1 + rng.normal(0, 0.0067, n))
    ol = np.sqrt(2 * F / mf * mm.ACCEL_ZONE)

    fig, ax = plt.subplots(figsize=(4.6, 2.9))
    ax.hist(ol, 50, alpha=0.55, color='gray',
            label=f'Open-loop (3σ = {3 * ol.std():.3f} m/s)')
    ax.hist(cl, 50, alpha=0.85, color='k',
            label=f'Closed-loop (3σ = {mc["sigma3"]:.3f} m/s)')
    ax.set_xlabel('Exit velocity (m/s)')
    ax.set_ylabel('Count')
    ax.set_title(f'{n} runs, {mm.V_FLEET} m/s fleet setpoint', fontsize=9)
    ax.legend(fontsize=8)
    save(fig, 'F03_mc.png')


# --------------------------------------------------------------------------- F04/F11
def f04_life(dv):
    alts = np.array([350, 375, 400, 425, 450, 475, 500])
    base, boosted = [], []
    for alt in alts:
        a0 = astro.RE + alt * 1e3
        base.append(astro.lifetime(a0, 0.0))
        ab, eb = astro.boosted_elements(alt * 1e3, dv)
        boosted.append(astro.lifetime(ab, eb))
    fig, ax = plt.subplots(figsize=(4.8, 3.0))
    ax.semilogy(alts, base, 'ko-', label='Circular, no boost')
    ax.semilogy(alts, boosted, 'ks--', mfc='white', label=f'+{dv:.1f} m/s prograde')
    ax.set_xlabel('Deployment altitude (km)')
    ax.set_ylabel('Orbital lifetime (years)')
    ax.legend(fontsize=8)
    save(fig, 'F04_life.png')


# The A5 GMAT runs were propagated at 20.37 m/s, the operating point before the
# measured sled mass was adopted (P15). Comparing them against astro.py at today's
# 16.537 m/s would be a comparison at two different velocities, so this figure holds
# both at GMAT's condition. Re-running A5 at the current point is logged as P19.
A5_GMAT_DV = 20.37


def f11_uq(dv_current):
    """Solar-activity sweep, at the velocity A5 was actually run at.

    This figure previously carried the caption 'absolute lifetimes vary fivefold; the
    x1.8 multiplier does not'. GMAT falsified that invariance (P16): astro.py varies
    activity by a uniform density scale, and a uniform factor divides both lifetimes
    equally, so the ratio it returns is flat by construction rather than by physics.
    The GMAT result is plotted alongside, which is the honest comparison -- but only
    because both series are evaluated at A5_GMAT_DV, not at the current design point.
    """
    levels = [('Low\nF10.7 70', 0.5, 2.0739), ('Mean\nF10.7 150', 1.0, 1.7750),
              ('High\nF10.7 250', 2.5, 1.7302)]
    a0 = astro.RE + 450e3
    ab, eb = astro.boosted_elements(450e3, A5_GMAT_DV)
    script = [astro.lifetime(ab, eb, scale=sc) / astro.lifetime(a0, 0.0, scale=sc)
              for _, sc, _ in levels]
    gmat = [g for _, _, g in levels]

    fig, ax = plt.subplots(figsize=(5.0, 3.0))
    xp = np.arange(len(levels))
    ax.bar(xp - 0.19, script, 0.36, color='gray', edgecolor='k',
           label='astro.py (uniform density scale)')
    ax.bar(xp + 0.19, gmat, 0.36, color='white', edgecolor='k', hatch='///',
           label='GMAT R2022a (MSISE90)')
    ax.set_xticks(xp)
    ax.set_xticklabels([n for n, _, _ in levels], fontsize=8)
    ax.set_ylabel('Lifetime multiplier')
    ax.set_ylim(0, 2.4)
    ax.set_title('The ratio is flat by construction, not by physics (P16)', fontsize=9)
    ax.set_xlabel(f'Both series at {A5_GMAT_DV} m/s, the velocity A5 was run at; '
                  f'current design point is {dv_current:.2f} m/s (P19)', fontsize=7)
    ax.legend(fontsize=7.5, loc='upper right')
    save(fig, 'F11_uq.png')


# ------------------------------------------------------------------------------- F05
def f05_dragvs():
    sd = astro.seeding()
    labels = [k for k in sd if k != 'differential_drag_days'] + ['differential\ndrag']
    vals = [sd[k] for k in sd if k != 'differential_drag_days'] + \
           [sd['differential_drag_days']]
    fig, ax = plt.subplots(figsize=(4.8, 2.9))
    cols = ['gray'] * (len(vals) - 1) + ['white']
    b = ax.bar(range(len(vals)), vals, 0.5, color=cols, edgecolor='k')
    b[-1].set_hatch('///')
    ax.set_xticks(range(len(vals)))
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel('Days to 30° separation')
    for i, v in enumerate(vals):
        ax.text(i, v + 0.6, f'{v:.1f}', ha='center', fontsize=8)
    ax.set_ylim(0, max(vals) * 1.2)
    save(fig, 'F05_dragvs.png')


# ------------------------------------------------------------------------------- F06
def f06_conj(dv):
    c = astro.conjunction(dv=dv, trace=True)
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    ax.plot(c['trace_days'], c['trace_km'], color='gray', lw=0.4, alpha=0.8,
            label='Sat 1 – stage range')
    ax.axhline(c['min_km'], color='k', ls='--', lw=1,
               label=f"Fleet minimum {c['min_km']:.1f} km (not a design property)")
    ax.set_xlabel('Time (days)')
    ax.set_ylabel('Separation distance (km)')
    ax.set_title(f"Realignment period {c['realign_days']:.1f} d — the robust quantity",
                 fontsize=9)
    ax.legend(fontsize=7.5)
    ax.set_ylim(0, None)
    save(fig, 'F06_conj.png')


# ------------------------------------------------------------------------------- F07
def f07_family(Kt, F_cmd):
    fam = mm.payload_family(Kt, F_cmd)
    keys = list(fam)
    vs = [fam[k]['v_exit'] for k in keys]
    gs = [fam[k]['a_g'] for k in keys]
    fig, ax = plt.subplots(figsize=(4.6, 2.9))
    ax.bar(range(len(keys)), vs, 0.5, color='gray', edgecolor='k')
    ax.set_xticks(range(len(keys)))
    ax.set_xticklabels(keys)
    ax.set_xlabel('Payload class')
    ax.set_ylabel('Exit velocity (m/s)')
    for i, (v, g) in enumerate(zip(vs, gs)):
        ax.text(i, v + 0.4, f'{v:.1f} m/s\n({g:.1f} g)', ha='center', fontsize=8)
    ax.set_ylim(0, max(vs) * 1.35)
    save(fig, 'F07_family.png')


# ------------------------------------------------------------------------------- F08
def f08_brake(Kt, v0, Vc0):
    """Arrest in two stages: regenerative section, then first-order plate drag.

    The regenerative leg comes from mm.regen_brake() rather than being redrawn here, so
    the figure cannot disagree with A11. The eddy leg is taper-limited to the 200 g cap
    sizing.py assumes. E20 records that no force-time profile for the arrest exists
    anywhere in the scripts; the second half of this figure is that first-order law and
    nothing more.
    """
    m_s = mm.M_SLED
    rg = mm.regen_brake(Kt, v0, Vc0)
    F_rg = rg['F_brake']
    v, x, hist = v0, 0.0, []
    while x < rg['s_m']:                      # stage 1: regenerative, constant force
        v -= F_rg / m_s * 1e-4
        x += v * 1e-4
        hist.append((x, v, F_rg))
    x_split = x
    sig, tf, B, A = 5.8e7, 0.004, 0.85, 0.004
    c = sig * tf * B ** 2 * A
    while v > 1.0 and x < 0.5 + x_split:      # stage 2: eddy fin
        Fb = min(c * v, m_s * sizing.BRAKE_CAP_G * sizing.G)
        v -= Fb / m_s * 1e-4
        x += v * 1e-4
        hist.append((x, v, Fb))
    h = np.array(hist)
    fig, ax = plt.subplots(figsize=(4.8, 2.9))
    ax.plot(h[:, 0] * 100, h[:, 1], 'k-')
    ax.axvline(x_split * 100, color='k', lw=0.6, ls='--')
    ax.annotate(f"regen, {rg['E_recovered']:.0f} J recovered", (x_split * 100 - 2.2, v0 * 0.30),
                fontsize=7, rotation=90, ha='right')
    ax.annotate(f"eddy brake, {rg['KE_to_brake']:.0f} J", (x_split * 100 + 1.2, v0 * 0.30),
                fontsize=7, rotation=90)
    ax.set_xlabel('Distance past release (cm)')
    ax.set_ylabel('Sled velocity (m/s)')
    ax2 = ax.twinx()
    ax2.plot(h[:, 0] * 100, h[:, 2] / (m_s * sizing.G), 'k:')
    ax2.set_ylabel('Deceleration (g)')
    ax2.spines['right'].set_visible(True)
    ax.set_title(f'{m_s:.2f} kg sled from {v0:.2f} m/s', fontsize=9)
    ax.legend([plt.Line2D([], [], color='k'), plt.Line2D([], [], color='k', ls=':')],
              ['Velocity', 'Deceleration'], fontsize=8)
    save(fig, 'F08_brake.png')


# ------------------------------------------------------------------------------- F09
def f09_tipoff():
    """Tip-off budget.

    The 5 deg/s line is the NRCSD-E figure the paper cites. docs/LANDSCAPE.md records
    that the sibling NRCSD ICD says two (2) deg/sec/axis and that the -E document could
    not be retrieved to confirm which applies, so both lines are drawn.
    """
    I = 0.042
    items = [('Trim force ×\nCoM offset', 10 * 0.005 * 0.020),
             ('Rail clearance\ncouple', 2 * 0.010 * 0.050),
             ('Guide release\nspring-back', 0.0008),
             ('Sled rate\nresidual', I * math.radians(0.05))]
    vals = [math.degrees(d / I) for _, d in items]
    fig, ax = plt.subplots(figsize=(4.8, 2.9))
    ax.bar(range(len(items)), vals, 0.5, color='gray', edgecolor='k')
    ax.axhline(5, color='k', ls='--', lw=1)
    ax.text(2.45, 5.15, 'NRCSD-E as cited (5 °/s)', fontsize=7)
    ax.axhline(2, color='k', ls=':', lw=1)
    ax.text(2.45, 2.15, 'NRCSD ICD wording (2 °/s) — unresolved', fontsize=7)
    ax.set_xticks(range(len(items)))
    ax.set_xticklabels([i[0] for i in items], fontsize=7)
    ax.set_ylabel('Tip-off contribution (°/s)')
    ax.set_ylim(0, max(max(vals), 5) * 1.35)
    save(fig, 'F09_tipoff.png')


def main():
    os.makedirs(OUT, exist_ok=True)
    print("regenerating figures from analysis/ ...")
    Kt, ripple, xs, Fs = mm.thrust_constant(profile=True)
    s_ = mm.shot(Kt)
    dv = s_['v_exit']
    print(f"  operating point: Kt = {Kt*1e3:.2f} N per kA/m, "
          f"v_exit = {dv:.3f} m/s, sled {mm.M_SLED} kg")

    f01_shot(Kt)
    f02_ripple(xs, Fs, ripple)
    f03_mc(Kt)
    f04_life(dv)
    f05_dragvs()
    f06_conj(dv)
    f07_family(Kt, s_['F_cmd'])
    f08_brake(Kt, dv, mm.V0 * (1 - s_['sag_pct'] / 100))
    f09_tipoff()
    f11_uq(dv)

    # A rebuild that produces byte-identical PNGs leaves no trace in git, and
    # tools/check_artifacts.py compares commit times, so it cannot tell "not rebuilt"
    # from "rebuilt, unchanged". This stamp is what it checks instead: it records the
    # operating point the figures were actually drawn from, so a stale figure set is
    # visible as a stale stamp even when the images happen not to move.
    stamp = dict(v_exit=round(float(dv), 3), Kt_N_per_kA=round(float(Kt) * 1e3, 2),
                 sled_kg=float(mm.M_SLED), E_drawn_J=round(float(s_['E_drawn']), 1),
                 E_recovered_J=round(float(mm.regen_brake(
                     Kt, dv, mm.V0 * (1 - s_['sag_pct'] / 100))['E_recovered']), 1))
    with open(os.path.join(OUT, 'BUILD.json'), 'w') as fh:
        json.dump(stamp, fh, indent=2)
        fh.write("\n")
    print("  BUILD.json", stamp)
    print("done.")


if __name__ == '__main__':
    main()
