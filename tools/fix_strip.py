#!/usr/bin/env python3
"""Tolerate the literal {key} closing tag left by the v2.4 block() bug."""
import os, sys, tempfile
from pathlib import Path

T = Path("tools") / "patch_readme.py"
OLD = r'''    text = re.sub(r"<!-- patch:(?:91|92|119) -->.*?<!-- /patch:(?:91|92|119) -->\n\n?", "", text, flags=re.S)'''
NEW = r'''    text = re.sub(r"<!-- patch:(?:91|92|119) -->.*?<!-- /patch:(?:91|92|119|\{key\}) -->\n\n?", "", text, flags=re.S)'''

src = T.read_text(encoding="utf-8")
if NEW in src:
    print("already applied"); raise SystemExit(0)
if src.count(OLD) != 1:
    print(f"anchor matched {src.count(OLD)}x; aborting", file=sys.stderr); raise SystemExit(1)

src = src.replace(OLD, NEW, 1)
fd, tmp = tempfile.mkstemp(dir="tools", prefix=".s-", suffix=".tmp")
with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(src); fh.flush(); os.fsync(fh.fileno())
os.replace(tmp, T)
print("strip now tolerates both close forms")