# Awwwards 级别网站排版系统参考手册

> 基于数百个 Awwwards SOTD 头奖网站的排版分析，系统梳理字体选择、配对方案、Variable Fonts、Kinetic Typography 和 CSS 实现。

---

## 目录

1. [字体选择原则](#1-字体选择原则)
2. [推荐字体库与获取方式](#2-推荐字体库与获取方式)
3. [字体配对方案](#3-字体配对方案)
4. [排版数值系统](#4-排版数值系统)
5. [Variable Fonts（可变字体）](#5-variable-fonts可变字体)
6. [Kinetic Typography（动态排版）](#6-kinetic-typography动态排版)
7. [多语言与中文排版](#7-多语言与中文排版)
8. [字体加载性能优化](#8-字体加载性能优化)
9. [CSS 排版实现模板](#9-css-排版实现模板)

---

## 1. 字体选择原则

### 为什么字体是第一视觉锚点？

用户打开网站的 0.5 秒内，会通过字体判断这个网站是否"做过设计"。字体是唯一在页面加载之前就开始渲染的视觉元素——在图片加载完成之前，字体已经传递了品质信号。

### 避免使用的原因不是质量

Inter、Roboto、Arial、Poppins 本身质量很高，但它们的问题是**被过度使用到了丧失视觉个性的程度**。它们是系统默认字体和模板标配——当用户看到 Inter 时，潜意识反应是"这是模板"或"这是 AI 生成的"。

### 字体选择决策树

```
项目类型是什么？
├── 高端品牌 / 建筑事务所 → 选择衬线体或极简无衬线
├── 科技产品 / SaaS → 选择几何无衬线
├── 创意机构 / 设计工作室 → 选择实验性字体
├── 个人作品集 → 选择有个性的展示字体
├── 文化 / 编辑内容 → 选择衬线体或混合排版
└── 复古 / 街头品牌 → 选择特殊风格字体
```

### 字体分类与推荐

| 分类 | 推荐 | 特征 | 避免 |
|------|------|------|------|
| **展示字体（Display）** | PP Neue Montreal, Clash Display, Druk Wide, Syncopate, Instrument Serif | 强个性、大字号、用于标题 | Inter, Roboto, Arial, Poppins |
| **正文字体（Body）** | Satoshi, Suisse Int'l, Söhne, Freight Text, General Sans | 高可读性、小字号、用于段落 | System-ui, sans-serif 默认 |
| **等宽/技术（Mono）** | Space Mono, Geist Mono, JetBrains Mono, IBM Plex Mono | 等宽、代码感、用于技术元素 | Courier New（除非档案风格） |
| **衬线体（Serif）** | Instrument Serif, Freight Display, Canela, Playfair Display | 有装饰衬线、经典感、用于品牌 | Times New Roman（正文） |

---

## 2. 推荐字体库与获取方式

### 免费商业字体源

| 字体库 | 网址 | 特点 |
|--------|------|------|
| **Fontshare** (Indian Type Foundry) | fontshare.com | 高质量、免费商用、Awwwards 常见（Satoshi, Clash Display 等） |
| **Google Fonts** | fonts.google.com | 免费、CDN 加速、部分字体质量参差不齐 |
| **Fontesk** | fontesk.com | 精选免费字体合集 |
| **Open Foundry** | open-foundry.com | 开源专业字体 |

### Fontshare 核心 Awwwards 字体

```css
/* 在 HTML <head> 中预连接 */
<link rel="preconnect" href="https://api.fontshare.com" />

/* CSS @font-face */
@font-face {
  font-family: 'Satoshi';
  src: url('https://api.fontshare.com/v2/css?f[]=satoshi@1,2&display=swap')
       format('woff2');
  font-weight: 300 900;
  font-style: normal;
  font-display: swap;
}
```

> **为什么选择 Fontshare？** 因为它是 Awwwards 头奖网站中使用率最高的免费字体源。Satoshi、Clash Display、General Sans 都是 Awwwards 常客。质量不输商业字体，且免费商用。

---

## 3. 字体配对方案

字体配对的核心原则是**对比但有和谐**。展示字体和正文字体应该在风格上有明显差异（衬线 vs 无衬线、粗 vs 细、几何 vs 人文），但在视觉重量和 x-height 上保持协调。

### 经典配对方案

```css
/* 方案 1：现代极简（最常见于 Awwwards） */
--font-display: 'Clash Display', sans-serif;  /* 几何无衬线，粗犷有力 */
--font-body:    'Satoshi', sans-serif;         /* 人文无衬线，温暖可读 */

/* 方案 2：新经典主义（高端品牌） */
--font-display: 'Instrument Serif', serif;    /* 优雅衬线 */
--font-body:    'Satoshi', sans-serif;         /* 现代无衬线 */

/* 方案 3：科技先锋 */
--font-display: 'Syncopate', sans-serif;      /* 极窄、未来感 */
--font-body:    'Space Grotesk', sans-serif;   /* 几何、可读性好 */

/* 方案 4：人文温暖 */
--font-display: 'Freight Display', serif;     /* 经典衬线，高对比 */
--font-body:    'Freight Text', serif;         /* 同族衬线，阅读舒适 */

/* 方案 5：实验创意 */
--font-display: 'Druk Wide', sans-serif;      /* 超宽、冲击力强 */
--font-body:    'Suisse Int'l', sans-serif;   /* 极细、中性、不抢展示字体风头 */

/* 方案 6：档案技术 */
--font-display: 'JetBrains Mono', monospace;  /* 等宽，终端感 */
--font-body:    'Geist Sans', sans-serif;     /* 现代几何无衬线 */
```

### 配对经验法则

1. **x-height 接近**：两种字体在相同字号下看起来差不多大，避免正文字号看起来比标题还大。
2. **字重对比**：展示字体用 Black/ExtraBold (700-900)，正文字体用 Light/Regular (300-400)。
3. **风格互补**：不要选两种几何无衬线（如 Inter + Poppins），选衬线 + 无衬线或人文 + 几何。
4. **测试混排**：把两种字体放在一起看看是否协调——不协调的配对会让人感到"不对劲"但说不出为什么。

---

## 4. 排版数值系统

### 字号体系

```css
:root {
  /* ─── 展示字号（Hero 级） ─── */
  --fs-hero: clamp(4rem, 12vw, 14rem);       /* 巨型标题，字体即视觉锚点 */
  --fs-h1:   clamp(2.5rem, 6vw, 6rem);        /* 一级标题 */
  --fs-h2:   clamp(1.5rem, 3vw, 3rem);        /* 二级标题 */
  --fs-h3:   clamp(1.25rem, 2vw, 1.5rem);     /* 三级标题 */

  /* ─── 正文字号 ─── */
  --fs-body:   clamp(0.9rem, 1.2vw, 1.15rem);  /* 正文 */
  --fs-body-lg: clamp(1rem, 1.3vw, 1.25rem);   /* 大号正文 */

  /* ─── 辅助字号 ─── */
  --fs-caption: clamp(0.7rem, 0.8vw, 0.75rem);  /* 标注/说明 */
  --fs-small:   clamp(0.625rem, 0.7vw, 0.7rem); /* 最小辅助文字 */
}
```

### 行高体系

```css
:root {
  --lh-hero:     0.85 – 0.92;   /* Hero 紧实感，视觉冲击 */
  --lh-heading:  1.0 – 1.1;     /* 标题紧凑 */
  --lh-body:     1.5 – 1.7;     /* 正文舒适阅读 */
  --lh-compact:  1.2;           /* 数据密集/标签 */
}
```

### 字间距体系

```css
:root {
  --ls-hero:    -0.03em to -0.05em;  /* 大号标题收紧，消除视觉空洞 */
  --ls-h1:      -0.02em to -0.03em;  /* 一级标题微紧 */
  --ls-body:    0;                    /* 正文正常 */
  --ls-caption: 0.1em to 0.15em;     /* 标注/说明加宽 + 大写化 */
  --ls-tag:     0.15em;               /* 标签/徽章加宽 */
}
```

### 段落宽度

```css
/* 正文最佳阅读宽度 */
p, .prose {
  max-width: 65ch;     /* 约 65 个字符 */
  min-width: 40ch;     /* 避免过窄 */
}
```

### 排版节奏法则

```
┌──────────────────────────────┐
│  Hero: 14rem, lh 0.85       │ ← 视觉爆炸
│  ↓ 巨大落差 ↓                 │
│  H2:   3rem, lh 1.05         │ ← 章节转折
│  ↓ 大落差 ↓                   │
│  Body: 1.15rem, lh 1.6       │ ← 阅读舒适
│  ↓ 小落差 ↓                   │
│  Caption: 0.75rem, ls 0.15em  │ ← 精致细节
└──────────────────────────────┘

节奏变化 = 视觉层次。如果所有字号差不多大，用户无法判断信息优先级。
```

---

## 5. Variable Fonts（可变字体）

### 为什么使用可变字体？

可变字体（Variable Fonts）将同一字族的所有字重（300-900）打包在 **一个文件** 中。相比为每个字重提供单独文件，可变字体节省了 HTTP 请求数和总体积。

| 对比项 | 固定字重（6 个文件） | 可变字体（1 个文件） |
|--------|---------------------|---------------------|
| 文件数 | 6 个 | 1 个 |
| 总大小 | ~120KB | ~80KB |
| HTTP 请求 | 6 次 | 1 次 |
| 字重精度 | 400, 500, 700 等固定值 | 300-900 之间任意值 |

### CSS 使用

```css
@font-face {
  font-family: 'Satoshi';
  src: url('/fonts/satoshi-variable.woff2') format('woff2') tech('variations');
  font-weight: 300 900;           /* 所有字重 */
  font-style: oblique 0deg 12deg; /* 可变斜体 */
  font-display: swap;
}

/* 使用时直接指定任意字重 */
.hero-title { font-weight: 750; }   /* 比标准 700 更粗 */
.body-text  { font-weight: 350; }   /* 比标准 300 更粗 */
```

### Awwwards 常用可变字体

| 字体 | 字重范围 | 特点 |
|------|---------|------|
| Satoshi | 300-900 | Fontshare 旗舰，Awwwards 使用率最高 |
| Clash Display | 300-700 | 几何无衬线，适合标题 |
| General Sans | 300 700 | 万能型，标题正文通吃 |
| Fraunces | 100-900 | 衬线+无衬线混合，情感丰富 |
| Space Grotesk | 300-700 | 科技感，几何感强 |

---

## 6. Kinetic Typography（动态排版）

### 什么是动态排版？

动态排版（Kinetic Typography）是当前 Awwwards 的核心趋势——**文字不只是被阅读的，它本身就是视觉设计**。文字随滚动、交互、时间运动、变形、揭示，创造超越静态排版的视觉体验。

### 为什么动态排版重要？

Awwwards 2024-2026 头奖网站中，**几乎每一个 SOTD 网站都使用了某种形式的动态排版**。它比 3D/WebGL 更轻量、比图片加载更快、比视频更灵活——是性价比最高的视觉差异化手段。

### 核心模式

#### 6.1 文字逐字揭示（Character Reveal）

最常见的动态排版模式。文字从底部滑入，每个字符有微小的延迟（stagger）。

```css
.char {
  display: inline-block;
  overflow: hidden;
}

.char-inner {
  display: inline-block;
  transform: translateY(110%);
  transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.is-visible .char-inner {
  transform: translateY(0);
}
```

```js
// GSAP 实现（性能更优）
gsap.from('.hero-title .char', {
  y: 120,
  rotateX: -80,
  opacity: 0,
  stagger: 0.03,
  duration: 0.8,
  ease: 'power3.out',
  scrollTrigger: {
    trigger: '.hero-title',
    start: 'top 85%',
    once: true,
  },
});
```

#### 6.2 逐词揭示（Word-by-Word Reveal）

```css
.word {
  display: inline-block;
  overflow: hidden;
  vertical-align: bottom;
}

.word-inner {
  display: inline-block;
  transform: translateY(120%);
}
```

> 完整 GSAP 实现参见 `references/animation-patterns.md` 配方 1。

#### 6.3 行级揭示（Line Reveal）

将文字按自然换行分割为行，每行整体滑入。

```css
.line {
  display: block;
  overflow: hidden;
}

.line-inner {
  display: block;
  transform: translateY(105%);
}
```

> 完整 GSAP 实现参见 `references/animation-patterns.md` 配方 2。

#### 6.4 跑马灯文字（Marquee）

连续滚动的大号文字，营造品牌氛围和能量感。

```css
.marquee {
  overflow: hidden;
  white-space: nowrap;
}

.marquee__track {
  display: inline-block;
  animation: marquee-scroll 20s linear infinite;
}

@keyframes marquee-scroll {
  from { transform: translateX(0); }
  to   { transform: translateX(-50%); }
}
```

> 注意：内容需重复一份以实现无缝循环。

#### 6.5 混合模式文字（Blend Mode）

文字与背景图片/视频通过 `mix-blend-mode` 产生交互效果。

```css
.blend-text {
  font-size: clamp(4rem, 10vw, 8rem);
  font-weight: 900;
  mix-blend-mode: difference;  /* 最常用：自动适配亮/暗背景 */
  color: #fff;
}

/* 或与图片层叠 */
.blend-section {
  position: relative;
}

.blend-section .text {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  mix-blend-mode: exclusion;  /* 图片上方文字产生色彩反转效果 */
}
```

#### 6.6 文字变形（Morphing）

通过 SVG 滤镜或 CSS `clip-path` 让文字形状变化。

```css
/* 文字在滚动过程中从圆形变为矩形 */
.morph-text {
  clip-path: circle(50% at 50% 50%);
  transition: clip-path 1s cubic-bezier(0.16, 1, 0.3, 1);
}

.morph-text.is-visible {
  clip-path: inset(0 0 0 0);
}
```

### 动态排版性能注意事项

| 技术 | 性能影响 | 建议 |
|------|---------|------|
| CSS `transition` | 低 | 简单入场动画首选 |
| GSAP `from`/`to` | 低 | 复杂序列推荐 |
| Web Animations API | 低 | 原生方案 |
| SVG `<animate>` | 中 | 形状变形可用 |
| Canvas 2D | 中 | 大量文字渲染 |
| WebGL/Canvas 文字纹理 | 高 | 仅用于极端效果 |

**核心原则：动态排版只动 `transform` 和 `opacity`，不动 `width`/`height`/`top`/`left`。**

---

## 7. 多语言与中文排版

### 中文字体推荐

| 用途 | 推荐 | 避免 |
|------|------|------|
| 展示字体 | 思源黑体 (Noto Sans SC), 霞鹜文楷 (LXGW WenKai), 小赖字体 | 系统默认宋体, 微软雅黑（模板感） |
| 正文字体 | 思源黑体, 霞鹜文楷 | 华文楷体, 黑体（默认） |
| 英文搭配 | Satoshi, Clash Display, Space Grotesk | — |

### 中文排版特殊处理

```css
/* 中文不需要 letter-spacing，但英文混排需要 */
html:lang(zh) {
  font-family: 'Noto Sans SC', sans-serif;
  letter-spacing: 0;
}

html:lang(en) {
  font-family: 'Satoshi', sans-serif;
  letter-spacing: -0.01em;
}

/* 中英文混排间距 */
.zh-en-mix {
  text-autospace: ideograph-alpha;  /* 自动在中英文间添加间距 */
}
```

### 中文字号调整

中文排版需要比英文稍大 10-15% 的字号以达到相同的视觉重量感：

```css
:root {
  --fs-hero-zh: clamp(3rem, 10vw, 12rem);      /* 中文 Hero 比英文略小 */
  --fs-body-zh: clamp(1rem, 1.3vw, 1.25rem);    /* 中文正文比英文略大 */
}
```

---

## 8. 字体加载性能优化

### font-display: swap

```css
@font-face {
  font-family: 'Satoshi';
  font-display: swap;  /* 先显示 fallback，加载完替换 */
}
```

> `swap` 是 Awwwards 网站的标准选择。避免 `block`（会阻塞渲染导致白屏）和 `optional`（可能永远不加载字体）。

### Preload 关键字体

```html
<!-- 仅预加载首屏 LCP 元素所用的 1-2 个字体文件 -->
<link rel="preload" as="font" href="/fonts/clash-display.woff2"
      type="font/woff2" crossorigin="anonymous">
```

### 字体度量校准（消除 CLS）

```css
@font-face {
  font-family: 'Clash Display';
  src: url('/fonts/clash-display.woff2') format('woff2');
  font-weight: 700;
  font-display: swap;
  /* 校正 fallback 字体的度量差异，消除字体切换时的布局偏移 */
  size-adjust: 108%;
  ascent-override: 85%;
  descent-override: 20%;
  line-gap-override: 0%;
}
```

> 使用 [font-style-matcher](https://meowni.ca/font-style-matcher/) 工具获取精确数值。

### 字体子集化

```css
@font-face {
  font-family: 'Display';
  src: url('/fonts/display-latin.woff2') format('woff2');
  /* 仅加载拉丁字符，大幅减少文件体积 */
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC,
    U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193;
}
```

> 中文字体文件通常很大（5-20MB），必须使用 unicode-range 子集化或使用可变字体。

---

## 9. CSS 排版实现模板

### 完整排版变量系统

```css
:root {
  /* ─── 字体 ─── */
  --font-display: 'Clash Display', sans-serif;
  --font-body:    'Satoshi', sans-serif;
  --font-mono:    'Space Mono', monospace;

  /* ─── 字号（流式缩放） ─── */
  --fs-hero:    clamp(4rem, 12vw, 14rem);
  --fs-h1:      clamp(2.5rem, 6vw, 6rem);
  --fs-h2:      clamp(1.5rem, 3vw, 3rem);
  --fs-h3:      clamp(1.25rem, 2vw, 1.5rem);
  --fs-body:    clamp(0.9rem, 1.2vw, 1.15rem);
  --fs-body-lg: clamp(1rem, 1.3vw, 1.25rem);
  --fs-caption: clamp(0.7rem, 0.8vw, 0.75rem);
  --fs-small:   clamp(0.625rem, 0.7vw, 0.7rem);

  /* ─── 字重 ─── */
  --fw-display: 700;
  --fw-body:    400;
  --fw-light:   300;
  --fw-bold:    700;

  /* ─── 行高 ─── */
  --lh-hero:    0.88;
  --lh-heading: 1.05;
  --lh-body:    1.6;
  --lh-compact: 1.2;

  /* ─── 字间距 ─── */
  --ls-hero:    -0.04em;
  --ls-h1:      -0.03em;
  --ls-body:    0;
  --ls-caption: 0.12em;
  --ls-tag:     0.15em;

  /* ─── 文本颜色 ─── */
  --c-text:       #f0ece4;
  --c-text-muted: #999;
  --c-heading:    var(--c-text);
}
```

### 基础排版类

```css
body {
  font-family: var(--font-body);
  font-size: var(--fs-body);
  font-weight: var(--fw-body);
  line-height: var(--lh-body);
  color: var(--c-text);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}

h1, .h1 {
  font-family: var(--font-display);
  font-size: var(--fs-h1);
  font-weight: var(--fw-display);
  line-height: var(--lh-heading);
  letter-spacing: var(--ls-h1);
}

.hero-title {
  font-family: var(--font-display);
  font-size: var(--fs-hero);
  font-weight: var(--fw-display);
  line-height: var(--lh-hero);
  letter-spacing: var(--ls-hero);
}

.caption, .label {
  font-size: var(--fs-caption);
  letter-spacing: var(--ls-caption);
  text-transform: uppercase;
  font-weight: 500;
}

.tag {
  font-size: var(--fs-small);
  letter-spacing: var(--ls-tag);
  text-transform: uppercase;
}

.prose {
  max-width: 65ch;
  font-size: var(--fs-body-lg);
  line-height: var(--lh-body);
}

/* 等宽/代码 */
code, .mono {
  font-family: var(--font-mono);
  font-size: 0.9em;
}

/* 超大段落标题（装饰性） */
.display-text {
  font-family: var(--font-display);
  font-size: var(--fs-hero);
  font-weight: var(--fw-display);
  line-height: var(--lh-hero);
  letter-spacing: var(--ls-hero);
  max-width: 20ch;     /* 限制每行字数，增强排版节奏 */
}
```

### 文字截断与省略

```css
.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  overflow: hidden;
}
```

---

> **参考资源**
> - [Fontshare](https://fontshare.com/) — Awwwards 常用免费字体
> - [Google Fonts](https://fonts.google.com/) — 最大免费字体库
> - [font-style-matcher](https://meowni.ca/font-style-matcher/) — 字体度量校准工具
> - [Web Typography](https://web.dev/learn/css/web-typography/) — MDN 网页排版指南
> - [Variable Fonts Guide](https://web.dev/variable-fonts/) — 可变字体完整教程
