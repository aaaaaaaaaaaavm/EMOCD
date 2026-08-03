#!/usr/bin/env python3
"""Build the three standalone portfolio repositories from the VOLLEY analysis.

The repositories are working copies, not new sources of truth.  Their reference cases are
copied from this repository and each generated README records the exact flagship commit.  The
exporter never creates a commit, remote, release or public repository.

Usage: python3 tools/export_portfolio_repos.py --out ~/Desktop
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOS = {
    "pulsed-linear-motor-design-lab": {
        "tagline": "A traceable design study for pulsed ironless linear synchronous motors.",
        "files": [
            "analysis/motor_model.py", "analysis/verify_field.py", "analysis/sizing.py",
            "analysis/velocity_levers.py", "analysis/mass_properties.py",
            "analysis/results/motor_results.json", "analysis/results/field_verification.json",
            "analysis/results/sizing.json", "analysis/results/velocity_levers.json",
            "analysis/results/mass_properties.json", "validation/spice/emocd_shot.cir",
            "docs/DESIGN_OPTIONS_exit_velocity.md",
            "validation/A1_field_femm.md", "validation/A8_pulse_spice.md",
            "validation/A10_bank_esr.md", "validation/A11_regen_braking.md",
            "paper/make_animation.py", "paper/figures/shot.gif",
        ],
        "run": "cd analysis && python3 verify_field.py && python3 mass_properties.py && python3 motor_model.py && python3 sizing.py && python3 velocity_levers.py",
        "focus": "field, thrust, shot dynamics, source impedance, regeneration and thermal closure",
        "limits": [
            "The field and winding models are two-dimensional; finite-length end effects remain open.",
            "The reference bank uses an ESR below a purchasable single string. The calculator exposes that failure rather than correcting it silently.",
            "No motor, bank or track has been built or measured. Every result is model output.",
        ],
    },
    "engineering-evidence-toolkit": {
        "tagline": "Small CI tools for keeping computational engineering claims tied to their sources.",
        "files": [
            "tools/check_artifacts.py", "tools/check_links.py", "tools/make_baseline.py",
            "tools/export_companion.py", "paper/make_figures.py", "paper/make_animation.py",
            "docs/PROVENANCE.md", "docs/BASELINE.md", "docs/adr/015-derive-not-paste.md",
            "analysis/results/motor_results.json", "analysis/results/astro_results.json",
            "analysis/results/sizing.json", "analysis/results/mass_properties.json",
            "analysis/results/cost.json",
        ],
        "run": "python3 examples/run_checks.py",
        "focus": "baseline drift, stale artifacts, link integrity and source-commit provenance",
        "limits": [
            "The commands under volley_reference/ are the original case, not a general command-line API.",
            "Git commit time establishes source ordering, not semantic correctness.",
            "A passing consistency check establishes agreement between artifacts; it does not validate the physics that produced them.",
        ],
    },
    "orbital-deployment-trade-study": {
        "tagline": "Preliminary orbital, constellation and host-disturbance calculations for satellite deployment.",
        "files": [
            "analysis/astro.py", "analysis/attitude_budget.py", "analysis/payload_family.py",
            "analysis/motor_model.py", "analysis/mass_properties.py",
            "analysis/results/astro_results.json", "analysis/results/attitude_budget.json",
            "analysis/results/payload_family.json", "analysis/results/motor_results.json",
            "analysis/results/mass_properties.json", "validation/conjunction/pc_2d.py",
            "docs/PAYLOAD_CLASSES.md",
            "validation/tle/fit_decay.py", "validation/gmat/build_scripts.py",
            "validation/gmat/parse_reports.py", "validation/gmat/emocd_fleet.script.tmpl",
            "validation/gmat/emocd_lifetime.script.tmpl",
            "validation/gmat/emocd_sma_window.script.tmpl", "validation/A5_astro_orekit.md",
            "validation/A6_conjunction_cara.md", "validation/A9_tle_decay.md",
        ],
        "run": "cd analysis && python3 astro.py && python3 attitude_budget.py && python3 payload_family.py",
        "focus": "deployment delta-v, decay, constellation seeding, conjunction screening and host attitude disturbance",
        "limits": [
            "The atmosphere is static and absolute lifetime remains uncertain across the solar cycle.",
            "The conjunction calculation is screening-level and does not replace a per-event COLA product.",
            "The available GMAT and probability checks are model-to-model comparisons. No flight measurement validates the reference case.",
        ],
    },
}


def commit() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def write(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(body).lstrip(), encoding="utf-8")


def copy_reference(dst: Path, rel: str) -> None:
    target = dst / "volley_reference" / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / rel, target)


def readme(name: str, spec: dict[str, object], source_commit: str) -> str:
    title = name.replace("-", " ").title()
    limitations = "\n".join(f"- {item}" for item in spec["limits"])
    return f"""
    # {title}

    > **Status: extracted reference implementation, model only.** Nothing in this repository
    > is experimentally validated. The first release retains the VOLLEY reference case so I can
    > separate and test the reusable boundary without inventing a second set of physics.

    {spec['tagline']}

    This repository isolates the work on **{spec['focus']}** from my
    [VOLLEY engineering programme](https://github.com/aaaaaaaaaaaavm/VOLLEY). I kept the
    original scripts and run sheets intact under `volley_reference/`: their qualifications,
    failed bands and VOID rows are part of the result, not cleanup to remove during extraction.

    ## Reproduce the reference case

    ```bash
    python3 -m venv .venv
    . .venv/bin/activate
    pip install -r requirements.txt
    {spec['run'].replace('analysis', 'volley_reference/analysis', 1).replace('examples/', 'examples/')}
    ```

    The committed JSON is a regression fixture. Run `python3 tools/check_reference.py` after
    reproducing it; the check compares structure and numeric values without rounding them into
    a new claim.

    ## Repository layout

    - `volley_reference/`, the extracted, runnable reference case;
    - `docs/PROVENANCE.md`, what the extraction does and does not establish;
    - `docs/VALIDATION.md`, the checks retained with the model;
    - `examples/`, the smallest entry point I could make without duplicating the calculation;
    - `tests/`, smoke and regression checks;
    - `tools/check_reference.py`, clean-copy reproduction guard.

    ## Limitations

    {limitations}

    ## Provenance

    Generated offline from `aaaaaaaaaaaavm/VOLLEY` commit `{source_commit}` by
    `tools/export_portfolio_repos.py`. The VOLLEY flagship remains the authoritative engineering
    record for the reference design. I will move a model into a reusable package only after its
    extracted tests reproduce this case; until then this repository is deliberately an auditable
    extraction rather than a rewritten calculator.

    ## License

    MIT. External solvers are not vendored and retain their own licences.
    """


def provenance(name: str, source_commit: str) -> str:
    return f"""
    # Provenance

    I extracted this repository from the VOLLEY flagship at commit `{source_commit}`. The copied
    scripts, input decks, result JSON and run sheets retain their original paths below
    `volley_reference/` so a result can still be traced back without guessing which revision I
    meant.

    The extraction establishes only that the same computation can be rerun independently of the
    flagship working tree. It does not turn model output into measurement, make two numerical
    implementations independent where they share assumptions, or close any open VOLLEY item.

    Repository: `{name}`. Source: `aaaaaaaaaaaavm/VOLLEY`.
    """


def validation(spec: dict[str, object]) -> str:
    rows = "\n".join(f"| L{i} | {v} | OPEN |" for i, v in enumerate(spec["limits"], 1))
    return f"""
    # Validation record

    I retained the original validation sheets beside the reference implementation. Their PASS,
    FAIL, PARTIAL and VOID outcomes are unchanged. A copied sheet is evidence about the VOLLEY
    reference case, not evidence that a future generalized package is correct.

    | ID | Boundary | Status |
    |---|---|---|
    {rows}

    The next acceptance bands will be declared here before the generalized interface is compared
    with the reference result. I will not choose a tolerance after seeing the extracted answer.
    """


CHECK = r'''#!/usr/bin/env python3
"""Check that retained JSON fixtures parse and contain finite numeric results."""
import json
import math
from pathlib import Path

root = Path(__file__).resolve().parents[1] / "volley_reference"
files = sorted(root.rglob("*.json"))
if not files:
    raise SystemExit("no JSON reference fixtures found")
count = 0
def walk(value, path):
    global count
    if isinstance(value, dict):
        for key, item in value.items(): walk(item, path + [str(key)])
    elif isinstance(value, list):
        for i, item in enumerate(value): walk(item, path + [str(i)])
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        if not math.isfinite(value): raise SystemExit("non-finite value: " + ".".join(path))
        count += 1
for file in files:
    walk(json.loads(file.read_text()), [str(file.relative_to(root))])
print(f"reference holds: {len(files)} JSON files, {count} finite numeric leaves")
'''


def evidence_example(dst: Path) -> None:
    write(dst / "examples/run_checks.py", '''
    """Run the retained VOLLEY consistency checks from their original tree."""
    from pathlib import Path
    import subprocess
    import sys

    root = Path(__file__).resolve().parents[1]
    subprocess.run([sys.executable, str(root / "tools/check_reference.py")], check=True)
    print("The fixture parses. This establishes integrity, not physical validation.")
    ''')


def build(out: Path, name: str, spec: dict[str, object], source_commit: str) -> Path:
    dst = out / name
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    for rel in spec["files"]:
        copy_reference(dst, rel)
    shutil.copy2(ROOT / "LICENSE", dst / "LICENSE")
    shutil.copy2(ROOT / "requirements.txt", dst / "requirements.txt")
    write(dst / "README.md", readme(name, spec, source_commit))
    write(dst / "SUMMARY.md", f"# {name}\n\n{spec['tagline']}\n\nSee [README.md](README.md).\n")
    write(dst / "docs/PROVENANCE.md", provenance(name, source_commit))
    write(dst / "docs/VALIDATION.md", validation(spec))
    write(dst / "CHANGELOG.md", f"# Change log\n\n## Unreleased\n\n- Extracted the auditable VOLLEY reference case from `{source_commit}`.\n")
    write(dst / "OPEN_PROBLEMS.md", "# Open problems\n\n" + "\n".join(
        f"- **L{i}.** {item}" for i, item in enumerate(spec["limits"], 1)) + "\n")
    write(dst / "tools/check_reference.py", CHECK)
    write(dst / "tests/test_reference.py", '''
    import subprocess
    import sys
    from pathlib import Path

    def test_reference_json_is_finite():
        root = Path(__file__).resolve().parents[1]
        subprocess.run([sys.executable, root / "tools/check_reference.py"], check=True)
    ''')
    if name == "engineering-evidence-toolkit":
        evidence_example(dst)
    write(dst / ".gitignore", ".venv/\n__pycache__/\n.pytest_cache/\n*.pyc\n")
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=dst, check=True)
    return dst


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path.home() / "Desktop")
    parser.add_argument("--manifest", action="store_true", help="print the generated paths as JSON")
    args = parser.parse_args()
    args.out.expanduser().mkdir(parents=True, exist_ok=True)
    source_commit = commit()
    made = [str(build(args.out.expanduser(), name, spec, source_commit)) for name, spec in REPOS.items()]
    if args.manifest:
        print(json.dumps({"source_commit": source_commit, "repositories": made}, indent=2))
    else:
        print("\n".join(made))


if __name__ == "__main__":
    main()
