---
description: Save session state for seamless continuation later
allowed-tools: Read, Write, Glob, Bash
model: sonnet
argument-hint: [optional: topic name]
---

# Session Handoff

## Purpose

Create a structured handoff file capturing your current work state. Use this before ending a session so you (or someone else) can pick up exactly where you left off. Pairs with `/pickup`.

## Variables

TOPIC: $ARGUMENTS
HANDOFF_DIR: specs/handoffs/

## Instructions

- Review the current conversation to capture context
- Include specific file paths, not vague descriptions
- Number handoffs sequentially (001, 002, 003...)
- Be detailed about next steps - future you will thank present you

## Workflow

1. **Ensure folder exists**
   - Run `mkdir -p specs/handoffs`

2. **Determine handoff number**
   - List existing files in `specs/handoffs/`
   - Find the highest number and increment by 1
   - Format: `001`, `002`, `003`, etc.

3. **Generate filename**
   - Format: `[NNN]-[YYYY-MM-DD]-[topic].md`
   - Example: `001-2026-01-24-api-setup.md`
   - If no topic provided, use "session"

4. **Gather context from conversation**
   - What task/feature we were working on
   - What was completed
   - What is still in progress
   - What the next steps are
   - Any blockers or important decisions
   - Key files that were modified or are relevant

5. **Create handoff file**
   - Write to `specs/handoffs/[filename]`
   - Use the structured format below

6. **Confirm creation**
   - Report the filename and location
   - Remind user to run `/pickup` in next session

## Handoff File Format

```markdown
# Session Handoff - [YYYY-MM-DD]

## Context
[1-2 sentences: What we were working on and why]

## Completed
- [Item 1]
- [Item 2]

## In Progress
- [Current state/status of ongoing work]

## Next Steps
1. [Most important next action]
2. [Second priority]
3. [Third priority]

## Key Files
- [path/to/file1] - [brief description]
- [path/to/file2] - [brief description]

## Blockers / Notes
- [Any issues, decisions, or context needed]
```

## Report

```
Handoff Created

File: specs/handoffs/[filename]
Number: [NNN]
Topic: [topic]

To resume: Run `/pickup` in your next session
```
