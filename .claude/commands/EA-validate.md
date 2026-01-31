---
description: Run tests and validate the application works correctly
allowed-tools: Bash, Read, Glob, Grep
model: sonnet
argument-hint: [--fix] [--quick]
---

# EA-Validate

## Purpose

Run validation tests to ensure the application works correctly. Automatically detects project type and runs appropriate tests. Use this after `/EA-build` to verify your implementation.

## Variables

FIX_MODE: Arguments contain "--fix"
QUICK_MODE: Arguments contain "--quick"

## Instructions

- Detect project type from config files (package.json, pyproject.toml, etc.)
- Run ALL tests even if some fail
- In QUICK_MODE, skip long-running tests
- In FIX_MODE, attempt to auto-fix linting issues
- Provide clear, actionable feedback

## Project Detection

Check for key files to determine project type:
- `package.json` -> Node.js/JavaScript project
- `pyproject.toml` or `requirements.txt` -> Python project
- `Cargo.toml` -> Rust project
- `go.mod` -> Go project

## Workflow

1. **Detect project type**
   - Read config files to determine technology stack
   - Identify available test/lint/build scripts

2. **Run type checking** (if applicable)
   - TypeScript: `npx tsc --noEmit`
   - Python: `python -m py_compile [main files]`

3. **Run linting** (if lint script exists)
   - Node: `npm run lint` (add `--fix` in FIX_MODE)
   - Python: `ruff check .` or `flake8`

4. **Run build** (if build script exists)
   - Node: `npm run build`
   - Validates production build works

5. **Run tests** (skip in QUICK_MODE)
   - Node: `npm test`
   - Python: `pytest tests/ -v --tb=short`

6. **Compile results**
   - Count passed/failed/skipped
   - Extract error messages for failures

## Report

```
## Validation Results

**Project:** [project name]
**Status:** PASSED | PARTIAL | FAILED

### Summary
- Total Checks: [count]
- Passed: [count]
- Failed: [count]
- Skipped: [count]

### Check Details

[CHECK_NAME] - PASSED/FAILED
  [details or error message]

### Failed Tests (if any)

1. **[test name]**
   - Error: [error message]
   - File: [file:line]
   - Suggestion: [fix suggestion if obvious]

### Next Steps

- [actionable next step based on results]
```

## Examples

**Basic validation:**
```
/EA-validate
```

**Quick validation (skip long tests):**
```
/EA-validate --quick
```

**Auto-fix linting issues:**
```
/EA-validate --fix
```
