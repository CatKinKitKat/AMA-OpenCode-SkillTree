# DOM fallback rank scan notes

Use when packaged scrapers or exact tab-click selectors return empty, but the public page visibly renders rank data.

## Pattern

1. Open the public rank/home page with browser automation.
2. Take a snapshot first. If rank entries are visible, treat it as primary evidence.
3. Use browser-side text extraction for fast capture:

```js
document.body.innerText.slice(0, 30000)
```

4. If the site exposes clickable refs in the snapshot, click the visible rank type/tab (`新书榜`, `大热榜`, etc.) and repeat text extraction.
5. Preserve evidence tiers in the output:
   - visible DOM/snapshot facts: title, category, rank, word count, heat, intro
   - inferred pattern: title bone, conflict bone, opening mechanic
   - creative synthesis: new project concept

## Platform notes

- Fanqie: homepage snapshot can expose `番茄巅峰榜`, `男频精选`, `女频精选`, and sometimes category rank text through `document.body.innerText`. Some deeper rank text may be font-mangled, so prefer homepage visible titles/categories as higher-confidence facts.
- Qimao: `/paihang/` public DOM often exposes full rank rows: title, author, category, status, word count, intro, update, heat. If a scraper cannot find `男生/女生` tabs because selector text changed, use snapshot refs or direct visible links and then `document.body.innerText`.
- Qidian: if PC/mobile rank pages show safety verification, stop spending time on challenge handling. Label it as unavailable live DOM and use it only as platform-tone reference.

## Output rule

Do not block scan-to-project delivery on one platform failing. Mark the limitation, extract bones from available platforms, and proceed to the project package.
