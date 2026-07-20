#!/bin/bash
# setup_cdp_chrome.sh
# 检查并复用用户已有的 Chrome CDP 环境。永不杀进程，永不启新实例，永不换 profile。
#
# 用法: bash setup_cdp_chrome.sh [端口号]
#   端口号: CDP 调试端口（默认: 9222）

set -e

CDP_PORT="${1:-9222}"

echo "=== CDP Chrome 环境检查 ==="
echo "CDP 端口: $CDP_PORT"

# 第一步：检查 CDP 端口是否已在监听
if lsof -nP -iTCP:${CDP_PORT} -sTCP:LISTEN &>/dev/null; then
    echo "✅ CDP 端口 $CDP_PORT 已处于活跃状态。"
    # 验证端口是否正常响应
    if curl -s --connect-timeout 3 http://127.0.0.1:${CDP_PORT}/json/version &>/dev/null; then
        echo "✅ CDP 连接已验证，Chrome 就绪。"
        curl -s http://127.0.0.1:${CDP_PORT}/json/version 2>/dev/null | head -5
        exit 0
    else
        echo "❌ 端口正在监听但无响应。可能是 Chrome 仍在启动中，或端口被非 Chrome 进程占用。"
        echo "   请手动排查后重试。"
        exit 1
    fi
fi

# 第二步：端口未监听 — 不再做任何操作，仅报告
echo "❌ CDP 端口 $CDP_PORT 未监听。"
echo ""
echo "请手动启动 Chrome 远程调试："
echo "  /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome \\"
echo "    --remote-debugging-port=$CDP_PORT \\"
echo "    --user-data-dir=\"\$HOME/Library/Application Support/Google/Chrome\" \\"
echo "    --profile-directory=Default"
echo ""
echo "注意：如果 Chrome 已在运行，需先关闭所有窗口再执行上述命令。"
exit 1
