---
name: the agent-code
description: "Delegate coding to the coding agent CLI (features, PRs)."
version: 2.2.0
author: the agent + Teknium
license: MIT
metadata:
  agent:
    tags: [Coding-Agent, the assistant, Anthropic, Code-Review, Refactoring, PTY, Automation]
    related_skills: [agent-runtime, opencode]
---

# the coding agent: the agent Orchestration Guide

Delegate coding tasks to [the coding agent](https://code.the assistant.com/docs/en/cli-reference) (Anthropic's autonomous coding agent CLI) via the AMA agent terminal. the coding agent v2.x can read files, write code, run shell commands, spawn subagents, and manage git workflows autonomously.

## Prerequisites

- **Install:** `npm install -g @anthropic-ai/coding-agent`
- **Auth:** run `coding-agent` once to log in (browser OAuth for Pro/Max, or set `ANTHROPIC_API_KEY`)
- **Console auth:** `the agent auth login --console` for API key billing
- **SSO auth:** `the agent auth login --sso` for Enterprise
- **Check status:** `the agent auth status` (JSON) or `the agent auth status --text` (human-readable)
- **Health check:** `the agent doctor`: checks auto-updater and installation health
- **Version check:** `the agent --version` (requires v2.x+)
- **Update:** `the agent update` or `the agent upgrade`

## Two Orchestration Modes

the agent interacts with the coding agent in two fundamentally different ways. Choose based on the task.

### Mode 1: Print Mode (`-p`): Non-Interactive (PREFERRED for most tasks)

Print mode runs a one-shot task, returns the result, and exits. No PTY needed. No interactive prompts. This is the cleanest integration path.

```
terminal(command="the agent -p 'Add error handling to all API calls in src/' --allowedTools 'Read,Edit' --max-turns 10", workdir="/path/to/project", timeout=120)
```

**When to use print mode:**
- One-shot coding tasks (fix a bug, add a feature, refactor)
- CI/CD automation and scripting
- Structured data extraction with `--json-schema`
- Piped input processing (`cat file | the agent -p "analyze this"`)
- Any task where you don't need multi-turn conversation

**Print mode skips ALL interactive dialogs**: no workspace trust prompt, no permission confirmations. This makes it ideal for automation.

### Mode 2: Interactive PTY via tmux: Multi-Turn Sessions

Interactive mode gives you a full conversational REPL where you can send follow-up prompts, use slash commands, and watch The agent work in real time. **Requires tmux orchestration.**

```
# Start a tmux session
terminal(command="tmux new-session -d -s the agent-work -x 140 -y 40")

# Launch the coding agent inside it
terminal(command="tmux send-keys -t the agent-work 'cd /path/to/project && the agent' Enter")

# Wait for startup, then send your task
# (after ~3-5 seconds for the welcome screen)
terminal(command="sleep 5 && tmux send-keys -t the agent-work 'Refactor the auth module to use JWT tokens' Enter")

# Monitor progress by capturing the pane
terminal(command="sleep 15 && tmux capture-pane -t the agent-work -p -S -50")

# Send follow-up tasks
terminal(command="tmux send-keys -t the agent-work 'Now add unit tests for the new JWT code' Enter")

# Exit when done
terminal(command="tmux send-keys -t the agent-work '/exit' Enter")
```

**When to use interactive mode:**
- Multi-turn iterative work (refactor → review → fix → test cycle)
- Tasks requiring human-in-the-loop decisions
- Exploratory coding sessions
- When you need to use The agent's slash commands (`/compact`, `/review`, `/model`)

## PTY Dialog Handling (CRITICAL for Interactive Mode)

the coding agent presents up to two confirmation dialogs on first launch. You MUST handle these via tmux send-keys:

### Dialog 1: Workspace Trust (first visit to a directory)
```
❯ 1. Yes, I trust this folder    ← DEFAULT (just press Enter)
  2. No, exit
```
**Handling:** `tmux send-keys -t <session> Enter`: default selection is correct.

### Dialog 2: Bypass Permissions Warning (only with --dangerously-skip-permissions)
```
❯ 1. No, exit                    ← DEFAULT (WRONG choice!)
  2. Yes, I accept
```
**Handling:** Must navigate DOWN first, then Enter:
```
tmux send-keys -t <session> Down && sleep 0.3 && tmux send-keys -t <session> Enter
```

### Robust Dialog Handling Pattern
```
# Launch with permissions bypass
terminal(command="tmux send-keys -t the agent-work 'the agent --dangerously-skip-permissions \"your task\"' Enter")

# Handle trust dialog (Enter for default "Yes")
terminal(command="sleep 4 && tmux send-keys -t the agent-work Enter")

# Handle permissions dialog (Down then Enter for "Yes, I accept")
terminal(command="sleep 3 && tmux send-keys -t the agent-work Down && sleep 0.3 && tmux send-keys -t the agent-work Enter")

# Now wait for The agent to work
terminal(command="sleep 15 && tmux capture-pane -t the agent-work -p -S -60")
```

**Note:** After the first trust acceptance for a directory, the trust dialog won't appear again. Only the permissions dialog recurs each time you use `--dangerously-skip-permissions`.

## CLI Subcommands

| Subcommand | Purpose |
|------------|---------|
| `the agent` | Start interactive REPL |
| `the agent "query"` | Start REPL with initial prompt |
| `the agent -p "query"` | Print mode (non-interactive, exits when done) |
| `cat file \| the agent -p "query"` | Pipe content as stdin context |
| `the agent -c` | Continue the most recent conversation in this directory |
| `the agent -r "id"` | Resume a specific session by ID or name |
| `the agent auth login` | Sign in (add `--console` for API billing, `--sso` for Enterprise) |
| `the agent auth status` | Check login status (returns JSON. `--text` for human-readable) |
| `the agent mcp add <name> -- <cmd>` | Add an MCP server |
| `the agent mcp list` | List configured MCP servers |
| `the agent mcp remove <name>` | Remove an MCP server |
| `the agent agents` | List configured agents |
| `the agent doctor` | Run health checks on installation and auto-updater |
| `the agent update` / `the agent upgrade` | Update the coding agent to latest version |
| `coding-agent remote-control` | Start server to control the assistant from the assistant.ai or mobile app |
| `the agent install [target]` | Install native build (stable, latest, or specific version) |
| `the agent setup-token` | Set up long-lived auth token (requires subscription) |
| `the agent plugin` / `the agent plugins` | Manage the coding agent plugins |
| `the agent auto-mode` | Inspect auto mode classifier configuration |

## Print Mode Deep Dive

### Structured JSON Output
```
terminal(command="the agent -p 'Analyze auth.py for security issues' --output-format json --max-turns 5", workdir="/project", timeout=120)
```

Returns a JSON object with:
```json
{
  "type": "result",
  "subtype": "success",
  "result": "The analysis text...",
  "session_id": "75e2167f-...",
  "num_turns": 3,
  "total_cost_usd": 0.0787,
  "duration_ms": 10276,
  "stop_reason": "end_turn",
  "terminal_reason": "completed",
  "usage": { "input_tokens": 5, "output_tokens": 603, ... },
  "modelUsage": { "the agent-sonnet-4-6": { "costUSD": 0.078, "contextWindow": 200000 } }
}
```

**Key fields:** `session_id` for resumption, `num_turns` for agentic loop count, `total_cost_usd` for spend tracking, `subtype` for success/error detection (`success`, `error_max_turns`, `error_budget`).

### Streaming JSON Output
For real-time token streaming, use `stream-json` with `--verbose`:
```
terminal(command="the agent -p 'Write a summary' --output-format stream-json --verbose --include-partial-messages", timeout=60)
```

Returns newline-delimited JSON events. Filter with jq for live text:
```
the agent -p "Explain X" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

Stream events include `system/api_retry` with `attempt`, `max_retries`, and `error` fields (e.g., `rate_limit`, `billing_error`).

### Bidirectional Streaming
For real-time input AND output streaming:
```
the agent -p "task" --input-format stream-json --output-format stream-json --replay-user-messages
```
`--replay-user-messages` re-emits user messages on stdout for acknowledgment.

### Piped Input
```
# Pipe a file for analysis
terminal(command="cat src/auth.py | the agent -p 'Review this code for bugs' --max-turns 1", timeout=60)

# Pipe multiple files
terminal(command="cat src/*.py | the agent -p 'Find all TODO comments' --max-turns 1", timeout=60)

# Pipe command output
terminal(command="git diff HEAD~3 | the agent -p 'Summarize these changes' --max-turns 1", timeout=60)
```

### JSON Schema for Structured Extraction
```
terminal(command="the agent -p 'List all functions in src/' --output-format json --json-schema '{\"type\":\"object\",\"properties\":{\"functions\":{\"type\":\"array\",\"items\":{\"type\":\"string\"}}},\"required\":[\"functions\"]}' --max-turns 5", workdir="/project", timeout=90)
```

Parse `structured_output` from the JSON result. The agent validates output against the schema before returning.

### Session Continuation
```
# Start a task
terminal(command="the agent -p 'Start refactoring the database layer' --output-format json --max-turns 10 > /tmp/session.json", workdir="/project", timeout=180)

# Resume with session ID
terminal(command="the agent -p 'Continue and add connection pooling' --resume $(cat /tmp/session.json | python3 -c 'import json,sys; print(json.load(sys.stdin)[\"session_id\"])') --max-turns 5", workdir="/project", timeout=120)

# Or resume the most recent session in the same directory
terminal(command="the agent -p 'What did you do last time?' --continue --max-turns 1", workdir="/project", timeout=30)

# Fork a session (new ID, keeps history)
terminal(command="the agent -p 'Try a different approach' --resume <id> --fork-session --max-turns 10", workdir="/project", timeout=120)
```

### Bare Mode for CI/Scripting
```
terminal(command="the agent --bare -p 'Run all tests and report failures' --allowedTools 'Read,Bash' --max-turns 10", workdir="/project", timeout=180)
```

`--bare` skips hooks, plugins, MCP discovery, and AGENTS.md loading. Fastest startup. Requires `ANTHROPIC_API_KEY` (skips OAuth).

To selectively load context in bare mode:
| To load | Flag |
|---------|------|
| System prompt additions | `--append-system-prompt "text"` or `--append-system-prompt-file path` |
| Settings | `--settings <file-or-json>` |
| MCP servers | `--mcp-config <file-or-json>` |
| Custom agents | `--agents '<json>'` |

### Fallback Model for Overload
```
terminal(command="the agent -p 'task' --fallback-model haiku --max-turns 5", timeout=90)
```
Automatically falls back to the specified model when the default is overloaded (print mode only).

## Complete CLI Flags Reference

### Session & Environment
| Flag | Effect |
|------|--------|
| `-p, --print` | Non-interactive one-shot mode (exits when done) |
| `-c, --continue` | Resume most recent conversation in current directory |
| `-r, --resume <id>` | Resume specific session by ID or name (interactive picker if no ID) |
| `--fork-session` | When resuming, create new session ID instead of reusing original |
| `--session-id <uuid>` | Use a specific UUID for the conversation |
| `--no-session-persistence` | Don't save session to disk (print mode only) |
| `--add-dir <paths...>` | Grant The agent access to additional working directories |
| `-w, --worktree [name]` | Run in an isolated git worktree at `.opencode/worktrees/<name>` |
| `--tmux` | Create a tmux session for the worktree (requires `--worktree`) |
| `--ide` | Auto-connect to a valid IDE on startup |
| `--chrome` / `--no-chrome` | Enable/disable Chrome browser integration for web testing |
| `--from-pr [number]` | Resume session linked to a specific GitHub PR |
| `--file <specs...>` | File resources to download at startup (format: `file_id:relative_path`) |

### Model & Performance
| Flag | Effect |
|------|--------|
| `--model <alias>` | Model selection: `sonnet`, `opus`, `haiku`, or full name like `the agent-sonnet-4-6` |
| `--effort <level>` | Reasoning depth: `low`, `medium`, `high`, `max`, `auto` | Both |
| `--max-turns <n>` | Limit agentic loops (print mode only. Prevents runaway) |
| `--max-budget-usd <n>` | Cap API spend in dollars (print mode only) |
| `--fallback-model <model>` | Auto-fallback when default model is overloaded (print mode only) |
| `--betas <betas...>` | Beta headers to include in API requests (API key users only) |

### Permission & Safety
| Flag | Effect |
|------|--------|
| `--dangerously-skip-permissions` | Auto-approve ALL tool use (file writes, bash, network, etc.) |
| `--allow-dangerously-skip-permissions` | Enable bypass as an *option* without enabling it by default |
| `--permission-mode <mode>` | `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions` |
| `--allowedTools <tools...>` | Whitelist specific tools (comma or space-separated) |
| `--disallowedTools <tools...>` | Blacklist specific tools |
| `--tools <tools...>` | Override built-in tool set (`""` = none, `"default"` = all, or tool names) |

### Output & Input Format
| Flag | Effect |
|------|--------|
| `--output-format <fmt>` | `text` (default), `json` (single result object), `stream-json` (newline-delimited) |
| `--input-format <fmt>` | `text` (default) or `stream-json` (real-time streaming input) |
| `--json-schema <schema>` | Force structured JSON output matching a schema |
| `--verbose` | Full turn-by-turn output |
| `--include-partial-messages` | Include partial message chunks as they arrive (stream-json + print) |
| `--replay-user-messages` | Re-emit user messages on stdout (stream-json bidirectional) |

### System Prompt & Context
| Flag | Effect |
|------|--------|
| `--append-system-prompt <text>` | **Add** to the default system prompt (preserves built-in capabilities) |
| `--append-system-prompt-file <path>` | **Add** file contents to the default system prompt |
| `--system-prompt <text>` | **Replace** the entire system prompt (use --append instead usually) |
| `--system-prompt-file <path>` | **Replace** the system prompt with file contents |
| `--bare` | Skip hooks, plugins, MCP discovery, AGENTS.md, OAuth (fastest startup) |
| `--agents '<json>'` | Define custom subagents dynamically as JSON |
| `--mcp-config <path>` | Load MCP servers from JSON file (repeatable) |
| `--strict-mcp-config` | Only use MCP servers from `--mcp-config`, ignoring all other MCP configs |
| `--settings <file-or-json>` | Load additional settings from a JSON file or inline JSON |
| `--setting-sources <sources>` | Comma-separated sources to load: `user`, `project`, `local` |
| `--plugin-dir <paths...>` | Load plugins from directories for this session only |
| `--disable-slash-commands` | Disable all skills/slash commands |

### Debugging
| Flag | Effect |
|------|--------|
| `-d, --debug [filter]` | Enable debug logging with optional category filter (e.g., `"api,hooks"`, `"!1p,!file"`) |
| `--debug-file <path>` | Write debug logs to file (implicitly enables debug mode) |

### Agent Teams
| Flag | Effect |
|------|--------|
| `--teammate-mode <mode>` | How agent teams display: `auto`, `in-process`, or `tmux` |
| `--brief` | Enable `SendUserMessage` tool for agent-to-user communication |

### Tool Name Syntax for --allowedTools / --disallowedTools
```
Read                    # All file reading
Edit                    # File editing (existing files)
Write                   # File creation (new files)
Bash                    # All shell commands
Bash(git *)             # Only git commands
Bash(git commit *)      # Only git commit commands
Bash(npm run lint:*)    # Pattern matching with wildcards
WebSearch               # Web search capability
WebFetch                # Web page fetching
mcp__<server>__<tool>   # Specific MCP tool
```

## Settings & Configuration

### Settings Hierarchy (highest to lowest priority)
1. **CLI flags**: override everything
2. **Local project:** `.opencode/settings.local.json` (personal, gitignored)
3. **Project:** `.opencode/settings.json` (shared, git-tracked)
4. **User:** `~/.opencode/settings.json` (global)

### Permissions in Settings
```json
{
  "permissions": {
    "allow": ["Bash(npm run lint:*)", "WebSearch", "Read"],
    "ask": ["Write(*.ts)", "Bash(git push*)"],
    "deny": ["Read(.env)", "Bash(rm -rf *)"]
  }
}
```

### Memory Files (AGENTS.md) Hierarchy
1. **Global:** `~/.opencode/AGENTS.md`: applies to all projects
2. **Project:** `./AGENTS.md`: project-specific context (git-tracked)
3. **Local:** `.opencode/AGENTS.local.md`: personal project overrides (gitignored)

Use the `#` prefix in interactive mode to quickly add to memory: `# Always use 2-space indentation`.

## Interactive Session: Slash Commands

### Session & Context
| Command | Purpose |
|---------|---------|
| `/help` | Show all commands (including custom and MCP commands) |
| `/compact [focus]` | Compress context to save tokens. AGENTS.md survives compaction. E.g., `/compact focus on auth logic` |
| `/clear` | Wipe conversation history for a fresh start |
| `/context` | Visualize context usage as a colored grid with optimization tips |
| `/cost` | View token usage with per-model and cache-hit breakdowns |
| `/resume` | Switch to or resume a different session |
| `/rewind` | Revert to a previous checkpoint in conversation or code |
| `/btw <question>` | Ask a side question without adding to context cost |
| `/status` | Show version, connectivity, and session info |
| `/todos` | List tracked action items from the conversation |
| `/exit` or `Ctrl+D` | End session |

### Development & Review
| Command | Purpose |
|---------|---------|
| `/review` | Request code review of current changes |
| `/security-review` | Perform security analysis of current changes |
| `/plan [description]` | Enter Plan mode with auto-start for task planning |
| `/loop [interval]` | Schedule recurring tasks within the session |
| `/batch` | Auto-create worktrees for large parallel changes (5-30 worktrees) |

### Configuration & Tools
| Command | Purpose |
|---------|---------|
| `/model [model]` | Switch models mid-session (use arrow keys to adjust effort) |
| `/effort [level]` | Set reasoning effort: `low`, `medium`, `high`, `max`, or `auto` |
| `/init` | Create a AGENTS.md file for project memory |
| `/memory` | Open AGENTS.md for editing |
| `/config` | Open interactive settings configuration |
| `/permissions` | View/update tool permissions |
| `/agents` | Manage specialized subagents |
| `/mcp` | Interactive UI to manage MCP servers |
| `/add-dir` | Add additional working directories (useful for monorepos) |
| `/usage` | Show plan limits and rate limit status |
| `/voice` | Enable push-to-talk voice mode (20 languages. Hold Space to record, release to send) |
| `/release-notes` | Interactive picker for version release notes |

### Custom Slash Commands
Create `.opencode/commands/<name>.md` (project-shared) or `~/.opencode/commands/<name>.md` (personal):

```markdown
# .opencode/commands/deploy.md
Run the deploy pipeline:
1. Run all tests
2. Build the Docker image
3. Push to registry
4. Update the $ARGUMENTS environment (default: staging)
```

Usage: `/deploy production`: `$ARGUMENTS` is replaced with the user's input.

### Skills (Natural Language Invocation)
Unlike slash commands (manually invoked), skills in `.opencode/skills/` are markdown guides that The agent invokes automatically via natural language when the task matches:

```markdown
# .opencode/skills/database-migration.md
When asked to create or modify database migrations:
1. Use Alembic for migration generation
2. Always create a rollback function
3. Test migrations against a local database copy
```

## Interactive Session: Keyboard Shortcuts

### General Controls
| Key | Action |
|-----|--------|
| `Ctrl+C` | Cancel current input or generation |
| `Ctrl+D` | Exit session |
| `Ctrl+R` | Reverse search command history |
| `Ctrl+B` | Background a running task |
| `Ctrl+V` | Paste image into conversation |
| `Ctrl+O` | Transcript mode: see The agent's thinking process |
| `Ctrl+G` or `Ctrl+X Ctrl+E` | Open prompt in external editor |
| `Esc Esc` | Rewind conversation or code state / summarize |

### Mode Toggles
| Key | Action |
|-----|--------|
| `Shift+Tab` | Cycle permission modes (Normal → Auto-Accept → Plan) |
| `Alt+P` | Switch model |
| `Alt+T` | Toggle thinking mode |
| `Alt+O` | Toggle Fast Mode |

### Multiline Input
| Key | Action |
|-----|--------|
| `\` + `Enter` | Quick newline |
| `Shift+Enter` | Newline (alternative) |
| `Ctrl+J` | Newline (alternative) |

### Input Prefixes
| Prefix | Action |
|--------|--------|
| `!` | Execute bash directly, bypassing AI (e.g., `!npm test`). Use `!` alone to toggle shell mode. |
| `@` | Reference files/directories with autocomplete (e.g., `@./src/api/`) |
| `#` | Quick add to AGENTS.md memory (e.g., `# Use 2-space indentation`) |
| `/` | Slash commands |

### Pro Tip: "ultrathink"
Use the keyword "ultrathink" in your prompt for maximum reasoning effort on a specific turn. This triggers the deepest thinking mode regardless of the current `/effort` setting.

## PR Review Pattern

### Quick Review (Print Mode)
```
terminal(command="cd /path/to/repo && git diff main...feature-branch | the agent -p 'Review this diff for bugs, security issues, and style problems. Be thorough.' --max-turns 1", timeout=60)
```

### Deep Review (Interactive + Worktree)
```
terminal(command="tmux new-session -d -s review -x 140 -y 40")
terminal(command="tmux send-keys -t review 'cd /path/to/repo && the agent -w pr-review' Enter")
terminal(command="sleep 5 && tmux send-keys -t review Enter")  # Trust dialog
terminal(command="sleep 2 && tmux send-keys -t review 'Review all changes vs main. Check for bugs, security issues, race conditions, and missing tests.' Enter")
terminal(command="sleep 30 && tmux capture-pane -t review -p -S -60")
```

### PR Review from Number
```
terminal(command="the agent -p 'Review this PR thoroughly' --from-pr 42 --max-turns 10", workdir="/path/to/repo", timeout=120)
```

### The agent Worktree with tmux
```
terminal(command="the agent -w feature-x --tmux", workdir="/path/to/repo")
```
Creates an isolated git worktree at `.opencode/worktrees/feature-x` AND a tmux session for it. Uses iTerm2 native panes when available. Add `--tmux=classic` for traditional tmux.

## Parallel The agent Instances

Run multiple independent The agent tasks simultaneously:

```
# Task 1: Fix backend
terminal(command="tmux new-session -d -s task1 -x 140 -y 40 && tmux send-keys -t task1 'cd ~/project && the agent -p \"Fix the auth bug in src/auth.py\" --allowedTools \"Read,Edit\" --max-turns 10' Enter")

# Task 2: Write tests
terminal(command="tmux new-session -d -s task2 -x 140 -y 40 && tmux send-keys -t task2 'cd ~/project && the agent -p \"Write integration tests for the API endpoints\" --allowedTools \"Read,Write,Bash\" --max-turns 15' Enter")

# Task 3: Update docs
terminal(command="tmux new-session -d -s task3 -x 140 -y 40 && tmux send-keys -t task3 'cd ~/project && the agent -p \"Update README.md with the new API endpoints\" --allowedTools \"Read,Edit\" --max-turns 5' Enter")

# Monitor all
terminal(command="sleep 30 && for s in task1 task2 task3; do echo '=== '$s' ==='; tmux capture-pane -t $s -p -S -5 2>/dev/null; done")
```

## AGENTS.md: Project Context File

the coding agent auto-loads `AGENTS.md` from the project root. Use it to persist project context:

```markdown
# Project: My API

## Architecture
- FastAPI backend with SQLAlchemy ORM
- PostgreSQL database, Redis cache
- pytest for testing with 90% coverage target

## Key Commands
- `make test` — run full test suite
- `make lint` — ruff + mypy
- `make dev` — start dev server on :8000

## Code Standards
- Type hints on all public functions
- Docstrings in Google style
- 2-space indentation for YAML, 4-space for Python
- No wildcard imports
```

**Be specific.** Instead of "Write good code", use "Use 2-space indentation for JS" or "Name test files with `.test.ts` suffix." Specific instructions save correction cycles.

### Rules Directory (Modular AGENTS.md)
For projects with many rules, use the rules directory instead of one massive AGENTS.md:
- **Project rules:** `.opencode/rules/*.md`: team-shared, git-tracked
- **User rules:** `~/.opencode/rules/*.md`: personal, global

Each `.md` file in the rules directory is loaded as additional context. This is cleaner than cramming everything into a single AGENTS.md.

### Auto-Memory
The agent automatically stores learned project context in `~/.opencode/projects/<project>/memory/`.
- **Limit:** 25KB or 200 lines per project
- This is separate from AGENTS.md: it's The agent's own notes about the project, accumulated across sessions

## Custom Subagents

Define specialized agents in `.opencode/agents/` (project), `~/.opencode/agents/` (personal), or via `--agents` CLI flag (session):

### Agent Location Priority
1. `.opencode/agents/`: project-level, team-shared
2. `--agents` CLI flag: session-specific, dynamic
3. `~/.opencode/agents/`: user-level, personal

### Creating an Agent
```markdown
# .opencode/agents/security-reviewer.md
---
name: security-reviewer
description: Security-focused code review
model: opus
tools: [Read, Bash]
---
You are a senior security engineer. Review code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication/authorization flaws
- Secrets in code
- Unsafe deserialization
```

Invoke via: `@security-reviewer review the auth module`

### Dynamic Agents via CLI
```
terminal(command="the agent --agents '{\"reviewer\": {\"description\": \"Reviews code\", \"prompt\": \"You are a code reviewer focused on performance\"}}' -p 'Use @reviewer to check auth.py'", timeout=120)
```

The agent can orchestrate multiple agents: "Use @db-expert to optimize queries, then @security to audit the changes."

## Hooks: Automation on Events

Configure in `.opencode/settings.json` (project) or `~/.opencode/settings.json` (global):

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write(*.py)",
      "hooks": [{"type": "command", "command": "ruff check --fix $AGENT_FILE_PATHS"}]
    }],
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{"type": "command", "command": "if echo \"$AGENT_TOOL_INPUT\" | grep -q 'rm -rf'; then echo 'Blocked!' && exit 2; fi"}]
    }],
    "Stop": [{
      "hooks": [{"type": "command", "command": "echo 'The agent finished a response' >> /tmp/the agent-activity.log"}]
    }]
  }
}
```

### All 8 Hook Types
| Hook | When it fires | Common use |
|------|--------------|------------|
| `UserPromptSubmit` | Before The agent processes a user prompt | Input validation, logging |
| `PreToolUse` | Before tool execution | Security gates, block dangerous commands (exit 2 = block) |
| `PostToolUse` | After a tool finishes | Auto-format code, run linters |
| `Notification` | On permission requests or input waits | Desktop notifications, alerts |
| `Stop` | When The agent finishes a response | Completion logging, status updates |
| `SubagentStop` | When a subagent completes | Agent orchestration |
| `PreCompact` | Before context memory is cleared | Backup session transcripts |
| `SessionStart` | When a session begins | Load dev context (e.g., `git status`) |

### Hook Environment Variables
| Variable | Content |
|----------|---------|
| `AGENT_PROJECT_DIR` | Current project path |
| `AGENT_FILE_PATHS` | Files being modified |
| `AGENT_TOOL_INPUT` | Tool parameters as JSON |

### Security Hook Examples
```json
{
  "PreToolUse": [{
    "matcher": "Bash",
    "hooks": [{"type": "command", "command": "if echo \"$AGENT_TOOL_INPUT\" | grep -qE 'rm -rf|git push.*--force|:(){ :|:& };:'; then echo 'Dangerous command blocked!' && exit 2; fi"}]
  }]
}
```

## MCP Integration

Add external tool servers for databases, APIs, and services:

```
# GitHub integration
terminal(command="the agent mcp add -s user github -- npx @modelcontextprotocol/server-github", timeout=30)

