#!/usr/bin/env python3
"""fix_dup_lookup.py — collapse the doubled §139 lookup row and footer sentence,
and make fix_index_and_link.py idempotent.

Two FIXES entries had `old` as an exact prefix of `new`, so the
`new in text and old not in text` test could never report them as applied and a
second run doubled them. The test becomes `new in text`, which asks whether the
result is already present.

  python tools/fix_dup_lookup.py          # fix, gate, push
  python tools/fix_dup_lookup.py --dry    # fix, gate, no push
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
TOOL = ROOT / "tools" / "patch_readme.py"
FIXER = ROOT / "tools" / "fix_index_and_link.py"
MSG = "docs: dedupe §139 lookup row and footer prose; make the fixer idempotent"

DUPS = [
    "| 139 | 28 |\n",
    " Page 28 is this page; §139 follows on it.",
]
TEST_OLD = "        if new in text and old not in text:"
TEST_NEW = "        if new in text:"


def die(m: str) -> None:
    print(f"\nFAIL: {m}", file=sys.stderr)
    raise SystemExit(1)


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True, cwd=ROOT,
                          encoding="utf-8", errors="replace")


def main() -> int:
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="replace")
    dry = "--dry" in sys.argv

    print("[0/4] preconditions")
    for p in (README, TOOL, FIXER, ROOT / ".git"):
        if not p.exists():
            die(f"missing {p}")
    text = README.read_text(encoding="utf-8")
    fixer = FIXER.read_text(encoding="utf-8")

    print("[1/4] collapse duplicates")
    for dup in DUPS:
        n = text.count(dup)
        while text.count(dup + dup):
            text = text.replace(dup + dup, dup, 1)
        left = text.count(dup)
        if left != 1:
            die(f"{left} copies of {dup.strip()[:40]!r}, expected 1")
        print(f"     {n} -> {left}: {dup.strip()[:48]}")
    README.write_text(text, encoding="utf-8", newline="\n")

    print("[2/4] make the fixer idempotent")
    if TEST_NEW in fixer and TEST_OLD not in fixer:
        print("     already strict")
    elif TEST_OLD in fixer:
        FIXER.write_text(fixer.replace(TEST_OLD, TEST_NEW, 1),
                         encoding="utf-8", newline="\n")
        print("     test is now `new in text`")
    else:
        die("idempotency test not recognised")

    print("[3/4] gate")
    r = run([sys.executable, str(TOOL), "--check"])
    out = (r.stdout or "") + (r.stderr or "")
    print("     " + "\n     ".join(out.strip().splitlines()))
    if r.returncode != 0:
        die(f"--check exited {r.returncode}, expected 0")
    for w in ("unverified=0 ", "hotlinks=0", "toc_blocks=24", "literal_key=0"):
        if w not in out:
            die(f"check line missing {w!r}")

    doc = README.read_text(encoding="utf-8")
    if doc.count("| 139 | 28 |") != 1:
        die("§139 row is not single")
    if doc.count("Page 28 is this page; §139 follows on it.") != 1:
        die("footer sentence is not single")
    parts = doc.split("| Page | Contents |", 1)
    if len(parts) < 2:
        die("page index table not found")
    nums = [int(n) for n in re.findall(r"^\| (\d+) \| ", parts[1].split("\n\n", 1)[0], re.MULTILINE)]
    if nums != list(range(1, 34)):
        die(f"page index rows are {len(nums)}: {nums}")
    if doc.count("| ✓ |") != 55:
        die(f"{doc.count('| ✓ |')} ticks, expected 55")
    print(f"     one §139 row, index 1-33, {doc.count('| ✓ |')} ticks intact")

    print("[4/4] re-run the fixer to prove it holds")
    d = run([sys.executable, str(FIXER), "--dry"])
    lines = (d.stdout or "").splitlines()
    print("     " + "\n     ".join(lines[-4:]))
    if d.returncode != 0:
        die("fixer no longer passes on the repaired file")
    if "index runs 1-33 with no hole" not in (d.stdout or ""):
        die("fixer gate did not reach its row check")

    after = README.read_text(encoding="utf-8")
    if after.count("| 139 | 28 |") != 1 or after.count("Page 28 is this page; §139 follows on it.") != 1:
        die("dry re-run re-doubled the rows")

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

    print("\nOK. Pushed. One §139 row, one footer sentence, fixer idempotent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())