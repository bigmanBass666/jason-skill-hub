# Element Patterns for TRAE SOLO CN

This reference documents stable patterns for finding UI elements by their semantic role and text content, rather than hardcoded `@e` refs which change per session.

## How to Use

Run `agent-browser snapshot -i` and look for elements matching these patterns. The ref numbers change, but the element types and text labels remain stable.

## Left Sidebar Navigation

| Element | Type | Text Pattern | How to Find |
|---------|------|-------------|-------------|
| New Task | generic | "新建任务" | `snapshot -i` → find generic with text "新建任务" |
| Skills | generic | "技能" | `snapshot -i` → find generic with text "技能" |
| Automation | generic | "自动化" | `snapshot -i` → find generic with text "自动化" |

## Workspace Buttons

| Element | Type | Text Pattern | Notes |
|---------|------|-------------|-------|
| Workspace container | button | Contains workspace name | Each workspace is a button with its name + task list |
| New task in workspace | button | "New task" | Appears inside each workspace's expandable section |
| Workspace name label | generic | Workspace name text | Clickable, navigates to workspace |

**Known workspace names** (may vary per user):
- `trae-solo-unlock`
- `jerry_ZhuanShengBen`
- `android_creator`
- `trae_solo_auto_model`
- `默认`

## Skills Panel

| Element | Type | Text Pattern | Notes |
|---------|------|-------------|-------|
| Upload Skill | button/menuitem | "上传技能" | Top of skills panel |
| Skills Marketplace | button | "技能市场" | Navigate to marketplace |
| Installed Count | button | "已安装 N" | Shows count of installed skills |
| Search Box | textbox | (placeholder: "搜索") | Search for skills |
| Category: All | button | "全部" | Filter by all categories |
| Category: Dev Tools | button | "开发工具" | Filter by development tools |
| Category: Data Analysis | button | "数据分析" | Filter by data analysis |
| Category: UI Design | button | "界面设计" | Filter by UI design |
| Category: Content | button | "内容创作" | Filter by content creation |
| Category: Efficiency | button | "效率提升" | Filter by efficiency tools |

## Automation Panel

| Element | Type | Text Pattern | Notes |
|---------|------|-------------|-------|
| Manual Create | button | "手动新建" | Create automation manually |
| Chat Create | button | "在对话中创建" | Create from conversation |
| Configured Tab | button | "已配置" | View active automations |
| History Tab | button | "执行历史" | View execution history |
| Templates Tab | button | "任务模板" | Browse templates |
| Enable Checkbox | checkbox | (no text) | Toggle automation on/off |

## Chat Interface (Bottom of Center Panel)

| Element | Type | Text Pattern | Notes |
|---------|------|-------------|-------|
| Input Box | textbox | (empty, multi-line) | Main prompt input |
| Send Button | button | (icon, no text) | Submit prompt — check it's not disabled |
| Attach Button | button | (icon, no text) | Upload files |
| Model Selector | generic | Model name (e.g., "GLM-5.1") | Click to open model picker |
| Model Combobox | combobox | Current model name | Select from dropdown |
| Settings Button | button | (icon, no text) | Chat settings |

## Task Result Actions

Each completed task card has these buttons (appear after AI responds):

| Element | Type | Text Pattern | Notes |
|---------|------|-------------|-------|
| Like | button | "赞" | Thumbs up (may be disabled) |
| Dislike | button | "踩" | Thumbs down (may be disabled) |
| Copy All | button | "复制全部" | Copy entire response (may be disabled) |
| Retry | button | "重试" | Re-execute the task (may be disabled) |
| Duration | button | "任务耗时 Xh Xm Xs" | Shows how long the task took |
| Thinking Process | generic | "思考过程" | Expandable, shows AI reasoning |
| Executed Commands | generic | "已执行 N 条命令" | Shows commands run during task |
| Code Block: Plain Text | button | "Plain Text" | Toggle code block format |
| Code Block: Copy | button | "Copy Code" | Copy code block content |

## Top Menu Bar

| Element | Type | Text Pattern | Notes |
|---------|------|-------------|-------|
| Edit Menu | menuitem | "编辑" | Opens edit dropdown |
| Help Menu | menuitem | "帮助" | Opens help dropdown |
| Undo | menuitem | "撤消 Control+Z" | In Edit menu |
| Redo | menuitem | "恢复 Control+Y" | In Edit menu |
| Cut | menuitem | "剪切 Control+X" | In Edit menu |
| Copy | menuitem | "复制 Control+C" | In Edit menu |
| Paste | menuitem | "粘贴 Control+V" | In Edit menu |
| Switch to Work mode | button | "Switch to Work mode" | Mode toggle |

## Right Panel

| Element | Type | Text Pattern | Notes |
|---------|------|-------------|-------|
| Todo Items | generic | Task step descriptions | Clickable, navigates to that step |
| Upload Progress | generic | Percentage text | Shows upload/download progress |

## Message Navigation

| Element | Type | Text Pattern | Notes |
|---------|------|-------------|-------|
| Navigate buttons | button | "Navigate to message: ..." | Quick-jump to specific messages |

## Finding Elements Programmatically

When you need to find a specific element without knowing its ref:

```bash
# Get full interactive snapshot
agent-browser snapshot -i

# Get snapshot as JSON for programmatic parsing
agent-browser snapshot -i --json

# Find element by text content
agent-browser find text "新建任务" click

# Find element by role
agent-browser find role button click --name "New task"
```
