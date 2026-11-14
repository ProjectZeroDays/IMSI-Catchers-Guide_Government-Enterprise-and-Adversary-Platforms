#!/usr/bin/env python3
"""ship_v25.py — restore the TOC footer, run the pipeline, gate, push.

  1. inserts the TOC version line into build_toc (skipped if already there)
  2. runs `python tools/patch_readme.py --run`
  3. gates on the check line, the footer set and the marker set
  4. commits and pushes only if every gate passes

  python tools/ship_v25.py            # edit, run, gate, push
  python tools/ship_v25.py --dry      # edit, run, gate, no push
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

TOOL = Path("tools/patch_readme.py")
README = Path("README.md")
MSG = "v2.5: TOC covers front matter, all parts and back matter; keyed verify markers; numeric part sort"

LINE = '    out.append(f"\\n*Version {VERSION} · Page 0 of 0. Next page: document map.*\\n")\n'
ANCHOR = '    text = text[:start] + "".join(out) + "---\\n---\\n\\n" + text[end:]\n'

WANT = ("unverified=3 hotlinks=0 missing_assets=0 toc_blocks=24",
        "literal_key=0", "part6=True", "frontback_links=True")


def die(m: str) -> None:
    print(f"\nFAIL: {m}", file=sys.stderr)
    raise SystemExit(1)


def step(n: str, m: str) -> None:
    print(f"[{n}] {m}")


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")


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
    if '"2.5"' not in TOOL.read_text(encoding="utf-8"):
        die("tools/patch_readme.py is not v2.5 — re-paste the file first")
    if "unwrap" not in TOOL.read_text(encoding="utf-8"):
        die("tools/patch_readme.py lacks the summary unwrap — re-paste the file")

    # 1. insert the footer line, idempotently
    step("1/4", "TOC footer line")
    src = TOOL.read_text(encoding="utf-8")
    if LINE in src:
        print("     already present, nothing to insert")
    else:
        hits = src.count(ANCHOR)
        if hits != 1:
            die(f"anchor found {hits} times in build_toc, expected 1")
        shutil.copy2(TOOL, TOOL.with_suffix(".py.pre-ship"))
        TOOL.write_text(src.replace(ANCHOR, LINE + ANCHOR, 1), encoding="utf-8", newline="\n")
        print("     inserted before the region splice")

    # 2. run the pipeline
    step("2/4", "pipeline")
    r = run([sys.executable, str(TOOL), "--run"])
    out = (r.stdout or "") + (r.stderr or "")
    print("     " + "\n     ".join(out.strip().splitlines()))
    if r.returncode > 1:
        die(f"patch_readme.py --run exited {r.returncode} (structural)")
    if r.returncode == 1:
        print("     exit 1 = verification blocks outstanding, expected")

    # 3. gate
    step("3/4", "gate")
    for w in WANT:
        if w not in out:
            die(f"check line missing {w!r}")

    text = README.read_text(encoding="utf-8")
    foot = re.findall(r"\*Version [\d.]+ · Page \d+ of \d+\.[^*\n]*\*", text)
    if len(foot) != 3:
        die(f"{len(foot)} footers, expected 3 — the TOC footer did not take")
    if not all("of 34" in f for f in foot):
        die("footer page total is not 34")
    if not any("Page 2 of 34" in f for f in foot):
        die("no footer on page 2 — the TOC page footer is missing")
    if text.count("{key}"):
        die("literal {key} close tag present")
    print(f"     {len(foot)} footers, TOC page footer present, page total 34")

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

    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()
    print(f"\nOK. Pushed to {branch}. Now open the rendered page and confirm the triangles appear.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())