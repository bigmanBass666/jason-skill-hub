---
name: trae-solo-cn-config
description: |
  TRAE 系列应用配置快速定位助手。当用户需要查找 TRAE SOLO CN、Trae CN (国内版)、Trae (国际版) 的配置文件、设置、MCP 服务器配置、工作区配置、历史记录或任何与 TRAE 相关的配置信息时，必须使用此 skill。触发关键词包括："TRAE SOLO CN 配置"、"Trae CN 配置"、"Trae 配置"、"Solo 配置"、"trae solo 设置"、"MCP 配置"、"找配置文件"、"配置在哪里"、"历史记录位置"、"工作区配置"、"skill 配置"、"工具配置"等。此 skill 提供三个版本的完整配置目录结构映射，帮助 AI 快速定位到具体配置文件路径，避免版本混淆和盲目搜索。
---

# TRAE 系列应用配置快速定位助手

此 skill 提供 TRAE 三个版本（SOLO CN、Trae CN、Trae 国际版）的完整配置目录结构，帮助 AI 快速定位配置文件，避免版本混淆。

## 三个版本的区别

| 版本 | 目录名称 | 特点 |
|------|---------|------|
| **TRAE SOLO CN** | `TRAE SOLO CN` | 字节跳动国内 Solo 版本，有独立的 AI Agent 工具系统 |
| **Trae CN** | `Trae CN` | 字节跳动国内主版本，功能最完整 |
| **Trae (国际版)** | `Trae` | 国际版本，面向海外用户 |

## 配置根目录

**Windows 默认路径**:
- TRAE SOLO CN: `C:\Users\{用户名}\AppData\Roaming\TRAE SOLO CN`
- Trae CN: `C:\Users\{用户名}\AppData\Roaming\Trae CN`
- Trae (国际版): `C:\Users\{用户名}\AppData\Roaming\Trae`

---

## TRAE SOLO CN 特有配置

### 1. 用户设置 (User Settings)
- **路径**: `User\settings.json`
- **特有配置**: 
  - `solo.shell.env` - Solo 专属 Shell 环境变量
  - `AI.toolcall.v2.command.allowList` - AI 工具调用白名单
  - `AI.toolcall.v2.confirmation.mode` - 自动确认设置

### 2. MCP 服务器配置
- **路径**: `User\mcp.json`
- **用途**: MCP (Model Context Protocol) 服务器配置

### 3. AI Agent 工具配置 (SOLO 特有)
- **路径**: `ModularData\ai-agent\vm\tools.json`
- **用途**: AI Agent 可用工具目录配置
- **包含**: Python、Node.js、JRE、系统工具等路径

