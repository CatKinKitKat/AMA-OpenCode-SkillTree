# KYA agent magic-link and delegated-staking flow

Observed workflow on macOS with the agent + awp-wallet + Ardi.

## Trigger
- User gives `kya-sign://twitter-claim` or `kya-sign://email-claim?email=...` and asks to pull latest `https://github.com/awp-worknet/kya-skill`.
- Goal is usually KYA delegated staking for another worknet such as Ardi.

## Safe sequence
1. Pull or clone `~/kya-skill` from `https://github.com/awp-worknet/kya-skill`.
2. Inspect/read `README.md`, `SKILL.md`, `install.sh`, `src/wallet.rs`, `src/magiclink.rs`, and `Cargo.toml` before trusting it.
3. Install `kya-agent` via `install.sh` if release download works.
4. If release download fails with TLS/GitHub release-assets errors, build locally:
   ```bash
   cd ~/kya-skill
   cargo build --release
   mkdir -p ~/.local/bin
   cp target/release/kya-agent ~/.local/bin/kya-agent
   ```
5. Verify:
   ```bash
   PATH="$HOME/.local/bin:$HOME/.npm-global/bin:$PATH" kya-agent --version
   PATH="$HOME/.local/bin:$HOME/.npm-global/bin:$PATH" kya-agent preflight
   ```
6. For any magic link, dry-run first:
   ```bash
   kya-agent open --dry-run 'kya-sign://twitter-claim'
   kya-agent open --dry-run 'kya-sign://email-claim?email=name%40example.com'
   ```
7. Then execute with `kya-agent open '<magic link>'` only for one-shot web handoff flows. For email, prefer the PTY flow below.

## Twitter claim behavior
- `kya-agent open 'kya-sign://twitter-claim'` signs two KYA actions and returns a `handoff_url`.
- Relay `handoff_url` verbatim to the user.
- Do not ask user to paste a tweet URL back. KYA web handles tweet/post and claim submission.
- After user says browser flow is done, run `kya-agent attestations`.

## Email claim behavior
Important pitfall: `kya-agent claim-email --email X --code NNNNNN` performs a fresh `email_prepare` before confirming, so a code from a previous prepare may be invalidated or mismatched. Do not use the non-interactive two-command resume unless the upstream CLI changes.

Correct the agent flow:
1. Start an interactive PTY and let it stop at the code prompt:
   ```bash
   PATH="$HOME/.local/bin:$HOME/.npm-global/bin:$PATH" kya-agent claim-email --email user@example.com
   ```
2. Wait for output containing `Verification code (6 digits):`.
3. Use `clarify` to ask the user for the 6-digit code.
4. Submit the code to the same background PTY/process, not a new `claim-email --code` process.
5. Wait for `confirm.ok` and then run:
   ```bash
   kya-agent attestations
   ```

Why: the single interactive process runs `email_prepare`, waits for the code, then runs `email_confirm` without re-preparing. Starting a new non-interactive process can send a new email and make the user's current code stale.

## Address resolution
- Default agent address comes from current `awp-wallet` profile:
  ```bash
  awp-wallet receive
  ```
- In the observed session the address was `0x270fB39E708a742b9523403597780decd7e92707`. Do not hardcode it for future users.

## Notes
- KYA preflight requires AWP registration. Ardi preflight can gaslessly register the same awp-wallet address before KYA.
- KYA itself signs via `awp-wallet sign-typed-data` and posts to KYA/AWP endpoints. It does not require Base ETH for claim flows.
- Email attestations can become active, but KYA delegated staking still requires active `twitter_claim` in current KYA behavior. `email_claim` alone returns `qualifies_for_delegated_staking: false`.
