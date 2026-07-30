#!/usr/bin/env bash
#
# Create and push the three companion repositories of the VOLLEY programme.
#
# WHY THIS IS A SCRIPT RATHER THAN SOMETHING ALREADY DONE
# -------------------------------------------------------
# The environment the programme structure was built in cannot create repositories: its git
# proxy accepts refs/heads/* but returns 403 for refs/tags/*, and its network policy
# intercepts api.github.com ("GitHub access is not enabled for this session"). Everything is
# prepared here so this is one command from any machine with ordinary GitHub access.
#
#   gh auth login          # once
#   ./tools/bootstrap_repos.sh
#
# Idempotent: existing repositories are updated, not recreated. Safe to re-run.
#
# WHAT IT CREATES
#   VOLLEY-paper    generated from the flagship by tools/export_companion.py
#   VOLLEY-thesis   generated likewise, plus a university/ directory the exporter never touches
#   VOLLEY-lab      Phase II. Seeded from tools/lab-seed/, then yours to do as you like
#
set -euo pipefail

OWNER="${OWNER:-aaaaaaaaaaaavm}"
FLAGSHIP="${FLAGSHIP:-VOLLEY}"
# The About panel's Website field. Set it on all four: it is the one link on the page aimed at
# a reader who is not going to clone anything.
PAGES="${PAGES:-https://$OWNER.github.io/$FLAGSHIP/}"

# The repositories must already be renamed to VOLLEY-* before this runs. If they are not,
# `gh repo create` below will cheerfully create empty new ones under the VOLLEY names and push
# there, leaving the real repositories untouched. Override for the pre-rename names:
#   FLAGSHIP=EMOCD REPO_PREFIX=EMOCD ./tools/bootstrap_repos.sh
for r in "$FLAGSHIP" "$FLAGSHIP-paper" "$FLAGSHIP-thesis" "$FLAGSHIP-lab"; do
  gh repo view "$OWNER/$r" >/dev/null 2>&1 || {
    echo "note: $OWNER/$r does not exist yet."
    echo "      If the repositories have not been renamed, re-run as:"
    echo "        FLAGSHIP=EMOCD REPO_PREFIX=EMOCD $0"; }
done
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="${WORK:-$(mktemp -d)}"

command -v gh >/dev/null || { echo "gh CLI not found: https://cli.github.com/"; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "Run: gh auth login"; exit 1; }

if [ -n "$(git -C "$ROOT" status --porcelain)" ]; then
  echo "Flagship working tree is dirty. Commit first -- the companions record the commit"
  echo "they were generated from, and a dirty tree makes that record a lie."
  exit 1
fi
COMMIT=$(git -C "$ROOT" rev-parse --short HEAD)
echo "flagship at $COMMIT; staging in $WORK"

echo
echo "== generating companions =="
python3 "$ROOT/tools/export_companion.py" --out "$WORK"

echo
echo "== seeding VOLLEY-lab =="
mkdir -p "$WORK/VOLLEY-lab"
cp -r "$ROOT/tools/lab-seed/." "$WORK/VOLLEY-lab/"

push_one () {   # $1 = repo name, $2 = description
  local name="$1" desc="$2" dir="$WORK/$1"
  echo
  echo "== $name =="
  [ -d "$dir" ] || { echo "   nothing staged, skipped"; return; }
  ( cd "$dir"
    git init -q -b main
    git add -A
    git -c user.email="adityavardhanmishr@gmail.com" \
        -c user.name="Adityavardhan Mishra" \
        commit -q -m "$name: generated from VOLLEY flagship $COMMIT

Programme structure per docs/programme/ADOPTION.md in the flagship."
    if gh repo view "$OWNER/$name" >/dev/null 2>&1; then
      echo "   exists -- force-pushing regenerated content"
      git remote add origin "https://github.com/$OWNER/$name.git"
      git push -q --force origin main
    else
      gh repo create "$OWNER/$name" --public --description "$desc" --source=. --push
    fi
    gh repo edit "$OWNER/$name" --description "$desc" --homepage "$PAGES" >/dev/null 2>&1 || true
    # Without topics a repository is invisible to the search most people actually use.
    gh repo edit "$OWNER/$name" \
      --add-topic cubesat --add-topic aerospace --add-topic electromagnetic-launch \
      --add-topic space-systems >/dev/null 2>&1 || true
  )
  echo "   https://github.com/$OWNER/$name"
}

push_one VOLLEY-paper  "IEEE companion for VOLLEY: manuscript, figures, and the analysis that reproduces every number in it from a clean clone. Generated from the flagship; do not edit here."
push_one VOLLEY-thesis "Thesis companion for VOLLEY: final-year submission material, with the decision records and defect ledger as appendices. Generated from the flagship; edit university/ only."
push_one VOLLEY-lab    "VOLLEY Phase II: research and redesign, where the frozen baseline does not apply. Deliberately unstable; nothing here should be cited."

echo
echo "== enabling Issues on the flagship =="
# Issues are currently DISABLED on VOLLEY (the API returns 410). The programme board and the
# issue seeding both need them, so this turns them on. Nothing is filed until seed_issues.sh.
gh repo edit "$OWNER/$FLAGSHIP" --enable-issues >/dev/null 2>&1 \
  && echo "   enabled" || echo "   could not enable -- do it in Settings > General > Features"

echo
echo "== flagship description and topics =="
gh repo edit "$OWNER/$FLAGSHIP" \
  --description "VOLLEY: a magazine-fed ironless Halbach linear synchronous motor that ejects unmodified 3U CubeSats at 16.5 m/s and 10.7 g. Design study, TRL 2-3, every number a model output, every defect published." \
  --homepage "$PAGES" \
  --add-topic cubesat --add-topic aerospace --add-topic linear-motor \
  --add-topic halbach-array --add-topic orbital-mechanics --add-topic design-study \
  --add-topic electromagnetic-launch --add-topic space-systems \
  --add-topic finite-element-analysis --add-topic astrodynamics \
  >/dev/null 2>&1 || echo "   (topic edit failed -- set them in the web UI)"

echo
echo "Done. Next: ./tools/seed_issues.sh, then ./tools/setup_project.sh."
echo
echo "REMINDER: VOLLEY-paper and VOLLEY-thesis are OUTPUT. Never edit them directly."
echo "Re-run this script after any flagship change that should reach them."
