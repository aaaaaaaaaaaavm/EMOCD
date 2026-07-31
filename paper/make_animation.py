"""Animate one shot: sled position, velocity, force and current through the stroke.

The whole point of this machine is that it is dynamic, and it has so far been presented
entirely with static plots. This draws the stroke as it happens.

It imports motor_model and calls shot(trace=True), which already returns the time series, so
the animation is drawn from the same integrator the paper's numbers come from. There is no
second copy of the physics here, for the same reason make_figures.py has none: the two would
drift, and the figure would start disagreeing with the number it illustrates.

Run:  python3 paper/make_animation.py
Out:  paper/figures/shot.gif
"""
import os
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                    # noqa: E402
from matplotlib.animation import FuncAnimation, PillowWriter   # noqa: E402
import numpy as np                                 # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "analysis"))
import motor_model as mm                           # noqa: E402

FPS = 25
SECONDS = 6.0            # a 157 ms stroke stretched out enough to watch
INK = "#111318"
ACCENT = "#c1452b"
MUTED = "#8a8f98"


def build():
    Kt, _ = mm.thrust_constant()
    out = mm.shot(Kt, trace=True)
    tr = out["trace"]
    t, x, v, Vc, I = (tr[:, i] for i in range(5))
    t_ms = t * 1e3
    F = np.full_like(t, out["F_cmd"])

    n = int(FPS * SECONDS)
    idx = np.linspace(0, len(t) - 1, n).astype(int)

    fig, axes = plt.subplots(4, 1, figsize=(7.2, 8.4), sharex=True,
                             gridspec_kw=dict(hspace=0.18))
    fig.patch.set_facecolor("white")

    series = [
        (x * 1e3, "Position", "mm", (0, mm.ACCEL_ZONE * 1e3 * 1.02)),
        (v, "Velocity", "m/s", (0, out["v_exit"] * 1.08)),
        (F, "Commanded force", "N", (0, out["F_cmd"] * 1.25)),
        (I, "Bank current", "A", (0, out["I_peak"] * 1.08)),
    ]

    lines, dots = [], []
    for ax, (y, label, unit, ylim) in zip(axes, series):
        ax.plot(t_ms, y, color=MUTED, lw=1.0, alpha=0.35)
        ln, = ax.plot([], [], color=INK, lw=2.0)
        dt_, = ax.plot([], [], "o", color=ACCENT, ms=6)
        lines.append(ln)
        dots.append(dt_)
        ax.set_ylabel(f"{label}\n[{unit}]", fontsize=9)
        ax.set_xlim(0, t_ms[-1])
        ax.set_ylim(*ylim)
        ax.grid(alpha=0.15, lw=0.6)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    axes[-1].set_xlabel("time [ms]", fontsize=9)

    title = fig.suptitle("", fontsize=11, y=0.965)
    fig.text(0.5, 0.012,
             f"one shot: 3U payload to {out['v_exit']:.2f} m/s at {out['a_g']:.1f} g, "
             f"{mm.ACCEL_ZONE*1e3:.0f} mm stroke in {out['t_ms']:.1f} ms",
             ha="center", fontsize=8.5, color=MUTED)

    def frame(k):
        j = idx[k]
        for (y, *_), ln, dt_ in zip(series, lines, dots):
            ln.set_data(t_ms[:j + 1], y[:j + 1])
            dt_.set_data([t_ms[j]], [y[j]])
        title.set_text(f"t = {t_ms[j]:6.1f} ms    x = {x[j]*1e3:6.0f} mm    "
                       f"v = {v[j]:5.2f} m/s")
        return lines + dots + [title]

    return fig, frame, n, out


def main():
    fig, frame, n, out = build()
    dest = os.path.join(HERE, "figures", "shot.gif")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    anim = FuncAnimation(fig, frame, frames=n, blit=False)
    anim.save(dest, writer=PillowWriter(fps=FPS))
    plt.close(fig)
    kb = os.path.getsize(dest) / 1024
    print(f"wrote {os.path.relpath(dest)}  ({n} frames, {kb:.0f} kB)")
    print(f"  exit velocity {out['v_exit']:.3f} m/s at {out['a_g']:.2f} g, "
          f"{out['t_ms']:.1f} ms, peak {out['I_peak']:.0f} A")
    # Same reason make_figures.py writes one: a rebuild whose GIF comes out
    # byte-identical is invisible to git, so tools/check_artifacts.py has nothing to
    # compare commit times against. The stamp is what it checks.
    stamp = dict(v_exit=round(float(out['v_exit']), 3), a_g=round(float(out['a_g']), 2),
                 t_ms=round(float(out['t_ms']), 1), I_peak=round(float(out['I_peak']), 1),
                 frames=n)
    with open(os.path.join(HERE, "figures", "BUILD_anim.json"), "w") as fh:
        json.dump(stamp, fh, indent=2)
        fh.write("\n")


if __name__ == "__main__":
    main()
