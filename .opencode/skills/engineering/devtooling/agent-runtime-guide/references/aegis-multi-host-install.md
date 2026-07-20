# Aegis 多宿主安装参考

## 项目信息
- 仓库: https://github.com/GanyuanRan/Aegis
- 定位: Architecture-Driven Development (ADD) Method Pack
- 技能数: 17 个（brainstorming, writing-plans, systematic-debugging, tdd, verification-before-completion 等）
- 许可: MIT

## the agent 安装

```bash
git clone https://github.com/GanyuanRan/Aegis.git /tmp/Aegis  # 或任意位置
rm -rf ~/.agent/skills/aegis
cp -R /tmp/Aegis/skills ~/.agent/skills/aegis
```

重启 the agent 或 `/reset` 后生效。

## the coding agent 安装

```bash
the agent plugin marketplace add GanyuanRan/Aegis
the agent plugin install aegis@aegis-dev --scope user
```

## 激活方式

对任一宿主说: `use aegis:using-aegis` 或在任务中使用 Aegis 技能名。

## 已知限制
- 不支持 `agent skills install` 自动安装（非 indexed source）
- 如需更新，重新从上游同步 `skills/` 到 `~/.agent/skills/aegis`
