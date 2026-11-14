#!/usr/bin/env python3
"""fix_v25.py — apply the v2.5 corrections to tools/patch_readme.py.

Each edit is an exact find/replace that must match exactly once. Already-applied
edits are skipped, so re-running is safe. Nothing is written unless every edit
resolves.

  python tools\\fix_v25.py            apply edits only
  python tools\\fix_v25.py --run      apply, restore README, run --all, then --check
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TARGET = Path("tools") / "patch_readme.py"
BAK = Path("tools") / "patch_readme.py.bak"

EDITS: list[tuple[str, str, str]] = [
    (
        "block() closing tag outside f-string",
        r'''            f"{hdr}\n|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n\n</details>\n<!-- /patch:{key} -->\n")''',
        r'''            f"{hdr}\n|---|---|---|---|---|---|\n" + "\n".join(rows) + f"\n\n</details>\n<!-- /patch:{key} -->\n")''',
    ),
    (
        "TOC groups: any bold label, numbered or bulleted entries",
        r'''    parts = re.split(r"^\*\*(Part [IVX]+ — [^\n*]+)\*\*\s*$", body, flags=re.MULTILINE)
    out = ["## Table of Contents\n", TOC_CSS]
    for i in range(1, len(parts), 2):
        title, chunk = parts[i], parts[i + 1]
        secs = re.findall(r"^\s*(\d+)\.\s*\[([^\]]+)\]\(#([^)]+)\)\s*$", chunk, re.MULTILINE)
        out.append(f"<details class=\"toc\">\n<summary>{title}</summary>\n")
        for num, label, anchor in secs:
            out.append(f"{num}. [{label}](#{anchor})\n")
        out.append("\n</details>\n")''',
        r'''    parts = re.split(r"^\*\*([^*\n]+)\*\*\s*$", body, flags=re.MULTILINE)
    out = ["## Table of Contents\n\n", TOC_CSS]
    for i in range(1, len(parts), 2):
        title, chunk = parts[i], parts[i + 1]
        entries = re.findall(r"^(?:(\d+)\.\s*|[-*]\s+)\[([^\]]+)\]\(#([^)]+)\)\s*$", chunk, re.MULTILINE)
        if not entries:
            continue
        out.append(f"<details class=\"toc\">\n<summary>{title}</summary>\n")
        for num, label, anchor in entries:
            out.append(f"{num}. [{label}](#{anchor})\n" if num else f"- [{label}](#{anchor})\n")
        out.append("\n</details>\n")''',
    ),
    (
        "index: skip empty pages",
        r'''    rows = [f"| {i + 1} | {head(p)} |" for i, p in enumerate(pages) if i != idx]''',
        r'''    rows = [f"| {i + 1} | {head(p)} |" for i, p in enumerate(pages) if i != idx and head(p) != "—"]''',
    ),
    (
        "index: sort parts by first page",
        r'''               "| Part | Pages |\n|---|---|\n" + "\n".join(f"| {k} | {ranges(v)} |" for k, v in sorted(part.items())) + "\n", p, count=1)''',
        r'''               "| Part | Pages |\n|---|---|\n" + "\n".join(
                   f"| {k} | {ranges(v)} |" for k, v in sorted(part.items(), key=lambda kv: min(kv[1]))) + "\n", p, count=1)''',
    ),
    (
        "fix_counts: reconcile counts, versions, change history",
        r'''def fix_counts(t: str, total: int) -> str:
    t = re.sub(r"\b(?:runs to|complete at|extent is) \d+ pages\b", lambda m: re.sub(r"\d+", str(total), m.group(0)), t)
    t = re.sub(r"page count for this edition is \d+", f"page count for this edition is {total}", t)
    return re.sub(r"Page N of \d+", f"Page N of {total}", t)''',
        r'''def fix_counts(t: str, total: int) -> str:
    t = re.sub(r"\b(?:runs to|complete at) \d+ pages\b", lambda m: re.sub(r"\d+", str(total), m.group(0)), t)
    t = re.sub(r"\bextent is \d+\b", f"extent is {total}", t)
    t = re.sub(r"\bextends the document to \d+ pages\b", f"extends the document to {total} pages", t)
    t = re.sub(r"restore the original footer count of \d+(?: plus one)?", f"restore the footer count of {total}", t)
    t = re.sub(r"page count for this edition is \d+", f"page count for this edition is {total}", t)
    t = re.sub(r"\bThirty-one pages\b", f"{total} pages", t)
    t = re.sub(r"\bthis is 2\.0\b", f"this is {VERSION}", t)
    t = re.sub(r"\bVersion 2\.0\b", f"Version {VERSION}", t)
    t = re.sub(r"\bv2\.0\b", f"v{VERSION}", t)
    t = re.sub(r"(\| 2\.0 \| 2026-11-14 \|[^\n]*\n)",
               lambda m: m.group(1) + f"| {VERSION} | 2026-11-14 | Collapsible TOC, 32 plates re-hosted locally, verification blocks, page-8 draft removed |\n", t, count=1)
    return re.sub(r"Page N of \d+", f"Page N of {total}", t)''',
    ),
    (
        "--check: literal markers and front/back links",
        r'''        bad = n or hot or miss or any(c > 1 for c in dup.values()) or tocs < 8''',
        r'''        literal = text.count("{key}")
        toc_region = text.split("## Document Map")[0]
        frontback = ("About this edition" in toc_region) and ("Change history" in toc_region)
        print(f"literal_key={literal} frontback_links={frontback}")
        bad = n or hot or miss or any(c > 1 for c in dup.values()) or tocs < 8 or literal or not frontback''',
    ),
]


def die(m: str) -> "None":
    print("error: " + m, file=sys.stderr)
    raise SystemExit(1)


def write_atomic(path: Path, text: str) -> None:
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".fix-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    a = ap.parse_args()

    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="replace")

    if not TARGET.exists():
        die(f"{TARGET} not found; run from the repository root")

    src = TARGET.read_text(encoding="utf-8")
    applied = skipped = 0
    missing: list[str] = []

    for label, old, new in EDITS:
        n = src.count(old)
        if n == 1:
            src = src.replace(old, new, 1)
            applied += 1
            print(f"  applied  {label}")
        elif n == 0 and new in src:
            skipped += 1
            print(f"  skipped  {label} (already applied)")
        elif n == 0:
            missing.append(label)
            print(f"  MISSING  {label}")
        else:
            missing.append(f"{label} (matched {n}x)")
            print(f"  AMBIG    {label} (matched {n}x)")

    if missing:
        print("\nnothing written; resolve these first:", file=sys.stderr)
        for m in missing:
            print("  - " + m, file=sys.stderr)
        return 1

    if 'VERSION = "2.4"' in src:
        src = src.replace('VERSION = "2.4"', 'VERSION = "2.5"', 1)
        print("  applied  VERSION 2.4 -> 2.5")

    if '<!-- /patch:{key} -->' in src and 'f"\\n\\n</details>\\n<!-- /patch:{key} -->\\n"' not in src:
        print("  WARN     closing tag may still be literal; check block()", file=sys.stderr)

    if not BAK.exists():
        shutil.copy2(TARGET, BAK)
        print(f"  backup   {BAK}")

    write_atomic(TARGET, src)
    print(f"\nwrote {TARGET} ({len(src)} chars): {applied} applied, {skipped} skipped")

    if not a.run:
        print("\nnext:  python tools\\patch_readme.py --check")
        return 0

    print("\n== git checkout README.md")
    if subprocess.run(["git", "checkout", "--", "README.md"]).returncode != 0:
        die("git checkout failed")
    print(f"   README.md {(Path('README.md').stat().st_size)} bytes")

    print("\n== python tools\\patch_readme.py --all")
    if subprocess.run([sys.executable, str(TARGET), "--all"]).returncode != 0:
        die("--all failed; README.bak holds the previous copy")

    print("\n== python tools\\patch_readme.py --check")
    return subprocess.run([sys.executable, str(TARGET), "--check"]).returncode


if __name__ == "__main__":
    raise SystemExit(main())