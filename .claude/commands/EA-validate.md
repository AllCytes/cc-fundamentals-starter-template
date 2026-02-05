---
description: Run tests and validate the application works correctly
allowed-tools: Bash, Read, Glob, Grep
model: sonnet
argument-hint: [--fix] [--quick] [--verbose]
---

# EA-Validate Command

Run comprehensive validation for the current project by detecting the test framework and executing appropriate checks.

## Arguments

- `--fix` - Auto-fix linting issues where possible
- `--quick` - Skip long-running tests (type check and lint only)
- `--verbose` - Show detailed output for all checks

## Workflow

### Step 1: Detect Project Type

Check for configuration files to determine the project type:

| Priority | File Present | Framework | Test Command |
|----------|--------------|-----------|--------------|
| 1 | `package.json` + `vitest.config.*` | Vitest | `npx vitest run` |
| 2 | `package.json` + `jest.config.*` | Jest | `npm test` |
| 3 | `bun.lockb` | Bun | `bun test` |
| 4 | `package.json` (with test script) | npm | `npm test` |
| 5 | `pyproject.toml` (with pytest) | Pytest | `pytest tests/ -v --tb=short` |
| 6 | `requirements.txt` | Python | `python -m pytest` |
| 7 | `Cargo.toml` | Rust | `cargo test` |
| 8 | `go.mod` | Go | `go test ./...` |

Use Glob to check which configuration files exist:
```
Glob: package.json, vitest.config.*, jest.config.*, bun.lockb, pyproject.toml, requirements.txt, Cargo.toml, go.mod
```

### Step 2: Run Type Checking

Based on detected framework:

**TypeScript/JavaScript:**
```bash
npx tsc --noEmit
```

**Python:**
```bash
python -m py_compile *.py
# Or for a project with src/:
find . -name "*.py" -exec python -m py_compile {} \;
```

### Step 3: Run Linting

**TypeScript/JavaScript:**
```bash
# With --fix argument
npx eslint . --fix

# Without --fix
npx eslint .
```

**Python:**
```bash
# With --fix argument
ruff check . --fix

# Without --fix
ruff check .
```

### Step 4: Run Build (if applicable)

Check if a build script exists in package.json:
```bash
npm run build
```

Or for Python projects with a build step:
```bash
python -m build
```

### Step 5: Run Tests

Skip this step if `--quick` argument is provided.

Execute the test command based on detected framework:
- Vitest: `npx vitest run`
- Jest: `npm test`
- Bun: `bun test`
- npm: `npm test`
- Pytest: `pytest tests/ -v --tb=short`
- Rust: `cargo test`
- Go: `go test ./...`

### Step 6: Generate Summary Report

Output the validation results in this format:

```markdown
## Validation Results

**Project:** [project name from package.json or directory]
**Status:** PASSED | PARTIAL | FAILED
**Framework:** [detected framework]

### Summary
- Total Checks: [count]
- Passed: [count]
- Failed: [count]

### Check Details

[TYPE CHECK] - PASSED/FAILED
  [output or "No errors"]

[LINT] - PASSED/FAILED
  [issues found or "No issues"]

[BUILD] - PASSED/FAILED/SKIPPED
  [output or "Build successful"]

[TESTS] - PASSED/FAILED/SKIPPED
  [test results summary]

### Next Steps
- [actionable items based on failures]
```

## Status Determination

- **PASSED**: All checks pass
- **PARTIAL**: Some checks pass, some fail (or some skipped with --quick)
- **FAILED**: Critical checks fail (type check or tests)

## Error Handling

- If no project type is detected, report "Unknown project type" and suggest manual configuration
- If a check command is not found, mark as SKIPPED and continue
- Capture both stdout and stderr for comprehensive error reporting
