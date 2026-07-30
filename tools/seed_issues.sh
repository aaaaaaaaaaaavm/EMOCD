#!/usr/bin/env bash
#
# File the live work as GitHub issues, so the programme board has content.
#
# The Markdown ledgers stay AUTHORITATIVE. OPEN_PROBLEMS.md and docs/ROADMAP.md are the record;
# these issues are a view onto them and each links back. If the two ever disagree, the Markdown
# is right and the issue is stale.
#
# Deliberately limited to the roadmap sequence, the currently-open HIGH defects, and the first
# measurement. Filing all 24 P-items and 24 E-items, most of them closed or low, would bury the
# live work under the audit trail.
#
#   ./tools/bootstrap_repos.sh    # enables Issues first; they are disabled by default here
#   ./tools/seed_issues.sh
#
# Safe to re-run: an issue whose exact title already exists is skipped, not duplicated.
#
set -euo pipefail
OWNER="${OWNER:-aaaaaaaaaaaavm}"
REPO_NAME="${REPO_NAME:-VOLLEY}"         # tracks the repository; override if not yet renamed
REPO="$OWNER/$REPO_NAME"
B="https://github.com/$OWNER/$REPO_NAME/blob/main"

command -v gh >/dev/null || { echo "gh CLI not found"; exit 1; }
gh issue list --repo "$REPO" --limit 1 >/dev/null 2>&1 || {
  echo "Issues are disabled on $REPO. Run tools/bootstrap_repos.sh, or enable them in"
  echo "Settings > General > Features > Issues."; exit 1; }

for L in "defect:d73a4a" "validation:0e8a16" "documentation:0075ca" \
         "phase-I:5319e7" "phase-II:cccccc" "blocking:b60205" \
         "stale-operating-point:fbca04" "prior-art:1d76db"; do
  gh label create "${L%%:*}" --repo "$REPO" --color "${L##*:}" --force >/dev/null 2>&1 || true
done

file () {  # title, labels, body
  gh issue list --repo "$REPO" --state all --search "\"$1\" in:title" --json title \
    --jq '.[].title' 2>/dev/null | grep -qxF "$1" && { echo "  = $1"; return; }
  gh issue create --repo "$REPO" --title "$1" --label "$2" --body "$3" >/dev/null
  echo "  + $1"
}

echo "== roadmap =="

file "Source the bank ESR, or measure it" "validation,phase-I" \
"What keeps **E17** open now that the modelling gap is closed.

A8-R found the analytic model missing the bank's series-resistance loss entirely, and P24 propagated the fix: \`motor_model.py\` now solves for the current at the bank terminal and integrates I^2 R. The two methods agree on peak current to **0.01 %** where they differed by 5 %.

