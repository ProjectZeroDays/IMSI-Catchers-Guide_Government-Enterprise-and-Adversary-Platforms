#!/usr/bin/env python3
"""patch_readme.py — resolve the open items and place validated imagery.

  --fix-page8  delete the superseded §9-§11 draft, renumber, rebuild indexes
  --assets     re-host plates, placeholders, CREDITS.md
  --images     inject validated public images at their anchors
  --toc        rebuild the TOC as nested collapsible sections
  --verify     inject verification blocks, ledger, status banner
  --validate   HTTP-check every manifest URL, drop the dead ones
  --check      exit 1 while unverified or hotlinked
  --all        everything except --validate

Idempotent. Every insertion is marker-fenced and replaced, never appended.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path

VERSION = "2.2"
SEP = "\n---\n---\n"
FOOTER = re.compile(r"\*Version [\d.]+ · Page \d+ of \d+\.(?:[^*\n]*)\*")
SUPERSEDED = "condensed working draft"
INDEX_H = "# Appendix — Page Index"
SEC = re.compile(r"^## (\d+)\.", re.MULTILINE)
H = re.compile(r"^#{1,3} .+$", re.MULTILINE)
UNVER = "STATUS: UNVERIFIED"

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
 "lmr400":    ("https://www.pasternack.com/images/Product/large/PE3C0105.jpg", "LMR-400 cable", "Pasternack", "vendor"),
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
 "gnuradio":  ("https://wiki.gnuradio.org/images/thumb/5/58/NewGRCFlowgraph.png/500px-NewGRCFlowgraph.png", "GNU Radio Companion", "GNU Radio wiki", "project"),
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
    return m.group(0).lstrip("# ").strip() if m else "—"


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


def slug(t: str) -> str:
    t = t.lower().replace("—", "").replace("–", "")
    return re.sub(r"[^a-z0-9 ]", "", t).strip().replace(" ", "-")


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


def rebuild_index(pages: list[str]) -> list[str]:
    idx = next((i for i, p in enumerate(pages) if p.startswith(INDEX_H)), None)
    if idx is None:
        print("warn: no page index", file=sys.stderr)
        return pages
    rows = [f"| {i + 1} | {head(p)} |" for i, p in enumerate(pages) if i != idx]
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
               "| Part | Pages |\n|---|---|\n" + "\n".join(f"| {k} | {ranges(v)} |" for k, v in sorted(part.items())) + "\n", p, count=1)
    pages[idx] = p
    return pages


def build_toc(text: str) -> str:
    """Replace the TOC region with nested collapsible details."""
    start = text.find("## Table of Contents")
    end = text.find("## Document Map")
    if start < 0 or end < 0:
        print("warn: TOC region not found", file=sys.stderr)
        return text
    body = text[start:end]

    parts = re.split(r"^\*\*(Part [IVX]+ — [^\n*]+)\*\*\s*$", body, flags=re.MULTILINE)
    out = ["## Table of Contents\n", TOC_CSS]
    for i in range(1, len(parts), 2):
        title, chunk = parts[i], parts[i + 1]
        secs = re.findall(r"^\s*(\d+)\.\s*\[([^\]]+)\]\(#([^)]+)\)\s*$", chunk, re.MULTILINE)
        out.append(f"<details class=\"toc\">\n<summary>{title}</summary>\n")
        for num, label, anchor in secs:
            out.append(f"{num}. [{label}](#{anchor})\n")
        out.append("\n</details>\n")
    text = text[:start] + "".join(out) + "\n---\n\n" + text[end:]

    # part indexes become collapsible too
    def wrap_idx(m: re.Match) -> str:
        items = "".join(f"{n}. [{l}](#{a})\n" for n, l, a in
                        re.findall(r"^(\d+)\. \[([^\]]+)\]\(#([^)]+)\)\s*$", m.group(2), re.MULTILINE))
        return f"**Part {m.group(1)} index**\n\n<details class=\"toc\">\n<summary>Show sections</summary>\n\n{items}\n</details>\n"

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


def inject_images(text: str, allow: set[str]) -> str:
    for anchor, keys in ANCHORS.items():
        text = re.sub(rf"<!-- patch:img:{re.escape(anchor)} -->.*?<!-- /patch:img -->\n\n?", "", text, flags=re.S)
        if anchor not in text:
            print(f"warn: anchor missing {anchor}", file=sys.stderr)
            continue
        live = [k for k in keys if k in allow]
        if not live:
            continue
        figs = "\n".join(
            f'<figure><img src="{M[k][0]}" alt="{M[k][1]}" width="220" loading="lazy">'
            f'<figcaption>{M[k][1]} — {M[k][2]} ({M[k][3]})</figcaption></figure>'
            for k in live)
        blk = (f"<!-- patch:img:{anchor} -->\n"
               f'<p class="plates">\n{figs}\n</p>\n<!-- /patch:img -->\n\n')
        text = text.replace(anchor, anchor + "\n\n" + blk, 1)
    return text


def do_assets(root: Path, allow: set[str]) -> None:
    d = root / "assets" / "plates"
    d.mkdir(parents=True, exist_ok=True)
    cr = ["# Image credits", "", "Hotlinked from public sources; validate before redistribution.", "",
          "| Key | Source | Licence | URL |", "|---|---|---|---|"]
    for k in sorted(allow):
        url, alt, credit, lic = M[k]
        cr.append(f"| {k} | {credit} | {lic} | {url} |")
    (d / "CREDITS.md").write_text("\n".join(cr) + "\n")
    for name, svg in (("banner", BANNER), ("front-end-exploded", PH.format(label="front end exploded"))):
        if not (root / "assets" / f"{name}.png").exists():
            (root / "assets" / f"{name}.svg").write_text(svg)


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
            f"{hdr}\n|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n\n</details>\n<!-- /patch:{key} -->\n")


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
    for k, a in A.items():
        text = re.sub(rf"<!-- patch:{k} -->.*?<!-- /patch:{k} -->\n\n?", "", text, flags=re.S)
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
                                    "\n\nFill, flip to `STATUS: VERIFIED`, run `--check`.\n")


def status(text: str, total: int) -> str:
    text = re.sub(r"<!-- patch:status -->.*?<!-- /patch:status -->\n\n?", "", text, flags=re.S)
    n = len(re.findall(UNVER, text))
    hot = len(re.findall(r"https://(?!img\.shields)", text))
    blk = (f"<!-- patch:status -->\n> **Release status.** {total} pages · {n} verification block(s) outstanding · "
           f"{hot} hotlink(s) · images injected where anchored.\n"
           "> `--check` is green only at zero outstanding and zero hotlinks.\n<!-- /patch:status -->\n\n")
    m = re.search(r"^(# IMSI Catcher Platforms[^\n]*\n)", text, re.MULTILINE)
    return text[:m.end()] + "\n" + blk + text[m.end():] if m else blk + text


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
    a = ap.parse_args()

    if not a.src.exists():
        die(f"{a.src} not found")
    text = a.src.read_text()

    if a.check:
        n = len(re.findall(UNVER, text))
        hot = len(re.findall(r"https://(?!img\.shields)", text))
        print(f"unverified={n} hotlinks={hot}")
        return 1 if n or hot else 0

    root = Path.cwd()
    allow = set(M)
    if a.validate:
        good, bad = validate()
        allow = set(good)
        print(f"validated {len(good)} ok, {len(bad)} dead", file=sys.stderr)
        (root / "dead-images.txt").write_text("\n".join(bad) + "\n")

    do = a.all or a.fix_page8 or a.assets or a.images or a.toc or a.verify
    if not do:
        die("nothing to do; use --all or a specific flag")

    pages = text.split(SEP)
    before = len(pages)
    if a.all or a.fix_page8:
        pages, removed = fix_page8(pages, a.keep_page8)
        pages = rebuild_index(renumber(pages))
        text = fix_counts(SEP.join(pages), len(pages))
        print(f"pages {before} -> {len(pages)} (removed {removed})", file=sys.stderr)
    if a.all or a.toc:
        text = build_toc(text)
    if a.all or a.assets:
        if not a.dry_run:
            do_assets(root, allow)
    if a.all or a.images:
        text = inject_images(text, allow)
    if a.all or a.verify:
        text = inject_verify(text)

    text = status(text, len(text.split(SEP)))
    ledger(root, text)

    if a.dry_run:
        print("dry run: only VERIFY.md written", file=sys.stderr)
        return 0
    bak = a.src.with_suffix(".bak")
    if not bak.exists():
        shutil.copy2(a.src, bak)
    (a.out or a.src).write_text(text)
    print(f"wrote {a.out or a.src}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())