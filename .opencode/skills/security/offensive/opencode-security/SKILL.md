---
name: security-audit
description: Audits codebases for security vulnerabilities across 11 domains — secrets, database, auth, payments, mobile, AI/LLM, deployment, data access, API, and CI/CD
version: 1.0.0
license: MIT
metadata: 
author: azizaeffendi
tags: [security, audit, owasp, supabase, firebase, stripe, nextjs, react-native, jwt, rls, ai-safety, cicd, api-security]
category: security
requires_toolsets: [terminal]
fallback_for_toolsets: [web]
---


Audit code for security vulnerabilities across 11 domains. Covers every pattern AI coding assistants consistently get wrong: from hardcoded secrets to disabled database access control, from missing webhook verification to prompt injection vulnerabilities.

Load only the reference files relevant to the tech stack being audited. Skip domains that don't apply.


## The Core Principle

**Never trust the client.** Every price, user ID, role, subscription status, and rate limit counter must be validated server-side. If it only exists in the browser, mobile bundle, or request body: an attacker controls it.


## When to Use

Trigger this skill whenever:

- User invokes: `/security-audit`, `$security-audit`
- User asks: "audit my code", "is this secure?", "check for vulnerabilities", "is this safe to ship?", "scan for security issues", "can someone hack this?"
- Writing or reviewing code that touches: authentication, payments, database queries, API keys, secrets, user data
- Any Supabase RLS configuration, Firebase security rules, or Convex auth guards
- Any Stripe webhook, checkout session, or subscription logic
- Any React Native / Expo app handling tokens, secrets, or deep links
- Any endpoint calling an AI API (OpenAI, Anthropic, Google AI)
- CI/CD pipeline configuration files (`.github/workflows/*.yml`, `gitlab-ci.yml`)
- Before a production deployment or security review


## Quick Reference

```bash
# ── SECRETS ──────────────────────────────────────────────────────────
gitleaks detect --source . --verbose --no-banner
grep -rE "NEXT_PUBLIC_.*(SECRET|KEY|TOKEN)" . --include="*.ts"
git ls-files | grep -E "\.env$|\.env\."

# ── DATABASE ──────────────────────────────────────────────────────────
# Supabase: tables without RLS (run in SQL Editor)
SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND rowsecurity = false;
# Find dangerous "allow all" policies
grep -rn "USING (true)\|allow read: if true\|allow write: if true" .

# ── AUTHENTICATION ────────────────────────────────────────────────────
grep -rn "jwt\.decode\b" . --include="*.ts" --include="*.js"
grep -rn "localStorage.*token\|localStorage.*auth" . --include="*.ts"

# ── PAYMENTS ──────────────────────────────────────────────────────────
grep -rn "unit_amount.*body\|price.*req\.body" . --include="*.ts"
grep -rn "constructEvent" . --include="*.ts"   # must be present

# ── AI / LLM ──────────────────────────────────────────────────────────
grep -rn "NEXT_PUBLIC_OPENAI\|NEXT_PUBLIC_ANTHROPIC" . --include="*.ts"
grep -rn "dangerouslyAllowBrowser.*true" . --include="*.ts"

# ── DEPLOYMENT ────────────────────────────────────────────────────────
curl -si https://your-domain.com/.git/HEAD | head -1
curl -si https://your-domain.com | grep -i "strict-transport\|x-frame"

# ── CI/CD ─────────────────────────────────────────────────────────────
grep -rn "echo.*SECRET\|echo.*TOKEN\|echo.*KEY" .github/workflows/
```


## Audit Process

Work through each domain systematically. Load the reference file only when the codebase uses that technology.

**01: Secrets & Environment Variables**
Scan for hardcoded credentials. Check for secrets leaked via client-side env var prefixes (`NEXT_PUBLIC_`, `VITE_`, `EXPO_PUBLIC_`). Verify `.env` is in `.gitignore`.
→ Load: `references/secrets-and-env.md`

**02: Database Access Control**
The #1 vulnerability source. Check Supabase RLS, Firebase Security Rules, Convex auth guards. Verify no `USING (true)`, no missing `WITH CHECK`, no `service_role` on client.
→ Load: `references/database-security.md`

**03: Authentication & Authorization**
Check JWT handling (`verify` not `decode`), middleware-only auth gaps, unprotected Server Actions, session storage. Every action needs: validate → authenticate → authorize.
→ Load: `references/authentication.md`

**04: Rate Limiting & Abuse Prevention**
Verify rate limits on auth, AI, email, SMS, and file endpoints. Check rate counters are not in public Supabase tables. Verify billing caps are set.
→ Load: `references/rate-limiting.md`

**05: Payment Security**
Check for client-submitted prices. Verify webhook uses `constructEvent` with raw body. Verify subscription status is checked from DB, not session/JWT.
→ Load: `references/payments.md`

