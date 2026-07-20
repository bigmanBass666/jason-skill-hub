---
name: tailscale-ssh
description: >-
  Windows 双机 Tailscale 整体方案。涵盖 Tailscale 核心功能（SSH、Taildrop 文件传输、SMB 远程磁盘挂载、ACL 访问控制、MagicDNS）在 Windows 上的完整配置与踩坑记录。当用户提到 SSH、Tailscale、远程执行命令、远程 Claude Code、两台电脑之间传文件、跨机操作、远程磁盘挂载、网络驱动器映射、或者需要了解 Tailscale 功能时触发。注意：Windows 上 Tailscale SSH server 不可用，需要使用 OpenSSH Server + 密钥认证替代。
---

# Tailscale on Windows 双机互连方案

## 环境信息

| 项目 | 值 |
|------|-----|
| 电脑 A（本机） | PC-zZ，Tailscale IP: 100.65.183.101，用户名: 86150 |
| 电脑 B（远程） | MS-EKOQRYREIHTY，Tailscale IP: 100.64.141.0，用户名: administrator |
| Tailscale 账号 | wingiscrazy@qq.com（两台同账号） |
| 网络 | 同 Wi-Fi（192.168.x.x） |

## Tailscale 核心功能总览

Tailscale 不仅仅是 VPN，它是一个完整的**安全组网工具套件**，基于 WireGuard 加密：

| 功能 | 用途 | Windows 支持 |
|------|------|-------------|
| **WireGuard 加密隧道** | 设备间所有流量端到端加密 | ✅ |
| **ACL 访问控制** | 定义谁可以访问什么设备/端口 | ✅ 管理后台配置 |
| **MagicDNS** | 自动分配 `设备名.tailnet名.ts.net` 域名 | ✅ |
| **Tailscale SSH** | ACL 控制的 SSH，无需管理密钥 | ❌ 仅服务端不可用 |
| **Taildrop** | 设备间加密文件传输 | ✅ |

> **核心理念：** Tailscale 是加密网络层，具体的服务（SSH、文件共享等）仍需要传统方式配置，但 Tailscale 提供了安全传输通道和集中访问控制。

---

## 一、Taildrop 文件传输

Taildrop 是 Tailscale 内置的加密文件传输功能，端到端加密，不依赖任何第三方服务。

### 发送文件

```powershell
# 查看可发送的目标设备
tailscale file cp --targets

# 发送文件（目标名后面加冒号）
tailscale file cp D:\path\to\file.txt 目标设备名:
```

### 接收文件

在接收端设备上，文件会到达 Taildrop 收件箱。收件箱位于**用户下载目录**：

```powershell
# 查看收件箱
dir "$env:USERPROFILE\Downloads"

# 或者用命令行取出到指定目录
tailscale file get "D:\目标目录"
```

### 实用示例

```powershell
# 本机 → 远程笔记本，发送配置文件
tailscale file cp "D:\Users\86150\.claude\rules\installation.md" ms-ekoqryreihty:

# 远程笔记本上，取出到 .claude 目录
tailscale file get "C:\Users\Administrator\.claude\rules"
```

### 注意事项

- Taildrop 走 Tailscale 加密隧道，不经过第三方服务器
- 文件大小没有硬性限制，但大文件传输速度取决于两设备间的直连质量
- 目标设备必须在线并连接到同一 tailnet
- 接收端需要用 `tailscale file get` 或手动从下载目录取出文件

---

## 二、SMB 远程磁盘挂载（网络驱动器）

通过 Tailscale 的加密隧道，可以将远程电脑的磁盘**映射为本地网络驱动器**，像操作本地文件一样读写远程文件，无需每次都 SSH 或传文件。

### 使用管理共享（推荐）

Windows 内置有**管理共享**（Administrative Shares），自动为每个硬盘分区创建隐藏共享：

| 共享名 | 指向 | 说明 |
|--------|------|------|
| `C$` | `C:\` | C 盘管理共享 |
| `D$` | `D:\` | D 盘管理共享 |
| `ADMIN$` | `C:\Windows` | 系统目录管理共享 |

特点：自动创建、隐藏（名后有 `$`、网上邻居不可见）、仅 Administrators 可访问。**无需手动创建共享，直接映射即可。**

```powershell
# 映射远程 C$ 到本机 Y:
net use Y: \\远程TailscaleIP\C$ /persistent:yes

# 映射远程 D$ 到本机 Z:
net use Z: \\远程TailscaleIP\D$ /persistent:yes
```

### 使用示例

```bash
# 操作远程 D 盘
ls Z:/
cat Z:/somefile.txt

