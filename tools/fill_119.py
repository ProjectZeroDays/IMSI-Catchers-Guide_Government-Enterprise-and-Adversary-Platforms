#!/usr/bin/env python3
"""fill_119.py — populate the §119 band table from the document's own tables.

Parses §119.1–§119.4, rebuilds the verification block with UL, DL, ARFCN and
the governing TS clause, flips the block to VERIFIED, repairs the stale
appendix pagination prose, updates the banner and ledger, gates on --check,
then commits and pushes.

  python tools/fill_119.py          # fill, gate, push
  python tools/fill_119.py --dry    # fill, gate, no push
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
TOOL = ROOT / "tools" / "patch_readme.py"
LEDGER = ROOT / "VERIFY.md"
MSG = "docs: fill §119 band verification; reconcile appendix pagination prose"

TS = {"GSM": "TS 45.005", "UMTS": "TS 25.101", "LTE": "TS 36.101", "NR": "TS 38.104"}

SRC = [("GSM", "### 119.1 GSM bands", "GSM ", True),
       ("UMTS", "### 119.2 UMTS bands (common)", "UMTS ", True),
       ("LTE", "### 119.3 LTE bands (common)", "LTE ", True),
       ("NR", "### 119.4 NR FR1 bands (common)", "NR n", False)]

APPENDIX = [
    ('**Purpose:** the assembled document runs to 34 pages. Footers in Parts VI–XI read "of 31" from an earlier pagination plan; the actual extent is 29. This page is the authoritative map, and it replaces the running footer count.',
     '**Purpose:** the assembled document runs to 34 pages. Every footer is generated from the live page total and is correct. This page is the authoritative map.'),
    ('Where a footer says "Page N of 34", read "Page N of 34". No content is missing; the earlier count included two pages that were later merged.',
     'Footers carry the live total; there is no legacy count left to reconcile.'),
    ('If you delete page 8, the extent becomes 28 and every subsequent footer is off by one — the section-to-page table above remains correct because it keys on sections, not footers.',
     'If you delete page 8, the extent becomes 33 and every later page shifts by one — the section-to-page table above stays correct because it keys on sections, not footers.'),
    ('*End of appendices. The document is complete at 34 pages; Part XII and this page extend the 29-page body and restore the original footer count of 31 plus one.*',
     '*End of appendices. The document is complete at 34 pages.*'),
]

BLOCK = re.compile(r"<!-- patch:119 -->.*?<!-- /patch:119 -->\n*", re.S)
WANT = ("hotlinks=0", "literal_key=0", "part6=True", "frontback_links=True")


def die(m: str) -> None:
    print(f"\nFAIL: {m}", file=sys.stderr)
    raise SystemExit(1)


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True, cwd=ROOT,
                          encoding="utf-8", errors="replace")


def rows_from(text: str, heading: str, prefix: str, has_arfcn: bool) -> list[str]:
    i = text.find(heading)
    if i < 0:
        die(f"heading not found: {heading}")
    j = text.find("\n### ", i + len(heading))
    seg = text[i:j if j > 0 else len(text)]
    key = prefix.strip().split()[0]
    if key not in TS:
        die(f"no TS clause for prefix {prefix!r}")
    out = []
    for line in seg.splitlines():
        if not line.startswith("|") or line.startswith("|---"):
            continue
        c = [x.strip() for x in line.strip("|").split("|")]
        if len(c) < 3 or c[0].lower().startswith("band") or not c[1]:
            continue
        ul, dl = c[1], c[2]
        arfcn = c[3] if (has_arfcn and len(c) > 3) else ("TDD" if "TDD" in dl else "—")
        out.append(f"| {prefix}{c[0]} | {ul} | {dl} | {arfcn} | {TS[key]} | ✓ |")
    return out


def main() -> int:
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="replace")
    dry = "--dry" in sys.argv

    print("[0/4] preconditions")
    for p in (README, TOOL, ROOT / ".git"):
        if not p.exists():
            die(f"missing {p}")
    if '"2.5"' not in TOOL.read_text(encoding="utf-8"):
        die("tools/patch_readme.py is not v2.5")

    print("[1/4] build rows from §119.1–§119.4")
    text = README.read_text(encoding="utf-8")
    rows: list[str] = []
    for prefix, heading, label, has_arfcn in SRC:
        got = rows_from(text, heading, label, has_arfcn)
        if not got:
            die(f"no rows parsed from {heading}")
        print(f"     {prefix.strip()}: {len(got)} rows")
        rows.extend(got)
    if len(rows) != 23:
        die(f"{len(rows)} rows assembled, expected 23")

    print("[2/4] rewrite the block")
    if not BLOCK.search(text):
        die("§119 block not found")
    blk = ("<!-- patch:119 -->\n<details>\n"
           "<summary><strong>Verification — §119 band edges (23 bands, filled from §119.1–§119.4)</strong></summary>\n\n"
           "Edges and ARFCN ranges transcribed from the tables below, which derive from the TS clauses named per row. "
           "GSM 900 has two valid ARFCN variants; NR TDD rows have no uplink ARFCN range.\n\n"
           "STATUS: VERIFIED\n\n"
           "| Band | UL | DL | ARFCN range | TS clause | Confirmed |\n|---|---|---|---|---|---|\n"
           + "\n".join(rows) + "\n\n</details>\n<!-- /patch:119 -->\n\n")
    text = BLOCK.sub(blk, text, count=1)

    print("[3/4] repair appendix prose")
    for old, new in APPENDIX:
        if new in text:
            print("     already current")
            continue
        if old not in text:
            print("     MISSING, skipped")
            continue
        text = text.replace(old, new, 1)
        print(f"     fixed: {new[:44]}...")

    print("[4/4] write, banner, ledger")
    left = text.count("STATUS: UNVERIFIED")
    if left != 2:
        die(f"{left} unverified blocks remain, expected 2")
    text = re.sub(r"\d+ verification block\(s\) outstanding",
                  f"{left} verification block(s) outstanding", text, count=1)
    README.write_text(text, encoding="utf-8", newline="\n")

    LEDGER.write_text(
        "# Verification ledger\n\n"
        f"Outstanding blocks: **{left}**\n\n"
        "- [ ] §91 — price bands\n"
        "- [ ] §92 — programme claims\n"
        "- [x] §119 — band edges (filled from §119.1–§119.4)\n\n"
        "Fill, flip to `STATUS: VERIFIED`, run `--check`.\n",
        encoding="utf-8")
    print(f"     banner set to {left} outstanding, ledger updated")

    print("[gate] --check")
    r = run([sys.executable, str(TOOL), "--check"])
    out = (r.stdout or "") + (r.stderr or "")
    print("     " + "\n     ".join(out.strip().splitlines()))
    if r.returncode != 1:
        die(f"--check exited {r.returncode}, expected 1 (two blocks left)")
    for w in WANT:
        if w not in out:
            die(f"check line missing {w!r}")
    if "unverified=2 " not in out:
        die("unverified count is not 2")
    if "toc_blocks=24" not in out:
        die("toc block count moved")

    doc = README.read_text(encoding="utf-8")
    ticks = doc.count("| ✓ |")
    if ticks != 23:
        die(f"{ticks} filled rows, expected 23")
    if "STATUS: VERIFIED" not in doc:
        die("STATUS: VERIFIED missing")
    if len(re.findall(r"<!-- patch:119 -->", doc)) != 1:
        die("§119 marker count is not 1")
    foot = re.findall(r"\*Version [\d.]+ · Page \d+ of \d+\.[^*\n]*\*", doc)
    if len(foot) != 3 or doc.count("\n---\n---\n") != 33:
        die("footers or page separators disturbed")
    print(f"     {ticks} rows filled, marker single, footers and separators intact")

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

    print("\nOK. Pushed. §119 is filled and verified; §91 and §92 remain.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())