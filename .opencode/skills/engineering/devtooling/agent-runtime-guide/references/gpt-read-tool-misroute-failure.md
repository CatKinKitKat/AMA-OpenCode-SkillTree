## GPT 模型误调用 `read` 工具导致循环卡死的修复  

**症状**  
- GPT 模型反复调用不存在的工具 `read`（而非正确的 `read_file`）  
- 连续 3 次调用后对话卡死  
- 问题只出现在 GPT 模型（The agent 无此问题）  

**根因**  
- 工具命名空间存在歧义（`read` vs `read_file`）  
- GPT 模型对 `read` 有较强的先验幻觉，容易跳过正确的 `read_file`  
- 网关层缺少自动别名映射，导致无效工具调用链被重复执行  

**修复层（由底向上）**  

| 层级 | 改动文件 | 动作 | 优先级 |
|------|----------|------|--------|
| 工具描述层 | `tools/file_tools.py` | 修改 `read_file` 的 schema 描述，增加“禁止使用 `read`”的指令 | P0 |
| 网关中间层 | `model_tools.py` | 在 `handle_function_call` 前加别名映射：`read` → `read_file` | P0 |
| 工具映射 | `tools/registry.py` | 注册别名 `read` → `read_file` | P1 |
| 系统提示词 | `agent/prompt_builder.py` | 在 prompt 头部加入硬性约束，禁止调用 `read` | P1 |
| 死循环防护 | `run_agent.py` | 相同无效工具连续失败 ≥2 次时自动注入纠正提示 | P2 |

### 1. 工具描述层（file_tools.py）  

**修改前**  
```python
description="Read a text file with line numbers and pagination.",
```

**修改后**  
```python
description="Read a text file with line numbers and pagination. Use this tool instead of 'read'. Do NOT call 'read' — it does not exist. Only 'read_file' works.",
```

### 2. 网关中间层（model_tools.py）  

在 `handle_function_call` 函数入口加入：  

```python
# 别名自动映射：read → read_file
if tool_name == "read" and "path" in args:
    tool_name = "read_file"
    # 可选：打印警告日志
    print(f"[GW] Auto-rewrote 'read' to 'read_file' for path={args.get('path')}")
```

同时在映射失败时返回：  

```plaintext
Tool 'read' not found. Did you mean 'read_file'?
```

### 3. 工具映射（tools/registry.py）  

新增别名注册方法：  

```python
class ToolRegistry:
    def __init__(self):
        self._tools = {}
        self._aliases = {}

    def register_alias(self, alias: str, target: str):
        self._aliases[alias] = target

    def get(self, name: str):
        return self._tools.get(self._aliases.get(name, name))
```

在 `file_tools.py` 末尾调用：  

```python
registry.register_alias("read", "read_file")
```

### 4. 系统提示词（prompt_builder.py）  

在系统 prompt 的最前面（优先级最高）加入：  

```text
TOOL USAGE RULES:
- There is NO tool named 'read'.
- To read a file, you MUST use 'read_file'.
- If you attempt to call 'read', it will fail and waste turns.
- NEVER call 'read'. Use 'read_file' exclusively.
```

### 5. 死循环防护（run_agent.py）  

在 `run_conversation` 循环内插入：  

```python
if consecutive_failed_tool_calls.get('read', 0) >= 2:
    self.messages.append({
        "role": "assistant",
        "content": "'read' is not a valid tool. Use 'read_file' instead. Proceeding."
    })
    consecutive_failed_tool_calls['read'] = 0
```

### 验证步骤  
1. 重启 the agent（或 `/reset` 会话）  
2. 用 GPT 模型发出指令："读取 config.yaml"  
3. 确认只生成 `read_file` 调用，无 `read` 调用  
4. 确认即使手动强制 `read` 也会被自动映射为 `read_file` 并正常返回  
5. 确认连续失败 2 次后自动注入纠正提示，不会卡死