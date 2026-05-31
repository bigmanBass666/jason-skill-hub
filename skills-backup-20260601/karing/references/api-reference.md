# Clash API Reference (Karing sing-box core)

Base URL: `http://127.0.0.1:{control_port}` (default 3057)
Auth: `Authorization: Bearer {secret}`

Read `service.json` from `%APPDATA%/karing/karing/service.json` to get `control_port` and `secret`.

## Version

```
GET /version
→ {"meta":true,"premium":true,"version":"sing-box 1.13.x.xxxx"}
```

## Proxies

### List all proxies and groups
```
GET /proxies
→ {"proxies": {"GLOBAL": {...}, "节点名": {...}, ...}}
```
Each proxy has: `name`, `type` (Selector/URLTest/Fallback/VLESS/Hysteria2/Direct/Reject), `now` (current selection), `all` (child node names).

### Get proxy group detail
```
GET /proxies/{name}
→ {"name":"...", "type":"selector", "now":"selected_node", "all":["node1","node2"], ...}
```

### Switch selected node (PUT)
```
PUT /proxies/{group_name}
Content-Type: application/json
Body: {"name": "target_node_name"}
→ 204 No Content on success
```

### Test proxy delay
```
GET /proxies/{name}/delay?timeout=5000&url=https://www.gstatic.com/generate_204
→ {"delay": 123}
```
If failed: HTTP error or `{"delay": 0}`

## Providers

### List providers
```
GET /providers
```

### Update provider (refresh subscription)
```
PUT /providers/{name}
```

## Configs

### Get current config
```
GET /configs
→ {"port":0, "socks-port":0, "mixed-port":3067, "mode":"Rule", ...}
```

### Modify config
```
PATCH /configs
Content-Type: application/json
Body: {"mode": "global"}  // or "rule", "direct"
→ 204 No Content
```

## Connections

### List connections
```
GET /connections
→ {"connections": [...], "downloadTotal":..., "uploadTotal":...}
```

### Close all connections
```
DELETE /connections
```

### Close specific connection
```
DELETE /connections/{id}
```

## Streaming (SSE)

### Traffic stream
```
GET /traffic
```

### Log stream
```
GET /logs?level=info
```

## Common Test URLs

| URL | Use case |
|-----|----------|
| `https://www.gstatic.com/generate_204` | Standard connectivity test |
| `https://www.google.com/generate_204` | Google connectivity |
| `https://cp.cloudflare.com/generate_204` | Cloudflare connectivity |

## Common Proxy Types in Karing

| Type | Description |
|------|-------------|
| Selector | Manual selection group |
| URLTest | Auto-select by latency |
| Fallback | Failover group |
| VLESS | VLESS protocol node |
| Hysteria2 | Hysteria2 protocol node |
| TUIC | TUIC protocol node |
| Direct | Direct connection |
| Reject | Block connection |
