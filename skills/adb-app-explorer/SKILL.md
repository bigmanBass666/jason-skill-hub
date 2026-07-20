---
name: adb-app-explorer
---
# ADB App Explorer

> 快速、系统性地对任何陌生 Android App 进行全量 UI 探索，生成完整的功能地图。目标是让 AI 在 10 分钟内掌握一个 App 的所有能力，而不是花几个小时被反复纠正。

## 核心原则

1. **先拿地图，再走路** — 进入 App 前，先获取所有 Activity 和入口点
2. **dumpsys 优先，dump 兜底，截图保底** — 三种方法按可靠性排序使用
3. **工具失败立即换路径** — 同一方法失败 2 次就切换，不重试
4. **递归到底** — 每个可交互元素都要点进去，不能只看顶层
5. **发现隐藏元素** — dumpsys 能看到 View 树中隐藏（GONE/INVISIBLE）的元素
6. **像用户一样探索，不像机器人** — 不是逐个点过去完成清单，而是理解每个功能的用途和价值
7. **发现一个记录一个** — 不攒到最后再整理，每探索完一个页面立即输出发现
8. **核心功能深入，边缘功能一笔带过** — 主页面和核心流程深入探索，法律信息等页面快速记录即可

## 触发场景

- 用户说"探索这个 app 的 UI"、"看看这个 app 有什么功能"、"帮我看看这个 app"
- 需要通过 ADB 自动化操作 Android 设备上的 App
- 需要了解某个 App 的完整功能结构
- 用户提到 ADB + App 功能探索

## 工具要求

- ADB（Android Debug Bridge）已安装且设备已连接
- free-vision skill（用于截图分析）

---

## 探索流程

### Phase 0: 侦察（进入 App 前）

```bash
# 1. 确认设备连接
adb devices

# 2. 获取目标 App 信息
adb shell pm dump <package_name> | grep -E "versionName|versionCode|targetSdk" | head -5

# 3. 获取所有 Activity 入口点（这是最关键的一步）
adb shell cmd package resolve-activity --brief -c android.intent.category.LAUNCHER <package_name>

# 4. 获取完整的 Activity 列表
adb shell dumpsys package <package_name> | grep "Activity" | grep -v "activityManager" | sort -u

# 5. 获取当前前台 Activity 栈
adb shell "dumpsys activity activities" | grep "Hist #"
```

### Phase 1: 获取第一屏的完整 View 树

对每个 Activity 用三种方法获取 UI 信息（按优先级）：

**方法 A（首选）: dumpsys activity top**
```bash
# 获取 native View 树（永远可用，包含隐藏元素）
adb shell "dumpsys activity top" > /tmp/dumpsys_full.txt

# 提取当前 Activity 的 View 树
grep -n "DecorView" /tmp/dumpsys_full.txt  # 找到所有 View Hierarchy 位置
# 提取最后一个（最顶层）的 View 树
sed -n '/DecorView.*<ActivityName>/,/^$/p' /tmp/dumpsys_full.txt | grep "app:id/"
```

**方法 B（补充）: uiautomator dump**
```bash
# 获取 accessibility tree（有文字和交互属性）
adb shell uiautomator dump //sdcard//ui.xml && adb pull //sdcard//ui.xml
# 分析所有可交互元素
cat ui.xml | tr '>' '\n' | grep "clickable=\"true\"\|text=" | grep -v 'text=""'
```

**方法 C（兜底）: 截图 + vision**
```bash
# ✅ 正确：直接 pipe 到电脑，不经过手机存储
adb exec-out screencap -p > /tmp/screenshot.png

# ❌ 错误：这会把文件存到手机 /sdcard/，占满存储
# adb shell screencap -p //sdcard//screen.png && adb pull //sdcard//screen.png
```

### Phase 4: 自动清理

**每次探索结束后必须执行：**
```bash
# 清理手机上所有探索产生的临时文件
adb shell "rm -f //sdcard//ui*.xml //sdcard//screen*.png //sdcard//s*.png //sdcard//diag*.png"
```

**探索开始前也检查并清理残留：**
```bash
# 检查手机上是否有残留的探索文件
adb shell "ls //sdcard//ui*.xml //sdcard//screen*.png //sdcard//s*.png 2>/dev/null | wc -l"
# 如果 > 0，先清理
adb shell "rm -f //sdcard//ui*.xml //sdcard//screen*.png //sdcard//s*.png"
```

### Phase 2: 系统性遍历（像用户一样探索）

**不是逐个点过去完成清单，而是理解每个功能的用途和价值。**

**遍历策略：**
- 从主页面开始，按重要性排序探索（核心功能 > 配置选项 > 辅助页面）
- 在核心功能上花 80% 的时间，边缘页面快速记录即可
- 发现一个页面就立即记录，不攒到最后
- 遇到子页面就递归进去，不要跳过

