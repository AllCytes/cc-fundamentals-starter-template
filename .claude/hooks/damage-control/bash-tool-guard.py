#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = ["pyyaml"]
# ///
"""
Bash Tool Guard - PreToolUse Hook

Blocks dangerous bash commands before execution.
Checks: bashToolPatterns, zeroAccessPaths, readOnlyPaths, noDeletePaths

Exit codes:
  0 = Allow
  0 + JSON {"decision": "ask"} = Request confirmation
  2 = Block (stderr sent to Claude)
"""

import json
import sys
import re
import os
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(0)


def load_patterns():
    """Load patterns from patterns.yaml in same directory as script."""
    script_dir = Path(__file__).parent
    patterns_file = script_dir / "patterns.yaml"

    if not patterns_file.exists():
        return {}

    with open(patterns_file, "r") as f:
        return yaml.safe_load(f) or {}


def expand_path(path: str) -> str:
    """Expand ~ and environment variables in path."""
    return os.path.expanduser(os.path.expandvars(path))


def matches_path_pattern(command: str, patterns: list) -> tuple:
    """Check if command accesses any protected path. Returns (matched, pattern)."""
    for pattern in patterns:
        expanded = expand_path(pattern)

        # Handle glob patterns
        if "*" in pattern:
            # Convert glob to regex
            regex_pattern = pattern.replace(".", r"\.").replace("*", ".*")
            if re.search(regex_pattern, command, re.IGNORECASE):
                return True, pattern
        else:
            # Direct path match
            if expanded in command or pattern in command:
                return True, pattern

    return False, None


def check_command(command: str, config: dict) -> dict:
    """
    Check command against all patterns.
    Returns: {"allow": True/False, "ask": True/False, "reason": str}
    """
    # Check bash tool patterns
    for item in config.get("bashToolPatterns", []):
        pattern = item.get("pattern", "")
        reason = item.get("reason", "Matched blocked pattern")
        ask = item.get("ask", False)

        try:
            if re.search(pattern, command, re.IGNORECASE):
                if ask:
                    return {"allow": False, "ask": True, "reason": reason}
                else:
                    return {"allow": False, "ask": False, "reason": reason}
        except re.error:
            continue

    # Check zero access paths (block completely)
    matched, pattern = matches_path_pattern(command, config.get("zeroAccessPaths", []))
    if matched:
        return {
            "allow": False,
            "ask": False,
            "reason": f"Access to protected path blocked: {pattern}"
        }

    # Check read-only paths (block modifications)
    modification_indicators = ["rm ", "mv ", ">", ">>", "tee ", "sed -i", "chmod ", "chown "]
    for indicator in modification_indicators:
        if indicator in command:
            matched, pattern = matches_path_pattern(command, config.get("readOnlyPaths", []))
            if matched:
                return {
                    "allow": False,
                    "ask": False,
                    "reason": f"Modification of read-only path blocked: {pattern}"
                }

    # Check no-delete paths
    deletion_indicators = ["rm ", "rmdir ", "unlink ", "del "]
    for indicator in deletion_indicators:
        if indicator in command:
            matched, pattern = matches_path_pattern(command, config.get("noDeletePaths", []))
            if matched:
                return {
                    "allow": False,
                    "ask": False,
                    "reason": f"Deletion of protected path blocked: {pattern}"
                }

    return {"allow": True, "ask": False, "reason": ""}


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)  # Allow on parse error

    tool_name = input_data.get("tool_name", "")

    if tool_name != "Bash":
        sys.exit(0)  # Only check Bash tool

    tool_input = input_data.get("tool_input", {})
    command = tool_input.get("command", "")

    if not command:
        sys.exit(0)

    config = load_patterns()
    result = check_command(command, config)

    if result["allow"]:
        sys.exit(0)
    elif result["ask"]:
        # Request user confirmation
        output = {
            "decision": "ask",
            "reason": result["reason"]
        }
        print(json.dumps(output))
        sys.exit(0)
    else:
        # Block the command
        print(f"BLOCKED: {result['reason']}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
