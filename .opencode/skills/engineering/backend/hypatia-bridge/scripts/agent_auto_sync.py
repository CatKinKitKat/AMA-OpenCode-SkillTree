#!/usr/bin/env python3
from pathlib import Path
import runpy

runpy.run_path(str(Path('~/Downloads/agent-hacks/agent-hypatia-bridge/agent_auto_sync.py').expanduser()), run_name='__main__')
