# Multi-platform scan to story project handoff

Use when the user asks to scan multiple web-novel platforms, deconstruct market patterns, then create a new story project with outline assets.

## Evidence pattern from this session

- Fanqie homepage DOM gave useful public samples: peak/rank titles, genres, male/female featured lists, and category rank text.
- Qimao ranking pages exposed clean DOM list items with rank, title, author, genre, subgenre, status, word count, intro, update, and heat.
- Qidian rank pages may present a WAF/captcha page in live browser. Treat that as a source limitation, not a hard stop.

## Practical fallback ladder

1. Try normal browser navigation and DOM extraction first.
2. If agent-browser/CDP CLI returns discovery or websocket errors, use the available browser DOM tools instead of stalling.
3. If one platform blocks, record it explicitly in the scan notes and use only platform-level trend knowledge for that source.
4. Continue with the platforms that yielded evidence. Do not claim blocked-platform samples as observed data.

## Minimum project artifact set

Create a project folder under the requested projects root and write at least:

- `扫书感悟.md`: source samples, observed trends, borrowed bones, blocked-source notes.
- `背景.md`: project goal, target platform/readers, boundaries.
- `简介.md`: title, one-line hook, formal intro, platform-selling-points.
- `大纲.md`: target word count, chapter count, chapter table, golden-three-chapter outline.
- `金手指.md`: trigger, reward, limits, upgrade route, first activation.
- `世界观.md`: geography, power/order structure, theme, tone.
- `人物关系.md`: protagonist, allies, antagonists, relationship graph, function roles.
- `伏笔铺垫.md`: visible setup, hidden setup, chapter recovery table.
- `封面提示词.md`: Chinese prompt, English prompt, negative prompt, typography notes.

## Quality gates

- State the scan sources and limitations in `扫书感悟.md`.
- Keep borrowed elements at the bone level: title structure, conflict shape, setting pressure, mechanism type. Avoid copying proper nouns or distinctive premise sentences.
- If the user requested 8万字 and 不超过十章, the outline must explicitly state both constraints and show the arithmetic.
- Verify file existence before reporting completion.