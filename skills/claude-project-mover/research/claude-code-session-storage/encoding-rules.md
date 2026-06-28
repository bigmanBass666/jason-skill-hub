# encoding-rules.md — Claude Code 路径编码规则

来源：泄露源码 + 本地磁盘验证（2026-06-02）

## sanitizePath 源码（来自 v2.1.88 source map）

```typescript
export const MAX_SANITIZED_LENGTH = 200;

function simpleHash(str: string): string {
    return Math.abs(djb2Hash(str)).toString(36);
}

export function sanitizePath(name: string): string {
    const sanitized = name.replace(/[^a-zA-Z0-9]/g, '-');
    if (sanitized.length <= MAX_SANITIZED_LENGTH) {
        return sanitized;
    }
    const hash = typeof Bun !== 'undefined' ? Bun.hash(name).toString(36) : simpleHash(name);
    return sanitized.slice(0, MAX_SANITIZED_LENGTH) + '-' + hash;
}
```

```typescript
// djb2 哈希 fallback（Node.js 环境）
export function djb2Hash(str: string): number {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = ((hash << 5) - hash + str.charCodeAt(i)) | 0;
    }
    return hash;
}
```

路径获取：

```typescript
try {
    resolvedCwd = realpathSync(cwd).normalize('NFC');
} catch {
    resolvedCwd = rawCwd.normalize('NFC');
}
```

## 磁盘实际 vs 源码差异

| 特性 | 源码 `sanitizePath` | 磁盘实际（~/.claude/projects/） | 当前脚本 |
|------|---|---|---|
| 非字母数字字符 | 逐个替换为 `-`（单连字符） | `\` 变为 `--`（双连字符） | `\` → `--` |
| 路径分隔符 `/` | → `-`（单连字符） | → `--`（双连字符） | 先转 `\` 再 → `--` |
| `:` | 删除 | 删除 | 删除 |
| 大小写 | 保留 | 保留 | 保留 |
| 长路径哈希 | djb2 + `MAX_SANITIZED_LENGTH=200` | 未观察到（本地路径均<200） | 已实现 djb2 |

### 可能的解释

1. 旧版本使用双连字符，新泄露源码改成了单连字符
2. 或者源码是外层包装，实际调用前有路径标准化步骤

**以磁盘实际行为为准**（60 个目录全部验证通过）。

## 路径编码对照表（实际磁盘验证）

```
C:\Users\86150\.agents\skills\claude-project-mover
  → C--Users--86150--.agents--skills--claude-project-mover

C:\Users\86150\Documents
  → C--Users-86150-Documents

D:\BaiduSyncFolder\Test\claude-code
  → D--BaiduSyncFolder-Test--------claude-code

D:\Test\claude-test
  → D--Test-claude-test
```

注意 `D--BaiduSyncFolder-Test--------claude-code` 中 `claude` 前后有 `----`，说明路径末尾 `\` 不变会额外产生 `--`。

## WSL / MSYS2 路径风险

从 Git Bash 启动的 Claude Code 可能看到 `/c/Projects/my-app` 而非 `C:\Projects\my-app`，编码结果完全不同：

```
/mnt/c/Projects/my-app  → -mnt-c-Projects-my-app  (无 drive letter)
C:\Projects\my-app       → C--Projects-my-app      (有 drive letter)
```

同一物理目录可能产生多个编码目录，导致历史分散。
`move_project_history.py` 的 `check` 子命令会列出所有匹配目录。
