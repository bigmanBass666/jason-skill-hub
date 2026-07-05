---
name: cc-switch
description: "管理和操作 cc-switch 配置数据库。当用户提到 cc-switch、provider 管理、MCP 服务器配置、AI 供应商切换、故障转移设置、代理配置时触发。覆盖：添加/删除/切换 provider、MCP 服务器管理、Skills 管理、Prompts 管理、Failover 队列、Proxy 配置、环境检查。即使用户只是说「加个 AI 供应商」「切一下 provider」「看看 cc-switch 配置」也应触发。"
disable-model-invocation: true
---

# cc-switch 配置管理

cc-switch 通过 SQLite 数据库集中管理 AI 客户端的 MCP、Provider 和本地代理。

## 关键路径

| 资源 | 路径 |
|------|------|
| CLI | `D:\apps\cc-switch-cli\cc-switch.exe` |
| GUI（管理路由） | `D:\apps\CC Switch\cc-switch.exe` |
| 数据库 | `$env:USERPROFILE\.cc-switch\cc-switch.db` |

## 先决条件

调用任何命令前，先验证环境：

```powershell
$ccs = "D:\apps\cc-switch-cli\cc-switch.exe"
$dbPath = "$env:USERPROFILE\.cc-switch\cc-switch.db"

# 1. CLI 存在
if (-not (Test-Path $ccs)) { Write-Host "❌ CLI 不存在: $ccs"; return }

# 2. 数据库存在
if (-not (Test-Path $dbPath)) { Write-Host "❌ 数据库不存在: $dbPath"; return }

# 3. CLI 版本检查（如果遇到版本不兼容错误）
& $ccs --version
# 如果报 "当前应用: vX.Y.Z，最高支持数据库版本: N" → 先升级
# & $ccs update
```

每次操作前，用 `$ccs` 和 `$dbPath` 变量引用 CLI 和数据库。

## 如何调用 CLI

```powershell
$ccs = "D:\apps\cc-switch-cli\cc-switch.exe"

# 查看可用命令
& $ccs --help
& $ccs mcp --help           # MCP 子命令
& $ccs provider --help      # Provider 子命令

# 查看具体子命令的参数
& $ccs mcp list --help
& $ccs mcp enable --help
```

---

## 工具选择决策指南

遇到操作请求时，按以下顺序判断用哪个工具：

```
1. 这是读操作还是写操作？
   ↓
2. CLI 有对应的子命令吗？
   ├── 有 → 用 --help 确认参数 → 直接调用 CLI
   └── 没有 → 下一步
   ↓
3. 这个操作是交互式的吗？
   ├── 非交互 → 直接调用 CLI
   └── 交互式 ↓
   ↓
4. 必须改数据库吗？
   ├── 必须改 → SQL（先停 GUI 避免关路由）
   ├── 能改 .claude.json 解决 → 直接改 .claude.json（路由安全，但可能被覆盖）
   └── 两样都不行 → 告知用户手动操作（GUI 里改）
```

**简版：**

| 操作类型 | 工具 | 路由影响 |
|---------|------|---------|
| 查看/列出 | CLI 直接查 | ✅ 无 |
| 启用/禁用 MCP | `mcp enable/disable` | ✅ 无 |
| 切换 provider | `provider switch` | ✅ 无 |
| 编辑通用模板 | `config common set --snippet` | ✅ 无 |
| 查看路由/环境 | `proxy show` / `env check` | ✅ 无 |
| 改 MCP server_config | SQL（先停 GUI）或 改 .claude.json | ⚠️ 看操作 |
| 增删 provider | SQL（先停 GUI） | ⚠️ 看操作 |
| 同步数据库到文件 | `mcp sync` | ✅ 无 |
| 交互式命令（mcp add/delete 等） | 告知用户手动操作 | — |

---

## ⚠️ 核心：路由副作用

**SQL 直写数据库**（`sqlite3` 直接修改）会触发 cc-switch GUI 的安全机制——**自动关闭本地代理路由**。

路由状态存在 **GUI 进程内存** 中：
- ❌ 改 `proxy_config` 表的 `enabled` 字段没用
- ❌ `proxy enable` 在 Windows 上不支持
- ❌ 无法程序化抢回，被关了只能 GUI 里手动打开

**唯一安全的改库方式：先停 GUI，再操作。**

```powershell
# 1. 停 GUI
Stop-Process -Name "cc-switch" -Force

# 2. 备份
$ts = Get-Date -Format "yyyyMMdd_HHmmss"
$dbPath = "$env:USERPROFILE\.cc-switch\cc-switch.db"
Copy-Item $dbPath "$dbPath.backup_$ts"

# 3. SQL 操作
# ...

# 4. 启 GUI + 同步
Start-Process "D:\apps\CC Switch\cc-switch.exe"
& $ccs mcp sync
```

---

## 交互式命令清单

`-h` 只标注了 `mcp add (interactive)`。实测以下也都是交互式（agent 调用会阻塞）：

