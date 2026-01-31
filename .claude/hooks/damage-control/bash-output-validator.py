#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# ///
"""
Bash Output Validator - PostToolUse Hook

Scans command output for accidentally exposed secrets/credentials.
Provides rotation guidance when secrets are detected.

Exit codes:
  0 = Always (PostToolUse hooks observe, don't block)

Output: Warning message to stderr when secrets detected
"""

import json
import sys
import re


# Secret detection patterns with provider info
SECRET_PATTERNS = [
    {
        "pattern": r"sk-ant-[A-Za-z0-9\-_]{20,}",
        "name": "Anthropic API Key",
        "rotate_url": "console.anthropic.com/settings/keys"
    },
    {
        "pattern": r"sk-[A-Za-z0-9]{48,}",
        "name": "OpenAI API Key",
        "rotate_url": "platform.openai.com/api-keys"
    },
    {
        "pattern": r"ghp_[A-Za-z0-9]{36}",
        "name": "GitHub Personal Access Token",
        "rotate_url": "github.com/settings/tokens"
    },
    {
        "pattern": r"gho_[A-Za-z0-9]{36}",
        "name": "GitHub OAuth Token",
        "rotate_url": "github.com/settings/tokens"
    },
    {
        "pattern": r"AKIA[A-Z0-9]{16}",
        "name": "AWS Access Key ID",
        "rotate_url": "console.aws.amazon.com/iam"
    },
    {
        "pattern": r"-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----",
        "name": "Private Key",
        "rotate_url": "Generate new key pair and update all services"
    },
    {
        "pattern": r"Bearer\s+[A-Za-z0-9\-_\.]{20,}",
        "name": "Bearer Token",
        "rotate_url": "Rotate at the issuing service"
    },
    {
        "pattern": r"xox[baprs]-[A-Za-z0-9\-]{10,}",
        "name": "Slack Token",
        "rotate_url": "api.slack.com/apps"
    },
    {
        "pattern": r"sq0[a-z]{3}-[A-Za-z0-9\-_]{22,}",
        "name": "Square Access Token",
        "rotate_url": "developer.squareup.com/apps"
    },
    {
        "pattern": r"stripe[_-]?[a-z]*[_-]?key['\"]?\s*[:=]\s*['\"]?[a-zA-Z0-9_\-]{20,}",
        "name": "Stripe API Key",
        "rotate_url": "dashboard.stripe.com/apikeys"
    },
]

# Generic patterns (lower confidence)
GENERIC_PATTERNS = [
    {
        "pattern": r"['\"]?password['\"]?\s*[:=]\s*['\"][^'\"]{8,}['\"]",
        "name": "Hardcoded Password",
        "rotate_url": "Change the password immediately"
    },
    {
        "pattern": r"['\"]?api[_-]?key['\"]?\s*[:=]\s*['\"][A-Za-z0-9\-_]{20,}['\"]",
        "name": "Generic API Key",
        "rotate_url": "Identify the service and rotate the key"
    },
]


def scan_for_secrets(content: str) -> list:
    """Scan content for secret patterns. Returns list of findings."""
    findings = []

    # High confidence patterns first
    for item in SECRET_PATTERNS:
        try:
            if re.search(item["pattern"], content, re.IGNORECASE):
                findings.append({
                    "name": item["name"],
                    "rotate_url": item["rotate_url"],
                    "confidence": "high"
                })
        except re.error:
            continue

    # Generic patterns (only if no high-confidence matches)
    if not findings:
        for item in GENERIC_PATTERNS:
            try:
                if re.search(item["pattern"], content, re.IGNORECASE):
                    findings.append({
                        "name": item["name"],
                        "rotate_url": item["rotate_url"],
                        "confidence": "medium"
                    })
            except re.error:
                continue

    return findings


def format_warning(findings: list) -> str:
    """Format warning message with rotation guidance."""
    lines = [
        "",
        "=" * 60,
        "  SECURITY ALERT: Possible credentials exposed in output!",
        "=" * 60,
        "",
        "Detected:",
    ]

    for f in findings:
        lines.append(f"  - {f['name']} (confidence: {f['confidence']})")

    lines.extend([
        "",
        "IMMEDIATE ACTIONS:",
        "  1. Rotate this credential immediately",
        "  2. Check if this was committed to git (git log -p | grep <key>)",
        "  3. Review who has access to this terminal/logs",
        "",
        "ROTATION LINKS:",
    ])

    for f in findings:
        lines.append(f"  - {f['name']}: {f['rotate_url']}")

    lines.extend([
        "",
        "BEST PRACTICES:",
        "  - Store secrets in .env files (add .env to .gitignore)",
        "  - Use environment variables, not hardcoded values",
        "  - Never commit secrets to version control",
        "  - Use secret managers for production (AWS Secrets Manager, etc.)",
        "",
        "=" * 60,
        ""
    ])

    return "\n".join(lines)


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = input_data.get("tool_name", "")

    if tool_name != "Bash":
        sys.exit(0)

    tool_output = input_data.get("tool_output", {})
    stdout = str(tool_output.get("stdout", ""))
    stderr = str(tool_output.get("stderr", ""))

    content = stdout + "\n" + stderr

    if not content.strip():
        sys.exit(0)

    findings = scan_for_secrets(content)

    if findings:
        warning = format_warning(findings)
        print(warning, file=sys.stderr)

    # PostToolUse hooks always exit 0 (observe, don't block)
    sys.exit(0)


if __name__ == "__main__":
    main()
