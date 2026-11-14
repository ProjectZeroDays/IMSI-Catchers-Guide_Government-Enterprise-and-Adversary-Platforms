#!/usr/bin/env python3
"""fix_drift.py — stop build_toc duplicating the region separator, verify, push.

  1. inserts the separator strip into build_toc (skipped if already there)
  2. runs the pipeline twice and requires an identical byte count
  3. gates on the counts, the footer set and the separator count
  4. commits and pushes only if every gate passes

  python tools/fix_drift.py           # patch, verify, gate, push
  python tools/fix_drift.py --dry     # patch, verify, gate, no push
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

TOOL = Path("tools/patch_readme.py")
README = Path("README.md")
MSG = "fix: build_toc no longer duplicates the region separator"

ANCHOR = ('    body = FOOTER.sub("", body)\n'
          '    body = body.split("## Table of Contents", 1)[-1]\n')
LINE = '    body = re.sub(r"---\\n---\\n\\s*$", "", body)\n'

WANT = ("unverified=3 hotlinks=0 missing_assets=0 toc_blocks=24",
        "literal_key=0", "part6=True", "frontback_links=True")


def die(m: str) -> None:
    print(f"\nFAIL: {m}", file=sys.stderr)
    raise SystemExit(1)


def step(n: str, m: str) -> None:
    print(f"[{n}/4] {m}")


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def main() -> int:
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="replace")
    dry = "--dry" in sys.argv

    # 0. preconditions
    step("0/4", "preconditions")
    for p in (TOOL, README, Path(".git")):
        if not p.exists():
            die(f"missing {p}")
    src = TOOL.read_text(encoding="utf-8")
    if '"2.5"' not in src:
        die("tools/patch_readme.py is not v2.5")
    if "re.sub(r\"<summary>" not in src:
        die("summary unwrap missing — re-paste tools/patch_readme.py")

    # 1. insert the strip line, idempotently
    step("1/4", "separator strip")
    if LINE in src:
        print("     already present, nothing to insert")
    else:
        hits = src.count(ANCHOR)
        if hits != 1:
            die(f"anchor found {hits} times in build_toc, expected 1")
        shutil.copy2(TOOL, TOOL.with_suffix(".py.pre-drift"))
        TOOL.write_text(src.replace(ANCHOR, ANCHOR.splitlines(True)[0] + LINE
                                    + ANCHOR.splitlines(True)[1], 1),
                        encoding="utf-8", newline="\n")
        print("     inserted after the FOOTER strip")

    # 2. two runs, byte count must hold
    step("2/4", "idempotency")
    sizes = []
    for i in (1, 2):
        r = run([sys.executable, str(TOOL), "--run"])
        out = (r.stdout or "") + (r.stderr or "")
        print("     " + "\n     ".join(out.strip().splitlines()))
        if r.returncode > 1:
            die(f"run {i} exited {r.returncode} (structural)")
        for w in WANT:
            if w not in out:
                die(f"run {i}: check line missing {w!r}")
        if "warn: no TOC labels found" in out:
            die(f"run {i}: TOC parser lost its labels")
        sizes.append(README.stat().st_size)
        print(f"     run {i}: {sizes[-1]} bytes")

    if sizes[0] != sizes[1]:
        die(f"still drifting: {sizes[0]} -> {sizes[1]} bytes")
    print(f"     stable at {sizes[1]} bytes")

    # 3. gate
    step("3/4", "gate")
    text = README.read_text(encoding="utf-8")
    foot = re.findall(r"\*Version [\d.]+ · Page \d+ of \d+\.[^*\n]*\*", text)
    if len(foot) != 3:
        die(f"{len(foot)} footers, expected 3")
    if not any("Page 2 of 34" in f for f in foot):
        die("no footer on page 2")
    seps = len(re.findall(r"^---$", text, re.MULTILINE))
    if not 60 <= seps <= 70:
        die(f"{seps} separator lines, expected 66")
    blocks = len(re.findall(r'<details class="toc">', text))
    if blocks != 24:
        die(f"{blocks} toc blocks, expected 24")
    if text.count("{key}"):
        die("literal {key} close tag present")
    print(f"     {len(foot)} footers, {seps} separators, {blocks} toc blocks")

    # 4. commit and push
    step("4/4", "commit")
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