**功能重要性分级：**
| 级别 | 定义 | 探索深度 |
|------|------|----------|
| P0 核心 | 主要入口、核心操作流程 | 深入：每个可交互元素都点 |
| P1 重要 | 配置选项、账户管理 | 中等：主要选项都记录 |
| P2 辅助 | 诊断、帮助、法律 | 快速：记录有哪些就行 |

**从 dumpsys 获取的 View 树中提取所有可交互元素：**
```bash
# 所有可点击元素
grep "clickable=\"true\"" ui.xml

# 所有有文字的元素（带 ID）
cat ui.xml | tr '>' '\n' | grep "text=" | grep -v 'text=""'
```

**对每个可交互元素：**
1. 记录元素信息（ID、文字、类型、bounds）
2. 计算中心坐标：`x = (left + right) / 2`, `y = (top + bottom) / 2`
3. 点击：`adb shell input tap $x $y`
4. 等待 2 秒让页面加载
5. 获取新页面的 View 树（Phase 1 的三种方法）
6. 如果是新页面/子页面，递归执行 Phase 2
7. 返回上一页：`adb shell input keyevent 4`

**滚动检测：**
```bash
# 如果页面可能有更多内容，向下滚动
adb shell input swipe 540 1800 540 400 500
# 再次获取 View 树，检查是否有新元素出现
```

**发现即记录（增量文档化）：**

每探索完一个页面，立即追加发现到输出文件，不攒到最后：

```markdown
## [页面名称] (Activity名)
- **入口**: 从 [上一级页面] 的 [按钮名] 进入
- **可见元素**: [元素1], [元素2], ...
- **可交互元素**: [元素1]→跳转到X, [元素2]→弹出对话框, ...
- **隐藏元素**: [element_id] (GONE/INVISIBLE), 说明
- **功能判断**: 这个页面是用于 [XXX] 的
```

### Phase 3: 构建地图

将所有发现整理为递归树结构，保存到项目记忆文件。

---

## 关键命令速查

| 操作 | 命令 |
|------|------|
| 启动 App | `adb shell am start -n <pkg>/<activity>` |
| 清数据 | `adb shell am force-stop <pkg>; adb shell pm clear <pkg>` |
| 点击 | `adb shell input tap $x $y` |
| 滑动 | `adb shell input swipe $x1 $y1 $x2 $y2 $duration` |
| 输入文字 | `adb shell input text "text"` |
| 返回 | `adb shell input keyevent 4` |
| 截图 | `adb shell screencap -p //sdcard//s.png && adb pull //sdcard//s.png` |
| UI dump | `adb shell uiautomator dump //sdcard//ui.xml && adb pull //sdcard//ui.xml` |
| View 树 | `adb shell "dumpsys activity top"` |
| Activity 栈 | `adb shell "dumpsys activity activities" | grep "Hist #"` |
| 包信息 | `adb shell pm dump <pkg> | grep version` |
| 杀进程 | `adb shell am force-stop <pkg>` |

---

## 输出格式

保存到项目记忆目录 `<memory_dir>/app-ui-map.md`：

```markdown
---
name: <app-name>-ui-map
description: "<App> 完整递归 UI 地图，含 dumpsys 验证的 View ID 和隐藏元素"
metadata:
  type: reference
---

# <App> 完整递归 UI 地图

## App 信息
- 包名/版本/SDK

## 完整 Activity 树
├── Activity 1
│   ├── 可交互元素 A → 跳转目标
│   ├── 可交互元素 B → 子页面
│   │   ├── 子元素 1
│   │   └── 子元素 2
│   └── 隐藏元素（GONE/INVISIBLE）
└── Activity 2
    └── ...

## dumpsys 发现的隐藏元素
| 元素 | 所在页面 | 说明 |
```

---

## 反复失败时的备选方案

当 uiautomator dump 反复失败时，按以下顺序尝试：

1. **dumpsys activity top** — 永远可用
2. **adb shell dumpsys window windows** — 窗口信息
3. **截图 + vision AI** — 最后的视觉兜底
4. **adb shell dumpsys input_method** — 输入法信息
5. **直接启动 Activity** — 绕过 UI 导航：`adb shell am start -n <pkg>/<full.activity.name>`

## 常见陷阱

- **UI dump 失败**：VPN 对话框、系统权限弹窗会阻塞 uiautomator
- **坐标偏移**：不同分辨率设备的坐标不同，用 bounds 计算而非硬编码
- **弹窗阻塞**：权限弹窗、电池优化弹窗会阻塞操作，需要先处理
- **React Native/Flutter 组件**：标准 tap 可能无效，需要尝试不同位置
- **隐藏元素**：`visibility=GONE` 的元素在 dumpsys 中可见但截图看不到