# 操作远程 C 盘（如 .claude 配置）
cat Y:/Users/Administrator/.claude/rules/installation.md
```

### 进阶用法：SMB 作为软件分发通道

SMB 不只是文件读写——它是**安装软件到远程**的最可靠方式，比 SCP 快且稳定，尤其适合大文件传输。

**典型场景：远程电脑因 GFW 无法下载 GitHub releases，从本机分发安装包。**

```powershell
# 1. 本机用 Scoop 安装软件（确保下载成功）
scoop install pwsh

# 2. 通过 SMB 把安装目录复制到远程 D: 盘
# Z: = 远程 D$
cp -r D:\apps\scoop\apps\pwsh\current\. Z:\apps\pwsh\

# 3. SSH 到远程验证并配置
ssh remote-laptop "D:\apps\pwsh\pwsh.exe --version"

# 4. 注册到远程 PATH（需执行一次）
[Environment]::SetEnvironmentVariable('PATH', "D:\apps\pwsh;$env:PATH", 'User')
```

**适用场景对比：**

| 手段 | 适合 | 不适合 |
|------|------|--------|
| **SMB 复制** | 大文件、目录结构、安装包分发 | 远程执行安装程序 |
| **SCP** | 小文件、单文件快速传输 | 大目录、嵌套结构 |
| **Taildrop** | 端到端加密传单文件 | 大目录、目标需在线 |
| **SSH 执行 curl** | 远程直接下载 | GFW 阻断时不可用 |

### 前置条件（远程电脑需配置）

**第一步：远程电脑开启凭据认证的 SMB 共享**

```powershell
# 1. 关闭 Guest 访问（如果有）
net user Guest /active:no
Set-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" -Name "EnableGuest" -Value 0 -Force

# 2. 关闭密码保护共享（允许空密码登录则设为 0；否则保持 1）
Set-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\Lsa" -Name "LimitBlankPasswordUse" -Value 0 -Force

# 3. 确保 SMB 防火墙规则在 Private 网络放行
Set-NetFirewallRule -Name "FPS-SMB-In-TCP" -Profile Private, Domain

# 4. 重启 SMB 服务
Restart-Service -Name LanmanServer -Force
```

**第二步：本机连接并存储凭据**

```powershell
# 存储远程 Administrator 凭据（空密码或实际密码）
cmdkey /add:远程TailscaleIP /user:Administrator /pass:""

# 映射 C$ 和 D$
net use Y: \\远程TailscaleIP\C$ /persistent:yes
net use Z: \\远程TailscaleIP\D$ /persistent:yes

# 如果需要 UAC 隔离修复（映射后文件管理器不显示）
New-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "EnableLinkedConnections" -PropertyType DWord -Value 1 -Force
# 重启电脑生效
```

### 注意事项

- 网络驱动器走的是 Tailscale 加密隧道，即使远程电脑不在同一局域网也能用
- 映射后重启电脑仍然保留（`/persistent:yes`）
- 如果远程电脑的 Karing TUN 模式开启，需要在 route_exclude_address 中添加本机 Tailscale IP
- 管理共享默认 Administrators 完全控制，可读可写

---

## 三、SSH 远程连接

### 核心结论（重要）

**Windows 上 Tailscale SSH 服务端不可用。** 官方文档明确说明 Tailscale SSH server component 仅支持 Linux 和 macOS。

所以在 Windows 上：
- ✅ Tailscale 负责**网络层加密和 ACL 访问控制**
- ✅ 需要 **Windows OpenSSH Server** 作为 SSH 服务端
- ✅ SSH 认证走传统的 **authorized_keys** 方式
- ❌ `tailscale set --ssh=true` 不支持 Windows
- ❌ `tailscale ssh` 包装器在 Windows 上因主机密钥校验问题不可用

### SSH Config（别名简化）

本机 `~/.ssh/config` 已配置别名，连接时无需记 IP 和用户名：

```
Host remote-laptop
  HostName 100.64.141.0
  User administrator
  StrictHostKeyChecking accept-new
```

### 连接命令

```bash
# 从本机 → 远程笔记本（推荐）
ssh remote-laptop "要执行的命令"

# 从远程笔记本 → 本机
ssh 86150@100.65.183.101 "要执行的命令"
```

### 执行远程 PowerShell 命令（重要注意事项）

**直接通过 SSH 传复杂 PowerShell 命令是灾难——** 嵌套引号、`$` 变量、反引号会导致 escape 地狱，反复调试无果是常态。

**推荐做法（经过实战验证）：** 本地写脚本 → SMB 复制到远程 → SSH 执行。

```bash
# 1. 本地写好脚本文件（D:\Test\remote_task.ps1）

