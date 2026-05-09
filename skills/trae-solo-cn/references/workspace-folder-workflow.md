# Workspace & Folder Management

Dynamic workspace selection patterns for TRAE SOLO CN. **Do not hardcode workspace names** — always discover from snapshot.

## ⚠️ Key Principle

**All workspace names are DYNAMIC** — they come from the user's Solo instance. Always discover via `snapshot -i`.

---

## Contents

- [Understanding the Flow](#understanding-the-flow)
- [Scenario 1: New Folder (Not in Solo)](#scenario-1-new-folder-not-in-solo)
- [Scenario 2: Existing Workspace](#scenario-2-existing-workspace)
- [Scenario 3: Check Current Workspace](#scenario-3-check-current-workspace)
- [Discovering Workspaces](#discovering-workspaces)

---

## Understanding the Flow

### The Three Scenarios

```
┌─────────────────────────────────────────────────────────────────┐
│ User says: "Use folder X for AI chat"                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Is folder X already a workspace in Solo?                      │
│         ↓                                                       │
│    ┌─────────┐    ┌─────────┐                                  │
│    │   YES   │    │   NO    │                                  │
│    └────┬────┘    └────┬────┘                                  │
│         ↓              ↓                                        │
│  Click "New task"   Click "选择文件夹"                          │
│  inside workspace   (opens native dialog)                      │
│         ↓              ↓                                        │
│  Direct to chat     Auto-creates workspace                     │
│                     ↓                                           │
│                     Already in chat                            │
│                     (NO need to click "新建任务")               │
└─────────────────────────────────────────────────────────────────┘
```

**Critical Insight**: 
- **选择文件夹** = 新建工作区 + 新建对话（一步完成）
- **Existing workspace** = 点击其中的 "New task" 进入对话
- **不要重复点击 "新建任务"** — 选择文件夹后已经在对话界面了

---

## Scenario 1: New Folder (Not in Solo)

**When**: User specifies a local folder not yet in Solo's workspace list

### Flow

```bash
# Step 1: Start Solo (clean launch)
# ... (see SKILL.md for clean launch)

# Step 2: Open folder selector
agent-browser snapshot -i
# Find dropdown arrow next to any workspace
agent-browser click "@e27"  # dropdown arrow
agent-browser wait 500

# Step 3: Click "选择文件夹"
agent-browser find text "选择文件夹" click
# ⚠️ NATIVE FILE DIALOG OPENS — manual step

# Step 4: [USER] Selects folder in OS dialog

# Step 5: Verify new workspace created
agent-browser wait 3000
agent-browser snapshot -i | Select-String "NEW_WORKSPACE_NAME"

# Step 6: ✅ ALREADY IN CHAT INTERFACE
# NO need to click "新建任务"!
# Directly start chatting:
agent-browser find role textbox click
agent-browser keyboard type "分析这个项目的代码"
agent-browser press Enter
```

### Why No "新建任务"?

Because **选择文件夹** already:
1. ✅ Creates the workspace
2. ✅ Opens the chat interface
3. ✅ Sets it as active

Clicking "新建任务" again would be redundant.

---

## Scenario 2: Existing Workspace

**When**: User says "Use workspace XYZ" and XYZ is in the list

### Flow

```bash
# Step 1: Discover workspaces
agent-browser snapshot -i

# Step 2: Find target workspace
agent-browser snapshot -i | Select-String "XYZ"
# Output: button "XYZ New task Task1 Task2..." [ref=e18]

# Step 3: Click "New task" INSIDE that workspace
# This enters the workspace and opens chat
agent-browser find text "New task" click

# Step 4: ✅ Now in chat interface
agent-browser find role textbox click
agent-browser keyboard type "你的问题"
agent-browser press Enter
```

### Key Difference

| Action | Result |
|--------|--------|
| 选择文件夹 | Creates workspace + Opens chat (one step) |
| Click "New task" in workspace | Opens chat for existing workspace |

---

## Scenario 3: Check Current Workspace

**When**: User says "Continue working on current project"

### Flow

```bash
# Step 1: Check current workspace (bottom bar)
agent-browser snapshot -i | Select-String "·"
# Output: generic "CurrentWorkspaceName · 16:30" [ref=e13]

# Step 2: Verify it's the right one
# If yes → continue
# If no → switch (Scenario 2)

# Step 3: Continue chatting
agent-browser find role textbox click
agent-browser keyboard type "继续刚才的话题..."
agent-browser press Enter
```

---

## Discovering Workspaces

### List All Available Workspaces

```bash
# Get all workspace buttons
agent-browser snapshot -i | Select-String "New task task"

# Extract workspace names
agent-browser snapshot -i | ForEach-Object {
    if ($_ -match '^button "(.+?) New task') {
        $matches[1]
    }
}
```

### Check if Folder is Already a Workspace

```bash
# Search for folder name
$folderName = "MyWebApp"
agent-browser snapshot -i | Select-String $folderName

# If found → Scenario 2 (existing)
# If not found → Scenario 1 (new folder)
```

---

## Quick Reference

### Decision Tree

```
User: "Use [folder/workspace] X"
         ↓
    Is X in workspace list?
         ↓
    ┌────────┴────────┐
    YES              NO
    ↓                 ↓
Click "New task"   选择文件夹
in workspace       (native dialog)
    ↓                 ↓
Chat interface    Chat interface
    ↓                 ↓
Start typing      Start typing
```

### Common Mistakes

| Mistake | Why Wrong | Correct |
|---------|-----------|---------|
| 选择文件夹后点 "新建任务" | 已经在对话界面了 | 直接开始打字 |
| 点击工作区名称 | 不会进入对话 | 点击其中的 "New task" |
| 不检查当前工作区 | 可能在错误项目工作 | 先 `snapshot -i` 检查底部栏 |

---

## Key Rules

1. **选择文件夹后 = 已经在对话界面** — 不要再点 "新建任务"
2. **Existing workspace = 点击其中的 "New task"** — 不是工作区名称
3. **Always check current workspace first** — 底部栏显示当前项目
4. **Never hardcode** — 动态发现工作区列表
