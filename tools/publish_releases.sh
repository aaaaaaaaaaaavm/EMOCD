#!/usr/bin/env bash
#
# Push the milestone tags and create their GitHub Releases.
#
# WHY THIS SCRIPT EXISTS
# ----------------------
# The reconstructed history and its six annotated tags were built in an environment whose
# git proxy permits pushes to refs/heads/* but returns 403 for refs/tags/*, and whose network
# policy blocks the GitHub REST API. The commits are already on GitHub; the tags and releases
# are not. Everything needed is committed here so this is one command from any machine with
# ordinary GitHub access.
#
# WHAT IT DOES
#   1. Pushes the six milestone tags.
#   2. Re-points v0.1.0, whose GitHub release currently references a commit that the history
#      reconstruction removed.
#   3. Creates a Release for each tag, with notes taken from the annotated tag message so
#      there is one source of truth rather than two.
#
# REQUIREMENTS
#   gh CLI, authenticated:  gh auth login
#   Run from the repository root, on the branch carrying the reconstructed history.
#
# ON THE DATES
#   These releases mark design periods, four of the six approximate. GitHub stamps its own
#   creation date on a Release and that cannot be backdated through the API -- the *tag* dates
#   carry the design periods, the Release creation dates will all read "now". HISTORY.md
#   explains the distinction; do not let the Release dates be read as the work dates.
#
set -euo pipefail

REPO="${REPO:-aaaaaaaaaaaavm/VOLLEY}"
TAGS=(v0.0-concept v0.1-lsm v0.2-gen1 v0.3-gen2 v0.4-gen3 v1.0 v1.1)

command -v gh >/dev/null || { echo "gh CLI not found. https://cli.github.com/"; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "Run: gh auth login"; exit 1; }
git rev-parse --git-dir >/dev/null 2>&1 || { echo "Run from the repository root."; exit 1; }

# A fresh clone has NONE of the milestone tags -- they are not on GitHub as tag objects a
# clone would fetch, and v0.1.0 arrives pointing at a commit the reconstruction removed.
# Verified by cloning and looking. Without this, the loop below skips all six and creates
# nothing, which is exactly the failure mode this guard exists to prevent.
if ! git rev-parse -q --verify refs/tags/v0.0-concept >/dev/null; then
  echo "== 0. milestone tags absent -- restoring =="
  "$(dirname "$0")/restore_tags.sh"
  echo
fi

echo "== 1. pushing milestone tags =="
for t in "${TAGS[@]}"; do
  if git rev-parse -q --verify "refs/tags/$t" >/dev/null; then
    git push origin "refs/tags/$t" && echo "   $t pushed"
  else
    echo "   $t MISSING locally -- skipped"
  fi
done

echo
echo "== 2. re-pointing v0.1.0 =="
# Its GitHub release references a commit removed by the history reconstruction. The tag is
# force-updated to the equivalent commit in the rebuilt history; the release itself keeps its
# original notes and its original publication date.
if git rev-parse -q --verify refs/tags/v0.1.0 >/dev/null; then
  git push --force origin refs/tags/v0.1.0 && echo "   v0.1.0 re-pointed"
else
  echo "   v0.1.0 missing locally -- skipped"
fi

echo
echo "== 3. creating releases =="
for t in "${TAGS[@]}"; do
  if gh release view "$t" --repo "$REPO" >/dev/null 2>&1; then
    echo "   $t release already exists -- skipped"
    continue
  fi
  # Notes come from the annotated tag message, so the tag and the release cannot disagree.
  # :body, not :contents. %(contents) includes the subject line, which is already the
  # release title, so using it prints the title twice on the release page.
  notes="$(git for-each-ref "refs/tags/$t" --format='%(contents:body)')"
  title="$(git for-each-ref "refs/tags/$t" --format='%(contents:subject)')"
  latest=""
  [ "$t" = "v1.1" ] && latest="--latest"
  gh release create "$t" --repo "$REPO" --title "$title" --notes "$notes" $latest \
    && echo "   $t release created"
done

echo
echo "Done. Verify:  gh release list --repo $REPO"
echo
echo "Note: Release creation dates will read today. The design periods live in the tag"
echo "dates and in HISTORY.md -- GitHub does not allow a Release's date to be set."
