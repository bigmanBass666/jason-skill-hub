# Everything Status Checker
# Checks if Everything is running and displays memory usage

param(
    [switch]$Detailed
)

$processes = Get-Process -Name "Everything*" -ErrorAction SilentlyContinue

if ($processes) {
    Write-Host "✅ Everything is running" -ForegroundColor Green
    Write-Host ""
    
    $totalMemory = 0
    foreach ($proc in $processes) {
        $memoryMB = [math]::Round($proc.WorkingSet / 1MB, 2)
        $totalMemory += $memoryMB
        
        Write-Host "Process: $($proc.ProcessName)" -ForegroundColor Cyan
        Write-Host "  PID: $($proc.Id)"
        Write-Host "  Memory: $memoryMB MB"
        Write-Host "  Path: $($proc.Path)"
        Write-Host ""
    }
    
    Write-Host "Total Memory Usage: $totalMemory MB" -ForegroundColor Yellow
    
    if ($Detailed) {
        # Check service status
        $service = Get-Service -Name "Everything" -ErrorAction SilentlyContinue
        if ($service) {
            Write-Host ""
            Write-Host "Service Status: $($service.Status)" -ForegroundColor Cyan
            Write-Host "Start Type: $($service.StartType)"
        }
        
        # Check config file
        $configPaths = @(
            "D:\apps\Everything\Everything.ini",
            "C:\Program Files\Everything\Everything.ini",
            "C:\Program Files (x86)\Everything\Everything.ini"
        )
        
        foreach ($configPath in $configPaths) {
            if (Test-Path $configPath) {
                Write-Host ""
                Write-Host "Config File: $configPath" -ForegroundColor Cyan
                
                # Read exclude folders
                $content = Get-Content $configPath -Raw
                if ($content -match 'exclude_folders=(.+)?\r?\n') {
                    $excludes = $matches[1]
                    if ($excludes) {
                        Write-Host "Excluded Folders: $excludes"
                    } else {
                        Write-Host "Excluded Folders: (none)"
                    }
                }
                break
            }
        }
    }
} else {
    Write-Host "❌ Everything is not running" -ForegroundColor Red
    Write-Host ""
    Write-Host "To start Everything, run:" -ForegroundColor Yellow
    Write-Host "  Everything.exe -startup    # Background mode"
    Write-Host "  Everything.exe             # With GUI"
}
