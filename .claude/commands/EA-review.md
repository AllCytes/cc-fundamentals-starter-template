---
description: Review implementation against the original spec file
allowed-tools: Bash, Read, Glob, Grep, mcp__playwright__playwright_navigate, mcp__playwright__playwright_screenshot
model: sonnet
argument-hint: [spec-file-path]
---

# EA-Review

## Purpose

Compare the implemented code against the original specification to ensure you built what was planned. Optionally capture screenshots of working features for visual verification.

## Variables

SPEC_FILE: $ARGUMENTS
SCREENSHOT_DIR: specs/review-screenshots/

## Instructions

- Read the spec file to understand original requirements
- Use git diff to see what changed
- Check each requirement against the implementation
- Take screenshots of key UI changes (if applicable)
- Report issues by severity: skippable, tech_debt, blocker

## Issue Severity Guide

| Severity | Description | Action |
|----------|-------------|--------|
| `skippable` | Non-blocking, minor issue | Can release, note for later |
| `tech_debt` | Works but needs cleanup | Can release, create follow-up task |
| `blocker` | Breaks functionality or UX | Must fix before release |

## Workflow

1. **Locate the spec**
   - If SPEC_FILE provided, use it
   - Otherwise, check `specs/done/` for recent specs
   - Read the spec file completely

2. **Review the changes**
   - Run `git diff origin/main` to see all changes
   - Compare each spec requirement to implementation
   - Check that all requirements are addressed

3. **Visual verification** (for UI changes)
   - Use Playwright to navigate to the app
   - Take 1-5 screenshots of key functionality
   - Save to SCREENSHOT_DIR with descriptive names
   - Format: `01_feature_working.png`, `02_another_view.png`

4. **Document issues** (if any)
   - Describe what's wrong
   - Suggest resolution
   - Assign severity
   - Include screenshot if visual issue

5. **Make recommendation**
   - APPROVED: All requirements met, no blockers
   - APPROVED_WITH_NOTES: Works, but has skippable/tech_debt issues
   - NEEDS_CHANGES: Has blocker issues

## Report

```
## Spec Review Results

**Spec:** [spec file path]
**Status:** APPROVED | APPROVED_WITH_NOTES | NEEDS_CHANGES

### Summary
[2-4 sentences: what was built and whether it matches spec]

### Requirements Checklist
- [x] Requirement 1 - Implemented correctly
- [x] Requirement 2 - Implemented correctly
- [ ] Requirement 3 - Partial (see issues)

### Issues Found (if any)

**Issue #1** (severity)
- Description: [what's wrong]
- Resolution: [how to fix]
- Screenshot: [path if applicable]

### Screenshots (if taken)
1. `specs/review-screenshots/01_feature.png` - [description]
2. `specs/review-screenshots/02_detail.png` - [description]

### Recommendation
[APPROVED / APPROVED_WITH_NOTES / NEEDS_CHANGES] - [brief rationale]
```

## Examples

**Review a specific spec:**
```
/EA-review specs/done/user-auth.md
```

**Review most recent spec:**
```
/EA-review
```
