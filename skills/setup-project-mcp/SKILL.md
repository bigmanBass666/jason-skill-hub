---
name: setup-project-mcp
description: 一键在项目中注册 MCP 服务器，自动创建/更新 .mcp.json。当用户说"添加项目级 MCP"、"配置 MCP 服务器"、"register MCP"、"setup project MCP"、"帮我在项目中注册一个 MCP"或需要将某个 MCP 服务器关联到当前项目时，使用此 skill。即使配置来自其他 MCP 服务器的 deferred tools 列表（系统注入的 <system-reminder>），也应使用此 skill 将其写入 .mcp.json。
---

# Setup Project MCP

在项目根目录的 `.mcp.json` 中注册一个 MCP 服务器。如果文件已存在，合并新配置而不覆盖现有条目。

## 执行步骤

### 1. 获取配置

两种来源：
- **用户直接描述**：用户会给出名称和类型（stdio/http），有时含 command/args/url
- **系统注入的 deferred tools**：从 `<system-reminder>` 中的 deferred tools 列表提取。典型格式：
  ```
  "mcp__<server-name>__<tool-name>"
  ```
  其中的 `<server-name>` 就是 MCP 服务器名。配置中包含 `<command>` 和 `<args>`（stdio 类型）

### 2. 确定文件路径

当前工作目录的 `.mcp.json`。如果存在 `~/.claude.json` 且其中有该服务器，对于本地覆盖场景，仍然需要在项目级写入（`.mcp.json` 优先级高于用户级）。

### 3. 合并逻辑

```
如果 .mcp.json 不存在：
    创建 {"mcpServers": {<server>: <config>}}

如果 .mcp.json 存在：
    如果同名已在 mcpServers 中：
       覆盖该条目（用新配置替换）
    否则：
       添加新条目
    保持其他条目不变
```

### 4. JSON 字段映射

| 配置来源 | type=stdio | type=http |
|---------|-----------|-----------|
| 命令行 `claude mcp add --transport stdio` | command + args | N/A |
| 命令行 `claude mcp add --transport http` | N/A | url |
| 系统注入 deferred tools | command + args | N/A |
| `.claude.json` 中的 `mcpServers` | command + args | url |

示例：
```jsonc
// stdio（本地进程）
{ "type": "stdio", "command": "python", "args": ["server.py"] }

// http（远程 URL）
{ "type": "http", "url": "https://example.com/mcp" }
```

不要加 `"command"` 到 http 类型，也不要加 `"url"` 到 stdio 类型。

### 5. 写入并验证

用 Write 工具写入 `.mcp.json`。完成后：

```text
已添加/更新 MCP 服务器 "<name>" → .mcp.json

下一步：
1. 退出当前 Claude Code 会话（Exit）
2. 重新进入项目目录启动 Claude Code
3. 输入 /mcp 批准出现的服务器
4. 输入 /doctor 检查连接状态
```

## 注意事项

- 不要调用 `claude mcp add-json` CLI，直接操作 `.mcp.json`
- `env` 字段可选，默认 `{}`
- `args` 必须是数组，如果是单个字符串也要包装成数组
