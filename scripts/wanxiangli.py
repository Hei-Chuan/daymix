#!/usr/bin/env python3
"""Convenience entry point from the repository root."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).resolve().parents[1]/'skills/wanxiangli/scripts/wanxiangli.py'),run_name='__main__')