# PostgreSQL queries
terminal(command="the assistant mcp add -s local postgres -- npx @anthropic-ai/server-postgres --connection-string postgresql://localhost/mydb", timeout=30)

# Puppeteer for web testing
terminal(command="the assistant mcp add puppeteer -- npx @anthropic-ai/server-puppeteer", timeout=30)
```

### MCP Scopes
| Flag | Scope | Storage |
|------|-------|---------|
| `-s user` | Global (all projects) | `~/.the agent.json` |
| `-s local` | This project (personal) | `.opencode/settings.local.json` (gitignored) |
| `-s project` | This project (team-shared) | `.opencode/settings.json` (git-tracked) |

### MCP in Print/CI Mode
```
terminal(command="the agent --bare -p 'Query database' --mcp-config mcp-servers.json --strict-mcp-config", timeout=60)
```
`--strict-mcp-config` ignores all MCP servers except those from `--mcp-config`.

Reference MCP resources in chat: `@github:issue://123`

### MCP Limits & Tuning
- **Tool descriptions:** 2KB cap per server for tool descriptions and server instructions
- **Result size:** Default capped. Use `maxResultSizeChars` annotation to allow up to **500K** characters for large outputs
- **Output tokens:** `export MAX_MCP_OUTPUT_TOKENS=50000`: cap output from MCP servers to prevent context flooding
- **Transports:** `stdio` (local process), `http` (remote), `sse` (server-sent events)

