#!/usr/bin/env python3
"""settle.py — run the pipeline until the byte count stops moving, then push.

The strip regexes now consume the blanks they insert, so repeated runs converge
rather than grow. This loops until two consecutive sizes match, confirms with
one more run, gates, and only then commits.

  python tools/settle.py          # settle, gate, push
  python tools/settle.py --dry    # settle, gate, no push
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

TOOL = Path("tools/patch_readme.py")
README = Path("README.md")
MSG = "fix: strip regexes consume the blank line they insert"
MAX_RUNS = 6

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

    print("[0/3] preconditions")
    for p in (TOOL, README, Path(".git")):
        if not p.exists():
            die(f"missing {p}")
    src = TOOL.read_text(encoding="utf-8")
    for need, label in (('"2.5"', "v2.5"),
                        ('r"---\\n---\\n\\s*$"', "separator strip"),
                        ('r"\\n*<!-- patch:img', "image strip"),
                        ('r"\\n*<!-- patch:status', "status strip"),
                        ('\\n*<!-- patch:(91|92|119)', "verify strip")):
        if need not in src:
            die(f"{label} missing from tools/patch_readme.py")

    print(f"[1/3] settle (max {MAX_RUNS} runs)")
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

    print("[2/3] confirm")
    again = once("confirm")
    if again != prev:
        die(f"not a fixed point: {prev} -> {again} bytes")
    print(f"     holds at {again} bytes")

    print("[3/3] gate")
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
    if len(re.findall(r"^#{1,2} ", text, re.MULTILINE)) < 130:
        die("heading count collapsed")
    print(f"     {len(foot)} footers, {seps} separators, {blocks} toc blocks")

    print("[4] commit")
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