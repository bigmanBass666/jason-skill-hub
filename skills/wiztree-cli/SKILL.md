---
name: wiztree-cli
description: >
  WizTree 磁盘空间分析工具的完整 CLI 参考手册。覆盖命令行导出、自动化扫描、
  过滤排序、Treemap 图片导出、MFT dump、静默安装等所有参数。
  当用户提到 WizTree、磁盘扫描导出、磁盘空间分析、CSV 导出、命令行扫描、
  或想自动化磁盘分析时触发此 skill。即使用户只是说"帮我扫一下磁盘"或
  "导出磁盘数据"，也应该使用此 skill。
---

# WizTree CLI 完整参考

WizTree 是最快的磁盘空间分析工具（直接读 NTFS MFT），支持命令行导出 CSV 和图片。
安装路径通常在 `D:\apps\WizTree\WizTree64.exe`。

> 64 位系统**必须**用 `Wiztree64.exe`，用 `wiztree.exe` 会立即返回（不等待完成）。
> 扫描 NTFS 需要**管理员权限**。

---

## 基本语法

```
WizTree64.exe "<drive/folder>" /export="<filename>" [options]
```

- `"C:"` — 扫描整个 C 盘
- `"D:\Projects"` — 只扫描指定目录
- 批处理中 `%d` → `%%d`，`%t` → `%%t`

---

## 核心导出参数

| 参数 | 说明 | 默认 |
|------|------|------|
| `/export="file.csv"` | 导出 CSV，支持 `%d`(YYYYMMDD) `%t`(HHMMSS) | — |
| `/admin=0\|1` | 管理员模式（MFT 扫描需要 1） | 1 |
| `/sortby=0\|1\|2\|3` | 排序：0=名称 1=大小↓ 2=分配↓ 3=修改时间↓ | 0 |
| `/filter="*.mp3\|*.wav"` | 只导出匹配的文件，支持 `|` 分隔多模式 | — |
| `/filterexclude="*.tmp"` | 排除匹配的文件 | — |
| `/filterfullpath=0\|1` | 0=按文件名过滤 1=按完整路径过滤（≥4.13） | 1 |
| `/exportfolders=0\|1` | 是否导出文件夹行 | 1 |
| `/exportfiles=0\|1` | 是否导出文件行 | 1 |

---

## 高级导出参数

| 参数 | 说明 |
|------|------|
| `/exportdrivecapacity=1` | 导出磁盘容量/剩余/已用（首行含 DRIVECAPACITY, FREESPACE, USEDSPACE 列） |
| `/exportpercentofparent=1` | 导出"占父目录百分比"列 |
| `/exportmaxdepth=N` | 最大导出深度（0=无限）— 减小 CSV 体积很有用 |
| `/exportalldates=1` | 额外导出"最后访问时间"和"创建时间" |
| `/exportallsizes=1` | 导出文件夹自身的大小（不含子目录） |
| `/exportsplitfilename=1` | 拆分：根目录、文件夹、文件名、扩展名各一列 |
| `/exportmftrecno=1` | 导出 MFT 记录号（仅 admin 全盘 NTFS 扫描有效） |
| `/exportUTCTime=1` | 时间用 UTC 而非本地时区 |

---

## 排序选项详解

| 值 | 排序方式 |
|----|----------|
| `0` | 文件名字母序 |
| `1` | 文件大小降序 → 文件名 |
| `2` | 分配大小降序 → 文件名 |
| `3` | 修改时间降序（≥4.13） |

---

## 文件类型统计导出

单独导出按扩展名汇总的统计：

```
WizTree64.exe "C:" /exportfiletypes="types.csv" [/admin=0|1] [/sortbyfiletypes=0|1|2]
```

- `/sortbyfiletypes=0` 按扩展名排序
- `/sortbyfiletypes=1` 按总大小降序（默认）
- `/sortbyfiletypes=2` 按分配大小降序

可与 `/export` 同时使用，一次扫描生成两个 CSV。

---

## Treemap 图片导出

| 参数 | 说明 | 默认 |
|------|------|------|
| `/treemapimagefile="out.png"` | PNG 输出路径，支持 `%d`/`%t` | 必填 |
| `/treemapimagewidth=N` | 像素宽度 | 1920 |
| `/treemapimageheight=N` | 像素高度 | 1080 |
| `/treemapimagegray=0\|1` | 灰度模式 | 0 |
| `/treemapimagefreespace=0\|1` | 显示剩余空间 | 1 |
| `/treemapimageshowallocated=0\|1` | 显示分配空间而非文件大小 | 0 |

