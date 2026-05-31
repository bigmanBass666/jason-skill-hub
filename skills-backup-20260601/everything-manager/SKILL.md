---
name: everything-manager
description: |
  Manage Everything Search on Windows - start, stop, restart, configure, and optimize Everything service and settings.
  Use this skill when the user wants to:
  - Start or stop Everything
  - Check Everything status
  - Optimize Everything memory usage
  - Configure Everything settings
  - Reindex Everything database
  - Troubleshoot Everything issues
  - View Everything command line options

  This skill provides convenient commands to manage Everything without manually editing config files or remembering command line parameters.
---

# Everything Manager Skill

## Overview

This skill helps you manage Everything Search (voidtools) on Windows. Everything is a fast file search utility that indexes your files for instant search results.

## Common Tasks

### Check Everything Status

Check if Everything is running and view its memory usage:

```powershell
Get-Process -Name "Everything*" | Select-Object Name, Id, WorkingSet, Path
```

### Start Everything

**Option 1: Start with GUI (normal)**
```powershell
Everything.exe
```

**Option 2: Start minimized**
```powershell
Everything.exe -minimized
```

**Option 3: Start in background (no window)**
```powershell
Everything.exe -startup
```

**Option 4: Start and reindex**
```powershell
Everything.exe -reindex -startup
```

### Stop Everything

**Close gracefully:**
```powershell
Everything.exe -exit
```

**Force stop:**
```powershell
Stop-Process -Name "Everything" -Force
```

### Restart Everything

```powershell
Everything.exe -exit
Start-Sleep -Seconds 2
Everything.exe -startup
```

### Reindex Database

Force Everything to rebuild its index:

```powershell
Everything.exe -reindex
```

Or restart with reindex:
```powershell
Everything.exe -exit
Everything.exe -reindex -startup
```

## Configuration Management

### View Configuration File

Everything's config is at:
```
<Everything_Directory>\Everything.ini
```

Example: `D:\apps\Everything\Everything.ini`

### Optimize Memory Usage

Add exclude folders to reduce memory usage. Edit `Everything.ini`:

```ini
exclude_folders=C:\\Windows;C:\\Program Files;C:\\Program Files (x86);C:\\ProgramData
```

Then restart with reindex:
```powershell
Everything.exe -exit
Everything.exe -reindex -startup
```

### Common Exclude Patterns

High-memory directories to exclude:
- `C:\Windows\` - Windows system files
- `C:\Program Files\` - Installed programs
- `C:\Program Files (x86)\` - 32-bit programs
- `C:\ProgramData\` - Program data
- `C:\$Recycle.Bin\` - Recycle bin
- `D:\$RECYCLE.BIN\` - D drive recycle bin
- `C:\Users\<User>\AppData\Local\Temp\` - Temp files

## Service Management

### Install Everything as Service

```powershell
Everything.exe -install-service
```

### Remove Service

```powershell
Everything.exe -uninstall-service
```

### Start Service

```powershell
Everything.exe -start-service
```

### Stop Service

```powershell
Everything.exe -stop-service
```

### Enable Auto-Start

```powershell
Everything.exe -install-run-on-system-startup
```

### Disable Auto-Start

```powershell
Everything.exe -uninstall-run-on-system-startup
```

## Command Line Reference

### Installation Commands

| Command | Description |
|---------|-------------|
| `-install <location>` | Install Everything to path |
| `-install-service` | Install as Windows service |
| `-uninstall-service` | Remove service |
| `-install-run-on-system-startup` | Add to startup |
| `-uninstall-run-on-system-startup` | Remove from startup |

### Runtime Commands

| Command | Description |
|---------|-------------|
| `-startup` | Run in background (no window) |
| `-minimized` | Start minimized |
| `-exit` | Quit Everything |
| `-reindex` | Rebuild database |
| `-update` | Update database |

### Search Commands

| Command | Description |
|---------|-------------|
| `-s <text>` | Search for text |
| `-search <text>` | Search for text |
| `-filter <name>` | Use saved filter |
| `-bookmark <name>` | Open bookmark |

### Window Commands

| Command | Description |
|---------|-------------|
| `-newwindow` | New search window |
| `-close` | Close window |
| `-toggle-window` | Show/hide window |
| `-ontop` | Always on top |
| `-fullscreen` | Fullscreen mode |

### Configuration Commands

| Command | Description |
|---------|-------------|
| `-config <filename>` | Use specific config file |
| `-db <filename>` | Use specific database |
| `-app-data` | Store data in AppData |
| `-noapp-data` | Store data in program folder |

## Troubleshooting

### Everything Not Responding

1. Force stop: `Stop-Process -Name "Everything" -Force`
2. Restart: `Everything.exe -startup`

### High Memory Usage

1. Add exclude folders to `Everything.ini`
2. Restart with reindex: `Everything.exe -reindex -startup`
3. Check memory: `Get-Process -Name "Everything*"`

### Service Issues

Check service status:
```powershell
Get-Service -Name "Everything" | Select-Object Status, StartType
```

Restart service:
```powershell
Everything.exe -stop-service
Everything.exe -start-service
```

### MCP Connection Failed

If MCP reports "Everything service not running":
1. Check if Everything is running: `Get-Process -Name "Everything*"`
2. If not, start it: `Everything.exe -startup`
3. If running but MCP fails, restart: `Everything.exe -exit; Everything.exe -startup`

## Best Practices

1. **Use `-startup`** for background operation without GUI
2. **Exclude system directories** to reduce memory usage
3. **Reindex after config changes** to apply exclusions
4. **Install as service** for automatic startup
5. **Monitor memory** periodically with `Get-Process`

## Finding Everything Path

If you don't know where Everything is installed:

```powershell
# Search common locations
$paths = @(
    "C:\Program Files\Everything\Everything.exe",
    "C:\Program Files (x86)\Everything\Everything.exe",
    "D:\apps\Everything\Everything.exe",
    "D:\tools\Everything\Everything.exe"
)

foreach ($path in $paths) {
    if (Test-Path $path) {
        Write-Host "Found: $path"
    }
}
```
