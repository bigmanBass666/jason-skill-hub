---
name: karing
description: >
  Karing 代理客户端管理工具。用于通过 Clash API、URL Scheme 和配置文件直接操控 Karing。
  当用户提到以下任何内容时触发此 skill：切换节点、测速、测试延迟、代理连接/断开、
  导入订阅、管理机场配置、选择最优节点、代理故障排查、Karing 配置修改、
  节点稳定性测试、按场景选节点（日常/下载/流媒体/游戏）。
  即使用户只是说"帮我选个快的节点"、"代理挂了"、"加个订阅"也应触发。
  如果用户提到 clash-mcp、sing-box 代理控制、代理面板订阅提取，同样触发。
---

# Karing 代理管理 Skill

通过 Clash API、URL Scheme 和本地配置文件操控 Karing 代理客户端。

## 前置依赖

- **clash-mcp**: 项目级 MCP 工具，提供 Clash API 封装
- **Playwright MCP** (可选): 浏览器面板提取订阅时使用

## 环境检测

每次执行前，先读取配置获取连接参数：

```python
import json, os
config_path = os.path.expandvars(r"%APPDATA%\karing\karing\service.json")
with open(config_path) as f:
    svc = json.load(f)
# svc["control_port"] → Clash API 端口 (通常 3057)
# svc["secret"] → API 认证密钥
# svc["version"] → Karing 版本
```

如果 clash-mcp 工具不可用，提示用户：
> 请先确保 clash-mcp 已配置（.mcp.json）并执行 /mcp 重载工具。

## 操作决策树

收到用户请求后，按以下顺序判断：

1. **节点操作**（测速/切换/选优）→ 使用 `mcp__clash-mcp__*` 工具
2. **连接控制**（连接/断开/重连）→ 使用 URL Scheme (`karing://connect` 等)
3. **导入订阅**
   a. 用户给了直接链接？→ URL Scheme `karing://install-config?url=...`
   b. 用户给了面板页面 URL？→ Playwright 登录面板 → 从 API 提取订阅 URL → URL Scheme 导入
4. **订阅管理**（启用/禁用/查看）→ 直接读写 `karing_subscribe.json`
5. **配置修改**（端口/TUN/DNS）→ 直接读写 `karing_setting.json`
6. **故障诊断**→ Clash API `/connections` + `/logs` + 配置文件检查

---

## 一、节点测速与选优

### 1.1 全量测速

对所有代理节点执行延迟测试：

```
对每个节点调用 mcp__clash-mcp__check_proxy_delay:
  - proxyName: 节点名称
  - url: "https://www.gstatic.com/generate_204"
  - timeoutMs: 5000
```

并行测试以节省时间。结果按地区分组展示：

```
| 节点 | 协议 | 延迟 |
|------|------|------|
| 🇯🇵日本东京01 | VLESS | 120ms |
| 🇭🇰香港-A | TUIC | 95ms |
```

### 1.2 稳定性测试

对延迟较低的候选节点（top 5-8）进行 3 轮重复测试：

- 第 1 轮：批量全量测试，筛出延迟 < 300ms 的节点
- 第 2 轮：对候选节点重复测试 2 次
- 第 3 轮：对 top 3 确认

评估指标：
- **平均延迟**: 3 轮均值
- **波动范围**: max - min（越小越稳定）
- **超时率**: 失败次数 / 总测试次数

**稳定性分级**:
- 极稳定: 波动 < 30ms 且 0 超时
- 稳定: 波动 < 80ms 且 0 超时
- 不稳定: 波动 > 80ms 或有超时
- 不可用: 全部超时

### 1.3 按场景推荐

| 场景 | 策略 | 说明 |
|------|------|------|
| **日常** | 低延迟 + 稳定 | 测日/港/新/韩/台节点，3 轮验证，选波动最小的 |
| **下载** | 协议优先 Hysteria2 | hy2 协议带宽大，延迟次要 |
| **流媒体** | 地区优先 | Netflix→日/港/新/美，YouTube→任意低延迟 |
| **游戏** | 超低延迟 | 只看延迟 < 100ms 的节点 |

### 1.4 切换节点

```
mcp__clash-mcp__prepare_proxy_switch → preflight → confirm
```

或直接用 Clash API:
```
PUT /proxies/{group_name}
Body: {"name": "目标节点名"}
```

---

## 二、连接控制

通过 PowerShell 调用 URL Scheme：

```powershell
# 连接
Start-Process "karing://connect?background=true"

# 断开
Start-Process "karing://disconnect"

# 重连
Start-Process "karing://reconnect"
```

---

## 三、订阅管理

