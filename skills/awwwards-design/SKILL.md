---
name: awwwards-design
description: "创建能在 Awwwards 获奖的设计级网站。当用户要求创建视觉震撼、沉浸式体验、获奖级别的网站、作品集、品牌展示页、产品落地页、创意代理网站，或任何追求极致视觉与交互体验的 web 项目时，必须使用此 skill。关键词触发：「Awwwards 级别」「沉浸式网站」「震撼视觉」「高端网站」「创意交互」「WebGL」「Scrollytelling」「获奖设计」「极致动效」「创意代理网站」「Site of the Day」「SOTD」「超酷网站」「逼格网站」「设计感网站」「3D 网站」「滚动动画」「叙事滚动」「品牌体验」「作品集」「Portfolio」。即使用户只说「帮我做个很酷的网站」「做个有设计感的页面」也应触发此 skill。"
---

# Awwwards 级别网站设计系统

此 skill 使你能够创建达到 Awwwards 获奖网站水准的 web 体验——视觉震撼、交互出众、性能卓越。它基于对 2024–2026 年度获奖网站的逆向工程研究，提炼出世界级设计的完整方法论。

---

## 设计质量优先级

世界级网站不是「每个方面都平均用力」，而是在正确的维度上做到极致。以下权重基于对数百个获奖网站的逆向工程——当你需要在设计决策中取舍时，用这个优先级指导投入：

| 维度 | 权重 | 核心关注 | 致命缺陷 |
|------|------|----------|----------|
| **Design 设计** | 40% | 视觉层次、字体品位、色彩克制、间距节奏、原创性 | 模板感、通用字体、素材库图片 |
| **Usability 可用性** | 30% | 导航直观、加载 <3s、移动端体验、Core Web Vitals | 移动端崩坏、5s+ 加载、导航混乱 |
| **Creativity 创意** | 20% | 一个签名式「Wow Moment」、交互创新、形式统一内容 | 抄袭模式、创意损害可用性 |
| **Content 内容** | 10% | 真实文案、品牌声音、原创媒体 | Lorem ipsum、机器翻译、素材图 |

> **为什么是这个权重？** 视觉 + 可用性 = 70%——好看又好用是基础。创意 20% 是让网站从「还不错」变成「令人难忘」的差异化因素。内容 10% 是最容易被忽视但能显著提升品质感的环节。

> 详细自检清单、第一印象测试、常见质量陷阱等，参见 `references/quality-framework.md`。

---

## 第一步：建立创意概念（代码之前必须完成）

世界级网站不是「炫技」——是「讲故事」。用户首先感知的是创意的独特性和执行的一致性。

### 三层定义框架

**1. 叙事核心（Narrative Core）**
这个网站在讲什么故事？用户从首屏到尾部的情感弧线是什么？
- 好例子：「速度作为一种美学」「从混沌走向秩序」「材质与光的对话」
- 坏例子：「展示我们的产品」「公司介绍」

**2. 视觉语言（Visual Language）**
从以下风格中选择一个并**坚定执行**。出色的核心不是风格多复杂，而是一种风格的执行深度：

| 风格 | 特征 | 代表案例 |
|------|------|---------|
| **新极简主义** | 超大字体 + 极端留白 + 2-3色克制 | Lando Norris SOTY 2025 |
| **有机感官** | 流体动画 + 噪点纹理 + 自然色调 | Immersive Garden |
| **数字朋克** | 高对比 + 故障美学 + 霓虹色 | Bruno Simon Portfolio |
| **Bento Grid** | 模块化网格 + 非对称变体 + 悬停动效 | Apple/Samsung 趋势 |
| **电影沉浸** | 全屏媒体 + 电影比例 + 暗色基底 | Igloo Inc SOTY 2024 |
| **反设计/粗野** | 原始边框 + 大面积色块 + 打破常规 | 2025-2026 新兴趋势 |
| **Y2K 复古** | 像素 + 霓虹 + 90年代怀旧 | 2026 回潮趋势 |
| **档案式排版** | 等宽字体 + 密集信息流 + 网格 | Developer 文档站 |

**3. 交互哲学（Interaction Philosophy）**
一句话定义交互行为：
- 「每次滚动揭开故事的下一页」（Scrollytelling）
- 「鼠标是这个世界的眼睛」（Cursor-driven）
- 「探索一个 3D 空间」（Spatial）
- 「内容像杂志一样翻阅」（Editorial）

