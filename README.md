# Claude Code Starter Template

A production-ready project template for the Claude Code Fundamentals course. Clone this repo to start any new project with best practices built in.

## Quick Start

```bash
# Clone the template
git clone https://github.com/[your-username]/claude-code-starter-template.git my-project
cd my-project

# Remove the original git history and start fresh
rm -rf .git
git init

# Set up your environment
cp .env.example .env
# Edit .env with your API keys

# Start Claude Code
claude
```

## What's Included

### Core Workflow Commands

| Command | Purpose |
|---------|---------|
| `/EA-plan` | Create a detailed implementation plan in `specs/todo/` |
| `/EA-build` | Build from a plan, move to `specs/done/` when complete |
| `/EA-validate` | Run tests and verify the application works |
| `/EA-commit` | Create a git commit with a descriptive message |
| `/EA-review` | Review implementation against the original spec |
| `/EA-prime` | Understand the codebase structure |
| `/EA-handoff` | Save session state for later continuation |
| `/EA-pickup` | Resume from a previous session handoff |

### Security Hooks (Active by Default)

The template includes damage-control hooks that protect you from dangerous operations:

- **bash-tool-guard.py** - Blocks dangerous bash commands (rm -rf, force push, etc.)
- **bash-output-validator.py** - Detects accidentally exposed secrets
- **edit-tool-guard.py** - Protects sensitive files from edits
- **write-tool-guard.py** - Protects sensitive files from writes

Protected paths include `.env`, `~/.ssh/`, `~/.aws/`, and more. See `patterns.yaml` for full list.

### Pre-configured MCPs

- **Playwright** - Browser automation for visual verification

### Project Structure

```
your-project/
├── .claude/
│   ├── CLAUDE.md           # Project memory (keep under 500 tokens)
│   ├── settings.json       # Permissions and hook configuration
│   ├── commands/           # Your slash commands
│   ├── hooks/              # Security hooks
│   │   └── damage-control/ # Pre-configured protection
│   ├── skills/             # Multi-file capability packages
│   └── agents/             # Subagent configurations
├── .mcp.json               # MCP server configuration
├── .env.example            # API key template
├── .gitignore              # Pre-configured ignore patterns
├── docs/                   # Project documentation
├── specs/                  # Planning and handoffs
│   ├── todo/               # Plans waiting to be built
│   ├── done/               # Completed plans
│   └── handoffs/           # Session state files
├── app/                    # Application code
│   ├── client/             # Frontend
│   └── server/             # Backend (optional)
├── ai_docs/                # API docs for Claude to reference
└── README.md
```

## The Core Workflow

```
PLAN → BUILD → VALIDATE → REVIEW → COMMIT
```

1. **Plan**: `/EA-plan "add user authentication"` - Creates detailed spec
2. **Build**: `/EA-build specs/todo/user-auth.md` - Implements the plan
3. **Validate**: `/EA-validate` - Runs tests and checks
4. **Review**: `/EA-review` - Compares implementation to spec
5. **Commit**: `/EA-commit` - Creates a meaningful commit

## Session Management

Before ending a session:
```
/EA-handoff "what we worked on"
```

When starting a new session:
```
/EA-pickup
```

## Customization

### Adding API Keys

1. Copy `.env.example` to `.env`
2. Add your keys (Google Gemini is free!)
3. Never commit `.env` to git

### Adding Skills

Create a folder in `.claude/skills/`:
```
.claude/skills/my-skill/
├── SKILL.md      # Entry point
└── cookbook/     # Workflow guides
```

### Adding Agents

Create markdown files in `.claude/agents/`:
```
.claude/agents/code-reviewer.md
```

### Modifying Security Patterns

Edit `.claude/hooks/damage-control/patterns.yaml` to customize:
- Blocked bash patterns
- Protected paths
- Read-only paths

## Requirements

- Claude Code installed (`npm install -g @anthropic-ai/claude-code`)
- Python 3.8+ (for security hooks)
- PyYAML (`pip install pyyaml`)

## Course Modules

This template incorporates concepts from:
- Module 1: Getting Started
- Module 2: Commands
- Module 3: Core Workflow
- Module 5: Skills (folder structure)
- Module 6: Subagents (folder structure)
- Module 7: Security (hooks)

---

*Part of the Claude Code Fundamentals course for Early AI Adopters*
