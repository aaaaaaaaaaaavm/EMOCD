#!/usr/bin/env bash
#
# Recreate the milestone tags in a fresh clone.
#
# WHY THIS EXISTS
# ---------------
# The tags were built in an environment whose git proxy refuses pushes to refs/tags/*, so
# they never reached GitHub -- and therefore they are in NO clone. Verified, not assumed: a
# fresh `git clone` of this repository arrives with exactly one tag, v0.1.0, and none of the
# six milestones. Without this script, publish_releases.sh finds nothing to push and creates
# no releases.
#
# The *commits* the tags point at are all on GitHub -- every one is an ancestor of the default
# branch -- so the tag objects can be rebuilt exactly from the data below plus your clone.
#
# Each tag is recreated ANNOTATED, with its original message and its original tagger date,
# because those dates are the design periods HISTORY.md describes. A lightweight tag would
# lose both. Read HISTORY.md before citing any of these dates: four of the six are approximate
# and it says which.
#
# USAGE
#   git clone https://github.com/aaaaaaaaaaaavm/VOLLEY.git    # full clone, not --depth
#   cd VOLLEY
#   ./tools/restore_tags.sh
#   ./tools/publish_releases.sh
#
# Re-running is safe: existing milestone tags are left alone unless FORCE=1.
#
set -euo pipefail

cd "$(dirname "$0")/.."

git rev-parse --git-dir >/dev/null 2>&1 || { echo "Not a git repository."; exit 1; }

if [ -f "$(git rev-parse --git-dir)/shallow" ]; then
  echo "This is a shallow clone -- the 2021-2026 milestone commits are not present."
  echo "Run:  git fetch --unshallow"
  exit 1
fi

# The tagger identity is pinned, not inherited. Verified necessary: run in a fresh clone
# whose global git config names someone else, `git tag -a` silently stamps THAT identity onto
# every milestone, and the tag objects stop matching the ones this history was built with.
# Override on the command line if you are recreating these under a different name.
TAGGER_NAME="${TAGGER_NAME:-Adityavardhan Mishra}"
TAGGER_EMAIL="${TAGGER_EMAIL:-adityavardhanmishr@gmail.com}"
export GIT_COMMITTER_NAME="$TAGGER_NAME"
export GIT_COMMITTER_EMAIL="$TAGGER_EMAIL"

FORCE="${FORCE:-0}"
missing=0
made=0

# ---------------------------------------------------------------- v0.0-concept
if [ "$FORCE" != "1" ] && git rev-parse -q --verify "refs/tags/v0.0-concept" >/dev/null; then
  echo "   v0.0-concept already exists, left alone (FORCE=1 to replace)"
elif ! git cat-file -e 0c3cfafea3dff26ea7275695baf11f4e509d598c^{commit} 2>/dev/null; then
  echo "   v0.0-concept SKIPPED, commit 0c3cfafea not in this clone"
  missing=$((missing+1))
else
  GIT_COMMITTER_DATE="2021-03-22T10:00:00+05:30" \
  git tag -f -a "v0.0-concept" 0c3cfafea3dff26ea7275695baf11f4e509d598c -m 'Concept (2021-03-22)

Electromagnetic alternative to the CubeSat deployment spring, built around a
coilgun. Presented at ARDE / INSARM 2021.

Date DOCUMENTED. Reconstructed tag -- see HISTORY.md.' >/dev/null
  echo "   v0.0-concept -> 0c3cfafea  (2021-03-22)"
  made=$((made+1))
fi

# ---------------------------------------------------------------- v0.1-lsm
if [ "$FORCE" != "1" ] && git rev-parse -q --verify "refs/tags/v0.1-lsm" >/dev/null; then
  echo "   v0.1-lsm already exists, left alone (FORCE=1 to replace)"
elif ! git cat-file -e dd63191f789f3184ff7a728f1b2b27051b92db37^{commit} 2>/dev/null; then
  echo "   v0.1-lsm SKIPPED, commit dd63191f7 not in this clone"
  missing=$((missing+1))
else
  GIT_COMMITTER_DATE="2025-07-01T10:00:00+05:30" \
  git tag -f -a "v0.1-lsm" dd63191f789f3184ff7a728f1b2b27051b92db37 -m 'Coilgun -> linear synchronous motor (mid-2025)

The pivotal decision. Everything downstream -- Halbach array, reusable sled,
eddy brake, supercapacitor bank -- follows from it.

