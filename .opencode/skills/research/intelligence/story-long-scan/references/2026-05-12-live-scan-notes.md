# Live scan notes: Fanqie / Qimao / Qidian

Date: 2026-05-12

## What worked
- Fanqie homepage DOM is readable from the visible page tree.
- `browser_console` with `document.body.innerText` is useful when the snapshot truncates the rank module.
- Qimao `/paihang/` exposes directly usable fields in DOM: rank, title, author, main genre, subgenre, status, word count, intro, recent update, and hotness.

## Evidence pattern from this session
- Fanqie top visible hooks clustered around:都市高武、悬疑脑洞、游戏体育、玄幻脑洞、现言脑洞.
- Qimao top visible hooks clustered around:都市高武、都市高手、架空历史、官场、东方玄幻、边关/历史.
- Qidian rank page rendered as empty/iframe-like in this browser session. Do not block on it.

## Practical takeaway
- For cross-platform scan-to-project work, use Fanqie + Qimao as live evidence anchors, and treat Qidian as调性参考 when live DOM is unavailable.
- When the snapshot is truncated, capture `document.body.innerText` before switching tabs.
