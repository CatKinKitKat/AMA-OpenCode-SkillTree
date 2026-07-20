# Cross-platform rank-scan degradation

Use this when scanning multiple novel platforms and some live pages/API paths fail or return partial data.

## Pattern

1. Prefer live public pages first, then CDP/browser snapshot, then HTTP parse, then existing trend references.
2. Keep a scan artifact under the user's project/workspace with:
   - timestamp and platform URLs
   - what was successfully extracted
   - what failed and exact observed symptom
   - which conclusions are based on live data vs historical/trend knowledge
3. Do not invent missing platform榜单. If Qidian returns a probe/empty challenge page or Qimao renders only nav/footer, mark the data unavailable and continue with platforms that yielded usable榜体.
4. For Fanqie public rank pages, HTML text may include font-obfuscated body copy. Titles, categories, rank labels, and some structured fields are often still usable enough for trend extraction. Label obfuscated fields as degraded.
5. When the user asks to 扫榜/拆书/有灵感就开项目 in one request, produce both:
   - a scan/deconstruction evidence file
   - a derived original project folder with outline, world, characters, foreshadowing, intro, and cover prompt.

## Data quality labels

- `live-full`: rank body and key fields extracted.
- `live-degraded`: rank body extracted but fields are obfuscated/missing.
- `page-shell-only`: page loads but only nav/footer/shell visible.
- `challenge-only`: HTTP/browser sees anti-bot/probe shell.
- `historical-reference`: no live data. Using stored trend/method references.

## Pitfalls

- Do not spend the whole session fighting one blocked platform if other platforms yielded enough signal.
- Do not treat browser/HTTP transient failures as durable tool rules. Record the symptom in the scan artifact only.
- Do not copy榜文皮相 into the new concept. Extract bones: title structure, conflict, gold-finger condition/feedback, and platform fit.
