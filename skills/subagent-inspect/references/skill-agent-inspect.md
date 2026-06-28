---
name: agent-inspect
description: "审计 Claude Code 交互会话或 sub-agent 的完整执行轨迹。用于排查：sub-agent 做了什么、为什么没做某件事、有没有调用某个工具。输入 JSONL 文件路径，输出可读的事件链。适用于 eval 验证、行为审计、debug agent 决策。"
argument-hint: "<jsonl-path> [--filter ToolName] [--stats]"
---

# Agent Inspector

解析 Claude Code 的 JSONL 会话日志，输出可读的执行轨迹。

## 用法

```bash
python scripts/inspect_agent.py <jsonl路径>
python scripts/inspect_agent.py <jsonl路径> --filter Read
python scripts/inspect_agent.py <jsonl路径> --stats
python scripts/inspect_agent.py <jsonl路径> --filter Skill --no-truncate
```

## 参数

| 参数 | 说明 |
|------|------|
| `jsonl` | JSONL 文件路径（必填） |
| `--filter <ToolName>` | 只显示匹配该工具的事件 |
| `--stats` | 打印工具调用统计 |
| `--no-truncate` | 显示完整内容，不截断 |

## 输出格式

- `[USER N]` — 用户消息
- `[TEXT N]` — 助手文本回复
- `[TOOL N]` — 工具调用（带参数）
- `[RESULT N]` — 工具返回结果
- `[THINKING N]` — 模型内部推理（如果存在）

## 找 JSONL 文件

Session 日志位置：`~/.claude/projects/<encoded-project-path>/`

项目路径编码规则：`D:\Test\Foo` → `D--Test-Foo`（`\` → `-`，`:` 去掉）