**But the 12 mohm itself has no source.** It reaches this repository through \`docs/EMOCD_Computation_Results_C1-C10.md\`, which is superseded, and no cell datasheet has been checked against it. A number that now moves the headline energy and efficiency should not rest on that.

Cheapest close: read the ESR off the datasheet for the 3.0 V / 190 F cell the bank is specified from, multiply by 32 in series, and compare. If it disagrees, the shot energy moves again. Record: [OPEN_PROBLEMS.md]($B/OPEN_PROBLEMS.md) E17 and P24."

file "A7, separation and tip-off" "validation,phase-I" \
"Gates the momentum-transfer option and closes E7. \`pychrono\` ships on conda-forge rather than PyPI, which is the likely cause of the 'not installable' note.

**Check the acceptance band against its source first:** the run sheet declares 5 deg/s citing NRCSD-E, and the sibling NRCSD ICD says 2 deg/s. A band that misquotes its source is no protection."

file "Close P17, inter-array attraction is 37 percent high" "defect,phase-I" \
"\`sizing.py\` gives 3672 N from a flat-plate Maxwell formula; a 3-D field-gradient integration converges to 2686.6 N. The mechanism is understood: Maxwell stress needs the mean of B squared, and the formula uses the square of mean B.

A4's conclusions do not reverse, since the real load is lighter, but its input was taken on trust. **Write the run sheet with a band declared in advance, then propagate \`sizing.py\` once.** The correction moves plate stress, retention-gate sizing and the A4 load together."

file "Re-run A5 once the sled mass is settled" "validation,phase-I,stale-operating-point" \
"All three GMAT legs were propagated at 20.37 m/s (P19). Days of wall time for the low-activity leg, so schedule it rather than babysit it.

**Do not re-run before the chassis question is settled**, or the same staleness recurs."

file "A6, conjunction probability" "validation,phase-I" \
"Around 50 lines of scipy against the OEM ephemerides \`validation/gmat/\` already emits. No MATLAB needed. E18's covariance problem stands regardless: state the assumption rather than pretending to a covariance that does not exist."

file "A9, decay against flown CubeSats" "validation,phase-I" \
"**The only analysis specified anywhere that compares the model against something that happened**, rather than against another model.

Bands declared and the script written ([validation/tle/fit_decay.py]($B/validation/tle/fit_decay.py)); blocked only by network policy where it was authored. Needs a free Space-Track account."

file "Adopt reachable-domain analysis (PII-6)" "phase-II,prior-art" \
"Feng et al. compute a 3-D envelope of the orbits one shot makes available, reconstructed with an alpha-shape algorithm. This project reports a scalar lifetime multiplier, which answers a smaller question.

Their method is better, and it is the single strongest thing to take from the prior-art review. See [docs/PRIOR_ART.md]($B/docs/PRIOR_ART.md) and PII-6 in the lab repository."

echo "== open HIGH defects =="

file "P22, the novelty claim rested on prior art that was not cited" "defect,phase-I,prior-art" \
"A literature check found published work on this exact concept that the paper cited nowhere, one paper of it published eight months before this repository went public.

Two claims were retracted and one ADR argument was found false. That work is done. **What keeps this open** is that the reachable-domain method should be adopted (PII-6), and E24 remains unmodelled.

Full record: [docs/PRIOR_ART.md]($B/docs/PRIOR_ART.md)."

file "P24, no script carried the bank ESR and the placeholder was 2x high" "defect,phase-I" \
"A8-R failed its energy-closure band at 97.0 %. The gap was **85.5 J per shot** of bank ESR dissipation that the circuit deck carried and no analysis script did.

Propagated: \`motor_model.py\` solves for the current at the bank terminal rather than at the capacitor. Energy drawn 2795.6 to **2881.2 J**, peak current 330.3 to **346.8 A**, sag 5.19 to **5.35 %**, efficiency 19.6 to **19.0 %**. Exit velocity, stroke time and dispersion unchanged.

**Two things worth more than the fix.** The 5 % peak-current gap that A8 and A8-R both blamed on the integrator was this term; corrected, the two methods agree to **0.01 %**. And the energy budget had been closing at 100.0 % while missing a real 86 J, because both sides of the ledger omitted it.

This issue stays open only for the sourcing of the 12 mohm. See the ESR issue."

file "P9, envelope exceeds ESPA Grande by 44 percent" "defect,phase-II" \
"1839 mm closed against the roughly 1270 mm class, because the brake sits beyond the 1500 mm release point and the enclosure spans it.

The *statement* is Phase I and the paper now makes it honestly. The *fix* is Phase II and needs an owner decision on target host class. See [docs/PHASE_II.md]($B/docs/PHASE_II.md) PII-4."

file "P14, G3-D5: Halbach arrays never re-centred" "defect,phase-I,blocking" \
"The chassis grew from 360 to 488 mm and \`sled.halbach_array_x_start = 230 mm\` was inherited from the shorter one. **Array position relative to the winding is what K_t depends on**, so this may invalidate K_t independently of A1.

Also blocking: **G3-D2**, the track has no roller channels or guide flanges modelled at all, so the rollers have nothing to run in."

file "P16, ballistic-coefficient invariance still untested" "defect,phase-I" \
"The solar-activity half is falsified and the paper is corrected. The BC half is **proven a tautology in \`astro.py\`**: \`scale\` and \`1/BC\` occupy the same multiplicative slot, so the sweep cannot move the ratio it claims to test.

Nobody has run GMAT at BC 40 and 90 to find the true dependence. **Until then the honest position is unknown, not invariant.**"

file "P10, enclosure, radiator and avionics absent from the mass rollup" "defect,phase-I" \
"The 76.9 kg dry figure excludes them, which means the 6.4 kg-per-satellite result in \`docs/LANDSCAPE.md\` rests on an incomplete number."

file "E24, magazine indexing disturbance is unmodelled" "defect,phase-I,prior-art" \
"Found by reading a competitor's problem statement rather than by examining this design. Xu et al. build a cost model for the attitude disturbance caused by moving CubeSats around inside a deployer, and optimise their transfer paths against it.

This project budgets recoil from the shot, 66.1 N.s, and nothing from the indexing between shots. Twelve satellites feed from two transverse cassettes, so a few kilograms translate across the structure between every pair of shots.

**The quantity that matters is residual attitude rate at trigger, and the settling time to reach it.** Neither exists anywhere in this repository. The bookkeeping is cheap: a rigid-body momentum budget, not a new solver."

echo "== first measurement =="

file "B-1, Halbach pair on a gaussmeter" "validation,phase-I" \
"**The cheapest route to this project's first measured number at any scale.** Roughly the price of two magnets and a Hall probe.

Every headline is downstream of a field model that has now been checked twice against other models and never against a magnet. A gaussmeter is a different *kind* of evidence.

Bands are declared in [docs/BENCHTOP_TESTS.md]($B/docs/BENCHTOP_TESTS.md), and are now derived from a per-term error budget rather than chosen. Two traps are documented there: a two-block bench pair built poles-facing reads exactly zero field, and the load cell must be sized to the smallest force in the sweep rather than the largest."

echo
echo "Done. Next: ./tools/setup_project.sh"
