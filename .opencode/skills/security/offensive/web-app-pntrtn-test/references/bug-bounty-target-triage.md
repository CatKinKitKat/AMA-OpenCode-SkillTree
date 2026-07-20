# Bug bounty target triage notes

Use this when the task is not to test one fixed app, but to choose profitable large-vendor bug bounty targets.

## Fast public-source workflow

1. Start with official bounty directories, not search results:
   - HackerOne: `https://hackerone.com/directory/programs?offers_bounties=true`
   - Bugcrowd: `https://bugcrowd.com/engagements`
   - Intigriti: `https://www.intigriti.com/researchers/bug-bounty-programs`
   - Vendor direct: Google Bug Hunters, Apple Security Bounty, Microsoft MSRC, Meta Bug Bounty.
2. Verify each candidate live before recommending it:
   - Browser snapshot for visible program metadata: active/in progress, bounty fields, average payout, reports resolved, scope rating, last updated.
   - Lightweight HTTP status check with Python `urllib.request` if only availability is needed.
3. Rank by earning likelihood, not brand alone:
   - Strong: active bounty, public scope, payout history, high average payout, many resolved reports, broad web/API assets.
   - Weak: VDP only, external listing without bounty fields, private/invite-only scope, vague safe harbor, low/no payout history.
4. Segment recommendations:
   - Tier 1 high-money/high-difficulty: Apple, Google, Microsoft, Meta.
   - Better starting ROI: GitLab, Shopify, Atlassian, PayPal, Coinbase, Tesla, Airbnb/Uber depending on public metrics.
5. Give actionable focus areas per program: IDOR, cross-tenant access, OAuth, SSRF, GraphQL, upload, CI/CD tokens, business logic.

## Pitfalls

- Do not treat an `External` directory listing as proof of platform-managed bounty. Apple on HackerOne can appear as External. Use Apple's official bounty page for reward claims.
- Do not sort only by launch date. For earning, click/sort by average bounty and inspect program pages for current state.
- Do not recommend broad scanning. Tell the user to choose one product line and read scope/exclusions before testing.
- If using shell status checks inside the agent, avoid brittle heredoc+argument composition. Use direct Python execution or a helper script.
