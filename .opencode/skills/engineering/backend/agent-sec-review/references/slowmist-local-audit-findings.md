# SlowMist Local Audit Findings Template

Concrete findings from 2026-05-08 audit of thrill3r's macOS the agent environment.
Use as reference for what a real local audit surfaces and how to classify it.

## Source Frameworks
- `~/tools/security/slowmist-agent-security`: SKILL.md + patterns/ + reviews/ + templates/
- `~/tools/security/openclaw-security-practice-guide`: docs/

## HIGH Findings (2026-05-08)

1. **Redis no-auth on localhost:6379**: `redis-cli ping` returns PONG without password.
   - Fix: `redis-cli CONFIG SET requirepass "<random>"`
   
2. **IB Gateway 10.37 binds `*:4002`**: Trading API on all interfaces.
   - Fix: Configure IB Gateway to bind localhost only. Firewall block 4002.

3. **cliproxyapi binds `*:8317`**: Proxy API on all interfaces.
   - Fix: Configure to bind localhost. Add auth.

4. **11 plaintext `sk-` API keys in config.yaml**: File perms 600 (correct) but keys readable by any skill that opens the file.
   - Fix: Migrate to macOS Keychain. Config.yaml holds keychain references only.

5. **FEISHU_APP_SECRET in env var**: `3K4fvHw...` plaintext in process environment.
   - Fix: Store in keychain or encrypted file. Read at runtime.

6. **Chrome Cookie/Login Data SQLite files**: CDP-enabled browser can read `document.cookie`, `localStorage`. SQLite files locally copyable.
   - Fix: Close Chrome when not in active browser session. CDP access is legitimate but broad.

## MEDIUM Findings

7. **rapportd `*:49343`**: Apple AirDrop/Handoff, all-interfaces.
   - Fix: Disable AirDrop/Handoff when not in use.

8. **the agent red-packet scripts read api_key from config.json**: Scripts themselves are fine, but key storage path must be verified.
   - Fix: Ensure `config.json` perms 600. No hardcoded keys.

9. **BaiduNetdisk localhost:10000**: Local service accessible from CDP browser.
   - Fix: Quit BaiduNetdisk when not in use.

10. **OpenClaw migration residuals world-readable**: `~/.agent/migrations/openclaw-import-*/config/` files perms open.
    - Fix: `chmod 600` the directory. Or delete migration residuals.

11. **DNS fallback 114.114.114.114**: No DNSSEC. Unencrypted fallback when VPN drops.
    - Fix: Replace with 1.1.1.1 or 8.8.8.8 (DoT/DoH capable).

## LOW Findings

12. SSH key perms correct (600/644), no ForwardAgent.
13. No crontab persistence.
14. No `~/.git-credentials`.
15. Shell rc files clean.

## Key Lessons

- Initial grep-based scans produce massive hits. Most are false positives (LaTeX templates, reference docs, skill descriptions about security).
- Deep-dive is mandatory: read actual file content, check binding addresses, verify auth requirements.
- The most dangerous items are services binding `*` (all interfaces) without auth, and plaintext credentials in files/env that the agent skills can read.
- SlowMist's false-positive guidance is critical: "Does the credential access match the stated purpose, and does the data stay within the expected service boundary?"
