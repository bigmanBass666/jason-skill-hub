---
name: awwwards-design
description: "创建具有 Awwwards 头奖级水准的设计级网站。当用户要求创建视觉震撼、沉浸式体验、头奖级的网站、作品集、品牌展示页、产品落地页、创意代理网站，或任何追求极致视觉与交互体验的 web 项目时，必须使用此 skill。关键词触发：「Awwwards 级别」「沉浸式网站」「震撼视觉」「高端网站」「创意交互」「WebGL」「Scrollytelling」「头奖设计」「极致动效」「创意代理网站」「Site of the Day」「SOTD」「超酷网站」「逼格网站」「设计感网站」「3D 网站」「滚动动画」「叙事滚动」「品牌体验」「作品集」「Portfolio」。即使用户只说「帮我做个很酷的网站」「做个有设计感的页面」也应触发此 skill。"
---

# Awwwards SOTD 头奖级网站设计系统

此 skill 使你能够创建达到 Awwwards SOTD 头奖网站水准的 web 体验——视觉震撼、交互出众、性能卓越。它基于对 2024–2026 年度头奖网站的逆向工程研究，提炼出世界级设计的完整方法论。

**核心理念：** Awwwards SOTD 头奖级的设计不是炫技——是视觉叙事、交互创新和工程品质的三位一体。一个真正优秀的网站让用户在打开的瞬间就知道"这不是模板"。

### 执行流程

1. **确定方向**：阅读下方「设计思维框架」，明确叙事核心、视觉语言、交互哲学和 Wow Moment
2. **深入设计**：参考 `references/design-process.md` 获取项目类型适配指南
3. **按需参考**：根据设计方向，读取 `references/` 中对应的参考文件（见末尾索引）
4. **实现交付**：按下方「交付标准」checklist 逐项通过

