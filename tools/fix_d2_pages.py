#!/usr/bin/env python3
"""Bring Appendix D.2 back into agreement with the page index.

--fix-page8 deleted the superseded working-draft page but D.2 kept counting it,
so every range from page 9 onward sat one page high and the §59-§66 rows
collided with the plates on page 18.

[1/4] drop the dead draft row
[2/4] pull every range from page 9 back by one (guarded so a re-run cannot shift twice)
[3/4] rewrite the assembly note
[4/4] gate: the section rows must cover the index exactly, then commit

Usage: python tools/fix_d2_pages.py [--dry-run]
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"

DRAFT = "| 8 | §9–§11 | C | Early working draft"
PLATES = "| 18 | Plates 1–18 |"
APPENDIX = "| 28–31 | Appendix, author, Part XII, this page |"

PAGE_ROW = re.compile(r"^\|\s*(\d+(?:–\d+)?)\s*\|")
INDEX_ROW = re.compile(r"^\|\s*(\d+)\s*\|")

NOTE_MARK = "**Assembly.**"
NEW_NOTE = (
    "> **Assembly.** The superseded page 8 draft row has been removed; the map runs "
    "§1 from page 4 continuously to the plates on page 18 and the appendix from page 28."
)


def rejoin(lines: list[str], original: str) -> str:
    out = "\n".join(lines)
    if original.endswith("\n"):
        out += "\n"
    return out


def d2_bounds(lines: list[str]) -> tuple[int | None, int | None]:
    """Return the (start, end) slice of the Appendix D.2 table body."""
    for i, line in enumerate(lines):
        if line.startswith("| Page |") and "Contents" not in line:
            start = i + 1
            end = start
            while end < len(lines) and lines[end].startswith("|"):
                end += 1
            return start, end
    return None, None


def d2_rows(text: str) -> list[str]:
    lines = text.splitlines()
    start, end = d2_bounds(lines)
    if start is None:
        return []
    return [line for line in lines[start:end] if PAGE_ROW.match(line)]


def index_pages(lines: list[str]) -> list[int]:
    """Page numbers from the `| Page | Contents |` table only."""
    for i, line in enumerate(lines):
        if line.strip() == "| Page | Contents |":
            pages: list[int] = []
            for follow in lines[i + 1 :]:
                if not follow.startswith("|"):
                    break
                m = INDEX_ROW.match(follow)
                if m:
                    pages.append(int(m.group(1)))
            return pages
    return []


def shift_row(line: str) -> str:
    m = PAGE_ROW.match(line)
    cell = m.group(1)
    pulled = "–".join(str(int(part) - 1) for part in cell.split("–"))
    return line[: m.start(1)] + pulled + line[m.end(1) :]


def main() -> int:
    dry = "--dry-run" in sys.argv
    text = README.read_text(encoding="utf-8")

    # [1/4] --------------------------------------------------------------
    lines = text.splitlines()
    start, end = d2_bounds(lines)
    if start is None:
        print("FAIL: could not find the Appendix D.2 table")
        return 1

    was_draft = any(line.startswith(DRAFT) for line in lines[start:end])
    if was_draft:
        body = [line for line in lines[start:end] if not line.startswith(DRAFT)]
        text = rejoin(lines[:start] + body + lines[end:], text)
        print("[1/4] removed the page 8 draft row")
    else:
        print("[1/4] draft row already gone")

    # [2/4] --------------------------------------------------------------
    lines = text.splitlines()
    start, end = d2_bounds(lines)
    plates_high = any(line.startswith("| 19 | Plates") for line in lines[start:end])
    if was_draft or plates_high:
        body = []
        moved = 0
        for line in lines[start:end]:
            m = PAGE_ROW.match(line)
            if m and int(m.group(1).split("–")[0]) >= 9:
                line = shift_row(line)
                moved += 1
            body.append(line)
        text = rejoin(lines[:start] + body + lines[end:], text)
        print(f"[2/4] pulled {moved} range(s) back by one")
    else:
        print("[2/4] ranges already shifted")

    # [3/4] --------------------------------------------------------------
    lines = text.splitlines()
    start, end = d2_bounds(lines)
    region = lines[start:end]
    if any(NOTE_MARK in line for line in region):
        print("[3/4] assembly note already current")
    else:
        hit = next(
            (i for i, line in enumerate(region) if "draft" in line.lower()),
            None,
        )
        if hit is None:
            print("[3/4] assembly note left as-is (no draft reference found)")
        else:
            region = list(region)
            region[hit] = NEW_NOTE
            text = rejoin(lines[:start] + region + lines[end:], text)
            print("[3/4] rewrote the assembly note")

    # [4/4] --------------------------------------------------------------
    lines = text.splitlines()
    pages = index_pages(lines)
    if pages != list(range(1, 34)):
        print(f"FAIL: page index is {pages}")
        return 1

    rows = d2_rows(text)
    print(f"      D.2 pages are {[PAGE_ROW.match(r).group(1) for r in rows]}")

    if not any(r.startswith(PLATES) for r in rows):
        print("FAIL: the plates row is not on page 18")
        return 1
    if not any(r.startswith(APPENDIX) for r in rows):
        print("FAIL: the appendix row is not 28–31")
        return 1

    sections = [r for r in rows if r.split("|")[2].strip().startswith("§")]
    others = [r for r in rows if r not in sections]

    blocked = {1, 2, 3, 18}
    for row in others:
        for part in PAGE_ROW.match(row).group(1).split("–"):
            blocked.add(int(part))

    expect = [str(p) for p in pages if 4 <= p < 28 and p not in blocked]

    got: list[str] = []
    for row in sections:
        got.extend(PAGE_ROW.match(row).group(1).split("–"))

    if got != expect:
        print(f"FAIL: D.2 section rows cover {got}")
        print(f"      the page index implies {expect}")
        return 1

    check = subprocess.run(
        [sys.executable, "tools/patch_readme.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if check.returncode != 0:
        print("FAIL: --check is not green")
        print(check.stdout + check.stderr)
        return 1
    counted = re.search(r"unverified=(\d+)", check.stdout + check.stderr)
    if counted and counted.group(1) != "0":
        print(f"FAIL: unverified={counted.group(1)}")
        return 1

    print(f"[4/4] {len(rows)} D.2 rows, {len(got)} section pages, gate green")

    if dry:
        print("dry run: nothing written")
        return 0

    readme_dirty = README.read_text(encoding="utf-8") != text
    README.write_text(text, encoding="utf-8", newline="\n")
    subprocess.run(
        ["git", "add", "README.md", "tools/fix_d2_pages.py"], cwd=ROOT, check=True
    )

    staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
    if staged.returncode == 0:
        print("tree already current, nothing to commit")
        return 0

    message = (
        "Fix Appendix D.2 page ranges and drop the dead draft row"
        if readme_dirty
        else "Harden the fix_d2_pages.py commit step"
    )
    subprocess.run(["git", "commit", "-m", message], cwd=ROOT, check=True)
    print(f"committed: {message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())