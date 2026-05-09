---
name: trae-solo-cn
description: "Automate the TRAE SOLO CN desktop app (AI coding assistant by ByteDance) using agent-browser via Chrome DevTools Protocol. Use when the user needs to interact with TRAE SOLO CN, automate tasks in Solo, control the Solo desktop app, send messages to Solo AI, switch workspaces, manage skills, configure automation jobs, or test the Solo application. Triggers include 'automate Solo', 'control TRAE SOLO', 'interact with Solo app', 'send prompt to Solo', 'switch Solo workspace', 'install Solo skill', 'configure Solo automation', 'test TRAE SOLO CN', or any task requiring automation of the TRAE SOLO CN desktop application. Also trigger when the user mentions 'Solo桌面版', 'Trae Solo', 'TRAE SOLO', 'solo-cn', or asks to do anything with the Solo AI coding assistant."
---

# TRAE SOLO CN Automation Skill

Automate the TRAE SOLO CN desktop app (ByteDance's AI coding assistant) using agent-browser via CDP. This skill covers the full application: workspace management, task creation, AI chat, skills marketplace, and automation engine.

## Prerequisites

- agent-browser installed (`npm i -g agent-browser && agent-browser install`)
- TRAE SOLO CN installed at `D:\apps\TRAE SOLO CN\`
- The app must be launched with `--remote-debugging-port=9222`

## Quick Start

### Launch & Connect

```bash
# Kill any existing instance first
Get-Process "TRAE SOLO CN" -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 2

# Launch with CDP enabled
Start-Process "D:\apps\TRAE SOLO CN\TRAE SOLO CN.exe" -ArgumentList "--remote-debugging-port=9222"
Start-Sleep -Seconds 5

# Verify port is listening
netstat -ano | findstr :9222

# Get the WebSocket URL (required for connection)
$wsUrl = (Invoke-RestMethod "http://127.0.0.1:9222/json/version").webSocketDebuggerUrl

# Connect via WebSocket URL (NOT just the port number)
agent-browser connect $wsUrl

# Verify connection
agent-browser snapshot -i
```

**Important**: `agent-browser connect 9222` does NOT work for this app. You MUST use the full WebSocket URL from `/json/version`. This is because TRAE SOLO CN uses Electron's browser-level CDP target, and `connect <port>` tries to create a new tab target which Electron doesn't support.

### Connection Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| "CDP error: Target.createTarget: Not supported" | Used `connect 9222` instead of WebSocket URL | Use `connect $wsUrl` |
| "Connection refused" | App not launched with `--remote-debugging-port` | Kill and relaunch with the flag |
| "Auto-launch failed" | agent-browser tried to launch its own Chrome | Use `connect $wsUrl` not `--cdp` |
| Port 9222 not listening | App already running without debug flag | Kill process, relaunch with flag |

## Application Architecture

TRAE SOLO CN has 7 core modules. Understanding their layout is essential for reliable automation.

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

## Core Operations

### 1. Navigate Between Panels

The left sidebar has 3 main navigation items plus workspace list:

```bash
# New Task panel
agent-browser click "@e4"

# Skills panel
agent-browser click "@e5"

# Automation panel
agent-browser click "@e6"
```

Element refs are **dynamic** — they change when the app updates or when you switch panels. Always run `agent-browser snapshot -i` before interacting if you're unsure of the current refs.

### 2. Switch Workspaces

Workspaces appear as buttons in the left sidebar. Each workspace has its own task list:

```bash
# Take a snapshot to find current workspace refs
agent-browser snapshot -i

# Click a workspace button (refs change per session)
# Look for buttons containing workspace names like:
#   "trae-solo-unlock", "jerry_ZhuanShengBen", "android_creator", "默认"
agent-browser click "@WORKSPACE_REF"
```

### 3. Create a New Task

```bash
# Option A: Click "新建任务" in sidebar
agent-browser click "@e4"

# Option B: Click "New task" button inside a specific workspace
# First snapshot to find the right "New task" button
agent-browser snapshot -i
agent-browser click "@NEW_TASK_REF"
```

### 4. Send a Message to AI

```bash
# Find the input textbox (usually near bottom of center panel)
agent-browser snapshot -i

# Type your prompt
agent-browser fill "@INPUT_REF" "你的指令内容"

# Click send button
agent-browser click "@SEND_REF"

# Wait for response
agent-browser wait 5000
agent-browser snapshot -i
```

### 5. Switch AI Model

```bash
# Click the model selector (shows current model name like "GLM-5.1")
agent-browser snapshot -i
agent-browser click "@MODEL_SELECTOR_REF"

# Select from the combobox
agent-browser select_option "@MODEL_COMBOBOX_REF" ["GLM-5.1"]
```

### 6. Interact with Task Results

Each completed task has action buttons:

```bash
# Copy all task output
agent-browser click "@COPY_ALL_REF"

# Retry a failed task
agent-browser click "@RETRY_REF"

# Expand thinking process
agent-browser click "@THINKING_REF"

# View task duration
agent-browser get text "@DURATION_REF"
```

### 7. Skills Marketplace

```bash
# Open Skills panel
agent-browser click "@e5"

# Search for a skill
agent-browser fill "@SEARCH_REF" "python"

# Browse categories
agent-browser click "@CATEGORY_REF"  # e.g., "开发工具", "数据分析"

# Visit Skills Marketplace
agent-browser click "@MARKETPLACE_REF"

# Upload a custom skill
agent-browser click "@UPLOAD_REF"
```

### 8. Automation Engine

```bash
# Open Automation panel
agent-browser click "@e6"

# Create new automation manually
agent-browser click "@MANUAL_CREATE_REF"

# Create automation from conversation
agent-browser click "@CHAT_CREATE_REF"

# View execution history
agent-browser click "@HISTORY_REF"

# Browse task templates
agent-browser click "@TEMPLATES_REF"
```

### 9. Edit Menu Operations

```bash
# Open Edit menu
agent-browser click "@EDIT_MENU_REF"

# Available: Undo (Ctrl+Z), Redo (Ctrl+Y), Cut (Ctrl+X), Copy (Ctrl+C), Paste (Ctrl+V)
# Often easier to use keyboard shortcuts directly:
agent-browser press Control+a
agent-browser press Control+c
agent-browser press Control+v
```

## Element Reference Strategy

Element refs (`@e1`, `@e2`, etc.) are **session-specific** and change when:
- The app restarts
- You switch between panels
- The app updates to a new version

**Reliable strategy**: Instead of memorizing refs, use semantic patterns:

```bash
# Step 1: Always snapshot before interacting
agent-browser snapshot -i

# Step 2: Find elements by their visible text/role
# The snapshot output shows element type + text, e.g.:
#   button "新建任务" [ref=e4]
#   textbox [ref=e117]
#   button "Switch to Work mode" [ref=e2]

# Step 3: Use the ref from the fresh snapshot
agent-browser click "@e4"
```

For frequently needed elements, see `references/element-patterns.md` which documents stable patterns for finding elements by their semantic role rather than hardcoded refs.

## Common Automation Patterns

### Pattern: Monitor Task Progress

```bash
# After sending a task, poll for completion
agent-browser snapshot -i
# Look for "任务耗时" buttons which indicate completed tasks
# Look for "正在执行命令…" which indicates running tasks
```

### Pattern: Batch Workspace Operations

```bash
# Iterate through workspaces
$workspaces = @("trae-solo-unlock", "jerry_ZhuanShengBen", "android_creator")
foreach ($ws in $workspaces) {
    agent-browser snapshot -i
    # Find and click the workspace button containing $ws name
    # Perform operations...
}
```

### Pattern: Take Annotated Screenshots for Documentation

```bash
agent-browser screenshot --annotate "output.png"
# This produces a numbered overlay mapping each @e ref to its visual position
```

### Pattern: Extract Task Output

```bash
# Navigate to the task
agent-browser snapshot -i
# Find and click "复制全部" button
agent-browser click "@COPY_ALL_REF"
# The content is now in clipboard
agent-browser clipboard read
```

## Important Warnings

1. **Never use `agent-browser connect 9222`** — always use the full WebSocket URL from `/json/version`
2. **Element refs are ephemeral** — always `snapshot -i` before interacting if there's any doubt
3. **The "重试" (Retry) button re-executes the entire task** — including any write operations
4. **Don't click too fast** — add `sleep 1` between actions to let the UI settle
5. **The app must be relaunched with `--remote-debugging-port`** after any restart or update
6. **Multiple windows** — TRAE SOLO CN may open multiple CDP targets. Use `agent-browser tab` to list and switch between them.

## Application Info

| Property | Value |
|----------|-------|
| App Name | TRAE SOLO CN |
| Version | 1.107.1 |
| Framework | Electron 39.2.7 |
| Engine | Chromium 142.0.7444.235 |
| Install Path | `D:\apps\TRAE SOLO CN\` |
| Executable | `TRAE SOLO CN.exe` |
| Debug Port | 9222 (configurable) |
| CDP Endpoint | `http://127.0.0.1:9222/json/version` |
| Language | Chinese (Simplified) |
| Default AI Model | GLM-5.1 |

## Reference Files

| File | When to Read |
|------|-------------|
| `references/element-patterns.md` | When you need to find specific UI elements by semantic role |
| `references/workflow-templates.md` | When building complex multi-step automation sequences |
