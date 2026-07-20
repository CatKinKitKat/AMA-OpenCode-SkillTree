---
name: agent-mcp-self-heal
description: Use when the agent MCP servers show failed or disconnected behavior and need structured self-heal: test each server, verify the backing listener or command, repair launchd persistence, and retest from the agent.
version: 1.0.0
author: the agent
license: MIT
metadata: 
tags: [agent, mcp, launchd, debugging, browser, anything-analyzer, openchronicle]
related_skills: [agent-runtime, systmt-dbggng, anything-analyzer-mcp, badboy-br-aa-routing]
---


# the agent MCP Self-Heal

## Overview

Use this when the agent shows an MCP server as failed, disconnected, or unusable.
Goal: repair the backing service first, then prove the agent can connect again.

Default environment assumed here:
- macOS
- the agent config at `~/.agent/config.yaml`
- MCP services may be stdio, HTTP, or launchd-backed local daemons

## When to Use

Trigger on asks like:
- `mcp failed`
- `mcp 挂了`
- `mcp 连不上`
- `修 mcp`
- `mcp 自愈`
- `openchronicle failed`
- `anything-analyzer failed`
- `browser-relay failed`
- `badboy-browser failed`
- `open-computer-use failed`
- `launchctl`
- `LaunchAgent`
- `后台常驻`
- `开机自启`

Load companion skills when relevant:
- `autonomous-ai-agents/agent-runtime` for the agent config/CLI truth
- `software-development/systmt-dbggng` for structured root-cause flow
- `devops/anything-analyzer-mcp` for AA/headless/MITM specifics
- `devops/badboy-br-aa-routing` for real-Chrome/CDP/browser routing

## Core Rule

Do not patch the agent config first.
First prove whether the backing service, listener, or executable is actually down.

When the user's goal is deliberate teardown/minimization rather than repair, switch modes explicitly:
- inspect the current `mcp_servers:` block and active launchd jobs first
- disable unwanted servers in `~/.agent/config.yaml`
- stop the backing daemons and boot out matching LaunchAgents
- verify the remaining enabled set with `agent mcp list`
- only then chase residual processes that should no longer exist

## Self-Heal Order

1. List configured MCP servers.
2. Test each failed server directly from the agent.
3. Inspect the exact backend:
   - HTTP server -> listener/health endpoint
   - stdio command -> binary path/help/test
   - launchd-backed service -> plist, logs, launchctl state
4. Repair the backend service.
5. Retest from the agent.
6. If the service must survive reboot/login, add or patch a per-user LaunchAgent.

## Minimal Command Set

### 1. Enumerate and test
```bash
agent mcp list
agent mcp test <name>
```

### 2. Inspect the agent config slice
Read `~/.agent/config.yaml` around `mcp_servers:` and confirm:
- `url` or `command`
- `args`
- `env`
- `headers`
- `timeout` / `connect_timeout`

### 3. HTTP MCP checks
```bash
lsof -nP -iTCP:<port> -sTCP:LISTEN || true
curl -sS -D - -o /dev/null -H 'Accept: application/json, text/event-stream' http://127.0.0.1:<port>/mcp || true
```

### 4. stdio MCP checks
```bash
ls -l <binary>
<binary> --help
agent mcp test <name>
```

### 5. launchd checks
```bash
launchctl print gui/$(id -u)/<label> | sed -n '1,140p'
tail -n 80 <stdout-log> 2>/dev/null || true
tail -n 80 <stderr-log> 2>/dev/null || true
```

### 6. launchd reload
```bash
launchctl bootout gui/$(id -u) "$HOME/Library/LaunchAgents/<label>.plist" >/dev/null 2>&1 || true
launchctl bootstrap gui/$(id -u) "$HOME/Library/LaunchAgents/<label>.plist"
launchctl kickstart -k gui/$(id -u)/<label>
```

## Known Local Truths

### OpenChronicle
- the agent URL: `http://127.0.0.1:8742/mcp`
- Local binary: `~/.local/bin/openchronicle`
- Persistence plist: `~/Library/LaunchAgents/com.thrill3r.openchronicle.plist`
- If failed, first run:
```bash
openchronicle status
openchronicle start
agent mcp test openchronicle
```
- Root cause already seen live: daemon stopped -> no listener on 8742.

### anything-analyzer
- the agent URL: `http://localhost:23816/mcp`
- Persistence plist: `~/Library/LaunchAgents/com.anything-analyzer.dev.plist`
- Must keep headless/no-UI unless user explicitly asks otherwise.
- Check 23816 listener before touching config.

### browser-relay
- Backing LaunchAgent: `~/Library/LaunchAgents/com.liaotechs.browser-relay.plist`
- Typical listener: `127.0.0.1:18795`
- the agent side is stdio wrapper. Verify both listener and `agent mcp test browser-relay`.

### badboy-browser
- the agent side uses shell wrapper + env injection.
- Transport may pass even when runtime emits harmless asyncio shutdown noise.
- Success criterion is `agent mcp test badboy-browser` discovering tools, not zero stderr noise.

### open-computer-use
- Usually stdio only.
- Verify executable path first. Then `agent mcp test open-computer-use`.

## LaunchAgent Pattern

For durable local MCP services on macOS, prefer per-user LaunchAgents:
- file under `~/Library/LaunchAgents/`
- `RunAtLoad`
- `KeepAlive`
- explicit `PATH`
- explicit logs under `~/Library/Logs/`

Use listener guards if the underlying CLI exits non-zero when already running.
Observed example: `openchronicle start` returns exit code 1 when daemon already exists, so a guard like `lsof ... || start` prevents launchd restart churn.

## Verification Checklist

- [ ] `agent mcp list` shows target enabled
- [ ] `agent mcp test <name>` succeeds after repair
- [ ] backing listener or stdio binary was directly verified
- [ ] if launchd-backed, plist path and `launchctl print` were checked
- [ ] if persistent service needed, LaunchAgent exists and reload command works
- [ ] final result proven from the agent side, not only backend side

## Common Pitfalls

1. Patching `~/.agent/config.yaml` before checking whether the backend daemon is simply down.
2. Missing the teardown case: if the user wants MCPs gone, leaving `enabled: true` on `agent`, `browser-relay`, `badboy-browser`, `anything-analyzer`, or `openchronicle` guarantees they can come back after reload/restart.
3. Treating noisy stderr as failure when `agent mcp test` already proves tool discovery works.
4. Forgetting `Accept: application/json, text/event-stream` on HTTP MCP probes.
5. Using ad-hoc shell backgrounding instead of launchd for services meant to persist.
6. For AA tasks, accidentally opening UI/Electron despite user preference for hidden/headless mode.
7. Declaring success because a port listens, without retesting from the agent.
8. Killing child MCP processes without checking the parent chain. A surviving parent `agent mcp serve` can recursively respawn `browser-relay-mcp-line`, `agent_context_server.py`, and more `agent mcp serve` children.
