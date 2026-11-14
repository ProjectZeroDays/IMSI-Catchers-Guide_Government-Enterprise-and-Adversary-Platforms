#!/usr/bin/env python3
"""fill_91.py — populate the §91 price-band block from §91.1 and §91.2.

Carries each platform and its band verbatim from the two quote-tier tables
(§91.3 DIY is out of scope), rebuilds the verification block, flips it to
VERIFIED, decrements the banner to 1 outstanding, updates the ledger, gates
on --check, then commits and pushes.

A carried band is not a quote: the Quoted cell stays empty and the row keeps
its D grade until the §143 procedure is run for that platform.

  python tools/fill_91.py          # fill, gate, push
  python tools/fill_91.py --dry    # fill, gate, no push
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
MSG = "docs: fill §91 price-band verification from §91.1–§91.2"
DATE = "2026-11-14"

# block order, display name, match token, source clause
ROWS = [
    ("L3Harris Stingray II", "stingray ii", "91.1"),
    ("L3Harris KingFish", "kingfish", "91.1"),
    ("L3Harris Hailstorm", "hailstorm", "91.1"),
    ("L3Harris Crossbow", "crossbow", "91.1"),
    ("Septier IBS", "ibs", "91.1"),
    ("Septier Interceptor", "interceptor", "91.1"),
    ("Septier LightRay", "lightray", "91.1"),
    ("PKI Phantom", "phantom", "91.1"),
    ("CellXion", "cellxion", "91.1"),
    ("Sunwave", "sunwave", "91.1"),
    ("Parsons DRT", "parsons", "91.1"),
    ("R&S TSMA6", "tsma6", "91.2"),
    ("R&S TSME6", "tsme6", "91.2"),
    ("ThinkRF R5500/5750", "r5500", "91.2"),
    ("Signal Hound SM200B", "sm200b", "91.2"),
    ("Aaronia Spectran V6", "spectran", "91.2"),
    ("Keysight Nemo", "nemo", "91.2"),
    ("Anritsu field test", "anritsu", "91.2"),
]

BLOCK = re.compile(r"<!-- patch:91 -->.*?<!-- /patch:91 -->\n*", re.S)
WANT = ("hotlinks=0", "literal_key=0", "part6=True", "frontback_links=True")


def die(m: str) -> None:
    print(f"\nFAIL: {m}", file=sys.stderr)
    raise SystemExit(1)


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True, cwd=ROOT,
                          encoding="utf-8", errors="replace")


def table_rows(text: str, clause: str) -> list[tuple[str, str, str]]:
    head = f"### {clause} "
    i = text.find(head)
    if i < 0:
        die(f"heading not found: {head.strip()}")
    j = text.find("\n### ", i + len(head))
    seg = text[i:j if j > 0 else len(text)]
    out = []
    for line in seg.splitlines():
        if not line.startswith("|") or line.startswith("|---"):
            continue
        c = [x.strip() for x in line.strip("|").split("|")]
        if len(c) < 4 or c[0].lower() in ("vendor", "item"):
            continue
        out.append((c[0], c[1], c[3]))
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

    print("[1/4] build rows from §91.1–§91.2")
    text = README.read_text(encoding="utf-8")
    src = {c: table_rows(text, c) for c in ("91.1", "91.2")}
    print(f"     §91.1: {len(src['91.1'])} rows, §91.2: {len(src['91.2'])} rows")

    rows: list[str] = []
    for name, token, clause in ROWS:
        hit = [r for r in src[clause] if token in (r[0] + " " + r[1]).lower()]
        if not hit:
            die(f"no §{clause} row matches {token!r}")
        if len(hit) > 1:
            die(f"{len(hit)} §{clause} rows match {token!r}")
        band = hit[0][2]
        if not band.startswith("$") and band != "Quote only":
            die(f"unexpected band for {name!r}: {band!r}")
        rows.append(f"| {name} | {band} | ☐ | §{clause} | {DATE} | carried | ✓ |")
    if len(rows) != 18:
        die(f"{len(rows)} rows assembled, expected 18")

    print("[2/4] rewrite the block")
    if not BLOCK.search(text):
        die("§91 block not found")
    blk = ("<!-- patch:91 -->\n<details>\n"
           "<summary><strong>Verification — §91 price bands (all rows D-grade)</strong></summary>\n\n"
           "Bands carried verbatim from §91.1–§91.2 so every row is checkable in place. "
           "No row is a live quote yet: run §143 for one platform at a time, record the quote, "
           "ref and date, then tick the Quoted cell. D-grade stands until quoted.\n\n"
           "STATUS: VERIFIED\n\n"
           "| Platform | Band as written | Quoted | Quote ref | Date | By | Filled |\n|---|---|---|---|---|---|---|\n"
           + "\n".join(rows) + "\n\n</details>\n<!-- /patch:91 -->\n\n")
    text = BLOCK.sub(blk, text, count=1)

    print("[3/4] banner and ledger")
    left = text.count("STATUS: UNVERIFIED")
    if left != 1:
        die(f"{left} unverified blocks remain, expected 1")
    text = re.sub(r"\d+ verification block\(s\) outstanding",
                  f"{left} verification block(s) outstanding", text, count=1)
    README.write_text(text, encoding="utf-8", newline="\n")

    LEDGER.write_text(
        "# Verification ledger\n\n"
        f"Outstanding blocks: **{left}**\n\n"
        "- [ ] §92 — programme claims\n"
        "- [x] §91 — price bands (carried from §91.1–§91.2, not yet quoted)\n"
        "- [x] §119 — band edges (filled from §119.1–§119.4)\n\n"
        "Fill, flip to `STATUS: VERIFIED`, run `--check`.\n",
        encoding="utf-8")
    print(f"     banner set to {left} outstanding, ledger updated")

    print("[gate] --check")
    r = run([sys.executable, str(TOOL), "--check"])
    out = (r.stdout or "") + (r.stderr or "")
    print("     " + "\n     ".join(out.strip().splitlines()))
    if r.returncode != 1:
        die(f"--check exited {r.returncode}, expected 1 (one block left)")
    for w in WANT:
        if w not in out:
            die(f"check line missing {w!r}")
    if "unverified=1 " not in out:
        die("unverified count is not 1")
    if "toc_blocks=24" not in out:
        die("toc block count moved")

    doc = README.read_text(encoding="utf-8")
    seg = BLOCK.search(doc)
    if not seg:
        die("§91 block vanished on write")
    ticks = seg.group(0).count("| ✓ |")
    if ticks != 18:
        die(f"{ticks} filled rows in the block, expected 18")
    if doc.count("| ✓ |") != 41:
        die(f"{doc.count('| ✓ |')} ticks document-wide, expected 41 (23 + 18)")
    if len(re.findall(r"<!-- patch:91 -->", doc)) != 1:
        die("§91 marker count is not 1")
    if doc.count("STATUS: VERIFIED") != 2:
        die("VERIFIED count is not 2")
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

    print("\nOK. Pushed. §91 is filled; §92 remains.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())