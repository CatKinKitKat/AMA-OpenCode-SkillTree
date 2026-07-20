# 番茄小说扫榜常见陷阱与解决方案

## 认证与登录陷阱

1. **未登录的任何浏览器（包括 CDP 和 camofox）** → 书库页面显示“没有找到相关结果”，API 要么 404 要么返回空数据。**必须先有登录态**。

2. **Cookie 注入**：
   - `document.cookie` 无法设置 `httpOnly` 的 cookie（sessionid、passport_mfa_token 等）。
   - 缺失关键认证 cookie 时，即使页面正常登录也会被网关 (`x-tt-agw-login`) 拦截。
   - 唯一可靠方式：让用户在 Chrome 中手动登录后，用 `--remote-debugging-port=9222` 启动并复用该 Profile，或用户通过浏览器扩展导出完整 cookie 并直接用 `curl` 携带（但不能绕过网关的次级检查）。

3. **API 调用**：
   - `/api/author/library/book_list/v0/` 端点：
     - 使用 `curl` 完整 cookie → 返回 `HTTP 404 + x-tt-agw-login:1`（网关拒绝）。
     - 在已登录的浏览器内用 `fetch` → 返回 `code:-2 "参数有误"`，即使 `category_list` 调用正常。
     - 2026-05 实测：`book_list` 在多种参数组合下均拒绝，可能接口已变化或需要额外请求体。
   - **目前稳定可用的 API 只有 `/api/author/book/category_list/v0/`**。

## 字体混淆陷阱

- `browser_snapshot` 返回的无障碍树文本为乱码（特殊字形映射）。
- `innerText` 提取的文字依然是原始字符，不可读。
- 唯一可靠方案：**截图 + 视觉识别**（`browser_vision`）。
- `browser_vision` 可能超时（页面重、图片大）→ 建议缩小截图区域或降低请求的书本数量。

## 筛选短篇（<30万字）

- API 参数 `word_count=1` 理论上对应“30万字以下”，但实测不稳定，有时返回超过30万的书。
- 视觉识别时需人工校验或额外验证字数。

## 已失效 / 变化的内容

- `category_id=10`（悬疑）等旧 ID 已失效。
- `book_list` 端点当前（2026-05）无法正常工作，即使带正确 cookie 也返回 -2。
- 历史映射表（女频悬疑→悬疑惊悚等）仍可用于分类匹配，但需用 `category_list` 动态获取最新的 ID。

## 当前唯一可靠扫榜流程（番茄短篇）

1. 用户手动在 Chrome 中登录 `fanqienovel.com`。
2. 用 CDP 方式连接该 Chrome：`open -a "Google Chrome" --args --remote-debugging-port=9222 --user-data-dir=...`。
3. 使用 `browser_navigate` 打开书库页面。
4. 点击“字数”筛选 → “30万以下”。
5. 用 `browser_vision` 识别页面截图，提取书名、作者、字数。
6. 若 `browser_vision` 超时，可先滚动页面只捕获前几本书。

camofox 目前无法通过 cookie 注入获得登录态，因此不能单独用于需要登录的扫描。
