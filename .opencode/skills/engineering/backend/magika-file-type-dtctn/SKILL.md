---
name: magika-file-type-dtctn
description: Use Google Magika for fast ML-based file-type detection from file bytes, not just extensions or MIME. Use when the user needs reliable file identification, suspicious upload triage, content-type validation, malware-prep filtering, or bulk file classification.
version: 1.0.0
author: the agent
license: Apache-2.0-or-similar-upstream
---


# Magika File Type Detection

用 Magika 判文件类型。

适用：
- 上传文件真类型校验
- 扩展名伪造排查
- 批量文件分类
- 安全前置检测
- 内容型路由

## 安装

优先低权限安装：
```bash
python3 -m pip install --user magika
```

若 PATH 未含用户 bin：
```bash
export PATH="$HOME/.local/bin:$PATH"
```

验证：
```bash
magika --version
magika somefile.bin
```

## 用法

单文件：
```bash
magika path/to/file
```

批量：
```bash
find path/to/dir -type f -print0 | xargs -0 magika
```

JSON 输出若上游版本支持，则优先 JSON；否则读标准文本输出。

## the agent 用法

1. 先装并验证 CLI 可运行。
2. 对用户给的文件或目录跑检测。
3. 若结果与扩展名/MIME 不符，明确标“伪装”或“待审”。
4. 若用于上传链路，先以 Magika 结果作为内容真相，再决定解析器。

## 判定原则

- 扩展名只作提示，不作真相。
- MIME 头只作旁证，不作真相。
- 真正路由以 Magika 内容判定为主。
- 对低置信或未知类型，再回退到人工/额外检测。

## 适合集成到 the agent 的场景

- 本地文档摄取前分类
- repo intake 时判断混入二进制/模型/媒体/文档
- 上传安全网关前置判断
- OCR、PDF、图像、代码文件分流

## 风险

- Magika 强，但非绝对；未知/混合/损坏文件仍可能需二次检查。
- 安全流程中，不可因识别成功就跳过沙箱或 AV。
