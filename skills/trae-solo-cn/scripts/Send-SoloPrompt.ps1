<#
.SYNOPSIS
    Send a prompt to TRAE SOLO CN and wait for completion.

.DESCRIPTION
    Automates sending a single prompt to TRAE SOLO CN AI and captures the result.
    Handles connection, task monitoring, and result extraction.

.PARAMETER Prompt
    The prompt text to send to the AI.

.PARAMETER Model
    The AI model to use (default: current selection).

.PARAMETER Workspace
    The workspace to switch to before sending (optional).

.PARAMETER TimeoutSeconds
    Maximum time to wait for task completion (default: 120).

.PARAMETER OutputDir
    Directory to save screenshots and logs (default: ./solo-output).

.EXAMPLE
    .\Send-SoloPrompt.ps1 -Prompt "解释什么是依赖注入"

.EXAMPLE
    .\Send-SoloPrompt.ps1 -Prompt "优化这段代码" -Model "Claude" -TimeoutSeconds 180

.EXAMPLE
    $result = .\Send-SoloPrompt.ps1 -Prompt "分析性能" -Workspace "my-project"
    if ($result.Success) { Write-Host "Completed in $($result.Duration)" }
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Prompt,

    [Parameter()]
    [string]$Model,

    [Parameter()]
    [string]$Workspace,

    [Parameter()]
    [int]$TimeoutSeconds = 120,

    [Parameter()]
    [string]$OutputDir = "./solo-output"
)

# Ensure output directory exists
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$sessionDir = Join-Path $OutputDir $timestamp
New-Item -ItemType Directory -Path $sessionDir -Force | Out-Null

# Logging function
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $logEntry = "[$(Get-Date -Format 'HH:mm:ss')] [$Level] $Message"
    Write-Host $logEntry
    Add-Content -Path "$sessionDir/session.log" -Value $logEntry
}

# Connect to TRAE SOLO CN
function Connect-Solo {
    Write-Log "Connecting to TRAE SOLO CN..."
    
    try {
        $wsUrl = (Invoke-RestMethod "http://127.0.0.1:9222/json/version" -TimeoutSec 5).webSocketDebuggerUrl
        agent-browser connect $wsUrl 2>&1 | Out-Null
        agent-browser wait 2000
        Write-Log "Connected successfully"
        return $true
    }
    catch {
        Write-Log "Failed to connect: $_" "ERROR"
        Write-Log "Ensure TRAE SOLO CN is running with --remote-debugging-port=9222" "ERROR"
        return $false
    }
}

# Get current snapshot
function Get-Snapshot {
    return agent-browser snapshot -i 2>&1
}

# Check task state
function Get-TaskState {
    param([string]$Snapshot)
    
    if ($Snapshot -match "正在执行命令|正在思考|Running") {
        return "Running"
    }
    elseif ($Snapshot -match "任务耗时|复制全部") {
        return "Completed"
    }
    elseif ($Snapshot -match "重试") {
        return "Failed"
    }
    else {
        return "Unknown"
    }
}

# Find element ref by pattern
function Find-ElementRef {
    param(
        [string]$Pattern,
        [string]$Role = "button"
    )
    
    $snapshot = Get-Snapshot
    if ($snapshot -match "$role.*$Pattern.*\[ref=(e\d+)\]") {
        return "@$($matches[1])"
    }
    return $null
}

# Main execution
try {
    $startTime = Get-Date
    Write-Log "Starting Solo automation session"
    Write-Log "Prompt: $Prompt"
    
    # Connect
    if (-not (Connect-Solo)) {
        exit 1
    }
    
    # Switch workspace if specified
    if ($Workspace) {
        Write-Log "Switching to workspace: $Workspace"
        $wsRef = Find-ElementRef -Pattern $Workspace
        if ($wsRef) {
            agent-browser click $wsRef
            agent-browser wait 2000
        }
        else {
            Write-Log "Workspace '$Workspace' not found, continuing with current" "WARN"
        }
    }
    
    # Switch model if specified
    if ($Model) {
        Write-Log "Switching to model: $Model"
        $snapshot = Get-Snapshot
        if ($snapshot -match "button \"(.+?)\".*\[ref=(e\d+)\]" -and $matches[1] -match "GLM|Claude|GPT") {
            agent-browser click "@$($matches[2])"
            agent-browser wait 500
        }
    }
    
    # Navigate to New Task panel
    Write-Log "Opening New Task panel"
    $newTaskRef = Find-ElementRef -Pattern "新建任务"
    if ($newTaskRef) {
        agent-browser click $newTaskRef
    }
    else {
        agent-browser click "@e4"
    }
    agent-browser wait 1000
    
    # Find input and send
    Write-Log "Sending prompt..."
    $snapshot = Get-Snapshot
    
    if ($snapshot -match "textbox.*\[ref=(e\d+)\]") {
        $inputRef = "@$($matches[1])"
        agent-browser fill $inputRef $Prompt
        agent-browser press Enter
    }
    else {
        throw "Could not find input textbox"
    }
    
    # Monitor task progress
    Write-Log "Waiting for task completion (timeout: ${TimeoutSeconds}s)..."
    $taskStart = Get-Date
    $state = "Unknown"
    $pollCount = 0
    
    while ($state -ne "Completed" -and $state -ne "Failed") {
        Start-Sleep -Seconds 5
        $pollCount++
        
        $snapshot = Get-Snapshot
        $state = Get-TaskState -Snapshot $snapshot
        $elapsed = [math]::Round(((Get-Date) - $taskStart).TotalSeconds)
        
        Write-Log "Poll #$pollCount`: State=$state, Elapsed=${elapsed}s"
        
        if ($pollCount % 3 -eq 0) {
            $snapshot | Out-File "$sessionDir/snapshot-$pollCount.txt"
            agent-browser screenshot "$sessionDir/progress-$pollCount.png" 2>&1 | Out-Null
        }
        
        if ($elapsed -gt $TimeoutSeconds) {
            Write-Log "Timeout reached!" "ERROR"
            $state = "Timeout"
            break
        }
    }
    
    # Capture result
    $result = @{
        Success = $false
        State = $state
        Duration = [math]::Round(((Get-Date) - $taskStart).TotalSeconds)
        TotalTime = [math]::Round(((Get-Date) - $startTime).TotalSeconds)
        OutputDir = $sessionDir
    }
    
    if ($state -eq "Completed") {
        Write-Log "Task completed successfully!"
        
        $copyRef = Find-ElementRef -Pattern "复制全部"
        if ($copyRef) {
            agent-browser click $copyRef
            Write-Log "Output copied to clipboard"
        }
        
        agent-browser screenshot "$sessionDir/final-result.png"
        $result.Success = $true
        $result.Screenshot = "$sessionDir/final-result.png"
    }
    else {
        Write-Log "Task ended with state: $state" "WARN"
        agent-browser screenshot "$sessionDir/failed-state.png"
    }
    
    # Save final snapshot
    Get-Snapshot | Out-File "$sessionDir/final-snapshot.txt"
    
    Write-Log "Session complete. Output in: $sessionDir"
    
    return $result
}
catch {
    Write-Log "Error: $_" "ERROR"
    agent-browser screenshot "$sessionDir/error-state.png" 2>&1 | Out-Null
    throw
}