Date APPROXIMATE: the decision log records only '"'"'mid-2025'"'"'. See HISTORY.md.' >/dev/null
  echo "   v0.1-lsm -> dd63191f7  (2025-07-01)"
  made=$((made+1))
fi

# ---------------------------------------------------------------- v0.2-gen1
if [ "$FORCE" != "1" ] && git rev-parse -q --verify "refs/tags/v0.2-gen1" >/dev/null; then
  echo "   v0.2-gen1 already exists, left alone (FORCE=1 to replace)"
elif ! git cat-file -e 1fc1203b2766df4d80f2222fe677ee1a7bce7cb8^{commit} 2>/dev/null; then
  echo "   v0.2-gen1 SKIPPED, commit 1fc1203b2 not in this clone"
  missing=$((missing+1))
else
  GIT_COMMITTER_DATE="2025-09-15T10:00:00+05:30" \
  git tag -f -a "v0.2-gen1" 1fc1203b2766df4d80f2222fe677ee1a7bce7cb8 -m 'Gen1 CAD

Eleven STEP exports establishing the geometry. The geometric ancestor of the
entire parameter set; sub-systems are structural proxies.

Date APPROXIMATE: cad/CHANGELOG_CAD.md gives a 2021-2025 range and states the
exact build history was never reconstructed. See HISTORY.md.' >/dev/null
  echo "   v0.2-gen1 -> 1fc1203b2  (2025-09-15)"
  made=$((made+1))
fi

# ---------------------------------------------------------------- v0.3-gen2
if [ "$FORCE" != "1" ] && git rev-parse -q --verify "refs/tags/v0.3-gen2" >/dev/null; then
  echo "   v0.3-gen2 already exists, left alone (FORCE=1 to replace)"
elif ! git cat-file -e 9b93d53fc3fdf2d6b675a01731bd622f65aa270b^{commit} 2>/dev/null; then
  echo "   v0.3-gen2 SKIPPED, commit 9b93d53fc not in this clone"
  missing=$((missing+1))
else
  GIT_COMMITTER_DATE="2026-02-15T10:00:00+05:30" \
  git tag -f -a "v0.3-gen2" 9b93d53fc3fdf2d6b675a01731bd622f65aa270b -m 'Gen2 CAD

First structured revision, rebuilt from the parameter set. Adds the
retention-gate pins and corrects the sled chassis length.

Date APPROXIMATE, within the documented 2025 to 2026-07 range. See HISTORY.md.' >/dev/null
  echo "   v0.3-gen2 -> 9b93d53fc  (2026-02-15)"
  made=$((made+1))
fi

# ---------------------------------------------------------------- v0.4-gen3
if [ "$FORCE" != "1" ] && git rev-parse -q --verify "refs/tags/v0.4-gen3" >/dev/null; then
  echo "   v0.4-gen3 already exists, left alone (FORCE=1 to replace)"
elif ! git cat-file -e 2162bb8d4fd84c154e2af339f9b001508d6f2be1^{commit} 2>/dev/null; then
  echo "   v0.4-gen3 SKIPPED, commit 2162bb8d4 not in this clone"
  missing=$((missing+1))
else
  GIT_COMMITTER_DATE="2026-07-23T10:00:00+05:30" \
  git tag -f -a "v0.4-gen3" 2162bb8d4fd84c154e2af339f9b001508d6f2be1 -m 'Gen3 CAD -- current

Parameter set rebuilt from the actual geometry via the Fusion API. Twelve
defects open (G3-D1 to G3-D12). Repository created the same day.

Date DOCUMENTED. See HISTORY.md.' >/dev/null
  echo "   v0.4-gen3 -> 2162bb8d4  (2026-07-23)"
  made=$((made+1))
fi

# ---------------------------------------------------------------- v1.0
if [ "$FORCE" != "1" ] && git rev-parse -q --verify "refs/tags/v1.0" >/dev/null; then
  echo "   v1.0 already exists, left alone (FORCE=1 to replace)"
elif ! git cat-file -e 715b61b13ae2c736118eec22f19932fe17ae12e3^{commit} 2>/dev/null; then
  echo "   v1.0 SKIPPED, commit 715b61b13 not in this clone"
  missing=$((missing+1))
else
  GIT_COMMITTER_DATE="2026-07-29T12:00:00+05:30" \
  git tag -f -a "v1.0" 715b61b13ae2c736118eec22f19932fe17ae12e3 -m 'v1.0 -- current published state (2026-07-29)

