---
name: trae-solo-cn-config
description: |
  TRAE SOLO CN 配置快速定位助手。当用户需要查找 TRAE SOLO CN 的配置文件、设置、MCP 服务器配置、工作区配置、历史记录或任何与 TRAE SOLO CN 相关的配置信息时，必须使用此 skill。触发关键词包括："TRAE SOLO CN 配置"、"Solo 配置"、"trae solo 设置"、"MCP 配置"、"找配置文件"、"配置在哪里"、"历史记录位置"、"工作区配置"、"skill 配置"、"工具配置"等。此 skill 提供完整的配置目录结构映射，帮助 AI 快速定位到具体配置文件路径，避免盲目搜索。
---

# TRAE SOLO CN 配置快速定位助手

此 skill 提供 TRAE SOLO CN 桌面应用的完整配置目录结构，帮助 AI 快速定位配置文件，节省探索时间。

## 配置根目录

**Windows 默认路径**: `C:\Users\{用户名}\AppData\Roaming\TRAE SOLO CN`

## 核心配置文件映射

### 1. 用户设置 (User Settings)
- **路径**: `User\settings.json`
- **用途**: 用户自定义的 VS Code 风格设置
- **包含内容**: 
  - 终端环境变量 (`terminal.integrated.env.windows`)
  - Shell 配置 (`solo.shell.env`, `solo.shell.strictEnv`)
  - AI 工具调用白名单 (`AI.toolcall.v2.command.allowList`)
  - 自动确认设置 (`AI.toolcall.v2.confirmation.mode`)

### 2. MCP 服务器配置
- **路径**: `User\mcp.json`
- **用途**: MCP (Model Context Protocol) 服务器配置
- **包含内容**: 
  - 已安装的 MCP 服务器列表
  - 每个服务器的命令、参数、环境变量
  - Gallery 来源标识 (`fromGalleryId`)

### 3. 全局存储 (Global Storage)
- **路径**: `User\globalStorage\storage.json`
- **用途**: 扩展和插件的全局状态存储

### 4. 工作区配置
- **路径**: `Workspaces\{workspace_id}\workspace.json`
- **用途**: 特定工作区的状态和配置
- **注意**: workspace_id 是数字时间戳格式

### 5. 工作区存储
- **路径**: `User\workspaceStorage\{hash}\workspace.json`
- **用途**: 工作区相关的扩展状态

### 6. 历史记录
- **路径**: `User\History\{folder_id}\`
- **文件**: 
  - `entries.json` - 历史条目索引
  - `{hash}.json` - 具体历史记录文件
- **用途**: 文件编辑历史、撤销历史

### 7. AI Agent 工具配置
- **路径**: `ModularData\ai-agent\vm\tools.json`
- **用途**: AI Agent 可用工具目录配置
- **包含**: Python、Node.js、JRE、系统工具等路径

### 8. 工具目录结构
- **Python**: `ModularData\ai-agent\vm\tools\python\`
- **Node.js**: `ModularData\ai-agent\vm\tools\node\`
- **系统工具**: `ModularData\ai-agent\vm\tools\bin\`
- **应用工具**: `ModularData\ai-agent\vm\tools\app\`
  - 7zip, ImageMagick, Tesseract, JRE 等

### 9. 代码知识图谱 (CKG)
- **路径**: `ModularData\ckg_server\`
- **文件**:
  - `local_env.json` - 本地环境配置
  - `env_codekg.db` - 代码知识图谱数据库
  - `codekg.log.{日期}_{小时}` - 日志文件

### 10. 应用程序偏好设置
- **路径**: `Preferences`
- **用途**: Electron 应用偏好设置
- **包含**: DevTools 状态、媒体设备、拼写检查等

### 11. 本地状态
- **路径**: `Local State`
- **用途**: 加密密钥、操作系统相关状态

### 12. 缓存目录
- **代码缓存**: `Code Cache\`
- **GPU 缓存**: `GPUCache\`
- **Dawn 缓存**: `DawnGraphiteCache\`, `DawnWebGPUCache\`
- **普通缓存**: `Cache\`

### 13. 存储
- **本地存储**: `Local Storage\leveldb\` 和 `Local Storage\config.db`
- **会话存储**: `Session Storage\`
- **共享字典**: `Shared Dictionary\`

### 14. 网络相关
- **路径**: `Network\`
- **包含**: Cookies、信任令牌、传输安全等

### 15. 崩溃报告
- **路径**: `Crashpad\`
- **包含**: 崩溃元数据和设置

### 16. 分区数据
- **路径**: `Partitions\trae-webview\`
- **用途**: Webview 分区隔离数据

### 17. Ahanet 配置
- **路径**: `ahanet\prefs\local_prefs.json`
- **用途**: Ahanet 相关偏好设置

### 18. 语言包
- **路径**: `languagepacks.json`
- **用途**: 已安装语言包信息

### 19. 默认配置覆盖
- **路径**: `CachedConfigurations\defaults\configurationDefaultsOverrides\configuration.json`
- **用途**: 默认配置覆盖

## 快速定位指南

当用户询问以下问题时，直接提供对应路径：

| 用户问题 | 配置文件路径 |
|---------|-------------|
| "MCP 配置在哪里" | `User\mcp.json` |
| "用户设置在哪" | `User\settings.json` |
| "历史记录在哪" | `User\History\{folder_id}\entries.json` |
| "工作区配置在哪" | `Workspaces\{id}\workspace.json` |
| "AI 工具路径配置" | `ModularData\ai-agent\vm\tools.json` |
| "Python 工具在哪" | `ModularData\ai-agent\vm\tools\python\python.exe` |
| "Node.js 在哪" | `ModularData\ai-agent\vm\tools\node\node.exe` |
| "全局存储在哪" | `User\globalStorage\storage.json` |
| "DevTools 设置在哪" | `Preferences` (electron 偏好) |
| "Cookie 在哪" | `Network\Cookies` |
| "缓存怎么清" | 删除 `Cache\`, `GPUCache\`, `Code Cache\` 等 |

## 使用示例

**示例 1**: 用户问 "MCP 服务器配置在哪？"
- 直接读取: `C:\Users\{username}\AppData\Roaming\TRAE SOLO CN\User\mcp.json`

**示例 2**: 用户问 "怎么修改终端环境变量？"
- 编辑: `User\settings.json` 中的 `terminal.integrated.env.windows`

**示例 3**: 用户问 "历史记录保存在哪？"
- 查看: `User\History\` 目录下的子文件夹

**示例 4**: 用户问 "AI 能用什么命令？"
- 查看: `User\settings.json` 中的 `AI.toolcall.v2.command.allowList`

## 注意事项

1. `{username}` 需要替换为实际用户名 (如 `86150`)
2. `{workspace_id}` 和 `{folder_id}` 是动态生成的哈希或时间戳
3. 某些文件是二进制格式 (如 Cookies、LevelDB)，需要专用工具读取
4. 修改配置前建议备份
5. 部分配置修改后需要重启 TRAE SOLO CN 生效