> **关键原则**：最终交付必须在 4 个维度都达到高标准，而不只是视觉效果惊艳。一个好看但导航混乱、加载缓慢的网站不会给人留下好印象。

---

## 第二步：设计系统

### 排版系统

字体是顶级网站最重要的设计武器。2025-2026 的核心趋势是 **Variable Fonts**——单个字体文件支持连续 weight/width/slant 变化。

**字体选择规则：**

| 场景 | 推荐 | 禁止 |
|------|------|------|
| 展示字体 | PP Neue Montreal, Clash Display, Druk Wide, Syncopate, Bespoke Custom | Inter, Roboto, Arial, Poppins |
| 正文字体 | Satoshi, Suisse Int'l, Söhne, Freight Text | System-ui, sans-serif 默认 |
| 等宽/技术 | Space Mono, Geist Mono, JetBrains Mono | Courier New（除非档案风格） |
| 衬线体 | Instrument Serif, Freight Display, Canela | Times New Roman, Georgia（正文） |

**排版数值：**
- Hero 字号：`clamp(4rem, 12vw, 14rem)` — 字体即视觉锚点
- Hero 行高：`0.85–0.92` — 紧实感
- Hero 字间距：`-0.03em` 到 `-0.05em` — 大字号收紧
- 正文字号：`clamp(0.9rem, 1.2vw, 1.15rem)`
- 正文行高：`1.5–1.7`，最大宽度 `65ch`
- 标签/标注：`0.7rem`，`letter-spacing: 0.15em`，`text-transform: uppercase`

**Kinetic Typography（动态排版）** 是 2025 的核心趋势——文字随滚动/交互运动、变形、揭示。文字不仅是「阅读」的，它就是视觉设计本身。

详细字体系统、配对方案、CSS 实现参见 `references/typography-system.md`。

### 色彩系统

**核心规律：背景 + 文字 + 1个强调色 = 完整调色板。不超过 3 色。**

```css
/* 模式1：极端对比（最高获奖率） */
--c-bg: #0a0a0a;
--c-text: #f0ece4;
--c-accent: #ff3d00;  /* 一个鲜明强调色，仅用于关键元素 */

/* 模式2：暗调奢华 */
--c-bg: #111111;
--c-text: #e8e0d0;
--c-accent: #c9a96e;

/* 模式3：泥土有机（2026 新兴） */
--c-bg: #f5f0e8;
--c-text: #1a1208;
--c-accent: #8b6914;

/* 模式4：赛博霓虹 */
--c-bg: #050510;
--c-text: #e0e8ff;
--c-accent: #00ff88;
```

**色彩趋势要点：**
- 暗色模式是获奖默认选择（让 3D 和渐变更突出）
- Lando Norris SOTY 2025 仅用 2 色（主色 #D2FF00 电黄绿）
- Glow 效果（文字/按钮/3D 元素发光）是 2025 关键趋势
- 反设计趋势使用高饱和多色，但需要有意识的设计而非随意堆砌

### 动画缓动曲线

```javascript
const easings = {
  enter:    "cubic-bezier(0.16, 1, 0.3, 1)",    // Expo Out — 出现动画
  hover:    "cubic-bezier(0.34, 1.56, 0.64, 1)", // Back Out — 悬停微交互
  page:     "cubic-bezier(0.87, 0, 0.13, 1)",    // Expo InOut — 页面切换
  reveal:   "cubic-bezier(0.25, 1, 0.5, 1)",     // Quart Out — 揭示动画
  magnetic: "cubic-bezier(0.23, 1, 0.32, 1)",    // — 磁性按钮回弹
}
```

---

## 第三步：核心交互模式

### 必备模式（获奖标配）

**A. Scroll-Driven 叙事（Scrollytelling）**
这是 2024-2025 世界级网站的第一交互范式。用 GSAP ScrollTrigger + Lenis 实现。
- 文字逐行/逐词揭示
- 固定视差滚动叙事（pinned sections）
- 进度驱动的动画序列
- 水平滚动画廊嵌套在垂直流中

**B. 自定义光标**
顶级网站几乎都有自定义光标。它是最小投入、最大视觉回报的元素。
- 小圆点 + 大跟随圈的基础模式
- 悬停时变形（放大、改变形状）
- 磁性按钮（光标吸引效果）

**C. 页面加载动画（Preloader）**
预加载器是第一印象。世界级网站的预加载器是品牌介绍，不是等待转圈。
- 计数器式（0→100%）
- 品牌化遮罩退场
- 多步骤序列（加载 → Logo → 内容入场）

