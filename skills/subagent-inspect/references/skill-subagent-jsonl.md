---
name: subagent-jsonl
description: "如何在 Claude Code 项目中定位、读取和解析子代理 (subagent) 的 JSONL 执行日志。当用户提到 eval 子代理、子代理推理链、subagent 日志、查看子代理执行过程、调试子代理行为、分析 agent 决策时使用此 skill。"
---

# 子代理 JSONL 审查指南

## 目录结构

```
~/.claude/projects/<project>/<session>/subagents/agent-<id>.jsonl
```

- `<project>` — 项目目录名（与工作目录路径对应，`\` 替换为 `-`，`:` 去掉）
- `<session>` — 会话 UUID（7 位前缀 + 完整 UUID）
- `<id>` — 子代理执行 ID

每个子代理运行生成**一个** `.jsonl` 文件。`.meta.json` 仅含元数据，推理过程在 `.jsonl` 中。

## 如何定位目标文件

### 方法一：从主会话找 agent ID

在主会话 JSONL 中搜索子代理创建记录：

```bash
grep "subagent" <主会话>.jsonl | head -20
```

或直接搜 agent 前缀路径：

```bash
grep "agent-" <主会话>.jsonl | head -10
```

会看到形如 `~/.claude/projects/.../subagents/agent-xxxx.jsonl` 的完整路径。

### 方法二：直接列出

```bash
ls ~/.claude/projects/<project>/<session>/subagents/
```

用文件大小判断哪个是活跃的 eval（通常 10KB-100KB，空文件是未执行的）。

## 执行原则：grep 优先，全文阅读最后 resort

> **不要一上来就 Read 整个 JSONL 文件。** 大文件（100+ 行）一次性读入会导致上下文混乱，而且大部分内容对你当前的问题没有用。

正确的顺序：

1. **先 grep** — 找到你想看的信息在不在、在哪一行
2. **再读局部** — 只读 grep 命中那一行或附近几行
3. **最后才全文读** — 只有上面两步都不够时才读完整文件

常见的 grep 套路都能覆盖 90% 的分析需求，不需要读全文。

## JSONL 行结构

每行一个 JSON 对象，按时间顺序排列。常见类型：

| type | 说明 | 关键字段 |
|------|------|----------|
| `system` | 系统提示词 | `content[0].text` |
| `tools_delta` | 可用工具列表 | `tools_delta` |
| `skill_list` | 注入的 skill | `skills[].name` |
| `assistant` | 模型输出 | `content[].type` (text / tool_use) |
| `tool_result` | 工具执行结果 | `content[0].text` |
| `result` | 最终结论 | `subtype`, `result` |

### assistant 行的两种形态

**纯文本回复**：
```json
{
  "type": "assistant",
  "content": [{"type": "text", "text": "直接回答..."}]
}
```

**工具调用 (tool_use)**：
```json
{
  "type": "assistant",
  "content": [{"type": "tool_use", "name": "Bash", "input": {"command": "..."}}]
}
```

**tool_result 对应工具调用**：
```json
{
  "type": "tool_result",
  "content": [{"type": "tool_result", "text": "执行输出..."}]
}
```

## 解析流程

### 提取完整推理链（6 步）

对每个 agent JSONL 文件，提取以下部分按顺序组合：

1. `system` 行 — 看系统提示词和注入的上下文
2. `tools_delta` 行 — 看可用工具列表（判断模型有什么选择）
3. `skill_list` 行 — 看加载了哪些 skill（关键：是否包含目标 skill）
4. `assistant` + `tool_result` 交替序列 — 决策链（模型每一步选了什么）
5. 最后一条 `assistant` — 最终决策
6. `result` 行 — 官方结果（subtype: "success" / "error"）

### 快速 grep 模式

```bash
# 看模型调用了哪些工具
grep '"type": "tool_use"' agent-xxx.jsonl | grep '"name"'

# 看最终答案
grep '"type": "result"' agent-xxx.jsonl

# 看整个执行中有多少轮工具调用
grep -c '"type": "tool_result"' agent-xxx.jsonl
```

### 提取关键决策点

最常见的判断：**模型第一步做了什么**

```bash
# 找到第一个 assistant/tool_use
grep '"type": "assistant"' agent-xxx.jsonl | head -1 | python -c "import sys,json; d=json.loads(sys.stdin.read()); print([c.get('name','') for c in d.get('content',[]) if c.get('type')=='tool_use'])"
```

## 多 agent 对比

当有多个 eval 的 agent 文件时，横向对比：

```bash
# 生成对比表
for f in agent-*.jsonl; do
  echo "=== $f ==="
  grep '"type": "result"' "$f"
  grep -c '"type": "tool_use"' "$f"
done
```

关注差异：
- 第一步工具选择是否相同
- 是否检查了环境变量（grep `VISION_BLOCK_READ` 等关键字）
- 是否调用了 skill（看 `skill_list` 行和工具名）
