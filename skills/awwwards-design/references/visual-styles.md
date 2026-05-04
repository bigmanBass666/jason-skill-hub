# Awwwards SOTD 头奖网站视觉风格参考手册

> 本文档系统梳理 8 种主流 Awwwards 头奖视觉风格，涵盖设计哲学、配色方案、排版策略及完整 CSS 实现。
> 最后更新：2025 年 7 月

---

## 目录

1. [新极简主义 Neo-Minimalism](#1-新极简主义-neo-minimalism)
2. [有机感官 Organic Sensory](#2-有机感官-organic-sensory)
3. [数字朋克 Digital Punk](#3-数字朋克-digital-punk)
4. [Bento Grid](#4-bento-grid)
5. [电影沉浸 Cinematic Immersion](#5-电影沉浸-cinematic-immersion)
6. [反设计/粗野 Anti-Design / Brutalism](#6-反设计粗野-anti-design--brutalism)
7. [Y2K 复古 Y2K Retro](#7-y2k-复古-y2k-retro)
8. [档案式排版 Archival Typography](#8-档案式排版-archival-typography)

---

## 1. 新极简主义 Neo-Minimalism

### 设计哲学

**"少即是多" 的终极表达。** 受 2025 年 Lando Norris SOTY（Site of the Year）头奖网站启发，新极简主义将信息压缩到极致——
一张全屏字体、一根细线、一个微妙的色彩偏移，便足以构成完整的叙事体验。

**适用场景：** 个人作品集、高端品牌官网、设计工作室、建筑事务所、奢侈品品牌。

**核心理念：**
- 极端留白（70%+ 页面为空白）
- 排版即设计（字体尺寸成为唯一的视觉层级手段）
- 微交互替代装饰元素
- 克制的色彩——近乎单色，偶尔用一个亮色作为"签名"

### 配色方案

```css
:root {
  /* Lando Norris SOTD 风格 */
  --nm-bg:           #F5F2EB;   /* 温暖的米白 */
  --nm-fg:           #1A1A1A;   /* 近似纯黑 */
  --nm-accent:       #E63312;   /* 唯一的亮色：赛车红 */
  --nm-muted:        #9C9C9C;   /* 中性灰，用于辅助文字 */
  --nm-border:       rgba(26, 26, 26, 0.08);
  --nm-gutter:       clamp(20px, 5vw, 80px);  /* 响应式间距 */
}
```

### 排版策略

```css
/* 新极简主义的排版：极端尺寸对比 */
:root {
  --nm-font-display: 'Clash Display', 'Helvetica Neue', sans-serif;
  --nm-font-body:    'Satoshi', sans-serif;

  /* 字号使用 clamp() 实现流式缩放 */
  --nm-size-hero:    clamp(4rem, 12vw, 14rem);    /* 主标题：巨大 */
  --nm-size-h1:      clamp(2.5rem, 6vw, 6rem);
  --nm-size-h2:      clamp(1.5rem, 3vw, 3rem);
  --nm-size-body:    clamp(0.875rem, 1.2vw, 1.125rem);
  --nm-size-caption: clamp(0.625rem, 0.8vw, 0.75rem);

  --nm-weight-display: 700;
  --nm-weight-body:    300;
  --nm-tracking:       -0.03em;    /* 紧凑字距 */
  --nm-leading:        1.1;        /* 紧凑行高 */
}
```

### 关键 CSS 实现

```css
/* === 新极简主义基础 === */
.neo-minimal {
  background-color: var(--nm-bg);
  color: var(--nm-fg);
  font-family: var(--nm-font-body);
  font-weight: var(--nm-weight-body);
  font-size: var(--nm-size-body);
  line-height: var(--nm-leading);
  letter-spacing: var(--nm-tracking);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* 全屏排版区块 —— 页面就是一块"海报" */
.nm-hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding: var(--nm-gutter);
}

.nm-hero-title {
  font-family: var(--nm-font-display);
  font-size: var(--nm-size-hero);
  font-weight: var(--nm-weight-display);
  line-height: 0.9;
  letter-spacing: -0.05em;
  max-width: 20ch;          /* 限制每行字数，增强排版节奏 */
}

/* 克制的分隔线 */
.nm-divider {
  width: 100%;
  height: 1px;
  background: var(--nm-border);
  border: none;
}

/* 导航：极简到极致 */
.nm-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--nm-gutter);
  z-index: 100;
  mix-blend-mode: difference; /* 自动适配亮/暗背景 */
}

.nm-nav a {
  font-size: var(--nm-size-caption);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  text-decoration: none;
  color: var(--nm-fg);
  position: relative;
}

.nm-nav a::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 1px;
  background: var(--nm-accent);
  transition: width 0.4s cubic-bezier(0.22, 1, 0.36, 1);
}

.nm-nav a:hover::after {
  width: 100%;
}

/* 悬停效果：仅用颜色偏移 */
.nm-hover-reveal {
  position: relative;
  overflow: hidden;
  cursor: pointer;
}

.nm-hover-reveal .hover-text {
  transition: transform 0.5s cubic-bezier(0.22, 1, 0.36, 1);
}

.nm-hover-reveal .hover-accent {
  position: absolute;
  top: 0;
  left: 0;
  color: var(--nm-accent);
  transform: translateY(100%);
  transition: transform 0.5s cubic-bezier(0.22, 1, 0.36, 1);
}

.nm-hover-reveal:hover .hover-text {
  transform: translateY(-100%);
}

.nm-hover-reveal:hover .hover-accent {
  transform: translateY(0);
}
```

### 代表作品

| 网站 | 年份 | 特点 |
|------|------|------|
| landonorris.com (SOTY 2025) | 2025 | 极端字体层级、单色+赛车红 |
| manvsMachine.design | 2024 | 黑白对比、精密网格 |
| noelshiro.com | 2023 | 巨型排版、零装饰 |

---

## 2. 有机感官 Organic Sensory

### 设计哲学

**"让页面呼吸。"** 受 Immersive Garden 等工作室影响，有机感官风格追求自然、流动、触感化的视觉体验。
页面元素如同液态般流动，背景带有细腻的噪点纹理，色彩取自自然——泥土、苔藓、海水。

**适用场景：** 环保品牌、健康/养生、自然主题、艺术展览、科技公司的"人性化"页面。

**核心理念：**
- 拒绝硬边矩形，拥抱曲线和不规则形状
- 噪点纹理（Grain）增加触感真实度
- 缓动动画模拟自然运动（使用 cubic-bezier 或 spring 物理引擎）
- 色彩低饱和、偏暖、有机

### 配色方案

```css
:root {
  /* Immersive Garden 自然色系 */
  --os-bg:           #EDE8E0;   /* 亚麻白 */
  --os-fg:           #2C2A26;   /* 深棕黑 */
  --os-accent:       #8B6F47;   /* 焦糖棕 */
  --os-secondary:    #6B8F71;   /* 苔藓绿 */
  --os-tertiary:     #C4A882;   /* 沙色 */
  --os-surface:      rgba(237, 232, 224, 0.6);
  --os-noise-opacity: 0.04;     /* 噪点叠加透明度 */
}
```

### 排版策略

```css
:root {
  --os-font-display: 'Playfair Display', 'Georgia', serif;
  --os-font-body:    'DM Sans', 'Helvetica Neue', sans-serif;

  --os-size-hero:    clamp(3rem, 8vw, 9rem);
  --os-size-h1:      clamp(2rem, 5vw, 5rem);
  --os-size-body:    clamp(1rem, 1.3vw, 1.25rem);

  --os-weight-display: 400;     /* 衬线体用常规而非粗体 */
  --os-weight-body:    400;
  --os-tracking:       0.01em;
  --os-leading:        1.6;     /* 宽松行高，增加呼吸感 */
}
```

### 关键 CSS 实现

```css
/* === SVG 噪点纹理叠加（全局） === */
.organic-sensory {
  position: relative;
}

.organic-sensory::before {
  content: '';
  position: fixed;
  inset: 0;
  z-index: 9999;
  pointer-events: none;
  opacity: var(--os-noise-opacity);
  /* 内联 SVG 噪点，无需外部图片 */
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-repeat: repeat;
  background-size: 256px 256px;
}

/* === Blob 有机形状 === */
.os-blob {
  border-radius: 60% 40% 50% 70% / 50% 60% 40% 50%;
  background: linear-gradient(
    135deg,
    var(--os-secondary) 0%,
    var(--os-accent) 100%
  );
  animation: blob-morph 8s ease-in-out infinite;
  filter: blur(40px);
}

@keyframes blob-morph {
  0%, 100% {
    border-radius: 60% 40% 50% 70% / 50% 60% 40% 50%;
    transform: rotate(0deg) scale(1);
  }
  33% {
    border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%;
    transform: rotate(120deg) scale(1.05);
  }
  66% {
    border-radius: 50% 60% 30% 60% / 30% 50% 70% 40%;
    transform: rotate(240deg) scale(0.95);
  }
}

/* === 有机容器圆角 === */
.os-card {
  background: var(--os-surface);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(44, 42, 38, 0.06);
  border-radius: 24px;
  padding: clamp(24px, 4vw, 48px);
  transition: transform 0.6s cubic-bezier(0.22, 1, 0.36, 1),
              box-shadow 0.6s cubic-bezier(0.22, 1, 0.36, 1);
}

.os-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 60px rgba(44, 42, 38, 0.08);
}

/* === 文字渐入动画（模拟"浮现"感） === */
.os-fade-up {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.8s ease-out,
              transform 0.8s cubic-bezier(0.22, 1, 0.36, 1);
}

.os-fade-up.is-visible {
  opacity: 1;
  transform: translateY(0);
}

/* === 自然色调渐变背景 === */
.os-gradient-bg {
  background:
    radial-gradient(ellipse at 20% 50%, rgba(107, 143, 113, 0.15) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 20%, rgba(139, 111, 71, 0.1) 0%, transparent 50%),
    radial-gradient(ellipse at 60% 80%, rgba(196, 168, 130, 0.12) 0%, transparent 50%),
    var(--os-bg);
}

/* === 有机分割线（SVG 曲线） === */
.os-wave-divider {
  width: 100%;
  height: 80px;
  background: transparent;
}

.os-wave-divider svg {
  width: 100%;
  height: 100%;
}
/* 使用内联 SVG path 实现波浪分割线 */
```

```html
<!-- 有机波浪分割线示例 -->
<div class="os-wave-divider">
  <svg viewBox="0 0 1440 80" preserveAspectRatio="none">
    <path d="M0,40 C360,80 720,0 1080,40 C1260,60 1380,50 1440,40 L1440,80 L0,80 Z"
          fill="var(--os-bg)"/>
  </svg>
</div>
```

### 代表作品

| 网站 | 年份 | 特点 |
|------|------|------|
| immersive-garden.com | 2024 | 噪点纹理、有机形态、滚动叙事 |
| ecoage.com | 2023 | 自然色调、blob 背景 |
| papergames.fr | 2024 | 手绘质感、柔和曲线 |

---

## 3. 数字朋克 Digital Punk

### 设计哲学

**"故障即美学。"** 受 Bruno Simon（Three.js 赛车游戏网站）等前卫开发者影响，数字朋克风格将数字世界的"错误"
转化为艺术——故障纹理（Glitch）、扫描线、CRT 效果、高对比度霓虹色、像素失真。这是赛博朋克在网页设计中的延续。

**适用场景：** 游戏工作室、音乐/电子音乐、地下文化品牌、Web3/Crypto 项目、黑客主题。

**核心理念：**
- 高对比度是底线
- 故障效果不是 Bug，是 Feature
- 霓虹色（Cyan / Magenta / Lime）在暗底上发光
- 3D 交互是标配（Three.js / WebGL）
- 打破常规——文字可以倒置、颜色可以错位

### 配色方案

```css
:root {
  /* Bruno Simon 赛博朋克风 */
  --dp-bg:           #0A0A0F;   /* 深空黑 */
  --dp-fg:           #E0E0E0;   /* 冷白 */
  --dp-neon-cyan:    #00F0FF;   /* 霓虹青 */
  --dp-neon-magenta: #FF00E5;   /* 霓虹品红 */
  --dp-neon-lime:    #B8FF00;   /* 霓虹酸绿 */
  --dp-neon-red:     #FF2244;   /* 警告红 */
  --dp-grid:         rgba(0, 240, 255, 0.05);
  --dp-scanline:     rgba(0, 0, 0, 0.15);
}
```

### 排版策略

```css
:root {
  --dp-font-display: 'Space Mono', 'Courier New', monospace;
  --dp-font-body:    'Satoshi', 'Helvetica Neue', sans-serif;

  --dp-size-hero:    clamp(3rem, 10vw, 10rem);
  --dp-size-body:    clamp(0.875rem, 1.1vw, 1rem);

  --dp-weight-display: 700;
  --dp-tracking-glitch: 0.05em;
  --dp-leading:        1.0;     /* 超紧凑行高 */
}
```

### 关键 CSS 实现

```css
/* === Glitch 文字效果 === */
.dp-glitch {
  position: relative;
  font-family: var(--dp-font-display);
  font-size: var(--dp-size-hero);
  color: var(--dp-fg);
  text-transform: uppercase;
}

.dp-glitch::before,
.dp-glitch::after {
  content: attr(data-text);
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.dp-glitch::before {
  color: var(--dp-neon-cyan);
  animation: glitch-1 3s infinite linear alternate-reverse;
  clip-path: polygon(0 0, 100% 0, 100% 45%, 0 45%);
  transform: translate(-2px, -1px);
}

.dp-glitch::after {
  color: var(--dp-neon-magenta);
  animation: glitch-2 2s infinite linear alternate-reverse;
  clip-path: polygon(0 60%, 100% 60%, 100% 100%, 0 100%);
  transform: translate(2px, 1px);
}

@keyframes glitch-1 {
  0%   { clip-path: polygon(0 0, 100% 0, 100% 45%, 0 45%); }
  20%  { clip-path: polygon(0 15%, 100% 15%, 100% 50%, 0 50%); }
  40%  { clip-path: polygon(0 35%, 100% 35%, 100% 60%, 0 60%); }
  60%  { clip-path: polygon(0 5%, 100% 5%, 100% 40%, 0 40%); }
  80%  { clip-path: polygon(0 25%, 100% 25%, 100% 55%, 0 55%); }
  100% { clip-path: polygon(0 45%, 100% 45%, 100% 70%, 0 70%); }
}

@keyframes glitch-2 {
  0%   { clip-path: polygon(0 55%, 100% 55%, 100% 100%, 0 100%); }
  20%  { clip-path: polygon(0 60%, 100% 60%, 100% 90%, 0 90%); }
  40%  { clip-path: polygon(0 65%, 100% 65%, 100% 95%, 0 95%); }
  60%  { clip-path: polygon(0 50%, 100% 50%, 100% 85%, 0 85%); }
  80%  { clip-path: polygon(0 70%, 100% 70%, 100% 100%, 0 100%); }
  100% { clip-path: polygon(0 58%, 100% 58%, 100% 92%, 0 92%); }
}

/* === CRT 扫描线效果 === */
.dp-scanlines::after {
  content: '';
  position: fixed;
  inset: 0;
  z-index: 9998;
  pointer-events: none;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    var(--dp-scanline) 2px,
    var(--dp-scanline) 4px
  );
}

/* === CRT 屏幕曲面 + 色差 === */
.dp-crt {
  border-radius: 12px;
  overflow: hidden;
  box-shadow:
    0 0 40px rgba(0, 240, 255, 0.1),
    inset 0 0 80px rgba(0, 0, 0, 0.4);
  position: relative;
}

.dp-crt::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    rgba(0, 240, 255, 0.03),
    rgba(255, 0, 229, 0.03)
  );
  mix-blend-mode: screen;
  pointer-events: none;
}

/* === 霓虹发光按钮 === */
.dp-neon-btn {
  font-family: var(--dp-font-display);
  font-size: var(--dp-size-body);
  text-transform: uppercase;
  letter-spacing: 0.15em;
  padding: 16px 40px;
  background: transparent;
  border: 2px solid var(--dp-neon-cyan);
  color: var(--dp-neon-cyan);
  cursor: pointer;
  position: relative;
  transition: all 0.3s ease;
}

.dp-neon-btn:hover {
  background: var(--dp-neon-cyan);
  color: var(--dp-bg);
  box-shadow:
    0 0 10px var(--dp-neon-cyan),
    0 0 40px rgba(0, 240, 255, 0.3),
    0 0 80px rgba(0, 240, 255, 0.1);
  text-shadow: 0 0 5px var(--dp-bg);
}

/* === 网格透视背景 === */
.dp-grid-bg {
  background-color: var(--dp-bg);
  background-image:
    linear-gradient(var(--dp-grid) 1px, transparent 1px),
    linear-gradient(90deg, var(--dp-grid) 1px, transparent 1px);
  background-size: 60px 60px;
  perspective: 500px;
}

/* === 文字 RGB 错位 Hover === */
.dp-rgb-hover {
  position: relative;
  transition: text-shadow 0.3s ease;
}

.dp-rgb-hover:hover {
  text-shadow:
    -3px 0 var(--dp-neon-cyan),
    3px 0 var(--dp-neon-magenta);
  animation: rgb-shift 0.4s ease;
}

@keyframes rgb-shift {
  0%   { text-shadow: none; }
  25%  { text-shadow: -4px 0 var(--dp-neon-cyan), 4px 0 var(--dp-neon-magenta); }
  50%  { text-shadow: 2px 0 var(--dp-neon-lime), -2px 0 var(--dp-neon-red); }
  75%  { text-shadow: -3px 0 var(--dp-neon-cyan), 3px 0 var(--dp-neon-magenta); }
  100% { text-shadow: none; }
}
```

### 代表作品

| 网站 | 年份 | 特点 |
|------|------|------|
| brunosimon.com (3D 赛车) | 2023 | WebGL 3D 交互、游戏化 |
| zeronorth.com | 2024 | 暗色调、扫描线、故障效果 |
| zyrouge.me | 2023 | 赛博朋克、霓虹、极暗 |

---

## 4. Bento Grid

### 设计哲学

**"模块化即美学。"** 2025-2026 年最显著的布局趋势，受 Apple 官网和 Samsung 产品页启发。
Bento Grid 将内容组织为大小不一的矩形模块，类似日本便当盒（Bento Box）的分区方式。

**适用场景：** 产品展示（SaaS 硬件/软件）、功能特性页、数据仪表盘、作品集展示、落地页。

**核心理念：**
- 所有内容被封装进矩形卡片
- 模块大小不均等——突出重点信息
- 紧凑排列，间距均匀（12-20px）
- Hover 时微动画（缩放、阴影加深、内容变化）
- 圆角统一，视觉上整洁有序

### 配色方案

```css
:root {
  /* Apple/Samsung 现代科技风 */
  --bg-grid:       #000000;        /* Apple 暗底方案 */
  --bg-card:       #1C1C1E;        /* iOS 深灰卡片 */
  --fg-primary:    #F5F5F7;        /* 苹果白 */
  --fg-secondary:  #86868B;        /* 苹果灰 */
  --accent-blue:   #0A84FF;        /* iOS 蓝 */
  --accent-green:  #30D158;        /* iOS 绿 */
  --accent-orange: #FF9F0A;        /* iOS 橙 */
  --accent-purple: #BF5AF2;        /* iOS 紫 */
  --grid-gap:      16px;
  --grid-radius:   24px;
}
```

### 排版策略

```css
:root {
  --grid-font-display: 'SF Pro Display', -apple-system, sans-serif;
  --grid-font-body:    'SF Pro Text', -apple-system, sans-serif;

  --grid-size-title:    clamp(1.25rem, 2vw, 2rem);
  --grid-size-headline: clamp(1rem, 1.5vw, 1.5rem);
  --grid-size-body:     clamp(0.8rem, 1vw, 1rem);
  --grid-size-label:    clamp(0.625rem, 0.7vw, 0.75rem);

  --grid-weight-title:  600;
  --grid-weight-body:   400;
}
```

### 关键 CSS 实现

```css
/* === Bento Grid 核心布局 === */
.bento-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(180px, auto);
  gap: var(--grid-gap);
  padding: var(--grid-gap);
  max-width: 1280px;
  margin: 0 auto;
}

/* 单元格基础样式 */
.bento-cell {
  background: var(--bg-card);
  border-radius: var(--grid-radius);
  padding: clamp(20px, 3vw, 32px);
  overflow: hidden;
  position: relative;
  transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1),
              box-shadow 0.4s cubic-bezier(0.22, 1, 0.36, 1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.bento-cell:hover {
  transform: scale(1.02);
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.3);
  z-index: 1;
}

/* === 非对称布局变体 === */

/* 大图卡片：跨 2 列 2 行 */
.bento-cell--hero {
  grid-column: span 2;
  grid-row: span 2;
}

/* 宽幅卡片：跨 3 列 */
.bento-cell--wide {
  grid-column: span 3;
}

/* 高卡片：跨 2 行 */
.bento-cell--tall {
  grid-row: span 2;
}

/* 窄条：跨 2 列 */
.bento-cell--bar {
  grid-column: span 2;
}

/* === 响应式 Bento Grid === */
@media (max-width: 1024px) {
  .bento-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .bento-cell--hero {
    grid-column: span 2;
    grid-row: span 1;
  }
  .bento-cell--wide {
    grid-column: span 2;
  }
  .bento-cell--tall {
    grid-row: span 1;
  }
}

@media (max-width: 640px) {
  .bento-grid {
    grid-template-columns: 1fr;
    grid-auto-rows: minmax(200px, auto);
  }
  .bento-cell--hero,
  .bento-cell--wide,
  .bento-cell--bar {
    grid-column: span 1;
  }
}

/* === 单元格内容样式 === */
.bento-cell__label {
  font-size: var(--grid-size-label);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--accent-blue);
  margin-bottom: 8px;
}

.bento-cell__title {
  font-family: var(--grid-font-display);
  font-size: var(--grid-size-headline);
  font-weight: var(--grid-weight-title);
  color: var(--fg-primary);
  margin-bottom: 8px;
}

.bento-cell__body {
  font-size: var(--grid-size-body);
  color: var(--fg-secondary);
  line-height: 1.5;
}

/* === 渐变色标签圆点 === */
.bento-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
  margin-right: 8px;
}

.bento-dot--blue   { background: var(--accent-blue); }
.bento-dot--green  { background: var(--accent-green); }
.bento-dot--orange { background: var(--accent-orange); }
.bento-dot--purple { background: var(--accent-purple); }

/* === 带图标的 Bento 卡片（图标居中放大） === */
.bento-cell__icon {
  width: 48px;
  height: 48px;
  margin-bottom: 16px;
  opacity: 0.8;
}
```

```html
<!-- Bento Grid 使用示例 -->
<section class="bento-grid">
  <div class="bento-cell bento-cell--hero">
    <span class="bento-cell__label"><span class="bento-dot bento-dot--blue"></span>性能</span>
    <h3 class="bento-cell__title">A18 Pro 芯片</h3>
    <p class="bento-cell__body">游戏级图形处理能力，超越任何移动芯片。</p>
    <!-- 可嵌入图片/3D 渲染 -->
  </div>

  <div class="bento-cell">
    <span class="bento-cell__label"><span class="bento-dot bento-dot--green"></span>续航</span>
    <h3 class="bento-cell__title">全天候电池</h3>
    <p class="bento-cell__body">长达 29 小时视频播放。</p>
  </div>

  <div class="bento-cell">
    <span class="bento-cell__label"><span class="bento-dot bento-dot--orange"></span>相机</span>
    <h3 class="bento-cell__title">4800 万像素</h3>
    <p class="bento-cell__body">融合式四合一像素。</p>
  </div>

  <div class="bento-cell bento-cell--wide">
    <span class="bento-cell__label"><span class="bento-dot bento-dot--purple"></span>设计</span>
    <h3 class="bento-cell__title">钛金属外壳</h3>
    <p class="bento-cell__body">航空级钛合金，轻至 191 克。</p>
  </div>

  <div class="bento-cell bento-cell--bar">
    <span class="bento-cell__label">存储</span>
    <h3 class="bento-cell__title">最高 2TB</h3>
  </div>
</section>
```

### 代表作品

| 网站 | 年份 | 特点 |
|------|------|------|
| apple.com/iphone-16-pro | 2024 | Apple Bento 模板，暗底圆角卡片 |
| samsung.com/galaxy | 2025 | 亮色 Bento，非对称布局 |
| linear.app | 2024 | Bento + 微动画，SaaS 功能展示 |

---

## 5. 电影沉浸 Cinematic Immersion

### 设计哲学

**"打开浏览器就是走进电影院。"** 受 Igloo Inc 等创意工作室影响，电影沉浸风格将全屏视频/图片与深色 UI 结合，
通过上下黑边（Letterbox）、电影宽幅比例和沉浸式滚动，创造影院级浏览体验。

**适用场景：** 电影/影视公司、纪录片、游戏大作官网、建筑可视化、品牌故事长页。

**核心理念：**
- 全屏媒体（视频/图片）是主角
- 深色 UI 完全让位给视觉内容
- 2.39:1 或 16:9 电影宽高比
- 文字覆盖在画面上，带模糊背景
- 声音是体验的一部分（可选自动播放音频）
- 滚动驱动叙事（Scroll-driven Storytelling）

### 配色方案

```css
:root {
  --ci-bg:           #000000;     /* 纯黑 */
  --ci-fg:           #FFFFFF;     /* 纯白 */
  --ci-fg-muted:     rgba(255, 255, 255, 0.6);
  --ci-overlay:      rgba(0, 0, 0, 0.4);
  --ci-overlay-heavy:rgba(0, 0, 0, 0.7);
  --ci-letterbox:    #000000;
  --ci-accent:       #C9A96E;     /* 金色（类似奥斯卡金） */
}
```

### 排版策略

```css
:root {
  --ci-font-display: 'Instrument Serif', 'Playfair Display', serif;
  --ci-font-body:    'Satoshi', sans-serif;
  --ci-font-mono:    'JetBrains Mono', monospace;

  --ci-size-hero:    clamp(3rem, 8vw, 7rem);
  --ci-size-subtitle:clamp(1rem, 2vw, 1.5rem);
  --ci-size-body:    clamp(0.875rem, 1.1vw, 1rem);
  --ci-size-meta:    clamp(0.625rem, 0.8vw, 0.75rem);

  --ci-weight-display: 400;
  --ci-weight-body:    300;
  --ci-leading:        1.7;
}
```

### 关键 CSS 实现

```css
/* === 电影宽高比容器 === */
.ci-cinematic {
  aspect-ratio: 16 / 9;
  width: 100%;
  overflow: hidden;
  position: relative;
  background: var(--ci-bg);
}

.ci-ultrawide {
  aspect-ratio: 21 / 9;   /* 超宽屏 */
}

.ci-letterbox {
  aspect-ratio: 2.39 / 1;  /* 标准 Cinescope 宽银幕 */
}

/* === 上下黑边（Letterbox Bars） === */
.ci-letterbox-wrap {
  position: relative;
  width: 100%;
  background: var(--ci-letterbox);
}

.ci-letterbox-wrap::before,
.ci-letterbox-wrap::after {
  content: '';
  display: block;
  width: 100%;
  height: clamp(30px, 8vh, 100px);
  background: var(--ci-letterbox);
  position: relative;
  z-index: 2;
}

/* === 全屏视频背景 === */
.ci-video-section {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.ci-video-section video {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.ci-video-section .ci-overlay {
  position: absolute;
  inset: 0;
  background: var(--ci-overlay);
  z-index: 1;
}

.ci-video-section .ci-content {
  position: relative;
  z-index: 2;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: clamp(24px, 5vw, 80px);
  padding-bottom: clamp(60px, 12vh, 160px);
}

/* === 暗色渐隐分隔 === */
.ci-fade-section {
  position: relative;
}

.ci-fade-section::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 40%;
  background: linear-gradient(transparent, var(--ci-bg));
  pointer-events: none;
}

/* === 电影标题覆盖 === */
.ci-title-overlay {
  font-family: var(--ci-font-display);
  font-size: var(--ci-size-hero);
  font-weight: var(--ci-weight-display);
  color: var(--ci-fg);
  line-height: 1.05;
  text-shadow: 0 2px 40px rgba(0, 0, 0, 0.5);
  max-width: 18ch;
}

.ci-subtitle-overlay {
  font-family: var(--ci-font-body);
  font-size: var(--ci-size-subtitle);
  font-weight: var(--ci-weight-body);
  color: var(--ci-fg-muted);
  margin-top: 16px;
  max-width: 40ch;
}

/* === 元信息标签（场景/时间等） === */
.ci-meta {
  font-family: var(--ci-font-mono);
  font-size: var(--ci-size-meta);
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--ci-accent);
}

/* === 滚动进度条 === */
.ci-progress {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  background: var(--ci-accent);
  z-index: 9999;
  transform-origin: left;
  /* 宽度由 JS 控制：transform: scaleX(scrollProgress) */
}

/* === 全屏过渡（黑屏淡入淡出） === */
.ci-scene-transition {
  position: fixed;
  inset: 0;
  background: var(--ci-bg);
  z-index: 9990;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.8s ease;
}

.ci-scene-transition.is-active {
  opacity: 1;
}
```

### 代表作品

| 网站 | 年份 | 特点 |
|------|------|------|
| igloo.com.au | 2023 | 电影级叙事、全屏视频滚动 |
| sony.com/a7R-series | 2024 | 相机产品页、Letterbox 宽屏 |
| hellomynameis.com | 2024 | 沉浸式滚动、暗色调 |

---

## 6. 反设计/粗野 Anti-Design / Brutalism

### 设计哲学

**"反叛是新的顺从。"** 粗野主义（Brutalism）在网页设计中的复兴，表现为故意打破传统审美规则——
粗边框、实色阴影（硬阴影）、亮色块、对齐偏移、字体混搭、"看起来像没做完"的感觉。
这是一种通过"丑"来传达态度和个性的设计策略。

**适用场景：** 设计工作室、独立杂志、地下音乐厂牌、创意机构官网、艺术项目、政治/社会议题网站。

**核心理念：**
- 粗黑边框（2-4px solid black）是标配
- 硬阴影（无模糊、纯偏移）替代柔和投影
- 高饱和度纯色块（红、黄、蓝、绿）
- 字体故意不协调——衬线与无衬线混用
- 拒绝完美对齐，拥抱"随意的"布局
- 可见网格系统（grid lines）
- 按钮/链接样式故意"原始"

### 配色方案

```css
:root {
  --br-bg:           #FFFEF2;    /* 随便的白 */
  --br-fg:           #000000;    /* 纯黑 */
  --br-yellow:       #FFE500;    /* 粗野黄 */
  --br-red:          #FF3333;    /* 粗野红 */
  --br-blue:         #3366FF;    /* 粗野蓝 */
  --br-green:        #00CC66;    /* 粗野绿 */
  --br-purple:       #9933FF;    /* 粗野紫 */
  --br-border:       #000000;
  --br-border-w:     3px;
  --br-shadow-offset: 6px;
}
```

### 排版策略

```css
:root {
  --br-font-display: 'Georgia', 'Times New Roman', serif;   /* 衬线体标题 */
  --br-font-body:    'Arial', 'Helvetica', sans-serif;       /* 无衬线正文 */
  --br-font-mono:    'Courier New', monospace;               /* 等宽装饰 */

  --br-size-hero:    clamp(3rem, 10vw, 9rem);
  --br-size-h1:      clamp(2rem, 5vw, 5rem);
  --br-size-body:    clamp(1rem, 1.2vw, 1.125rem);
  --br-size-small:   clamp(0.7rem, 0.9vw, 0.85rem);

  /* 字重故意极端 */
  --br-weight-display: 900;
  --br-weight-body:    400;
  --br-tracking:       0em;       /* 无字距调整 */
  --br-leading:        1.2;
}
```

### 关键 CSS 实现

```css
/* === 粗野主义基础 === */
.brutalism {
  background-color: var(--br-bg);
  color: var(--br-fg);
  font-family: var(--br-font-body);
}

/* === 硬阴影组件 === */
.br-card {
  background: var(--br-yellow);
  border: var(--br-border-w) solid var(--br-border);
  box-shadow: var(--br-shadow-offset) var(--br-shadow-offset) 0 var(--br-fg);
  padding: 24px;
  transition: transform 0.1s, box-shadow 0.1s;
  cursor: pointer;
}

.br-card:hover {
  transform: translate(-2px, -2px);
  box-shadow: 8px 8px 0 var(--br-fg);
}

.br-card:active {
  transform: translate(2px, 2px);
  box-shadow: 4px 4px 0 var(--br-fg);
}

/* === 颜色变体 === */
.br-card--red    { background: var(--br-red);    color: #fff; }
.br-card--blue   { background: var(--br-blue);   color: #fff; }
.br-card--green  { background: var(--br-green);  color: #000; }
.br-card--white  { background: #fff; }

/* === 粗野按钮 === */
.br-btn {
  display: inline-block;
  font-family: var(--br-font-body);
  font-size: var(--br-size-body);
  font-weight: var(--br-weight-body);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 12px 28px;
  border: var(--br-border-w) solid var(--br-border);
  background: var(--br-fg);
  color: var(--br-bg);
  cursor: pointer;
  box-shadow: var(--br-shadow-offset) var(--br-shadow-offset) 0 var(--br-fg);
  text-decoration: none;
  transition: transform 0.1s, box-shadow 0.1s;
}

.br-btn:hover {
  transform: translate(-2px, -2px);
  box-shadow: 8px 8px 0 var(--br-fg);
}

.br-btn:active {
  transform: translate(2px, 2px);
  box-shadow: 2px 2px 0 var(--br-fg);
}

.br-btn--outline {
  background: transparent;
  color: var(--br-fg);
}

/* === 粗野标签/徽章 === */
.br-tag {
  display: inline-block;
  font-family: var(--br-font-mono);
  font-size: var(--br-size-small);
  text-transform: uppercase;
  padding: 4px 12px;
  border: 2px solid var(--br-border);
  background: var(--br-yellow);
}

/* === 可见网格背景 === */
.br-grid-bg {
  background-color: var(--br-bg);
  background-image:
    linear-gradient(rgba(0,0,0,0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,0,0,0.1) 1px, transparent 1px);
  background-size: 40px 40px;
}

/* === 旋转文字（故意"歪斜"） === */
.br-rotate {
  transform: rotate(-3deg);
}

.br-rotate-alt {
  transform: rotate(2deg);
}

/* === Marquee 跑马灯（复古风格） === */
.br-marquee {
  overflow: hidden;
  white-space: nowrap;
  border-top: var(--br-border-w) solid var(--br-border);
  border-bottom: var(--br-border-w) solid var(--br-border);
  padding: 12px 0;
}

.br-marquee__track {
  display: inline-block;
  animation: marquee-scroll 20s linear infinite;
  font-family: var(--br-font-display);
  font-size: var(--br-size-h1);
  font-weight: var(--br-weight-display);
  text-transform: uppercase;
}

.br-marquee__track span {
  display: inline-block;
  margin-right: 40px;
}

@keyframes marquee-scroll {
  from { transform: translateX(0); }
  to   { transform: translateX(-50%); }
}

/* === 粗野分割线 === */
.br-divider {
  border: none;
  border-top: var(--br-border-w) solid var(--br-border);
}
```

### 代表作品

| 网站 | 年份 | 特点 |
|------|------|------|
| gumroad.com (旧版) | 2023 | 硬阴影、粗边框、亮色块 |
| yaleunion.org | 2023 | 纯粹粗野主义、无装饰 |
| cargocollective.com | — | 粗野设计工具平台 |

---

## 7. Y2K 复古 Y2K Retro

### 设计哲学

**"欢迎回到 1999。"** Y2K（千禧年）美学在 2024-2025 年全面回归。
特点是像素感、金属质感（Chrome）、霓虹渐变、3D 文字效果、Starburst 图形、
泡泡字体、透明度叠加——所有让你想起 Windows 98 / iMac G3 / 早期 Flash 网站的东西。

**适用场景：** 音乐/独立音乐、街头品牌、创意活动、Gen-Z 潮流品牌、Web 游戏入口、艺术实验项目。

**核心理念：**
- 金属渐变文字（Chrome Text）
- 像素化元素（CSS image-rendering: pixelated）
- 霓虹粉/蓝/紫渐变
- Starburst / 闪烁星形装饰
- 半透明层叠（类似早期 Windows）
- 鼓励使用 emoji 和 ASCII art
- 低分辨率图形被"有意保留"

### 配色方案

```css
:root {
  --y2k-bg:           #E8E0FF;    /* 薰衣草淡紫 */
  --y2k-fg:           #1A0033;    /* 深紫 */
  --y2k-pink:         #FF6EC7;    /* 热粉 */
  --y2k-cyan:         #00FFFF;    /* 赛博青 */
  --y2k-purple:       #9B30FF;    /* 电紫 */
  --y2k-magenta:      #FF00FF;    /* 品红 */
  --y2k-yellow:       #FFD700;    /* 金色 */
  --y2k-silver:       linear-gradient(135deg, #C0C0C0 0%, #E8E8E8 30%, #A0A0A0 50%, #D0D0D0 70%, #B0B0B0 100%);
  --y2k-chrome:       linear-gradient(180deg, #E8E8E8 0%, #A8A8A8 25%, #F0F0F0 50%, #888888 75%, #D8D8D8 100%);
}
```

### 排版策略

```css
:root {
  --y2k-font-display: 'Space Grotesk', 'Verdana', sans-serif;
  --y2k-font-body:    'Trebuchet MS', 'Verdana', sans-serif;
  --y2k-font-pixel:   'Press Start 2P', 'Courier New', monospace;  /* 像素字体 */

  --y2k-size-hero:    clamp(2.5rem, 8vw, 7rem);
  --y2k-size-h1:      clamp(1.5rem, 4vw, 4rem);
  --y2k-size-body:    clamp(0.875rem, 1.1vw, 1rem);
  --y2k-size-pixel:   clamp(0.5rem, 0.8vw, 0.75rem);

  --y2k-weight-display: 700;
  --y2k-weight-body:    400;
}
```

### 关键 CSS 实现

```css
/* === Chrome 金属渐变文字 === */
.y2k-chrome-text {
  font-family: var(--y2k-font-display);
  font-size: var(--y2k-size-hero);
  font-weight: var(--y2k-weight-display);
  background: var(--y2k-chrome);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: none;
  filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.3));
}

/* === 霓虹渐变文字 === */
.y2k-neon-text {
  font-family: var(--y2k-font-display);
  font-size: var(--y2k-size-hero);
  font-weight: var(--y2k-weight-display);
  background: linear-gradient(
    135deg,
    var(--y2k-pink) 0%,
    var(--y2k-magenta) 30%,
    var(--y2k-purple) 60%,
    var(--y2k-cyan) 100%
  );
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 0 20px rgba(255, 0, 255, 0.4));
}

/* === 像素化元素 === */
.y2k-pixel {
  image-rendering: pixelated;
  image-rendering: -moz-crisp-edges;
  image-rendering: crisp-edges;
}

.y2k-pixel-text {
  font-family: var(--y2k-font-pixel);
  font-size: var(--y2k-size-pixel);
  color: var(--y2k-fg);
  line-height: 2;
}

/* === Starburst 闪烁星形（纯 CSS） === */
.y2k-starburst {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 120px;
  height: 120px;
}

.y2k-starburst::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--y2k-yellow);
  clip-path: polygon(
    50% 0%, 61% 35%, 98% 35%, 68% 57%,
    79% 91%, 50% 70%, 21% 91%, 32% 57%,
    2% 35%, 39% 35%
  );
}

.y2k-starburst span {
  position: relative;
  z-index: 1;
  font-family: var(--y2k-font-display);
  font-weight: 700;
  font-size: 0.8rem;
  text-transform: uppercase;
  color: var(--y2k-fg);
}

/* === 半透明 Y2K 卡片（Windows 98 风格） === */
.y2k-card {
  background: rgba(232, 224, 255, 0.7);
  backdrop-filter: blur(2px);
  border: 2px solid var(--y2k-purple);
  border-radius: 12px;
  padding: 20px;
  box-shadow:
    4px 4px 0 rgba(155, 48, 255, 0.3),
    inset 0 0 30px rgba(255, 255, 255, 0.3);
}

/* === 渐变网格背景（Gradient Mesh 风格） === */
.y2k-gradient-mesh {
  background:
    radial-gradient(ellipse at 15% 20%, rgba(255, 110, 199, 0.4) 0%, transparent 50%),
    radial-gradient(ellipse at 85% 15%, rgba(0, 255, 255, 0.3) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 80%, rgba(155, 48, 255, 0.3) 0%, transparent 50%),
    radial-gradient(ellipse at 20% 70%, rgba(255, 215, 0, 0.2) 0%, transparent 50%),
    var(--y2k-bg);
}

/* === 3D 按钮凸起效果 === */
.y2k-btn-3d {
  font-family: var(--y2k-font-display);
  font-weight: 700;
  font-size: var(--y2k-size-body);
  text-transform: uppercase;
  padding: 14px 32px;
  border: none;
  border-radius: 8px;
  background: linear-gradient(180deg, #FF6EC7 0%, #CC3399 100%);
  color: #fff;
  cursor: pointer;
  box-shadow:
    0 4px 0 #990066,
    0 6px 8px rgba(0,0,0,0.2);
  transition: transform 0.1s, box-shadow 0.1s;
}

.y2k-btn-3d:hover {
  transform: translateY(-1px);
  box-shadow:
    0 5px 0 #990066,
    0 8px 12px rgba(0,0,0,0.25);
}

.y2k-btn-3d:active {
  transform: translateY(3px);
  box-shadow:
    0 1px 0 #990066,
    0 2px 4px rgba(0,0,0,0.2);
}

/* === 闪烁动画 === */
.y2k-blink {
  animation: y2k-blink 1s step-end infinite;
}

@keyframes y2k-blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

/* === 彩虹边框旋转 === */
.y2k-rainbow-border {
  position: relative;
  border-radius: 16px;
  padding: 3px;
  background: conic-gradient(
    from 0deg,
    var(--y2k-pink),
    var(--y2k-cyan),
    var(--y2k-purple),
    var(--y2k-magenta),
    var(--y2k-pink)
  );
  animation: rainbow-spin 4s linear infinite;
}

.y2k-rainbow-border > * {
  background: var(--y2k-bg);
  border-radius: 13px;
  display: block;
}

@keyframes rainbow-spin {
  to { filter: hue-rotate(360deg); }
}
```

### 代表作品

| 网站 | 年份 | 特点 |
|------|------|------|
| y2k.ae | 2024 | 纯粹 Y2K 复古、像素、渐变 |
| mschf.com | 2024 | 反主流、粗糙、彩色 |
| clubrhino.com | 2023 | Chrome 文字、霓虹渐变 |

---

## 8. 档案式排版 Archival Typography

### 设计哲学

**"信息即美学。"** 受编辑设计、学术出版物和档案系统影响，档案式排版将密集的文字信息本身变成视觉元素。
页面看起来像一份研究报告、一本产品手册、或者一个数据表格——但每一行、每个数字都被精心排版。

**适用场景：** 设计年鉴、建筑事务所、咨询公司、数据可视化项目、研究机构、出版机构。

**核心理念：**
- 等宽字体（Monospace）是主角
- 数据密度高——信息本身就是装饰
- 严格网格系统，一切对齐
- 小字号、密集排列
- 编号系统（01. / 02. / ...）作为视觉节奏
- 表格化布局、标签化信息
- 极少使用图片——如果用，也是功能性图片

### 配色方案

```css
:root {
  --at-bg:           #FAFAF8;     /* 略暖的档案白 */
  --at-fg:           #1A1A1A;     /* 深黑 */
  --at-muted:        #888888;     /* 辅助灰 */
  --at-accent:       #C41E3A;     /* 档案红（印章色） */
  --at-line:         #E5E5E3;     /* 表格线 */
  --at-hover-bg:     rgba(196, 30, 58, 0.05);
  --at-font-mono:    'SF Mono', 'JetBrains Mono', 'Fira Code', monospace;
  --at-font-sans:    'Inter', 'Helvetica Neue', sans-serif;
  --at-font-serif:   'Instrument Serif', 'Georgia', serif;
}
```

### 排版策略

```css
:root {
  --at-size-h1:      clamp(1.5rem, 3vw, 3rem);
  --at-size-h2:      clamp(1rem, 2vw, 1.75rem);
  --at-size-body:    clamp(0.75rem, 0.9vw, 0.875rem);
  --at-size-caption: clamp(0.625rem, 0.7vw, 0.7rem);
  --at-size-index:   clamp(0.6rem, 0.65vw, 0.65rem);

  --at-weight-display: 400;
  --at-weight-bold:    500;
  --at-tracking:       0.02em;
  --at-leading:        1.5;
  --at-tabular-nums:   font-variant-numeric: tabular-nums;
}
```

### 关键 CSS 实现

```css
/* === 档案式排版基础 === */
.archival-typography {
  background-color: var(--at-bg);
  color: var(--at-fg);
  font-family: var(--at-font-mono);
  font-size: var(--at-size-body);
  line-height: var(--at-leading);
  letter-spacing: var(--at-tracking);
  font-variant-numeric: tabular-nums;   /* 数字等宽对齐 */
}

/* === 编号标题系统 === */
.at-numbered-title {
  display: flex;
  gap: 16px;
  align-items: baseline;
  margin-bottom: 32px;
}

.at-numbered-title__index {
  font-family: var(--at-font-mono);
  font-size: var(--at-size-caption);
  color: var(--at-muted);
  min-width: 3ch;       /* 固定宽度，保证对齐 */
  padding-top: 4px;
}

.at-numbered-title__text {
  font-family: var(--at-font-serif);
  font-size: var(--at-size-h1);
  font-weight: var(--at-weight-display);
  line-height: 1.15;
}

/* === 数据行/表格式布局 === */
.at-data-row {
  display: grid;
  grid-template-columns: 3ch 1fr 1fr 1fr;
  gap: 24px;
  padding: 12px 0;
  border-bottom: 1px solid var(--at-line);
  font-size: var(--at-size-body);
  transition: background-color 0.2s ease;
  cursor: default;
}

.at-data-row:hover {
  background-color: var(--at-hover-bg);
}

.at-data-row__index {
  color: var(--at-muted);
  font-size: var(--at-size-caption);
}

.at-data-row__primary {
  font-weight: var(--at-weight-bold);
}

.at-data-row__secondary {
  color: var(--at-muted);
}

.at-data-row__meta {
  color: var(--at-accent);
  text-align: right;
  font-size: var(--at-size-caption);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* === 档案标签（Category Tag） === */
.at-tag {
  display: inline-block;
  font-family: var(--at-font-mono);
  font-size: var(--at-size-caption);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 3px 10px;
  border: 1px solid var(--at-line);
  color: var(--at-muted);
}

.at-tag--active {
  border-color: var(--at-accent);
  color: var(--at-accent);
  background: rgba(196, 30, 58, 0.05);
}

/* === 侧边注释 === */
.at-side-note {
  font-family: var(--at-font-mono);
  font-size: var(--at-size-caption);
  color: var(--at-muted);
  border-left: 2px solid var(--at-accent);
  padding-left: 12px;
  margin: 24px 0;
}

/* === 纯文字表格 === */
.at-text-table {
  width: 100%;
  border-collapse: collapse;
}

.at-text-table th {
  font-family: var(--at-font-mono);
  font-size: var(--at-size-caption);
  font-weight: var(--at-weight-bold);
  text-align: left;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--at-muted);
  padding: 8px 0;
  border-bottom: 2px solid var(--at-fg);
}

.at-text-table td {
  padding: 12px 0;
  border-bottom: 1px solid var(--at-line);
  font-size: var(--at-size-body);
  vertical-align: top;
}

.at-text-table tr:hover td {
  background-color: var(--at-hover-bg);
}

/* === 密集列表（密集项目索引） === */
.at-dense-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.at-dense-list li {
  font-family: var(--at-font-mono);
  font-size: var(--at-size-body);
  padding: 6px 0;
  border-bottom: 1px solid var(--at-line);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.at-dense-list li .list-index {
  color: var(--at-muted);
  font-size: var(--at-size-caption);
  min-width: 3ch;
}

.at-dense-list li .list-value {
  flex: 1;
}

.at-dense-list li .list-year {
  color: var(--at-muted);
  font-size: var(--at-size-caption);
  font-variant-numeric: tabular-nums;
}

/* === 统计数字面板 === */
.at-stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 1px;
  background: var(--at-line);
  border: 1px solid var(--at-line);
}

.at-stat {
  background: var(--at-bg);
  padding: clamp(16px, 2vw, 24px);
}

.at-stat__number {
  font-family: var(--at-font-mono);
  font-size: clamp(1.5rem, 3vw, 2.5rem);
  font-weight: var(--at-weight-bold);
  font-variant-numeric: tabular-nums;
  line-height: 1;
  margin-bottom: 8px;
}

.at-stat__label {
  font-family: var(--at-font-mono);
  font-size: var(--at-size-caption);
  color: var(--at-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* === 分页标识 === */
.at-page-indicator {
  position: fixed;
  bottom: 24px;
  right: 24px;
  font-family: var(--at-font-mono);
  font-size: var(--at-size-caption);
  color: var(--at-muted);
  z-index: 100;
}

.at-page-indicator::before {
  content: 'NO. ';
}
```

### 代表作品

| 网站 | 年份 | 特点 |
|------|------|------|
| atlasofplaces.com | — | 建筑档案、密集信息 |
| storefront.af | 2024 | 数据密集、等宽字体、编号系统 |
| randomstudio.com | 2024 | 实验工作室、档案式展示 |

---

## 附录：风格混搭指南

优秀的 Awwwards SOTD 头奖网站往往不是纯粹使用一种风格，而是创造性地混搭：

| 混搭组合 | 效果 | 示例 |
|----------|------|------|
| Neo-Minimal + Cinematic | 大面积留白 + 全屏视频 | 奢侈品牌官网 |
| Organic + Archival | 噪点纹理 + 密集数据 | 环境报告/年报 |
| Brutalism + Y2K | 硬阴影 + Chrome 渐变 | 地下音乐厂牌 |
| Bento + Neo-Minimal | 模块化 + 极致留白 | Apple/Linear 产品页 |
| Digital Punk + Cinematic | 故障效果 + 电影叙事 | 游戏/科幻品牌 |
| Y2K + Organic | 霓虹渐变 + 流动形状 | Gen-Z 潮流品牌 |

### 通用最佳实践

1. **始终使用 CSS 自定义属性**（`--var-name`）定义设计 Token，方便主题切换
2. **使用 `clamp()` 实现**流式排版，避免硬断点跳跃
3. **`prefers-reduced-motion`** 必须尊重——关闭所有非必要动画
4. **`-webkit-font-smoothing: antialiased`** 是高质量排版的标配
5. **测试极端内容长度**——风格系统需要在内容极端多/少的场景下依然可用
6. **性能优先**——SVG 内联优于外部图片、CSS 动画优于 JS 动画
7. **可访问性不是可选项**——确保对比度达标（WCAG AA）、所有交互可键盘操作

---

> 本文档持续更新。参考来源：Awwwards.com、FWA、CSS Design Awards、CSS-Tricks、各 SOTD 头奖网站源码分析。