**D. 页面过渡**
使用 Barba.js + GSAP 消除页面间的白色闪烁。
- 离场动画（当前页淡出）
- 内容切换（DOM 无缝更新）
- 入场动画（新页渐入）

### 进阶模式（从「好看」到「令人难忘」）

**E. 3D / WebGL 沉浸**
Three.js / React Three Fiber 是标准。但关键不是「有 3D」而是 3D + 好导航 + 好性能。
- Igloo Inc 的核心理念：「将沉浸式 3D 体验与易于导航的滚动布局结合——极少有网站做到这一点」

**F. 微交互精通**
每个元素都有响应：悬停、按压、聚焦、状态变化。

**G. 实验性导航**
- 全屏沉浸式导航
- 游戏化导航
- 手势驱动导航

详细实现代码参见 `references/interaction-patterns.md`。

---

## 第四步：性能约束（不可妥协）

**这是 Usability 评分的核心。一个好看但 5 秒加载的网站不会获奖。**

| 指标 | 获奖目标 | 行业平均 |
|------|---------|---------|
| LCP（最大内容绘制） | < 1.5s | 2.5–4s |
| CLS（累积布局偏移） | < 0.05 | 0.1–0.25 |
| INP（交互到绘制） | < 100ms | 200–500ms |
| 页面总大小 | < 3MB | 5–10MB |
| 动画帧率 | 60fps 持续 | 30–45fps |
| Lighthouse Mobile | 90+ 全项 | 50–70 |

**性能策略：**
- 3D 场景：Intersection Observer 懒初始化，仅在可视时渲染
- 图片：AVIF > WebP > JPEG，blur placeholder，lazy loading
- 字体：WOFF2 自托管，`font-display: swap`，预加载关键字体，`unicode-range` 子集化
- CSS：`will-change` 声明，`contain: layout style`，使用 `transform` 而非 `left/top`
- JS：动态 import 重型库，`requestAnimationFrame` 代替 scroll 事件
- 设备检测：低端设备自动简化 3D/粒子效果

详细优化清单参见 `references/performance-guide.md`。

---

## 第五步：移动端与可访问性

### 移动端（任何真实用户都会用手机打开）

移动端不是桌面版的缩小版，而是独立的创意挑战：
- 3D/WebGL 在移动端降级为 2D 替代效果
- 光标效果替换为触摸交互（tap/hold）
- 水平滚动在移动端变为垂直
- 动画数量减少，尊重 `prefers-reduced-motion`
- 触摸操作区域 >= 44px
- 垂直滚动为主流

### 可访问性（评分权重在增加）

- `prefers-reduced-motion: reduce` 时禁用 WebGL/视差
- WebGL Canvas 添加 ARIA labels
- 语义化 HTML
- 键盘可导航
- 色彩对比度达标（WCAG AA）

---

## 第六步：绝对禁止清单

这些特征会让人立即识别为「AI 生成的网站」或「模板网站」：

| 禁止 | 为什么 |
|------|--------|
| 蓝白配色 + Inter 字体 | 最典型 AI 生成特征 |
| 紫色到蓝色渐变 hero | 被过度使用 |
| 三栏卡片 features section | 模板感极强 |
| Bootstrap / Tailwind 默认组件 | 评委一眼识别 |
| 通用素材图（Unsplash 等） | 内容评分直接扣分 |
| Lorem ipsum / 占位内容 | 内容评分一票否决 |
| 无故旋转/缩放的 3D 几何体 | 无意义的炫技 |
| 卡片 + 圆角 + 阴影的堆砌 | 缺乏设计意图 |
| 底部仅一行版权的 footer | 设计系统不完整 |

**应该使用：**
- 超大字体作为视觉锚点（不是图片）
- 有意义的留白（Ma/間 的哲学）
- 滚动驱动的内容揭示
- 非对称排版和布局
- 页面过渡动画
- 一个令人想截图的 Wow Moment

---

## 第七步：Wow Moment 设计

**一个签名式时刻是从「好看」到「令人难忘」的核心。** 世界级网站都有一个让用户停下来截图的瞬间。

Wow = 意外交互 × 情感共鸣 × 技术打磨

**实践模式：**
- **3D 游戏导航**（Bruno Simon — 开车穿过作品集）
- **产品互动乐园**（Lando Norris — WebGL 赛车体验）
- **叙事滚动**（Igloo Inc — 在 3D 世界中浏览项目）
- **数据 × 娱乐融合**（Shopify Live Globe — 全球销售数据 + 可玩弹球游戏）
- **微交互杰作**（Messenger — 每个悬停/滚动都展示个性）

