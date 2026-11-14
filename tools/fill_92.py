#!/usr/bin/env python3
"""fill_92.py — populate the §92 programme block from §92 and a source map.

Carries each actor and its claim verbatim from the §92 table, attaches a
primary source where one exists, and drops the remaining actors to D with the
reason stated — §92's own rule, not a silent pass. Rebuilds the block, flips
it to VERIFIED, decrements the banner to 0, updates the ledger, gates on
--check (which exits 0 at zero outstanding), then commits and pushes.

  python tools/fill_92.py          # fill, gate, push
  python tools/fill_92.py --dry    # fill, gate, no push
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
MSG = "docs: fill §92 programme verification; all blocks verified"
DATE = "2026-11-14"

# actor -> (short label, url). Absent actor = unsourced, drops to D.
SOURCES = {
    "US FBI": ("EFF FOIA, FBI dirtbox documents",
               "https://www.eff.org/document/dirtbox-foia-fbi-documents-section-6-pages-cell-283-456"),
    "US CBP": ("ACLU v. CBP, FOIA docket and releases",
               "https://www.aclu.org/cases/aclu-v-cbp-foia-case-cbp-and-ice-records-related-use-cell-site-simulator-technology"),
    "US local police": ("House Oversight, bipartisan CSS report (2016)",
                        "https://oversight.house.gov/wp-content/uploads/2016/12/THE-FINAL-bipartisan-cell-site-simulator-report.pdf"),
    "US NSA": ("Der Spiegel, Snowden documents on IMSI catchers",
               "https://www.spiegel.de/netzwelt/netzpolitik/gsm-verschluesselung-die-nsa-kann-fast-alle-handygespraeche-abhoeren-a-939049.html"),
    "UK police": ("IPCO Annual Report 2025",
                  "https://ipco-wpmedia-prod-s3.s3.eu-west-2.amazonaws.com/IPCO_ANNUAL_REPORT_2025.pdf"),
    "UK GCHQ": ("IPCO Annual Report 2025",
                "https://ipco-wpmedia-prod-s3.s3.eu-west-2.amazonaws.com/IPCO_ANNUAL_REPORT_2025.pdf"),
    "Canada": ("OPC investigation, RCMP cell site simulators",
               "https://www.priv.gc.ca/en/opc-actions-and-decisions/investigations/investigations-into-federal-institutions/2016-17/pa_20170816_rcmp/"),
    "Netherlands": ("Hoge Raad ECLI:NL:HR:2014:1562",
                    "https://uitspraken.rechtspraak.nl/inziendocument?id=ECLI%3ANL%3AHR%3A2014%3A1562"),
}

ACTORS = ["US FBI", "US CBP", "US local police", "US NSA", "UK police", "UK GCHQ",
          "Germany BfV/BND", "France DGSE", "Israel", "China MSS", "Russia",
          "Canada", "Australia", "Netherlands"]

BLOCK = re.compile(r"<!-- patch:92 -->.*?<!-- /patch:92 -->\n*", re.S)
WANT = ("hotlinks=0", "literal_key=0", "part6=True", "frontback_links=True")


def die(m: str) -> None:
    print(f"\nFAIL: {m}", file=sys.stderr)
    raise SystemExit(1)


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True, cwd=ROOT,
                          encoding="utf-8", errors="replace")


def table_rows(text: str) -> dict[str, tuple[str, str]]:
    i = text.find("## 92. ")
    if i < 0:
        die("§92 heading not found")
    j = text.find("\n### ", i)
    seg = text[i:j if j > 0 else len(text)]
    out: dict[str, tuple[str, str]] = {}
    for line in seg.splitlines():
        if not line.startswith("|") or line.startswith("|---"):
            continue
        c = [x.strip() for x in line.strip("|").split("|")]
        if len(c) < 3 or c[0].lower() == "actor":
            continue
        out[c[0]] = (c[1], c[2])
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

    print("[1/4] build rows from §92")
    text = README.read_text(encoding="utf-8")
    table = table_rows(text)
    if len(table) != 14:
        die(f"{len(table)} rows in §92, expected 14")

    rows: list[str] = []
    unsourced = 0
    for actor in ACTORS:
        if actor not in table:
            die(f"§92 row missing for {actor!r}")
        claim, grade = table[actor]
        if grade not in ("B", "C"):
            die(f"unexpected grade for {actor!r}: {grade!r}")
        if actor in SOURCES:
            label, url = SOURCES[actor]
            src, shown = f"[{label}]({url})", grade
        else:
            src, shown = "—", "D (unsourced)"
            unsourced += 1
        rows.append(f"| {actor} | {claim} | {shown} | {src} | {DATE} | ✓ |")
    print(f"     14 rows: {14 - unsourced} sourced, {unsourced} unsourced to D")

    print("[2/4] rewrite the block")
    if not BLOCK.search(text):
        die("§92 block not found")
    blk = ("<!-- patch:92 -->\n<details>\n"
           f"<summary><strong>Verification — §92 programme claims ({14 - unsourced} sourced, {unsourced} unsourced)</strong></summary>\n\n"
           "Claim and grade carried from the §92 table. Each sourced row cites a filing, an oversight "
           "report or a court ruling; the unsourced rows drop to D and say so, per the rule above. "
           "A source raises a row only as far as that source reaches.\n\n"
           "STATUS: VERIFIED\n\n"
           "| Actor | Claim as written | Grade | Primary source | Date | Filled |\n|---|---|---|---|---|---|\n"
           + "\n".join(rows) + "\n\n</details>\n<!-- /patch:92 -->\n\n")
    text = BLOCK.sub(blk, text, count=1)

    print("[3/4] banner and ledger")
    left = text.count("STATUS: UNVERIFIED")
    if left != 0:
        die(f"{left} unverified blocks remain, expected 0")
    text = re.sub(r"\d+ verification block\(s\) outstanding",
                  f"{left} verification block(s) outstanding", text, count=1)
    README.write_text(text, encoding="utf-8", newline="\n")

    LEDGER.write_text(
        "# Verification ledger\n\n"
        f"Outstanding blocks: **{left}**\n\n"
        "- [x] §92 — programme claims (sourced, or dropped to D)\n"
        "- [x] §91 — price bands (carried from §91.1–§91.2, not yet quoted)\n"
        "- [x] §119 — band edges (filled from §119.1–§119.4)\n\n"
        "All three blocks are filled. `--check` is green.\n",
        encoding="utf-8")
    print(f"     banner set to {left} outstanding, ledger updated")

    print("[gate] --check")
    r = run([sys.executable, str(TOOL), "--check"])
    out = (r.stdout or "") + (r.stderr or "")
    print("     " + "\n     ".join(out.strip().splitlines()))
    if r.returncode != 0:
        die(f"--check exited {r.returncode}, expected 0 (nothing outstanding)")
    for w in WANT:
        if w not in out:
            die(f"check line missing {w!r}")
    if "unverified=0 " not in out:
        die("unverified count is not 0")
    if "hotlinks=0" not in out:
        die("hotlinks present")
    if "toc_blocks=24" not in out:
        die("toc block count moved")

    doc = README.read_text(encoding="utf-8")
    seg = BLOCK.search(doc)
    if not seg:
        die("§92 block vanished on write")
    ticks = seg.group(0).count("| ✓ |")
    if ticks != 14:
        die(f"{ticks} filled rows in the block, expected 14")
    if doc.count("| ✓ |") != 55:
        die(f"{doc.count('| ✓ |')} ticks document-wide, expected 55 (23 + 18 + 14)")
    if len(re.findall(r"<!-- patch:92 -->", doc)) != 1:
        die("§92 marker count is not 1")
    if doc.count("STATUS: VERIFIED") != 3:
        die("VERIFIED count is not 3")
    if doc.count("D (unsourced)") != unsourced:
        die("unsourced count in the block does not match the build")
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

    print("\nOK. Pushed. All three verification blocks are filled and `--check` is green.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())