Rated point 16.54 m/s at 10.7 g from a sled mass measured in CAD. Paper
rebuilt from corrected source. 19 numbered problems and 23 open engineering
items published; three of eight validations run, all against acceptance bands
declared before the run.

Known-open at this tag: P9 envelope, P14 CAD defects, P16 BC half untested,
P17 attraction 37% high, P19 validations predate the operating point.' >/dev/null
  echo "   v1.0 -> 715b61b13  (2026-07-29)"
  made=$((made+1))
fi

# ---------------------------------------------------------------- v1.1
if [ "$FORCE" != "1" ] && git rev-parse -q --verify "refs/tags/v1.1" >/dev/null; then
  echo "   v1.1 already exists, left alone (FORCE=1 to replace)"
elif ! git cat-file -e 6ec0dd1^{commit} 2>/dev/null; then
  echo "   v1.1 SKIPPED, commit 6ec0dd1 not in this clone"
  missing=$((missing+1))
else
  GIT_COMMITTER_DATE="2026-07-30T19:15:00+05:30" \
  git tag -f -a "v1.1" 6ec0dd1 -m 'v1.1 -- prior art, the bank ESR, and the rename (2026-07-30)

Rated point unchanged at 16.537 m/s and 10.7 g. What moved is the electrical
side and the honesty of the comparison.

Bank ESR now modelled. A8 re-run at the current operating point failed its
energy-closure band at 97.0 %, and the cause was a loss no analysis script
carried: 86 J a shot in the supercapacitor bank own series resistance.
Energy per shot 2.80 to 2.88 kJ, efficiency 19.6 to 19.0 %, sag 5.19 to
5.35 %. The correction also settled a 5 % peak-current disagreement that had
been recorded twice and blamed on the integrator; the analytic model and
ngspice now agree to 0.01 %.

Prior art found and two claims retracted. Published work on this exact
concept was cited nowhere, one paper of it eight months before this
repository went public. The novelty claim was narrowed to what survives it,
and ADR-003 efficiency argument was withdrawn as false rather than
re-sourced.

Programme renamed to VOLLEY. CAD part numbers keep the EMOCD prefix by
decision, not oversight; see ADR-018.

25 numbered problems and 24 open engineering items published, 18 decision
records. Four of nine validations run, each against a band declared before
the run.

Known-open at this tag: P9 envelope 44 % over ESPA Grande, P14 CAD defects
upstream of Kt, P16 ballistic-coefficient half untested, P17 attraction 37 %
high, P19 A5 still predates the operating point, P24 the 12 mohm ESR has no
source, P25 a retracted claim reached four artifacts before anyone noticed.

Still nothing built, fired or measured.' >/dev/null
  echo "   v1.1 -> 6ec0dd1  (2026-07-30)"
  made=$((made+1))
fi

# ---------------------------------------------------------------- v0.1.0
# ALWAYS re-pointed, never skipped. A clone may fetch this tag pointing at a
# superseded commit; leaving it alone would make publish_releases.sh push a stale
# pointer and change nothing. Its Release keeps its own notes and publication
# date; only the ref moves.
if ! git cat-file -e 0162a9071a34b0fb5654c4e1c64fb39e2e145a37^{commit} 2>/dev/null; then
  echo "   v0.1.0 SKIPPED, commit 0162a9071 not in this clone"
  missing=$((missing+1))
else
  GIT_COMMITTER_DATE="2026-07-23T18:00:00+05:30" \
  git tag -f -a "v0.1.0" 0162a9071a34b0fb5654c4e1c64fb39e2e145a37 -m 'VOLLEY v0.1.0 — design study, reproduced and corrected against its own scripts

Re-pointed 2026-07-29: the history was reconstructed and this tag'"'"'s original
commit no longer exists. It now points at the equivalent commit in the
rebuilt history. See HISTORY.md.' >/dev/null
  echo "   v0.1.0 -> 0162a9071  (2026-07-23)  [re-pointed]"
  made=$((made+1))
fi

echo
echo "$made tag(s) written."
if [ "$missing" -ne 0 ]; then
  echo
  echo "$missing tag(s) skipped, their commits are not in this clone."
  echo "A full clone of the default branch contains all seven."
  exit 1
fi
echo "Next:  ./tools/publish_releases.sh"
