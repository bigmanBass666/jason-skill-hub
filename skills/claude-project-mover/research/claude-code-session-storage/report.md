找到了全部关键源码。整理发现：

## `sanitizePath` —— 源码级实现

```typescript
// src/utils/sessionStoragePortable.ts
export function sanitizePath(name: string): string {
  const sanitized = name.replace(/[^a-zA-Z0-9]/g, '-')
  if (sanitized.length <= MAX_SANITIZED_LENGTH) {
    return sanitized
  }
  const hash = typeof Bun !== 'undefined' ? Bun.hash(name).toString(36) : simpleHash(name)
  return `${sanitized.slice(0, MAX_SANITIZED_LENGTH)}-${hash}`
}
```

**就这一行正则**——所有非字母数字字符统一替换为 `-`。

## Windows 上的完整流程

```
process.cwd()          → "U:\Projects\my-app"
         ↓ realpathSync + normalize('NFC')  (无转义符变化！)
originalCwd            → "U:\Projects\my-app"
         ↓ sanitizePath
~/.claude/projects/    → "U--Projects-my-app/"
```

## 关键发现：问题在哪里

**`sanitizePath` 上游没有任何路径规范化**。源码里没有：
- `\\` → `/` 的替换
- `realpathSync` 只做符号链接解析和 NFC 归一化，不做分隔符转换
- `normalize()` (Node.js path) 只处理 `.`/`..`，不分隔符转换

所以在 Windows 上，**同一目录的不同 cwd 表示会编码到不同目录**：

| 同一目录的 cwd 变体           | `sanitizePath` 结果     | 是否相同   |
| ----------------------------- | ----------------------- | ---------- |
| `U:\Projects\my-app`          | `U--Projects-my-app`    |            |
| `U:/Projects/my-app`          | `U--Projects-my-app`    | 碰巧相同   |
| `/u/Projects/my-app` (MSYS2)  | `-u-Projects-my-app`    | **不同！** |
| `\\server\share\my-app` (UNC) | `--server-share-my-app` | **不同！** |
| `C:\Users\Me\my-app`          | `C--Users-Me-my-app`    |            |

这就是 GitHub issue #54865 报告的 bug 根因——Windows + MSYS2/WSL 用户通过不同路径表示进入同一目录，编码后目录不同，导致历史会话"丢失"。

## 对你的工程的影响

你的 `claude-project-mover` 当前 SKILL.md 里的编码规则：

```powershell
$oldName = "<源路径>" -replace ':','' -replace '\\','-'
```

这个实现本身 **和源码逻辑一致**（`:` 删除 + `\` → `-`），因为源码的 `[^a-zA-Z0-9]` 也删除了 `:`。但要特别注意：

1. `/` 变 `-`：`.replace('\\','-')` 只替换了反斜杠，如果路径里有正斜杠（比如从 Git Bash 过来的路径），PowerShell 的 `-replace` 默认用正则，`':'` 在正则里是普通字符，`'\\'` 在正则里是字面 `\`——两者都没问题
2. MSYS2/WSL 路径：路径里可能没有 drive letter，直接以 `/u/` 或 `/mnt/d/` 开头，编码结果和 Windows 原生路径完全不同