#!/usr/bin/env python3
"""fix_title.py — move the subtitle's opening ** back onto its own line.

The previous repair left the opening emphasis glued to the end of the H1, so
the title line closed a bold it never opened and the subtitle had no opener.
This moves it, then settles, gates and pushes. The gate searches the whole
document rather than a fixed line window, and counts the doubled page
separator rather than every horizontal rule.

  python tools/fix_title.py          # repair, settle, gate, push
  python tools/fix_title.py --dry    # repair, settle, gate, no push
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

TOOL = Path("tools/patch_readme.py")
README = Path("README.md")
MSG = "fix: restore the subtitle's opening emphasis; banner placement holds"
MAX_RUNS = 8

SUB = "Reference, Field Guide, Build Manual, Category Study and Technical Annexes"
BAD = f"Adversary-Platforms**\n\n{SUB}**"
GOOD = f"Adversary-Platforms\n\n**{SUB}**"

WANT = ("unverified=3 hotlinks=0 missing_assets=0 toc_blocks=24",
        "literal_key=0", "part6=True", "frontback_links=True")


def die(m: str) -> None:
    print(f"\nFAIL: {m}", file=sys.stderr)
    raise SystemExit(1)


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def once(tag: str) -> int:
    r = run([sys.executable, str(TOOL), "--run"])
    out = (r.stdout or "") + (r.stderr or "")
    if r.returncode > 1:
        die(f"{tag}: exited {r.returncode} (structural)\n{out}")
    for w in WANT:
        if w not in out:
            die(f"{tag}: check line missing {w!r}\n{out}")
    if "warn: no TOC labels found" in out:
        die(f"{tag}: TOC parser lost its labels")
    size = README.stat().st_size
    print(f"     {tag}: {size} bytes")
    return size


def main() -> int:
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="replace")
    dry = "--dry" in sys.argv

    print("[0/4] preconditions")
    for p in (TOOL, README, Path(".git")):
        if not p.exists():
            die(f"missing {p}")
    src = TOOL.read_text(encoding="utf-8")
    if '"2.5"' not in src:
        die("tools/patch_readme.py is not v2.5")
    if "blk + a, 1)" not in src:
        die("status anchor missing — run tools/fix_strip3.py first")

    print("[1/4] repair subtitle emphasis")
    doc = README.read_text(encoding="utf-8")
    if GOOD in doc:
        print("     already correct")
    elif BAD in doc:
        README.write_text(doc.replace(BAD, GOOD, 1), encoding="utf-8", newline="\n")
        print("     emphasis moved to the subtitle line")
    else:
        die("neither the broken nor the correct subtitle was found — paste the head")

    print(f"[2/4] settle (max {MAX_RUNS} runs)")
    prev = once("run 1")
    stable = False
    for i in range(2, MAX_RUNS + 1):
        size = once(f"run {i}")
        if size == prev:
            print(f"     converged at {size} bytes after {i - 1} runs")
            stable = True
            break
        print(f"     delta {size - prev:+d}")
        prev = size
    if not stable:
        die(f"no fixed point after {MAX_RUNS} runs — last {prev} bytes")

    print("[3/4] gate")
    text = README.read_text(encoding="utf-8")
    if not re.search(r"^# IMSI Catchers:[^\n]*Platforms$", text, re.MULTILINE):
        die("H1 line is not clean")
    if not re.search(r"^\*\*Reference[^\n]*\*\*$", text, re.MULTILINE):
        die("subtitle line is not clean")
    if not re.search(r"\*\*Reference[^\n]*\*\*\n\n<!-- patch:status -->", text):
        die("banner not directly under the subtitle")
    if "## About this edition" not in text:
        die("About heading missing")
    for k in ("91", "92", "119"):
        c = len(re.findall(rf"<!-- patch:{k} -->", text))
        if c != 1:
            die(f"§{k} block x{c}")
    foot = re.findall(r"\*Version [\d.]+ · Page \d+ of \d+\.[^*\n]*\*", text)
    if len(foot) != 3 or not any("Page 2 of 34" in f for f in foot):
        die(f"footer set wrong: {len(foot)}")
    sep = text.count("\n---\n---\n")
    if sep != 33:
        die(f"{sep} page separators, expected 33")
    blocks = len(re.findall(r'<details class="toc">', text))
    if blocks != 24:
        die(f"{blocks} toc blocks, expected 24")
    print(f"     head clean, markers single, {len(foot)} footers, {sep} seps, {blocks} blocks")

    print("[4/4] commit")
    run(["git", "add", "-A"])
    c = run(["git", "commit", "-m", MSG])
    print("     " + " ".join((c.stdout or c.stderr).strip().splitlines()[:2]))
    if c.returncode != 0:
        die("commit failed — inspect `git status`")

    if dry:
        print("\nOK, committed, not pushed (--dry).")
        return 0

    p = run(["git", "push"])
    print("     " + " ".join((p.stdout or p.stderr).strip().splitlines()[-2:]))
    if p.returncode != 0:
        die("push failed — the commit stands, retry `git push`")

    print("\nOK. Pushed. Now open the rendered page and confirm the triangles.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())