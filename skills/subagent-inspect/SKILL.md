---
name: subagent-inspect
description: "审计 Claude Code 子代理 (subagent) 的完整执行轨迹，涵盖定位 JSONL 日志、审计工具调用序列、诊断 AI 决策-行动断裂点。当用户提到 eval 子代理、子代理推理链、subagent 日志、查看子代理执行过程、审计 sub-agent、分析 agent 决策、为什么 AI 没做 X、subagent trace 时使用此 skill。"
---

# subagent-inspect：子代理执行轨迹审计

## 三阶段工作流

| 阶段 | 目的 | 输出 |
|------|------|------|
| 定位 | 找到目标 subagent 的 JSONL 文件 | 文件路径 |
| 审计 | 格式化呈现执行轨迹 | 可读事件链 |
| 诊断 | 定位判断-行动断裂点 | 根因 + 修复建议 |

---

## 日志位置

```
~/.claude/projects/<project>/<session>/subagents/
├── agent-<id>.jsonl       ← 子代理完整执行轨迹
└── agent-<id>.meta.json   ← agent 描述（eval 名称、任务摘要）
```

**项目路径编码**：`\` → `-`，`:` 去掉。例：`D:\Test\Foo` → `D--Test-Foo`

---

## 阶段一：定位 JSONL 文件

### 方法 A：从主会话 grep
```bash
grep "agent-" <主会话>.jsonl | head -10          # 找 agent 前缀路径
grep "subagent" <主会话>.jsonl | head -20        # 找创建记录
```

### 方法 B：直接列出
```bash
ls ~/.claude/projects/<project>/<session>/subagents/
# 用文件大小判断：活跃 eval 通常 10KB-100KB，空文件未执行
```

### 方法 C：通过 meta 映射
```bash
for f in subagents/*.meta.json; do echo "$(basename $f): $(head -1 "$f")"; done
# 每行第一行的 "description" 字段 = eval 描述
```

---

## 阶段二：审计执行轨迹

### 工具脚本
```bash
python scripts/inspect_agent.py <jsonl路径>              # 完整事件链
python scripts/inspect_agent.py <jsonl路径> --filter Read # 只显示 Read 调用
python scripts/inspect_agent.py <jsonl路径> --stats      # 工具调用统计
python scripts/inspect_agent.py <jsonl路径> --no-truncate # 完整内容
```

### 输出标签
- `[USER N]` — 用户消息
- `[TEXT N]` — 模型文本回复
- `[TOOL N]` — 工具调用（带参数）
- `[RESULT N]` — 工具返回结果
- `[THINKING N]` — 模型内部推理

### 执行原则：grep 优先，全文阅读最后 resort

不要一上来就 Read 整个 JSONL 文件。正确顺序：

1. **grep** — 找信息在哪一行
2. **局部 Read** — 只读命中行附近几行
3. **全文 Read** — 前面两步不够时才读完整文件

### 快速 grep 模式
```bash
# 看模型调用了哪些工具
grep '"type": "tool_use"' agent-xxx.jsonl | grep '"name"'
# 看最终答案
grep '"type": "result"' agent-xxx.jsonl
# 看执行轮数
grep -c '"type": "tool_result"' agent-xxx.jsonl
```

### JSONL 事件类型

| type | 含义 | 关键字段 |
|------|------|----------|
| `system` | 系统提示词 | `content[0].text` |
| `user` | 输入 | `message.content` |
| `assistant` | 模型输出 | `message.content[].type` (text / tool_use) |
| `tool_result` | 工具返回 | `content[0].text` |
| `result` | 最终结论 | `subtype`, `result` |

`queue-operation`、`attachment` 等类型是基础设施噪音，跳过。

---

## 阶段三：诊断断裂点

当 eval 结果 partial/fail 时，需要理解 AI "怎么想、怎么做、哪里断裂"。

### 提取三类事件

从 assistant 事件中筛选：

**想了什么**
```json
{"type":"text","text":"按照 SKILL.md，复杂场景应该升级到 zhipu-thinking"}
```

**读了什么**
```json
{"type":"tool_use","name":"Read","input":{"file_path":"..."}}
```

**做了什么**
```json
{"type":"tool_use","name":"Bash","input":{"command":"python vision_read.py ..."}}
```

### 决策链输出格式

```markdown
### eval-N [描述] — 决策链分析

| 行 | 时间 | AI 想什么（判断） | AI 做什么（行动） | 断裂？ |
|----|------|-------------------|-------------------|--------|
| L10 | 13:05 | "该用 zhipu-thinking" | 决定先走默认路由 | ✅ |
| L17 | 13:06 | "预期模型: zhipu-thinking" | 执行时不带参数 | ✅ |

**根因**: [一句话——通常是 SKILL.md 的某段描述给了 AI "跳过后一步"的正当理由]
**建议**: [具体改哪段文字可以修复]
```

### 诊断原则
- **分段 Read**：大文件用 Read 的 offset/limit，每次 8-10 行
- **跳过噪音**：只关心 user/assistant 里的决策事件
- **根因指向可修复处**：不说"AI 偷懒"，说"SKILL.md 第 X 段描述了 Y，导致 AI 理解为 Z"
- **建议具体到文字**："把『先用默认路由』改为『完成默认路由后检查复杂场景并升级』"

---

## 多 agent 对比

```bash
# 横向对比多个 eval
for f in agent-*.jsonl; do
  echo "=== $f"
  grep '"type": "result"' "$f"
  grep -c '"type": "tool_use"' "$f"
done
```

关注：第一步工具选择是否相同、是否检查了环境变量、是否调用了 skill。
