---
name: memory-cleanup
description: >
  Scan and clean up Claude Code's auto memory (MEMORY.md + topic files).
  Identify stale, duplicate, orphaned, or bloated entries and help you consolidate
  them. Trigger when the user says "clean up memory", "memory is bloated",
  "review my memories", "check memory health", "memory is too big", "MEMORY.md
  needs cleaning", "memory maintenance", "帮我清理记忆", "记忆太多了",
  "memory is messy", or any variant of memory management / context hygiene.
  Also trigger when context seems crowded or when the user mentions the 200-line
  / 25KB MEMORY.md limit, or when they say "you should have known X but didn't"
  (which may indicate memory was truncated). Do NOT trigger for CLAUDE.md
  editing — only for auto memory (~/.claude/projects/.../memory/).
metadata:
  type: utility
  scope: project
  stability: stable
---

# Memory Cleanup Skill

## 目标

Claude Code 的 auto memory 只有**追加写入，没有自动清理**。系统提示的规则是"写前查重、错了就删、代码里有的不存"——但没有自动过期机制。记忆会越堆越多，直到 MEMORY.md 超过 200 行 / 25KB 的加载上限，超出的部分静默丢失，但你不知道丢了什么。

这个 skill 帮你做**定期记忆健康检查**：识别哪些记忆还有价值、哪些可以删除、哪些需要合并，然后执行清理。

## 使用方式

用户通过自然语言触发，不需要固定命令格式。识别以下意图：

| 用户意图 | 行为 |
|---------|------|
| "清理一下记忆" / "memory 太多了" | 全量审查，逐条确认后清理 |
| "看看记忆健康" / "dry run" / "先检查别删" | 只出报告，不修改任何文件 |
| "直接清理" / "force clean" / "把过时的全删了" | 自动清理，仅对"不确定"的条目询问 |

## 工作流程

### 第一步：定位 auto memory 目录

当前项目的 auto memory 路径是 `~/.claude/projects/<project>/memory/`。

- `<project>` 是 git 仓库路径的编码名（如 `D--Working-programming-projects-AK-Switch`）
- 如果不在 git 仓库中，提示用户并退出
- 如果 `~/.claude/projects/` 下没有当前项目的目录，说明 auto memory 从未启用或从未写入过，直接报告"没有 auto memory 需要清理"并退出

### 第二步：读取并分析所有记忆文件

1. 读取 `MEMORY.md`（索引文件，每行是一个 `- [Title](file.md) — description` 的链接）
2. 读取所有在 MEMORY.md 中被引用的 `.md` 文件（topic files）
3. 读取 `MEMORY.md` 中未引用的、但存在于 memory 目录中的 `.md` 文件（orphaned topic files）
4. 记录每个文件的行数、大小，以及 MEMORY.md 是否已接近 200 行 / 25KB 上限

### 第三步：对每条记忆应用分类规则

对每条记忆（MEMORY.md 中的一行 + 对应的 topic file 内容），判断其类别：

#### 🗑 可删除（STALE）

满足以下任一条件：

- **代码已反映**：记忆内容描述的是一个已完成的修复、已合并的 PR、已实施的决策。判断依据：记忆中提到具体的 commit SHA、PR 编号，或描述的是"已修复"、"已解决"、"已实施"等过去完成状态。代码本身就是该记忆的最终形态，不需要记忆来提醒。
- **CLAUDE.md 已覆盖**：记忆的内容现在在 `CLAUDE.md` 或 `.claude/rules/` 中有更权威的表述。CLAUDE.md 是项目级别的持久指令，auto memory 中的重复内容应删除。
- **纯操作记录**：记忆是"我们做了 X"、"花了 N 小时调试 Y"等操作日志，没有持续参考价值。这类信息在 git history 和会话记录中，不需要留在 auto memory 里。
- **时间上已过时**：记忆发生在很久以前且描述的状态已明显改变（如"当前版本 v0.1.0"但项目已到 v0.4.0）。

#### 📦 可合并（DUPLICATE / MERGEABLE）

满足以下任一条件：

- **重复内容**：多条记忆描述同一件事，措辞相近。保留最完整、最准确的一条，合并其他。
- **可整合**：多条记忆属于同一主题（如"API 设计约定"、"测试策略"），可以合并为一条综合性的 topic file，减少 MEMORY.md 的行数。
- **父/子关系**：一条 topic file 被另一条完全覆盖或包含。

#### ⚠️ 孤立引用（ORPHANED）

满足以下任一条件：

