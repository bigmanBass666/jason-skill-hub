# TRAE SOLO CN Common Tasks & Patterns

Reference guide for common automation patterns and task recipes when interacting with TRAE SOLO CN.

## Contents

- [Task Patterns](#task-patterns)
- [Monitoring Patterns](#monitoring-patterns)
- [Error Handling](#error-handling)
- [Element Finding Strategies](#element-finding-strategies)
- [Batch Operations](#batch-operations)
- [State Detection](#state-detection)

---

## Task Patterns

### Pattern: Send Single Prompt and Wait

**Goal:** Send one message to AI and capture the complete response.

```powershell
function Send-SoloPrompt {
    param([string]$Prompt, [int]$TimeoutSeconds = 120)
    
    # Navigate to New Task
    agent-browser click @e4
    agent-browser wait 1000
    
    # Send prompt
    agent-browser fill @INPUT_REF $Prompt
    agent-browser click @SEND_REF
    
    # Monitor completion
    $startTime = Get-Date
    $completed = $false
    
    while (-not $completed) {
        agent-browser wait 5000
        $snapshot = agent-browser snapshot -i
        
        # Check completion indicators
        if ($snapshot -match "任务耗时|复制全部") {
            $completed = $true
            Write-Host "Task completed!"
        }
        
        # Check timeout
        if ((Get-Date) - $startTime).TotalSeconds -gt $TimeoutSeconds) {
            Write-Warning "Timeout waiting for task completion"
            return $null
        }
        
        # Check for failure
        if ($snapshot -match "重试") {
            Write-Warning "Task failed - retry button detected"
            return $null
        }
    }
    
    # Extract result
    agent-browser click @COPY_ALL_REF
    agent-browser screenshot task-result.png
    
    return @{
        Success = $true
        Screenshot = "task-result.png"
    }
}
```

---

### Pattern: Multi-Turn Conversation

**Goal:** Have a back-and-forth conversation with context preserved.

```powershell
# Start conversation
agent-browser click @e4
agent-browser wait 1000

# First message
agent-browser fill @INPUT_REF "解释什么是依赖注入"
agent-browser click @SEND_REF

# Wait for first response
Wait-SoloTaskComplete

# Follow-up (context preserved in same task)
agent-browser fill @INPUT_REF "能给一个C#的例子吗？"
agent-browser click @SEND_REF

Wait-SoloTaskComplete

# Another follow-up
agent-browser fill @INPUT_REF "这个和工厂模式有什么区别？"
agent-browser click @SEND_REF

Wait-SoloTaskComplete
```

**Key Point:** Keep sending messages in the same task window to maintain context.

---

### Pattern: Compare Multiple AI Models

**Goal:** Send the same prompt to different models and compare outputs.

```powershell
$models = @("GLM-5.1", "Claude", "GPT-4")
$prompt = "优化这段代码的性能"
$results = @{}

foreach ($model in $models) {
    # Create new task
    agent-browser click @e4
    agent-browser wait 1000
    
    # Switch model
    agent-browser click @MODEL_SELECTOR_REF
    agent-browser select_option @MODEL_DROPDOWN_REF $model
    agent-browser wait 500
    
    # Send prompt
    agent-browser fill @INPUT_REF $prompt
    agent-browser click @SEND_REF
    
    # Wait and capture
    Wait-SoloTaskComplete
    agent-browser click @COPY_ALL_REF
    agent-browser screenshot "result-$model.png"
    
    $results[$model] = "result-$model.png"
}
```

---

## Monitoring Patterns

### Pattern: Poll with State Machine

**Goal:** Robustly detect task state with clear transitions.

```powershell
enum TaskState {
    Unknown
    Running
    Completed
    Failed
    Timeout
}

function Get-TaskState {
    $snapshot = agent-browser snapshot -i
    
    if ($snapshot -match "正在执行命令|正在思考") {
        return [TaskState]::Running
    }
    elseif ($snapshot -match "任务耗时|复制全部") {
        return [TaskState]::Completed
    }
    elseif ($snapshot -match "重试") {
        return [TaskState]::Failed
    }
    else {
        return [TaskState]::Unknown
    }
}

# Usage
$state = [TaskState]::Unknown
$attempts = 0
$maxAttempts = 30

while ($state -ne [TaskState]::Completed -and $attempts -lt $maxAttempts) {
    agent-browser wait 5000
    $state = Get-TaskState
    $attempts++
    
    Write-Host "State: $state (attempt $attempts/$maxAttempts)"
    
    if ($state -eq [TaskState]::Failed) {
        Write-Error "Task failed!"
        break
    }
}
```

---

### Pattern: Progress Logging

**Goal:** Track task progress with periodic snapshots.

```powershell
$taskId = [Guid]::NewGuid().ToString().Substring(0, 8)
$outputDir = "solo-tasks/$taskId"
New-Item -ItemType Directory -Path $outputDir -Force

# Start task
agent-browser click @e4
agent-browser fill @INPUT_REF "分析大型代码库"
agent-browser click @SEND_REF

# Log progress every 10 seconds
$counter = 0
while ($true) {
    agent-browser wait 10000
    $timestamp = Get-Date -Format "HHmmss"
    
    # Save snapshot
    agent-browser snapshot -i | Out-File "$outputDir/snapshot-$timestamp.txt"
    
    # Save screenshot every 30 seconds
    if ($counter % 3 -eq 0) {
        agent-browser screenshot "$outputDir/progress-$timestamp.png"
    }
    
    # Check completion
    $snapshot = Get-Content "$outputDir/snapshot-$timestamp.txt" -Raw
    if ($snapshot -match "任务耗时") {
        agent-browser screenshot "$outputDir/final-$timestamp.png"
        agent-browser click @COPY_ALL_REF
        Write-Host "Task complete! Output in $outputDir"
        break
    }
    
    $counter++
}
```

---

## Error Handling

### Pattern: Retry with Backoff

**Goal:** Handle transient failures gracefully.

```powershell
function Invoke-SoloActionWithRetry {
    param(
        [scriptblock]$Action,
        [int]$MaxRetries = 3,
        [int]$BaseDelayMs = 1000
    )
    
    for ($i = 0; $i -lt $MaxRetries; $i++) {
        try {
            & $Action
            return $true
        }
        catch {
            $delay = $BaseDelayMs * [Math]::Pow(2, $i)
            Write-Warning "Attempt $($i+1) failed: $_"
            Write-Host "Waiting ${delay}ms before retry..."
            Start-Sleep -Milliseconds $delay
        }
    }
    
    throw "Failed after $MaxRetries attempts"
}

# Usage
Invoke-SoloActionWithRetry -Action {
    agent-browser click @SEND_REF
}
```

---

### Pattern: Session Health Check

**Goal:** Verify CDP connection is still alive.

```powershell
function Test-SoloConnection {
    try {
        $result = agent-browser get url 2>&1
        if ($result -match "error|failed") {
            return $false
        }
        return $true
    }
    catch {
        return $false
    }
}

# Auto-reconnect pattern
if (-not (Test-SoloConnection)) {
    Write-Host "Connection lost, reconnecting..."
    $wsUrl = (Invoke-RestMethod "http://127.0.0.1:9222/json/version").webSocketDebuggerUrl
    agent-browser connect $wsUrl
}
```

---

## Element Finding Strategies

### Strategy: Find by Text Content

**Goal:** Locate elements by their visible text when refs change.

```powershell
# Get snapshot as JSON for parsing
$snapshot = agent-browser snapshot --json | ConvertFrom-Json

# Find element by text pattern
$targetRef = $snapshot | 
    Where-Object { $_.name -match "新建任务" } |
    Select-Object -First 1 -ExpandProperty ref

if ($targetRef) {
    agent-browser click "@$targetRef"
}
```

---

### Strategy: Find by Role and Position

**Goal:** Locate elements by their type and relative position.

```bash
# Get all buttons
agent-browser snapshot -i | grep "button"

# Find textbox in center panel (usually only one)
agent-browser snapshot -i | grep "textbox"

# Find send button (near input, often last button in that area)
agent-browser snapshot -i | grep -A2 -B2 "textbox"
```

---

### Strategy: Hierarchical Navigation

**Goal:** Navigate UI by parent-child relationships.

```
# Example snapshot structure:
- group [ref=e1]
  - button "新建任务" [ref=e2]
  - button "技能" [ref=e3]
  - button "自动化" [ref=e4]
- group [ref=e5]
  - textbox [ref=e6]
  - button [ref=e7]  # Send button
```

```powershell
# Find send button (sibling of textbox)
$snapshot = agent-browser snapshot --json | ConvertFrom-Json

$textbox = $snapshot | Where-Object { $_.role -eq "textbox" }
$parent = $snapshot | Where-Object { $_.ref -eq $textbox.parent }
$sendButton = $parent.children | Where-Object { $_.role -eq "button" } | Select-Object -First 1
```

---

## Batch Operations

### Pattern: Process File List

**Goal:** Send multiple files for analysis.

```powershell
$files = Get-ChildItem "src/*.cs" | Select-Object -First 5

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    $prompt = @"
分析这个文件的代码质量:

文件名: $($file.Name)

```csharp
$content
```

请指出:
1. 潜在的性能问题
2. 代码风格问题
3. 安全漏洞
"@
    
    # Send and wait
    agent-browser click @e4
    agent-browser wait 1000
    agent-browser fill @INPUT_REF $prompt
    agent-browser click @SEND_REF
    
    Wait-SoloTaskComplete
    
    # Save result with filename
    agent-browser screenshot "analysis-$($file.BaseName).png"
}
```

---

### Pattern: Workspace Audit

**Goal:** Check all workspaces for activity.

```powershell
# Get list of workspaces from sidebar
$snapshot = agent-browser snapshot -i
$workspaces = $snapshot | Select-String "button.*trae-solo|button.*jerry_|button.*默认"

$report = @()

foreach ($ws in $workspaces) {
    # Extract ref and name
    if ($ws -match "\[ref=(e\d+)\].*button \"(.+?)\"") {
        $ref = $matches[1]
        $name = $matches[2]
        
        # Click workspace
        agent-browser click "@$ref"
        agent-browser wait 2000
        
        # Check for activity
        $wsSnapshot = agent-browser snapshot -i
        $hasActivity = $wsSnapshot -match "任务耗时|正在执行"
        
        $report += [PSCustomObject]@{
            Workspace = $name
            HasActivity = $hasActivity
            Screenshot = "workspace-$name.png"
        }
        
        agent-browser screenshot "workspace-$name.png"
    }
}

$report | Format-Table -AutoSize
```

---

## State Detection

### Task State Indicators

| State | Text Indicators | Visual Indicators |
|-------|-----------------|-------------------|
| **Idle/Ready** | Input visible, no loading | Send button active |
| **Running** | `正在执行命令…`, `正在思考` | Loading spinner |
| **Completed** | `任务耗时`, `复制全部` | Result displayed |
| **Failed** | `重试` | Error message |
| **Waiting** | (no specific text) | Input disabled |

### Console Error Detection

```powershell
# Check for JS errors
$errors = agent-browser errors
if ($errors) {
    Write-Warning "Console errors detected:"
    $errors | ForEach-Object { Write-Host "  - $_" }
}
```

---

## Tips & Best Practices

1. **Always snapshot before clicking** - Refs change between sessions
2. **Use `--annotate` for debugging** - Shows element numbers on screenshots
3. **Add delays between rapid actions** - Let UI settle with `wait 1000`
4. **Save snapshots periodically** - For debugging and audit trails
5. **Check console for errors** - Many issues only appear in console
6. **Use session names for multiple tasks** - `agent-browser --session task1`
7. **Type slowly for video recording** - Use `type` instead of `fill` during recording

---

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Using wrong ref | Always snapshot first |
| Clicking too fast | Add `wait 1000` between actions |
| Not waiting for completion | Poll for `任务耗时` or `复制全部` |
| Ignoring failures | Check for `重试` button |
| Session timeout | Implement health check and reconnect |
| Wrong workspace | Verify workspace before sending task |
