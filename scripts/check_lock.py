#!/usr/bin/env python3
"""
project-initiator: check_lock.py
Quick structural lock check for pre-commit hooks, CI, and AI agent guardrails.
Returns exit code 0 on valid structure, 1 on unauthorized additions.
"""

import sys
from pathlib import Path

# Add scripts directory to path to import init_scaffold
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from init_scaffold import verify_structure

def main():
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    passed = verify_structure(root)
    sys.exit(0 if passed else 1)

if __name__ == "__main__":
    main()
