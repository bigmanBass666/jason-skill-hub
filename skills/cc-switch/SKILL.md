---
name: cc-switch
description: "管理和操作 cc-switch 配置数据库。当用户提到 cc-switch、provider 管理、MCP 服务器配置、AI 供应商切换、故障转移设置、代理配置时触发。覆盖：添加/删除/切换 provider、MCP 服务器管理、Skills 管理、Prompts 管理、Failover 队列、Proxy 配置、环境检查。即使用户只是说「加个 AI 供应商」「切一下 provider」「看看 cc-switch 配置」也应触发。"
---

# cc-switch 配置管理

cc-switch 通过 SQLite 数据库集中管理多个 AI 客户端的 MCP 服务器、Provider 和本地代理配置。

## 工具选择

根据操作类型选择 CLI 或 SQL：

- **CLI**：switch/list/current、MCP、Skills、Prompts、Failover、Proxy、Config、Env
- **SQL**：add/edit/delete Provider（CLI 是交互式的，agent 无法使用）

## 关键路径

| 资源 | 路径 |
|------|------|
| CLI | `D:\apps\cc-switch-cli\cc-switch.exe` |
| 数据库 | `$env:USERPROFILE\.cc-switch\cc-switch.db` |
| 设置文件 | `$env:USERPROFILE\.cc-switch\settings.json` |

## 数据库操作规范

使用 `sqlite3` CLI 执行 SQL，查询时加 `-header -column` 格式化输出。

**操作前必须**：
1. 关闭 cc-switch GUI（否则检测到外部修改会触发设置重置）
2. 备份数据库
3. 插入 provider 时同时插入 `provider_endpoints` 记录

```powershell
# 备份
$ts = Get-Date -Format "yyyyMMdd_HHmmss"
$dbPath = "$env:USERPROFILE\.cc-switch\cc-switch.db"
Copy-Item $dbPath "$dbPath.backup_$ts"
```

PowerShell 中 sqlite3 的正确用法：写 `.sql` 文件后管道传入（避免 JSON 转义问题）：

```powershell
$sql = @"
INSERT INTO providers (...) VALUES (...);
INSERT INTO provider_endpoints (...) VALUES (...);
"@
$sql | Out-File -FilePath "insert.sql" -Encoding utf8 -NoNewline
Get-Content "insert.sql" | sqlite3 $dbPath
```

## Provider 管理

### CLI 操作

```powershell
$ccs = "D:\apps\cc-switch-cli\cc-switch.exe"

# 列出、显示当前、切换
& $ccs provider list --app claude
& $ccs provider current --app claude
& $ccs provider switch <ID> --app claude
```

### SQL 操作

详细的表结构和 JSON 格式见 `references/provider-schemas.md`。

**添加 Provider 示例**：

```powershell
$dbPath = "$env:USERPROFILE\.cc-switch\cc-switch.db"

$sql = @"
INSERT INTO providers (id, app_type, name, settings_config, meta, created_at, is_current, in_failover_queue, cost_multiplier)
VALUES ('my-provider', 'claude', 'My Provider', '{"env":{"ANTHROPIC_BASE_URL":"https://api.example.com","ANTHROPIC_AUTH_TOKEN":"sk-xxx"}}', '{"apiFormat":"anthropic","endpointAutoSelect":true}', strftime('%s','now')*1000, 0, 0, '1.0');

INSERT INTO provider_endpoints (provider_id, app_type, url, added_at)
VALUES ('my-provider', 'claude', 'https://api.example.com', strftime('%s','now')*1000);
"@
$sql | Out-File -FilePath "insert.sql" -Encoding utf8 -NoNewline
Get-Content "insert.sql" | sqlite3 $dbPath
```

**更新/删除**：

```powershell
# 更新
sqlite3 $dbPath "UPDATE providers SET settings_config = '<JSON>' WHERE id = '<id>' AND app_type = '<app_type>';"

# 删除
sqlite3 $dbPath "DELETE FROM provider_endpoints WHERE provider_id = '<id>' AND app_type = '<app_type>';"
sqlite3 $dbPath "DELETE FROM providers WHERE id = '<id>' AND app_type = '<app_type>';"
```

## MCP 服务器管理

```powershell
$ccs = "D:\apps\cc-switch-cli\cc-switch.exe"

& $ccs mcp list
& $ccs mcp enable <ID> --app claude
& $ccs mcp disable <ID> --app claude
& $ccs mcp sync
& $ccs mcp import --app claude
```

添加 MCP（SQL）：

```powershell
$sql = @"
INSERT OR REPLACE INTO mcp_servers (id, name, server_config, description, tags, enabled_claude, enabled_codex, enabled_gemini, enabled_opencode, enabled_hermes)
VALUES ('my-mcp', 'My MCP', '{"type":"stdio","command":"npx","args":["-y","@scope/package"]}', '描述', '[]', 1, 0, 0, 0, 0);
"@
```

## Skills / Prompts / Failover / Proxy / Config / Env

这些功能通过 CLI 完整支持：

```powershell
$ccs = "D:\apps\cc-switch-cli\cc-switch.exe"

# Skills
& $ccs skills list | discover | install | uninstall | enable | disable | sync

# Prompts
& $ccs prompts list --app claude | current | activate | deactivate

# Failover
& $ccs failover show | enable | disable | list | add | remove | move

# Proxy
& $ccs proxy show | enable | disable

# Config
& $ccs config show | path | backup | restore | export | import

# Env
& $ccs env check | list | tools
```

## API Key 测试

添加 provider 前测试 key 是否可用：

```powershell
# Anthropic 兼容接口
curl.exe -s -w "\n%{http_code}" "$url/anthropic/v1/messages" `
  -H "x-api-key: $key" -H "anthropic-version: 2023-06-01" `
  -H "content-type: application/json" `
  -d '{"model":"xxx","max_tokens":10,"messages":[{"role":"user","content":"Hi"}]}'

# OpenAI 兼容接口
curl.exe -s -w "\n%{http_code}" "$url/v1/chat/completions" `
  -H "Authorization: Bearer $key" -H "Content-Type: application/json" `
  -d '{"model":"xxx","max_tokens":10,"messages":[{"role":"user","content":"Hi"}]}'

# 获取模型列表
curl.exe -s "$url/v1/models" -H "Authorization: Bearer $key"
```

HTTP 200 = 可用，401 = key 无效，400 = 模型名错或请求格式问题。

## 常见问题

**Provider 切换后不生效**：检查环境变量冲突（`cc-switch env check`），重启终端。

**JSON 格式错误**：参考同 app_type 的现有 provider：`sqlite3 $dbPath "SELECT settings_config FROM providers WHERE app_type = 'claude' LIMIT 1;"`

**删除当前 Provider**：先切换到另一个再删除。