| 命令 | 原因 | 替代方案 |
|------|------|---------|
| `mcp add` | -h 已标注 | 先停 GUI，SQL INSERT |
| `mcp edit <id>` | 无 `--args` 参数 | SQL `json_set()` |
| `mcp delete <id>` | 会问 "Are you sure?" | SQL DELETE |
| `provider add` | 交互式向导 | 先停 GUI，SQL INSERT |
| `provider edit <id>` | 无 `--settings-config` | 先停 GUI，SQL UPDATE |
| `provider delete <id>` | 会问确认 | 先停 GUI，SQL DELETE |
| `prompts edit <id>` | 无 `--content` 参数 | 告知用户手动操作 |

> `mcp import` 非交互，但只追加**新**服务器，不更新已有。

---

## 数据库 Schema

> 更多 JSON 格式细节见 `references/provider-schemas.md`（settings_config、meta 的完整字段说明）。

### mcp_servers

```sql
CREATE TABLE mcp_servers (
    id TEXT PRIMARY KEY, name TEXT, server_config TEXT NOT NULL,
    description TEXT DEFAULT '', tags TEXT DEFAULT '[]',
    enabled_claude INTEGER DEFAULT 0, enabled_codex INTEGER DEFAULT 0,
    enabled_gemini INTEGER DEFAULT 0, enabled_opencode INTEGER DEFAULT 0,
    enabled_hermes INTEGER DEFAULT 0
);
```

**server_config：**

```json
{ "type": "stdio", "command": "cmd",
  "args": ["/c", "npx", "-y", "package@latest"],
  "env": { "KEY": "value" } }
```

**精准修改（`json_set()`）：**

```powershell
$sql = "UPDATE mcp_servers SET server_config = json_set(server_config, '$.args[3]', '@scope/package@latest') WHERE id = 'my-mcp';"
$sql | Out-File -FilePath "$env:TEMP\fix.sql" -Encoding utf8 -NoNewline
Get-Content "$env:TEMP\fix.sql" | sqlite3 $dbPath
Remove-Item "$env:TEMP\fix.sql"
```

常用路径：`$.args[3]`（包名）· `$.command`（命令）· `$.env.KEY`（环境变量）· `$.type`（传输类型）

### providers

```sql
CREATE TABLE providers (
    id TEXT, app_type TEXT, name TEXT,
    settings_config TEXT NOT NULL, meta TEXT NOT NULL DEFAULT '{}',
    is_current BOOLEAN DEFAULT 0, PRIMARY KEY (id, app_type)
);
```

**settings_config（claude）：** `{"env":{"ANTHROPIC_BASE_URL":"...","ANTHROPIC_AUTH_TOKEN":"..."}}`

**meta：** `{"apiFormat":"anthropic","endpointAutoSelect":true,"commonConfigEnabled":true}`

### provider_endpoints

```sql
CREATE TABLE provider_endpoints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_id TEXT NOT NULL, app_type TEXT NOT NULL,
    url TEXT NOT NULL, added_at INTEGER,
    FOREIGN KEY (...) REFERENCES providers(...) ON DELETE CASCADE
);
```

### proxy_config

```sql
CREATE TABLE proxy_config (
    app_type TEXT PRIMARY KEY,
    enabled INTEGER DEFAULT 0,  -- GUI 控制，改无效
    listen_address TEXT DEFAULT '127.0.0.1',
    listen_port INTEGER DEFAULT 15721,
    auto_failover_enabled INTEGER DEFAULT 0
);
```

---

## 常用查询

```powershell
$dbPath = "$env:USERPROFILE\.cc-switch\cc-switch.db"

sqlite3 $dbPath "SELECT id, server_config FROM mcp_servers WHERE id = 'github';"
sqlite3 $dbPath "SELECT id, json_extract(server_config, '$.args[3]') FROM mcp_servers WHERE enabled_claude = 1;"
sqlite3 $dbPath "SELECT settings_config FROM providers WHERE is_current = 1 AND app_type = 'claude';"
sqlite3 $dbPath "SELECT value FROM settings WHERE key = 'common_config_claude';"
sqlite3 $dbPath "SELECT app_type, enabled FROM proxy_config;"
```

---

## 通用模板（common_config）工作流

```
common_config_claude + provider.settings_config → .claude.json（非 MCP 段）
mcp_servers 表 → .claude.json 的 mcpServers 段
```

通用模板用 CLI 操作：
```powershell
$ccs config common show --app claude          # 查看
$ccs config common set --snippet '{...}'      # 设置
```

---

## 常见问题

**路由被切断了？** → GUI 里手动打开。不能用 CLI 或 SQL 恢复。

**改库不想丢路由？** → 先停 GUI 再改。

**`mcp import` 没更新我的修改？** → 它只追加新服务器，不更新已有的。

**CLI 版本过低？** → `cc-switch update`（当前 v5.8.6+）。

**JSON 格式不清楚？** → 参考已有记录：`sqlite3 $dbPath "SELECT settings_config FROM providers WHERE app_type = 'claude' LIMIT 1;"`