#!/usr/bin/env python3
"""check_bands.py — audit §119 against TS 45.005 / 36.101 / 38.104.

Handles GSM 900 dual ARFCN variants and NR rows with no ARFCN column.
Exit 1 on any mismatch.
"""
import re
import sys
from pathlib import Path

# band -> list of acceptable (ul, dl, arfcn|None)
REF = {
    "850":  [("824–849", "869–894", "128–251")],
    "900":  [("890–915", "935–960", "1–124"),
             ("880–915", "925–960", "975–1023, 0–124")],
    "1800": [("1710–1785", "1805–1880", "512–885")],
    "1900": [("1850–1910", "1930–1990", "512–810")],
    "1":    [("1920–1980", "2110–2170", "0–599")],
    "3":    [("1710–1785", "1805–1880", "1200–1949")],
    "7":    [("2500–2570", "2620–2690", "2750–3449")],
    "8":    [("880–915", "925–960", "3450–3799")],
    "20":   [("832–862", "791–821", "6150–6449")],
    "28":   [("703–748", "758–803", "9210–9659")],
    "41":   [("2496–2690", "2496–2690 (TDD)", "39650–41589")],
    "n1":   [("1920–1980", "2110–2170", None)],
    "n3":   [("1710–1785", "1805–1880", None)],
    "n28":  [("703–748", "758–803", None)],
    "n41":  [("2496–2690", "TDD", None)],
    "n77":  [("3300–4200", "TDD", None)],
    "n78":  [("3300–3800", "TDD", None)],
    "n79":  [("4400–5000", "TDD", None)],
}
ROW = re.compile(r"^\|\s*([0-9]{2,4}|n\d{1,3})\s*\|(.+)$", re.MULTILINE)


def norm(s: str) -> str:
    return s.replace(" ", "").replace("(MHz)", "").replace("–", "-").strip()


def main() -> int:
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "README.md")
    text = src.read_text()
    m = re.search(r"## 119\. Band and Frequency Reference(.*?)\n## 120\.", text, re.S)
    if not m:
        print("error: §119 not found", file=sys.stderr)
        return 2

    bad = checked = 0
    for band, rest in ROW.findall(m.group(1)):
        cands = REF.get(band)
        if not cands:
            continue
        cells = [c.strip() for c in rest.split("|")][:3]
        if len(cells) < 2:
            continue
        ul, dl = norm(cells[0]), norm(cells[1])
        arfcn = norm(cells[2]) if len(cells) > 2 and band[0].isdigit() else None
        checked += 1
        hit = any(ul == norm(r[0]) and dl == norm(r[1]) and
                  (r[2] is None or arfcn is None or arfcn == norm(r[2]))
                  for r in cands)
        if not hit:
            print(f"MISMATCH band {band}: got {cells[:3]} vs {cands}")
            bad += 1
    print(f"checked {checked} bands, {bad} mismatch(es)")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())