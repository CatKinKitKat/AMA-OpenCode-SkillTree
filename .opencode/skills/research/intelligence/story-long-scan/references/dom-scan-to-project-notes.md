# 扫榜到开书：DOM 抓取速记

适用：用户要求番茄 / 七猫 / 起点扫书、拆书，并直接落新项目包。

## 番茄首页

首选公开首页：`https://fanqienovel.com/`

快速取可见文本：

```js
Array.from(document.body.innerText.split('\n')).filter(x => x.trim()).slice(0, 220)
```

可稳定取得：巅峰榜前排书名、分类、资讯、作家代表作。用于题材骨和标题骨足够。

## 七猫排行榜

首选：`https://www.qimao.com/paihang/`

快速取榜单条目：

```js
Array.from(document.querySelectorAll('li'))
  .map(li => li.innerText.trim())
  .filter(t => /^\d+\n/.test(t))
  .slice(0, 20)
```

可稳定取得：榜位、书名、作者、一级分类、二级分类、连载状态、字数、简介、更新时间、热度。适合做免费平台标题结构、低位身份、冲突词和可复制题材判断。

## 起点排行榜

入口：`https://www.qidian.com/rank/`

若 DOM 只见 iframe 或 `document.body.innerText` 为空，不要卡住。标注“实时 DOM 未取到”，降级为平台调性参考：规则闭环、升级逻辑、世界观纵深。

## 浏览器/脚本降级

- If a scraper script returns no rows but the rendered page clearly shows rank cards, treat the script as stale and switch to browser snapshot + `browser_console` + explicit click refs. Do not keep retrying the script as the primary path.
- For Qimao, `browser_console` on `document.body.innerText` can expose the full榜单 text after the snapshot truncates. That is enough to recover title/genre/status/word count/intro/hotness without needing the scraper.
- For tab changes, prefer clicking visible link refs from the snapshot when text-matching helpers fail. Then re-run `document.body.innerText`.

## 一体化交付原则

- 不因单个平台失败停工；保留数据质量标注。
- 番茄取脑洞 / 异常 / 收容感。
- 七猫取边关 / 官场 / 都市高手 / 玄幻强物件等强冲突免费平台骨架。
- 起点取体系化和规则闭环口径。
- 如果指定 projects 目录已有多个类似题材项目，先读现有项目名/README/大纲，避开已产出的母题；例如已有“边关+账本+灾年经营”时，优先转向都市诡异、规则职场、现代复仇等不同赛道。
- 最终产物必须落文件，不只聊天总结。
- 文件名必须精确匹配交付清单；不要用近义名替代。尤其 `封面生图提示词.md` 不等于 `封面提示词.md`，`正文计划.md` 不应只合并进 `大纲.md`。
- 写完后必须运行 `scripts/verify-scan-project-package.sh <book_dir>`。若失败，先补齐缺文件/字面目标，再给用户最终结果；`find`/`wc` 只证明文件存在和大小，不证明符合交付契约。
- 扫榜证据文件允许两个历史命名：`扫书感悟.md` 或 `扫榜拆书报告.md`。新项目优先用更清晰的 `扫榜拆书报告.md`，但验收脚本兼容两者。
- 如果工具调用后误返回空响应，下一轮必须直接处理已有工具结果并继续推进；不要重新解释或停在道歉。