---

## MFT 原始导出

```
WizTree64.exe "C:" /dumpmftfile="mft_dump.csv"
```

直接导出 MFT 记录，支持 `%d`/`%t`。速度快于完整扫描。

---

## 安装器参数（静默安装 ≥4.05）

```
wiztree_setup.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP- /MERGETASKS=!desktopicon /runasadmin=false /checkforupdates=false /supportercode=xxxx-xxxx-xxxx
```

| 参数 | 说明 |
|------|------|
| `/supportercode=xxx` | 捐赠码 |
| `/runasadmin=TRUE\|FALSE` | 始终以管理员运行 |
| `/checkforupdates=TRUE\|FALSE` | 自动检查更新 |
| `/!runasadmin=TRUE` | 前缀 `!` = 只读设置（用户不可改） |

---

## 配置文件

- **安装版**：`%appdata%\WizTree3\WizTree3.ini`
- **便携版**：与 `wiztree.exe` 同目录
- **注册表覆盖**（≥4.27）：`HKLM\Software\Antibody Software\WizTree\ConfigOverride\frmWizTreeMain`

---

## 常用场景示例

### 扫描全盘并导出（最常用）
```bat
start /wait WizTree64.exe "C:" /export="C:\temp\cdrive_%d_%t.csv" /exportdrivecapacity=1 /sortby=1
```

### 只导出前 6 层目录（减小体积）
```
WizTree64.exe "D:" /export="D:\scan.csv" /exportmaxdepth=6 /exportfolders=1 /exportfiles=0
```

### 查找大文件（只导出 >100MB 文件）
```
WizTree64.exe "C:" /export="big_files.csv" /sortby=1 /exportfolders=0
```
> WizTree CLI 本身不支持按大小过滤，需后处理 CSV。

### 导出特定类型文件
```
WizTree64.exe "D:\Projects" /export="code_files.csv" /filter="*.py|*.js|*.ts" /exportsplitfilename=1
```

### 同时导出 CSV + Treemap 图片
```
WizTree64.exe "C:" /export="C:\temp\c_%d_%t.csv" /treemapimagefile="C:\temp\c_%d_%t.png" /treemapimagewidth=1024 /treemapimageheight=768
```

### 导出文件类型统计
```
WizTree64.exe "C:" /exportfiletypes="C:\temp\filetypes_%d_%t.csv" /sortbyfiletypes=1
```

---

## 批处理 / 自动化注意事项

1. **用 `start /wait`** 等待扫描完成，否则立即返回
2. **64 位必须用 `WizTree64.exe`**，`wiztree.exe` 会自动启动 64 位版但不等待
3. **管理员权限**：NTFS MFT 扫描必须管理员，用 `powershell Start-Process -Verb RunAs` 提权
4. **路径含空格**：用双引号包裹
5. **过滤含引号的路径**（≥4.11）：用单引号代表字面双引号 → `/filter="'C:\Program Files\'"`
6. **%d %t 占位符**：批处理 `.bat` 中用 `%%d` `%%t`；PowerShell / Python 中用 `%d` `%t`
7. **过滤含反斜杠的路径**：`/filter` 的搜索词如果包含 `\`，无论 `/filterfullpath` 设置如何，都会自动按完整路径匹配

---

## CSV 输出格式

标准列（`/sortby=1` 时）：

```
文件名称,大小,分配,修改时间,属性,文件,文件夹,FOLDERSIZE,FOLDERALLOCATED,PERCENTOFPARENT[,DRIVECAPACITY,FREESPACE,USEDSPACE,RESERVEDSPACE]
```

- 第 1 行：版本注释（`生成由 WizTree 4.31 ...`）
- 第 2 行：列头
- 第 3 行起：数据行
- 根行：`"C:\",总大小,总分配,...`
- 文件夹行：以 `\` 结尾
- 大小单位：**字节**

使用 `/exportdrivecapacity=1` 时额外输出 DRIVECAPACITY, FREESPACE, USEDSPACE, RESERVEDSPACE 四列。
