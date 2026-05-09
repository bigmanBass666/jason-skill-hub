# Workspace & Folder Management

Dynamic workspace selection patterns for TRAE SOLO CN. **Do not hardcode workspace names** — always discover from snapshot.

## ⚠️ Key Principle

**All workspace names are DYNAMIC** — they come from the user's Solo instance. Always discover via `snapshot -i`.

---

## Contents

- [Discovering Workspaces](#discovering-workspaces)
- [Selecting a Workspace](#selecting-a-workspace)
- [Understanding Workspace Structure](#understanding-workspace-structure)
- [Opening Local Folders](#opening-local-folders)

---

## Discovering Workspaces

### Step 1: Take Snapshot

```bash
agent-browser snapshot -i
```

### Step 2: Identify Workspace Pattern

Workspaces appear as buttons with this pattern:

```
button "WORKSPACE_NAME New task task1 task2..." [ref=e18]
    - generic "WORKSPACE_NAME" [ref=e26]
    - button [ref=e27]           # Dropdown arrow
    - button "New task" [ref=e28] # Click to enter workspace
    - generic "Task 1" [ref=e29] # Existing tasks
    - generic "Task 2" [ref=e30]
```

### Step 3: Find Your Target Workspace

```bash
# Search for a specific workspace name
agent-browser snapshot -i | Select-String "TARGET_WORKSPACE_NAME"

# Get all workspace buttons
agent-browser snapshot -i | Select-String "New task task"
```

---

## Selecting a Workspace

### Method: Click "New task" Inside Workspace

**The key insight**: To enter a workspace, click its **"New task" button** (not the workspace name).

```bash
# 1. Find the workspace button
agent-browser snapshot -i | Select-String "MyTargetWorkspace"

# Example output:
#   button "MyTargetWorkspace New task Task1 Task2" [ref=e18]

# 2. Within that button, find "New task"
# It will be: button "New task" [ref=e28]

# 3. Click "New task" to enter the workspace
agent-browser find text "New task" click
```

### Why This Works

Clicking "New task" inside a workspace section:
1. Expands/enters that workspace
2. Shows the chat interface for that workspace
3. Sets it as the active workspace

### Alternative: Click Workspace Button Directly

```bash
# If you know the ref from current snapshot:
agent-browser click "@e18"  # The workspace button itself
agent-browser wait 500
```

---

## Understanding Workspace Structure

### Hierarchy

```
Sidebar
├── Navigation
│   ├── 新建任务 (New Task panel)
│   ├── 技能 (Skills panel)
│   └── 自动化 (Automation panel)
│
└── Workspaces (expandable buttons)
    └── button "WORKSPACE_NAME New task task1..." [ref=eXX]
        ├── generic "WORKSPACE_NAME" [ref=eYY]      # Name label
        ├── button [ref=eZZ]                        # Dropdown arrow
        ├── button "New task" [ref=eWW]             # Enter workspace
        └── generic "Task Name" [ref=eVV]          # Existing tasks
```

### Workspace Button Identification

Each workspace button contains:
- **Workspace name** at the start
- **"New task"** as first child item
- **List of existing tasks** below

Example for workspace "MyProject":
```
button "MyProject New task API Development Bug Fixes..." [ref=e18]
    - generic "MyProject" [ref=e26]
    - button [ref=e27]              # Dropdown
    - button "New task" [ref=e28]
    - generic "API Development" [ref=e29]
    - generic "Bug Fixes" [ref=e30]
```

---

## Opening Local Folders

### The "选择文件夹" Flow

To add a NEW local folder as a workspace:

```bash
# 1. Find the dropdown arrow next to any workspace
agent-browser snapshot -i | Select-String "button \[ref=e27\]"

# 2. Click the dropdown arrow
agent-browser click "@e27"  # or find the specific one
agent-browser wait 500

# 3. Look for "选择文件夹" in the dropdown menu
agent-browser snapshot -i | Select-String "选择文件夹"

# 4. Click "选择文件夹"
agent-browser find text "选择文件夹" click
```

**Note**: This opens the native OS file dialog — manual step required.

### For Existing Local Folders

If the folder is already open in Solo, it will appear in the workspace list. Just select it using the **"New task" method** above.

---

## Quick Reference

### Dynamic Discovery Commands

```bash
# Find ALL workspaces
agent-browser snapshot -i | Select-String "New task task"

# Find specific workspace
agent-browser snapshot -i | Select-String "WORKSPACE_NAME"

# Enter workspace (click New task inside it)
agent-browser find text "New task" click

# Get current workspace name (check bottom bar)
agent-browser snapshot -i | Select-String "·"
# Output: generic "WorkspaceName · timestamp" [ref=e13]
```

### Pattern Matching

```bash
# Match workspace by partial name
agent-browser snapshot -i | Select-String "partial"

# Match exact workspace name
agent-browser find text "ExactName" click --exact
```

---

## Common Patterns

### Pattern: User Says "Use workspace XYZ"

```bash
# 1. User specifies target workspace
# 2. Find it in snapshot
agent-browser snapshot -i | Select-String "XYZ"

# 3. Click "New task" inside that workspace
agent-browser find text "New task" click

# 4. Now you're in workspace XYZ
```

### Pattern: Switch Between Workspaces

```bash
# 1. Take snapshot to see all workspaces
agent-browser snapshot -i

# 2. Click "New task" inside target workspace
agent-browser find text "New task" click

# 3. Verify by checking bottom bar
agent-browser snapshot -i | Select-String "·"
# Should show: generic "TARGET_WORKSPACE · time"
```

### Pattern: List All Available Workspaces

```bash
# Get all workspace-containing buttons
agent-browser snapshot -i | Select-String "New task task"

# Extract just the names
agent-browser snapshot -i | Select-String "New task" | ForEach-Object {
    if ($_ -match "^button \"(.+?) New task") {
        $matches[1]
    }
}
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Workspace not found | Check exact spelling in snapshot |
| "New task" clicks wrong workspace | Use `find text --exact` or ref from snapshot |
| Dropdown not showing | Click the arrow button first |
| "选择文件夹" not visible | Open dropdown menu first |
| Wrong workspace active | Click "New task" inside target workspace |

---

## Key Rules

1. **Never hardcode workspace names** — always `snapshot -i` first
2. **Click "New task" inside workspace** — not the workspace name itself
3. **Refs change every session** — what worked last time may not work now
4. **Verify after clicking** — check bottom bar for current workspace
