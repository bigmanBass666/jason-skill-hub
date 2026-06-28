# jason-skill-hub

Skill CDN 分发仓库。`~/.agents/skills/` → `mklink /J` → GitHub → jsDelivr CDN。

## 一句话规则

**改 skill 去 `~/.agents/skills/`，别碰 `skills/`。** `skills/` 是目录联接，改了也会被覆盖。

## 架构

```
~/.agents/skills/          ← 唯一编辑源
    ↓ mklink /J（同一份文件）
jason-skill-hub/skills/    ← 透明镜像
    ↓ git push
GitHub → jsDelivr CDN      ← CI 自动 purge 缓存
```

## 常用命令

| 命令 | 用途 |
|------|------|
| `node scripts/scan.js` | 重新生成索引（SKILLS_INDEX.md + _redirects） |
| `node scripts/sync-watch.js --once` | 手动同步：scan + git commit + push |
| `git commit --no-verify` | 跳过 pre-commit hook（误报时用） |

## 防护机制

- **`.skillignore`** — scan.js 扫描时跳过 `__pycache__/`、`*-workspace/`、`*.zip`、`*.pyc`
- **`.gitignore`** — 同上，阻止 git 追踪
- **`~/.git-hooks/pre-commit`** — 全局 hook，拦截 API key/secret 提交
- **CI purge** — push 后自动全量刷新 jsDelivr CDN 缓存

## 给 AI Agent 的完整文档

[AGENTS.md](./AGENTS.md) — 架构说明、编辑规则、commit 规范、边界约束。所有 AI coding tools 共享此文件。