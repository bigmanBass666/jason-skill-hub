---
name: claude-project-mover
description: 在两个项目路径之间同步 Claude 会话历史（非搬文件）。覆盖两种场景：(1) 全量历史迁移 — 用户自己搬了项目文件夹后迁移所有历史会话；(2) 单会话同步 — 把当前或指定会话复制到另一项目目录（worktree / 多目录场景）。当用户说"搬项目"、"迁移历史"、"同步聊天记录"、"sync session"、"保留对话"、"claude 历史不见了"、"change project path but keep history"、"relocate project"、"move this folder but keep claude history"时触发。
---

# Claude Project Mover — 会话历史同步

⚠ **默认只读副本操作。** 本 skill 的所有处理均在副本上执行，绝不碰源文件。**删除旧历史目录或旧项目目录必须由用户手动确认后自行操作。**

调用 `python move_project_history.py` 同步 `~/.claude/projects/` 下的会话。核心逻辑：复制模式（不动源）+ JSONL 中 `cwd` 字段修正。

## 场景 1：全量历史迁移（migrate）

用户自己用 git / mv / cp 把项目文件夹搬到了新位置，需要将所有历史会话迁移到新项目路径。

```powershell
python move_project_history.py check "D:\旧路径" "D:\新路径"
python move_project_history.py migrate "D:\旧路径" "D:\新路径"
```

## 场景 2：单会话同步（sync-session）

用户有多个 worktree，或想在另一目录继续当前对话。将当前（或指定）会话复制到目标项目目录。

```powershell
# 同步最新会话
python move_project_history.py sync-session "D:\src" "D:\dst"

# 指定会话 ID
python move_project_history.py sync-session --session <uuid> "D:\src" "D:\dst"
```

## 通用选项

| 选项 | 说明 |
|------|------|
| `--dry-run` | 预览将要执行的操作，不实际修改文件 |
| `--no-backup` | 不创建备份（仅 migrate 场景） |

任何操作前先用 `--dry-run` 预览再执行。

## 删除指引

确认新路径下的历史会话无误后，再手动清理旧目录：
1. 删除旧项目目录：`Remove-Item -Recurse "D:\旧项目路径"`
2. 删除旧历史记录：`Remove-Item -Recurse "~/.claude/projects/<旧项目名>"`

