---
name: trae-solo-cn
description: Automate the TRAE SOLO CN desktop app (ByteDance's AI coding assistant) using agent-browser via Chrome DevTools Protocol. Use when the user needs to interact with TRAE SOLO CN, automate AI chat tasks, manage workspaces, install skills, configure automation jobs, or perform dogfooding/QA on the Solo application. Triggers include 'automate Solo', 'control TRAE SOLO', 'interact with Solo app', 'send prompt to Solo AI', 'switch Solo workspace', 'install Solo skill', 'configure Solo automation', 'dogfood TRAE SOLO', 'test TRAE SOLO CN', or any task requiring automation of the TRAE SOLO CN desktop application. Also trigger when the user mentions 'Solo桌面版', 'Trae Solo', 'TRAE SOLO', 'solo-cn', 'Solo AI', or asks to do anything with the Solo AI coding assistant.
allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*)
---

# TRAE SOLO CN Automation

Automate TRAE SOLO CN desktop app (ByteDance's AI coding assistant) via CDP. Covers workspace management, AI chat, task automation, skills marketplace, and exploratory testing.

## ⚠️ IMPORTANT: Refs Are Ephemeral

**官方规范**: element refs (`@e1`, `@e2`, ...) are assigned **fresh on every snapshot**. They become **stale the moment the page changes**. Always `snapshot -i` before interacting.

**推荐方式**: Use `agent-browser find` commands for semantic定位 instead of hardcoded refs.

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

# Connect via WebSocket URL
$wsUrl = (Invoke-RestMethod "http://127.0.0.1:9222/json/version").webSocketDebuggerUrl
agent-browser connect $wsUrl

# Set dark mode (TRAE SOLO uses dark theme)
agent-browser --color-scheme dark snapshot -i
```

## Core Workflow

```
1. Connect      → Get WebSocket URL, connect
2. Navigate    → Use find commands, NOT hardcoded refs
3. Interact    → find → snapshot → click/type → wait → snapshot
4. Monitor     → Use wait --text instead of bare waits
5. Extract     → Copy results, screenshot
```

## Sending Messages (Official Pattern)

### Step 1: Find Elements Using Semantic Commands

```bash
# Navigate to New Task panel (recommended way)
agent-browser find text "新建任务" click
agent-browser wait 500

# Find the textbox using semantic search
agent-browser snapshot -i
# Look for: textbox element

# OR use find directly (preferred)
agent-browser find textbox click  # Click the textbox
```

### Step 2: Type Using keyboard Commands

TRAE SOLO uses custom input components where `fill` may not work:

```bash
# Focus the textbox first
agent-browser focus "@eN"  # Use ref from latest snapshot

# Type using keyboard (REQUIRED)
agent-browser keyboard type "你的指令内容"

# Send with Enter
agent-browser press Enter
```

### Step 3: Monitor Using wait --text

```bash
# ✅ CORRECT: Wait for completion indicator
agent-browser wait --text "任务耗时"

# ❌ WRONG: Bare wait
# agent-browser wait 5000  # Avoid this
```

### Step 4: Extract Results

```bash
# Find and click "复制全部" button
agent-browser find text "复制全部" click

# Take annotated screenshot
agent-browser screenshot --annotate result.png

# Get task duration
agent-browser find text "任务耗时" get text
```

## Complete Workflow: Folder → AI Chat

```powershell
# === FOLDER → AI CHAT (Official Pattern) ===

# 1. Connect
$wsUrl = (Invoke-RestMethod "http://127.0.0.1:9222/json/version").webSocketDebuggerUrl
agent-browser connect $wsUrl
agent-browser wait 2000

# 2. Open folder selector (find by semantic text)
agent-browser find text "选择文件夹" click
# NOTE: This opens native OS dialog - manual step required
agent-browser wait 3000

# 3. Go to New Task panel
agent-browser find text "新建任务" click
agent-browser wait 500

# 4. Find and use textbox
agent-browser snapshot -i
agent-browser find textbox click
agent-browser keyboard type "分析这个项目的结构和功能"

# 5. Send
agent-browser press Enter

# 6. Wait for completion (use wait --text)
agent-browser wait --text "任务耗时"

# 7. Get results
agent-browser find text "复制全部" click
agent-browser screenshot --annotate chat-result.png
```

## Semantic Find Commands (Recommended)

```bash
# Find by text content (MOST USEFUL)
agent-browser find text "新建任务" click
agent-browser find text "应用开发" click
agent-browser find text "复制全部" click
agent-browser find text "任务耗时" get text

# Find by role
agent-browser find textbox click
agent-browser find button click
agent-browser find generic click

# Find with exact match
agent-browser find text "Sign In" click --exact

# Find by partial text
agent-browser find text "新建" click  # Matches "新建任务"

# Chained: find then get
agent-browser find text "任务耗时" get text
```

## Snapshot Pattern

**ALWAYS snapshot before interacting with new refs:**

```bash
# 1. Take snapshot
agent-browser snapshot -i

# 2. Look for your element in output
# Example output:
#   @e1 generic "新建任务" [ref=e4]
#   @e2 textbox [ref=e89]

# 3. Use the ref shown in THAT snapshot
agent-browser click "@e89"  # Only use refs from current snapshot!
```

## Waiting Strategies (Official)

```bash
# ✅ BEST: Wait for specific content
agent-browser wait --text "任务耗时"           # Wait for completion
agent-browser wait --text "正在执行命令"        # Wait for running indicator

# ✅ GOOD: Wait for element
agent-browser wait "@e5"                      # Wait for element to appear

# ✅ GOOD: Wait for URL (if navigating)
agent-browser wait --url "**/dashboard"

# ✅ GOOD: Wait for network idle (SPA navigation)
agent-browser wait --load networkidle

# ❌ AVOID: Bare wait (makes scripts slow and flaky)
agent-browser wait 5000  # Only use for debugging
```

## Switching Workspaces

```bash
# Method 1: Find workspace by name
agent-browser find text "jerry_ZhuanShengBen" click
agent-browser wait 1000

# Method 2: Use dropdown
agent-browser find text "选择文件夹" click  # Opens dropdown
agent-browser wait 500
agent-browser find text "Android" click      # Select workspace
```

## Switching Panels

```bash
# Navigate between panels using find
agent-browser find text "新建任务" click     # New Task panel
agent-browser find text "技能" click        # Skills panel
agent-browser find text "自动化" click       # Automation panel
```

## Application Architecture

```
┌──────────────────────────────────────────────────────────────┐
│  Top Bar: [编辑] [帮助]                                     │
├──────────┬────────────────────────────┬──────────────────────┤
│ Sidebar  │  Center Area               │  Right Panel         │
│          │                            │                      │
│ 新建任务  │  ┌──────────────────────┐  │  (Task results)     │
│ 技能     │  │ 4 Template Cards     │  │                      │
│ 自动化    │  │ 应用开发/项目理解/...│  │                      │
│          │  ├──────────────────────┤  │                      │
│ Workspaces│  │ Input: [textbox]    │  │                      │
│ □ ws-1   │  │ Model: [combobox]   │  │                      │
│ □ ws-2   │  └──────────────────────┘  │                      │
├──────────┴────────────────────────────┴──────────────────────┤
│  Bottom: User info | 本地/工作树/云端                       │
└──────────────────────────────────────────────────────────────┘
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| "Element not found" | Ref stale from old snapshot | Re-snapshot and use new ref |
| "选择文件夹" not visible | Dropdown not opened | Click the dropdown arrow first |
| Input not working | Custom input component | Use `keyboard type` not `fill` |
| Task never completes | Using wrong wait | Use `wait --text "任务耗时"` |
| Wrong workspace | Using old ref | Use `find text "workspace_name"` |

## Important Rules

1. **Always `snapshot -i` before using a ref** — refs expire after page changes
2. **Use `find text "..."` instead of hardcoded refs** — more reliable
3. **Use `wait --text` instead of bare waits** — faster and more reliable
4. **Use `keyboard type` not `fill`** — TRAE SOLO's input components require it
5. **Set `--color-scheme dark`** — TRAE SOLO uses dark theme

## Application Info

| Property | Value |
|----------|-------|
| App Name | TRAE SOLO CN |
| Framework | Electron 39.2.7 |
| Engine | Chromium 142.0.7444.235 |
| Install Path | `D:\apps\TRAE SOLO CN\` |
| Debug Port | 9222 |
| CDP Endpoint | `http://127.0.0.1:9222/json/version` |
| Language | Chinese (Simplified) |
| Default Model | GLM-5V-Turbo |
| Color Scheme | Dark |

## References

| Reference | When to Read |
|-----------|--------------|
| [references/trae-solo-tasks.md](references/trae-solo-tasks.md) | Common automation patterns and task recipes |
| [references/workspace-folder-workflow.md](references/workspace-folder-workflow.md) | Opening folders, switching workspaces |