# 2. 通过 SMB（Y: 盘 = 远程 C$）复制到远程
cp D:\Test\remote_task.ps1 Y:/Users/Administrator/remote_task.ps1

# 3. SSH 执行（务必加 -ExecutionPolicy Bypass）
ssh remote-laptop "powershell -ExecutionPolicy Bypass -File C:\Users\Administrator\remote_task.ps1"

# 4. 执行完后清理远程脚本
ssh remote-laptop "del C:\Users\Administrator\remote_task.ps1"
```

**如果必须在 SSH 命令中内联写 PowerShell，注意：**
- **`$env:VAR`** 中的 `$` 要转义为 `\$`（在双引号中）或用单引号包裹
- **反引号 `` ` ``** 要转义为 `` \` ``
- **中文** 在 SSH 输出中会乱码，见"中文 Windows 路径问题"小节的解决方法
- **布尔条件**（`&&`、`||`、`;`）在跨 shell 时行为不一致，尽量拆成多条命令

**执行策略问题：** 远程 Windows 的 PowerShell 默认执行策略可能是 Restricted，导致脚本无法运行。**任何远程执行的 .ps1 脚本都必须加 `-ExecutionPolicy Bypass`：**

```bash
# ✅ 正确
ssh remote-laptop "powershell -ExecutionPolicy Bypass -File C:\path\to\script.ps1"

# ❌ 错误（Permission denied）
ssh remote-laptop "powershell -File C:\path\to\script.ps1"
```

### 前置条件

#### 1. Tailscale ACL 规则

在 https://login.tailscale.com/admin/acls 配置 SSH 规则，**必须删除或注释掉默认的 check 规则**，只保留以下规则：

```json
{
    "src":    ["wingiscrazy@qq.com"],
    "dst":    ["autogroup:self"],
    "users":  ["autogroup:nonroot"],
    "action": "accept",
}
```

#### 2. 安装 OpenSSH Server（被连接方）

```powershell
Add-WindowsCapability -Online -Name "OpenSSH.Server~~~~0.0.1.0"
Start-Service sshd
Set-Service -Name sshd -StartupType "Automatic"
```

#### 3. 配置 SSH 公钥

**客户端公钥（本机）：**
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDVsYK0hsbIr1sAa7BZhHZR9dQN/n0TxQEUx1v+z8jkA Gitee SSH Key
```

**服务端 authorized_keys 位置（关键）：**
管理员用户的授权文件路径是 `C:\ProgramData\ssh\administrators_authorized_keys`，**不是** `~/.ssh/authorized_keys`。

添加公钥后必须重置权限（否则 SSH 不认）：
```powershell
# 写入公钥
$key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDVsYK0hsbIr1sAa7BZhHZR9dQN/n0TxQEUx1v+z8jkA Gitee SSH Key"
$key | Out-File -FilePath "$env:ProgramData\ssh\administrators_authorized_keys" -Encoding ascii -Force

# 重置权限（关键！）
icacls "$env:ProgramData\ssh\administrators_authorized_keys" /inheritance:r /grant "SYSTEM:(R)" /grant "BUILTIN\Administrators:(R)"

# 重启 SSH 服务
Restart-Service sshd
```

---

## 四、已知问题与解决方法

### 1. Karing TUN 模式干扰 SSH

**问题：** Karing TUN 模式会拦截所有流量，导致 SSH 端口 22 连接被重置。

**解决方法（已配置好）：**
在 `karing_setting.json` 的 TUN 配置中添加排除规则：

```json
{
  "enable": true,
  "allow_bypass": true,
  "exclude_local_networks": true,
  "route_exclude_address": ["100.64.141.0/32"]
}
```

- `route_exclude_address` — 远程笔记本的 Tailscale IP 绕过 TUN
- `exclude_local_networks` — 本地局域网（192.168.x.x）不走 TUN
- 修改后重启 Karing 生效

### 2. 首次连接主机密钥确认

```bash
ssh -o StrictHostKeyChecking=accept-new remote-laptop "命令"
```

### 3. Permission denied 排查

先检查 authorized_keys 路径和权限：
- 管理员用户：`C:\ProgramData\ssh\administrators_authorized_keys`
- 必须执行 `icacls` 重置权限
- 文件内容必须是单行公钥，无多余空格

### 4. 管理共享（C$、D$）相关知识

