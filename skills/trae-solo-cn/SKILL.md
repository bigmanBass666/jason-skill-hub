---
name: trae-solo-cn
description: Automate the TRAE SOLO CN desktop app (ByteDance's AI coding assistant) using agent-browser via Chrome DevTools Protocol. Use when the user needs to interact with TRAE SOLO CN, automate AI chat tasks, manage workspaces, install skills, configure automation jobs, or perform dogfooding/QA on the Solo application. Triggers include 'automate Solo', 'control TRAE SOLO', 'interact with Solo app', 'send prompt to Solo AI', 'switch Solo workspace', 'install Solo skill', 'configure Solo automation', 'dogfood TRAE SOLO', 'test TRAE SOLO CN', or any task requiring automation of the TRAE SOLO CN desktop application. Also trigger when the user mentions 'Solo桌面版', 'Trae Solo', 'TRAE SOLO', 'solo-cn', 'Solo AI', or asks to do anything with the Solo AI coding assistant.
allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*)
---

# TRAE SOLO CN Automation

Automate TRAE SOLO CN desktop app (ByteDance's AI coding assistant) via CDP. Covers workspace management, AI chat, task automation, skills marketplace, and exploratory testing.

## Prerequisites

- agent-browser installed (`npm i -g agent-browser && agent-browser install`)
- TRAE SOLO CN installed at `D:\apps\TRAE SOLO CN\`
- App launched with `--remote-debugging-port=9222`

## Quick Start

### Launch & Connect

```powershell
# Kill existing instance
Get-Process "TRAE SOLO CN" -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 2

# Launch with CDP
Start-Process "D:\apps\TRAE SOLO CN\TRAE SOLO CN.exe" -ArgumentList "--remote-debugging-port=9222"
Start-Sleep -Seconds 5

# Verify port
netstat -ano | findstr :9222

# Get WebSocket URL (CRITICAL for Electron apps)
$wsUrl = (Invoke-RestMethod "http://127.0.0.1:9222/json/version").webSocketDebuggerUrl

# Connect via WebSocket URL
agent-browser connect $wsUrl

# Set dark mode (TRAE SOLO uses dark theme)
agent-browser --color-scheme dark snapshot -i
```

**Critical**:
- Always use full WebSocket URL from `/json/version`, not just port 9222
- TRAE SOLO CN uses Electron's browser-level CDP target which doesn't support tab creation
- Always set `--color-scheme dark` to match the app's dark theme

## Core Workflow

```
1. Initialize    Launch app, connect CDP, set color scheme, verify session
2. Navigate      Switch workspace or panel
3. Interact      Send prompts, manage tasks, install skills
4. Monitor       Poll for task completion, capture results
5. Extract       Copy output, take screenshots, document
```

### 1. Initialize

```powershell
# Standard startup sequence
$wsUrl = (Invoke-RestMethod "http://127.0.0.1:9222/json/version").webSocketDebuggerUrl
agent-browser connect $wsUrl
agent-browser wait 2000
agent-browser --color-scheme dark snapshot -i
```

### 2. Navigate

**Switch Workspace:**
```bash
agent-browser snapshot -i
# Look for workspace buttons in sidebar (contain workspace names)
agent-browser click "@WORKSPACE_REF"
```

**Switch Panel:**
```bash
# "新建任务" (New Task) - @e4
# "技能" (Skills) - @e5
# "自动化" (Automation) - @e6
agent-browser click "@e4"
```

### 3. Interact - Send Message to AI

**Important**: TRAE SOLO uses custom input components where `fill` may not work. Use `keyboard type` instead:

```bash
# 1. Ensure in New Task panel
agent-browser click "@e4"

# 2. Find input (textbox near bottom of center panel)
agent-browser snapshot -i

# 3. Click input field to focus
agent-browser click "@e125"  # textbox ref

# 4. Type prompt using keyboard type (REQUIRED for this app)
agent-browser keyboard type "你的指令内容"

# 5. Press Enter to send (send button often disabled until text entered)
agent-browser press Enter

# 6. Wait for response (see Monitoring section)
```

**PowerShell Note**: In PowerShell, always quote refs like `"@e125"` to avoid array interpretation.

### 4. Monitor Task Progress

**Key indicators in snapshot:**
- `正在执行命令…` - Task is running
- `任务耗时` button - Task completed
- `重试` button - Task failed
- `复制全部` button - Output ready to copy

**Polling pattern:**
```bash
# Poll every 3-5 seconds
for ($i = 0; $i -lt 20; $i++) {
    agent-browser wait 5000
    agent-browser snapshot -i | Tee-Object -FilePath "snapshot-$i.txt"

    # Check if completed
    if (Select-String -Path "snapshot-$i.txt" -Pattern "任务耗时|复制全部") {
        Write-Host "Task completed!"
        break
    }
}
```

### 5. Extract Results

```bash
# Copy all output to clipboard
agent-browser click "@e142"  # 复制全部

# Take screenshot of result
agent-browser screenshot --annotate task-result.png

# Get task duration
agent-browser get text "@e135"  # 任务耗时 23s
```

## Common Tasks

### Task: Create New Project from Template

TRAE SOLO CN provides 4 built-in project templates in the New Task panel:

**Template 1: 应用开发 (Application Development)** @e8
```bash
# Click template to auto-fill prompt
agent-browser click "@e8"
agent-browser wait 500

# The textbox will be filled with:
# "开发一款支持多语种学习的在线教育平台，涵盖英语、日语、韩语等主流语言。
#  平台需打造沉浸式语言学习体验，提供以下能力：
#  1、分级课程体系
#  2、互动式学习模块（单词记忆、语法练习、口语跟读、听力训练）
#  3、学习进度追踪功能..."

# Then send the task
agent-browser click "@e89"  # textbox
agent-browser keyboard type ""  # Optional: modify or add more context
agent-browser press Enter
```

**Template 2: 项目理解 (Project Understanding)** @e9
```
"分析并理解这个项目仓库，生成结构化的完整的Code Wiki文档(md文件)。
这套文档需要包括项目整体架构、主要模块职责、关键类与函数说明、
依赖关系以及项目运行方式等关键信息"
```

**Template 3: 游戏创意 (Game Creation)** @e10
```
"设计并实现一个简单的像素风机甲对战小游戏。"
```

**Template 4: 工具脚本 (Tool/Script)** @e11
```
"设计并实现一个电商商品价格自动化采集与对比的脚本工具。"
```

### Task: Send Custom Prompt

```bash
# Click textbox and type your own prompt
agent-browser click "@e89"  # textbox ref
agent-browser keyboard type "你的自定义需求描述"
agent-browser press Enter
```

### Task: Create and Complete AI Task (Verified)

```bash
# Full workflow - VERIFIED WORKING
$wsUrl = (Invoke-RestMethod "http://127.0.0.1:9222/json/version").webSocketDebuggerUrl
agent-browser connect $wsUrl

# Switch to target workspace (optional)
agent-browser snapshot -i
agent-browser click "@WORKSPACE_REF"

# Create new task
agent-browser click "@e4"
agent-browser wait 1000

# Send prompt - MUST use keyboard type for this app
agent-browser click "@e89"  # textbox
agent-browser keyboard type "分析这段代码的性能问题"
agent-browser press Enter

# Monitor until complete
$completed = $false
while (-not $completed) {
    agent-browser wait 5000
    $snapshot = agent-browser snapshot -i
    if ($snapshot -match "任务耗时|复制全部") {
        $completed = $true
    }
}

# Extract result
agent-browser click "@e142"  # 复制全部
agent-browser screenshot task-complete.png
```

### Task: Switch AI Model

```bash
agent-browser snapshot -i

# Click model selector (shows current model like "GLM-5V-Turbo")
agent-browser click "@e144"  # combobox

# Select from dropdown
agent-browser select "@e144" "GLM-5V-Turbo"
```

### Task: Install Skill from Marketplace

```bash
# Open Skills panel
agent-browser click "@e5"
agent-browser wait 1000

# Go to marketplace
agent-browser click "@MARKETPLACE_REF"

# Search for skill
agent-browser fill "@SEARCH_REF" "python"
agent-browser press Enter

# Click install on target skill
agent-browser snapshot -i
agent-browser click "@INSTALL_BUTTON_REF"
```

## Tab Management

TRAE SOLO CN may have multiple windows or webviews. Use tab commands to manage them:

```bash
# List all available targets
agent-browser tab

# Example output:
#   0: [page]    TRAE SOLO CN - Main Window
#   1: [webview] Embedded Content

# Switch to a specific tab
agent-browser tab 1

# Switch by URL pattern
agent-browser tab --url "*settings*"
```

## Element Reference Strategy

### Dynamic Refs

Element refs (`@e1`, `@e2`) are **session-specific**. They change when:
- App restarts
- Panels switch
- App updates

**Always snapshot before interacting:**
```bash
agent-browser snapshot -i
# Then use refs from fresh output
```

### Semantic Patterns (Dogfood Verified)

Look for elements by their verified ref:

| What | Look For | Verified Ref | Notes |
|------|----------|--------------|-------|
| New Task button | `generic "新建任务"` | @e4 | ✅ |
| Skills button | `generic "技能"` | @e5 | ✅ |
| Automation button | `generic "自动化"` | @e6 | ✅ |
| Input textbox | `textbox` | @e125 | ✅ Key element |
| Enter to send | `press Enter` | Works | ✅ Send via Enter |
| Model selector | `combobox` | @e144 | Shows "GLM-5V-Turbo" |
| Copy All button | `button "复制全部"` | @e142 | ✅ |
| Retry button | `button "重试"` | @e143 | ✅ |
| Task duration | `button "任务耗时"` | @e135 | ✅ Format: "任务耗时 23s" |
| Thinking indicator | `generic "正在..."` | @e130 | e.g., "正在梳理问题…" |
| Like button | `button "赞"` | @e140 | ✅ |
| Dislike button | `button "踩"` | @e141 | ✅ |

### Finding Input Box Pattern

```bash
# Always find the textbox this way:
agent-browser snapshot -i | Select-String "textbox"
# Look for: textbox [ref=eNNN]:
```

### Finding Action Buttons Pattern

```bash
# After task completes, find these buttons:
agent-browser snapshot -i | Select-String "复制全部|重试|任务耗时"
```

## Input Methods for Electron Apps

If `fill` doesn't work (common in Electron apps), try these alternatives:

```bash
# Method 1: Click then keyboard type (VERIFIED WORKING)
agent-browser click "@e125"
agent-browser keyboard type "your text"

# Method 2: Use inserttext (bypasses key events)
agent-browser click "@e125"
agent-browser keyboard inserttext "your text"

# Method 3: Press keys individually
agent-browser press Control+a  # Select all
agent-browser press Delete     # Clear
agent-browser keyboard type "new text"
```

## Application Architecture

```
┌──────────────────────────────────────────────────────────────┐
│  Top Bar: Code | 编辑(E) | 帮助(H)                           │
├──────────┬────────────────────────────┬──────────────────────┤
│ Left     │  Center (Main Area)        │  Right Panel         │
│ Sidebar  │                            │                      │
│          │  ┌──────────────────────┐  │  ┌────────────────┐  │
│ 新建任务  │  │ Task Title + Time    │  │  │ Todo List      │  │
│ 技能     │  ├──────────────────────┤  │  │                │  │
│ 自动化    │  │                      │  │  │ ✓ Done item    │  │
│          │  │  Chat / Task Content  │  │  │ ○ Pending item │  │
│ Workspaces│  │  (Markdown support)  │  │  ├────────────────┤  │
│ □ ws-1   │  │                      │  │  │ Upload Status  │  │
│ □ ws-2   │  ├──────────────────────┤  │  └────────────────┘  │
│ □ ws-3   │  │ Input | Model | Send │  │                      │
│ □ ...    │  └──────────────────────┘  │                      │
├──────────┴────────────────────────────┴──────────────────────┤
│  Bottom: User info | Connection status                        │
└──────────────────────────────────────────────────────────────┘
```

**7 Core Modules:**
1. **新建任务** - Create and manage AI tasks
2. **技能** - Skills marketplace and management
3. **自动化** - Automation engine and job configuration
4. **Workspaces** - Project/workspace switching
5. **Chat Interface** - AI conversation and task execution
6. **Todo Panel** - Task checklist on right sidebar
7. **Upload Status** - File upload progress

## Connection Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| "CDP error: Target.createTarget: Not supported" | Used `connect 9222` instead of WebSocket URL | Use `connect $wsUrl` with full URL from `/json/version` |
| "Connection refused" | App not launched with debug flag | Kill and relaunch with `--remote-debugging-port` |
| "Auto-launch failed" | agent-browser tried to launch Chrome | Use `connect $wsUrl` not `--cdp` |
| Port 9222 not listening | App running without debug flag | Kill process, relaunch with flag |
| Multiple CDP targets | TRAE SOLO opened multiple windows | Use `agent-browser tab` to list and switch |
| Input not working | Electron custom input component | Use `keyboard type` instead of `fill` |
| Wrong color scheme | Default is light | Use `--color-scheme dark` |

## Important Warnings

1. **Never use `agent-browser connect 9222`** — always use full WebSocket URL from `/json/version`
2. **Element refs are ephemeral** — always `snapshot -i` before interacting if unsure
3. **The "重试" (Retry) button re-executes entire task** — including all write operations
4. **Don't click too fast** — add `wait 1000` between actions for UI to settle
5. **App must be relaunched with `--remote-debugging-port`** after restart or update
6. **Multiple windows possible** — use `agent-browser tab` to manage
7. **Use `--color-scheme dark`** — TRAE SOLO uses dark theme
8. **Use `keyboard type` NOT `fill`** — Verified that fill doesn't work on this app
9. **PowerShell quoting** — Always quote refs like `"@e125"` to avoid array interpretation

## Application Info

| Property | Value |
|----------|-------|
| App Name | TRAE SOLO CN |
| Framework | Electron 39.2.7 |
| Engine | Chromium 142.0.7444.235 |
| Install Path | `D:\apps\TRAE SOLO CN\` |
| Executable | `TRAE SOLO CN.exe` |
| Debug Port | 9222 (configurable) |
| CDP Endpoint | `http://127.0.0.1:9222/json/version` |
| Language | Chinese (Simplified) |
| Default Model | GLM-5V-Turbo |
| Color Scheme | Dark |

## References

| Reference | When to Read |
|-----------|--------------|
| [references/trae-solo-tasks.md](references/trae-solo-tasks.md) | Common automation patterns and task recipes |

## Templates

| Template | Purpose |
|----------|---------|
| [templates/session-report-template.md](templates/session-report-template.md) | Document automation session results |
