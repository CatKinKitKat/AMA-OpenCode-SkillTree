---
name: cloakbrowser
description: Route for CloakBrowser. Use when the task mentions CloakBrowser, stealth Chromium, anti-detect browser, browser fingerprinting, Playwright/Puppeteer stealth replacement, or Chinese triggers: 隐身浏览器、反检测浏览器、指纹浏览器、浏览器指纹、抗指纹、过检测、Cloudflare Turnstile、自动化浏览器伪装。
tags: [cloakbrowser, browser, stealth, playwright, puppeteer, fingerprint]
version: 1
---


# CloakBrowser

Purpose
- Route CloakBrowser tasks to the local reviewed source clone.
- Treat binary auto-downloads and profile/session storage as security-sensitive.

Local source
- ~/.agent/external-repos/CloakBrowser
- Upstream: https://github.com/CloakHQ/CloakBrowser

Safe workflow
1. Read README, Python/JS package manifests, and binary/update behavior first.
2. Before `pip install cloakbrowser`, `npm install cloakbrowser`, Docker pulls, or first launch, confirm scope if it will download binaries or persist profiles.
3. Do not mix profile stores with unrelated real browser profiles unless requested.
4. Use for authorized browser automation, testing, and sandbox anti-bot research only.

Chinese route triggers
- CloakBrowser, 隐身浏览器, 反检测浏览器, 指纹浏览器, 浏览器指纹, 抗指纹, stealth chromium, Playwright 隐身, Puppeteer 隐身, Turnstile 测试, 自动化浏览器伪装