关键：不是 20 个炫酷效果，而是 **1 个令人难忘的时刻**。

---

## 技术栈参考

### 世界级技术栈分层

```
┌─ 展示层 ─────────────────────────────┐
│  Three.js / React Three Fiber (R3F)  │
│  GLSL Shaders / WebGPU               │
├─ 动画层 ─────────────────────────────┤
│  GSAP + ScrollTrigger                │
│  Lenis (平滑滚动，已取代 Locomotive) │
├─ 导航层 ─────────────────────────────┤
│  Barba.js + GSAP (页面过渡)          │
│  View Transitions API (原生替代)     │
├─ 框架层 ─────────────────────────────┤
│  Next.js (最常见) / Webflow (已获SOTY)│
│  Astro (快速崛起) / Nuxt 3           │
├─ 3D 资产管线 ───────────────────────┤
│  Blender / Houdini / ZBrush          │
│  Spline (无代码 3D)                  │
└─────────────────────────────────────┘
```

### CDN 引用（单 HTML 文件场景）

```html
<!-- GSAP 3.12+ -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>

<!-- Lenis 平滑滚动 -->
<script src="https://unpkg.com/lenis@1.1.18/dist/lenis.min.js"></script>

<!-- Three.js -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<!-- Barba.js 页面过渡 -->
<script src="https://unpkg.com/@barba/core@2.9.7/dist/barba.umd.js"></script>

<!-- 字体 (Fontshare 免费高品质) -->
<link href="https://api.fontshare.com/v2/css?f[]=clash-display@700,600&display=swap" rel="stylesheet">
<link href="https://api.fontshare.com/v2/css?f[]=satoshi@700,500,400&display=swap" rel="stylesheet">
```

> Next.js 项目中使用 `npm install gsap @studio-freight/lenis three @barba/core`

---

## 参考文件索引

根据需要读取以下文件获取详细实现：

| 文件 | 内容 | 何时读取 |
|------|------|---------|
| `references/quality-framework.md` | 设计质量四维自检框架、第一印象测试、常见陷阱、Ma/間 哲学 | 设计完成后自检时 |
| `references/visual-styles.md` | 8 种视觉风格完整定义、色彩系统、CSS 实现 | 确定设计方向时 |
| `references/typography-system.md` | 字体系统、Variable Fonts、配对方案、Kinetic Typography | 设计排版时 |
| `references/animation-patterns.md` | GSAP 配方、Intro 动画、ScrollTrigger、磁性按钮、文字揭示 | 实现动画时 |
| `references/webgl-patterns.md` | Three.js/R3F 模式、粒子、流体、Shader、性能优化 | 实现 3D 时 |
| `references/interaction-patterns.md` | 光标、微交互、导航模式、Wow Moment 设计模式 | 设计交互时 |
| `references/performance-guide.md` | Core Web Vitals 优化、懒加载、设备检测、打包策略 | 优化性能时 |

---

## 快速启动：Next.js 模板结构

```tsx
// app/layout.tsx — 基础设置
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import Lenis from '@studio-freight/lenis'

gsap.registerPlugin(ScrollTrigger)

export default function RootLayout({ children }) {
  return (
    <html lang="zh">
      <head>
        <link rel="preconnect" href="https://api.fontshare.com" />
        {/* 字体预加载 */}
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

```tsx
// components/SmoothScroll.tsx — Lenis + GSAP 集成
useEffect(() => {
  const lenis = new Lenis({
    duration: 1.2,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    touchMultiplier: 2,
  })

  lenis.on('scroll', ScrollTrigger.update)
  gsap.ticker.add((time) => lenis.raf(time * 1000))
  gsap.ticker.lagSmoothing(0)

  return () => { lenis.destroy(); gsap.ticker.remove(lenis.raf) }
}, [])
```

```css
/* globals.css — 基础 CSS 变量系统 */
:root {
  --c-bg: #0a0a0a;
  --c-text: #f0ece4;
  --c-accent: #ff3d00;
  --font-display: 'Clash Display', sans-serif;
  --font-body: 'Satoshi', sans-serif;
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body { overflow-x: hidden; -webkit-font-smoothing: antialiased; }

/* 噪点质感（可选，增加设计感） */
body::after {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,...");
  opacity: 0.035;
  pointer-events: none;
  z-index: 9999;
}

/* 减少动效偏好 */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```
