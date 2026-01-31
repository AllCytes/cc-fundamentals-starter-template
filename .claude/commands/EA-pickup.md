---
description: Resume from a previous session handoff
allowed-tools: Read, Glob, Bash
model: sonnet
argument-hint: [optional: handoff number or "list"]
---

# Pick Up From Last Session

## Purpose

Resume work from a previous session by reading the most recent handoff file. Provides context summary and next steps so you can continue seamlessly. Pairs with `/handoff`.

## Variables

HANDOFF_ARG: $ARGUMENTS
HANDOFF_DIR: specs/handoffs/

## Instructions

- Default: Load the most recent handoff (highest number)
- If a number is provided, load that specific handoff
- If "list" is provided, show all available handoffs
- Present information in a clear, actionable format

## Workflow

1. **Check for handoffs folder**
   - If `specs/handoffs/` doesn't exist, inform user no handoffs found

2. **Parse argument**
   - Empty -> Load most recent (highest numbered) handoff
   - Number (e.g., "2" or "002") -> Load that specific handoff
   - "list" -> Show all available handoffs

3. **Find handoff file**
   - List all files in `specs/handoffs/`
   - Sort by number prefix (001, 002, 003...)
   - Select appropriate file based on argument

4. **Read and present**
   - Read the handoff file
   - Present in the summary format below

5. **Offer next steps**
   - Based on handoff content, suggest where to start

## Report

```
Session Pickup Summary

Handoff: [filename]
Date: [date from handoff]

## Where We Left Off
[Context from handoff]

## Completed Previously
- [items from Completed section]

## Still In Progress
- [items from In Progress section]

## Next Steps
1. [from Next Steps]
2. [continue list]

## Key Files
- [from Key Files section]

## Notes
- [from Blockers/Notes if any]

---

Ready to continue. Would you like me to:
1. Start on the first next step
2. Review the in-progress items first
3. Something else?
```

## List Mode Report

When `/pickup list` is run:

```
Available Handoffs

001-2026-01-20-initial-setup.md
002-2026-01-21-api-endpoints.md
003-2026-01-24-frontend-ui.md  <- Most Recent

To load a specific handoff: /pickup 2
To load most recent: /pickup
```
