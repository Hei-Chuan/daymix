#!/usr/bin/env python3
"""Legacy Skill entry point: replay v2.1 unless an engine is supplied."""
import runpy
import sys
from pathlib import Path

if '--engine' not in sys.argv:
    sys.argv[1:1] = ['--engine', 'v2.1']
runpy.run_path(str(Path(__file__).with_name('daymix.py')), run_name='__main__')
