# Workspace & Folder Management

Complete guide for managing workspaces and selecting local folders in TRAE SOLO CN.

## ⚠️ Official Rules

- **Refs are ephemeral** — Always `snapshot -i` before using refs
- **Use `find` commands** — Semantic positioning is more reliable than hardcoded refs
- **Use `wait --text`** — Instead of bare waits for monitoring

## Contents

- [Opening a Local Folder](#opening-a-local-folder)
- [Switching Workspaces](#switching-workspaces)
- [Understanding Workspace Structure](#understanding-workspace-structure)
- [Quick Reference](#quick-reference)

---

## Opening a Local Folder

### The Complete Workflow (Official Pattern)

**Step 1: Connect**
```powershell
$wsUrl = (Invoke-RestMethod "http://127.0.0.1:9222/json/version").webSocketDebuggerUrl
agent-browser connect $wsUrl
agent-browser --color-scheme dark wait 2000
```

**Step 2: Open Folder Selector**

⚠️ **The folder selector is in a dropdown menu:**

```bash
# 1. Click the dropdown arrow (use find to locate it)
agent-browser snapshot -i
# Look for a button with no text near the workspace name

# 2. Alternative: Use find text if you can see "选择文件夹"
agent-browser find text "选择文件夹" click

# 3. If that doesn't work, open the dropdown first
agent-browser find text "jerry_ZhuanShengBen" click
agent-browser wait 500
# Then look for 选择文件夹 in the menu
```

**Step 3: Handle Native File Dialog**

⚠️ **This is a native OS dialog — agent-browser cannot automate this:**

```
Manual action required:
1. Use mouse/keyboard to navigate to your folder
2. Click "选择文件夹" or press Enter
3. TRAE SOLO creates a workspace for that folder
```

**Step 4: Verify Workspace Loaded**
```bash
agent-browser wait 3000
agent-browser snapshot -i
# Look for your folder name in the workspace list
```

---

## Switching Workspaces

### Official Pattern: Use find text

```bash
# Find and click workspace by name
agent-browser find text "Android" click
agent-browser wait 1000

# Or use the full name
agent-browser find text "jerry_ZhuanShengBen" click
agent-browser wait 1000
```

### Alternative: Dropdown Menu

```bash
# Open dropdown (find the arrow button)
agent-browser snapshot -i
# Look for: button [ref=e35] (no text)

# Click it
agent-browser click "@e35"
agent-browser wait 500

# Find workspace in dropdown
agent-browser find text "Android" click
```

---

## Understanding Workspace Structure

### Sidebar Structure

```
┌─────────────────────────────────────────┐
│ 新建任务  (clickable)                   │
│ 技能     (clickable)                   │
│ 自动化    (clickable)                   │
├─────────────────────────────────────────┤
│ ▼ jerry_ZhuanShengBen    [dropdown]    │
│   ├─ New task                         │
│   ├─ 电商商品价格采集对比工具           │
│   ├─ Test Folder Path                  │
│   └─ ...                              │
│ ▼ Android                             │
│ ▼ trae-solo-unlock                   │
│ ▼ 默认                               │
└─────────────────────────────────────────┘
```

### Available Workspaces

| Workspace | How to Select |
|-----------|---------------|
| jerry_ZhuanShengBen | `find text "jerry_ZhuanShengBen" click` |
| Android | `find text "Android" click` |
| trae-solo-unlock | `find text "trae-solo-unlock" click` |
| 默认 | `find text "默认" click` |

---

## Quick Reference

### Complete Folder → Chat Flow (Copy-Paste Ready)

```powershell
# === FOLDER → AI CHAT (Official Pattern) ===

# 1. Connect
$wsUrl = (Invoke-RestMethod "http://127.0.0.1:9222/json/version").webSocketDebuggerUrl
agent-browser connect $wsUrl
agent-browser wait 2000

# 2. Open folder selector
agent-browser find text "选择文件夹" click
# [MANUAL] Select folder in OS dialog

# 3. Wait and navigate
agent-browser wait 3000
agent-browser find text "新建任务" click
agent-browser wait 500

# 4. Start chatting
agent-browser find textbox click
agent-browser keyboard type "你的任务描述"
agent-browser press Enter

# 5. Monitor completion
agent-browser wait --text "任务耗时"

# 6. Get results
agent-browser find text "复制全部" click
agent-browser screenshot --annotate result.png
```

### Essential find Commands

```bash
# Navigation
agent-browser find text "新建任务" click    # New Task panel
agent-browser find text "技能" click       # Skills panel
agent-browser find text "自动化" click     # Automation panel

# Workspace
agent-browser find text "workspace_name" click  # Switch workspace

# Actions
agent-browser find text "选择文件夹" click     # Open folder selector
agent-browser find text "复制全部" click        # Copy results
agent-browser find text "重试" click           # Retry task

# Monitoring
agent-browser find text "任务耗时" get text     # Get duration
agent-browser find text "正在执行命令" click    # Check running
```

### Snapshot Before Interacting

```bash
# ALWAYS do this before using refs:
agent-browser snapshot -i
# Now use refs from THIS snapshot only

# Example: Find textbox
agent-browser snapshot -i
# Output shows: textbox [ref=e89]
agent-browser click "@e89"  # Use ref from current snapshot!
```

### Better Waiting

```bash
# ✅ CORRECT: Wait for content
agent-browser wait --text "任务耗时"         # Wait for completion
agent-browser wait --text "正在执行命令"     # Wait for running

# ❌ AVOID: Bare waits
agent-browser wait 5000  # Slow and unreliable
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "选择文件夹" not found | Open dropdown first, then find |
| Workspace not switching | Use `find text "name"` not hardcoded ref |
| Element not found | Re-snapshot — refs are stale |
| Task never completes | Use `wait --text "任务耗时"` |
| Input doesn't work | Use `keyboard type` not `fill` |
