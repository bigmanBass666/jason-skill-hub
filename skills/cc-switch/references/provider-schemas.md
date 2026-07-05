# Provider 数据库 Schema

## providers 表结构

```sql
CREATE TABLE providers (
    id TEXT NOT NULL,                    -- UUID 或英文标识符
    app_type TEXT NOT NULL,              -- claude/codex/gemini/opencode/openclaw/hermes
    name TEXT NOT NULL,                  -- 显示名称
    settings_config TEXT NOT NULL,       -- JSON，格式因 app_type 而异
    website_url TEXT,
    category TEXT,
    created_at INTEGER,                  -- 毫秒时间戳
    sort_index INTEGER,
    notes TEXT,
    icon TEXT,
    icon_color TEXT,
    meta TEXT NOT NULL DEFAULT '{}',     -- JSON，ProviderMeta
    is_current BOOLEAN NOT NULL DEFAULT 0,
    in_failover_queue BOOLEAN NOT NULL DEFAULT 0,
    cost_multiplier TEXT NOT NULL DEFAULT '1.0',
    limit_daily_usd TEXT,
    limit_monthly_usd TEXT,
    provider_type TEXT,
    PRIMARY KEY (id, app_type)
);
```

## provider_endpoints 表结构

```sql
CREATE TABLE provider_endpoints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_id TEXT NOT NULL,
    app_type TEXT NOT NULL,
    url TEXT NOT NULL,
    added_at INTEGER,
    FOREIGN KEY (provider_id, app_type) REFERENCES providers(id, app_type) ON DELETE CASCADE
);
```

## settings_config JSON 格式

### claude / claude-desktop

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.example.com",
    "ANTHROPIC_AUTH_TOKEN": "sk-xxx",
    "ANTHROPIC_MODEL": "claude-sonnet-4-20250514",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-haiku-4-5",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-20250514",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-4-7"
  }
}
```

### codex

```json
{
  "auth": { "OPENAI_API_KEY": "sk-xxx" },
  "config": "model_provider = \"my-provider\"\nmodel = \"gpt-4o\"\n\n[model_providers.my-provider]\nname = \"My Provider\"\nbase_url = \"https://api.example.com/v1\"\nwire_api = \"responses\"\nrequires_openai_auth = true"
}
```

### gemini

```json
{
  "config": {
    "env": { "GEMINI_API_KEY": "AIzaSyxxx" },
    "model": { "name": "gemini-2.5-flash" },
    "security": { "auth": { "selectedType": "gemini-api-key" } }
  },
  "env": {
    "GEMINI_API_KEY": "AIzaSyxxx",
    "GOOGLE_GEMINI_BASE_URL": "https://generativelanguage.googleapis.com/v1beta"
  }
}
```

### opencode

```json
{
  "npm": "@ai-sdk/openai-compatible",
  "name": "Provider Name",
  "options": {
    "baseURL": "https://api.example.com/v1",
    "apiKey": "sk-xxx"
  },
  "models": {
    "model-id": { "name": "Display Name" }
  }
}
```

### openclaw

```json
{
  "baseUrl": "https://api.example.com/v1",
  "apiKey": "sk-xxx",
  "api": "openai-completions",
  "models": [
    { "id": "model-id", "name": "Model Name", "contextWindow": 200000 }
  ]
}
```

### hermes

```json
{
  "name": "provider-name",
  "base_url": "https://api.example.com/v1",
  "api_key": "sk-xxx",
  "api_mode": "chat_completions",
  "models": [
    { "id": "model-id", "name": "Model Name" }
  ]
}
```

## meta 字段格式

```json
{
  "apiFormat": "anthropic",           // 或 "openai_chat"
  "endpointAutoSelect": true,
  "commonConfigEnabled": true
}
```

## settings 表（通用模板）

cc-switch 用 `settings` 表存储 key-value 配置。最重要的 key 是 `common_config_<app_type>`，它存储每种客户端的**通用模板**——切换 provider 时不变的配置。

### 工作原理

```
common_config_claude（通用模板） + provider.settings_config（模型 env） → settings.json
```

cc-switch 切换 provider 时，将 provider 的 `settings_config`（主要是 `env` 里的模型变量）合并到 `common_config_claude` 上，生成最终的 `settings.json`。

### 查询通用模板

```powershell
$dbPath = "$env:USERPROFILE\.cc-switch\cc-switch.db"

# 查看 Claude 通用模板
sqlite3 $dbPath "SELECT value FROM settings WHERE key = 'common_config_claude';"

