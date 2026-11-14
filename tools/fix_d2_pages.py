#!/usr/bin/env python3
"""fix_d2_pages.py — pull the Appendix D.2 page ranges back by one and drop the
row for the superseded draft page.

D.2 still counted the page that --fix-page8 deleted, so every section from §12
onward pointed one page too high and §59–§66 collided with the plates on 18.
The gate compares D.2 against the page index row for row.

  python tools/fix_d2_pages.py          # fix, gate, push
  python tools/fix_d2_pages.py --dry    # fix, gate, no push
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
TOOL = ROOT / "tools" / "patch_readme.py"
MSG = "docs: pull D.2 page ranges back by one; drop the deleted draft row"

DRAFT = "| 8 | §9–§11 | C | Early working draft. Superseded by page 9; keep or delete |\n"

SHIFTS = [
    ("| 9 | §9–§11 | V | Authoritative |", "| 8 | §9–§11 | V | Renumbered |"),
    ("| 10 | §12–§15 | V | Verbatim, including the four-grade confidence scale |",
     "| 9 | §12–§15 | V | Verbatim, including the four-grade confidence scale |"),
    ('| 11 | §16–§20 | V | Renumbered; "see 6.8" → §21.8 |',
     '| 10 | §16–§20 | V | Renumbered; "see 6.8" → §21.8 |'),
    ("| 12 | §21–§26 | V | Renumbered |", "| 11 | §21–§26 | V | Renumbered |"),
    ("| 13 | §27–§29 | V | Renumbered |", "| 12 | §27–§29 | V | Renumbered |"),
    ("| 14 | §30–§34 | V | Renumbered |", "| 13 | §30–§34 | V | Renumbered |"),
    ("| 15 | §35–§41 | V | Renumbered |", "| 14 | §35–§41 | V | Renumbered |"),
    ('| 16 | §42–§49 | V | Renumbered; "§10 tests" → §44, "Volume II §6" → §21 |',
     '| 15 | §42–§49 | V | Renumbered; "§10 tests" → §44, "Volume II §6" → §21 |'),
    ('| 17 | §50–§58 | V | Renumbered; "Volume III §4" → §30 |',
     '| 16 | §50–§58 | V | Renumbered; "Volume III §4" → §30 |'),
    ('| 18 | §59–§66 | V | Renumbered; "Volume I Appendix B" → §14.3 |',
     '| 17 | §59–§66 | V | Renumbered; "Volume I Appendix B" → §14.3 |'),
]

NOTE_OLD = ("Concatenate in page order. Page 8 and page 9 both carry §9–§11; keep both, "
            "or delete page 8 and renumber from there. If you delete page 8, the extent "
            "becomes 33 and every later page shifts by one — the section-to-page table "
            "above stays correct because it keys on sections, not footers.")
NOTE_NEW = ("Concatenate in page order. The superseded draft page has been deleted, so "
            "§9–§11 occupy a single page and there is no duplicate left to reconcile. "
            "The extent is 34.")

EXPECT = ["4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16",
          "17", "18", "19–20", "21–22", "23–24", "25", "26–27", "28–31"]


def die(m: str) -> None:
    print(f"\nFAIL: {m}", file=sys.stderr)
    raise SystemExit(1)


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True, cwd=ROOT,
                          encoding="utf-8", errors="replace")


def d2_pages(doc: str) -> list[str]:
    parts = doc.split("| Page | Sections | Class | Notes |", 1)
    if len(parts) < 2:
        die("D.2 table not found")
    table = parts[1].split("\n\n", 1)[0]
    return [c for c in re.findall(r"^\| ([^|]+?) \| §", table, re.MULTILINE)]


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

    print("[1/4] drop the deleted draft row")
    if DRAFT in text:
        text = text.replace(DRAFT, "", 1)
        print("     removed the page 8 draft row")
    else:
        print("     already gone")

    print("[2/4] pull the ranges back by one")
    for old, new in SHIFTS:
        if new in text:
            print("     already current")
            continue
        if old not in text:
            die(f"anchor not found: {old[:52]!r}")
        text = text.replace(old, new, 1)
        print(f"     fixed: {new.split('|')[1].strip():>7}  {new.split('|')[2].strip()}")
    if NOTE_NEW in text:
        print("     assembly note already current")
    elif NOTE_OLD in text:
        text = text.replace(NOTE_OLD, NOTE_NEW, 1)
        print("     assembly note rewritten")
    else:
        die("assembly note not recognised")
    README.write_text(text, encoding="utf-8", newline="\n")

    print("[3/4] gate")
    r = run([sys.executable, str(TOOL), "--check"])
    out = (r.stdout or "") + (r.stderr or "")
    print("     " + "\n     ".join(out.strip().splitlines()))
    if r.returncode != 0:
        die(f"--check exited {r.returncode}, expected 0")
    for w in ("unverified=0 ", "hotlinks=0", "toc_blocks=24", "literal_key=0"):
       