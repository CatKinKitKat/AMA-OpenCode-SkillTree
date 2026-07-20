# Cross-platform scan-to-project pattern

Use after a session where the user asks to scan multiple web-novel platforms, deconstruct market patterns, and immediately create a new story project.

## Durable pattern

1. Route primarily to `story-long-scan`, then load `story-long-ana` and `story-long-write` as supporting skills when the requested output includes both market deconstruction and project artifacts.
2. Gather live data in parallel where possible:
   - fanqie: homepage/rank public DOM, rank page when available
   - qimao: public `/paihang` DOM, male/female + hot/new when possible
   - qidian: PC may be WAF-gated. Mobile public rank pages can be a useful fallback
3. Mark evidence tiers explicitly:
   - live DOM/public page facts
   - visible rank/title/category/metadata
   - inferred golden-three-chapter structure
   - creative synthesis for the new project
4. For a direct-to-project request, do not stop at a report. Create a compact project folder with separate files:
   - `扫榜拆书报告.md`
   - `项目设定总纲.md`
   - `大纲_8万字10章.md` or equivalent requested length/chapters
   - `金手指.md`
   - `世界观.md`
   - `人物关系.md`
   - `伏笔铺垫.md`
   - `简介.md`
   - `封面生图提示词.md`
5. Pick one market-fit concept rather than dumping many undeveloped ideas. Use scan evidence to justify the selected title/genre.

## Pitfalls

- If one platform blocks PC pages, do not conclude the platform is unusable. Try mobile/public HTML or visible page snapshots and label the limitation.
- Do not over-copy榜书. Extract title bones, emotion chains, and opening mechanics. Then synthesize a different setting/mechanism.
- Keep the generated project files modular. Avoid a single giant brief that future writing sessions cannot selectively load.
