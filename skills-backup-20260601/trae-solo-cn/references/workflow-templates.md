# Workflow Templates for TRAE SOLO CN

Ready-to-use automation sequences for common tasks.

## Table of Contents

1. [Full Launch & Connect](#1-full-launch--connect)
2. [Create and Monitor a Task](#2-create-and-monitor-a-task)
3. [Batch Workspace Tour](#3-batch-workspace-tour)
4. [Install a Skill](#4-install-a-skill)
5. [Configure an Automation Job](#5-configure-an-automation-job)
6. [Extract All Task Outputs](#6-extract-all-task-outputs)
7. [Switch Model and Send Prompt](#7-switch-model-and-send-prompt)
8. [Screenshot Documentation](#8-screenshot-documentation)

---

## 1. Full Launch & Connect

Complete startup sequence from cold start to connected.

```powershell
# Step 1: Kill existing instances
Get-Process "TRAE SOLO CN" -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 3

# Step 2: Launch with CDP
Start-Process "D:\apps\TRAE SOLO CN\TRAE SOLO CN.exe" -ArgumentList "--remote-debugging-port=9222"
Start-Sleep -Seconds 5

# Step 3: Verify port
$portCheck = netstat -ano | findstr ":9222.*LISTENING"
if (-not $portCheck) {
    Write-Error "Port 9222 not listening. App may have failed to start."
    exit 1
}

# Step 4: Get WebSocket URL
$versionInfo = Invoke-RestMethod "http://127.0.0.1:9222/json/version"
$wsUrl = $versionInfo.webSocketDebuggerUrl
Write-Host "WebSocket URL: $wsUrl"

# Step 5: Connect
agent-browser connect $wsUrl

# Step 6: Verify
agent-browser snapshot -i
Write-Host "Connected successfully!"
```

---

## 2. Create and Monitor a Task

Create a new AI task and wait for completion.

```bash
# Step 1: Navigate to New Task
agent-browser snapshot -i
# Find the "新建任务" generic element and click it
agent-browser click "@NEW_TASK_REF"

# Step 2: Wait for task creation dialog
agent-browser wait 1000
agent-browser snapshot -i

# Step 3: Enter task description in the input box
agent-browser fill "@INPUT_REF" "帮我分析这个项目的代码质量，给出改进建议"

# Step 4: Send the task
agent-browser click "@SEND_REF"

# Step 5: Poll for completion (check every 10 seconds, up to 5 minutes)
for i in $(seq 1 30); do
    sleep 10
    result=$(agent-browser snapshot -i 2>/dev/null)
    if echo "$result" | grep -q "任务耗时"; then
        echo "Task completed!"
        break
    fi
    echo "Still running... ($i/30)"
done

# Step 6: Take screenshot of result
agent-browser screenshot "task-result.png"
```

---

## 3. Batch Workspace Tour

Visit each workspace and take a screenshot.

```bash
# Step 1: Get current snapshot
agent-browser snapshot -i > /tmp/snapshot.txt

# Step 2: Find all workspace buttons
# Look for button elements containing workspace names
# Common pattern: button "workspace-name New task ..."

# Step 3: Click each workspace and document
# (Refs change, so use snapshot to find them dynamically)

# For each workspace found:
agent-browser click "@WS_REF"
agent-browser wait 2000
agent-browser screenshot "workspace-NAME.png"
agent-browser snapshot -i > "workspace-NAME-snapshot.txt"
```

---

## 4. Install a Skill

Search and install a skill from the marketplace.

```bash
# Step 1: Open Skills panel
agent-browser snapshot -i
agent-browser click "@SKILLS_NAV_REF"  # "技能" in sidebar

# Step 2: Wait for panel to load
agent-browser wait 1000

# Step 3: Search for the skill
agent-browser fill "@SEARCH_REF" "git-commit"

# Step 4: Wait for results
agent-browser wait 2000
agent-browser snapshot -i

# Step 5: Find and click the install button (+ icon)
# Look for buttons near the skill card that are small icon buttons
agent-browser click "@INSTALL_REF"

# Step 6: Verify installation
agent-browser snapshot -i
# Check "已安装" count increased
```

---

## 5. Configure an Automation Job

Create a scheduled automation task.

```bash
# Step 1: Open Automation panel
agent-browser snapshot -i
agent-browser click "@AUTOMATION_NAV_REF"  # "自动化" in sidebar

# Step 2: Click "手动新建"
agent-browser click "@MANUAL_CREATE_REF"

# Step 3: Fill in automation details
agent-browser wait 1000
agent-browser snapshot -i
# Fill name, schedule, and action fields based on the form that appears

# Step 4: Save and enable
# Look for save/confirm button
agent-browser click "@SAVE_REF"

# Step 5: Verify in "已配置" tab
agent-browser click "@CONFIGURED_TAB_REF"
agent-browser snapshot -i
```

---

## 6. Extract All Task Outputs

Copy the output from all completed tasks in the current workspace.

```bash
# Step 1: Navigate to workspace
agent-browser snapshot -i
agent-browser click "@WS_REF"

# Step 2: Scroll through task history
# Each task has a "复制全部" button
agent-browser snapshot -i

# Step 3: For each task found, click "复制全部"
agent-browser click "@COPY_ALL_REF_1"
agent-browser clipboard read > "task-1-output.md"

agent-browser click "@COPY_ALL_REF_2"
agent-browser clipboard read > "task-2-output.md"

# Repeat for all tasks...
```

---

## 7. Switch Model and Send Prompt

Change the AI model and send a specific prompt.

```bash
# Step 1: Click model selector
agent-browser snapshot -i
agent-browser click "@MODEL_SELECTOR_REF"

# Step 2: Select model from combobox
agent-browser select_option "@MODEL_COMBOBOX_REF" ["GLM-4"]

# Step 3: Type prompt
agent-browser fill "@INPUT_REF" "用 Python 写一个快速排序算法"

# Step 4: Send
agent-browser click "@SEND_REF"

# Step 5: Wait and capture result
agent-browser wait 10000
agent-browser screenshot "model-response.png"
```

---

## 8. Screenshot Documentation

Take a complete set of annotated screenshots for documentation.

```bash
# Main interface
agent-browser screenshot --annotate "doc-main.png"

# Skills panel
agent-browser click "@SKILLS_NAV_REF"
agent-browser wait 1000
agent-browser screenshot --annotate "doc-skills.png"

# Automation panel
agent-browser click "@AUTOMATION_NAV_REF"
agent-browser wait 1000
agent-browser screenshot --annotate "doc-automation.png"

# Edit menu
agent-browser click "@EDIT_MENU_REF"
agent-browser wait 500
agent-browser screenshot --annotate "doc-edit-menu.png"

# Each workspace
# (Click each workspace, wait, screenshot)
```

---

## Tips for Building Custom Workflows

1. **Always snapshot before acting** — refs change between interactions
2. **Add waits between steps** — `agent-browser wait 1000` or `sleep 1`
3. **Check for disabled buttons** — some actions are unavailable during task execution
4. **Use `--annotate` screenshots** for debugging — they show ref numbers on the image
5. **Save snapshots to files** — `agent-browser snapshot -i > snapshot.txt` for later analysis
6. **Handle errors gracefully** — check exit codes and retry on transient failures
