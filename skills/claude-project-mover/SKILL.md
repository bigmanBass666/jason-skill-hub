---
name: claude-project-mover
description: 在两个项目路径之间同步 Claude 会话历史（非搬文件）。覆盖两种场景：(1) 全量历史迁移 — 用户自己搬了项目文件夹后迁移所有历史会话；(2) 单会话同步 — 把当前或指定会话复制到另一项目目录（worktree / 多目录场景）。当用户说"搬项目"、"迁移历史"、"同步聊天记录"、"sync session"、"保留对话"、"claude 历史不见了"、"change project path but keep history"、"relocate project"、"move this folder but keep claude history"时触发。注意：用户说"聊天记录不见了"或"历史会话不见了"通常也是这个 skill 的触发场景——先检查 `~/.claude/projects/` 下的目录是否存在且名字匹配实际项目路径。
---

# Claude Project Mover — 会话历史同步

⚠ **默认只读副本操作。** 本 skill 的所有处理均在副本上执行，绝不碰源文件。**删除旧历史目录或旧项目目录必须由用户手动确认后自行操作。**

## 核心逻辑

Claude 执行脚本（Bash），用户提供路径。流程：

1. **确认路径** — 和用户确认旧项目路径和新项目路径
2. **check 预览** — 用 `--dry-run` 检查要迁移的内容
3. **migrate 执行** — 用户确认后执行迁移
4. **清理** — 指导用户手动删除旧记录

## 路径转换规则（重要）

Claude Code 将项目路径转为历史目录名的规则（实测验证）：

| 输入 | 转换 | 说明 |
|------|------|------|
| `D:\` | `D--` | 盘符 `:` + 分隔符 `\` → `--` |
| `\` 或 `/` | `-` | 路径分隔符 → `-` |
| `_` `.` `!` `@` `#` 等 | `-` | 非字母数字字符 → `-` |
| Unicode/中文 | `-` | 全部 Unicode 非 ASCII 字母数字 → `-` |
| `a-z` `A-Z` `0-9` | 原样保留 | 字母和数字保留 |
| `-` | `-` | 连字符保留（但与路径分隔符无法区分） |

**一句话：仅保留 `[a-zA-Z0-9]`，其余所有字符 → `-`**

**worktree 目录命名规则：**
- 主项目路径编码后，追加 `--claude-worktrees-<worktree名>`
- 示例：`D:\Work\Projects\AK-Switch` → `D--Work-Projects-AK-Switch`（主目录）
- 示例：`D:\Work\Projects\AK-Switch` 的 worktree `cli-logs` → `D--Work-Projects-AK-Switch--claude-worktrees-cli-logs`

## 脚本路径

所有脚本在 skill 目录的 `scripts/` 下。skill 目录路径通过 `$(dirname "$(realpath "$0")")` 动态获取，Claude 直接调用即可。

```bash
SKILL_DIR="D:/Users/86150/.claude/skills/claude-project-mover"
python3 "$SKILL_DIR/scripts/move_project_history.py" <command> <args>
```

## 场景 1：全量历史迁移（migrate）

用户用 git / mv / cp 把项目文件夹搬到新位置后，迁移所有历史会话。

**worktree 自动迁移：** 如果旧项目有 worktree 会话（`<主目录>--claude-worktrees-*`），`migrate` 会自动发现并同步它们到新项目路径。同步后会话也会备份到主项目目录，方便 `-r` 查找。

```bash
# 1. 预览
python3 "$SKILL_DIR/scripts/move_project_history.py" check "旧路径" "新路径"

# 2. 迁移（会创建备份）
python3 "$SKILL_DIR/scripts/move_project_history.py" migrate "旧路径" "新路径"
```

## 场景 2：单会话同步（sync-session）

用户有多个 worktree，或想在另一目录继续当前对话。

**worktree 会话查找：** 如果指定会话 ID 在主项目目录中找不到，`sync-session` 会自动搜索 worktree 目录。找到后会同步到新项目的对应 worktree 目录 + 主项目目录。

```bash
# 同步最新会话（先 dry-run）
python3 "$SKILL_DIR/scripts/move_project_history.py" sync-session --dry-run "源路径" "目标路径"
python3 "$SKILL_DIR/scripts/move_project_history.py" sync-session "源路径" "目标路径"

# 指定会话 ID（支持 worktree 中的会话）
python3 "$SKILL_DIR/scripts/move_project_history.py" sync-session --session <uuid> "源路径" "目标路径"
```

## 通用选项

| 选项 | 说明 |
|------|------|
| `--dry-run` | 预览将要执行的操作，不实际修改文件 |
| `--no-backup` | 不创建备份（仅 migrate 场景） |

**任何实际修改操作前，必须先用 `--dry-run` 让用户确认。**

## 路径查询工具

`scripts/path_to_dirname.py` 是一个独立 CLI 工具，用于查询任意项目路径对应的历史目录名：

```bash
python3 "$SKILL_DIR/scripts/path_to_dirname.py" "D:\Working\programming_projects\AK-Switch"
# 输出: D--Working-programming-projects-AK-Switch

# 自测
python3 "$SKILL_DIR/scripts/path_to_dirname.py" --test
```

用于调试和验证路径转换是否正确。

## 删除指引

确认新路径下的历史会话无误后，**告诉用户手动执行**：

```powershell
Remove-Item -Recurse "~/.claude/projects/<旧目录名>"
```

不要自己删，让用户确认后自己操作。