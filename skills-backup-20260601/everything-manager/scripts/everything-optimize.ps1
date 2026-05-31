# Everything Memory Optimizer
# Adds common exclude patterns to reduce memory usage

param(
    [string]$EverythingPath = "D:\apps\Everything",
    [switch]$Restart
)

$configFile = Join-Path $EverythingPath "Everything.ini"

if (-not (Test-Path $configFile)) {
    Write-Error "Config file not found: $configFile"
    Write-Host "Please specify the correct Everything path with -EverythingPath"
    exit 1
}

Write-Host "Optimizing Everything configuration..." -ForegroundColor Cyan
Write-Host "Config file: $configFile"
Write-Host ""

# Common directories to exclude for memory optimization
$excludeFolders = @(
    "C:\\Windows",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "C:\\ProgramData",
    "C:\\$Recycle.Bin",
    "D:\\$RECYCLE.BIN",
    "C:\\Users\\$env:USERNAME\\AppData\\Local\\Temp",
    "C:\\Windows\\Installer",
    "C:\\Windows\\WinSxS",
    "C:\\Windows\\System32\\DriverStore"
)

# Read current config
$content = Get-Content $configFile -Raw

# Check current exclude_folders setting
if ($content -match 'exclude_folders=(.+)?\r?\n') {
    $currentExcludes = $matches[1]
    Write-Host "Current excluded folders: $currentExcludes" -ForegroundColor Yellow
    Write-Host ""
}

# Build new exclude string
$newExcludes = $excludeFolders -join ";"

# Update or add exclude_folders line
if ($content -match 'exclude_folders=.*\r?\n') {
    $content = $content -replace 'exclude_folders=.*\r?\n', "exclude_folders=$newExcludes`r`n"
    Write-Host "✅ Updated exclude_folders in config" -ForegroundColor Green
} else {
    # Add after exclude_list_enabled line
    $content = $content -replace '(exclude_list_enabled=\d+\r?\n)', "`$1exclude_folders=$newExcludes`r`n"
    Write-Host "✅ Added exclude_folders to config" -ForegroundColor Green
}

# Save config
Set-Content -Path $configFile -Value $content -NoNewline

Write-Host ""
Write-Host "Excluded folders:" -ForegroundColor Cyan
foreach ($folder in $excludeFolders) {
    Write-Host "  - $folder"
}

Write-Host ""
Write-Host "Memory optimization complete!" -ForegroundColor Green

if ($Restart) {
    Write-Host ""
    Write-Host "Restarting Everything with reindex..." -ForegroundColor Yellow
    
    # Stop Everything
    $proc = Get-Process -Name "Everything" -ErrorAction SilentlyContinue
    if ($proc) {
        Stop-Process -Name "Everything" -Force
        Start-Sleep -Seconds 2
    }
    
    # Start with reindex
    $everythingExe = Join-Path $EverythingPath "Everything.exe"
    Start-Process $everythingExe -ArgumentList "-reindex -startup"
    
    Write-Host "✅ Everything restarted" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "To apply changes, restart Everything with:" -ForegroundColor Yellow
    Write-Host "  Everything.exe -exit"
    Write-Host "  Everything.exe -reindex -startup"
}
