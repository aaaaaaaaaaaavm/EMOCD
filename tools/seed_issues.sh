#!/usr/bin/env bash
#
# File the live work as GitHub issues, so the programme board has content.
#
# The Markdown ledgers stay AUTHORITATIVE. OPEN_PROBLEMS.md and ROADMAP.md are the record;
# these issues are a view onto them and each links back. If the two ever disagree, the
# Markdown is right and the issue is stale.
#
# Deliberately limited to the roadmap sequence and the currently-open HIGH defects. Filing all
# 19 P-items and 23 E-items -- most of them closed or low -- would bury the live work.
#
#   ./tools/bootstrap_repos.sh    # enables Issues first; they are disabled by default here
#   ./tools/seed_issues.sh
#
set -euo pipefail
OWNER="${OWNER:-aaaaaaaaaaaavm}"
REPO="$OWNER/EMOCD"
B="https://github.com/$OWNER/EMOCD/blob/main"

command -v gh >/dev/null || { echo "gh CLI not found"; exit 1; }
gh issue list --repo "$REPO" --limit 1 >/dev/null 2>&1 || {
  echo "Issues are disabled on $REPO. Run tools/bootstrap_repos.sh, or enable them in"
  echo "Settings > General > Features > Issues."; exit 1; }

for L in "defect:d73a4a" "validation:0e8a16" "documentation:0075ca" \
         "phase-I:5319e7" "phase-II:cccccc" "blocking:b60205"; do
  gh label create "${L%%:*}" --repo "$REPO" --color "${L##*:}" --force >/dev/null 2>&1 || true
done

file () {  # title, labels, body
  gh issue list --repo "$REPO" --state all --search "\"$1\" in:title" --json title \
    --jq '.[].title' 2>/dev/null | grep -qxF "$1" && { echo "  = $1"; return; }
  gh issue create --repo "$REPO" --title "$1" --label "$2" --body "$3" >/dev/null
  echo "  + $1"
}

echo "== roadmap =="
file "A1 — airgap magnetostatic field" "validation,phase-I,blocking" \
"K_t = 11.22 N per kA/m is checked only analytic-against-analytic. **Every number in the baseline is downstream of it**, so if it is wrong everything after is re-work.

FEMM 4.2 runs under Wine; Elmer and GetDP+Gmsh are native Linux and are meshed differential FEM, which is the bar E2 sets. The DXF and run sheet already exist in \`analysis/femm/\` — this is an install problem, not a modelling one.

Band declared in advance: [validation/A1_field_femm.md]($B/validation/A1_field_femm.md). Record: [ROADMAP.md]($B/ROADMAP.md) step 1."

file "Re-run A8 at the current operating point" "validation,phase-I" \
"Closes half of P19. \`validation/spice/emocd_shot.cir\` still carries the superseded operating point — peak current moved 392 → 330 A and pulse 128 → 157 ms, which is exactly what A8 exists to check.

Minutes of work. **Re-read the declared bands before running, not after.** Record: [OPEN_PROBLEMS.md]($B/OPEN_PROBLEMS.md) P19."

file "Rib-stiffened chassis — design the lighter sled" "phase-II" \
"A4 passes the drawn plate with a **17× stress margin**, so mass can come out — but nobody has designed the lighter chassis, which is why the 60 % pocketing row in \`docs/DESIGN_OPTIONS_exit_velocity.md\` is unsupported.

Uniform thinning is nearly worthless (deflection goes as 1/t³). Entry criterion in [docs/PHASE_II.md]($B/docs/PHASE_II.md) PII-2."

file "A7 — separation and tip-off" "validation,phase-I" \
"Gates the momentum-transfer option and closes E7. \`pychrono\` ships on conda-forge, not PyPI — the likely cause of the 'not installable' note.

**Check the acceptance band against its source first:** the run sheet declares ≤5 °/s citing NRCSD-E, and the sibling NRCSD ICD says 2 °/s. A band that misquotes its source is no protection."

file "Close P17 — inter-array attraction is 37 % high" "defect,phase-I" \
"\`sizing.py\` gives 3672 N from a flat-plate Maxwell formula; a 3-D field-gradient integration converges to 2686.6 N. Mechanism understood: Maxwell stress needs mean(B²), the formula uses mean(B)².

A4's conclusions do not reverse — the real load is lighter — but its input was taken on trust. **Write the run sheet with a band declared in advance, then propagate \`sizing.py\` once**; the correction moves plate stress, retention-gate sizing and the A4 load together."

file "Re-run A5 once the sled mass is settled" "validation,phase-I" \
"All three GMAT legs were propagated at 20.37 m/s (P19). Days of wall time for the low-activity leg — schedule it, do not babysit it.

**Do not re-run before the chassis question is settled**, or the same staleness recurs."

file "A6 — conjunction probability" "validation,phase-I" \
"~50 lines of scipy against the OEM ephemerides \`validation/gmat/\` already emits. No MATLAB needed. E18's covariance problem stands regardless — state the assumption rather than pretending to a covariance that does not exist."

file "A9 — decay against flown CubeSats" "validation,phase-I" \
"**The only analysis specified anywhere that compares the model against something that happened** rather than against another model.

Bands declared and script written ([validation/tle/fit_decay.py]($B/validation/tle/fit_decay.py)); blocked only by network policy where it was authored. Needs a free Space-Track account."

echo "== open HIGH defects =="
file "P9 — envelope exceeds ESPA Grande by 44 %" "defect,phase-II" \
"1839 mm closed against the ~1270 mm class, because the brake sits beyond the 1500 mm release point and the enclosure spans it.

The *statement* is Phase I and the paper now makes it honestly. The *fix* is Phase II and needs an owner decision on target host class — see [docs/PHASE_II.md]($B/docs/PHASE_II.md) PII-4."

file "P14 — G3-D5: Halbach arrays never re-centred" "defect,phase-I,blocking" \
"The chassis grew 360 → 488 mm and \`sled.halbach_array_x_start = 230 mm\` was inherited from the shorter one. **Array position relative to the winding is what K_t depends on**, so this may invalidate K_t independently of A1.

Also blocking: **G3-D2**, the track has no roller channels or guide flanges modelled at all — the rollers have nothing to run in."

file "P16 — ballistic-coefficient invariance still untested" "defect,phase-I" \
"The solar-activity half is falsified and the paper is corrected. The BC half is **proven a tautology in \`astro.py\`** — \`scale\` and \`1/BC\` occupy the same multiplicative slot, so the sweep cannot move the ratio it claims to test.

Nobody has run GMAT at BC 40 and 90 to find the true dependence. **Until then the honest position is *unknown*, not *invariant*.**"

file "P10 — enclosure, radiator and avionics absent from the mass rollup" "defect,phase-I" \
"The 76.9 kg dry figure excludes them, which means the 6.4 kg-per-satellite result in \`docs/LANDSCAPE.md\` rests on an incomplete number."

echo "== first measurement =="
file "B-1 — Halbach pair on a gaussmeter" "validation,phase-I" \
"**The cheapest route to this project's first measured number at any scale.** Roughly the price of two magnets and a Hall probe.

Every headline is downstream of a field model checked only analytic-against-analytic. A gaussmeter is a different *kind* of evidence. Bands declared in [docs/BENCHTOP_TESTS.md]($B/docs/BENCHTOP_TESTS.md), deliberately wide where the model deserves no better."

echo
echo "Done. Next: ./tools/setup_project.sh"