### 4. 工具目录结构 (SOLO 特有)
- **Python**: `ModularData\ai-agent\vm\tools\python\`
- **Node.js**: `ModularData\ai-agent\vm\tools\node\`
- **系统工具**: `ModularData\ai-agent\vm\tools\bin\`
- **应用工具**: `ModularData\ai-agent\vm\tools\app\`
  - 7zip, ImageMagick, Tesseract, JRE 等

### 5. 代码知识图谱 (CKG) (SOLO 特有)
- **路径**: `ModularData\ckg_server\`
- **文件**:
  - `local_env.json` - 本地环境配置
  - `env_codekg.db` - 代码知识图谱数据库
  - `codekg.log.{日期}_{小时}` - 日志文件

---

## Trae CN (国内版) 特有配置

### 1. 用户设置
- **路径**: `User\settings.json`
- **特有配置**:
  - `AI.rules.importClaudeMd` - Claude 规则导入
  - `AI.toolcall.reviewMode.solo` - Solo 模式审查设置
  - `AI.toolcall.reviewMode.ide` - IDE 模式审查设置
  - `chat.useAgentsMdFile` - Agents.md 文件支持
  - `chat.useNestedAgentsMdFiles` - 嵌套 Agents 支持
  - `chat.customAgentInSubagent.enabled` - 子 Agent 自定义
  - `chat.tools.terminal.enableAutoApprove` - 终端自动批准

### 2. MCP 服务器配置
- **路径**: `User\mcp.json`
- **特点**: 通常包含更完整的 MCP 服务器配置

### 3. 特有目录
- **ModularData**: `ModularData\ttnet\` - 字节跳动网络相关
- **remote-widgets**: `remote-widgets\` - 远程小组件

---

## Trae (国际版) 特有配置

### 1. 用户设置
- **路径**: `User\settings.json`
- **特点**: 配置与 Trae CN 类似，但可能缺少国内特有的 AI 功能配置

### 2. MCP 服务器配置
- **路径**: `User\mcp.json`
- **注意**: 可能不存在此文件（如果未配置 MCP）

### 3. 特有目录
- **logs**: `logs\` - 详细的日志目录结构
  - ` Modular\` - AI Agent、CKG、Cue Server 日志
  - `window1\` - 窗口相关日志
  - `aha_log\` - Aha 网络日志
- **monitor**: `monitor\parfait\` - 性能监控数据
- **ahanet**: `ahanet\` - Aha 网络配置
  - `server.json` - 服务器配置
  - `tt_net_config.config` - 网络配置

---

## 三个版本共有的配置

### 全局存储 (Global Storage)
- **路径**: `User\globalStorage\storage.json`
- **用途**: 扩展和插件的全局状态存储

### 工作区配置
- **路径**: `Workspaces\{workspace_id}\workspace.json` (SOLO)
- **路径**: `User\workspaceStorage\{hash}\workspace.json` (CN/国际版)
- **用途**: 特定工作区的状态和配置

### 历史记录
- **路径**: `User\History\{folder_id}\`
- **文件**: 
  - `entries.json` - 历史条目索引
  - `{hash}.json` - 具体历史记录文件
- **用途**: 文件编辑历史、撤销历史

### 应用程序偏好设置
- **路径**: `Preferences`
- **用途**: Electron 应用偏好设置
- **包含**: DevTools 状态、媒体设备、拼写检查等

### 本地状态
- **路径**: `Local State`
- **用途**: 加密密钥、操作系统相关状态

### 缓存目录
- **代码缓存**: `Code Cache\`
- **GPU 缓存**: `GPUCache\`
- **Dawn 缓存**: `DawnGraphiteCache\`, `DawnWebGPUCache\`
- **普通缓存**: `Cache\`

### 存储
- **本地存储**: `Local Storage\leveldb\` 和 `Local Storage\config.db`
- **会话存储**: `Session Storage\`
- **共享字典**: `Shared Dictionary\`

### 网络相关
- **路径**: `Network\`
- **包含**: Cookies、信任令牌、传输安全等

### 崩溃报告
- **路径**: `Crashpad\`
- **包含**: 崩溃元数据和设置

### 分区数据
- **路径**: `Partitions\trae-webview\`
- **用途**: Webview 分区隔离数据

### Ahanet 配置
- **路径**: `ahanet\prefs\local_prefs.json`
- **用途**: Ahanet 相关偏好设置

### 语言包
- **路径**: `languagepacks.json`
- **用途**: 已安装语言包信息

### 代码片段
- **路径**: `User\snippets\`
- **文件**: `{language}.json` (c.json, java.json, html.json 等)

### 快捷键绑定
- **路径**: `User\keybindings.json`
- **用途**: 自定义快捷键配置

---

## 版本快速识别指南

当用户提到以下关键词时，确定对应的版本：

| 用户说法 | 对应版本 | 目录名 |
|---------|---------|--------|
| "Solo" / "SOLO" / "solo" | TRAE SOLO CN | `TRAE SOLO CN` |
| "Trae CN" / "trae cn" / "国内版" | Trae CN | `Trae CN` |
| "Trae" / "trae" / "国际版" | Trae (国际版) | `Trae` |
| 未明确说明 | **询问用户** | - |

---

## 快速定位指南

### TRAE SOLO CN 特有

| 用户问题 | 配置文件路径 |
|---------|-------------|
| "SOLO 的 MCP 配置在哪里" | `User\mcp.json` |
| "SOLO 的 AI 工具路径" | `ModularData\ai-agent\vm\tools.json` |
| "SOLO 的代码知识图谱" | `ModularData\ckg_server\local_env.json` |
| "SOLO 的 Python 工具在哪" | `ModularData\ai-agent\vm\tools\python\python.exe` |
| "SOLO 的系统工具在哪" | `ModularData\ai-agent\vm\tools\bin\` |

### Trae CN 特有

| 用户问题 | 配置文件路径 |
|---------|-------------|
| "Trae CN 的 MCP 配置" | `User\mcp.json` |
| "Trae CN 的 AI 规则配置" | `User\settings.json` (AI.rules.*) |
| "Trae CN 的终端自动批准" | `User\settings.json` (chat.tools.terminal.*) |

### Trae (国际版) 特有

| 用户问题 | 配置文件路径 |
|---------|-------------|
| "Trae 的日志在哪" | `logs\{日期}T{时间}\` |
| "Trae 的网络配置" | `ahanet\server.json` |
| "Trae 的性能监控" | `monitor\parfait\` |

### 三个版本通用

| 用户问题 | 配置文件路径 |
|---------|-------------|
| "用户设置在哪" | `User\settings.json` |
| "历史记录在哪" | `User\History\{folder_id}\entries.json` |
| "工作区配置在哪" | `User\workspaceStorage\{hash}\workspace.json` |
| "全局存储在哪" | `User\globalStorage\storage.json` |
| "DevTools 设置在哪" | `Preferences` |
| "Cookie 在哪" | `Network\Cookies` |
| "代码片段在哪" | `User\snippets\` |
| "快捷键配置在哪" | `User\keybindings.json` |

---

## 使用示例

**示例 1**: 用户问 "SOLO 的 MCP 服务器配置在哪？"
- 版本识别: TRAE SOLO CN
- 路径: `C:sersusername}ppDataoamingRAE SOLO CNsercp.json`

**示例 2**: 用户问 "Trae CN 的 AI 规则怎么配置？"
- 版本识别: Trae CN
- 路径: `C:sersusername}ppDataoamingrae CNserettings.json`
- 相关配置项: `AI.rules.importClaudeMd`, `chat.useAgentsMdFile`

**示例 3**: 用户问 "Trae 的日志文件在哪？"
- 版本识别: Trae (国际版)
- 路径: `C:sersusername}ppDataoamingraeogs

**示例 4**: 用户问 "历史记录保存在哪？" (未指定版本)
- **必须询问**: "您指的是哪个版本？SOLO、Trae CN 还是 Trae 国际版？"

---

## 注意事项

1. **版本区分最重要**: 三个版本的配置目录完全不同，必须先确认用户指的是哪个版本
2. `{username}` 需要替换为实际用户名 (如 `86150`)
3. `{workspace_id}` 和 `{folder_id}` 是动态生成的哈希或时间戳
4. 某些文件是二进制格式 (如 Cookies、LevelDB)，需要专用工具读取
5. 修改配置前建议备份
6. 部分配置修改后需要重启对应版本的 TRAE 应用生效
7. **不要混淆版本**: 
   - `TRAE SOLO CN` ≠ `Trae CN`
   - `Trae CN` ≠ `Trae`
   - 三个版本配置不互通
