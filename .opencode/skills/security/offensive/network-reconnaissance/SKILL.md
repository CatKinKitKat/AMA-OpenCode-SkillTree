---
name: network-reconnaissance
description: Passive and active network reconnaissance: nmap, masscan, nuclei, subfinder, httpx, ffuf, WhatWeb. Use when mapping the attack surface of a network during an authorized engagement or gathering baseline telemetry for defensive operations.
---
# Network Reconnaissance

Structured network reconnaissance: passive footprinting, active scanning, service enumeration, and web application discovery.

## When to Use

- [done] First 48 hours of an authorized pentest engagement (recon phase)
- [done] Periodic attack-surface monitoring (network drift detection)
- [done] Defensive network mapping (blue team: know your own perimeter)

## Tech Stack

- nmap (TCP/UDP scan, version detection, NSE scripts)
- masscan (fast large-prefix scan)
- subfinder / amass (subdomain enumeration)
- nuclei (CVE scanner, 8000+ templates)
- httpx / ffuf (web probe, directory fuzzing)
- WhatWeb (fingerprinting)

## Workflow

### Phase 1: Passive footprinting

```bash
dig +short example.com A AAAA MX NS
whois example.com | grep -i "registrant"
```

### Phase 2: TCP scan

```bash
nmap -sC -sV -oA recon/light-top-1000 <scope-ips> --top-ports 1000
```

### Phase 3: Full TCP

```bash
nmap -sC -sV -p- -oA recon/full-tcp <scope-ips>
masscan -p1-65535 --rate=10000 <scope-ips> -oL recon/masscan.txt
```

### Phase 4: Service enumeration

Per open port run nmap NSE scripts (http-enum, ssh-auth-methods, ssl-enum-ciphers), WhatWeb, nuclei.

### Phase 5: Web discovery

```bash
subfinder -d example.com -o recon/subs.txt
httpx -l recon/subs.txt -o recon/alive.txt
ffuf -u https://example.com/FUZZ -w wordlist/common.txt -mc 200,301,302
```

## Output

Save to recon/ directory for audit and reproducibility.
