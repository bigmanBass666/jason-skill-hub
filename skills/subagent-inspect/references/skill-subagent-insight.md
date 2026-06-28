---
name: subagent-insight
description: "将子代理 JSONL 执行日志转化为可读的决策链，定位 AI 的『判断-行动断裂点』。用于 skill-creator eval 循环的诊断阶段：当 eval 结果出现 partial/fail，需要理解 AI 『怎么想、怎么做、哪里断裂』时触发。也适用于调试 subagent 行为、分析 agent 决策逻辑。触发词：分析子代理决策链、trace 子代理、看 eval 怎么失败的、为什么 AI 没做 X、subagent trace、决策链审查。"
argument-hint: "[eval-name或agent-description]"
allowed-tools: Read, Bash, Grep
---

# subagent-insight

定位：skill-creator eval 循环中的诊断层。当 grading.json 告诉你"有什么错了"但没说"AI 为什么没有这样做"时，用这个 skill 挖深层原因。

## 输入定位

### 1. 找到当前项目的主会话 JSONL

```bash
ls ~/.claude/projects/<project-name>/      # 找最新修改的 JSONL
```

### 2. 同目录下找 subagents 目录

```
~/.claude/projects/<project-name>/<session-uuid>/subagents/
  ├── agent-<id>.jsonl      ← 子代理完整执行轨迹
  └── agent-<id>.meta.json  ← agent 描述（eval名称、任务摘要）
```

### 3. 用 meta 建立映射

```bash
for f in subagents/*.meta.json; do
  echo "$(basename $f): $(head -1 "$f")"
done
```

每个 .meta.json 第一行包含 `"description"` 字段——这是 eval 描述（如 "free-vision eval: model-selection-reasoning"）。

## JSONL 格式速览

每个子代理 JSONL 只有三种有效事件：

| type | 含义 | 关键字段 |
|------|------|---------|
| `user` | 输入——eval prompt 或 tool_result | `message.content` → `tool_use_id`, `type: text` |
| `assistant` | AI 的响应——推理或工具调用 | `message.content[]` → `type: text`(思考) 或 `type: tool_use`(行动) |
| `attachment` | 工具注册/系统事件 | 一般跳过，不包含决策信息 |

不要关心 `queue-operation`、`attachment`（hook）、`system` 等类型——它们是基础设施噪音。

## 提取三类事件

从 assistant 事件中筛选：

### 读了什么
```json
{"type":"tool_use","name":"Read","input":{"file_path":"..."}}
{"type":"tool_use","name":"Bash","input":{"command":"cat ..."}}
```

### 想了什么
```json
{"type":"text","text":"按照 routing.md，复杂图表应该首选 zhipu-thinking"}
```

### 做了什么
```json
{"type":"tool_use","name":"Bash","input":{"command":"python vision_read.py ..."}}
```

## 输出格式

按时间线排列，标注"判断-行动断裂点"：

```markdown
### eval-N [描述] — 决策链分析

| 行 | 时间 | AI 想什么（判断） | AI 做什么（行动） | 断裂？ |
|---|------|-------------------|-------------------|-------|
| L10 | 13:05 | "该用 zhipu-thinking" | 决定先走默认路由 | ✅ |
| L17 | 13:06 | "预期模型: zhipu-thinking" | 执行时不带 --backend | ✅ |
| L18 | 13:06 | — | `python vision_read.py ...` | 落实断裂 |

**根因**: [一句话说明断裂的原因——通常是 SKILL.md 的某段描述给了 AI 一个"跳过后一步"的正当理由]

**建议**: [具体改哪段文字可以修复这个问题]
```

## 执行步骤

```
1. ls ~/.claude/projects/<project>/<session>/subagents/  → 找到 agent .jsonl + .meta.json
2. 读 .meta.json → 确认 agentId → eval 描述匹配
3. 用分段 Read（每次 8-10 行）读 .jsonl，跳过 attachment/queue-operation
4. 提取三类事件（读/想/做），按时间排列
5. 对比"判断"和"行动"，标注断裂点
6. 输出决策链表 + 根因 + 建议
```

## 原则

- **分段读**：大文件用 Read 的 offset/limit，不要一次读全部
- **跳过噪音**：只关心 user/assistant 里包含决策的事件
- **精确到行号和时间**：让用户可以定位回 JSONL 原文
- **根因指向可修复的地方**：不说"AI 偷懒"，说"SKILL.md 第 X 段描述了 Y，导致 AI 理解为 Z"
- **建议具体到文字**："把『先用默认路由』改为『完成默认路由后，若图片属于复杂图表场景则升级到 zhipu-thinking』"
