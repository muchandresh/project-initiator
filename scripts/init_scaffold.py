#!/usr/bin/env python3
"""
project-initiator: init_scaffold.py
Universal directory scaffolding, lock generation, and structural integrity verifier.
Standard library only - zero external dependencies.
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

DEFAULT_DIRECTORIES = [
    ".agents/skills",
    "src/core",
    "src/api",
    "src/models",
    "src/services",
    "src/utils",
    "tests/unit",
    "tests/integration",
    "config",
]

DEFAULT_FILES = [
    "PRD.md",
    "ARCHITECTURE.md",
    "AGENTS.md",
    "SECURITY_AND_PERFORMANCE.md",
    ".structure_lock.json",
    ".gitignore",
    "README.md",
]

def load_lock(project_root: Path) -> dict:
    lock_file = project_root / ".structure_lock.json"
    if not lock_file.exists():
        return {}
    try:
        with open(lock_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Warning: Failed to read .structure_lock.json: {e}", file=sys.stderr)
        return {}

def save_lock(project_root: Path, lock_data: dict):
    lock_file = project_root / ".structure_lock.json"
    with open(lock_file, "w", encoding="utf-8") as f:
        json.dump(lock_data, f, indent=2)
    print(f"🔒 Structure lock updated: {lock_file}")

def scaffold_project(project_root: Path, project_name: str, custom_dirs=None, custom_files=None):
    dirs = custom_dirs if custom_dirs else DEFAULT_DIRECTORIES
    files = custom_files if custom_files else DEFAULT_FILES

    print(f"🚀 Initializing scaffold for '{project_name}' in: {project_root}")

    # Create directories
    for d in dirs:
        dir_path = project_root / d
        dir_path.mkdir(parents=True, exist_ok=True)
        # Create .gitkeep if empty
        gitkeep = dir_path / ".gitkeep"
        if not gitkeep.exists() and not any(dir_path.iterdir()):
            gitkeep.touch()
        print(f"  📁 Created directory: {d}")

    # Prepare lock file
    now_iso = datetime.now().isoformat()
    lock_data = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "project": project_name,
        "initialized_at": now_iso,
        "lock_active": True,
        "rules": {
            "disallow_unauthorized_files": True,
            "disallow_unauthorized_directories": True,
            "require_explicit_user_permission": True,
            "attach_vibe_map": True
        },
        "authorized_directories": sorted(list(set(dirs))),
        "authorized_files": sorted(list(set(files))),
        "permission_log": [
            {
                "timestamp": now_iso,
                "action": "initial_scaffolding",
                "authorized_by": "user",
                "details": f"Initial project scaffold for {project_name}"
            }
        ]
    }
    save_lock(project_root, lock_data)

    print("\n✅ Scaffolding complete! Structure is locked.")
    print("⚠️ Remember: AI models MUST ask explicit permission before creating files outside this lock.")

def verify_structure(project_root: Path) -> bool:
    lock = load_lock(project_root)
    if not lock:
        print("❌ Error: No .structure_lock.json found. Run scaffold first.", file=sys.stderr)
        return False

    auth_dirs = set(lock.get("authorized_directories", []))
    auth_files = set(lock.get("authorized_files", []))

    # Also allow standard git/env metadata
    allowed_system_paths = {
        ".git", ".gitignore", ".env", ".env.example", ".structure_lock.json",
        ".DS_Store", "__pycache__", "node_modules", "vibe-map-out"
    }

    violations = []
    
    for root, dirs, files in os.walk(project_root):
        rel_root = os.path.relpath(root, project_root)
        if rel_root == ".":
            rel_root = ""

        # Skip ignored trees
        first_segment = rel_root.split(os.sep)[0] if rel_root else ""
        if first_segment in allowed_system_paths or ".git" in rel_root:
            continue

        if rel_root and rel_root not in auth_dirs:
            # Check if any parent is authorized or exact match
            if not any(rel_root.startswith(d) for d in auth_dirs):
                violations.append(f"Unauthorized Directory: {rel_root}")

        for f in files:
            if f in allowed_system_paths or f == ".gitkeep":
                continue
            rel_file = os.path.join(rel_root, f) if rel_root else f
            rel_file_normalized = rel_file.replace("\\", "/")

            if rel_file_normalized not in auth_files:
                # Check if it resides within an authorized directory
                file_dir = os.path.dirname(rel_file_normalized)
                if file_dir not in auth_dirs and not any(file_dir.startswith(d) for d in auth_dirs):
                    violations.append(f"Unauthorized File: {rel_file_normalized}")

    if violations:
        print("❌ Structure Lock Violations Detected:")
        for v in violations:
            print(f"  🚨 {v}")
        print("\n⚠️ Agents must ask the user for permission before creating or accessing unauthorized paths!")
        return False
    else:
        print("✅ Structure Verification Passed: All directories and files conform to .structure_lock.json")
        return True

def grant_permission(project_root: Path, target_path: str, reason: str):
    lock = load_lock(project_root)
    if not lock:
        print("❌ Error: No .structure_lock.json found.", file=sys.stderr)
        return

    normalized_path = target_path.strip().replace("\\", "/").rstrip("/")
    now_iso = datetime.now().isoformat()

    full_path = project_root / normalized_path
    is_dir = full_path.is_dir() or not (Path(normalized_path).suffix)

    if is_dir:
        if normalized_path not in lock["authorized_directories"]:
            lock["authorized_directories"].append(normalized_path)
            lock["authorized_directories"].sort()
    else:
        if normalized_path not in lock["authorized_files"]:
            lock["authorized_files"].append(normalized_path)
            lock["authorized_files"].sort()

    lock["permission_log"].append({
        "timestamp": now_iso,
        "action": "user_permission_granted",
        "path": normalized_path,
        "is_dir": is_dir,
        "reason": reason or "User explicitly granted permission."
    })

    save_lock(project_root, lock)
    print(f"✅ Permission granted and logged for: {normalized_path}")

def main():
    parser = argparse.ArgumentParser(description="Project Initiator Scaffold & Structure Lock Utility")
    parser.add_argument("--root", default=".", help="Project root directory (default: current directory)")
    parser.add_argument("--init", action="store_true", help="Initialize directory scaffold & lock")
    parser.add_argument("--name", default="MyProject", help="Project name for initialization")
    parser.add_argument("--verify", action="store_true", help="Verify workspace against .structure_lock.json")
    parser.add_argument("--grant", help="Grant permission for a new file or directory path")
    parser.add_argument("--reason", default="", help="Reason for granting permission")

    args = parser.parse_args()
    project_root = Path(args.root).resolve()

    if args.init:
        scaffold_project(project_root, args.name)
    elif args.verify:
        success = verify_structure(project_root)
        sys.exit(0 if success else 1)
    elif args.grant:
        grant_permission(project_root, args.grant, args.reason)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