**06: Mobile Security**
Check for secrets in JS bundle. Verify `expo-secure-store` / `react-native-keychain` used instead of `AsyncStorage`. Check deep link parameter validation.
→ Load: `references/mobile.md`

**07: AI / LLM Integration**
No AI API keys client-side. Hard spending caps set. User input in separate message role. LLM output sanitized before render. Tool call parameters validated.
→ Load: `references/ai-integration.md`

**08: Deployment Configuration**
Debug mode off, source maps off, `.git` not public, security headers set, CORS restricted to own domains. Secrets separated by environment.
→ Load: `references/deployment.md`

**09: Data Access & Input Validation**
No `$queryRawUnsafe`. No Prisma with raw request body as WHERE. Input validated with Zod/Yup at every boundary. No mass assignment spread. IDOR checks on every query.
→ Load: `references/data-access.md`

**10: API Security**
All endpoints require auth. No GraphQL introspection in production. CORS restricted. No IDOR via object ID traversal. Input schema validated on all endpoints.
→ Load: `references/api-security.md`

**11: CI/CD Pipeline Security**
No secrets echoed in workflow steps. Pinned action versions. Protected branches. Secrets only via `${{ secrets.NAME }}`. No untrusted code in pipelines.
→ Load: `references/cicd-security.md`


## Core Instructions

- Report only genuine security vulnerabilities. Do not flag style, performance, or non-security concerns.
- Prioritize by real-world exploitability and blast radius, not theoretical severity.
- If the codebase doesn't use a technology (e.g., no Stripe), skip that domain entirely.
- When generating new code, proactively check the relevant reference file before writing code that touches auth, payments, database, or user data.
- If a Critical issue is found (exposed secrets, disabled RLS, auth bypass), flag it at the **top** of the response before all other findings.


## Output Format

Organize by severity: **Critical → High → Medium → Low**

For each finding:
1. File path and line number
2. Vulnerability name
3. Concrete attacker impact (what can they actually do?)
4. Before/After code fix

Skip domains with no issues. End with a prioritized summary table.

### Severity Definitions

| Severity | Criteria |
|: : : : : |: : : : -|
| 🔴 Critical | Exploitable remotely, no auth required, immediate data loss or account takeover risk |
| 🟠 High | Exploitable with minimal effort, significant data or financial impact |
| 🟡 Medium | Requires some conditions, moderate impact |
| 🔵 Low | Defense-in-depth improvement, low direct impact |


## Pitfalls

Common mistakes to avoid during security audits:

- **`SECURITY DEFINER` Postgres functions bypass RLS** entirely: check `SELECT proname FROM pg_proc WHERE prosecdef = true`
- **Next.js middleware can be bypassed** via `x-middleware-subrequest` header (CVE-2025-29927): never treat it as the final auth gate
- **`service_role` without `NEXT_PUBLIC_` is still dangerous** if consumed client-side: check where the variable is used, not just its name
- **Webhook "verified" can still be replayed**: check for idempotency handling, not just `constructEvent`
- **Rate limiting only on `/login`**: always check `/register`, `/forgot-password`, `/resend-otp`, and all AI endpoints too
- **Missing `WITH CHECK`** on Supabase UPDATE/INSERT allows ownership transfer even with correct `USING` clause
- **`parseInt()` is not input validation**: `parseInt("1; DROP TABLE", 10)` returns `1`
- **TypeScript types don't exist at runtime**: they protect nothing from malformed API requests


## Verification

After applying fixes, run these to confirm resolution:

```bash
# Secrets clean
gitleaks detect --source . --no-banner
# → "No leaks found"

# RLS on all tables (Supabase SQL Editor)
SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND rowsecurity = false;
# → 0 rows

# No jwt.decode
grep -rn "jwt\.decode\b" . --include="*.ts"
# → no output

# Security headers present
curl -si https://your-domain.com | grep -iE "strict-transport|x-frame|content-security"
# → all 3 headers present

# .git not public
curl -s -o /dev/null -w "%{http_code}" https://your-domain.com/.git/HEAD
# → 403 or 404
```


## References

- `references/secrets-and-env.md`: API keys, env prefixes, `.gitignore`, detection commands
- `references/database-security.md`: Supabase RLS, Firebase rules, Convex auth, service_role
- `references/authentication.md`: JWT, middleware bypass, Server Actions, session storage
- `references/rate-limiting.md`: Rate limit strategies, Upstash patterns, billing protection
- `references/payments.md`: Stripe security, webhook verification, price validation
- `references/mobile.md`: React Native/Expo: secure storage, backend proxy, deep links
- `references/ai-integration.md`: LLM API protection, prompt injection, output sanitization
- `references/deployment.md`: Production config, security headers, environment separation
- `references/data-access.md`: SQL injection, ORM safety, mass assignment, IDOR
- `references/api-security.md`: REST/GraphQL auth, CORS, object-level authorization
- `references/cicd-security.md`: GitHub Actions secrets, pipeline security, supply chain
