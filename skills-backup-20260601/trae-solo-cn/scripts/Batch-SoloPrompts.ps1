<#
.SYNOPSIS
    Batch process multiple prompts through TRAE SOLO CN.

.DESCRIPTION
    Sends multiple prompts to TRAE SOLO CN sequentially and captures all results.
    Useful for running a suite of tasks or comparing responses.

.PARAMETER Prompts
    Array of prompt strings to process.

.PARAMETER PromptsFile
    Path to a text file with one prompt per line.

.PARAMETER DelaySeconds
    Delay between tasks (default: 2).

.PARAMETER TimeoutSeconds
    Maximum time per task (default: 120).

.PARAMETER ContinueOnError
    Continue processing if one task fails.

.PARAMETER OutputDir
    Directory for results (default: ./solo-batch).

.EXAMPLE
    $prompts = @("优化SQL", "解释正则", "重构代码")
    .\Batch-SoloPrompts.ps1 -Prompts $prompts

.EXAMPLE
    .\Batch-SoloPrompts.ps1 -PromptsFile ./prompts.txt -TimeoutSeconds 180

.EXAMPLE
    Get-Content tasks.txt | .\Batch-SoloPrompts.ps1 -ContinueOnError
#>

[CmdletBinding()]
param(
    [Parameter(ValueFromPipeline = $true, ParameterSetName = "Pipeline")]
    [string[]]$Prompts,

    [Parameter(ParameterSetName = "File")]
    [string]$PromptsFile,

    [Parameter()]
    [int]$DelaySeconds = 2,

    [Parameter()]
    [int]$TimeoutSeconds = 120,

    [Parameter()]
    [switch]$ContinueOnError,

    [Parameter()]
    [string]$OutputDir = "./solo-batch"
)

begin {
    $allPrompts = @()
    $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $batchDir = Join-Path $OutputDir $timestamp
    New-Item -ItemType Directory -Path $batchDir -Force | Out-Null
    
    # Results collection
    $results = @()
    $taskNumber = 0
    
    function Write-Log {
        param([string]$Message, [string]$Level = "INFO")
        $logEntry = "[$(Get-Date -Format 'HH:mm:ss')] [$Level] $Message"
        Write-Host $logEntry
        Add-Content -Path "$batchDir/batch.log" -Value $logEntry
    }
    
    # Import the single prompt function
    $scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
    $sendSoloScript = Join-Path $scriptPath "Send-SoloPrompt.ps1"
}

process {
    if ($Prompts) {
        $allPrompts += $Prompts
    }
}

end {
    # Load from file if specified
    if ($PromptsFile) {
        $allPrompts = Get-Content $PromptsFile | Where-Object { $_.Trim() -ne "" }
    }
    
    $total = $allPrompts.Count
    Write-Log "Starting batch processing of $total prompts"
    Write-Log "Output directory: $batchDir"
    
    $startTime = Get-Date
    
    foreach ($prompt in $allPrompts) {
        $taskNumber++
        $taskDir = Join-Path $batchDir "task-$($taskNumber.ToString("D3"))"
        New-Item -ItemType Directory -Path $taskDir -Force | Out-Null
        
        Write-Log "--- Task $taskNumber/$total ---"
        Write-Log "Prompt: $prompt"
        
        try {
            # Execute single prompt
            $result = & $sendSoloScript `
                -Prompt $prompt `
                -TimeoutSeconds $TimeoutSeconds `
                -OutputDir $taskDir `
                -ErrorAction Stop
            
            $taskResult = [PSCustomObject]@{
                TaskNumber = $taskNumber
                Prompt = $prompt
                Success = $result.Success
                State = $result.State
                Duration = $result.Duration
                OutputDir = $result.OutputDir
                Screenshot = $result.Screenshot
            }
            
            if ($result.Success) {
                Write-Log "Task $taskNumber completed in $($result.Duration)s" "SUCCESS"
            }
            else {
                Write-Log "Task $taskNumber failed: $($result.State)" "WARN"
            }
        }
        catch {
            Write-Log "Task $taskNumber error: $_" "ERROR"
            
            $taskResult = [PSCustomObject]@{
                TaskNumber = $taskNumber
                Prompt = $prompt
                Success = $false
                State = "Error"
                Duration = 0
                OutputDir = $taskDir
                Screenshot = $null
            }
            
            if (-not $ContinueOnError) {
                Write-Log "Stopping batch due to error (use -ContinueOnError to override)" "ERROR"
                break
            }
        }
        
        $results += $taskResult
        
        # Save progress after each task
        $results | Export-Csv -Path "$batchDir/results.csv" -NoTypeInformation -Force
        
        # Delay between tasks
        if ($taskNumber -lt $total) {
            Write-Log "Waiting $DelaySeconds seconds before next task..."
            Start-Sleep -Seconds $DelaySeconds
        }
    }
    
    # Generate summary
    $endTime = Get-Date
    $totalDuration = [math]::Round(($endTime - $startTime).TotalSeconds)
    $successCount = ($results | Where-Object { $_.Success }).Count
    $failCount = $results.Count - $successCount
    
    Write-Log "=== Batch Complete ==="
    Write-Log "Total tasks: $total"
    Write-Log "Successful: $successCount"
    Write-Log "Failed: $failCount"
    Write-Log "Total duration: ${totalDuration}s"
    Write-Log "Average per task: $([math]::Round($totalDuration / $total, 1))s"
    
    # Generate report
    $report = @"
# Batch Processing Report

**Date:** $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
**Total Tasks:** $total
**Successful:** $successCount
**Failed:** $failCount
**Total Duration:** ${totalDuration}s

## Summary

| Metric | Value |
|--------|-------|
| Success Rate | $([math]::Round($successCount / $total * 100, 1))% |
| Avg Duration | $([math]::Round(($results | Measure-Object -Property Duration -Average).Average, 1))s |
| Min Duration | $([math]::Round(($results | Measure-Object -Property Duration -Minimum).Minimum, 1))s |
| Max Duration | $([math]::Round(($results | Measure-Object -Property Duration -Maximum).Maximum, 1))s |

## Task Details

| # | Status | Duration | Prompt |
|---|--------|----------|--------|
"@
    
    foreach ($r in $results) {
        $status = if ($r.Success) { "✅" } else { "❌" }
        $report += "| $($r.TaskNumber) | $status | $($r.Duration)s | $($r.Prompt.Substring(0, [Math]::Min(50, $r.Prompt.Length)))... |`n"
    }
    
    $report += @"

## Failed Tasks

"@
    
    $failed = $results | Where-Object { -not $_.Success }
    if ($failed) {
        foreach ($f in $failed) {
            $report += "- **Task $($f.TaskNumber)**: $($f.Prompt)`n"
        }
    }
    else {
        $report += "All tasks completed successfully!`n"
    }
    
    $report | Out-File -FilePath "$batchDir/REPORT.md" -Encoding UTF8
    Write-Log "Report saved to: $batchDir/REPORT.md"
    
    # Return results
    return [PSCustomObject]@{
        Success = ($failCount -eq 0)
        TotalTasks = $total
        Successful = $successCount
        Failed = $failCount
        Duration = $totalDuration
        OutputDir = $batchDir
        Results = $results
    }
}
