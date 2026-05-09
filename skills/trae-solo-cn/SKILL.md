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
agent-browser click @WORKSPACE_REF
```

**Switch Panel:**
```bash
# "新建任务" (New Task) - usually @e4
# "技能" (Skills) - usually @e5
# "自动化" (Automation) - usually @e6
agent-browser click @e4
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
agent-browser click @COPY_ALL_REF

# Take screenshot of result
agent-browser screenshot --annotate task-result.png

# Get task duration
agent-browser get text @DURATION_REF
```

## Common Tasks

### Task: Create and Complete AI Task

```bash
# Full workflow
$wsUrl = (Invoke-RestMethod "http://127.0.0.1:9222/json/version").webSocketDebuggerUrl
agent-browser connect $wsUrl

# Switch to target workspace (optional)
agent-browser snapshot -i
agent-browser click @WORKSPACE_REF

# Create new task
agent-browser click @e4
agent-browser wait 1000

# Send prompt
agent-browser fill @TEXTBOX_REF "分析这段代码的性能问题"
agent-browser click @SEND_REF

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
agent-browser click @COPY_ALL_REF
agent-browser screenshot task-complete.png
```

### Task: Switch AI Model

```bash
agent-browser snapshot -i

# Click model selector (shows current model like "GLM-5.1")
agent-browser click @MODEL_SELECTOR_REF

# Select from dropdown
agent-browser select @MODEL_DROPDOWN_REF "GLM-5.1"
```

### Task: Install Skill from Marketplace

```bash
# Open Skills panel
agent-browser click @e5
agent-browser wait 1000

# Go to marketplace
agent-browser click @MARKETPLACE_REF

# Search for skill
agent-browser fill @SEARCH_REF "python"
agent-browser press Enter

# Click install on target skill
agent-browser snapshot -i
agent-browser click @INSTALL_BUTTON_REF
```

### Task: Batch Process Multiple Prompts

```powershell
$prompts = @(
    "优化这段SQL查询",
    "解释这个正则表达式",
    "重构这个函数"
)

$wsUrl = (Invoke-RestMethod "http://127.0.0.1:9222/json/version").webSocketDebuggerUrl
agent-browser connect $wsUrl

foreach ($prompt in $prompts) {
    # Create new task
    agent-browser click @e4
    agent-browser wait 1000
    
    # Send prompt
    agent-browser fill @INPUT_REF $prompt
    agent-browser click @SEND_REF
    
    # Wait for completion
    $completed = $false
    $attempts = 0
    while (-not $completed -and $attempts -lt 30) {
        agent-browser wait 5000
        $snapshot = agent-browser snapshot -i
        if ($snapshot -match "任务耗时") {
            $completed = $true
        }
        $attempts++
    }
    
    # Copy result
    if ($completed) {
        agent-browser click @COPY_ALL_REF
        Write-Host "Completed: $prompt"
    }
}
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

### Semantic Patterns

Look for elements by their visible text/role:

| What | Look For | Example Pattern |
|------|----------|-----------------|
| New Task button | `button "新建任务"` | Usually @e4 |
| Skills button | `button "技能"` | Usually @e5 |
| Automation button | `button "自动化"` | Usually @e6 |
| Input textbox | `textbox` near bottom | Varies |
| Send button | `button` near input | Usually has send icon |
| Workspace buttons | `button` with workspace name | Contains name like "trae-solo-unlock" |
| Copy All button | `button "复制全部"` | Appears when task done |
| Retry button | `button "重试"` | Appears when task fails |
| Task duration | `button "任务耗时"` | Shows elapsed time |

### Stable Identifiers

Some elements can be found by partial text matching:
- Workspaces: Look for buttons containing workspace name
- Task results: Look for "任务耗时" or "复制全部"
- Input area: Usually the only `textbox` in the center panel bottom area

## Input Methods for Electron Apps

If `fill` doesn't work (common in Electron apps), try these alternatives:

```bash
# Method 1: Click then keyboard type
agent-browser click @INPUT_REF
agent-browser keyboard type "your text"

# Method 2: Use inserttext (bypasses key events)
agent-browser click @INPUT_REF
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
8. **Try `keyboard type` if `fill` fails** — common in Electron apps

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
| Default Model | GLM-5.1 |
| Color Scheme | Dark |

## References

| Reference | When to Read |
|-----------|--------------|
| [references/trae-solo-tasks.md](references/trae-solo-tasks.md) | Common automation patterns and task recipes |

## Templates

| Template | Purpose |
|----------|---------|
| [templates/session-report-template.md](templates/session-report-template.md) | Document automation session results |
