# Continuation 扫榜到开项目续跑心得（2026-05）

适用：用户连续发送 `[Continuing toward your standing goal]`，目标是“去番茄/七猫/起点扫书、拆书，有灵感后在 projects 下新建 8 万字不超过 10 章项目包”。

## 行为规则

- 不把“已产出一个项目”视为总目标完成；默认继续下一轮，产出下一本。
- 每轮必须换题材/钩子，避免重复上轮核心能力或场景。
- 每轮最小闭环：采样 → 读 2-3 个详情页简介/目录信号 → 抽可迁移点 → 新建项目 → 写 10 文件 → 验证文件齐全与计划行数。

## 番茄公开 DOM 稳定路径

1. `browser_navigate https://fanqienovel.com/`
2. `browser_console` 提取最近更新表格：

```js
(() => {
  const rows=[...document.querySelectorAll('table tr')].slice(1).map(tr=>{
    const t=[...tr.querySelectorAll('td')].map(td=>td.innerText.trim());
    const a=tr.querySelector('a[href*="/page/"]');
    return {type:t[0]||'', title:t[1]||'', chapter:t[2]||'', author:t[3]||'', time:t[4]||'', href:a?.href||''};
  }).filter(x=>x.href);
  return rows;
})()
```

3. 选 2-3 个样本详情页，优先：
   - 7-10 万字新书/短篇感强。
   - 标题有强钩子。
   - 简介中有明确能力、职业、封闭场景、倒计时、旧案、关系张力。
4. 从每本只取“可迁移点”，避免复刻原书主角职业、案名、核心反转。

## 七猫 / 起点取数质量处理

- 七猫搜索页可能只渲染导航与页脚；书库可见筛选但无作品。记录“公开页未取到可用书单”，不要卡住。
- 七猫排行榜更稳：先打开 `https://www.qimao.com/paihang/`，再点击页面内“新书榜”。本轮可读到标题、作者、分类、简介、最近更新；适合抽“边关猎户/东北打猎/官场下乡/都市高手”等七猫强情绪与主流爽点信号。
- 起点 rank 页面可能返回 probe/iframe 空壳。记录“探针页/空壳”，不要卡住。
- 只要番茄公开详情页可读，或番茄 + 七猫任一主源可读，就继续产出。

## 项目差异化例子

同一连续目标中已跑出多类：
- 古风亡魂美食旧案：`shadow-recipe-soul-inn`
- 古代捕快外卖订单：`copper-well-bento-catcher`
- 都市死亡线食堂：`deathline-canteen-thirty-seconds`
- 雪山镜庄采药悬疑：`mirror-lodge-ginseng-snow`

后续续跑应优先找未覆盖组合，例如：
- 校园/宿舍规则怪谈 + 证据链。
- 家庭复仇/婚恋反转 + 职业技能。
- 民国/旧影/报社档案。
- 科幻末世短篇 + 亲情/女性互救。

## 验收清单

必有 10 文件：
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

`正文计划.md` 必须写：
- 总字数 8 万字以内。
- 章数不超过 10 章。
- 每章字数、功能、章尾钩子。

验证命令或等价工具检查：
- `search_files('*.md', target='files', path=project_dir)` 返回 10。
- `read_file(简介.md)` 非空。
- `read_file(正文计划.md)` 非空且含章级计划。
