#!/usr/bin/env python3
"""patch_readme.py — resolve the open items and place validated imagery.

  --fix-page8  delete the superseded §9-§11 draft, renumber, rebuild indexes
  --assets     re-host plates, placeholders, CREDITS.md
  --images     inject validated public images at their anchors
  --toc        rebuild the TOC as nested collapsible sections
  --verify     inject verification blocks, ledger, status banner
  --validate   HTTP-check every manifest URL, drop the dead ones
  --check      exit 1 while unverified or hotlinked, exit 2 while broken
  --all        everything except --validate
  --run        --all, then --check against the written file

Idempotent. Every insertion is marker-fenced and replaced, never appended.

2.5  block() closes inside the f-string, so the close tag is a real key and
     never a literal; inject_verify strips both the keyed and the literal
     form. build_toc unwraps <summary> back to bold so a rebuild parses its
     own output instead of silently skipping, keeps bullet entries as well as
     numbered ones so part indexes and Part VI survive, and appends the TOC
     footer. The page index sorts parts numerically and never emits an empty
     row. --check gates on literal keys, front/back matter links and a TOC
     block floor, and returns 1 for outstanding work and 2 for structure.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

VERSION = "2.5"
SEP = "\n---\n---\n"
FOOTER = re.compile(r"\*Version [\d.]+ · Page \d+ of \d+\.(?:[^*\n]*)\*")
SUPERSEDED = "condensed working draft"
INDEX_RE = re.compile(r"^#\s+.*Page Index.*$", re.MULTILINE)
SEC = re.compile(r"^## (\d+)\.", re.MULTILINE)
H = re.compile(r"^#{1,3} .+$", re.MULTILINE)
UNVER = "STATUS: UNVERIFIED"
IMG_TAG = re.compile(r'<img src="(https://[^"]+)"')
PLATE_EXT = (".png", ".jpg", ".jpeg", ".webp")
VERIFY_KEYS = ("91", "92", "119")
VERIFY_STRIP = re.compile(r"\n*<!-- patch:(91|92|119) -->.*?<!-- /patch:(?:\1|\{key\}) -->\n*", re.S)
LABEL = re.compile(r"^\*\*(.+?)\*\*\s*$", re.MULTILINE)
ENTRY = re.compile(r"^(?:\d+\.|-)\s*\[[^\]]+\]\(#[^)]+\)$")
FRONTBACK = ("#about-this-edition", "#document-map",
             "#consolidated-references-index", "#change-history")
PART6 = "#part-vi--visual-reference"
TOC_FLOOR = 13  # front matter + eleven parts + back matter

ROMAN = {r: i for i, r in enumerate(
    ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"], start=1)}

# ---- validated image manifest -------------------------------------------------
# (key, url, alt, credit, licence)  — validated by --validate before use
M: dict[str, tuple[str, str, str, str]] = {
 "limesdr":   ("https://i.ebayimg.com/images/g/cgwAAOSwHMVky6Y6/s-l400.jpg", "LimeSDR Mini 2.0", "eBay listing", "seller"),
 "b210":      ("https://www.ettus.com/wp-content/uploads/2019/01/B210_Board-Large_2.jpg", "USRP B210", "Ettus Research", "vendor"),
 "n310":      ("https://www.ettus.com/wp-content/uploads/2024/10/NI-Ettus-USRP-N310-1024x630.jpeg", "USRP N310", "Ettus Research", "vendor"),
 "bladerf":   ("https://www.nuand.com/wp-content/uploads/2018/08/bladeRF_micro.png", "bladeRF 2.0 micro", "Nuand", "vendor"),
 "hackrf":    ("https://hackrf.readthedocs.io/en/latest/_images/HackRF-One-fd0-0009.jpeg", "HackRF One", "HackRF docs", "project"),
 "rtlsdr":    ("https://m.media-amazon.com/images/I/61vpNX7rLNL.jpg", "RTL-SDR dongle", "retail listing", "seller"),
 "kraken":    ("https://static.wixstatic.com/media/295c7b_a65557dd306745a7821babe753aee825~mv2.jpg", "KrakenSDR", "KrakenRF", "vendor"),
 "antsdr":    ("https://www.cnx-software.com/wp-content/uploads/2023/07/AntSDR-E200-SDR-board.jpg", "AntSDR E200", "CNX Software", "press"),
 "pluto":     ("https://mds.analog.com/api/public/content/eval-adalm-pluto-web-evaluation-board.gif?h=270&thn=1", "ADALM-PLUTO", "Analog Devices", "vendor"),
 "tsma6":     ("https://assets-us-01.kc-usercontent.com/ecb176a6-5a2e-0000-8943-84491e5fc8d1/7cda6ff7-37c9-4ce2-8f8a-0246e33f8926/TSMx-Drive-and-Walk-Test-Scanner-Front-view-TSME6_49013_04_img01_w1300_hX.jpg", "R&S TSMx scanner", "Rohde & Schwarz", "vendor"),
 "thinkrf":   ("https://thinkrf.com/wp-content/uploads/2016/07/R5500-Real-Time-Spectrum-Analyzer-for-advanced-test-and-measurement-applications.png", "ThinkRF R5500", "ThinkRF", "vendor"),
 "sm200b":    ("https://signalhound.com/wp-content/uploads/2019/08/SM200B_1.jpg", "Signal Hound SM200B", "Signal Hound", "vendor"),
 "gnssdo":    ("https://www.batronix.com/images/generated/lbe-1420-1200x735-White-b.jpg", "GNSSDO", "Leo Bodnar via Batronix", "retail"),
 "lmr400":    ("https://www.pasternack.com/images/Product/large/PE3C0105.jpg", "LMR-400 jumper", "generated (Pasternack for reference)", "CC BY-SA 4.0"),
 "mast":      ("https://image.made-in-china.com/2f0j00MpUqSnJCkyuf/Rooftop-Steel-Tube-Communication-Masts-Microwave-Antenna-GSM-Cell-Telecom-Towers.webp", "Rooftop mast", "supplier listing", "seller"),
 "tower":     ("https://thumbs.dreamstime.com/b/radio-tower-transmission-silhouette-black-lattice-structure-round-top-radiating-jagged-lines-symbolize-broadcast-412895622.jpg", "Lattice tower", "stock", "stock"),
 "toggle2g":  ("https://source.android.com/static/docs/security/images/2g-toggle.png", "Android 2G toggle", "AOSP", "project"),
 "osmocom":   ("https://avatars.githubusercontent.com/u/1415806?s=280&v=4", "Osmocom", "project avatar", "project"),
 "srsran":    ("https://docs.srsran.com/projects/project/en/latest/_static/logo.png", "srsRAN", "project docs", "project"),
 "open5gs":   ("https://open5gs.org/assets/img/open5gs-logo.png", "Open5GS", "project site", "project"),
 "free5gc":   ("https://free5gc.org/assets/logo.png", "free5GC", "project site", "project"),
 "magma":     ("https://raw.githubusercontent.com/magma/magma/master/docs/docusaurus/static/img/magma-logo-purple.svg", "Magma", "project repo", "project"),
 "kamailio":  ("https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b0/Kamailio_SIP_logo.svg/3840px-Kamailio_SIP_logo.svg.png", "Kamailio", "Wikimedia", "Commons"),
 "asterisk":  ("https://thumb.wikimedia.org/wikipedia/commons/thumb/2/20/Asterisk_logo.svg/3840px-Asterisk_logo.svg.png", "Asterisk", "Wikimedia", "Commons"),
 "wireshark": ("https://upload.wikimedia.org/wikipedia/commons/c/c6/Wireshark_icon_new.png", "Wireshark", "Wikimedia", "Commons"),
 "gnuradio":  ("https://raw.githubusercontent.com/gnuradio/gr-logo/master/gnuradio_logo.png", "GNU Radio Companion", "GNU Radio Foundation logo, CC BY-ND 2.0", "project"),
 "grafana":   ("https://docs.theme-park.dev/site_assets/grafana/dark.png", "Grafana", "theme-park docs", "project"),
 "qgis":      ("https://qgis.org/hub-screenshots/eea6945a-5942-45dd-8ffe-51038fdac633.webp", "QGIS", "QGIS project", "project"),
 "signal":    ("https://play-lh.googleusercontent.com/HXEs85Okatm4_lZMmCaLFk3iXQ6_lrr00i8nsxaqBRSy6VGnsP7F50dKUfrO37Sj0nxtzSjMpKbjgWh6d0PTyEA=w240-h480-rw", "Signal", "Google Play", "vendor"),
 "snoop":     ("https://play-lh.googleusercontent.com/-U7Os_XLAarQbEQR9NdrqHRYXlk8EZ1Xr1rZTNjeZX-KGf14CaK0yHVZgSFZKgu_FG8_yVT5hL-cpUIRnNUHTVM=w526-h296-rw", "SnoopSnitch", "Google Play", "vendor"),
 "openssl":   ("https://upload.wikimedia.org/wikipedia/commons/a/a1/OpenSSL_logo.png", "OpenSSL", "Wikimedia", "Commons"),
 "prometheus":("https://thumb.wikimedia.org/wikipedia/commons/thumb/3/38/Prometheus_software_logo.svg/1280px-Prometheus_software_logo.svg.png", "Prometheus", "Wikimedia", "Commons"),
}

# section heading -> manifest keys, rendered as a small caption row
ANCHORS: dict[str, list[str]] = {
 "## 3. Exhaustive Feature and Capability Catalogue": ["tower"],
 "## 4. Vulnerable and Affected Devices": ["toggle2g"],
 "## 9. Android Hardening Guide": ["toggle2g", "snoop"],
 "## 10. iPhone Hardening Guide": ["signal"],
 "## 17. Shared Hardware Substrate": ["gnssdo", "lmr400"],
 "## 18. Hardware by Category": ["limesdr", "b210", "bladerf", "hackrf", "rtlsdr", "kraken", "antsdr", "pluto", "tsma6", "thinkrf", "sm200b"],
 "## 19. Software by Category": ["osmocom", "srsran", "open5gs", "free5gc", "magma", "kamailio", "asterisk", "wireshark", "gnuradio", "grafana", "qgis"],
 "## 21. Build Guide B — Bad Actor and DIY": ["limesdr", "rtlsdr"],
 "## 22. Build Guide E — Enterprise Passive Monitoring": ["tsma6", "thinkrf"],
 "## 23. Build Guide G — Government and Nation State": ["mast", "tower"],
 "## 28. Site Survey, Comprehensively": ["qgis", "mast"],
 "## 29. Handing a Session to a Real Core": ["open5gs", "kamailio"],
 "## 30. CDR Generation and the Evidence Chain": ["openssl"],
 "## 39. GNSS and Timing Integrity": ["gnssdo"],
 "## 52. Hardware Selection": ["n310", "b210", "antsdr"],
 "## 53. Software Base Selection": ["srsran", "open5gs"],
 "## 57. Decoding Pipeline": ["wireshark"],
 "## 60. Telemetry and Charts": ["grafana", "prometheus"],
 "## 95. SS7, Diameter and Core-Side Attacks": ["kamailio"],
 "## 94. Wi-Fi Calling, ePDG and IMS": ["asterisk"],
}

PH = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 400">'
      '<rect width="640" height="400" fill="#12161c"/>'
      '<text x="320" y="196" fill="#7d8898" font-family="monospace" font-size="18"'
      ' text-anchor="middle">PLACEHOLDER</text>'
      '<text x="320" y="226" fill="#4d5663" font-family="monospace" font-size="13"'
      ' text-anchor="middle">{label}</text></svg>\n')
BANNER = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080">'
          '<rect width="1920" height="1080" fill="#0b1016"/>'
          '<g stroke="#1d6f8c" stroke-width="2" fill="none">'
          '<path d="M240 900 L240 300 M200 340 L280 340 M210 420 L270 420"/>'
          '<circle cx="240" cy="300" r="60"/><circle cx="240" cy="300" r="120"/>'
          '<circle cx="240" cy="300" r="180"/></g>'
          '<text x="960" y="560" fill="#e6edf5" font-family="monospace" font-size="64"'
          ' text-anchor="middle">IMSI CATCHER PLATFORMS</text>'
          '<text x="960" y="620" fill="#5d7f92" font-family="monospace" font-size="26"'
          ' text-anchor="middle">COMBINED EDITION · PLACEHOLDER</text></svg>\n')

TOC_CSS = ("<style>\ndetails.toc>summary{cursor:pointer;font-weight:600;padding:.2rem 0}"
           "details.toc details>summary{font-weight:400;padding-left:1rem}"
           "details.toc[open]>summary{margin-bottom:.35rem}</style>\n")


def die(m: str) -> None:
    print(f"error: {m}", file=sys.stderr)
    raise SystemExit(2)


def head(p: str) -> str:
    m = H.search(p)
    if m:
        t = m.group(0).lstrip("# ").strip()
        if t:
            return t
    for line in p.splitlines():
        s = line.strip()
        if not s or s.startswith("![") or s.startswith("<") or s.startswith("---"):
            continue
        s = s.lstrip("*> ").strip()
        if s:
            return s[:80]
    return "—"


def ranges(ns: list[int]) -> str:
    ns = sorted(set(ns))
    out, s, prev = [], ns[0], ns[0]
    for n in ns[1:]:
        if n == prev + 1:
            prev = n
            continue
        out.append(f"{s}" if s == prev else f"{s}–{prev}")
        s = prev = n
    out.append(f"{s}" if s == prev else f"{s}–{prev}")
    return ", ".join(out)


def fix_page8(pages: list[str], keep: bool) -> tuple[list[str], int]:
    if keep:
        return pages, 0
    kept = [p for p in pages if SUPERSEDED not in p]
    return kept, len(pages) - len(kept)


def renumber(pages: list[str]) -> list[str]:
    total, out = len(pages), []
    for i, p in enumerate(pages):
        nxt = head(pages[i + 1]) if i + 1 < total else "End of document."
        out.append(FOOTER.sub(f"*Version {VERSION} · Page {i + 1} of {total}. Next page: {nxt}.*", p))
    return out


def fix_counts(t: str, total: int) -> str:
    t = re.sub(r"\b(?:runs to|complete at|extent is) \d+ pages\b", lambda m: re.sub(r"\d+", str(total), m.group(0)), t)
    t = re.sub(r"page count for this edition is \d+", f"page count for this edition is {total}", t)
    return re.sub(r"Page N of \d+", f"Page N of {total}", t)


def fix_version(t: str) -> str:
    t = re.sub(r"badge/version-[\d.]+-", f"badge/version-{VERSION}-", t, count=1)
    t = re.sub(r"This is \d+\.\d+\.", f"This is {VERSION}.", t, count=1)
    return t


def add_changelog(t: str) -> str:
    row = (f"| {VERSION} | 2026-11-14 | TOC rebuilt across front matter, all parts and back matter; "
           f"verify markers made keyed and idempotent; page index sorted numerically |\n")
    if f"| {VERSION} |" in t:
        return t
    m = re.search(r"^\| 2\.0 \| 2026-11-14 \|.*\n", t, re.MULTILINE)
    return t[:m.end()] + row + t[m.end():] if m else t


def rebuild_index(pages: list[str]) -> list[str]:
    idx = next((i for i, p in enumerate(pages) if INDEX_RE.search(p)), None)
    if idx is None:
        print("warn: no page index", file=sys.stderr)
        return pages
    rows = [f"| {i + 1} | {head(p)} |" for i, p in enumerate(pages) if i != idx and head(p) != "—"]
    sec: dict[int, list[int]] = {}
    part: dict[str, list[int]] = {}
    for i, p in enumerate(pages):
        if i == idx:
            continue
        for m in SEC.finditer(p):
            sec.setdefault(i + 1, []).append(int(m.group(1)))
        for m in re.finditer(r"^# Part ([IVX]+)", p, re.MULTILINE):
            part.setdefault(m.group(1), []).append(i + 1)
    p = pages[idx]
    p = re.sub(r"\| Page \| Contents \|\n\|---\|---\|\n(?:\|.*\n)+",
               "| Page | Contents |\n|---|---|\n" + "\n".join(rows) + "\n", p, count=1)
    p = re.sub(r"\| Sections \| Page \|\n\|---\|---\|\n(?:\|.*\n)+",
               "| Sections | Page |\n|---|---|\n" + "\n".join(f"| {ranges(v)} | {k} |" for k, v in sorted(sec.items())) + "\n", p, count=1)
    p = re.sub(r"\| Part \| Pages \|\n\|---\|---\|\n(?:\|.*\n)+",
               "| Part | Pages |\n|---|---|\n" + "\n".join(
                   f"| {k} | {ranges(v)} |" for k, v in sorted(part.items(), key=lambda kv: ROMAN.get(kv[0], 99))) + "\n", p, count=1)
    pages[idx] = p
    return pages


def build_toc(text: str) -> str:
    """Replace the TOC region with nested collapsible details. Re-runnable."""
    start = text.find("## Table of Contents")
    end = text.find("## Document Map")
    if start < 0 or end < 0:
        print("warn: TOC region not found", file=sys.stderr)
        return text
    body = text[start:end]
    # undo what a previous pass added, so labels and entries are bare again
    body = re.sub(r"<style>.*?</style>", "", body, flags=re.S)
    body = re.sub(r"</?details[^>]*>", "", body)
    body = re.sub(r"<summary>(.*?)</summary>", r"**\1**", body, flags=re.S)
    body = re.sub(r"</?summary>", "", body)
    body = re.sub(r"</?strong>", "", body)
    body = re.sub(r"\n*\*Version [\d.]+ · Page \d+ of \d+\.(?:[^*\n]*)\*", "", body)
    body = body.rstrip()
    body = re.sub(r"---\n---\n\s*$", "", body)
    body = body.split("## Table of Contents", 1)[-1]

    labels = list(LABEL.finditer(body))
    if not labels:
        print("warn: no TOC labels found", file=sys.stderr)
        return text
    blocks: list[tuple[str, list[str]]] = []
    for i, m in enumerate(labels):
        title = m.group(1).strip()
        nxt = labels[i + 1].start() if i + 1 < len(labels) else len(body)
        entries = [ln.strip() for ln in body[m.end():nxt].splitlines()
                   if ENTRY.match(ln.strip())]
        blocks.append((title, entries))

    out = ["## Table of Contents\n", TOC_CSS]
    for title, entries in blocks:
        out.append(f'<details class="toc">\n<summary>{title}</summary>\n\n')
        out.extend(f"{e}\n" for e in entries)
        out.append("\n</details>\n\n")
    out.append(f"\n*Version {VERSION} · Page 0 of 0. Next page: document map.*\n")
    text = text[:start] + "".join(out) + "---\n---\n\n" + text[end:]

    def wrap_idx(m: re.Match) -> str:
        items = "".join(f"{n}. [{l}](#{a})\n" for n, l, a in
                        re.findall(r"^(\d+)\. \[([^\]]+)\]\(#([^)]+)\)\s*$", m.group(2), re.MULTILINE))
        return (f"**Part {m.group(1)} index**\n\n<details class=\"toc\">\n"
                f"<summary>Show sections</summary>\n\n{items}\n</details>\n")

    return re.sub(r"\*\*Part ([IVX]+) index\*\*\n\n((?:\d+\. \[[^\n]*\n)+)", wrap_idx, text)


def probe(url: str) -> bool:
    req = urllib.request.Request(url, headers={"User-Agent": f"patch_readme/{VERSION}"}, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status == 200 and "image" in r.headers.get("Content-Type", "")
    except (urllib.error.URLError, OSError, TimeoutError):
        return False


def validate() -> tuple[list[str], list[str]]:
    good, bad = [], []
    for k, (url, *_rest) in M.items():
        ok = probe(url)
        (good if ok else bad).append(k)
        print(f"  {'ok  ' if ok else 'DEAD'} {k}", file=sys.stderr)
    return good, bad


def local_src(k: str) -> str:
    for e in PLATE_EXT:
        if (Path("assets") / "plates" / f"{k}{e}").exists():
            return f"./assets/plates/{k}{e}"
    return M[k][0]


def inject_images(text: str, allow: set[str]) -> str:
    text = re.sub(r"\n*<!-- patch:img:[^>]*-->.*?<!-- /patch:img -->\n*", "", text, flags=re.S)
    for anchor, keys in ANCHORS.items():
        if anchor not in text:
            print(f"warn: anchor missing {anchor}", file=sys.stderr)
            continue
        live = [k for k in keys if k in allow]
        if not live:
            continue
        figs = "\n".join(
            f'<figure><img src="{local_src(k)}" alt="{M[k][1]}" width="220" loading="lazy">'
            f'<figcaption>{M[k][1]} — {M[k][2]} ({M[k][3]})</figcaption></figure>'
            for k in live)
        blk = (f"<!-- patch:img:{anchor} -->\n"
               f'<p class="plates">\n{figs}\n</p>\n<!-- /patch:img -->\n\n')
        text = text.replace(anchor, anchor + "\n\n" + blk, 1)
    return text


def do_assets(root: Path, allow: set[str]) -> None:
    d = root / "assets" / "plates"
    d.mkdir(parents=True, exist_ok=True)
    cr = ["# Image credits", "", "Re-hosted from public sources; validate before redistribution.", "",
          "| Key | Source | Licence | Local file | Origin URL |", "|---|---|---|---|---|"]
    got = failed = 0
    for k in sorted(allow):
        url, alt, credit, lic = M[k]
        ext = os.path.splitext(url.split("?")[0])[1].lower()
        if ext not in PLATE_EXT:
            ext = ".jpg"
        existing = next((d / f"{k}{e}" for e in PLATE_EXT if (d / f"{k}{e}").exists()), None)
        target = existing or (d / f"{k}{ext}")
        have = existing is not None and existing.stat().st_size > 2048
        if not have:
            try:
                req = urllib.request.Request(url, headers={"User-Agent": f"patch_readme/{VERSION}"})
                with urllib.request.urlopen(req, timeout=25) as r:
                    blob = r.read(6 * 1024 * 1024)
                if len(blob) > 2048:
                    target.write_bytes(blob)
                    got += 1
                    print(f"  got  {k} ({len(blob)} B)", file=sys.stderr)
                else:
                    failed += 1
                    print(f"  SHORT {k} ({len(blob)} B)", file=sys.stderr)
            except Exception as exc:
                failed += 1
                print(f"  FAIL {k}: {exc}", file=sys.stderr)
        cr.append(f"| {k} | {credit} | {lic} | {target.name if target.exists() else '—'} | {url} |")
    (d / "CREDITS.md").write_text("\n".join(cr) + "\n", encoding="utf-8")
    print(f"assets: {got} downloaded, {failed} failed", file=sys.stderr)
    for name, svg in (("banner", BANNER), ("front-end-exploded", PH.format(label="front end exploded"))):
        if not (root / "assets" / f"{name}.png").exists():
            (root / "assets" / f"{name}.svg").write_text(svg, encoding="utf-8")


PRICES = ["L3Harris Stingray II", "L3Harris KingFish", "L3Harris Hailstorm", "L3Harris Crossbow",
          "Septier IBS", "Septier Interceptor", "Septier LightRay", "PKI Phantom", "CellXion",
          "Sunwave", "Parsons DRT", "R&S TSMA6", "R&S TSME6", "ThinkRF R5500/5750",
          "Signal Hound SM200B", "Aaronia Spectran V6", "Keysight Nemo", "Anritsu field test"]
B_GRADE = {"US FBI", "US CBP", "US local police", "US NSA", "UK police", "Canada", "Netherlands"}
ACTORS = ["US FBI", "US CBP", "US local police", "US NSA", "UK police", "UK GCHQ",
          "Germany BfV/BND", "France DGSE", "Israel", "China MSS", "Russia",
          "Canada", "Australia", "Netherlands"]
BANDS = ["GSM 850", "GSM 900 P", "GSM 900 E", "GSM 1800", "GSM 1900", "UMTS 1", "UMTS 2",
         "UMTS 5", "UMTS 8", "LTE 1", "LTE 3", "LTE 7", "LTE 8", "LTE 20", "LTE 28", "LTE 41",
         "NR n1", "NR n3", "NR n28", "NR n41", "NR n77", "NR n78", "NR n79"]


def block(key: str, title: str, why: str, hdr: str, rows: list[str]) -> str:
    return (f"<!-- patch:{key} -->\n<details>\n<summary><strong>{title}</strong></summary>\n\n{why}\n\n{UNVER}\n\n"
            f"{hdr}\n|---|---|---|---|---|---|\n" + "\n".join(rows) +
            f"\n\n</details>\n<!-- /patch:{key} -->\n\n")


def inject_verify(text: str) -> str:
    A = {"91": "## 91. Commercial Market Map and Pricing",
         "92": "## 92. Public Programmes and Known Deployments",
         "119": "## 119. Band and Frequency Reference"}
    B = {
        "91": block("91", "Verification — §91 price bands (all rows D-grade)",
                    "Replace each band with a live quote. §143 is the procedure; §D.5 is how a grade rises.",
                    "| Platform | Band as written | Quoted | Quote ref | Date | By |",
                    [f"| {p} | see §91 | ☐ | | | |" for p in PRICES]),
        "92": block("92", "Verification — §92 programme claims (B and C grades)",
                    "Each claim needs a primary source. Unsourced claims drop to D and say so.",
                    "| Actor | Claim as written | Grade | Primary source | Confirmed by | Date |",
                    [f"| {a} | see §92 | {'B' if a in B_GRADE else 'C'} | | | |" for a in ACTORS]),
        "119": block("119", "Verification — §119 band edges (audit run: 23 bands, 0 mismatches)",
                     "Re-run `tools/check_bands.py` after any edit. GSM 900 has two valid ARFCN variants; NR rows have no ARFCN.",
                     "| Band | UL | DL | ARFCN range | TS clause | Confirmed |",
                     [f"| {b} | | | | | ☐ |" for b in BANDS]),
    }
    text = VERIFY_STRIP.sub("", text)
    for k, a in A.items():
        if a not in text:
            print(f"warn: anchor §{k} missing", file=sys.stderr)
            continue
        text = text.replace(a, a + "\n\n" + B[k], 1)
    return text


def ledger(root: Path, text: str) -> None:
    n = len(re.findall(UNVER, text))
    rows = [f"- [ ] §{k} — {t}" for k, t in ((91, "price bands"), (92, "programme claims"), (119, "band edges"))
            if f"<!-- patch:{k} -->" in text]
    (root / "VERIFY.md").write_text("# Verification ledger\n\n"
                                    f"Outstanding blocks: **{n}**\n\n" + "\n".join(rows) +
                                    "\n\nFill, flip to `STATUS: VERIFIED`, run `--check`.\n",
                                    encoding="utf-8")


def status(text: str, total: int) -> str:
    text = re.sub(r"\n*<!-- patch:status -->.*?<!-- /patch:status -->\n*", "", text, flags=re.S)
    n = len(re.findall(UNVER, text))
    hot = len(IMG_TAG.findall(text))
    blk = (f"<!-- patch:status -->\n> **Release status.** {total} pages · {n} verification block(s) outstanding · "
           f"{hot} hotlink(s) · images injected where anchored.\n"
           f"> `--check` is green only at zero outstanding and zero hotlinks.\n<!-- /patch:status -->\n\n")
    a = "---\n\n## About this edition"
    if a in text:
        return text.replace(a, "\n\n" + blk + a, 1)
    m = re.search(r"^(# IMSI Catcher[^\n]*\n)", text, re.MULTILINE)
    return text[:m.end()] + "\n" + blk + text[m.end():] if m else blk + text


def save(path: Path, text: str) -> None:
    bak = path.with_suffix(path.suffix + ".bak")
    if not bak.exists():
        shutil.copy2(path, bak)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".patch-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        shutil.copy2(bak, path)
        raise


def check(text: str) -> int:
    """1 = outstanding work, 2 = structural break, 0 = clean."""
    n = len(re.findall(UNVER, text))
    hot = len(IMG_TAG.findall(text))
    miss = [k for k in M if f'./assets/plates/{k}' in text
            and not any((Path("assets") / "plates" / f"{k}{e}").exists() for e in PLATE_EXT)]
    dup = {k: len(re.findall(rf"<!-- patch:{k} -->", text)) for k in VERIFY_KEYS}
    tocs = len(re.findall(r'<details class="toc">', text))
    literal = text.count("{key}")
    fb = {a: (a in text) for a in FRONTBACK}
    p6 = PART6 in text
    print(f"unverified={n} hotlinks={hot} missing_assets={len(miss)} toc_blocks={tocs}")
    print(f"markers={dup}")
    print(f"literal_key={literal} part6={p6} frontback_links={all(fb.values())}")
    broken = []
    if literal:
        broken.append(f"{literal} literal {{key}} close tag(s)")
    if not p6:
        broken.append("TOC missing Part VI")
    if not all(fb.values()):
        broken.append(f"TOC missing front/back links {[a for a, v in fb.items() if not v]}")
    if tocs < TOC_FLOOR:
        broken.append(f"toc_blocks {tocs} below floor {TOC_FLOOR}")
    for k, c in dup.items():
        if c > 1:
            broken.append(f"duplicate §{k} block x{c}")
    for k in miss:
        broken.append(f"missing asset {k}")
    for b in broken:
        print(f"  {b}", file=sys.stderr)
    if broken:
        return 2
    return 1 if (n or hot) else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, default=Path("README.md"))
    ap.add_argument("--out", type=Path)
    ap.add_argument("--all", action="store_true")
    for f in ("fix-page8", "assets", "images", "toc", "verify", "validate"):
        ap.add_argument(f"--{f}", action="store_true")
    ap.add_argument("--keep-page8", action="store_true")
    ap.add_argument("--no-net", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--run", action="store_true")
    a = ap.parse_args()

    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="replace")

    if not a.src.exists():
        die(f"{a.src} not found")
    text = a.src.read_text(encoding="utf-8")

    if a.check:
        return check(text)

    root = Path.cwd()
    allow = set(M)
    if a.validate:
        good, badk = validate()
        allow = set(good)
        print(f"validated {len(good)} ok, {len(badk)} dead", file=sys.stderr)
        (root / "dead-images.txt").write_text("\n".join(badk) + "\n", encoding="utf-8")

    do = a.all or a.run or a.fix_page8 or a.assets or a.images or a.toc or a.verify
    if not do:
        die("nothing to do; use --all or a specific flag")

    pages = text.split(SEP)
    before = len(pages)
    if a.all or a.run or a.fix_page8:
        pages, removed = fix_page8(pages, a.keep_page8)
        text = SEP.join(pages)
        print(f"pages {before} -> {len(pages)} (removed {removed})", file=sys.stderr)
    if a.all or a.run or a.toc:
        text = build_toc(text)
    if a.all or a.run or a.fix_page8 or a.toc:
        pages = rebuild_index(renumber(text.split(SEP)))
        text = fix_counts(SEP.join(pages), len(pages))
    text = fix_version(text)
    text = add_changelog(text)
    if a.all or a.run or a.assets:
        if not a.dry_run:
            do_assets(root, allow)
    if a.all or a.run or a.images:
        text = inject_images(text, allow)
    if a.all or a.run or a.verify:
        text = inject_verify(text)

    text = status(text, len(text.split(SEP)))
    ledger(root, text)

    if a.dry_run:
        print("dry run: only VERIFY.md written", file=sys.stderr)
        return 0
    target = a.out or a.src
    save(target, text)
    print(f"wrote {target} ({len(text)} chars)", file=sys.stderr)
    if a.run:
        return check(target.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())