#!/usr/bin/env bash
#
# Create the programme-level GitHub Project board spanning all four repositories.
#
# WHY THIS IS A SCRIPT
# --------------------
# Project boards need the ProjectsV2 GraphQL API. No tooling for it existed in the environment
# the programme structure was built in, and the REST path there is intercepted by network
# policy. `gh project` handles it in one command from any authenticated machine.
#
#   gh auth login --scopes project     # the project scope is NOT in the default set
#   ./tools/setup_project.sh
#
# Run tools/bootstrap_repos.sh first -- the board is worth little before the repositories and
# their issues exist.
#
set -euo pipefail

OWNER="${OWNER:-aaaaaaaaaaaavm}"
TITLE="${TITLE:-VOLLEY Engineering Programme}"
REPOS=(VOLLEY VOLLEY-paper VOLLEY-thesis VOLLEY-lab)

command -v gh >/dev/null || { echo "gh CLI not found"; exit 1; }
gh auth status 2>&1 | grep -q "project" || {
  echo "The 'project' scope is missing. Run:  gh auth refresh -s project,read:project"
  exit 1; }

echo "== creating project board =="
if gh project list --owner "$OWNER" --format json 2>/dev/null | grep -q "\"title\":\"$TITLE\""; then
  echo "   '$TITLE' already exists -- reusing"
  NUM=$(gh project list --owner "$OWNER" --format json \
        | python3 -c "import json,sys;print(next(p['number'] for p in json.load(sys.stdin)['projects'] if p['title']=='$TITLE'))")
else
  NUM=$(gh project create --owner "$OWNER" --title "$TITLE" --format json \
        | python3 -c "import json,sys;print(json.load(sys.stdin)['number'])")
  echo "   created project #$NUM"
fi

echo
echo "== adding open issues from all four repositories =="
for r in "${REPOS[@]}"; do
  gh repo view "$OWNER/$r" >/dev/null 2>&1 || { echo "   $r does not exist yet -- skipped"; continue; }
  n=0
  while read -r url; do
    [ -z "$url" ] && continue
    gh project item-add "$NUM" --owner "$OWNER" --url "$url" >/dev/null 2>&1 && n=$((n+1))
  done < <(gh issue list --repo "$OWNER/$r" --state open --limit 100 --json url --jq '.[].url')
  echo "   $r: $n items"
done

echo
echo "Board: https://github.com/users/$OWNER/projects/$NUM"
echo
echo "Suggested fields to add by hand (gh cannot create custom fields reliably):"
echo "  Phase      single-select: I / II"
echo "  Kind       single-select: defect / validation / documentation / research"
echo "  Blocking   single-select: yes / no"
echo
echo "NOTE: the Markdown ledgers stay authoritative. OPEN_PROBLEMS.md and ROADMAP.md are the"
echo "record; these issues are a view onto them. If the two disagree, the Markdown is right."
