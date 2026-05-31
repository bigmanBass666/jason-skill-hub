---
name: claude-project-mover
description: 移动项目文件夹并同步更新 Claude 聊天记录路径，确保移动后对话历史不丢失。当用户说"移动项目"、"搬项目"、"把XX移到别处但保留聊天记录"、"relocate project"、"move this folder but keep claude history"、"换位置但保留对话"时触发。即使只说"帮我搬个项目"也应触发。
---

# Claude Project Mover

用户要求移动项目时，必须同步更新 `~/.claude/projects/` 下的聊天记录目录名，否则历史对话会"丢失"。

## 编码规则

Claude 把项目绝对路径编码成目录名：
- `\` → `-`
- `:` → 去掉
- 大小写保留

示例：`D:\Test\claude_test\claude-mem-trae` → `D--Test-claude-test-claude-mem-trae`

## 执行流程

### 1. 确认路径
问清楚源路径和目标路径，如果用户没说清楚，必须追问。

### 2. 检查历史记录是否存在
```powershell
$oldName = "<源路径>" -replace ':','' -replace '\\','-'
$historyDir = "$env:USERPROFILE\.claude\projects\$oldName"
Test-Path $historyDir
```
不存在则跳过历史迁移，直接执行第 3 步。

### 3. 移动项目
```powershell
Move-Item -Path "<源路径>" -Destination "<目标路径>"
```
目标位置已有同名文件夹时，先问用户是否覆盖，不要直接执行。

### 4. 重命名历史记录目录（如果有）
```powershell
Rename-Item $historyDir -NewName ("<目标路径>" -replace ':','' -replace '\\','-')
```

### 5. 修正 JSONL 中的 cwd 字段（关键）

Claude Code 用 JSONL 中的 `cwd` 字段匹配项目路径。目录重命名后 cwd 仍指向旧路径，必须替换：

```python
import json
from pathlib import Path

history_dir = Path.home() / ".claude" / "projects" / "<新编码目录名>"
old_cwd = r"<源路径>"
new_cwd = r"<目标路径>"

for f in history_dir.glob("*.jsonl"):
    lines = []
    changed = 0
    with open(f, "r", encoding="utf-8") as fh:
        for line in fh:
            try:
                d = json.loads(line.strip())
                if d.get("cwd") == old_cwd:
                    d["cwd"] = new_cwd
                    line = json.dumps(d, ensure_ascii=False) + "\n"
                    changed += 1
            except:
                pass
            lines.append(line)
    with open(f, "w", encoding="utf-8") as fh:
        fh.writelines(lines)
    print(f"  {f.name}: {changed} cwd entries fixed")
```

> **为什么不能用字符串替换？** JSONL 中路径的反斜杠是双转义的（`D:\\\\Test`），直接字符串替换匹配不到。必须通过 `json.loads` → 修改 → `json.dumps`。

### 6. 告知用户
确认两个操作都成功，告诉用户：
> 项目已移至 `<目标路径>`，聊天记录已同步。下次在新位置打开 Claude 时历史对话会自动恢复。
