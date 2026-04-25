---
name: process-cleanup
description: 自动检测并清理所有残留的开发进程。当用户提到"清理进程"、"清理残留"、"结束工作"或需要释放资源时使用。支持清理 Node.js/npm、Python、Claude/MCP、Ruby 等各类开发相关进程，采用强制终止确保彻底清理。
---

# Process Cleanup Skill

自动识别并强制终止系统中所有残留的开发相关进程，释放系统资源。

## 何时使用

- 用户说"清理进程"、"清理残留"、"结束工作"
- 需要释放被占用的端口或资源
- 长时间开发后系统变慢，怀疑有僵尸进程
- 切换项目前清理环境
- 自动化开发任务结束后清理

## 支持的进程类型

这个 skill 会清理以下类型的进程：

| 进程类型 | 匹配模式 | 描述 |
|---------|---------|------|
| Node.js | `node` | Node.js 运行时（Claude 自动化开发常用） |
| npm | `npm` | npm 包管理器 |
| Python | `python`, `python3`, `pip` | Python 及 pip |
| uv | `uv` | Rust 写的 Python 包管理器（快速虚拟环境） |
| Vite | `vite` | Vite 开发服务器 |
| Claude/MCP | `claude`, `mcp` | Claude CLI 和 MCP 服务 |
| Ruby | `ruby`, `bundle`, `rails` | Ruby 及其包管理器 |
| Ruby gems | `gem` | RubyGems |
| Webpack | `webpack`, `webpack-dev-server` | Webpack 相关 |
| React scripts | `react-scripts` | Create React App |
| esbuild | `esbuild` | 前端打包工具（Claude 常用） |

## 使用方法

当用户请求清理进程时：

1. **检查当前进程状态** - 使用 `ps` 命令查看所有相关进程
2. **强制终止进程** - 使用 `kill -9` 确保彻底清理
3. **验证清理结果** - 再次检查确保无残留
4. **报告结果** - 总结清理的进程数量和类型

### 快速方式：使用内置脚本

优先使用 bundled 的清理脚本：

```bash
bash ~/.claude/skills/process-cleanup/scripts/clean.sh
```

### 详细步骤（手动）

```bash
# 1. 检查当前状态（用于报告）
ps aux | grep -E "(node|npm|python|vite|claude|mcp|ruby|bundle|webpack)" | grep -v grep

# 2. 强制终止所有匹配进程
ps -ef | grep -E "(node|npm|python|vite|claude|mcp|ruby|bundle|webpack)" | grep -v grep | awk '{print $2}' | xargs -r kill -9 2>/dev/null || true

# 3. 验证清理完成
ps aux | grep -E "(node|npm|python|vite|claude|mcp)" | grep -v grep
```

## 清理策略

- ✅ **强制终止**：直接使用 `kill -9` 确保进程立即停止
- ✅ **批量处理**：一次性清理所有匹配的进程类型
- ✅ **静默失败**：忽略不存在的进程，避免错误中断
- ✅ **完整验证**：清理后验证确保无残留

## 注意事项

- 终止的进程无法恢复，使用前确保用户已保存工作
- 可能会终止用户当前目录外的进程（跨项目清理）
- 在 Windows 环境下使用 Bash（MSYS/MinGW），`kill -9` 为强制终止
- 建议清理前询问用户确认，或在用户明确请求时直接执行
