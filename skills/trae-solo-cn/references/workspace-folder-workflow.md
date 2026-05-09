# Workspace & Folder Management

Complete guide for managing workspaces and selecting local folders in TRAE SOLO CN.

## Contents

- [Opening a Local Folder](#opening-a-local-folder)
- [Switching Workspaces](#switching-workspaces)
- [Understanding Workspace Structure](#understanding-workspace-structure)
- [Quick Reference](#quick-reference)

---

## Opening a Local Folder

### The Complete Workflow

**Step 1: Connect to TRAE SOLO CN**
```powershell
$wsUrl = (Invoke-RestMethod "http://127.0.0.1:9222/json/version").webSocketDebuggerUrl
agent-browser connect $wsUrl
agent-browser --color-scheme dark wait 2000
```

**Step 2: Open the Folder Selector**

The folder selector is hidden in the workspace dropdown menu:

```bash
# 1. Take snapshot to find the dropdown arrow
agent-browser snapshot -i

# 2. Look for the workspace button and its dropdown arrow
# Example structure:
#   button "jerry_ZhuanShengBen" [ref=e34]
#       button [ref=e35]  <- This is the dropdown arrow

# 3. Click the dropdown arrow
agent-browser click "@e35"  # Dropdown arrow ref
agent-browser wait 500

# 4. Now the menu appears with "选择文件夹" at the bottom
agent-browser snapshot -i | Select-String "选择文件夹"
# Output: menuitem "选择文件夹" [ref=e2]

# 5. Click "选择文件夹"
agent-browser click "@e2"
```

**Step 3: Handle Native File Dialog**

⚠️ **Important**: The file dialog is a **native OS component** that agent-browser cannot automate.

```
Manual action required:
1. Use mouse/keyboard to navigate to your folder
2. Click "选择文件夹" or press Enter
3. TRAE SOLO will create a workspace for that folder
```

**Step 4: Wait for Workspace to Load**
```bash
agent-browser wait 3000
agent-browser snapshot -i
# Look for your folder name in the workspace list
```

---

## Switching Workspaces

### Method 1: Sidebar Click

```bash
# Take snapshot to find workspace buttons
agent-browser snapshot -i

# Look for:
#   button "workspace_name New task task1 task2..." [ref=e21]
#       generic "workspace_name" [ref=e34]

# Click the workspace button
agent-browser click "@e34"
agent-browser wait 1000
```

### Method 2: Dropdown Menu

```bash
# Open workspace dropdown
agent-browser click "@e35"
agent-browser wait 500

# Look for workspace in menu
#   menuitem "Android" [ref=e19]
#   menuitem "trae-solo-unlock" [ref=e20]
#   menuitem "jerry_ZhuanShengBen" [ref=e23]

# Click desired workspace
agent-browser click "@e23"
agent-browser wait 1000
```

### Method 3: User Menu

```bash
# Click user avatar/name at bottom-left
agent-browser click "@e14"
agent-browser wait 500

# Same workspace list appears in dropdown
```

---

## Understanding Workspace Structure

### Sidebar Workspace Button Hierarchy

```
button "jerry_ZhuanShengBen New task 电商商品价格采集对比工具..." [ref=e21]
│
├── generic "jerry_ZhuanShengBen" [ref=e34]        <- Workspace name (clickable)
├── button [ref=e35]                                <- Dropdown arrow
├── button "New task" [ref=e36]                   <- Quick new task
└── generic "任务名" [ref=e37]                     <- Task items (clickable)
    ├── generic "任务名" [ref=e92]                 <- Duplicate ref
    └── ... (more tasks)
```

### Available Workspaces (Example)

| Workspace | Ref | Tasks |
|-----------|-----|-------|
| jerry_ZhuanShengBen | @e34 | 电商商品价格采集对比工具, Test Folder Path, 测试 Playwright... |
| Android | @e46 | 修复 PATH 环境变量问题, 新任务, 完成实验4文档 |
| trae-solo-unlock | @e52 | 深入研究 Solo 源码 |
| android_creator | @e67 | 创建AGENTS.md并自动Git提交, 修复 android_creator 脚本问题 |
| trae_solo_auto_model | @e75 | 红队首席AI任务, 查找交接文档, 开始工作... |
| 默认 | @e80 | 20+ various tasks including scheduled jobs |

### Creating New Workspace via Folder Selection

```bash
# The "选择文件夹" flow:
# 1. User clicks "选择文件夹" button
# 2. Native file dialog opens
# 3. User selects a folder (e.g., D:\Projects\my-new-app)
# 4. TRAE SOLO creates:
#    - A new workspace named after the folder
#    - Associates the folder path
#    - Adds to workspace list
```

---

## Quick Reference

### Finding Folder Selector Elements

```bash
# Pattern 1: Dropdown arrow
agent-browser snapshot -i | Select-String "button \[ref=e35\]"
# Output: button [ref=e35] (no text - this is the dropdown)

# Pattern 2: Select Folder menuitem
agent-browser snapshot -i | Select-String "选择文件夹"
# Output: menuitem "选择文件夹" [ref=e2]

# Pattern 3: All workspaces in dropdown
agent-browser click "@e35"
agent-browser snapshot -i | Select-String "menuitem.*\[ref=e[12][0-9]\]"
```

### Complete Folder → Chat Flow (Copy-Paste Ready)

```powershell
# === FOLDER → AI CHAT WORKFLOW ===

# 1. Connect
$wsUrl = (Invoke-RestMethod "http://127.0.0.1:9222/json/version").webSocketDebuggerUrl
agent-browser connect $wsUrl
agent-browser wait 2000

# 2. Open folder selector dropdown
agent-browser snapshot -i
agent-browser click "@e35"  # Dropdown arrow
agent-browser wait 500

# 3. Click "选择文件夹" (MANUAL STEP - use mouse)
agent-browser click "@e2"

# 4. [MANUAL] Select folder in OS dialog, confirm

# 5. Wait and verify
agent-browser wait 3000
agent-browser snapshot -i

# 6. Go to New Task panel
agent-browser click "@e4"
agent-browser wait 500

# 7. Start chatting
agent-browser snapshot -i | Select-String "textbox"
agent-browser click "@e89"  # textbox
agent-browser keyboard type "你的任务描述"
agent-browser press Enter

# 8. Monitor
for ($i = 0; $i -lt 30; $i++) {
    agent-browser wait 5000
    $snap = agent-browser snapshot -i
    if ($snap -match "任务耗时") {
        Write-Host "Done!"
        break
    }
}
```

### Common Refs for Folder Operations

| Element | Pattern | Example Ref |
|---------|---------|-------------|
| Workspace dropdown arrow | `button [ref=e35]` (no text) | @e35 |
| 选择文件夹 | `menuitem "选择文件夹"` | @e2 |
| Workspace name | `generic "workspace_name"` | @e34 |
| User menu | `generic "用户1918706576"` | @e14 |
| 工作区列表项 | `menuitem "workspace_name"` | @e23 |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "选择文件夹" not in snapshot | Click dropdown arrow first, then snapshot |
| Multiple workspaces shown | Use workspace dropdown to switch |
| Folder not creating workspace | Check if folder is valid (not empty path) |
| Workspace not switching | Use dropdown menu method for reliability |
| Old workspace still active | Click workspace name in sidebar |
