---
description: Gain a general understanding of the codebase
allowed-tools: Bash, Read, Glob
model: sonnet
---

# Prime

## Purpose

Quickly understand any codebase by reading key files and summarizing the project structure. Run this when starting work on a new or unfamiliar project.

## Workflow

1. Run `git ls-files` to list all tracked files in the repository
2. Read `README.md` for project overview (if it exists)
3. Identify the main technology stack from package.json, requirements.txt, or similar
4. Note the folder structure and key directories
5. Identify entry points (main.py, index.ts, app.js, etc.)

## Report

Summarize your understanding:

```
Project: [name]
Stack: [technologies identified]

Structure:
- [key folder]: [purpose]
- [key folder]: [purpose]

Entry Points:
- [file]: [description]

Key Files:
- [file]: [what it does]

Ready to work. What would you like to do?
```
