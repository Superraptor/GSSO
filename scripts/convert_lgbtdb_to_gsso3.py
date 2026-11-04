#!/usr/bin/env python3
"""
Top-level runner script for lgbtDB to GSSO 3.0.0 converter backbone.
Usage:
    python scripts/convert_lgbtdb_to_gsso3.py all --limit 100
    python scripts/convert_lgbtdb_to_gsso3.py validate
"""

import sys
import os

# Ensure repo root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.lgbtdb_to_gsso3.cli import main

if __name__ == "__main__":
    main()
