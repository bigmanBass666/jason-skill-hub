<#
.SYNOPSIS
    Robustly start TRAE SOLO CN with CDP support and health checks.

.DESCRIPTION
    This script ensures TRAE SOLO CN starts cleanly by:
    1. Killing any existing processes
    2. Verifying cleanup
    3. Starting fresh instance
    4. Waiting for CDP port
    5. Verifying window loaded correctly
    6. Returning connection info

.PARAMETER InstallPath
    Path to TRAE SOLO CN installation (default: D:\apps\TRAE SOLO CN\)

.PARAMETER DebugPort
    CDP debug port (default: 9222)

.PARAMETER WaitSeconds
    Seconds to wait for app startup (default: 5)

.EXAMPLE
    .\Start-Solo.ps1

.EXAMPLE
    .\Start-Solo.ps1 -InstallPath "C:\Program Files\TRAE SOLO CN\" -DebugPort 9223

.EXAMPLE
    $result = .\Start-Solo.ps1
    if ($result.Success) { agent-browser connect $result.WebSocketUrl }
#>

[CmdletBinding()]
param(
    [string]$InstallPath = "D:\apps\TRAE SOLO CN\",
    [int]$DebugPort = 9222,
    [int]$WaitSeconds = 5
)

$ErrorActionPreference = "Stop"

function Write-Status {
    param([string]$Message, [string]$Status = "INFO")
    $timestamp = Get-Date -Format "HH:mm:ss"
    $prefix = switch ($Status) {
        "SUCCESS" { "[✓]" }
        "ERROR"   { "[✗]" }
        "WARN"    { "[!]" }
        default   { "[→]" }
    }
    Write-Host "$timestamp $prefix $Message"
}

# Step 1: Check for existing processes
Write-Status "Checking for existing TRAE SOLO CN processes..."
$existing = Get-Process "TRAE SOLO CN" -ErrorAction SilentlyContinue

if ($existing) {
    $count = ($existing | Measure-Object).Count
    Write-Status "Found $count existing process(es). Terminating..." "WARN"
    
    # Kill all processes
    taskkill /F /IM "TRAE SOLO CN.exe" 2>&1 | Out-Null
    Start-Sleep -Seconds 3
    
    # Verify cleanup
    $remaining = Get-Process "TRAE SOLO CN" -ErrorAction SilentlyContinue
    if ($remaining) {
        $remainingCount = ($remaining | Measure-Object).Count
        Write-Status "Failed to kill $remainingCount process(es)" "ERROR"
        Write-Status "Please restart your computer and try again" "ERROR"
        return @{ Success = $false; Error = "Process cleanup failed" }
    }
    
    Write-Status "All existing processes terminated" "SUCCESS"
}
else {
    Write-Status "No existing processes found" "SUCCESS"
}

# Step 2: Launch TRAE SOLO CN
Write-Status "Starting TRAE SOLO CN..."
$exePath = Join-Path $InstallPath "TRAE SOLO CN.exe"

if (-not (Test-Path $exePath)) {
    Write-Status "Executable not found: $exePath" "ERROR"
    return @{ Success = $false; Error = "Executable not found" }
}

Start-Process $exePath -ArgumentList "--remote-debugging-port=$DebugPort"
Write-Status "Waiting $WaitSeconds seconds for startup..."
Start-Sleep -Seconds $WaitSeconds

# Step 3: Verify process started
Write-Status "Verifying process started..."
$process = Get-Process "TRAE SOLO CN" -ErrorAction SilentlyContinue | Select-Object -First 1

if (-not $process) {
    Write-Status "Process did not start" "ERROR"
    return @{ Success = $false; Error = "Process failed to start" }
}

Write-Status "Process started (PID: $($process.Id))" "SUCCESS"

# Step 4: Wait for CDP port
Write-Status "Waiting for CDP port $DebugPort..."
$portReady = $false
$portAttempts = 0
$maxPortAttempts = 10

while (-not $portReady -and $portAttempts -lt $maxPortAttempts) {
    Start-Sleep -Seconds 1
    $portCheck = netstat -ano | Select-String ":$DebugPort"
    if ($portCheck) {
        $portReady = $true
    }
    $portAttempts++
}

if (-not $portReady) {
    Write-Status "CDP port $DebugPort not ready after $maxPortAttempts attempts" "ERROR"
    return @{ Success = $false; Error = "CDP port not ready" }
}

Write-Status "CDP port $DebugPort is listening" "SUCCESS"

# Step 5: Get WebSocket URL
Write-Status "Getting WebSocket URL..."
try {
    $wsUrl = (Invoke-RestMethod "http://127.0.0.1:$DebugPort/json/version" -TimeoutSec 5).webSocketDebuggerUrl
    Write-Status "WebSocket URL: $wsUrl" "SUCCESS"
}
catch {
    Write-Status "Failed to get WebSocket URL: $_" "ERROR"
    return @{ Success = $false; Error = "Failed to get WebSocket URL" }
}

# Step 6: Connect and verify window loaded
Write-Status "Connecting to verify window loaded..."
try {
    agent-browser connect $wsUrl 2>&1 | Out-Null
    agent-browser wait 2000
    
    $snapshot = agent-browser snapshot -i 2>&1
    
    # Check for critical UI elements
    $hasNewTask = $snapshot -match "新建任务"
    $hasSkills = $snapshot -match "技能"
    $hasAutomation = $snapshot -match "自动化"
    
    if ($hasNewTask -and $hasSkills -and $hasAutomation) {
        Write-Status "Window loaded successfully with all UI elements" "SUCCESS"
    }
    else {
        Write-Status "Window loaded but UI elements may be incomplete" "WARN"
        Write-Status "Missing: $(if(-not $hasNewTask){'新建任务 '})$(if(-not $hasSkills){'技能 '})$(if(-not $hasAutomation){'自动化'})" "WARN"
    }
}
catch {
    Write-Status "Failed to connect or verify: $_" "WARN"
    # Don't fail here - connection might work on retry
}

# Return success
Write-Status "TRAE SOLO CN is ready!" "SUCCESS"

return @{
    Success = $true
    ProcessId = $process.Id
    WebSocketUrl = $wsUrl
    DebugPort = $DebugPort
    InstallPath = $InstallPath
}
