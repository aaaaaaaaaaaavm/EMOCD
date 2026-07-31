"""Check that every built artifact is newer than the source it was built from.

WHY THIS EXISTS
---------------
Every other guard here compares an artifact to a *script*: make_baseline.py --check compares
BASELINE.md to the JSON, _check_operating_point() compares two modules, check_links.py compares
links to files. Nothing compared a built file to the thing it was built from.

So on 2026-07-30 paper.tex was corrected twice, for the bank ESR and for a retracted
coilgun-efficiency claim, and the PDF was not rebuilt. The published PDF -- the artifact linked
from the Pages site and shipped inside VOLLEY-paper -- went on printing 2.80 kJ, 20 % efficiency
and the retracted figure, for as long as nobody thought to look. This is that check.

WHY MTIMES WOULD NOT WORK
-------------------------
Git does not record modification times. A fresh clone writes every file at checkout time, so
mtime comparisons are meaningless the moment anyone clones: they would either all pass or all
fail depending on checkout order, and neither answer means anything.

The commit in which each path last changed is the durable fact. `git log -1 --format=%ct -- path`
gives it, and it is identical in every clone. That is what this compares.

USAGE
    python3 tools/check_artifacts.py
Exits non-zero if any artifact is older than its source.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (artifact, [sources]) -- the artifact must not predate any of its sources.
PAIRS = [
    ("paper/VOLLEY_IEEE_Conference.pdf", ["paper/paper.tex"]),
    ("paper/cv/cv.tex", ["paper/cv/make_cv.py", "analysis/results/motor_results.json"]),
    ("paper/cv/cv.pdf", ["paper/cv/cv.tex"]),
    ("docs/BASELINE.md", ["analysis/results/motor_results.json",
                          "analysis/results/sizing.json",
                          "analysis/results/astro_results.json",
                          "tools/make_baseline.py"]),
    # The figures are checked through their build stamp, not through the PNGs. A rebuild
    # whose output happens to be byte-identical leaves nothing in git, so commit times
    # cannot distinguish "not rebuilt" from "rebuilt, unchanged" -- and F01 hit exactly
    # that on 2026-07-31, when the shot was untouched but the figure script was not.
    # make_figures.py writes BUILD.json with the operating point it drew from, so the
    # stamp moves whenever the figures are actually regenerated.
    ("paper/figures/BUILD.json", ["analysis/results/motor_results.json",
                                  "paper/make_figures.py"]),
    ("paper/figures/BUILD_anim.json", ["analysis/results/motor_results.json",
                                       "paper/make_animation.py"]),
]


def last_commit_time(path):
    """Unix time of the commit that last touched `path`, or None if never committed."""
    out = subprocess.run(
        ["git", "-C", ROOT, "log", "-1", "--format=%ct", "--", path],
        capture_output=True, text=True).stdout.strip()
    return int(out) if out else None


def main():
    dirty = subprocess.run(["git", "-C", ROOT, "status", "--porcelain"],
                           capture_output=True, text=True).stdout.strip()
    if dirty:
        print("note: working tree is dirty, so this compares committed state only.\n")

    stale, missing, ok = [], [], 0
    for artifact, sources in PAIRS:
        if not os.path.exists(os.path.join(ROOT, artifact)):
            missing.append(artifact)
            continue
        a_time = last_commit_time(artifact)
        if a_time is None:
            missing.append(f"{artifact} (never committed)")
            continue
        for src in sources:
            s_time = last_commit_time(src)
            if s_time is None:
                continue
            if a_time < s_time:
                behind = (s_time - a_time) / 3600.0
                stale.append((artifact, src, behind))
        ok += 1

    for artifact, src, behind in stale:
        print(f"STALE  {artifact}")
        print(f"       built before {src}, which changed {behind:.1f} h later")
        print(f"       rebuild it, or the published artifact contradicts its own source")
    for m in missing:
        print(f"MISSING  {m}")

    if not stale and not missing:
        print(f"artifacts: {ok} checked, all newer than their sources")
        return 0
    print(f"\n{len(stale)} stale, {len(missing)} missing, of {len(PAIRS)} checked")
    return 1


if __name__ == "__main__":
    sys.exit(main())
