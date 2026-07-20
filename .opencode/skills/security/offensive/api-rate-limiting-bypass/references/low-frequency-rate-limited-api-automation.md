# Low-frequency automation for rate-limited challenge APIs

Session pattern: a web app exposed proof-of-work endpoints:
- `GET /api/mining/challenge`
- `POST /api/mining/submit`
- `POST /api/auth/login`

The user asked whether to bypass rate limits or go directly to chain/contracts. Static frontend inspection found no Web3/RPC/ethers/metamask/contract address strings. The app was a centralized API with site-internal contracts. The safe operational path was low-frequency automation that respects 429 responses rather than evasion.

Architecture triage:

```bash
python3 - <<'PY'
import re
s=open('/tmp/app.js').read()
for term in ['ethereum','web3','ethers','rpc','chain','metamask','solidity','contractAddress']:
    print(term, len(list(re.finditer(re.escape(term), s, re.I))))
print(sorted(set(re.findall(r'"(/api/[^"`]+)"', s))))
PY
```

Low-frequency miner pattern:
- authenticate once, but retry login after 401/403
- fetch challenge slowly
- skip challenges above local cost threshold (`difficulty > 4` in this case)
- compute proof locally: `sha256(prefix + str(nonce)).hexdigest().startswith('0' * difficulty)`
- submit once per challenge
- on 429, exponential or wide random backoff (minutes, not seconds)
- log every request, response code, selected challenge, sleep, and submission

Operational pitfall:
- if the helper runs in a the agent background process, stdout may appear empty even while healthy. Add explicit file logging and run with `python3 -u`
- a background terminal command may have a bash wrapper PID and a separate Python child PID. Inspect the child for real state

Decision rule:
- If the goal is security testing of rate-limit bypass, stay within written authorization and bounded request volumes.
- If the goal is normal participation in a rate-limited challenge service, do not use bypass techniques. Use low-frequency scheduling, backoff, and cost filtering.
