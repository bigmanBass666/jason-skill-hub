---
name: trae-solo-cn
description: Automate the TRAE SOLO CN desktop app (ByteDance's AI coding assistant) using agent-browser via Chrome DevTools Protocol. Use when the user needs to interact with TRAE SOLO CN, automate AI chat tasks, manage workspaces, install skills, configure automation jobs, or perform dogfooding/QA on the Solo application. Triggers include 'automate Solo', 'control TRAE SOLO', 'interact with Solo app', 'send prompt to Solo AI', 'switch Solo workspace', 'install Solo skill', 'configure Solo automation', 'dogfood TRAE SOLO', 'test TRAE SOLO CN', or any task requiring automation of the TRAE SOLO CN desktop application. Also trigger when the user mentions 'Solo桌面版', 'Trae Solo', 'TRAE SOLO', 'solo-cn', 'Solo AI', or asks to do anything with the Solo AI coding assistant.
allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*)
---

# TRAE SOLO CN Automation

Automate TRAE SOLO CN desktop app (ByteDance's AI coding assistant) via CDP. Covers workspace management, AI chat, task automation, skills marketplace, and exploratory testing.

## ⚠️ CRITICAL RULES (Official Pattern)

### Rule 1: ALWAYS Snapshot First

**NEVER** click, type, or interact without taking a snapshot first!

```bash
# ❌ WRONG: Blind action
agent-browser click "@e5"

# ✅ CORRECT: Look first, then act
agent-browser snapshot -i
# [Read and understand the page structure]
agent-browser click "@e5"  # Now you know what you're clicking
```

### Rule 2: Re-Snapshot After Every Navigation

```bash
# After clicking anything that changes the page:
agent-browser click "@e10"
agent-browser wait 500
agent-browser snapshot -i  # MUST re-snapshot to see new state
```

### Rule 3: Understand Before Acting

```bash
# Before: Take snapshot
agent-browser snapshot -i

# During: Read and understand
# - What workspace am I in?
# - What panel is open?
# - What elements are available?
# - What is the current state?

# After: Then act based on understanding
```

---

## The OBSERVE-UNDERSTAND-ACT Pattern (Official)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. OBSERVE                                                  │
│    agent-browser snapshot -i                               │
│    → See the full page structure                           │
├─────────────────────────────────────────────────────────────┤
│ 2. UNDERSTAND                                               │
│    → What is the current state?                            │
│    → What elements are available?                          │
│    → What is my goal?                                      │
├─────────────────────────────────────────────────────────────┤
│ 3. ACT                                                      │
│    → Choose action based on observation                    │
│    → Execute with confidence                               │
├─────────────────────────────────────────────────────────────┤
│ 4. VERIFY                                                   │
│    agent-browser snapshot -i                               │
│    → Confirm action succeeded                              │
│    → See new state before next action                      │
└─────────────────────────────────────────────────────────────┘
```

---

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

### Step 3: OBSERVE - First Snapshot (MANDATORY)

```powershell
# ALWAYS start with snapshot
agent-browser snapshot -i

# Read the output to understand:
# - What workspaces are available?
# - What is the current workspace? (check bottom bar)
# - What panel is open?
# - What elements can I interact with?
```

### Step 4: Health Check

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

---

## State Awareness Checklist

Before any action, answer these questions:

1. **What workspace am I in?**
   ```bash
   agent-browser snapshot -i | Select-String "·"
   # Output: generic "WorkspaceName · 16:30" [ref=e13]
   ```

2. **What panel is open?**
   - 新建任务 (New Task)?
   - 技能 (Skills)?
   - 自动化 (Automation)?
   - Chat interface?

3. **What elements are available?**
   - Look for: buttons, textboxes, generic elements
   - Note their refs from current snapshot

4. **What is my goal?**
   - Send message to AI?
   - Switch workspace?
   - Check task status?

---

## Complete Workflow Example

### Example: Send Message to AI in Specific Workspace

```powershell
# === OBSERVE-UNDERSTAND-ACT WORKFLOW ===

# 1. OBSERVE: Take snapshot to see current state
Write-Host "=== Step 1: OBSERVE ==="
$snapshot = agent-browser snapshot -i

# 2. UNDERSTAND: Analyze the snapshot
Write-Host "=== Step 2: UNDERSTAND ==="
# - What workspaces are available?
# - What is the current workspace?
# - Is the chat interface open?

# Check current workspace (bottom bar)
$currentWorkspace = $snapshot | Select-String "·"
Write-Host "Current workspace: $currentWorkspace"

# 3. ACT: Based on observation
Write-Host "=== Step 3: ACT ==="

# If not in target workspace, navigate there
# Find "New task" button in target workspace section
agent-browser find text "New task" click
agent-browser wait 500

# 4. VERIFY: Re-snapshot to confirm navigation
Write-Host "=== Step 4: VERIFY ==="
agent-browser snapshot -i | Select-String "·"
# Should show target workspace

# 5. Continue with OBSERVE-UNDERSTAND-ACT for each step
# ...
```

---

## Common Workflows (With Mandatory Snapshots)

### Workflow: Select Workspace and Send Message

```powershell
# OBSERVE: See available workspaces
agent-browser snapshot -i
# Look for: button "WORKSPACE_NAME New task ..." [ref=eXX]

# UNDERSTAND: Identify target workspace
# User wants: "MyProject"
# Found: button "MyProject New task ..." [ref=e18]

# ACT: Click "New task" inside that workspace
agent-browser click "@e18"  # Or: find text "New task" click
agent-browser wait 500

# VERIFY: Confirm we're in chat interface
agent-browser snapshot -i
# Should see: textbox, input area

# OBSERVE: Find textbox
agent-browser snapshot -i | Select-String "textbox"
# Found: textbox [ref=e98]

# ACT: Send message
agent-browser find role textbox click
agent-browser keyboard type "分析代码性能"
agent-browser press Enter

# VERIFY: Check task is running
agent-browser snapshot -i | Select-String "正在|任务耗时"
```

---

## Snapshot Commands (Use These Frequently)

```bash
# Basic snapshot (always use this)
agent-browser snapshot -i

# Snapshot with search
agent-browser snapshot -i | Select-String "keyword"

# JSON snapshot (for parsing)
agent-browser snapshot --json > state.json

# Screenshot (visual confirmation)
agent-browser screenshot --annotate current-state.png
```

---

## Troubleshooting

### Problem: "I don't know what to click"

**Solution**: You didn't observe first!

```bash
# ALWAYS do this first:
agent-browser snapshot -i

# Then read the output to understand the page
```

### Problem: "Element not found"

**Solution**: Ref is stale, re-snapshot!

```bash
# ❌ WRONG: Using old ref
agent-browser click "@e5"  # From 5 minutes ago

# ✅ CORRECT: Fresh snapshot
agent-browser snapshot -i
# Find current ref
agent-browser click "@e25"  # Current ref
```

### Problem: "Clicked wrong thing"

**Solution**: Didn't understand the page structure

```bash
# Before clicking, always:
agent-browser snapshot -i
# Read and understand what each element is
# Then click with confidence
```

---

## Key Principles Summary

1. **Snapshot First** — Always `snapshot -i` before any action
2. **Re-Snapshot Often** — After every navigation or state change
3. **Understand Before Acting** — Read snapshot output, understand page structure
4. **Verify After Acting** — Re-snapshot to confirm action succeeded
5. **No Blind Actions** — Never click/type without knowing what you're interacting with

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
| [references/workspace-folder-workflow.md](references/workspace-folder-workflow.md) | Workspace selection with OBSERVE-ACT pattern |
| [references/trae-solo-tasks.md](references/trae-solo-tasks.md) | Task patterns with mandatory snapshots |
