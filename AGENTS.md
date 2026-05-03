# AI Agent 项目指南

## 项目概述
这是一个 AI Skill 托管仓库，将 skills 通过 CDN URL 暴露给任何 AI agent 自动索引和读取。

## Skills CDN 地址
- **INDEX.md**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/INDEX.md
- **skills.json**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/skills.json

## Skills 同步机制（重要）

本项目的 `skills/` 文件夹**不是手动编辑的**，而是从源头文件夹自动镜像同步过来的：

- **源头文件夹**: `C:\Users\86150\.agents\skills`（统一 skills 源）
- **同步方向**: 源头 → 项目 `skills/`（单向镜像）
- **同步间隔**: 最少 5 分钟一次

### 你需要知道的
1. **不要手动编辑 `skills/` 下的文件** — 任何修改都会在下次同步时被源头覆盖
2. **如需修改 skill 内容** — 去源头文件夹 `C:\Users\86150\.agents\skills` 编辑
3. **如需新增/删除 skill** — 在源头文件夹操作，同步会自动反映到项目
4. **`skills/INDEX.md`、`skills/skills.json`** 是由 `scripts/scan.js` 自动生成的，不要手动编辑

### 同步命令
```bash
npm run sync          # 启动守护进程，持续监听源头变化并自动同步
npm run sync:once     # 执行一次同步（同步 → 构建 → git commit & push）
npm run sync:dry-run  # 预览模式，只输出变更列表不实际执行
```

### 同步流程
源头变化 → 镜像同步到 `skills/` → 运行 `scan.js` 重建索引 → git commit & push

### NSSM 服务（可选）
可通过 `scripts\sync-service.bat install` 注册为 Windows 服务，实现开机自启和崩溃自动重启。

## 引用关系
当 SKILL.md 中引用了相对路径的附属文件时，按以下规则推断完整 URL：
1. 当前 SKILL.md URL 去掉文件名，保留目录路径
2. 拼接相对路径，去掉 `./` 前缀
3. 示例：SKILL.md 在 `.../arch-design/SKILL.md`，引用 `./references/guide.md` → `.../arch-design/references/guide.md`