Windows 自动为每个硬盘分区创建隐藏管理共享（`C$`、`D$`、`ADMIN$`），仅 Administrators 可访问。
- 这是系统内置功能，**无需手动创建共享**，直接 `net use` 映射即可
- `D` 普通共享 ≠ `D$` 管理共享，前者需手动创建，后者自动存在
- 管理共享名带 `$` 后缀，网上邻居不可见，需要知道路径才能访问

### 5. 网络驱动器映射后文件管理器不显示

**问题：** 在管理员（提权）PowerShell 中用 `net use` 映射的网络驱动器，在普通权限的文件管理器（explorer.exe）中不可见。这是 Windows UAC 的权限隔离机制。

**解决方法：**
```powershell
# 添加注册表项 EnableLinkedConnections（需管理员身份运行）
New-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "EnableLinkedConnections" -PropertyType DWord -Value 1 -Force
# 重启电脑生效
```

或者在普通（非管理员）PowerShell 中运行 `net use` 映射。

### 6. 中文 Windows 路径与 SSH 乱码

**问题：** SSH 命令中的中文字符（路径、注释、错误消息）在终端输出会变成乱码（如 `ϵͳҲָ·` 或 ``）。原因是：SSH 客户端（Git Bash）使用 UTF-8，而远程 Windows 的 cmd/PowerShell 使用系统区域编码（中文 Windows = GBK/CP936），编码不匹配导致显示错误。

**永久解决方案（推荐，一次配置永久生效）：**

在远程电脑的 PowerShell Profile 中添加编码设置：

```powershell
# 放在 profile 顶部
$OutputEncoding = [Console]::OutputEncoding = [Text.Encoding]::UTF8
```

这会修改远程 PowerShell 会话的控制台编码为 UTF-8，所有后续的 SSH 命令输出都能正确显示中文。PS5.1 和 PS7 都需要加（如果 PS7 的 profile 是 dot-source PS5.1 的，则只需加一次）。

**验证方法：**
```bash
# 修改后测试 SSH 中文输出
ssh remote-laptop "powershell -Command \"Write-Host '中文测试'\""
# 应该正常显示"中文测试"而不是乱码
```

**临时解决方法（来不及改 profile 时）：**

| 方法 | 做法 | 适用场景 |
|------|------|---------|
| 切换远程 console 到 UTF-8 | 命令前加 `chcp 65001 > nul &&` | 单次执行 |
| 避免中文 | 用 `$env:USERPROFILE` 替代中文路径 | 最稳妥 |
| 通过 SMB 操作 | Y:/Z: 盘中文正常显示 | 文件操作 |
| 设置 PowerShell 输出编码 | `[Console]::OutputEncoding = [Text.Encoding]::UTF8` | 单次 session |

### 7. GFW 导致 GitHub 不可用

**问题：** 两台机器在中国大陆，`raw.githubusercontent.com` 被 DNS 污染阻断，`github.com` 间歇性阻断，GitHub releases 下载（`objects.githubusercontent.com` / `release-assets.githubusercontent.com`）超时或截断。

**表现：**
- `Invoke-WebRequest github.com` → OK
- `Invoke-WebRequest raw.githubusercontent.com` → 超时
- `git clone github.com` → 间歇性 fail
- `curl -L github.com/releases/...` → 下载中途断连，zip 文件损坏（"找不到中央目录结尾记录"）

**应对方案（按优先级）：**

| 方案 | 做法 | 适用场景 |
|------|------|---------|
| **本机安装 → SMB 复制** | 本机 Scoop 安装成功 → SMB 复制 `D:\apps\scoop\apps\<name>` 到远程 `Z:\apps\<name>` | 最可靠，已验证通过 |
| **Git 克隆替代** | 用 `git clone --depth 1` 替代 `Invoke-WebRequest`（`github.com` 的 git 通道有时能通） | Scoop 本身的安装 |
| **重试** | GFW 是间歇性阻断，等几分钟重试可能就通了 | Starship 等小文件 |
| **开代理（如有 Karing）** | 启动 Karing 或 VPN，通过代理路由 GitHub 流量 | 远程有 Karing 但通常没开 |

**验证连接的命令：**
```powershell
# 测试 GitHub 连通性
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
Invoke-WebRequest -Uri 'https://github.com' -UseBasicParsing -TimeoutSec 10 -Method Head

# 测试 raw.githubusercontent.com
Invoke-WebRequest -Uri 'https://raw.githubusercontent.com' -UseBasicParsing -TimeoutSec 10 -Method Head
```

---

## 五、日常使用流程

### 远程执行命令

```bash
ssh remote-laptop "要执行的命令"
```

### 传文件到远程

