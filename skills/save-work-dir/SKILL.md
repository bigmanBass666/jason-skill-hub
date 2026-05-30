---
name: save-work-dir
description: 记录当前工作目录到桌面的历史文件。当用户说"记录工作目录"、"保存工作目录"、"记录当前目录"、"save work dir"、"记住这个目录"时触发此 skill。
---

# 保存工作目录

将当前工作目录路径追加到桌面的 `previous_work_dir.txt` 文件，方便后续快速访问历史项目。

## 执行步骤

### 1. 获取当前工作目录

获取 Claude Code 当前的工作目录绝对路径。

### 2. 更新记录文件

使用 PowerShell 脚本完成以下操作：

```powershell
$desktopPath = [Environment]::GetFolderPath("Desktop")
$filePath = Join-Path $desktopPath "previous_work_dir.txt"
$currentDir = "获取到的当前工作目录路径"

# 读取已有内容（如果文件存在）
$existingLines = @()
if (Test-Path $filePath) {
    $existingLines = Get-Content $filePath | Where-Object { $_ -ne "" }
}

# 移除已存在的相同路径（实现去重）
$existingLines = $existingLines | Where-Object { $_ -ne $currentDir }

# 追加新路径到末尾
$existingLines += $currentDir

# 写入文件
$existingLines | Set-Content $filePath -Encoding UTF8

# 输出文件内容供 Claude 显示
Write-Output "FILE_CONTENT_START"
Get-Content $filePath
Write-Output "FILE_CONTENT_END"
```

### 3. 显示结果

从脚本输出中提取 `FILE_CONTENT_START` 和 `FILE_CONTENT_END` 之间的内容，格式化显示给用户：

```
已记录: D:\Projects\my-app

📋 历史记录:
1. D:\Projects\other-app
2. D:\Projects\my-app
```

编号从 1 开始，最新的在最后。

## 注意事项

- 使用 UTF-8 编码确保中文路径正常显示
- 每行只记录一个路径
- 相同路径会被移到文件末尾（去重逻辑）
