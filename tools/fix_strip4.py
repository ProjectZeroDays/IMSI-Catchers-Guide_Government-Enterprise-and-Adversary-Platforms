#!/usr/bin/env python3
"""fix_strip4.py — \n* on both sides of every strip, \n\n restored on both sides.

Strips tolerate any number of surrounding newlines, so they match blocks written
by earlier versions. Every insert puts exactly two newlines back on each side,
so headings cannot fuse. block() ends with two newlines so it restores its own
right side. Settle loop must reach a fixed point before committing.

  python tools/fix_strip4.py          # patch, settle, gate, push
  python tools/fix_strip4.py --dry    # patch, settle, gate, no push
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

TOOL = Path("tools/patch_readme.py")
README = Path("README.md")
MSG = "fix: tolerant strips that restore both sides; banner off the H1"
MAX_RUNS = 8

EDITS = [
    ("verify strip",
     'VERIFY_STRIP = re.compile(r"\\n\\n<!-- patch:(91|92|119) -->.*?<!-- /patch:(?:\\1|\\{key\\}) -->\\n\\n", re.S)',
     'VERIFY_STRIP = re.compile(r"\\n*<!-- patch:(91|92|119) -->.*?<!-- /patch:(?:\\1|\\{key\\}) -->\\n*", re.S)'),
    ("image strip",
     '    text = re.sub(r"\\n\\n<!-- patch:img:[^>]*-->.*?<!-- /patch:img -->\\n\\n", "", text, flags=re.S)\n',
     '    text = re.sub(r"\\n*<!-- patch:img:[^>]*-->.*?<!-- /patch:img -->\\n*", "", text, flags=re.S)\n'),
    ("status strip",
     '    text = re.sub(r"\\n\\n<!-- patch:status -->.*?<!-- /patch:status -->\\n\\n", "", text, flags=re.S)\n',
     '    text = re.sub(r"\\n*<!-- patch:status -->.*?<!-- /patch:status -->\\n*", "", text, flags=re.S)\n'),
    ("block tail",
     '            f"\\n\\n</details>\\n<!-- /patch:{key} -->\\n")',
     '            f"\\n\\n</details>\\n<!-- /patch:{key} -->\\n\\n")'),
]

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

    print("[0/5] preconditions")
    for p in (TOOL, README, Path(".git")):
        if not p.exists():
            die(f"missing {p}")
    src = TOOL.read_text(encoding="utf-8")
    if '"2.5"' not in src:
        die("tools/patch_readme.py is not v2.5")
    if 'r"---\\n---\\n\\s*$"' not in src:
        die("separator strip missing — run tools/fix_drift.py first")
    if 'blk + a, 1)' not in src:
        die("status anchor missing — run tools/fix_strip3.py first")

    print("[1/5] tool edits")
    shutil.copy2(TOOL, TOOL.with_suffix(".py.pre-strip4"))
    for name, old, new in EDITS:
        if new in src:
            print(f"     {name}: already tolerant")
            continue
        if src.count(old) != 1:
            die(f"{name}: anchor found {src.count(old)} times, expected 1")
        src = src.replace(old, new, 1)
        print(f"     {name}: tolerant")
    TOOL.write_text(src, encoding="utf-8", newline="\n")

    print("[2/5] repair duplicates and fused title")
    doc = README.read_text(encoding="utf-8")
    before = doc
    for k in ("91", "92", "119"):
        doc = re.sub(rf"(<!-- patch:{k} -->.*?<!-- /patch:{k} -->)\n*(?=.*?<!-- patch:{k} -->)", r"\1", doc, flags=re.S)
    doc = re.sub(rf"(<!-- patch:{k} -->.*?<!-- /patch:{k} -->)\n*", r"\1\n\n", doc, flags=re.S)
    doc = doc.replace("Adversary-Platforms**Reference, Field Guide",
                      "Adversary-Platforms**\n\nReference, Field Guide")
    doc = re.sub(r"<!-- patch:status -->.*?<!-- /patch:status -->\n*", "", doc, flags=re.S)
    if doc != before:
        README.write_text(doc, encoding="utf-8", newline="\n")
        print("     cleaned")
    else:
        print("     nothing to clean")

    print(f"[3/5] settle (max {MAX_RUNS} runs)")
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

    print("[4/5] gate")
    text = README.read_text(encoding="utf-8")
    head = "\n".join(text.splitlines()[:26])
    if re.search(r"Adversary-Platforms\*\*[^\n]", head):
        die("title still fused")
    if not re.search(r"\*\*Reference[^\n]*\*\*\n\n<!-- patch:status -->", head):
        die("banner not directly under the subtitle")
    if "## About this edition" not in head:
        die("About heading displaced")
    for k in ("91", "92", "119"):
        c = len(re.findall(rf"<!-- patch:{k} -->", text))
        if c != 1:
            die(f"§{k} block x{c}")
    foot = re.findall(r"\*Version [\d.]+ · Page \d+ of \d+\.[^*\n]*\*", text)
    if len(foot) != 3 or not any("Page 2 of 34" in f for f in foot):
        die(f"footer set wrong: {len(foot)}")
    seps = len(re.findall(r"^---$", text, re.MULTILINE))
    if not 60 <= seps <= 70:
        die(f"{seps} separators, expected 66")
    blocks = len(re.findall(r'<details class="toc">', text))
    if blocks != 24:
        die(f"{blocks} toc blocks, expected 24")
    print(f"     head clean, markers single, {len(foot)} footers, {seps} seps, {blocks} blocks")

    print("[5/5] commit")
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