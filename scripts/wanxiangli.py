#!/usr/bin/env python3
"""Legacy CLI path: replay the historical v2.1 result by default."""
import runpy
import sys
from pathlib import Path

if '--engine' not in sys.argv:
    sys.argv[1:1] = ['--engine', 'v2.1']
runpy.run_path(str(Path(__file__).resolve().parents[1] / 'scripts/daymix.py'), run_name='__main__')
