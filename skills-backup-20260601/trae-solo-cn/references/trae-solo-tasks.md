# TRAE SOLO CN Task Patterns

Common automation task patterns for TRAE SOLO CN. **All patterns use dynamic discovery** — no hardcoded refs or names.

## ⚠️ Key Principle

**All element refs change every session. All workspace/task names come from the user's instance. Always use `snapshot -i` to discover current state.**

---

## Contents

- [Sending Messages](#sending-messages)
- [Monitoring Tasks](#monitoring-tasks)
- [Extracting Results](#extracting-results)
- [Task Templates](#task-templates)
- [Error Handling](#error-handling)

---

## Sending Messages

### Standard Pattern

```bash
# 1. Navigate to chat area (click New task if needed)
agent-browser find text "新建任务" click
agent-browser wait 500

# 2. Find and focus the textbox
agent-browser find role textbox click

# 3. Type message (NOT fill - use keyboard type)
agent-browser keyboard type "你的问题或任务描述"

# 4. Send
agent-browser press Enter
```

### Multi-Part Message

```bash
# Type in parts if message is long
agent-browser find role textbox click
agent-browser keyboard type "第一部分内容"
agent-browser press Shift+Enter  # Newline

# Continue typing
agent-browser keyboard type "第二部分内容"
agent-browser press Enter
```

### With Context (Multi-turn)

```bash
# After first response, continue in same thread
agent-browser find role textbox click
agent-browser keyboard type "针对你刚才的回答，有一个跟进问题..."
agent-browser press Enter
```

---

## Monitoring Tasks

### Poll Until Completion

```bash
# Pattern: Keep checking until "任务耗时" appears
$completed = $false
$attempts = 0
$maxAttempts = 30

while (-not $completed -and $attempts -lt $maxAttempts) {
    agent-browser wait 5000
    $snapshot = agent-browser snapshot -i

    if ($snapshot -match "任务耗时") {
        Write-Host "Task completed!"
        $completed = $true
    }
    elseif ($snapshot -match "重试") {
        Write-Host "Task failed - retry available"
        $completed = $true
    }
    elseif ($snapshot -match "正在") {
        Write-Host "Task still running..."
    }

    $attempts++
}

if (-not $completed) {
    Write-Warning "Timeout waiting for task completion"
}
```

### Check Current Status

```bash
# Quick status check
agent-browser snapshot -i | Select-String "正在|任务耗时|重试"

# Possible outputs:
# - "正在梳理问题..." = AI is thinking
# - "正在执行命令..." = Task is running
# - "任务耗时 23s" = Completed with duration
# - "重试" = Failed, retry available
```

### Progress Indicators

| Indicator | Meaning | Action |
|-----------|---------|--------|
| `正在梳理问题…` | AI analyzing | Wait |
| `正在执行命令…` | Task running | Wait |
| `任务耗时 XXs` | Completed | Extract results |
| `重试` | Failed | Retry or debug |

---

## Extracting Results

### Copy All Output

```bash
# Find and click "复制全部"
agent-browser find text "复制全部" click

# Or use ref if found
agent-browser click "@e129"
```

### Take Screenshot

```bash
# Annotated screenshot (shows element refs)
agent-browser screenshot --annotate result.png

# Regular screenshot
agent-browser screenshot result.png
```

### Get Task Duration

```bash
# Find and get text of duration element
agent-browser find text "任务耗时" get text

# Example output: "任务耗时 23s"
```

### Read Clipboard (After Copy)

```bash
# After clicking "复制全部", read clipboard
# PowerShell:
Get-Clipboard

# Or in bash (if available):
powershell -Command "Get-Clipboard"
```

---

## Task Templates

### Template: Code Analysis

```bash
# 1. Navigate
agent-browser find text "新建任务" click
agent-browser wait 500

# 2. Send prompt
agent-browser find role textbox click
agent-browser keyboard type "分析这段代码的性能问题和潜在bug:
\`\`\`
$PCODE
\`\`\`

请指出:
1. 性能问题
2. 代码坏味道
3. 安全漏洞
4. 改进建议"
agent-browser press Enter

# 3. Monitor
# ... (use poll pattern above)

# 4. Extract
agent-browser find text "复制全部" click
```

### Template: Bug Investigation

```bash
# 1. Navigate
agent-browser find text "新建任务" click

# 2. Send
agent-browser find role textbox click
agent-browser keyboard type "调查以下错误:
\`\`\`
$ERROR_LOG
\`\`\`

可能的原因是什么？如何修复？"
agent-browser press Enter

# 3. Monitor & extract
```

### Template: Code Generation

```bash
# 1. Navigate
agent-browser find text "新建任务" click

# 2. Send with requirements
agent-browser find role textbox click
agent-browser keyboard type "用$LANGUAGE实现以下功能:
$REQUIREMENTS

要求:
1. 生产级代码质量
2. 包含适当的错误处理
3. 添加注释说明"
agent-browser press Enter

# 3. Monitor & extract
```

---

## Error Handling

### Connection Lost

```bash
# If commands start failing
$wsUrl = (Invoke-RestMethod "http://127.0.0.1:9222/json/version").webSocketDebuggerUrl
agent-browser connect $wsUrl
agent-browser wait 2000

# Resume from last state
agent-browser snapshot -i
```

### Element Not Found

```bash
# If find fails, re-snapshot
agent-browser snapshot -i

# Search again with new snapshot
agent-browser snapshot -i | Select-String "target_element"

# Try again with updated ref
```

### Task Timeout

```bash
# If task takes too long
$timeout = 180  # seconds
$startTime = Get-Date

# In loop:
if ((Get-Date) - $startTime).TotalSeconds -gt $timeout {
    Write-Warning "Task timeout"
    # Take screenshot for debugging
    agent-browser screenshot timeout.png
    break
}
```

### Retry Failed Task

```bash
# Check if retry button exists
agent-browser snapshot -i | Select-String "重试"

# If found, click it
agent-browser find text "重试" click

# Or use ref
agent-browser click "@e130"

# Monitor the retry
```

---

## Common Patterns

### Pattern: Complete Chat Workflow

```powershell
# === COMPLETE WORKFLOW ===

# 1. Connect
$wsUrl = (Invoke-RestMethod "http://127.0.0.1:9222/json/version").webSocketDebuggerUrl
agent-browser connect $wsUrl
agent-browser wait 2000

# 2. Enter target workspace
agent-browser find text "New task" click
agent-browser wait 500

# 3. Send message
agent-browser find role textbox click
agent-browser keyboard type $UserPrompt
agent-browser press Enter

# 4. Monitor
do {
    agent-browser wait 5000
    $snapshot = agent-browser snapshot -i
} until ($snapshot -match "任务耗时" -or $snapshot -match "重试")

# 5. Extract results
if ($snapshot -match "任务耗时") {
    agent-browser find text "复制全部" click
    agent-browser screenshot result.png
    Write-Host "Success!"
}
else {
    Write-Host "Task failed"
}
```

### Pattern: Quick Status Check

```bash
# Single command to check if task is done
agent-browser snapshot -i | Select-String "任务耗时|正在|重试"
```

### Pattern: Navigate to Specific Task

```bash
# User wants to continue existing task
agent-browser snapshot -i | Select-String "TaskName"
# Find the task ref

agent-browser find text "TaskName" click
```

---

## Key Rules

1. **No hardcoded refs** — `snapshot -i` before every action
2. **Use `keyboard type`** — not `fill`
3. **Use `press Enter`** — to send messages
4. **Poll for "任务耗时"** — to detect completion
5. **Handle errors gracefully** — reconnect, retry, timeout

---

## Quick Reference

```bash
# Navigation
agent-browser find text "新建任务" click    # New Task
agent-browser find text "技能" click       # Skills
agent-browser find text "自动化" click      # Automation

# Input
agent-browser find role textbox click     # Focus textbox
agent-browser keyboard type "message"      # Type (NOT fill)
agent-browser press Enter                 # Send

# Output
agent-browser find text "复制全部" click   # Copy results
agent-browser screenshot --annotate .png  # Screenshot

# Status
agent-browser snapshot -i | Select-String "任务耗时"  # Done?
agent-browser snapshot -i | Select-String "正在"      # Running?
agent-browser snapshot -i | Select-String "重试"      # Failed?
```