## Monitoring Interactive Sessions

### Reading the TUI Status
```
# Periodic capture to check if The agent is still working or waiting for input
terminal(command="tmux capture-pane -t dev -p -S -10")
```

Look for these indicators:
- `❯` at bottom = waiting for your input (The agent is done or asking a question)
- `●` lines = The agent is actively using tools (reading, writing, running commands)
- `⏵⏵ bypass permissions on` = status bar showing permissions mode
- `◐ medium · /effort` = current effort level in status bar
- `ctrl+o to expand` = tool output was truncated (can be expanded interactively)

### Context Window Health
Use `/context` in interactive mode to see a colored grid of context usage. Key thresholds:
- **< 70%**: Normal operation, full precision
- **70-85%**: Precision starts dropping, consider `/compact`
- **> 85%**: Hallucination risk spikes significantly, use `/compact` or `/clear`

## Environment Variables

| Variable | Effect |
|----------|--------|
| `ANTHROPIC_API_KEY` | API key for authentication (alternative to OAuth) |
| `CLAUDE_CODE_EFFORT_LEVEL` | Default effort: `low`, `medium`, `high`, `max`, or `auto` |
| `MAX_THINKING_TOKENS` | Cap thinking tokens (set to `0` to disable thinking entirely) |
| `MAX_MCP_OUTPUT_TOKENS` | Cap output from MCP servers (default varies. Set e.g., `50000`) |
| `CLAUDE_CODE_NO_FLICKER=1` | Enable alt-screen rendering to eliminate terminal flicker |
| `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` | Strip credentials from sub-processes for security |

