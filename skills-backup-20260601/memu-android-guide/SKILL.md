---
name: memu-android-guide
description: >
  逍遥模拟器 (MEmu) Android 自动化操作与排错知识库。当用户需要操作逍遥模拟器、
  通过 android-mcp 控制模拟器、排查 MEmu 截图/连接/ADB 问题、配置 android-mcp、
  或提到"逍遥模拟器""MEmu""android-mcp""模拟器截图白屏""模拟器ADB连接"时，
  必须使用此 skill。即使用户只说"帮我操作一下模拟器""模拟器截图怎么不行"
  "android-mcp 连不上"也应触发。覆盖：MEmu 特有配置、Vulkan 渲染要求、
  3 层截图回退机制、ADB 路径选择、android-mcp 源码部署、常见问题排查。
---

# 逍遥模拟器 (MEmu) Android 自动化指南

本 skill 封装了在实际使用逍遥模拟器 + android-mcp 过程中积累的全部经验知识，
帮助避免重复踩坑，快速定位和解决问题。

## 1. 核心配置参数

### 设备信息

| 参数 | 值 |
|------|-----|
| 模拟器型号 | ASUS_I005DA |
| Android 版本 | 9 (SDK 28) |
| 屏幕分辨率 | 1600x900 |
| ADB 地址 | `127.0.0.1:21503` |
| 默认实例端口 | 21503（多实例：21503, 21513, 21523...） |

### ADB 路径（关键！）

**必须使用逍遥模拟器自带的 ADB**，不能用 Android SDK 的 adb.exe：

```
D:\apps\Microvirt\MEMu\adb.exe   <- 正确
D:\apps\Android\Sdk\platform-tools\adb.exe  <- 会导致 screencap 损坏
```

原因：MEmu 的 ADB 是定制版本，与 MEmu 的帧缓冲区协议兼容。Android SDK 的标准 ADB
在 MEmu 上 `screencap -p` 会产生 7738 字节的损坏 PNG（全白），而 MEmu ADB 能正确
获取 800KB+ 的有效截图。

### 渲染模式（关键！）

**必须使用 Vulkan 渲染模式。** 在 MEmu 设置 -> 引擎设置 -> 渲染模式中选择 Vulkan。

| 渲染模式 | minicap 截图 | ADB screencap | mss 截图 | 推荐度 |
|---------|-------------|---------------|---------|--------|
| **Vulkan** | 100% 成功 | 正常 | 黑屏 | 最佳 |
| OpenGL | ~17% 白屏 | 不稳定 | 正常 | 不推荐 |
| DirectX | 类似 OpenGL | 不稳定 | 正常 | 不推荐 |

OpenGL/DirectX 下 GPU 离屏渲染导致帧缓冲区不同步，minicap 和 screencap 读取到
的是过期/空白的缓冲区内容。Vulkan 的底层 API 保证了帧缓冲区与显示同步。

## 2. android-mcp 配置

### 从源码运行（推荐）

PyPI 上的 `android-mcp 0.1.0` 是过时版本（2025年12月），只支持 `--emulator` 参数。
GitHub 最新版支持 `--device`、`--wifi`、`--usb`、`--connection` 参数，功能完整
（408行 vs 78行）。

**源码路径：** `D:\Test\jerry_ZhuanShengBen\Android-MCP\Android-MCP-master\`

**MCP 配置（mcp.json）：**

```json
{
  "android-mcp": {
    "command": "C:\\Users\\86150\\.local\\bin\\uv.exe",
    "args": [
      "--directory",
      "D:\\Test\\jerry_ZhuanShengBen\\Android-MCP\\Android-MCP-master",
      "run",
      "android-mcp",
      "--device",
      "127.0.0.1:21503"
    ]
  }
}
```

**全局配置文件路径：** `C:\Users\86150\AppData\Roaming\TRAE SOLO CN\User\mcp.json`

注意：Trae SOLO CN 中项目级 `.mcp.json` 不会覆盖全局配置，必须修改全局文件。

### 连接参数说明

| 参数 | 用途 | 示例 |
|------|------|------|
| `--device SERIAL` | 通过 ADB 序列号连接 | `--device 127.0.0.1:21503` |
| `--wifi HOST:PORT` | 通过 WiFi 连接 | `--wifi 192.168.1.100:5555` |
| `--usb` | 通过 USB 连接首个设备 | `--usb` |
| `--emulator` | 连接 emulator-5554（旧版） | `--emulator` |

### 可用的 14 个 MCP 工具

| 工具 | 功能 |
|------|------|
| ListDevices | 列出已连接设备 |
| ConnectDevice | 连接指定设备 |
| Click / ClickBySelector | 点击（坐标/选择器） |
| LongClick | 长按 |
| Swipe | 滑动 |
| Drag | 拖拽 |
| Type | 输入文本 |
| Press | 按键（Home/Back/Enter 等） |
| Snapshot | 截图 + UI 层级快照 |
| Notification | 获取通知栏内容 |
| Wait / WaitForElement | 等待条件满足 |
| Device | 获取设备信息 |
| Shell | 执行 ADB shell 命令 |

## 3. 截图机制详解

### 3 层回退架构

已修改 `service.py` 中的截图逻辑，实现智能回退：

```
Tier 1: uiautomator2 minicap（最快 ~0.65s）
  | 检测到白屏（>99% 亮色像素 或 <=3 种颜色）时降级
  v