# 查看所有通用模板 key
sqlite3 -header -column $dbPath "SELECT key, length(value) as size FROM settings WHERE key LIKE 'common_config_%';"
```

### 通用模板内容

`common_config_claude` 包含**非 provider 特定**的配置：

| 字段 | 说明 |
|------|------|
| `env` | 公共环境变量（`DISABLE_AUTOUPDATER`, `ENABLE_TOOL_SEARCH`, `API_TIMEOUT_MS` 等） |
| `enabledPlugins` | 插件开关 |
| `statusLine` | HUD 状态栏配置 |
| `language`, `model` | 语言、默认模型 |
| `hooks` | Hook 配置（PreToolUse 等） |
| `skipDangerousModePermissionPrompt` 等 | 行为开关 |

### 编辑通用模板

⚠️ **必须关闭 cc-switch GUI**，否则外部修改会触发设置重置。

```powershell
$dbPath = "$env:USERPROFILE\.cc-switch\cc-switch.db"

# 1. 导出当前模板
sqlite3 $dbPath "SELECT value FROM settings WHERE key = 'common_config_claude';" > /tmp/common.json

# 2. 编辑 common.json（添加/修改字段）

# 3. 更新回数据库
$ts = Get-Date -Format "yyyyMMdd_HHmmss"
Copy-Item $dbPath "$dbPath.backup_$ts"
$newValue = Get-Content /tmp/common.json -Raw
$sql = "UPDATE settings SET value = '$($newValue -replace "'", "''")' WHERE key = 'common_config_claude';"
$sql | Out-File -FilePath "update.sql" -Encoding utf8 -NoNewline
Get-Content "update.sql" | sqlite3 $dbPath

# 4. 切换 provider 触发重新生成 settings.json
```

### 其他 settings key

| key | 说明 |
|-----|------|
| `stream_check_config` | 流式连接测试配置 |
| `rectifier_config` | 请求整形配置（thinking signature 等） |
| `optimizer_config` | 缓存优化配置 |
| `common_config_gemini` | Gemini 通用模板 |
| `common_config_codex` | Codex 通用模板 |
| `common_config_opencode` | OpenCode 通用模板 |
| `official_providers_seeded` | 官方 provider 是否已初始化 |

## mcp_servers 表结构

```sql
CREATE TABLE mcp_servers (
    id TEXT NOT NULL,                    -- 标识符（如 "github", "web-search"）
    name TEXT NOT NULL,                  -- 显示名称
    server_config TEXT NOT NULL,         -- JSON，server 配置
    description TEXT DEFAULT '',         -- 描述
    tags TEXT DEFAULT '[]',              -- JSON 数组
    enabled_claude INTEGER DEFAULT 0,    -- 是否在 Claude Code 中启用
    enabled_codex INTEGER DEFAULT 0,     -- 是否在 Codex 中启用
    enabled_gemini INTEGER DEFAULT 0,    -- 是否在 Gemini CLI 中启用
    enabled_opencode INTEGER DEFAULT 0,  -- 是否在 OpenCode 中启用
    enabled_hermes INTEGER DEFAULT 0,    -- 是否在 Hermes CLI 中启用
    PRIMARY KEY (id)
);
```

### server_config 格式

```json
{
  "type": "stdio",           // "stdio" | "http"
  "command": "cmd",          // stdio 的可执行文件
  "args": ["/c", "npx", "-y", "package@latest"],  // 命令行参数
  "env": {                   // 可选的环境变量
    "KEY": "value"
  }
}
```

### 常用查询

```sql
-- 查看所有启用的 MCP（按客户端）
SELECT id, name, enabled_claude, enabled_codex FROM mcp_servers WHERE enabled_claude = 1 OR enabled_codex = 1;

-- 查看某个 MCP 的完整配置
SELECT id, server_config FROM mcp_servers WHERE id = 'github';

-- 查看 npm 包名（args 数组第 3 个元素）
SELECT id, json_extract(server_config, '$.args[3]') as package FROM mcp_servers WHERE json_extract(server_config, '$.args[3]') IS NOT NULL;

-- 统计各客户端启用数量
SELECT
  SUM(enabled_claude) as claude,
  SUM(enabled_codex) as codex,
  SUM(enabled_gemini) as gemini,
  SUM(enabled_opencode) as opencode
FROM mcp_servers;
```

## 参考现有 Provider

```powershell
$dbPath = "$env:USERPROFILE\.cc-switch\cc-switch.db"

# 查看某个 provider 的完整配置
sqlite3 -header -column $dbPath "SELECT id, name, app_type, settings_config, meta FROM providers WHERE name LIKE '%关键词%';"

# 查看所有 app_type 的 provider
sqlite3 -header -column $dbPath "SELECT id, name, app_type, is_current FROM providers ORDER BY app_type, name;"
```
