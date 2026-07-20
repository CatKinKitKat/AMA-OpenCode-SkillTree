# Public bounty directory triage

Use when choosing bounty targets before logging in or testing assets.

## Scope guard

- Do not use user-provided passwords for triage. Public metadata is enough.
- Do not submit probes against assets until a specific program scope is read and recorded.
- If the user asks to "go make money" without a target, default to public ROI triage, not blind scanning.

## HackerOne public directory

URL: `https://hackerone.com/directory/programs?offers_bounties=true`

Public fields visible without login:
- program name and handle link
- launch date
- reports resolved
- minimum bounty
- average bounty range
- feature tags such as Managed, Retesting, Collaboration

Useful browser-console extraction after sorting by average bounty:

```js
Array.from(document.querySelectorAll('table tr')).slice(1,26).map(tr => {
  const a = tr.querySelector('a');
  const cells = Array.from(tr.cells).map(td => td.innerText.trim());
  return {
    program: cells[0]?.split('\n')[0],
    href: a?.href,
    launch: cells[1],
    resolved: cells[2],
    min: cells[3],
    avg: cells[4],
  };
}).filter(x => x.program);
```

Ranking signals:
- Strong: high average bounty, many resolved reports, recent launch, broad web/API/code scope.
- Weak: no resolved reports, VDP-style wording, vague external listing, very narrow assets.

High-ROI patterns seen in May 2026 public directory:
- New/high-average: Anthropic, Vercel Open Source, Robinhood.
- Mature/high-signal: GitLab, PayPal, GitHub, TikTok.
- White-box advantage: open-source programs where source review can drive focused reports.

## Butian public reward hall

URL: `https://www.butian.net/Reward/plan/1` or `/Reward/plan/2`

Public fields visible without login:
- program name
- short description
- reward range, e.g. `奖金范围：75 ~ 40,000元`
- some operational constraints embedded in descriptions, e.g. testing hours or self-account-only notes

Submitting redirects to login. Do not treat submit access as scope proof. Read the public card and then program rules after login before probing.

Useful browser-console extraction for visible reward cards:

```js
(() => {
  const lines = document.body.innerText.split('\n').map(s => s.trim()).filter(Boolean);
  const out = [];
  for (let i = 0; i < lines.length; i++) {
    const m = lines[i].match(/(?:奖金范围：([\d,]+) ~ ([\d,]+)元|最高奖金：\s*([\d,]+)元)/);
    if (m) out.push({
      name: lines[i - 2],
      desc: lines[i - 1],
      min: m[1] || '',
      max: m[2] || m[3],
      raw: lines[i],
    });
  }
  return out.sort((a,b) => Number(b.max.replace(/,/g,'')) - Number(a.max.replace(/,/g,'')));
})();
```

Ranking signals:
- Strong: high max reward, consumer/mobile/API-heavy business, clear current reward plan.
- Weak: very low max reward, narrow hardware-only scope without equipment, strict time windows unless user can comply.

High-ROI public cards observed:
- 理想汽车: `75 ~ 40,000元`
- 美团安全应急响应中心 / 大众点评专测: `70 ~ 24,000元`
- SHEIN: `50 ~ 10,000元`
- 叮咚买菜: `50 ~ 8,000元`
- 水滴公司: `30 ~ 8,000元`
- 翼支付 / 乐信 / 信也: finance targets with higher rule sensitivity. Use self-owned accounts only.

## Output format

Keep it short:
1. top targets by platform
2. public evidence: URL, reward/resolved/average fields
3. why ROI is good
4. first safe focus areas
5. ask user to choose one target before any in-scope testing
