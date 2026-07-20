# Session pattern: cross-platform scan to 80k/10-chapter project

Use for requests that say: scan Fanqie/Qimao/Qidian, deconstruct hot/new/short patterns, then create a project folder with outline, mechanism, world, relationships, foreshadowing, synopsis, and cover prompt.

## Live-data tactics that worked

- Fanqie homepage public DOM is enough for trend bones. `document.body.innerText` can surface current peak-rank titles, categories, news, selected male/female books, and sometimes a category reading榜. If the visible rank starts at 22-30, still use it as trend evidence instead of retrying forever.
- Qimao `/paihang/` public DOM is high-value: list items include rank, title, author, genre, status, word count, intro, update time, heat, and trend flags.
- Qimao direct `/paihang/newbook/` can return a sparse fallback page. More reliable: open `/paihang/`, click the visible `新书榜` link, then extract `document.querySelectorAll('li')` text.
- Qidian PC/mobile rank pages may show a verification iframe/dialog. Treat as `real-time DOM unavailable`, use only platform-positioning inference, and do not block project creation.

## Extraction snippets

Fanqie visible text:

```js
(() => {
  const lines = document.body.innerText.split('\n').map(s => s.trim()).filter(Boolean);
  return lines.slice(0, 260);
})();
```

Qimao rank cards:

```js
(() => Array.from(document.querySelectorAll('li'))
  .map(li => li.innerText.trim())
  .filter(t => t.length > 20)
  .slice(0, 20))();
```

## Creative synthesis rule

Pick one concept, not a bundle of half-ideas. Good short-hot 80k project bones combine:

1. Qimao new-book low-position start: demotion, exile, public humiliation, being sent to a dead-end office/place.
2. Qimao hot-list direct conflict: officialdom, audit, border, hunting, resource control, family betrayal.
3. Fanqie high-concept engine: rule anomaly, monster/abnormal institution, time or record mechanism, profession-as-entry.
4. Short-story emotion chain: grievance -> hidden ledger/mechanism -> evidence -> public reversal.

## Output contract

Create a folder under the user's target `projects/` path and write at least:

- `README.md`
- `扫书感悟.md`
- `简介.md`
- `大纲.md`
- `正文计划.md`
- `金手指.md`
- `世界观.md`
- `人物关系.md`
- `伏笔铺垫.md`
- `封面生图提示词.md`

`正文计划.md` must state about 80,000 words and no more than 10 chapters, with per-chapter word count, function, core content, and chapter-end hook.

Verify with a file listing and a spot-read of `正文计划.md` before final response.
