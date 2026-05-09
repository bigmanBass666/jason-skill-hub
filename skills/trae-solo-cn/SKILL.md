---
name: trae-solo-cn
description: Automate the TRAE SOLO CN desktop app (ByteDance's AI coding assistant) using agent-browser via Chrome DevTools Protocol. Use when the user needs to interact with TRAE SOLO CN, automate AI chat tasks, manage workspaces, install skills, configure automation jobs, or perform dogfooding/QA on the Solo application. Triggers include 'automate Solo', 'control TRAE SOLO', 'interact with Solo app', 'send prompt to Solo AI', 'switch Solo workspace', 'install Solo skill', 'configure Solo automation', 'dogfood TRAE SOLO', 'test TRAE SOLO CN', or any task requiring automation of the TRAE SOLO CN desktop application. Also trigger when the user mentions 'Solo桌面版', 'Trae Solo', 'TRAE SOLO', 'solo-cn', 'Solo AI', or asks to do anything with the Solo AI coding assistant.
allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*)
---

# TRAE SOLO CN Automation

Automate TRAE SOLO CN desktop app (ByteDance's AI coding assistant) via CDP. Covers workspace management, AI chat, task automation, skills marketplace, and exploratory testing.

## ⚠️ CRITICAL RULES

1. **No hardcoded refs** — `snapshot -i` before EVERY interaction, refs change every session
2. **No hardcoded workspace names** — Discover from snapshot, use `find text "name"`
3. **No hardcoded element refs** — Always use semantic `find` commands
4. **Use `keyboard type` not `fill`** — TRAE SOLO's input components require keyboard input

## Quick Start

### Step 1: Clean Launch (CRITICAL)

```powershell
# MUST kill existing processes first to avoid conflicts
$existing = Get-Process "TRAE SOLO CN" -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "Killing existing TRAE SOLO CN processes..."
    taskkill /F /IM "TRAE SOLO CN.exe" 2>&1 | Out-Null
    Start-Sleep -Seconds 3
}

# Verify cleanup
$remaining = Get-Process "TRAE SOLO CN" -ErrorAction SilentlyContinue
if ($remaining) {
    Write-Error "Failed to kill existing processes. Please restart computer."
    exit 1
}

# Launch fresh instance
Start-Process "D:\apps\TRAE SOLO CN\TRAE SOLO CN.exe" -ArgumentList "--remote-debugging-port=9222"
Start-Sleep -Seconds 5
```

### Step 2: Connect

```powershell
$wsUrl = (Invoke-RestMethod "http://127.0.0.1:9222/json/version").webSocketDebuggerUrl
agent-browser connect $wsUrl
agent-browser wait 2000
```

### Step 3: Health Check (Verify Window Loaded)

```powershell
# Verify TRAE SOLO window loaded correctly
$snapshot = agent-browser snapshot -i

# Check for critical UI elements
if ($snapshot -match "新建任务" -and $snapshot -match "技能" -and $snapshot -match "自动化") {
    Write-Host "✓ TRAE SOLO loaded successfully"
}
else {
    Write-Error "✗ Window not loaded properly. Key elements missing."
    Write-Error "Try: Kill all processes and restart"
    exit 1
}
```

### Step 4: Discover Current State

```powershell
agent-browser snapshot -i
```

---

## Core Workflow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. CONNECT                                                  │
│    $wsUrl = Get WebSocket URL → agent-browser connect      │
├─────────────────────────────────────────────────────────────┤
│ 2. DISCOVER                                                 │
│    agent-browser snapshot -i                               │
│    → See available workspaces, elements, current state     │
├─────────────────────────────────────────────────────────────┤
│ 3. NAVIGATE (based on user requirement)                    │
│    agent-browser find text "target_workspace" click        │
│    agent-browser find text "New task" click               │
├─────────────────────────────────────────────────────────────┤
│ 4. INTERACT                                                 │
│    agent-browser find role textbox click                  │
│    agent-browser keyboard type "user's prompt"             │
│    agent-browser press Enter                               │
├─────────────────────────────────────────────────────────────┤
│ 5. MONITOR                                                  │
│    Poll snapshot until "任务耗时" appears                  │
├─────────────────────────────────────────────────────────────┤
│ 6. EXTRACT                                                  │
│    agent-browser find text "复制全部" click                │
│    agent-browser screenshot --annotate result.png          │
└─────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Operations

### Step 1: Connect

```powershell
# Kill existing TRAE SOLO CN
Get-Process "TRAE SOLO CN" -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 2

# Launch with CDP port
Start-Process "D:\apps\TRAE SOLO CN\TRAE SOLO CN.exe" -ArgumentList "--remote-debugging-port=9222"
Start-Sleep -Seconds 5

# Connect via WebSocket URL
$wsUrl = (Invoke-RestMethod "http://127.0.0.1:9222/json/version").webSocketDebuggerUrl
agent-browser connect $wsUrl
agent-browser wait 2000
```

### Step 2: Discover Available Workspaces

```bash
# ALWAYS start with snapshot to see current state
agent-browser snapshot -i

# To find available workspaces, look for patterns like:
#   button "WORKSPACE_NAME New task task1 task2..." [ref=e18]
#   generic "WORKSPACE_NAME" [ref=e26]

# Example output:
#   button "MyProject New task Task1 Task2" [ref=e18]
#       generic "MyProject" [ref=e26]
#   button "AnotherProject New task ..." [ref=e19]
#       generic "AnotherProject" [ref=e36]
```

### Step 3: Select Target Workspace

**Based on user's requirement** (e.g., "use MyProject workspace"):

```bash
# Method: Click "New task" inside the target workspace
# 1. First, find which workspace button contains your target
agent-browser snapshot -i
# Look for: button "TARGET_WORKSPACE New task ..." [ref=eXX]

# 2. Find the "New task" button inside that workspace section
# It will be a child of the workspace button, like:
#   button "WORKSPACE_NAME New task task1..." [ref=e18]
#       ...
#       button "New task" [ref=e28]  <- This is the one to click

# 3. Click "New task" to enter that workspace
agent-browser find text "New task" click

# Or use ref if found in snapshot:
agent-browser click "@e28"
```

**Key insight**: Click the **workspace's "New task" button**, not the workspace name itself.

### Step 4: Send AI Chat Message

```bash
# 1. Find and click the textbox
agent-browser find role textbox click

# 2. Type your prompt (NOT fill - use keyboard type)
agent-browser keyboard type "你的问题或任务描述"

# 3. Send with Enter
agent-browser press Enter
```

### Step 5: Monitor Task Progress

```bash
# Poll until task completes (look for "任务耗时" = task duration)
for ($i = 0; $i -lt 30; $i++) {
    agent-browser wait 5000
    $snapshot = agent-browser snapshot -i

    if ($snapshot -match "任务耗时") {
        Write-Host "Task completed!"
        break
    }

    if ($snapshot -match "重试") {
        Write-Host "Task failed"
        break
    }
}
```

### Step 6: Extract Results

```bash
# Copy all output
agent-browser find text "复制全部" click

# Take screenshot
agent-browser screenshot --annotate result.png

# Get task duration
agent-browser find text "任务耗时" get text
```

---

## Semantic Find Commands (Always Use These)

```bash
# Navigation
agent-browser find text "新建任务" click    # New Task panel
agent-browser find text "技能" click       # Skills panel
agent-browser find text "自动化" click     # Automation panel

# Workspace (USER-SPECIFIC - discover from snapshot)
# Do NOT hardcode - always discover from snapshot first
# Look for: button "WORKSPACE_NAME New task ..." [ref=eXX]

# Element finding
agent-browser find role textbox click     # Input textbox
agent-browser find role button click      # Generic button

# Actions
agent-browser find text "复制全部" click   # Copy results
agent-browser find text "重试" click      # Retry failed task
```

---

## Common Workflows

### Workflow: Select Workspace and Send Message

```powershell
# User says: "Use workspace XYZ to analyze this code"

# 1. Connect
$wsUrl = (Invoke-RestMethod "http://127.0.0.1:9222/json/version").webSocketDebuggerUrl
agent-browser connect $wsUrl
agent-browser wait 2000

# 2. Discover workspaces
agent-browser snapshot -i

# 3. User specifies target workspace (e.g., "XYZ")
# 4. Find and click "New task" inside that workspace section
#    Look in snapshot for: button "XYZ New task ..." [ref=eXX]
#    Then find its child: button "New task" [ref=eYY]
agent-browser find text "New task" click

# 5. Send message
agent-browser find role textbox click
agent-browser keyboard type "analyze this code"
agent-browser press Enter

# 6. Monitor
for ($i = 0; $i -lt 30; $i++) {
    agent-browser wait 5000
    $snapshot = agent-browser snapshot -i
    if ($snapshot -match "任务耗时") { break }
}

# 7. Get results
agent-browser find text "复制全部" click
```

### Workflow: Switch Between Existing Tasks

```bash
# User wants to continue a specific task
# 1. Discover tasks in current workspace
agent-browser snapshot -i

# 2. Look for: generic "Task Name" [ref=eXX]
# 3. Click to select
agent-browser find text "Task Name" click
```

---

## Snapshot Pattern (MUST FOLLOW)

```bash
# BEFORE every click/type action:
agent-browser snapshot -i

# Example - finding the textbox:
# Output: textbox [ref=e133]:
agent-browser click "@e133"  # Use ref from THIS snapshot ONLY

# NEVER use refs from a previous snapshot!
# ALWAYS re-snapshot before critical actions
```

---

## Element Discovery Pattern

**How to find ANY element dynamically:**

```bash
# 1. Take snapshot
agent-browser snapshot -i

# 2. Search for your target
agent-browser snapshot -i | Select-String "target_text"

# 3. Use the ref shown in current snapshot
agent-browser click "@eNN"  # eNN from current snapshot

# OR use find (preferred)
agent-browser find text "exact_text" click
agent-browser find text "partial_text" click --exact
```

---

## Troubleshooting

### Startup Issues

| Symptom | Diagnosis | Solution |
|---------|-----------|----------|
| **AI requests fail / "请求失败"** | Multiple processes running | Kill all: `taskkill /F /IM "TRAE SOLO CN.exe"` |
| **Window blank / UI not loading** | Resource conflict | Kill all processes, restart fresh instance |
| **CDP connection refused** | App not started with debug flag | Kill and relaunch with `--remote-debugging-port=9222` |
| **Port 9222 not listening** | Process crashed | Check: `Get-Process "TRAE SOLO CN"`, restart if missing |

### Quick Diagnosis Commands

```powershell
# Check for multiple processes (should be 1 main + 7-8 subprocesses)
Get-Process "TRAE SOLO CN" | Measure-Object
# If Count > 10, kill all and restart

# Check if CDP port is listening
netstat -ano | findstr :9222
# Should show: TCP 127.0.0.1:9222 LISTENING

# Verify window loaded correctly
agent-browser snapshot -i | Select-String "新建任务|技能|自动化"
# Should find all three elements
```

### Runtime Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| "Element not found" | Ref stale | Re-snapshot, use new ref |
| "New task" not working | Wrong location | Click "New task" inside workspace section |
| Input doesn't appear | Custom component | Use `keyboard type`, not `fill` |
| Task never completes | Still running | Continue polling, or check for errors |
| Workspace list empty | Not expanded | Click workspace button to expand |
| Connection lost | Process crashed | Reconnect: `agent-browser connect $wsUrl` |

---

## Important Rules Summary

1. **ALWAYS `snapshot -i` BEFORE using refs**
2. **Use `find text` for navigation** — more reliable than hardcoded refs
3. **Use `keyboard type` NOT `fill`** — verified for this app
4. **Use `press Enter` to send** — more reliable than clicking send button
5. **Poll for "任务耗时" to detect completion** — don't use fixed timeouts
6. **Discover workspaces from snapshot** — don't assume they're hardcoded

---

## Application Info

| Property | Value |
|----------|-------|
| Framework | Electron |
| Debug Port | 9222 |
| CDP Endpoint | `http://127.0.0.1:9222/json/version` |
| Color Scheme | Dark |

## References

| Reference | Purpose |
|----------|---------|
| [references/workspace-folder-workflow.md](references/workspace-folder-workflow.md) | Dynamic workspace selection patterns |
| [references/trae-solo-tasks.md](references/trae-solo-tasks.md) | Common automation task patterns |