> **快速导航：** [设计品质维度](#设计品质维度) → [设计思维框架](#设计思维框架) → [设计系统](#设计系统) → [核心交互模式](#核心交互模式) → [性能约束](#性能约束可用性的核心) → [交付标准](#交付标准) → [参考文件索引](#参考文件索引)

---

## 设计品质维度

世界级网站不是「每个方面都平均用力」，而是在正确的维度上做到极致。Awwwards 的评审权重（Design 40% + Usability 30% + Creativity 20% + Content 10%）揭示了一个关键洞察：**视觉和可用性合计占 70%——好看又好用是基础**。创意 20% 是从「还不错」到「令人难忘」的差异化因素。内容 10% 是最容易被忽视但能显著提升品质感的环节。

用这个优先级指导设计决策时的取舍：

| 维度 | 权重 | 核心关注 | 常见陷阱 |
|------|------|----------|----------|
| **Design 设计** | 40% | 视觉层次、字体品位、色彩克制、间距节奏、原创性 | 使用模板/通用字体/素材库图片会让网站看起来"千篇一律" |
| **Usability 可用性** | 30% | 导航直观、加载 <3s、移动端体验、Core Web Vitals | 一个好看但 5 秒加载的网站，用户不会等 |
| **Creativity 创意** | 20% | **一个**签名式「Wow Moment」、交互创新、形式统一内容 | 20 个普通特效 ≠ 1 个令人难忘的时刻 |
| **Content 内容** | 10% | 真实文案、品牌声音、原创媒体 | Lorem ipsum 和素材图会让品质感崩塌 |

> 详细自检清单、第一印象测试、常见陷阱、Ma/間 哲学、SOTD 差距诊断、设计陷阱识别，参见 `references/quality-framework.md`。

---

## 设计思维框架

世界级网站是「讲故事」——不是堆砌技术。在写任何代码之前，先想清楚这三个层面：

### 1. 叙事核心（Narrative Core）—— 这个网站在讲什么故事？

用户从首屏到尾部的情感弧线是什么？这决定了所有设计决策的方向。

- **好的叙事核心：**「速度作为一种美学」「从混沌走向秩序」「材质与光的对话」「在数字空间中漫步」
- **模糊的叙事核心：**「展示我们的产品」「公司介绍」「一个好看的网站」

> 为什么这很重要？没有叙事核心的设计容易变成特效的堆砌。每个设计决策——字体选择、色彩方案、动画节奏——都应该服务于这个故事。

### 2. 视觉语言（Visual Language）—— 选择一种风格并坚定执行

出色的设计不是风格多复杂，而是一种风格的执行深度。从以下风格中选择一个：

| 风格 | 特征 | 适用场景 |
|------|------|----------|
| **新极简主义** | 超大字体 + 极端留白 + 2-3色克制 | 个人作品集、高端品牌、建筑事务所 |
| **有机感官** | 流体动画 + 噪点纹理 + 自然色调 | 环保品牌、艺术展览、科技"人性化"页面 |
| **数字朋克** | 高对比 + 故障美学 + 霓虹色 | 游戏工作室、音乐品牌、Web3 项目 |
| **Bento Grid** | 模块化网格 + 非对称变体 + 悬停动效 | SaaS 产品页、功能展示、数据仪表盘 |
| **电影沉浸** | 全屏媒体 + 电影比例 + 暗色基底 | 影视公司、品牌故事长页、建筑可视化 |
| **反设计/粗野** | 原始边框 + 大面积色块 + 打破常规 | 设计工作室、独立杂志、创意机构 |
| **Y2K 复古** | 像素 + 霓虹 + 90年代怀旧 | 音乐品牌、街头品牌、Gen-Z 潮流 |
| **档案式排版** | 等宽字体 + 密集信息流 + 网格 | 技术文档、开发者工具、数据平台 |

> 每种风格的完整配色方案、排版策略和 CSS 实现，参见 `references/visual-styles.md`。

### 3. 交互哲学（Interaction Philosophy）—— 一句话定义交互行为

交互风格应该自然地服务于叙事核心，而不是生硬地叠加：

- 「每次滚动揭开故事的下一页」（Scrollytelling）— 适合品牌叙事
- 「鼠标是这个世界的眼睛」（Cursor-driven）— 适合探索式体验
- 「在 3D 空间中漫游」（Spatial）— 适合产品展示
- 「内容像杂志一样翻阅」（Editorial）— 适合内容密集型

### 4. 签名式 Wow Moment —— 从「好看」到「令人难忘」

**这是最重要的设计决策。** Awwwards SOTD 头奖网站的核心区别不是 20 个炫酷效果，而是 **1 个让用户停下来截图的时刻**。

```
Wow = 意外交互 × 情感共鸣 × 极致打磨
```

> 为什么强调"1个"而不是"多个"？因为人的记忆是选择性的——用户离开网站后只会记住一个瞬间。把所有精力集中在一个真正令人难忘的时刻上，比分散在 20 个平庸效果上有效得多。

**设计 Wow Moment 的步骤：**
1. 明确核心印象：用户离开后，唯一会记住的瞬间是什么？
2. 选择表达载体：3D 场景 / 滚动叙事 / 数据可视化 / 游戏 / 艺术装置
3. 设计惊喜转折：在哪个节点制造"意料之外"？
4. 注入情感层：幽默 / 震撼 / 温暖 / 好奇 — 选一种
5. 极致打磨：easing、timing、loading、降级方案，全部到位

**经典模式参考：**
- 3D 游戏导航（Bruno Simon — 开车穿过作品集）
- 产品互动乐园（Lando Norris — WebGL 赛车体验）
- 叙事滚动（Igloo Inc — 在 3D 世界中浏览项目）
- 数据 × 娱乐融合（Shopify Live Globe — 全球销售数据 + 可玩游戏）
- 微交互杰作（Messenger — 每个悬停/滚动都展示个性）

> 详细的 Wow Moment 设计模式和实现代码，参见 `references/interaction-patterns.md`。

---

## 设计系统

### 排版系统

字体是顶级网站最重要的设计武器。Awwwards 评委和用户会在 0.5 秒内通过字体判断一个网站是否"做过设计"。

**为什么避免 Inter/Roboto/Arial？** 因为它们是系统默认字体和模板标配——使用它们会让网站立刻看起来像模板或 AI 生成。这和字体本身的质量无关，而是它们已经被过度使用到了丧失视觉个性的程度。

**字体选择指南：**

| 场景 | 推荐 | 避免 |
|------|------|------|
| 展示字体 | PP Neue Montreal, Clash Display, Druk Wide, Syncopate, Instrument Serif | Inter, Roboto, Arial, Poppins |
| 正文字体 | Satoshi, Suisse Int'l, Söhne, Freight Text | System-ui, sans-serif 默认 |
| 等宽/技术 | Space Mono, Geist Mono, JetBrains Mono | Courier New（除非档案风格） |
| 衬线体 | Instrument Serif, Freight Display, Canela | Times New Roman（正文） |

**关键排版数值：**
- Hero 字号：`clamp(4rem, 12vw, 14rem)` — 字体即视觉锚点
- Hero 行高：`0.85–0.92` — 紧实感
- Hero 字间距：`-0.03em` 到 `-0.05em` — 大字号收紧
- 正文字号：`clamp(0.9rem, 1.2vw, 1.15rem)`
- 正文行高：`1.5–1.7`，最大宽度 `65ch`
- 标签/标注：`0.7rem`，`letter-spacing: 0.15em`，`text-transform: uppercase`

**Kinetic Typography（动态排版）** 是当前的核心趋势——文字随滚动/交互运动、变形、揭示。文字不仅是「阅读」的，它就是视觉设计本身。

> 详细字体系统、配对方案、CSS 实现参见 `references/typography-system.md`。

### 色彩系统

**核心规律：背景 + 文字 + 1个强调色 = 完整调色板。不超过 3 色。** 为什么？因为克制本身就是高级感。看看 Lando Norris SOTY 2025——仅用 2 色就创造了年度最佳网站。

```css
/* 模式1：极端对比（最经典、头奖率最高） */
--c-bg: #0a0a0a;
--c-text: #f0ece4;
--c-accent: #ff3d00;  /* 一个鲜明强调色，仅用于关键元素 */

/* 模式2：暗调奢华 */
--c-bg: #111111;
--c-text: #e8e0d0;
--c-accent: #c9a96e;

/* 模式3：泥土有机（2026 新兴趋势） */
--c-bg: #f5f0e8;
--c-text: #1a1208;
--c-accent: #8b6914;

/* 模式4：赛博霓虹 */
--c-bg: #050510;
--c-text: #e0e8ff;
--c-accent: #00ff88;
```

**色彩趋势要点：**
- 暗色模式是默认选择——让 3D 元素、渐变和发光效果更突出
- Glow 效果（文字/按钮/3D 元素发光）是当前关键趋势
- 反设计趋势使用高饱和多色，但需要有意识的设计意图而非随意堆砌

### 动画缓动曲线

为什么缓动曲线重要？因为默认的 `ease-in-out` 让动画看起来像 PowerPoint。自定义缓动是区分"专业"和"业余"动画的最简单方式。

```javascript
const easings = {
  enter:    "cubic-bezier(0.16, 1, 0.3, 1)",    // Expo Out — 出现动画
  hover:    "cubic-bezier(0.34, 1.56, 0.64, 1)", // Back Out — 悬停微交互（带回弹）
  page:     "cubic-bezier(0.87, 0, 0.13, 1)",    // Expo InOut — 页面切换
  reveal:   "cubic-bezier(0.25, 1, 0.5, 1)",     // Quart Out — 揭示动画
  magnetic: "cubic-bezier(0.23, 1, 0.32, 1)",    // 磁性按钮回弹
}
```

---

## 核心交互模式

### SOTD 标配模式

**A. Scroll-Driven 叙事（Scrollytelling）**
这是当前世界级网站的第一交互范式。用 GSAP ScrollTrigger + Lenis 实现。
- 文字逐行/逐词揭示
- 固定视差滚动叙事（pinned sections）
- 进度驱动的动画序列
- 水平滚动画廊嵌套在垂直流中

**B. 自定义光标**
SOTD 头奖网站中出现频率最高的交互模式（466+ 收藏集收录）。它是最小投入、最大视觉回报的元素——一个小圆点 + 跟随圆环就能让网站立刻区别于普通网站。

**C. CSS 品质信号**

以下 CSS 规则是 SOTD 头奖网站的标配。它们不增加任何加载成本，但传递的信息是「这个网站的每个像素都被设计过」——缺失它们就像穿着定制西装搭配运动鞋：

```css
/* 1. 自定义选中色 ::selection */
::selection {
  background: var(--c-accent);
  color: var(--c-bg);
}
::-moz-selection {
  background: var(--c-accent);
  color: var(--c-bg);
}

/* 2. 字体渲染优化 */
body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}

/* 3. 文字智能换行 */
h1, h2, h3, h4, h5, h6 {
  text-wrap: balance;   /* 标题均匀分行，避免最后一行只有一个词 */
}
p, li, blockquote {
  text-wrap: pretty;    /* 段落避免末尾孤词 */
}

/* 4. 平滑滚动（如未使用 Lenis） */
html { scroll-behavior: smooth; }

/* 5. 自定义滚动条 */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--c-bg); }
::-webkit-scrollbar-thumb {
  background: var(--c-muted);
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: var(--c-accent); }

/* 6. 表单元素统一（如页面含表单） */
::placeholder { color: var(--c-muted); opacity: 0.6; }
input:focus, textarea:focus, select:focus {
  outline: none;
  border-color: var(--c-accent);
}

/* 7. 同心圆角 — 嵌套元素的圆角必须同心对齐 */
/* 公式：外层圆角 = 内层圆角 + padding */
/* 例：内层 12px + padding 8px = 外层 20px */
/* 错误示范：外层 20px + 内层 16px + padding 8px → 视觉断裂 */
```

> **为什么这些很重要？** 用户选中文字时的背景色是第一个「这不普通」的信号。自定义滚动条是第二个。字体抗锯齿是第三个。`text-wrap: balance` 让标题排版看起来经过设计而非浏览器默认行为。同心圆角公式避免了嵌套元素圆角不一致的「业余感」。这几项加起来不到 5 分钟，但传递的信息是「这个网站的每个像素都被设计过」。

**D. 页面加载动画（Preloader）**
第一印象的起点。世界级网站的预加载器是品牌介绍，不是等待转圈。
- 计数器式（0→100%）、品牌化遮罩退场、多步骤序列

**E. 页面过渡**
消除页面间的白色闪烁。推荐优先使用 View Transitions API（原生），复杂场景用 Barba.js。

### 进阶模式（创造差异化的关键）

**F. 3D / WebGL 沉浸**
Three.js / React Three Fiber 是标准。关键是 3D + 好导航 + 好性能——只有 3D 但导航混乱或加载缓慢反而会降低体验。

**G. 微交互精通**
每个元素都有响应：悬停、按压、聚焦、状态变化。这不是锦上添花——它决定了网站是"精心设计的"还是"随便做的"。

**动画可中断原则：** 交互动画应优先使用 CSS transitions 或 GSAP `.to()` / `.fromTo()`，而不是 CSS keyframes。原因：transitions 会自动插值到最新状态，用户中途改变意图时动画能平滑响应；keyframes 跑在固定时间线上，一旦开始就无法重新定向。规则很简单：
- **交互类动画**（下拉菜单展开/收起、hover 状态、开关切换）→ transition
- **装饰类动画**（入场序列、背景循环、一次性展示动画）→ keyframe

**退出动画克制原则：** 退出动画的位移量应远小于入场动画。例如入场 `y: 40px`，退出只需 `y: -12px`。退出元素不需要和入场同等的运动量和注意力，过大的退出位移会让界面感觉「粗暴」。保留微小的方向性运动即可，完全不要退出动画反而会显得生硬。

**H. 实验性导航**
全屏沉浸式导航、游戏化导航、手势驱动导航。

> 详细实现代码参见 `references/interaction-patterns.md`。
> 动画配方和 GSAP 配方参见 `references/animation-patterns.md`。

---

## 性能约束（可用性的核心）

**为什么性能是设计问题而不是工程问题？** 因为在 Awwwards 的评分中，性能是 Usability（30%）的核心组成部分。一个好看但 5 秒加载的网站 = 一个好看但用户已经离开的网站。Lighthouse 90+ 是基准线，不是目标。

| 指标 | 目标 | 行业平均 |
|------|------|---------|
| LCP（最大内容绘制） | < 1.5s | 2.5–4s |
| CLS（累积布局偏移） | < 0.05 | 0.1–0.25 |
| INP（交互到绘制） | < 100ms | 200–500ms |
| 页面总大小 | < 3MB | 5–10MB |
| 动画帧率 | 60fps 持续 | 30–45fps |
| Lighthouse Mobile | 90+ 全项 | 50–70 |

**性能是设计约束，不是优化步骤：** 从设计阶段就要考虑——3D 场景是否可以懒加载？大图片是否可以渐进式加载？动画是否可以在低端设备上降级？

> 详细优化清单参见 `references/performance-guide.md`。

---

## 移动端优先

**为什么移动端重要？** Awwwards 评委在评审时首先检查移动端体验。桌面端精美但移动端崩坏的网站几乎不可能获得高评价。

- 移动端是独立的创意挑战，不是桌面版的缩小版
- 3D/WebGL 在移动端降级为 2D 替代效果
- 光标效果替换为触摸交互（tap/hold）
- 水平滚动在移动端变为垂直
- 动画数量减少，尊重 `prefers-reduced-motion`
- 触摸操作区域 >= 44px

### 可访问性

- `prefers-reduced-motion: reduce` 时禁用 WebGL/视差
- WebGL Canvas 添加 ARIA labels
- 语义化 HTML、键盘可导航
- 色彩对比度达标（WCAG AA）

---

## 技术栈参考

### 世界级技术栈分层

```
┌─ 展示层 ─────────────────────────────┐
│  Three.js / React Three Fiber (R3F)  │
│  GLSL Shaders / WebGPU               │
├─ 动画层 ─────────────────────────────┤
│  GSAP + ScrollTrigger                │
│  Lenis (平滑滚动)                    │
├─ 导航层 ─────────────────────────────┤
│  View Transitions API (优先)         │
│  Barba.js + GSAP (复杂场景)          │
├─ 框架层 ─────────────────────────────┤
│  Next.js (最常见) / Astro (快速崛起) │
│  Nuxt 3 / Webflow                    │
├─ 3D 资产管线 ───────────────────────┤
│  Blender / Houdini / ZBrush          │
│  Spline (无代码 3D)                  │
└─────────────────────────────────────┘
```

### Next.js 快速启动

> 完整的模板结构、Lenis + GSAP 集成、CSS 变量系统等，参见 `references/animation-patterns.md` 末尾的快速启动模板。

```tsx
// app/layout.tsx — 基础设置
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

export default function RootLayout({ children }) {
  return (
    <html lang="zh">
      <head>
        <link rel="preconnect" href="https://api.fontshare.com" />
      </head>
      <body style={{
        background: 'var(--c-bg)',
        color: 'var(--c-text)',
        fontFamily: 'var(--font-display)',
        WebkitFontSmoothing: 'antialiased',
      }}>
        {children}
      </body>
    </html>
  )
}
```

---

## 交付标准

SOTD 头奖级网站的交付不是「代码能跑」——是每个维度都达到专业基准。

### 输出物定义

最终交付物是一个完整的 Next.js 项目，包含以下必要组成部分：
- **设计系统实现**：CSS 变量系统（色彩、字体、间距、缓动曲线）作为全局配置
- **至少 1 个签名式交互**（Wow Moment）——这是区别"还不错"和"令人难忘"的关键
- **完整移动端适配**——独立设计而非桌面缩小版
- **加载体验**：预加载器 + 页面过渡，加载过程本身就是品牌叙事的一部分
- **全部 CSS 品质信号**：下方 checklist 中的每一项

以下品质线定义了「交付完成」——

### CSS 品质信号门槛

以下项目是「设计完成度」的零成本检验——缺失任何一个都会让网站看起来「没做完」：

- [ ] **自定义 `::selection` 选中色** — `background: var(--c-accent); color: var(--c-bg);`
- [ ] **自定义光标** — scripts/custom-cursor.js，含移动端触摸涟漪降级
- [ ] **隐藏系统光标** — 桌面端 `body { cursor: none; }`，配合自定义光标
- [ ] **字体抗锯齿** — `body { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }`
- [ ] **文字智能换行** — 标题 `text-wrap: balance`，段落 `text-wrap: pretty`
- [ ] **同心圆角** — 嵌套元素外层圆角 = 内层圆角 + padding
- [ ] **自定义滚动条** — `::-webkit-scrollbar` 样式与设计系统一致
- [ ] **平滑滚动** — 使用 Lenis 或 `scroll-behavior: smooth`
- [ ] **表单元素统一**（如含表单） — `::placeholder` 和 `:focus` 状态

### 性能门槛（硬性）

| 指标 | 交付标准 | 验证方式 |
|------|---------|---------|
| Lighthouse Mobile | Performance >= 90, 全项 >= 80 | Chrome DevTools Lighthouse |
| LCP | < 1.5s | Lighthouse |
| CLS | < 0.05 | Lighthouse |
| INP | < 100ms | Lighthouse |
| 页面总大小 | < 3MB | Network 面板 |
| 动画帧率 | 60fps（CPU throttling 4x） | DevTools Performance |
| 3D/WebGL | 中端设备不卡顿 | 真机测试 |

### 设计品质门槛

- [ ] 使用 quality-framework.md 四维自检框架逐项通过
- [ ] 通过 5 秒法则第一印象测试
- [ ] 零库存图片
- [ ] 所有交互元素都有自定义 hover/active/focus 状态
- [ ] 内页与首页设计系统一致
- [ ] 加载过程是品牌叙事
- [ ] 404/空状态/错误状态都有设计
- [ ] 每个动画都有独立的 easing 曲线
- [ ] 交互动画使用 transition（可中断），装饰动画才使用 keyframe
- [ ] 退出动画位移量远小于入场动画（如入场 40px → 退出 -12px）

### 移动端门槛

- [ ] 移动端是独立设计
- [ ] 触摸操作区域 >= 44px
- [ ] 3D/WebGL 有降级方案
- [ ] 光标效果替换为触摸反馈
- [ ] prefers-reduced-motion 下体验完整

### 可访问性门槛

- [ ] 语义化 HTML、键盘可导航
- [ ] 色彩对比度达标（WCAG AA）
- [ ] WebGL Canvas 有 ARIA labels

---

## 参考文件索引

根据当前需要读取对应文件。**不需要一次全部加载**——只在相关阶段读取相关文件：

| 文件 | 内容 | 何时读取 |
|------|------|---------|
| `references/quality-framework.md` | 四维自检框架、第一印象测试、常见陷阱、Ma/間 哲学、SOTD 差距诊断、设计陷阱识别 | 设计完成后自检时 |
| `references/design-process.md` | 完整设计流程、项目类型适配、设计决策框架 | 开始新项目时 |
| `references/visual-styles.md` | 8 种视觉风格完整定义、色彩系统、CSS 实现 | 确定设计方向时 |
| `references/typography-system.md` | 字体系统、Variable Fonts、配对方案、Kinetic Typography | 设计排版时 |
| `references/animation-patterns.md` | GSAP 配方、Lenis 集成、Intro 动画、ScrollTrigger、磁性按钮、文字揭示 | 实现动画时 |
| `references/webgl-patterns.md` | Three.js/R3F 模式、粒子、流体、Shader、性能优化 | 实现 3D 时 |
| `references/interaction-patterns.md` | 光标系统、微交互、导航模式、Wow Moment 设计模式 | 设计交互时 |
| `references/performance-guide.md` | Core Web Vitals 优化、懒加载、设备检测、打包策略 | 优化性能时 |
| `scripts/custom-cursor.js` | 自定义光标系统（CustomCursor 类） | 实现光标交互时 |
| `scripts/preloader.js` | 预加载器模式（计数器/遮罩/多步骤/文字拆分） | 实现加载动画时 |
| `scripts/magnetic-button.js` | 磁性按钮（MagneticElement 类 + GSAP 版） | 实现磁性交互时 |
| `scripts/performance-utils.js` | 防抖/节流、Intersection Observer、LazyWebGL、资源释放 | 性能优化时 |
