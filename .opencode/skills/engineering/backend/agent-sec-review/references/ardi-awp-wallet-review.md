# Ardi / AWP wallet install review note

Session signal: installing `github.com/awp-worknet/ardi-skill` required external skill/repo review before enabling mining.

Decisive findings:
- `ardi-agent` install path downloads a release binary into `~/.local/bin/ardi-agent`. Binary verified with `ardi-agent --version` and `--help`.
- the agent `agent skills inspect https://github.com/awp-worknet/ardi-skill` did not resolve the GitHub URL, so a safe fallback was manual copy into `~/.agent/skills/web3/ardi` after review.
- `ardi-agent preflight` stopped at `WALLET_NOT_CONFIGURED` when `awp-wallet` was missing.
- `ardi-agent auto-mine` on macOS returned `AUTOMINE_UNSUPPORTED_OS`. Upstream daemon path is Linux/systemd only.
- `awp-wallet` repo review contradicted the safer claim in Ardi docs: current wallet code stores plaintext `privateKey` and optional `mnemonic` in `~/.openclaw-wallet/.../wallet.json`, mode `0600`, and exposes `export-private-key`.

Reusable rule:
- For web3/on-chain skill installs, treat wallet installation, wallet initialization/import, funding, staking, and auto-mining as HIGH risk. Install/read-only binary setup can proceed after review. Stop before wallet creation or transaction-capable daemons unless the user explicitly approves the precise side effects.

Useful commands:
```bash
git clone https://github.com/awp-worknet/ardi-skill /tmp/ardi-skill-review
INSTALL_DIR="$HOME/.local/bin" sh /tmp/ardi-skill-review/install.sh
mkdir -p "$HOME/.agent/skills/web3"
rm -rf "$HOME/.agent/skills/web3/ardi"
cp -R /tmp/ardi-skill-review "$HOME/.agent/skills/web3/ardi"
PATH="$HOME/.local/bin:$PATH" ardi-agent preflight
PATH="$HOME/.local/bin:$PATH" ardi-agent auto-mine
```