- MEMORY.md 中引用了一个 topic file，但该文件已被删除 → 从 MEMORY.md 中移除该行
- memory 目录中存在一个 `.md` 文件，但 MEMORY.md 中没有任何行指向它 → 要么添加到 MEMORY.md，要么删除该文件
- MEMORY.md 超过 200 行 / 25KB 加载上限，超出部分中的条目 → 这些条目从未被加载过，等同于"无声的孤立"。标记它们，让用户决定是保留还是删除

#### ✅ 保留（KEEP）

满足以下任一条件：

- **活跃约束**：记录的是一个仍在生效的决策、限制或约定，且没有在 CLAUDE.md 中体现
- **已知问题**：记录的是一个尚未修复的 bug、待解决的 issue 或已知的限制
- **架构决策**：记录的是一个重要的架构决策（ADR-like），对理解代码设计有帮助
- **调试/构建经验**：记录的是"如果遇到 X 错误，试试 Y 做法"这类对 future sessions 有价值的信息

#### ❓ 不确定（UNCERTAIN）

不符合以上任何条件的，或混合了多种特征难以判断的 → 标记为"不确定"，让用户决定。

### 第四步：生成清理报告

无论哪种模式，都生成一个结构化的报告：

```
## Memory Cleanup Report

### 概览
- 总计: N 条记忆
- MEMORY.md: N 行 / N KB（加载上限 200 行 / 25KB）
- Topic files: N 个文件，共 N 行 / N KB

### 建议清理
- 🗑 可删除: N 条
  - [title] — 原因
- 📦 可合并: N 组
  - [title] + [title] → 合并为 [title]
- ⚠️ 孤立引用: N 处
  - [description]

### 保留
- ✅ N 条

### 不确定
- ❓ N 条 — 需用户确认
  - [title] — 原因
```

### 第五步：执行清理

根据模式执行：

- **`--dry-run`**（只看不删）：只输出报告，问用户是否满意，或者是否需要进一步检查某些条目。不修改任何文件。
- **默认模式**（逐条确认）：输出报告后，对"可删除"和"可合并"的条目，逐条询问用户是否确认执行。先处理删除，再处理合并。对"不确定"的条目，询问用户决定。
- **`--force`**（自动清理）：输出报告摘要，然后直接执行所有"可删除"和"可合并"的清理操作。对"不确定"的条目，跳过并列出。

### 第六步：清理后验证

执行清理后：

1. 重新读取 MEMORY.md，确认行数减少
2. 验证所有 topic file 引用仍然有效（没有 dangling references）
3. 报告清理结果：
   ```
   ## Cleanup Complete
   - 删除了 N 条记忆
   - 合并了 N 组记忆（减少 N 条）
   - 修复了 N 处孤立引用
   - MEMORY.md 从 N 行减至 N 行
   ```

## 判断策略

### 保守原则

- **存疑即保留**：如果无法确定一条记忆是否有价值，不要删除。标记为"不确定"让用户决定。
- **CLAUDE.md 优先**：如果一条记忆的内容被 CLAUDE.md 覆盖了，auto memory 中应删除（因为 CLAUDE.md 更权威、更持久）。但反之不成立——不要因为 auto memory 中有某条记录就把 CLAUDE.md 的内容删掉。
- **代码优先**：如果一条记忆描述的是"我们修复了 X bug"，而代码中已经包含了该修复，这条记忆可以删除。代码是最终的真相来源。

### 信号词（辅助判断）

以下词汇在记忆内容中出现时，通常意味着该条目可能已过时：

- "已修复"、"已合并"、"已解决"、"已完成"、"已关闭"
- "fixed"、"merged"、"resolved"、"completed"、"closed"、"done"
- 引用具体的 commit SHA 或 PR 编号（如 `#21`、`f415b6b`）

以下词汇在记忆内容中出现时，通常意味着该条目还有参考价值：

- "注意"、"小心"、"限制"、"约束"、"已知问题"
- "note"、"caution"、"limitation"、"constraint"、"known issue"
- "workaround"、"workaround"、"hack"、"temporary"
- 以 "如果遇到 X，试试 Y" 开头的模式

### 数量控制

- MEMORY.md 保持在 50-100 行之间是最优状态
- 超过 150 行就应该考虑清理
- 超过 200 行意味着超出的条目在 session 启动时不会被加载，它们已经"事实上的丢失"了——但用户不知道丢了什么

## 参考

- 官方文档: https://code.claude.com/docs/en/memory.md
- 加载上限: MEMORY.md 前 200 行或 25KB
- 存储位置: `~/.claude/projects/<project>/memory/`