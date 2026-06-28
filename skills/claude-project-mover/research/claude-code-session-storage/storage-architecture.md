# storage-architecture.md — Claude Code 会话存储架构

来源：官方文档 + 社区逆向分析（2026-06-02）

## 三层存储模型

```
本地磁盘 (authoritative)      →  SDK mirror (best-effort)
~/.claude/projects/<dir>/<session>.jsonl    SessionStore 外部存储
                                          └── 外部挂了不影响本地写入
```

| 层级 | 路径 | 性质 |
|------|------|------|
| 本地文件 | `~/.claude/projects/<encoded>/<session-id>.jsonl` | 主存储，append-only |
| 扩展数据 | `~/.claude/file-history/` | 文件 checkpoint（16-char hash） |
| 关联数据 | `~/.claude/todos/`, `~/.claude/plans/`, `~/.claude/debug/` | 随 session 清理 |

## ~/.claude/ 目录结构

```
~/.claude/
├── projects/            # 会话日志（按编码路径分目录）
│   ├── C--Users--.../   #   JSONL 文件（按 session UUID 命名）
│   └── 01f7540f-.../    #   旧版本目录（UUID 格式）
├── file-history/        # 文件版本 checkpoint（16-char hash @ version）
├── history.jsonl        # 全局 prompt 历史
├── todos/               # todo 任务列表
├── plans/               # plan mode 文档
├── debug/               # 调试日志
├── session-env/         # 会话环境变量
├── shell-snapshots/     # shell 状态快照
├── stats-cache.json     # 使用统计
└── ...
```

## JSONL 格式速览

每行一个 JSON 事件，主要类型：

| type | 说明 |
|------|------|
| `user` / `assistant` / `system` | 对话消息 |
| `file-history-snapshot` | 文件 checkpoint 引用 |
| `queue-operation` | 工具调用队列操作 |
| `compact_boundary` | 上下文压缩边界 |
| `last-prompt` | 会话结束标记 |

关键字段：`sessionId`（完整 UUID）、`cwd`（项目路径，迁移时需要修正）、`timestamp`。

## Session 生命周期

- 创建：启动新会话 → 生成 UUID → 创建 `.jsonl`
- 恢复：`/resume` → 按 `cwd` 匹配历史目录
- 分支：`/branch` → 从 compaction point 切出新 session
- 清理：30 天自动清理（`cleanupPeriodDays` 可调）
- 跨文件 continuation：一个 session 可能被拆成多个 `.jsonl` 文件

## 数据串联

```
Session UUID: 31f3f224-xxxx
├── projects/<path>/31f3f224-....jsonl   ← 对话
├── file-history/31f3f224-..../          ← 文件 checkpoint
├── todos/31f3f224-...-agent-....json    ← 任务列表
├── session-env/31f3f224-....            ← 环境变量
└── debug/31f3f224-....txt               ← 调试日志
```

## 迁移关联数据

如果项目迁移涉及 file-history 或 todos，需要同步迁移：
- `file-history/<session-uuid>/` → 原地保留（按 session UUID，不随项目路径变）
- `todos/` → 按 session UUID 存储，迁移时无需移动
- `history.jsonl` → 如果包含 project 字段指向旧路径，需要修正

> 当前 `move_project_history.py` 只处理 `projects/` 下的 JSONL，不涉及 file-history/todos。