### 3.1 导入订阅（直接链接）

```powershell
# 对 URL 进行 percent-encode 后拼接
$url = [System.Uri]::EscapeDataString("https://example.com/subscribe?token=xxx")
Start-Process "karing://install-config?url=$url&name=机场名称"
```

支持的订阅格式: Clash, sing-box, V2ray, Shadowsocks, Sub, Github

### 3.2 导入订阅（从面板提取）

当用户给出机场面板 URL（如 `https://xxx.com/app/dashboard`）时：

1. 用 Playwright 打开页面，提示用户手动登录
2. 用户确认登录后，用 `browser_evaluate` 从 Vue 状态提取订阅：
   ```js
   const app = document.querySelector('#app').__vue_app__;
   const pinia = app.config.globalProperties.$pinia;
   const sub = pinia.state.value.user.subscribe;
   return sub.subscribe_url;
   ```
3. 如果是 V2board 面板，尝试构造直接订阅 URL：
   ```
   https://{api_host}/api/v1/client/subscribe?token={token}&flag=sing-box
   ```
4. 用 URL Scheme 导入

### 3.3 查看订阅状态

读取配置文件：

```python
import json, os
path = os.path.expandvars(r"%APPDATA%\karing\karing\karing_subscribe.json")
with open(path) as f:
    data = json.load(f)
for item in data["items"]:
    status = "ON" if item.get("enable") else "OFF"
    print(f"[{status}] {item['remark']} | {item['type']} | {item['urlOrPath'][:50]}")
```

### 3.4 启用/禁用订阅

直接编辑 `karing_subscribe.json`，找到目标订阅的 `enable` 字段修改为 `true`/`false`。
修改后提醒用户：重启 Karing 或断开重连以生效。

---

## 四、故障诊断

当用户报告连接问题时，按以下顺序排查：

### 4.1 检查 Karing 是否运行
```bash
tasklist | grep karing  # 或 tasklist | findstr karing
```

### 4.2 检查 Clash API 是否可达
```
GET /version
```
如果无响应 → Karing 未启动或端口被占用

### 4.3 检查连接状态
```
GET /connections
```
查看活跃连接数、是否有异常

### 4.4 常见问题速查

| 错误 | 原因 | 解决 |
|------|------|------|
| `listen tcp 127.0.0.1:3065: bind` | 端口被占用 | 改端口或杀占用进程 |
| `A required privilege is not held` | 权限不足 | 以管理员启动 |
| `configure tun interface: Cannot create` | TUN 冲突 | 卸载其他 VPN 软件 |
| `CERTIFICATE_VERIFY_FAILED` | 证书错误 | 更新系统根证书 |
| `Connection reset by peer` | 订阅被阻断 | 开代理后重试 |

---

## 五、配置文件参考

| 文件路径 | 内容 |
|---------|------|
| `%APPDATA%/karing/karing/service.json` | API 端口、密钥、核心路径 |
| `%APPDATA%/karing/karing/karing_setting.json` | 代理端口、TUN、DNS、UI 设置 |
| `%APPDATA%/karing/karing/karing_subscribe.json` | 订阅源列表及节点数据 |
| `%APPDATA%/karing/karing/karing_routing_group.json` | 路由规则分组 |

## 六、完整操作清单

用于交叉验证，确保每个底层操作都有对应的用户命令覆盖：

### Clash API 操作
- [x] GET /version → 故障诊断
- [x] GET /proxies → "看看节点"、测速、选优
- [x] GET /proxies/:name → (内部) 查看组详情
- [x] PUT /proxies/:name → "切换到XX"
- [x] GET /proxies/:name/delay → 测速核心
- [x] GET /providers → (内部) 查看订阅源
- [x] PUT /providers/:name → "更新订阅"
- [x] GET /configs → 故障诊断
- [x] PATCH /configs → "切全局模式"
- [x] GET /connections → 故障诊断
- [x] DELETE /connections → "断开所有连接"
- [x] GET /traffic → (内部) 流量监控
- [x] GET /logs → 故障诊断

### URL Scheme 操作
- [x] karing://connect → "连接"
- [x] karing://disconnect → "断开"
- [x] karing://reconnect → "重连"
- [x] karing://install-config → "导入订阅"
- [ ] karing://restore-backup → (暂不暴露)

### 配置文件操作
- [x] karing_subscribe.json enable → "启用/禁用订阅"
- [x] karing_subscribe.json 读取 → "查看订阅情况"
- [x] karing_setting.json → "改端口/TUN/DNS"
- [ ] karing_routing_group.json → (暂不暴露，复杂度高)

详细 API 文档见 `references/api-reference.md`。
