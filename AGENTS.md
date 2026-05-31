# jason-skill-hub — AGENTS.md

AI Skill Hub：托管 Agent Skill 文件，通过 CDN 分发给所有 AI agent。
技术栈：静态站点（Netlify）+ Node.js 工具链（scan.js / sync-watch.js）+ GitHub Actions CI。

## 架构说明

**单一源原则**：所有 skill 文件的真实来源是 `~/.agents/skills/`，本仓库的 `skills/` 目录是指向它的 Windows 目录联接（`mklink /J`）。

```
~/.agents/skills/（唯一编辑源）
    ↓ mklink /J（自动同步）
jason-skill-hub/skills/（透明镜像，不直接编辑）
    ↓ scan.js 生成索引
    ↓ git push
GitHub → CDN (jsdelivr) → 云端 agent
```

**关键影响**：
- 在 `jason-skill-hub/skills/` 下直接修改文件**不会持久化**——重新同步后会被 `.agents/skills/` 的内容覆盖
- 所有 skill 编辑必须在 `~/.agents/skills/` 进行
- `scan.js` 生成的索引文件（`SKILLS_INDEX.md`、`skills.json`）在仓库根目录，不在 `skills/` 下

## Dev Environment

| 命令 | 用途 |
|------|------|
| `node scripts/scan.js` | 扫描 skills/ 目录，生成 SKILLS_INDEX.md + skills.json + _redirects |
| `node scripts/sync-watch.js --once` | 手动触发一次同步（scan + git push） |
| `node scripts/sync-watch.js` | 启动监听模式（chokidar 监听 .agents/skills/ 变化，自动 push） |
| `node scripts/sync-watch.js --once --dry-run` | 试运行，不实际 push |

## Build & Test

本项目没有传统意义上的 build/test。核心验证：
- `node scripts/scan.js` 成功执行，生成文件无报错
- CI 有两个 GitHub Actions workflow：
  - `Auto Fix Skill Index`：自动检测索引文件是否需要更新并 push
  - `Validate Skill Index`：PR 时验证索引文件是最新的

## Project Structure

| 路径 | 用途 |
|------|------|
| `skills/` | 指向 `~/.agents/skills/` 的目录联接（不要直接编辑） |
| `scripts/scan.js` | 扫描 skills 目录，生成索引文件 |
| `scripts/sync-watch.js` | 监听 .agents/skills/ 变化，自动 git push |
| `scripts/sync-lib.js` | 同步核心库（runBuild + gitCommitAndPush） |
| `scripts/config.js` | 项目配置（路径、URL、同步间隔） |
| `scripts/scheduled-task-prompt.md` | 定时推送任务的 prompt 模板 |
| `SKILLS_INDEX.md` | scan.js 生成的 skill 目录索引（根目录） |
| `skills.json` | scan.js 生成的结构化 skill 列表（根目录） |
| `INDEX_HEADER.md` | INDEX.md 的头部模板（根目录） |
| `_redirects` | Netlify 重定向规则（根目录，scan.js 生成） |
| `.github/workflows/` | CI workflow 定义 |

## Code Style & Conventions

- **脚本文件**：Node.js CommonJS（`require`），不用 ES modules
- **配置文件**：`config.js` 集中管理所有路径和 URL
- **生成文件**：`SKILLS_INDEX.md`、`skills.json`、`_redirects` 由 scan.js 自动生成，不要手动编辑

## Boundaries

- ✅ **可以**：修改 `scripts/` 下的工具脚本、`.github/workflows/`、`config.js`
- ✅ **可以**：在 `~/.agents/skills/` 中编辑 skill 文件（通过符号链接自动反映到 hub）
- 🚫 **不要**：直接编辑 `jason-skill-hub/skills/` 下的文件（会被覆盖）
- 🚫 **不要**：手动编辑 `SKILLS_INDEX.md`、`skills.json`、`_redirects`（scan.js 生成）
- 🚫 **不要**：提交包含 API key / token / secret 的文件（全局 pre-commit hook 会拦截）

## Commit 规范

- 格式：`<type>: <description>`
- type 前缀：`feat` / `fix` / `refactor` / `chore` / `docs`
- 示例：`fix: validate.yml 路径更新`
- auto-sync 提交的格式固定为：`sync: auto-sync skills from source [timestamp]`

## Secret 防护

全局 pre-commit hook（`~/.git-hooks/pre-commit`）已配置，会自动检测并阻止包含以下模式的 commit：
- API key 赋值（`api_key = "xxx"`）
- 已知 key 前缀（`sk-`、`gsk-`、`ghp_`、`github_pat_` 等）
- 如果误报需要跳过：`git commit --no-verify`

## Common Pitfalls

1. **不要在 hub 的 skills/ 目录下编辑文件**——改了也会被 sync-watch 覆盖
2. **scan.js 生成路径是根目录**——不是 `skills/INDEX.md`，是 `SKILLS_INDEX.md`
3. **CI 失败先看路径**——如果 validate/auto-fix 报 failure，首先检查生成文件路径是否匹配
4. **force push 后需要重新 rebase**——如果本地落后于 remote，先 `git pull --rebase`