Tier 2: ADB screencap -p 写文件 + pull（~1.5s）
  | 也白屏时继续降级
  v
Tier 3: mss Windows Desktop Duplication API（~0.06s）
  | Vulkan 下黑屏时记录日志，返回最佳可用结果
  v
返回最后一张可用截图（即使空白也返回，不抛异常）
```

### 白屏检测逻辑

MEmu 的"空白截图"不是黑色而是 **纯白色 (255,255,255)**，
PNG 压缩后仅 6.5KB。通过检测亮色像素比例和唯一颜色数来判断：
- 亮色像素（RGB 各通道之和 > 240）占比 > 99% → 白屏
- 唯一颜色数 <= 3 → 白屏

### 各方案在不同渲染模式下的表现

**Vulkan 模式（推荐）：**
- minicap：100% 成功，0.65s，1600x900，~460KB
- ADB screencap：正常，~797KB
- mss：黑屏（Vulkan 独占 GPU，Desktop Duplication 无法捕获）

**OpenGL 模式（不推荐）：**
- minicap：~17% 成功，大部分返回 6.5KB 白屏
- ADB screencap：7738 字节损坏文件
- mss：正常，1920x1080，~177KB

## 4. 常见问题排查

### 问题：android-mcp 启动报错 `unrecognized arguments: --device`

**原因：** PyPI 版本 0.1.0 只支持 `--emulator`，不支持 `--device`。

**解决：** 使用 GitHub 源码运行，见第 2 节配置。

### 问题：截图全白/空白

**排查步骤：**

1. 确认渲染模式是否为 Vulkan（MEmu 设置 -> 引擎设置）
2. 如果是 OpenGL，切换到 Vulkan 并重启模拟器
3. 如果已经是 Vulkan 仍白屏，检查是否是特定 App（如 Settings）的问题
4. 确认使用的是 MEmu 自带 ADB，不是 Android SDK 的

### 问题：ADB 连接失败

```bash
# 检查设备是否在线
D:\apps\Microvirt\MEMu\adb.exe devices

# 手动连接
D:\apps\Microvirt\MEMu\adb.exe connect 127.0.0.1:21503

# 重启 ADB 服务
D:\apps\Microvirt\MEMu\adb.exe kill-server
D:\apps\Microvirt\MEMu\adb.exe start-server
```

### 问题：MCP 配置不生效

Trae SOLO CN 中项目级 `.mcp.json` 不会覆盖全局配置。必须修改：
`C:\Users\86150\AppData\Roaming\TRAE SOLO CN\User\mcp.json`

修改后需要重启 Trae IDE。

### 问题：uiautomator2 截图卡住

minicap 进程可能死锁。解决：
1. 重启模拟器
2. 或通过 ADB 杀掉 minicap 进程：`adb shell killall minicap`
3. uiautomator2 会在下次截图时自动重启 minicap

### 问题：screencap -p 管道输出损坏

MEmu 的 `adb shell screencap -p` 通过 stdout 管道输出时会产生 7738 字节损坏文件。
**必须使用文件中转方式：**

```bash
adb shell screencap -p /sdcard/screenshot.png
adb pull /sdcard/screenshot.png ./screenshot.png
adb shell rm /sdcard/screenshot.png
```

## 5. 操作最佳实践

### 坐标系统

MEmu 屏幕分辨率 1600x900，坐标原点在左上角：
- 中心点：(800, 450)
- 状态栏区域：y < 50
- 导航栏区域：y > 850

### 等待策略

UI 操作后建议等待 0.5-1 秒再截图，确保画面渲染完成：

```python
d.click(400, 300)
time.sleep(0.8)
img = d.screenshot()
```

### App 操作

```python
d.app_start('com.android.settings')
d.app_stop('com.android.settings')
d.app_current()
```

### 输入文本

Type 操作会触发输入法，可能影响截图。输入完成后建议按 Back 关闭键盘：

```python
d.click(400, 300)
time.sleep(0.3)
d.send_keys('hello world')
d.press("back")
```

### 多实例管理

MEmu 多实例的 ADB 端口规律：
- 实例 1：127.0.0.1:21503
- 实例 2：127.0.0.1:21513
- 实例 3：127.0.0.1:21523
- 依此类推，每次 +10

## 6. 依赖与版本

| 依赖 | 版本 | 说明 |
|------|------|------|
| Python | >=3.13,<3.14 | android-mcp 源码要求 |
| fastmcp | >=2.14.0 | MCP 服务器框架 |
| pillow | >=11.2.1 | 图像处理 |
| uiautomator2 | >=3.3.1 | Android UI 自动化 |
| mss | latest | Windows 截图回退（已安装到 venv） |
| uv | latest | Python 包管理器 |

## 7. 文件路径速查

| 文件 | 路径 |
|------|------|
| MEmu ADB | `D:\apps\Microvirt\MEMu\adb.exe` |
| uv 可执行文件 | `C:\Users\86150\.local\bin\uv.exe` |
| android-mcp 源码 | `D:\Test\jerry_ZhuanShengBen\Android-MCP\Android-MCP-master\` |
| 全局 MCP 配置 | `C:\Users\86150\AppData\Roaming\TRAE SOLO CN\User\mcp.json` |
| 修改后的 service.py | `...Android-MCP-master\src\android_mcp\mobile\service.py` |
