Hypatia bridge local assets

Workspace
- ~/Downloads/agent-hacks/agent-hypatia-bridge/

Bridge CLI
- python3 ~/Downloads/agent-hacks/agent-hypatia-bridge/agent_hypatia.py add-note "Name" "Body" --tags a,b
- python3 ~/Downloads/agent-hacks/agent-hypatia-bridge/agent_hypatia.py search "query"
- python3 ~/Downloads/agent-hacks/agent-hypatia-bridge/agent_hypatia.py add-statement the agent uses Hypatia --data "external memory backend"
- python3 ~/Downloads/agent-hacks/agent-hypatia-bridge/agent_hypatia.py query-triple the agent uses Hypatia

Sync helper
- python3 ~/Downloads/agent-hacks/agent-hypatia-bridge/agent_memory_sync.py add-memory user persona "Default terse Wenyan mode"
- python3 ~/Downloads/agent-hacks/agent-hypatia-bridge/agent_memory_sync.py add-fact the agent uses Hypatia --data "external memory backend"

Semi-auto wrapper
- python3 ~/Downloads/agent-hacks/agent-hypatia-bridge/agent_auto_sync.py memory user persona "Default terse Wenyan mode"
- python3 ~/Downloads/agent-hacks/agent-hypatia-bridge/agent_auto_sync.py fact the agent uses Hypatia --data "external memory backend"
- python3 ~/Downloads/agent-hacks/agent-hypatia-bridge/agent_auto_sync.py memory memory long_term_rule "Prefer direct execution" --sync no
