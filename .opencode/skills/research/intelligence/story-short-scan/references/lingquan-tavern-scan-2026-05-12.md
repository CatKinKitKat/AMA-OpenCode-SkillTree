# 灵泉酒馆扫书到项目样例：2026-05-12

## 触发场景

用户要求番茄/七猫/起点扫书、拆书，偏新书、火、短篇；扫出灵感后直接在 `~/Downloads/oh-story-the agentcode/projects` 落 8 万字且不超过 10 章项目包。

## 有效取数

番茄首页最近更新可直接提取 `table tr`：

```js
(() => Array.from(document.querySelectorAll('table tr')).slice(1).map(tr => {
  const cells = [...tr.querySelectorAll('td')].map(td => td.innerText.trim());
  const a = tr.querySelector('a[href*="/page/"]');
  return {type: cells[0], title: cells[1], chapter: cells[2], author: cells[3], time: cells[4], href: a ? new URL(a.getAttribute('href'), location.href).href : null};
}).filter(x => x.title))();
```

本轮可读样本：
- 《全部身家四十五，反手圈养残疾大》：女强反向供养、系统误读、残疾男主、强保护关系。
- 《女尊：全家穿越带灵泉在大隋躺赢》：女尊大隋、灵泉空间、府邸经营、朝堂宅斗。
- 《万朝酒馆》：独立酒馆连接多个朝代、交易历史难题、系统升级。
- 《修地煞七十二变后无敌》：梦中得法、三选神通、低阶觉醒。

七猫搜索页本轮只返回导航/页脚；起点榜单本轮空页。记录质量即可，不阻塞项目落盘。

## 可复用合成公式

“女强反向供养 + 女尊灵泉经营 + 酒馆单元剧 + 旧案罪证清算”。

适合 8 万字 / 10 章结构：
- 每章一位夜客。
- 每章一件遗物/罪证。
- 白天完成一笔“善账”，夜里洗出一段真相。
- 感情线用“把废太子养回尊严”承载爽点。
- 主线用十件罪证翻十年前宫变旧案。

## 项目模板注意

当用户明确列出文件名（如 大纲/金手指/世界观/人物关系/伏笔铺垫/简介/封面提示词/正文计划）时，先满足用户列出的文件与最低交付 `README.md`、`扫书感悟.md`；`背景.md` 只在项目需要或用户未限定文件时默认补充，不因缺少 `背景.md` 判失败。

验收：用 `search_files` 确认目标目录 `.md` 文件齐全；抽查 `README.md` 与 `正文计划.md`，后者必须含 `80,000 字左右`、`10 章`、每章字数、功能、章尾钩子。
