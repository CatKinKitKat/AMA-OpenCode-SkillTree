# MoonPay no-account skill supply-chain triage

Session pattern: scope CSV has an eligible org-level `SOURCE_CODE` row plus later repo-specific rows marked ineligible. For source-first bounty work, treat explicit repo rows as overrides and prioritize non-archived repos under the eligible org that are not separately excluded.

## Scope handling

MoonPay CSV pattern observed:
- Eligible org source root: `https://github.com/moonpay`
- Explicitly ineligible repos: `moonpay-sign`, `moonpay-demo-integrations`, `devops-challenge`
- Non-archived org repos from GitHub API included: `moonpay/skills`, plus the explicitly ineligible repos above

Conservative route:
1. Parse CSV first.
2. If an org-level source row is eligible, enumerate org repos via GitHub API.
3. Remove archived repos.
4. Remove repos that have explicit ineligible rows in the CSV.
5. Audit the remaining repos first.

Useful command:
```bash
python3 - <<'PY'
import json, urllib.request
org='moonpay'
repos=[]
for page in range(1,6):
    data=json.load(urllib.request.urlopen(f'https://api.github.com/orgs/{org}/repos?per_page=100&page={page}'))
    if not data: break
    repos += data
for r in repos:
    if not r.get('archived'):
        print(f"{r['name']}\t{r.get('language')}\tstars={r['stargazers_count']}\tupdated={r['updated_at']}\t{r['html_url']}")
PY
```

## Agent skill supply-chain checks

For repositories containing AI-agent skills, add these sweeps after normal `exec/eval` checks:
- `curl`
- `curl -sSL`
- `| sh`, `| bash`
- `install:` frontmatter
- remote `http://` URLs
- instructions that fetch remote markdown or scripts before execution

Risk pattern:
```bash
curl -sSL http://example.tld/install.sh | sh
```

Even if the live server currently returns `301` to HTTPS, the first hop is plaintext HTTP. A network attacker can intercept that first request and return a malicious shell script instead of the redirect. Because the command pipes directly to `sh`, this is a no-account code-execution supply-chain issue.

## MoonPay finding candidate

Asset:
- `https://github.com/moonpay` -> `moonpay/skills`

File:
- `skills/allium-x402/SKILL.md`

Observed unsafe command:
```bash
curl -sSL http://agents.allium.so/cli/install.sh | sh
```

Live behavior at time of triage:
```text
HTTP/1.1 301 Moved Permanently
Location: https://agents.allium.so:443/cli/install.sh
```

Classification:
- Weakness: `Download of Code Without Integrity Check (CWE-494)`
- Better than CWE-78 unless there is a separate shell metacharacter injection path.
- Severity: usually Medium. Consider High only if the agent skill is expected to be auto-installed or executed in an environment with wallet, signing, or deployment privileges.

Safe PoC idea:
- Do not execute a remote attacker server in the report.
- Demonstrate the trust boundary by showing the exact plaintext HTTP first-hop command and current 301.
- Explain that a MITM can replace the response body with:
```sh
#!/bin/sh
touch /tmp/moonpay-skill-poc
```

## Pitfalls

- Do not spend time on repo-specific ineligible rows first when the CSV has a broader eligible org source row.
- Do not report demo/example repos if the CSV explicitly marks them ineligible, even if they contain attractive issues.
- Do not overclaim `curl | sh` over HTTPS alone. The high-signal issue here is plaintext HTTP first hop plus direct shell execution and no integrity pin.
