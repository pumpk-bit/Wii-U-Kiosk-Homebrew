#!/usr/bin/env python3
"""Forward to the shared generator so `python ../tools/generate_title_xml.py` still works."""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
SHARED = PROJECT.parent / "tools" / "generate_title_xml.py"
sys.argv = [str(SHARED), "--project", str(PROJECT), *sys.argv[1:]]
runpy.run_path(str(SHARED), run_name="__main__")