## Cost & Performance Tips

1. **Use `--max-turns`** in print mode to prevent runaway loops. Start with 5-10 for most tasks.
2. **Use `--max-budget-usd`** for cost caps. Note: minimum ~$0.05 for system prompt cache creation.
3. **Use `--effort low`** for simple tasks (faster, cheaper). `high` or `max` for complex reasoning.
4. **Use `--bare`** for CI/scripting to skip plugin/hook discovery overhead.
5. **Use `--allowedTools`** to restrict to only what's needed (e.g., `Read` only for reviews).
6. **Use `/compact`** in interactive sessions when context gets large.
7. **Pipe input** instead of having The agent read files when you just need analysis of known content.
8. **Use `--model haiku`** for simple tasks (cheaper) and `--model opus` for complex multi-step work.
9. **Use `--fallback-model haiku`** in print mode to gracefully handle model overload.
10. **Start new sessions for distinct tasks**: sessions last 5 hours. Fresh context is more efficient.
11. **Use `--no-session-persistence`** in CI to avoid accumulating saved sessions on disk.

## Pitfalls & Gotchas

1. **Interactive mode REQUIRES tmux**: the coding agent is a full TUI app. Using `pty=true` alone in the agent terminal works but tmux gives you `capture-pane` for monitoring and `send-keys` for input, which is essential for orchestration.
2. **`--dangerously-skip-permissions` dialog defaults to "No, exit"**: you must send Down then Enter to accept. Print mode (`-p`) skips this entirely.
3. **`--max-budget-usd` minimum is ~$0.05**: system prompt cache creation alone costs this much. Setting lower will error immediately.
4. **`--max-turns` is print-mode only**: ignored in interactive sessions.
5. **The agent may use `python` instead of `python3`**: on systems without a `python` symlink, The agent's bash commands will fail on first try but it self-corrects.
6. **Session resumption requires same directory**: `--continue` finds the most recent session for the current working directory.
7. **`--json-schema` needs enough `--max-turns`**: The agent must read files before producing structured output, which takes multiple turns.
8. **Trust dialog only appears once per directory**: first-time only, then cached.
9. **Background tmux sessions persist**: always clean up with `tmux kill-session -t <name>` when done.
10. **Slash commands (like `/commit`) only work in interactive mode**: in `-p` mode, describe the task in natural language instead.
11. **`--bare` skips OAuth**: requires `ANTHROPIC_API_KEY` env var or an `apiKeyHelper` in settings.
12. **Context degradation is real**: AI output quality measurably degrades above 70% context window usage. Monitor with `/context` and proactively `/compact`.

## Rules for the agents

1. **Prefer print mode (`-p`) for single tasks**: cleaner, no dialog handling, structured output
2. **Use tmux for multi-turn interactive work**: the only reliable way to orchestrate the TUI
3. **Always set `workdir`**: keep The agent focused on the right project directory
4. **Set `--max-turns` in print mode**: prevents infinite loops and runaway costs
5. **Monitor tmux sessions**: use `tmux capture-pane -t <session> -p -S -50` to check progress
6. **Look for the `❯` prompt**: indicates The agent is waiting for input (done or asking a question)
7. **Clean up tmux sessions**: kill them when done to avoid resource leaks
8. **Report results to user**: after completion, summarize what The agent did and what changed
9. **Don't kill slow sessions**: The agent may be doing multi-step work. Check progress instead
10. **Use `--allowedTools`**: restrict capabilities to what the task actually needs
