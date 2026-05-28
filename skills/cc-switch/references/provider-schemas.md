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

## 参考现有 Provider

```powershell
$dbPath = "$env:USERPROFILE\.cc-switch\cc-switch.db"

# 查看某个 provider 的完整配置
sqlite3 -header -column $dbPath "SELECT id, name, app_type, settings_config, meta FROM providers WHERE name LIKE '%关键词%';"

# 查看所有 app_type 的 provider
sqlite3 -header -column $dbPath "SELECT id, name, app_type, is_current FROM providers ORDER BY app_type, name;"
```
