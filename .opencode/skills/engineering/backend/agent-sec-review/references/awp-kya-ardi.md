# AWP / KYA / Ardi external skill install notes

Session-derived operational notes for reviewing and running AWP-family external skills (`ardi-skill`, `kya-skill`, `awp-wallet`). Treat these repos as external code and on-chain flows even when the README says gasless/no funds.

## Trust / install findings
- `ardi-skill` installs `ardi-agent` into `~/.local/bin` from GitHub releases. Its runtime signs/broadcasts Base mainnet transactions through `awp-wallet send-tx`.
- `kya-skill` installs `kya-agent`. Release downloads can fail on GitHub TLS/redirects, so local `cargo build --release` plus copying `target/release/kya-agent` to `~/.local/bin` is a valid fallback when Rust is present.
- `awp-wallet` (observed v1.5.0) stores plaintext wallet material at `~/.openclaw-wallet/wallets/default/wallet.json` with mode `0600`, including `privateKey` and often `mnemonic`. It also exposes `export-private-key`. Treat wallet installation/init as HIGH risk and require explicit user approval.
- `ardi-agent preflight` can gaslessly register the EOA on AWP before failing later on Base ETH balance.

## KYA email claim pitfall
- Non-TTY `kya-agent claim-email --email X --code NNNNNN` runs `email_prepare` again before `email_confirm`, which can invalidate the code the user just supplied.
- Correct no-duplicate flow: start `kya-agent claim-email --email X` in a PTY/background process, wait until it prints `Verification code (6 digits):`, ask the user for the code, then submit the code to the same process.
- Do not retry with `--code` after a prepare unless the user has the latest code for that prepare.

## KYA X / delegated staking checks
- `kya-agent attestations --type twitter_claim` only treats `status: active` as verified. KYA web can show a friendly `Verified` while the API record is still `pending`. Recheck until active.
- Direct status probe: `https://kya.link/v1/agents/<address>/attestations?type=twitter_claim` shows raw status, proof tweet, metadata, and timestamps.
- For delegated staking, `kya-agent set-recipient --worknet <ID> --amount 10000` first ensures AWP recipient is KYA deposit, then signs `delegated_staking_request`.
- If recipient is already set, stage 1 is skipped with `recipient_already_set`. This is normal.
- Worknet catalog behavior observed: `845300000003` and `845300000012` were in catalog but rejected by global cap. `845300000002`, `845300000010`, `845300000011`, `845300000013`, `845300000014` returned `UNKNOWN_WORKNET`.
- `UNKNOWN_WORKNET` from delegated staking means the target worknet is not in KYA's server catalog. It is not a local install/wallet issue and does not include a future availability time.
- `global delegated-staking cap reached` means the worknet is recognized but KYA capacity is exhausted. The observed response did not include a retry-after or next-available timestamp. Report that directly instead of inventing a schedule.

## Ardi mining on macOS
- `ardi-agent auto-mine` in v0.5.17 returns `AUTOMINE_UNSUPPORTED_OS` on macOS and points to manual cycle, despite some docs mentioning `loop` as no-systemd fallback.
- Manual cycle can be agent-operated: `ardi-agent preflight` -> stake/gas fixes -> `ardi-agent context` -> solve riddles -> serial `commit` -> wait -> `commits` -> `reveal` -> `inscribe`.
- Never fire Ardi commits in parallel. Nonce/state handling requires serial commits.
