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

# TRAE SOLO CN 专精指南

## SOLO 核心架构

SOLO 是一个独立的 AI 编程助手，拥有完整的内置工具链和沙箱系统，不依赖外部 VS Code。

### 1. AI Agent 系统 (`ModularData/ai-agent/`)

SOLO 的核心是 AI Agent 系统，包含以下组件：

#### 1.1 工具链配置
- **主配置**: `ModularData\ai-agent\vm\tools.json`
- **内容**: 定义了 4 个工具目录路径
  ```json
  {
    "tools_dir": [
      "...\\ModularData\\ai-agent\\vm\\tools\\python",
      "...\\ModularData\\ai-agent\\vm\\tools\\node", 
      "...\\ModularData\\ai-agent\\vm\\tools\\app\\jre\\bin",
      "...\\ModularData\\ai-agent\\vm\\tools\\bin"
    ]
  }
  ```

#### 1.2 内置 Python 环境
- **路径**: `ModularData\ai-agent\vm\tools\python\`
- **Python 版本**: 内置完整 Python 发行版
- **预装包**: PIL/Pillow, numpy, pandas, matplotlib, opencv-python, pypdf, python-docx, python-pptx, beautifulsoup4, lxml, requests, click, colorama, chardet, certifi, cffi, csvkit, agate, dbfread, dateutil, decorator, defusedxml, docx, dotenv, fontTools, idna, isodate, jedi, leather, magika, markdown, mpmath, odfpy, packaging, parso, pdfminer, pdfplumber, pip, pptx, pygments, pyparsing, pypdfium2, pytz, PyYAML, IPython, pickleshare
- **可执行文件**: `python.exe`, `python3.exe`

#### 1.3 内置 Node.js 环境
- **路径**: `ModularData\ai-agent\vm\tools\node\`
- **包含**: node.exe, npm, npx, pnpm, yarn, corepack
- **MCP 相关**: 
  - `mcp_prewarm/` - MCP 预热工具
  - `mcp_proxy_bootstrap/` - MCP 代理启动器

#### 1.4 系统工具目录 (`bin/`)
- **路径**: `ModularData\ai-agent\vm\tools\bin\`
- **特点**: 通过 `.shim` 文件包装调用实际工具
- **可用工具**:
  - **压缩**: 7z.exe
  - **搜索**: rg.exe (ripgrep)
  - **文档处理**: pandoc.exe, qpdf.exe, sqlite3.exe
  - **图像处理**: magick.cmd (ImageMagick), ffmpeg.cmd, ffprobe.cmd
  - **PDF 处理**: pdftotext.cmd, pdfimages.cmd, pdftocairo.cmd, pdfunite.cmd
  - **Java**: java.exe, plantuml.exe
  - **Graphviz**: dot.exe, neato.exe, fdp.exe, sfdp.exe, circo.exe, twopi.exe
  - **Node/Python**: node.cmd, npm.cmd, npx.cmd, python.cmd, pip.cmd
  - **办公**: soffice.exe (LibreOffice)
  - **其他**: jq.cmd, tesseract.cmd, file.cmd, make.cmd

#### 1.5 应用工具目录 (`app/`)
- **路径**: `ModularData\ai-agent\vm\tools\app\`
- **7zip**: 完整 7-Zip 发行版 (7z.exe, 7z.dll, 7zFM.exe 等)
- **Graphviz**: 完整 Graphviz 安装 (bin/, lib/, share/)
- **FFmpeg**: ffmpeg.exe, ffplay.exe, ffprobe.exe
- **File**: file.exe (文件类型识别)
- **Ghostscript**: gsdll64.dll, gswin64c.exe
- **ImageMagick**: 完整 ImageMagick (magick.exe, compare.exe, composite.exe, convert.exe 等)
- **Jq**: jq.exe (JSON 处理器)
- **JRE**: 完整 Java Runtime Environment (bin/, conf/, legal/, lib/)
  - 包含 plantuml.jar 和 plantuml.exe
- **LibreOffice**: 办公套件 (App/, help.html)
- **Make**: make.exe
- **Pandoc**: pandoc.exe (文档转换)
- **Poppler**: PDF 工具集 (pdfattach.exe, pdfdetach.exe, pdffonts.exe, pdfimages.exe, pdfinfo.exe, pdfseparate.exe, pdftocairo.exe, pdftohtml.exe, pdftoppm.exe, pdftops.exe, pdftotext.exe, pdfunite.exe)
- **QPDF**: qpdf.exe, qpdf30.dll
- **Ripgrep**: rg.exe
- **SQLite**: sqlite3.exe
- **Tesseract**: OCR 引擎 (tesseract.exe, 训练工具, lib 库)

### 2. 代码知识图谱 (CKG) 系统

- **路径**: `ModularData\ckg_server\`
- **本地环境**: `local_env.json`
  ```json
  {
    "host": "",
    "device_id": "0",
    "is_privacy_mode": false,
    "host_map": {
      "2197293361281892": "https://trae-api-cn.mchost.guru",
      "default": ""
    }
  }
  ```
- **数据库**: `env_codekg.db` - SQLite 格式的代码知识图谱
- **日志**: `codekg.log.{YYYY-MM-DD}_{HH}` - 按小时轮转的日志

### 3. AI Agent 数据库

- **路径**: `ModularData\ai-agent\database.db`
- **格式**: SQLite (二进制)
- **用途**: 存储 AI Agent 的状态和历史

### 4. 沙箱系统

- **路径**: `ModularData\ai-agent\sandbox\`
- **文件**: `{hash}.json`
- **内容示例**:
  ```json
  {
    "name": "69fe7a496f82f694159efbb8",
    "permission": [
      {"file_inherit_user": "D:\\Working\\Code\\Android"},
      {"file_inherit_user": "C:\\Users\\86150\\.trae-cn\\memory"},
      {"file_read_only": "D:\\Working\\Code\\Android\\.vscode"},
      {"file_read_only": "D:\\Working\\Code\\Android\\.trae\\mcp.json"},
      {"network_allow": "*"}
    ]
  }
  ```
- **作用**: 定义 AI Agent 的文件系统权限和网络访问权限

### 5. SOLO 特有配置项

#### 5.1 用户设置 (`User\settings.json`)
```json
{
  "terminal.integrated.env.windows": {
    "PATH": "..."
  },
  "solo.shell.strictEnv": false,
  "solo.shell.env": {
    "PATH": "..."
  },
  "AI.toolcall.v2.command.allowList": "[\"echo\",\"where\",\"python\",\"node\",\"git\",...]",
  "AI.toolcall.v2.confirmation.mode": "auto",
  "AI.toolcall.v2.confirmation.autoApprove": true
}
```

#### 5.2 MCP 配置 (`User\mcp.json`)
- 标准 MCP 服务器配置格式
- 支持 `fromGalleryId` 标识 Gallery 来源

### 6. 工作区机制

- **路径**: `Workspaces\{timestamp}\workspace.json`
- **格式**:
  ```json
  {
    "folders": [
      {"path": "D:/Test/solo-path-env-test"}
    ],
    "settings": {}
  }
  ```
- **特点**: 使用数字时间戳作为 workspace_id，而非哈希值

### 7. SOLO 工具调用白名单

SOLO 使用 `AI.toolcall.v2.command.allowList` 控制 AI 可调用的命令，包括：
- **基础命令**: echo, where, set, cd, dir, type, copy, move, del, mkdir, rmdir
- **PowerShell**: Get-Command, Get-Content, Select-Object, Write-Host, Invoke-RestMethod, ConvertFrom-Json, ConvertTo-Json, Test-Path, Get-Process, Start-Process, Stop-Process
- **Python**: python, python3, pip, pip3
- **Node**: node, npm, npx, pnpm, yarn
- **开发工具**: git, java, javac, mvn, gradle, go, cargo, rustc
- **容器**: docker, kubectl, helm, terraform
- **网络**: curl, wget, ping, nslookup, tracert, netstat, ipconfig
- **系统**: date, time, whoami, hostname, systeminfo, tasklist, taskkill

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
| "SOLO 的 Node.js 在哪" | `ModularData\ai-agent\vm\tools\node\node.exe` |
| "SOLO 的 Java 在哪" | `ModularData\ai-agent\vm\tools\app\jre\bin\java.exe` |
| "SOLO 的 ImageMagick 在哪" | `ModularData\ai-agent\vm\tools\app\imagemagick\magick.exe` |
| "SOLO 的 7zip 在哪" | `ModularData\ai-agent\vm\tools\app\7zip\7z.exe` |
| "SOLO 的 Tesseract 在哪" | `ModularData\ai-agent\vm\tools\app\tesseract\tesseract.exe` |
| "SOLO 的 Pandoc 在哪" | `ModularData\ai-agent\vm\tools\app\pandoc\pandoc.exe` |
| "SOLO 的 FFmpeg 在哪" | `ModularData\ai-agent\vm\tools\app\ffmpeg\ffmpeg.exe` |
| "SOLO 的 Graphviz 在哪" | `ModularData\ai-agent\vm\tools\app\Graphviz\bin\dot.exe` |
| "SOLO 的 Poppler 在哪" | `ModularData\ai-agent\vm\tools\app\poppler\pdftotext.exe` |
| "SOLO 的 SQLite 在哪" | `ModularData\ai-agent\vm\tools\app\sqlite\sqlite3.exe` |
| "SOLO 的 QPDF 在哪" | `ModularData\ai-agent\vm\tools\app\qpdf\qpdf.exe` |
| "SOLO 的 LibreOffice 在哪" | `ModularData\ai-agent\vm\tools\app\libreoffice\App\` |
| "SOLO 的 AI Agent 数据库" | `ModularData\ai-agent\database.db` |
| "SOLO 的沙箱配置" | `ModularData\ai-agent\sandbox\{hash}.json` |
| "SOLO 的 CKG 数据库" | `ModularData\ckg_server\env_codekg.db` |
| "SOLO 的 CKG 日志" | `ModularData\ckg_server\codekg.log.{日期}_{小时}` |
| "SOLO 的工具调用白名单" | `User\settings.json` (AI.toolcall.v2.command.allowList) |
| "SOLO 的 Shell 环境变量" | `User\settings.json` (solo.shell.env) |

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
| "工作区配置在哪" | `User\workspaceStorage\{hash}\workspace.json` (CN/国际版) 或 `Workspaces\{id}\workspace.json` (SOLO) |
| "全局存储在哪" | `User\globalStorage\storage.json` |
| "DevTools 设置在哪" | `Preferences` |
| "Cookie 在哪" | `Network\Cookies` |
| "代码片段在哪" | `User\snippets\` |
| "快捷键配置在哪" | `User\keybindings.json` |

---

## 使用示例

**示例 1**: 用户问 "SOLO 的 MCP 服务器配置在哪？"
- 版本识别: TRAE SOLO CN
- 路径: `C:\Users\{username}\AppData\Roaming\TRAE SOLO CN\User\mcp.json`

**示例 2**: 用户问 "SOLO 的 Python 环境在哪？"
- 版本识别: TRAE SOLO CN
- 路径: `C:\Users\{username}\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\vm\tools\python\python.exe`
- 说明: SOLO 内置完整 Python 环境，无需外部安装

**示例 3**: 用户问 "SOLO 的 AI 能用什么命令？"
- 版本识别: TRAE SOLO CN
- 路径: `User\settings.json` 中的 `AI.toolcall.v2.command.allowList`
- 说明: 查看白名单了解允许调用的命令

**示例 4**: 用户问 "SOLO 的代码知识图谱配置在哪？"
- 版本识别: TRAE SOLO CN
- 路径: `ModularData\ckg_server\local_env.json`
- 数据库: `ModularData\ckg_server\env_codekg.db`

**示例 5**: 用户问 "SOLO 的沙箱权限怎么配置？"
- 版本识别: TRAE SOLO CN
- 路径: `ModularData\ai-agent\sandbox\{hash}.json`
- 说明: 包含文件继承权限、只读权限和网络访问权限

**示例 6**: 用户问 "Trae CN 的 AI 规则怎么配置？"
- 版本识别: Trae CN
- 路径: `C:\Users\{username}\AppData\Roaming\Trae CN\User\settings.json`
- 相关配置项: `AI.rules.importClaudeMd`, `chat.useAgentsMdFile`

**示例 7**: 用户问 "Trae 的日志文件在哪？"
- 版本识别: Trae (国际版)
- 路径: `C:\Users\{username}\AppData\Roaming\Trae\logs\`

**示例 8**: 用户问 "历史记录保存在哪？" (未指定版本)
- **必须询问**: "您指的是哪个版本？SOLO、Trae CN 还是 Trae 国际版？"

---

## 注意事项

1. **版本区分最重要**: 三个版本的配置目录完全不同，必须先确认用户指的是哪个版本
2. `{username}` 需要替换为实际用户名 (如 `86150`)
3. `{workspace_id}` 和 `{folder_id}` 是动态生成的哈希或时间戳
4. 某些文件是二进制格式 (如 Cookies、LevelDB、SQLite 数据库)，需要专用工具读取
5. 修改配置前建议备份
6. 部分配置修改后需要重启对应版本的 TRAE 应用生效
7. **不要混淆版本**: 
   - `TRAE SOLO CN` ≠ `Trae CN`
   - `Trae CN` ≠ `Trae`
   - 三个版本配置不互通
8. **SOLO 的工具是内置的**: SOLO 拥有完整的内置工具链，不需要依赖系统 PATH
9. **SOLO 的沙箱权限**: AI Agent 的文件访问受沙箱权限控制，通过 `sandbox/{hash}.json` 配置
