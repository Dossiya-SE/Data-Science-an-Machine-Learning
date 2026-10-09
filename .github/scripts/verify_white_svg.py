"""Scoped XML color regression for governed scientific vector figures."""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

svg = Path(sys.argv[1])
raw = svg.read_text(encoding="utf-8")
root = ET.fromstring(raw)
ns = "{http://www.w3.org/2000/svg}"
assert root.find(ns+"title") is not None and root.find(ns+"desc") is not None
assert "--bg:#FFFFFF;--panel:#FFFFFF;" in raw
assert "prefers-color-scheme:dark" not in raw
assert "linearGradient" not in raw and "radialGradient" not in raw
assert not re.search(r'<text\b[^>]*fill="var\(--bg\)"', raw)
assert not re.search(r'<rect\b[^>]*fill="(?!#FFFFFF)"', raw)
assert re.search(r'\.panel\{fill:var\(--panel\)', raw)
print(f"PASS {svg}: white authored panels, scientific outline roles and legible dark text")
