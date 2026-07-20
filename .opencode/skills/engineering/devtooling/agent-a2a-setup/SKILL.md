---
name: agent-a2a-setup
description: >
tags: 
version: 1
---


## agent-a2a Plugin Setup

Source repo: agent-a2a (iamagenius00 on GitHub)

the agent plugin for peer-to-peer agent communication via Google's A2A protocol.
Zero external dependencies, pure Python stdlib.

### Prerequisites

- the agent v2026.4.23+ (plugin API with register_command)
- CLI mode only (gateway does NOT load plugins)

### Install Steps

1. Clone repo and run install.sh: copies 7 files to plugins directory
2. CRITICAL: Run `agent plugins enable a2a`: plugins are opt-in
3. Set A2A_ENABLED=true and A2A_PORT=8081 in environment
4. Restart CLI session (plugin loads at session start)

### Pitfall: Plugin Must Be Explicitly Enabled

The plugin system requires explicit enablement. After install, run:

```
agent plugins enable a2a
```

Without this, the plugin is discovered but NOT loaded.
User plugins are opt-in: only bundled backends auto-load.

### Pitfall: Gateway Does NOT Load Plugins

Only CLI mode supports A2A. Gateway (Telegram/Discord/Feishu) won't start the A2A server.
Plugin hooks only fire in CLI conversation loop.

### Tools Exposed

| Tool | Description |
|: : : |: : : : : : -|
| a2a_discover | Check remote agent's Agent Card |
| a2a_call | Send message to remote agent |
| a2a_list | List configured remote agents |

### Configuring Remote Agents

Add entries under a2a.agents in config yaml:

```yaml
a2a:
  agents:
    - name: "friend"
      url: "https://friend-a2a-endpoint.example.com"
      description: "My friend's agent"
      auth_token: "their-bearer-token"
```

### Security

- Bearer token auth (localhost-only without token)
- 20 req/min rate limit per IP
- 9 prompt injection patterns filtered
- Outbound secrets redacted
- Audit log at a2a_audit.jsonl

### Architecture

Remote Agent sends A2A JSON-RPC to localhost:8081
  → task_queue.enqueue()
  → webhook trigger fires agent turn
  → pre_llm_call hook injects message into current session
  → agent replies with full context
  → post_llm_call captures response
  → response returned synchronously (120s timeout)
  → exchange persisted to a2a_conversations/

### Files

| File | Purpose |
|: : : |: : : : -|
| __init__.py | Entry point, registers hooks/tools/server |
| server.py | A2A HTTP server + webhook + task queue |
| tools.py | a2a_discover, a2a_call, a2a_list |
| security.py | Injection filtering, redaction, rate limit |
| persistence.py | Saves conversations to disk |
| schemas.py | Tool schemas |
| plugin.yaml | Plugin manifest |

### Routing Keywords (in skill-router.md)

A2A agent 对话、agent 间通信、给别的 agent 发消息 → A2A 插件
