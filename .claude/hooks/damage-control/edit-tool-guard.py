#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = ["pyyaml"]
# ///
"""
Edit Tool Guard - PreToolUse Hook

Blocks edits to protected files (zeroAccess and readOnly paths).

Exit codes:
  0 = Allow
  2 = Block
"""

import json
import sys
import re
import os
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit(0)


def load_patterns():
    script_dir = Path(__file__).parent
    patterns_file = script_dir / "patterns.yaml"

    if not patterns_file.exists():
        return {}

    with open(patterns_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def expand_path(path: str) -> str:
    return os.path.expanduser(os.path.expandvars(path))


def matches_protected_path(file_path: str, patterns: list) -> tuple:
    """Check if file matches any protected pattern."""
    file_path = expand_path(file_path)

    for pattern in patterns:
        expanded = expand_path(pattern)

        if "*" in pattern:
            regex_pattern = pattern.replace(".", r"\.").replace("*", ".*")
            if re.search(regex_pattern, file_path, re.IGNORECASE):
                return True, pattern
        else:
            if expanded in file_path or pattern in file_path:
                return True, pattern
            if file_path.endswith(pattern) or file_path.endswith(pattern.rstrip("/")):
                return True, pattern

    return False, None


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = input_data.get("tool_name", "")

    if tool_name != "Edit":
        sys.exit(0)

    tool_input = input_data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    if not file_path:
        sys.exit(0)

    config = load_patterns()

    # Check zero access paths
    matched, pattern = matches_protected_path(file_path, config.get("zeroAccessPaths", []))
    if matched:
        print(f"BLOCKED: Cannot edit protected file matching: {pattern}", file=sys.stderr)
        sys.exit(2)

    # Check read-only paths
    matched, pattern = matches_protected_path(file_path, config.get("readOnlyPaths", []))
    if matched:
        print(f"BLOCKED: Cannot edit read-only file matching: {pattern}", file=sys.stderr)
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
