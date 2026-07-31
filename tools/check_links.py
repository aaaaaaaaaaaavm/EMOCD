"""Check every link in the repository resolves, and that the cross-link block has not forked.

Three failure modes have actually happened here, which is why each is checked:

  1. A file moved and the links to it did not. The front-door restructure moved ten files
     into docs/ and left three absolute links in wiki/Home.md pointing at the old root.
  2. A relative link was written against the wrong directory. docs/ pages linking to
     ../OPEN_PROBLEMS.md and docs pages linking to sibling docs are easy to get backwards.
  3. The shared repository table drifted between copies. It appears in the flagship's
     PROGRAMME.md, in the generated companions, and in tools/lab-seed/README.md, and a
     hand-edit to any one of them silently forks it.

Run:   python3 tools/check_links.py
Exits non-zero on the first category with any failure, so it works in CI.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OWNER = "aaaaaaaaaaaavm"

# Directories whose links are deliberately not maintained: superseded scripts kept for the
# record, and archived paper builds. Both are frozen by intent.
SKIP_DIRS = {".git", "legacy", "paper/archive", "node_modules", "__pycache__"}

# Only rendered files are checked. Scripts and LaTeX are excluded on purpose: the link-shaped
# strings inside make_baseline.py, export_companion.py and seed_issues.sh are templates for
# files written elsewhere, and seed_issues.sh interpolates a $B shell variable into every one
# of them. Checking those texts here reports the generator's own directory, which is never
# where the link will live. The generated output is checked instead, which is the thing a
# reader actually clicks.
EXTS = (".md", ".html")

REL = re.compile(r"\]\(([^)\s#]+\.(?:md|py|sh|json|tex|png|gif|stl|step|dxf|cir|csv))(?:#[^)]*)?\)")

# Only FLAGSHIP links are resolved against this checkout. Links to the sibling repositories
# (VOLLEY-lab, VOLLEY-paper, VOLLEY-thesis) point at files that do not exist here and must not
# be reported broken -- the trailing slash after the repo name is what stops "VOLLEY" matching
# "VOLLEY-lab". Found when tools/lab-seed/README.md gained links to two files that live in the
# lab repository by design.
FLAGSHIP = "VOLLEY"
ABS = re.compile(
    r"https://(?:github\.com/%s/%s/(?:blob|tree)/main|"
    r"raw\.githubusercontent\.com/%s/%s/main)/([^)\s\"'>]+)" % (OWNER, FLAGSHIP, OWNER, FLAGSHIP))


def tracked_files():
    for base, dirs, files in os.walk(ROOT):
        rel_base = os.path.relpath(base, ROOT)
        if any(rel_base == d or rel_base.startswith(d + os.sep) for d in SKIP_DIRS):
            dirs[:] = []
            continue
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith(EXTS):
                yield os.path.join(base, f)


def check_links():
    """Relative links resolve against the linking file; absolute ones against the repo root."""
    bad = []
    for path in tracked_files():
        rel = os.path.relpath(path, ROOT)
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        for m in REL.finditer(text):
            target = m.group(1)
            if target.startswith(("http", "mailto:")):
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
            if not os.path.exists(resolved):
                bad.append((rel, target, "relative"))
        for m in ABS.finditer(text):
            target = m.group(1).split("#")[0]
            if not os.path.exists(os.path.join(ROOT, target)):
                bad.append((rel, target, "absolute"))
    return bad


def check_header_block():
    """The repository table must be byte-identical everywhere it appears.

    export_companion.py builds it from HEADER_ROWS and writes it between the
    PROGRAMME-HEADER markers. Any copy that disagrees has been hand-edited.
    """
    marker = re.compile(
        r"<!-- PROGRAMME-HEADER-START -->\n(.*?)<!-- PROGRAMME-HEADER-END -->",
        re.S)
    found = {}
    for path in tracked_files():
        if not path.endswith(".md"):
            continue
        with open(path, encoding="utf-8", errors="replace") as fh:
            m = marker.search(fh.read())
        if m:
            # Two things vary per repository by design and are normalised away: the trailing
            # "You are here" column, and the bold markers, which are what mark the row for the
            # repository the reader is currently in. Everything else must match exactly.
            body = "\n".join(ln.rsplit("|", 2)[0].replace("**", "")
                             for ln in m.group(1).strip().splitlines())
            found[os.path.relpath(path, ROOT)] = body
    if len(set(found.values())) > 1:
        return found
    return None


def main():
    failed = False

    bad = check_links()
    if bad:
        failed = True
        print(f"{len(bad)} broken link(s):")
        for rel, target, kind in sorted(set(bad)):
            print(f"  {rel}  ->  {target}  ({kind})")
    else:
        print("links: all resolve")

    forked = check_header_block()
    if forked:
        failed = True
        print("\nthe cross-link block has forked between copies:")
        for rel in sorted(forked):
            print(f"  {rel}")
        print("  Fix PROGRAMME.md and re-run tools/export_companion.py; do not hand-edit.")
    else:
        print("cross-link block: consistent")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