```powershell
# 方法一：Taildrop（端到端加密，适合单文件）
tailscale file cp 本地文件路径 远程设备名:

# 方法二：SMB 网络驱动器（适合大量文件操作）
# 直接操作 Z: 盘，像本地文件一样读写
cp D:\本地文件.txt Z:\目标目录\
```

### 安装软件到远程（GFW 绕行方案）

```powershell
# 1. 本机用 Scoop 安装好
scoop install 软件名

# 2. SMB 复制到远程（Z: = 远程 D$, Y: = 远程 C$）
# 工具本身：复制到 D:\apps\<软件名>
cp -r D:\apps\scoop\apps\<软件名>\current\. Z:\apps\<软件名>\

# 3. 注册到远程 PATH
ssh remote-laptop "powershell -ExecutionPolicy Bypass -Command \"[Environment]::SetEnvironmentVariable('PATH', 'D:\apps\<软件名>;\'+[Environment]::GetEnvironmentVariable('PATH','User'), 'User')\""
```

### 从远程取文件

```powershell
# 方法一：通过 Z: 盘直接读取
cat Z:\远程文件.txt

# 方法二：远程用 Taildrop 发回来
ssh remote-laptop "tailscale file cp 文件路径 pc-zz:"
tailscale file get D:\目标目录
```

### 读写远程系统文件（如 .claude 配置）

Y: 盘已映射到远程 C$，直接操作：

```powershell
# 直接读取远程 .claude 配置
cat Y:/Users/Administrator/.claude/rules/installation.md

# 或者通过 SSH
ssh remote-laptop "powershell Get-Content \$env:USERPROFILE\.claude\rules\installation.md"
```

---

## 六、安全加固（重要）

### 安全风险矩阵

| 攻击面 | 防护措施 | 风险等级 |
|--------|---------|---------|
| **物理接触** | 远程电脑在国家级保密环境 | 🟢 极低 |
| **Tailscale 网络** | ACL 仅允许 `wingiscrazy@qq.com` 作为 Source | 🟢 极低 |
| **WireGuard 加密** | 端到端加密，无已知漏洞 | 🟢 极低 |
| **SMB 网络共享** | 仅限 Administrators 完全控制，防火墙仅 Domain/Private | 🟡 低 |
| **SSH 远程** | 仅密钥认证，Tailscale ACL 二次控制 | 🟢 极低 |
| **空密码账户** | 通过 `LimitBlankPasswordUse=0` 允许，但需结合物理安全 | 🟡 低（需物理安全） |

### 加固步骤

**第一步：远程电脑禁用匿名访问**

```powershell
# 禁用 Guest 账户
net user Guest /active:no

# 关闭 SMB Guest 访问
Set-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" -Name "EnableGuest" -Value 0 -Force

# 移除用户创建的普通共享（如果有），改用管理共享
Remove-SmbShare -Name "D" -Force -ErrorAction SilentlyContinue

# 移除 Everyone NTFS 权限（如有）
icacls D:\ /remove Everyone /q

# 修改 SMB 防火墙为 Private/Domain 专用（移除 Public）
Set-NetFirewallRule -Name "FPS-SMB-In-TCP" -Profile Private, Domain

# 重启 SMB 服务
Restart-Service -Name LanmanServer -Force
```

**第二步：本机安全连接**

```powershell
# 禁用 Guest 回退
Set-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters" -Name "AllowInsecureGuestAuth" -Value 0 -Force

# 使用 Administrator 凭据映射管理共享
cmdkey /add:远程TailscaleIP /user:Administrator /pass:""
net use Y: \\远程TailscaleIP\C$ /persistent:yes
net use Z: \\远程TailscaleIP\D$ /persistent:yes
```

**第三步：SSH 安全**

```powershell
# 确认 authorized_keys 权限正确
icacls "C:\ProgramData\ssh\administrators_authorized_keys"
# 应只有 BUILTIN\Administrators:(R) 和 NT AUTHORITY\SYSTEM:(R)
```

### 安全设计原则

- **最小权限原则**：SMB 共享仅授予 Administrators，无多余账户
- **纵深防御**：Tailscale ACL + SMB 防火墙 + NTFS 权限 + 凭据认证，多层防护
- **空密码合理性**：仅在物理安全有保障、网络仅通过 Tailscale 加密通道连接时可行
- **默认不信任**：所有网络服务默认不对外暴露，仅通过 Tailscale Private 网络访问

---

## 参考

- Tailscale 官方文档：https://tailscale.com/kb/1193/tailscale-ssh
- Taildrop 文档：https://tailscale.com/kb/1270/taildrop