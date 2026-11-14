#!/usr/bin/env python3
"""fix_index_and_link.py — repair the page index hole, the section lookup, the
Appendix D.2 ranges and the dead NSA source link.

Page 28 is the appendix index itself; rebuild_index() skipped its own page, so
the map ran 27 -> 29 and §139 appeared in no lookup. D.2's ranges were off by
one from row 19 for the same reason. The generator is patched so a future
rebuild reproduces the corrected map instead of reverting it.

  python tools/fix_index_and_link.py          # fix, gate, push
  python tools/fix_index_and_link.py --dry    # fix, gate, no push
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
TOOL = ROOT / "tools" / "patch_readme.py"
MSG = "docs: close page index hole, shift D.2 ranges, repair dead NSA source"

OLD_URL = ("https://www.spiegel.de/netzwelt/netzpolitik/"
           "gsm-verschluesselung-die-nsa-kann-fast-alle-handygespraeche-abhoeren-a939049.html")
NEW_URL = ("https://www.spiegel.de/netzwelt/netzpolitik/"
           "gsm-verschluesselung-die-nsa-kann-fast-alle-handygespraeche-abhoeren-a-939049.html")

# (old, new) — index row, section lookup row, D.2 shift, prose
FIXES = [
    ("| 27 | 134. Redaction Procedure |\n| 29 | Part XII — Appendices |",
     "| 27 | 134. Redaction Procedure |\n| 28 | Appendix — Page Index; 139. About the author |\n| 29 | Part XII — Appendices |"),
    ("| 134–138 | 27 |\n", "| 134–138 | 27 |\n| 139 | 28 |\n"),
    ("| 19 | Plates 1–18 |", "| 18 | Plates 1–18 |"),
    ("| 20–21 | §83–§92 |", "| 19–20 | §83–§92 |"),
    ("| 22–23 | §93–§105 |", "| 21–22 | §93–§105 |"),
    ("| 24–25 | §106–§118 |", "| 23–24 | §106–§118 |"),
    ("| 26 | §119–§128 |", "| 25 | §119–§128 |"),
    ("| 27–28 | §129–§138 |", "| 26–27 | §129–§138 |"),
    ("| 29–32 | Appendix, author, Part XII, this page |",
     "| 28–31 | Appendix, author, Part XII, this page |"),
    ("This page is the authoritative map.",
     "This page is the authoritative map, and it lists itself on page 28 so the numbering runs without a hole."),
    ("Footers carry the live total; there is no legacy count left to reconcile.",
     "Footers carry the live total; there is no legacy count left to reconcile. Page 28 is this page; §139 follows on it."),
]

GEN_OLD = '    rows = [f"| {i + 1} | {head(p)} |" for i, p in enumerate(pages) if i != idx and head(p) != "—"]'
GEN_NEW = '    rows = [f"| {i + 1} | {head(p)} |" for i, p in enumerate(pages) if head(p) != "—"]'
GEN_SKIP = "        if i == idx:\n            continue\n"
GEN_NOTE = "     never emits an empty row. The index page is listed like any other\n     so the map has no hole; --check gates on literal keys, front/back matter\n"


def die(m: str) -> None:
    print(f"\nFAIL: {m}", file=sys.stderr)
    raise SystemExit(1)


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True, cwd=ROOT,
                          encoding="utf-8", errors="replace")


def index_pages(doc: str) -> list[int]:
    """Page numbers from the page index table only, not from every table."""
    parts = doc.split("| Page | Contents |", 1)
    if len(parts) < 2:
        die("page index table not found")
    table = parts[1].split("\n\n", 1)[0]
    return [int(n) for n in re.findall(r"^\| (\d+) \| ", table, re.MULTILINE)]


def main() -> int:
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="replace")
    dry = "--dry" in sys.argv

    print("[0/4] preconditions")
    for p in (README, TOOL, ROOT / ".git"):
        if not p.exists():
            die(f"missing {p}")
    text = README.read_text(encoding="utf-8")
    gen = TOOL.read_text(encoding="utf-8")
    if '"2.5"' not in gen:
        die("tools/patch_readme.py is not v2.5")

    print("[1/4] repair the source link")
    if NEW_URL in text:
        print("     already correct")
    elif OLD_URL in text:
        text = text.replace(OLD_URL, NEW_URL, 1)
        print("     NSA link corrected (missing hyphen)")
    else:
        die("neither the broken nor the corrected NSA url is present")

    print("[2/4] close the index hole and shift D.2")
    for old, new in FIXES:
        if new in text and old not in text:
            print("     already current")
            continue
        if old not in text:
            die(f"anchor not found: {old[:52]!r}")
        text = text.replace(old, new, 1)
        print(f"     fixed: {new.splitlines()[0][:52]}")
    README.write_text(text, encoding="utf-8", newline="\n")

    print("[3/4] patch the generator so a rebuild keeps it")
    if GEN_NEW in gen:
        print("     generator already patched")
    elif GEN_OLD in gen:
        gen = gen.replace(GEN_OLD, GEN_NEW, 1)
        if GEN_SKIP in gen:
            gen = gen.replace(GEN_SKIP, "", 1)
        gen = gen.replace("     never emits an empty row.\n", GEN_NOTE, 1)
        TOOL.write_text(gen, encoding="utf-8", newline="\n")
        print("     rebuild_index now lists the index page")
    else:
        die("rebuild_index row expression not recognised")

    print("[gate] --check")
    r = run([sys.executable, str(TOOL), "--check"])
    out = (r.stdout or "") + (r.stderr or "")
    print("     " + "\n     ".join(out.strip().splitlines()))
    if r.returncode != 0:
        die(f"--check exited {r.returncode}, expected 0")
    for w in ("unverified=0 ", "hotlinks=0", "toc_blocks=24", "literal_key=0"):
        if w not in out:
            die(f"check line missing {w!r}")

    doc = README.read_text(encoding="utf-8")
    if OLD_URL in doc or NEW_URL not in doc:
        die("NSA link is still wrong")
    if "| 28 | Appendix — Page Index; 139. About the author |" not in doc:
        die("page 28 row missing")
    if "| 27 | 134. Redaction Procedure |\n| 29 " in doc:
        die("index still jumps 27 -> 29")
    if "| 139 | 28 |" not in doc:
        die("§139 missing from the section lookup")
    if "| 18 | Plates 1–18 |" not in doc or "| 29–32 | Appendix" in doc:
        die("D.2 ranges not shifted")
    if doc.count("| ✓ |") != 55:
        die(f"{doc.count('| ✓ |')} ticks, expected 55")
    nums = index_pages(doc)
    if nums != list(range(1, 34)):
        die(f"page index rows are {len(nums)}: {nums}")
    print(f"     index runs 1-33 with no hole, {doc.count('| ✓ |')} ticks intact")

    if dry:
        print("\nOK, written, not committed (--dry).")
        return 0

    print("[commit]")
    run(["git", "add", "-A"])
    c = run(["git", "commit", "-m", MSG])
    print("     " + " ".join((c.stdout or c.stderr).strip().splitlines()[:2]))
    if c.returncode != 0:
        die("commit failed — inspect `git status`")

    p = run(["git", "push"])
    print("     " + " ".join((p.stdout or p.stderr).strip().splitlines()[-2:]))
    if p.returncode != 0:
        die("push failed — the commit stands, retry `git push`")

    print("\nOK. Pushed. Page 28 is in the map, D.2 is shifted, the NSA link resolves.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())