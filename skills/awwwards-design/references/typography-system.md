# Awwwards 获奖网站排版系统参考

> 本文档涵盖 2025 年 Awwwards 获奖网站中最前沿的排版技术、字体搭配方案、动效模式与性能优化策略。

---

## 一、Variable Fonts（可变字体 —— 2025 核心趋势）

### 1.1 什么是可变字体

可变字体（Variable Fonts）是一种单文件字体格式，包含多个字形实例（粗细、宽度、斜体等轴）。相比传统方案需要为每个字重单独加载一个 WOFF2 文件，可变字体用一个文件覆盖所有变化轴。

**核心优势：**

| 对比项 | 传统字体 | 可变字体 |
|--------|---------|---------|
| 文件数量 | 每个字重一个文件 | 单个文件 |
| 粗细过渡 | 阶梯式（400 → 700） | 无级过渡（400 → 401 → … → 700） |
| 总体积 | 较大（冗余数据多） | 通常更小 40-60% |
| 动画能力 | 不支持平滑过渡 | 支持连续 CSS 动画 |

### 1.2 CSS 基础实现

```css
/* ========== 可变字体加载 ========== */
@font-face {
  font-family: 'Clash Display Variable';
  src: url('/fonts/ClashDisplay-Variable.woff2') format('woff2');
  font-weight: 200 900;         /* 支持的粗细范围 */
  font-stretch: 75% 125%;       /* 支持的宽度范围（如果有的话） */
  font-style: oblique 0deg 15deg; /* 支持的倾斜范围 */
  font-display: swap;
}

/* ========== 基础用法 ========== */
h1 {
  font-family: 'Clash Display Variable', sans-serif;
  font-weight: 450;  /* 传统写法：任意整数值 */
}

/* ========== font-variation-settings 显式控制 ========== */
.hero-title {
  font-family: 'PP Neue Montreal Variable', sans-serif;
  font-variation-settings:
    'wght' 750,    /* 粗细 Weight */
    'wdth' 100,    /* 宽度 Width */
    'ital' 0,      /* 斜体 Italic */
    'opsz' 16;     /* 光学尺寸 Optical Size */
}

/* ========== CSS 变量 + 可变字体（推荐模式） ========== */
:root {
  --font-display: 'Clash Display Variable', sans-serif;
  --font-body: 'Satoshi Variable', sans-serif;
}

h1 { font-family: var(--font-display); }
p  { font-family: var(--font-body); }
```

### 1.3 推荐可变字体清单

| 字体 | 风格 | 注册轴 | 最佳用途 |
|------|------|--------|---------|
| **PP Neue Montreal Variable** | 瑞士几何无衬线 | wght | 通用正文 / 标题 |
| **Clash Display Variable** | 展示型几何 | wght | Hero 标题 / 大字排版 |
| **Satoshi Variable** | 现代 Neo-Grotesk | wght | 正文 / UI 文字 |
| **Recursive** | 编程 + 展示混合 | wght, CASL, MONO, CRSV | 技术网站 / 代码展示 |
| **General Sans Variable** | 干净无衬线 | wght | 极简风格网站 |
| **Cabinet Grotesk Variable** | 人文几何 | wght | 温暖友好的品牌站 |
| **Instrument Serif Variable** | 高对比衬线 | wght, ital | 编辑式排版 |

### 1.4 font-weight 动画（可变字体独有能力）

```css
/* ========== Hover 时粗细平滑变化 ========== */
.nav-link {
  font-family: 'Clash Display Variable', sans-serif;
  font-weight: 400;
  transition: font-weight 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}

.nav-link:hover {
  font-weight: 700;
  /* 可变字体允许任意中间值，过渡完全平滑 */
}

/* ========== 用 font-variation-settings 精确控制 ========== */
.magnetic-button {
  font-family: 'Satoshi Variable', sans-serif;
  font-variation-settings: 'wght' 400;
  transition: font-variation-settings 0.4s ease;
}

.magnetic-button:hover {
  font-variation-settings: 'wght' 650;
}

/* ========== Scroll-driven weight 变化 ========== */
@supports (animation-timeline: scroll()) {
  .scroll-weight-text {
    font-family: 'Clash Display Variable', sans-serif;
    animation: weightByScroll linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 100%;
  }
}

@keyframes weightByScroll {
  from { font-variation-settings: 'wght' 200; }
  to   { font-variation-settings: 'wght' 900; }
}

/* ========== Recursive 字体：在等宽和比例字体之间过渡 ========== */
.code-transition {
  font-family: 'Recursive', monospace;
  font-variation-settings: 'MONO' 1, 'wght' 400;  /* 等宽模式 */
  transition: font-variation-settings 0.6s ease;
}

.code-transition:hover {
  font-variation-settings: 'MONO' 0, 'wght' 700;  /* 比例模式 */
}
```

### 1.5 性能对比

```css
/* ❌ 传统方式：需要加载 6 个文件 */
@font-face { font-family: 'Font'; src: url('Light.woff2'); font-weight: 300; }
@font-face { font-family: 'Font'; src: url('Regular.woff2'); font-weight: 400; }
@font-face { font-family: 'Font'; src: url('Medium.woff2'); font-weight: 500; }
@font-face { font-family: 'Font'; src: url('SemiBold.woff2'); font-weight: 600; }
@font-face { font-family: 'Font'; src: url('Bold.woff2'); font-weight: 700; }
@font-face { font-family: 'Font'; src: url('Black.woff2'); font-weight: 900; }
/* 总下载 ≈ 6 × 30KB = 180KB */

/* ✅ 可变字体：单个文件 */
@font-face {
  font-family: 'Font Variable';
  src: url('Font-Variable.woff2') format('woff2');
  font-weight: 200 900;
}
/* 总下载 ≈ 60-90KB（节省 50-67%） */
```

---

## 二、Font Pairing System（字体搭配系统）

### 2.1 Modern Contrast —— Clash Display + Satoshi

**风格：** 大胆几何展示字体 + 干净正文无衬线体
**适用场景：** 创意工作室、设计工具、科技产品官网

```css
:root {
  --font-heading: 'Clash Display', sans-serif;
  --font-body: 'Satoshi', sans-serif;
}

h1, h2, h3 {
  font-family: var(--font-heading);
  font-weight: 600;
  letter-spacing: -0.03em;
}

p, span, a {
  font-family: var(--font-body);
  font-weight: 400;
}

/* 搭配示例 —— Hero 区块 */
.hero {
  font-family: var(--font-heading);
  font-size: clamp(3rem, 10vw, 8rem);
  font-weight: 700;
  line-height: 0.9;
  letter-spacing: -0.04em;
  text-transform: uppercase;
}

.hero .subtitle {
  font-family: var(--font-body);
  font-size: clamp(1rem, 2vw, 1.25rem);
  font-weight: 400;
  letter-spacing: 0;
  text-transform: none;
}
```

### 2.2 Archival Serious —— Druk Wide + Courier

**风格：** 超粗展示字体 + 等宽打字机风格
**适用场景：** 新闻编辑、档案馆、实验性艺术、反叛文化品牌

```css
:root {
  --font-heading: 'Druk Wide', 'Impact', sans-serif;
  --font-body: 'Courier New', Courier, monospace;
}

h1 {
  font-family: var(--font-heading);
  font-size: clamp(3rem, 12vw, 10rem);
  font-weight: 700;
  line-height: 0.85;
  text-transform: uppercase;
  letter-spacing: -0.02em;
}

.body-text {
  font-family: var(--font-body);
  font-size: 0.875rem;
  line-height: 1.7;
  letter-spacing: 0.02em;
}

/* 日期标签 —— 强化档案感 */
.date-label {
  font-family: var(--font-body);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  border: 1px solid currentColor;
  padding: 4px 12px;
  display: inline-block;
}
```

### 2.3 Organic Warm —— Cabinet Grotesk + Georgia

**风格：** 人文主义无衬线 + 经典衬线
**适用场景：** 生活方式品牌、餐饮、建筑事务所、手工艺电商

```css
:root {
  --font-heading: 'Cabinet Grotesk', 'Segoe UI', sans-serif;
  --font-body: Georgia, 'Times New Roman', serif;
}

h1 {
  font-family: var(--font-heading);
  font-size: clamp(2.5rem, 8vw, 6rem);
  font-weight: 500;  /* 较轻的字重，温润不咄咄逼人 */
  line-height: 1.05;
  letter-spacing: -0.02em;
}

p {
  font-family: var(--font-body);
  font-size: clamp(1rem, 1.5vw, 1.125rem);
  line-height: 1.75;
  font-variant-numeric: oldstyle-nums;  /* 旧式数字，更优雅 */
}

/* 引用块 —— 衬线体独美 */
blockquote {
  font-family: var(--font-body);
  font-size: clamp(1.5rem, 3vw, 2.5rem);
  font-style: italic;
  line-height: 1.4;
  max-width: 55ch;
}
```

### 2.4 Minimal Tech —— Space Grotesk + Space Mono

**风格：** 科技感无衬线 + 等宽正文
**适用场景：** 开发者工具、SaaS 产品、Web3 / AI 项目、数据仪表盘

```css
:root {
  --font-heading: 'Space Grotesk', sans-serif;
  --font-body: 'Space Mono', monospace;
}

h1 {
  font-family: var(--font-heading);
  font-size: clamp(2rem, 7vw, 5rem);
  font-weight: 700;
  letter-spacing: -0.03em;
}

.label, .tag, .stat {
  font-family: var(--font-body);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

/* 数据展示 —— 等宽字体确保对齐 */
.data-grid {
  font-family: var(--font-body);
  font-variant-numeric: tabular-nums;
  font-size: 0.875rem;
}
```

### 2.5 Luxury Editorial —— Instrument Serif + Suisse Int'l

**风格：** 高对比衬线 + 瑞士无衬线
**适用场景：** 奢侈品、时尚品牌、高端杂志、建筑摄影集

```css
:root {
  --font-heading: 'Instrument Serif', Georgia, serif;
  --font-body: 'Suisse Int\'l', 'Helvetica Neue', sans-serif;
}

h1 {
  font-family: var(--font-heading);
  font-size: clamp(3rem, 9vw, 7rem);
  font-weight: 400;       /* 衬线体不需要太粗 */
  font-style: italic;     /* 斜体衬线 = 奢华感 */
  line-height: 1;
  letter-spacing: -0.01em;
}

.nav-item, .meta-text {
  font-family: var(--font-body);
  font-size: 0.8125rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

p {
  font-family: var(--font-body);
  font-size: clamp(1rem, 1.4vw, 1.125rem);
  line-height: 1.7;
  font-weight: 300;
}

/* 章节编号 —— 大号衬线装饰 */
.chapter-num {
  font-family: var(--font-heading);
  font-size: clamp(6rem, 20vw, 20rem);
  font-weight: 400;
  line-height: 0.7;
  color: transparent;
  -webkit-text-stroke: 1px currentColor;
}
```

### 2.6 Experimental —— Migra + Editorial New

**风格：** 展示衬线 + 编辑正文衬线
**适用场景：** 独立杂志、文化机构、创意咨询、先锋设计工作室

```css
:root {
  --font-heading: 'Migra', 'Didot', serif;
  --font-body: 'Editorial New', Georgia, serif;
}

h1 {
  font-family: var(--font-heading);
  font-size: clamp(4rem, 14vw, 12rem);
  font-weight: 300;
  line-height: 0.85;
  letter-spacing: -0.04em;
  text-transform: uppercase;
}

p {
  font-family: var(--font-body);
  font-size: clamp(1rem, 1.3vw, 1.0625rem);
  line-height: 1.8;
  font-weight: 400;
  orphans: 3;
  widows: 3;
}

/* 大段引用 —— 双衬线组合 */
.editorial-pull {
  font-family: var(--font-heading);
  font-size: clamp(1.5rem, 4vw, 3rem);
  font-weight: 200;
  line-height: 1.3;
  max-width: 40ch;
  text-align: justify;
  hyphens: auto;
}
```

---

## 三、Type Scale System（字号阶梯系统）

### 3.1 基于 Golden Ratio 的 clamp 值

```css
:root {
  /* ========== 黄金比例字号系统 ========== */
  /* 比例 1.618，基准 1rem (16px) */
  --fs-xs:   clamp(0.75rem, 0.7rem + 0.25vw, 0.8125rem);   /* 12-13px */
  --fs-sm:   clamp(0.875rem, 0.8rem + 0.3vw, 1rem);        /* 14-16px */
  --fs-base: clamp(1rem, 0.95rem + 0.25vw, 1.0625rem);     /* 16-17px */
  --fs-md:   clamp(1.125rem, 1rem + 0.5vw, 1.25rem);       /* 18-20px */
  --fs-lg:   clamp(1.25rem, 1rem + 1vw, 1.75rem);          /* 20-28px */
  --fs-xl:   clamp(1.75rem, 1.3rem + 2vw, 3rem);           /* 28-48px */
  --fs-2xl:  clamp(2.5rem, 1.5rem + 4vw, 5rem);            /* 40-80px */
  --fs-3xl:  clamp(3.5rem, 1.5rem + 8vw, 8rem);            /* 56-128px */
  --fs-hero: clamp(5rem, 2rem + 16vw, 12.5rem);            /* 80-200px */
}
```

### 3.2 与行高、字间距联动

```css
/* 每个层级的完整规范 */
.display-xl {
  font-size: var(--fs-hero);
  line-height: 0.85;
  letter-spacing: -0.05em;
  text-transform: uppercase;
}

.heading-1 {
  font-size: var(--fs-3xl);
  line-height: 0.9;
  letter-spacing: -0.04em;
}

.heading-2 {
  font-size: var(--fs-2xl);
  line-height: 1;
  letter-spacing: -0.03em;
}

.heading-3 {
  font-size: var(--fs-xl);
  line-height: 1.1;
  letter-spacing: -0.02em;
}

.lead {
  font-size: var(--fs-lg);
  line-height: 1.5;
  letter-spacing: -0.01em;
}

.body-lg {
  font-size: var(--fs-md);
  line-height: 1.7;
}

.body {
  font-size: var(--fs-base);
  line-height: 1.75;
}

.caption {
  font-size: var(--fs-xs);
  line-height: 1.6;
  letter-spacing: 0.03em;
}
```

### 3.3 极端尺度对比（200px Hero + 14px Body）

```css
/* Awwwards 2024-2025 最流行的排版策略 */
.hero-section {
  min-height: 100svh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: clamp(2rem, 5vw, 6rem);
}

.hero-title {
  font-family: 'Clash Display', sans-serif;
  font-size: clamp(4rem, 15vw, 12.5rem);   /* 64px → 200px */
  font-weight: 700;
  line-height: 0.85;
  letter-spacing: -0.05em;
  text-transform: uppercase;
}

.hero-meta {
  font-family: 'Satoshi', sans-serif;
  font-size: 0.875rem;                        /* 固定 14px */
  line-height: 1.6;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  margin-top: 2rem;
  max-width: 320px;
}

/* 尺度对比比 ≈ 14:1（14rem vs 1rem）*/
/* 这创造了强烈的视觉层级，是获奖网站的标配 */
```

---

## 四、Kinetic Typography（动态排版）

### 4.1 文字拆分模式

```html
<!-- HTML 结构：逐字拆分 -->
<h1 class="split-chars" data-split="chars">
  Award Winning Design
</h1>

<!-- HTML 结构：逐词拆分 -->
<p class="split-words" data-split="words">
  We craft digital experiences that push boundaries
</p>
```

```css
/* ========== 逐字拆分后的样式 ========== */
.split-chars .char {
  display: inline-block;
  /* 初始隐藏态 */
  opacity: 0;
  transform: translateY(100%) rotateX(-80deg);
  transform-origin: top center;
}

/* 入场动画 */
.split-chars.is-visible .char {
  animation: charReveal 0.6s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}

/* 逐字延迟通过 JS 设置 style="animation-delay: Xs" */
@keyframes charReveal {
  to {
    opacity: 1;
    transform: translateY(0) rotateX(0);
  }
}

/* ========== 逐词拆分后的 Hover 效果 ========== */
.split-words .word {
  display: inline-block;
  transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}

.split-words .word:hover {
  transform: translateY(-5px);
  color: var(--accent);
}
```

### 4.2 Scroll-driven 文字动画

```css
/* ========== 文字逐行淡入（纯 CSS，无需 JS） ========== */
@supports (animation-timeline: scroll()) {
  .reveal-text .line {
    opacity: 0;
    transform: translateY(2rem);
    animation: lineFadeIn linear both;
    animation-timeline: view();
    animation-range: entry 10% entry 50%;
  }

  @keyframes lineFadeIn {
    from {
      opacity: 0;
      transform: translateY(2rem);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
}

/* ========== 大标题的遮罩擦除效果 ========== */
.mask-reveal-text {
  /* 底部有一个白色遮罩向上移动 */
  background: linear-gradient(
    to top,
    transparent 0%,
    transparent 60%,
    white 100%
  );
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
```

### 4.3 CSS Shape 创意文字布局

```css
/* ========== 环形排列的文字（品牌 Logo 常见） ========== */
.circular-text {
  font-size: 0.875rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  animation: rotateText 20s linear infinite;
}

@keyframes rotateText {
  to { transform: rotate(360deg); }
}

/* ========== 弧形文字路径 ========== */
.arc-text {
  offset-path: path('M 0 200 Q 250 -100 500 200');
  offset-rotate: 0deg;
  animation: moveAlongArc 4s ease-in-out infinite alternate;
}

@keyframes moveAlongArc {
  from { offset-distance: 0%; }
  to   { offset-distance: 100%; }
}

/* ========== 波浪文字 ========== */
.wave-text .char {
  display: inline-block;
  animation: wave 2s ease-in-out infinite;
}

@keyframes wave {
  0%, 100% { transform: translateY(0); }
  50%      { transform: translateY(-10px); }
}
/* 每个字符设置递增的 animation-delay: calc(var(--i) * 0.05s) */
```

### 4.4 Marquee / Ticker 文字

```css
/* ========== 无限滚动 Marquee ========== */
.marquee {
  overflow: hidden;
  white-space: nowrap;
  /* 关键：用 mask 做两端淡出 */
  mask-image: linear-gradient(to right, transparent, black 10%, black 90%, transparent);
  -webkit-mask-image: linear-gradient(to right, transparent, black 10%, black 90%, transparent);
}

.marquee-inner {
  display: inline-flex;
  animation: marqueeScroll 30s linear infinite;
}

@keyframes marqueeScroll {
  from { transform: translateX(0); }
  to   { transform: translateX(-50%); }  /* 内容复制一份，平移 50% 实现无缝 */
}

/* ========== Hover 时暂停 ========== */
.marquee:hover .marquee-inner {
  animation-play-state: paused;
}

/* ========== 双行反向 Marquee ========== */
.marquee-row-1 .marquee-inner {
  animation-direction: normal;
}

.marquee-row-2 .marquee-inner {
  animation-direction: reverse;
  animation-duration: 25s;  /* 不同速度 = 更有机感 */
}
```

---

## 五、Creative CSS Effects（创意文字效果）

### 5.1 描边文字（Stroke Only）

```css
/* ========== 纯描边文字 ========== */
.outline-text {
  font-family: 'Clash Display', sans-serif;
  font-size: clamp(4rem, 12vw, 10rem);
  font-weight: 700;
  color: transparent;
  -webkit-text-stroke: 2px currentColor;  /* 描边宽度 + 颜色 */
  text-transform: uppercase;
  letter-spacing: -0.03em;
}

/* 粗描边版本 */
.outline-text-thick {
  color: transparent;
  -webkit-text-stroke: 3px var(--color-accent);
}

/* ========== Hover 时填充颜色 ========== */
.outline-fill-hover {
  color: transparent;
  -webkit-text-stroke: 2px var(--color-text);
  transition: color 0.4s ease, -webkit-text-stroke-color 0.4s ease;
}

.outline-fill-hover:hover {
  color: var(--color-text);
  -webkit-text-stroke-color: var(--color-text);
}
```

### 5.2 混合描边 + 填充（双层文字）

```css
/* ========== 使用 text-shadow 模拟双层 ========== */
.stroke-fill-text {
  font-family: 'Clash Display', sans-serif;
  font-size: clamp(3rem, 10vw, 8rem);
  font-weight: 700;
  color: var(--color-bg);                    /* 内部填充 = 背景色 */
  -webkit-text-stroke: 2px var(--color-accent);  /* 外部描边 = 强调色 */
  text-shadow:
    -4px -4px 0 var(--color-accent),
     4px -4px 0 var(--color-accent),
    -4px  4px 0 var(--color-accent),
     4px  4px 0 var(--color-accent);
}

/* ========== 复古 3D 文字效果 ========== */
.retro-3d-text {
  font-family: 'Clash Display', sans-serif;
  font-size: clamp(3rem, 8vw, 7rem);
  font-weight: 700;
  color: #fff;
  text-shadow:
    3px 3px 0 #000,
    6px 6px 0 #000,
    9px 9px 0 #000,
    12px 12px 0 #000;
  text-transform: uppercase;
}
```

### 5.3 图片 / 渐变填充文字

```css
/* ========== 渐变填充文字 ========== */
.gradient-text {
  font-family: 'Clash Display', sans-serif;
  font-size: clamp(3rem, 10vw, 8rem);
  font-weight: 700;
  background: linear-gradient(
    135deg,
    #667eea 0%,
    #764ba2 50%,
    #f093fb 100%
  );
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

/* ========== 动态渐变文字 ========== */
.animated-gradient-text {
  background: linear-gradient(
    90deg,
    #ff0000, #ff7700, #ffff00, #00ff00,
    #0000ff, #8b00ff, #ff0000
  );
  background-size: 300% 100%;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  animation: gradientShift 4s linear infinite;
}

@keyframes gradientShift {
  from { background-position: 0% 50%; }
  to   { background-position: 300% 50%; }
}

/* ========== 图片填充文字 ========== */
.image-text {
  font-family: 'Clash Display', sans-serif;
  font-size: clamp(5rem, 15vw, 12rem);
  font-weight: 900;
  background: url('/images/texture.jpg') center/cover;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  -webkit-text-stroke: 1px rgba(0,0,0,0.3);
}

/* ========== 视频/实时内容填充（伪元素方案） ========== */
.video-text-wrapper {
  position: relative;
  display: inline-block;
}

.video-text-wrapper::after {
  content: '';
  position: absolute;
  inset: 0;
  background: inherit;
  /* 或者使用 mix-blend-mode: source-atop */
  mask-image: url('text-mask.svg');  /* 文字形状的 SVG mask */
  -webkit-mask-image: url('text-mask.svg');
  mask-size: contain;
  -webkit-mask-size: contain;
  mask-repeat: no-repeat;
  -webkit-mask-repeat: no-repeat;
  mask-position: center;
  -webkit-mask-position: center;
}
```

### 5.4 竖排文字（日式美学）

```css
/* ========== 竖排文字（日本美学 + 编辑风格） ========== */
.vertical-text {
  writing-mode: vertical-rl;        /* 从右到左竖排 */
  text-orientation: mixed;          /* 中文保持竖排，英文旋转 90° */
  font-size: clamp(1rem, 1.5vw, 1.25rem);
  line-height: 2;
  letter-spacing: 0.1em;
  height: 100%;
}

/* 全竖排（英文也竖排） */
.vertical-text-force {
  writing-mode: vertical-rl;
  text-orientation: upright;        /* 所有字符竖排 */
  letter-spacing: 0.2em;
}

/* ========== 侧边竖排标签 ========== */
.side-label {
  writing-mode: vertical-rl;
  text-orientation: mixed;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  position: fixed;
  left: 1.5rem;
  top: 50%;
  transform: translateY(-50%) rotate(180deg); /* 翻转使文字底部朝上 */
}

/* ========== 日文特化排版 ========== */
.japanese-editorial {
  font-feature-settings: 'palt';    /* 比例字距，更舒适 */
  line-height: 2.2;                 /* 日文需要更大行高 */
  letter-spacing: 0.08em;
}
```

### 5.5 文字遮罩揭示（Mask Reveals）

```css
/* ========== 从下到上遮罩揭示 ========== */
.text-mask-reveal {
  position: relative;
  overflow: hidden;
  display: inline-block;
}

.text-mask-reveal::after {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--color-bg);
  transform-origin: top;
  animation: maskSlideUp 1s cubic-bezier(0.77, 0, 0.175, 1) 0.5s forwards;
}

@keyframes maskSlideUp {
  to { transform: scaleY(0); }
}

/* ========== 水平裁剪揭示 ========== */
.clip-reveal {
  clip-path: inset(0 100% 0 0);
  animation: clipReveal 1.2s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}

@keyframes clipReveal {
  to { clip-path: inset(0 0% 0 0); }
}

/* ========== 逐字缩放揭示 ========== */
@keyframes scaleReveal {
  from {
    opacity: 0;
    transform: scale(0.5) translateY(50%);
    filter: blur(10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
    filter: blur(0);
  }
}
```

---

## 六、Font Loading Strategy（字体加载策略）

### 6.1 自托管 WOFF2

```css
/* ========== 推荐的 @font-face 模板 ========== */
@font-face {
  font-family: 'Clash Display';
  src:
    local('Clash Display'),                          /* 1. 优先使用本地 */
    url('/fonts/ClashDisplay-Variable.woff2') format('woff2-variations'), /* 2. WOFF2 可变 */
    url('/fonts/ClashDisplay-Variable.woff2') format('woff2');           /* 3. WOFF2 回退 */
  font-weight: 200 900;
  font-style: normal;
  font-display: swap;                                /* 4. FOIT → FOUT */
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC,        /* 5. 子集化 */
    U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F,
    U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
```

### 6.2 font-display: swap 深入理解

```css
/* ========== font-display 各值对比 ========== */

/* swap（推荐）：立即显示后备字体，加载完后切换 */
/* 优点：文字立即可读；缺点：布局偏移（CLS） */
font-display: swap;

/* optional：只在极短时间内可用就显示，否则用后备字体 */
/* 优点：零 CLS；缺点：用户可能永远看到后备字体 */
font-display: optional;

/* fallback：短暂阻塞期（~100ms），然后 swap */
font-display: fallback;

/* block：最长阻塞 3 秒，之后无限 swap（默认） */
/* 不推荐：用户可能 3 秒看到白屏 */
font-display: block;
```

### 6.3 预加载关键字体

```html
<head>
  <!-- 预加载 Hero 区域使用的展示字体 -->
  <link rel="preload"
        href="/fonts/ClashDisplay-Variable.woff2"
        as="font"
        type="font/woff2"
        crossorigin="anonymous">

  <!-- 预加载导航使用的正文字体 -->
  <link rel="preload"
        href="/fonts/Satoshi-Variable.woff2"
        as="font"
        type="font/woff2"
        crossorigin="anonymous">
</head>
```

```css
/* ========== 使用 font-feature-settings 优化中文 ========== */
@font-face {
  font-family: 'Noto Sans SC';
  src: url('/fonts/NotoSansSC-Variable.woff2') format('woff2');
  font-weight: 100 900;
  font-display: swap;
  /* 中文字体巨大，必须子集化 */
  unicode-range: U+4E00-9FFF;     /* 基本汉字 */
}
```

### 6.4 size-adjust 减少 CLS

```css
/* ========== 使用 size-adjust 让后备字体尺寸匹配 ========== */
@font-face {
  font-family: 'Clash Display Fallback';
  src: local('Arial');
  ascent-override: 90%;
  descent-override: 22%;
  line-gap-override: 0%;
  size-adjust: 105%;               /* 调整整体缩放比例 */
}

/* 在 font-family 列表中先放 fallback */
.hero-title {
  font-family: 'Clash Display', 'Clash Display Fallback', sans-serif;
}

/* ========== 实战：Satoshi 的后备字体优化 ========== */
@font-face {
  font-family: 'Satoshi Fallback';
  src: local('Helvetica Neue'), local('Arial');
  ascent-override: 95.48%;
  descent-override: 27.74%;
  line-gap-override: 0%;
  size-adjust: 100.56%;
}

body {
  font-family: 'Satoshi', 'Satoshi Fallback', sans-serif;
}
```

### 6.5 Fontshare CDN 使用

```html
<!-- Fontshare 是 Indian Type Foundry 的免费字体 CDN -->
<!-- 直接使用，无需自托管 -->

<!-- 方式 1：CSS Link（简单） -->
<link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700&f[]=clash-display@600,700&display=swap" rel="stylesheet">

<!-- 方式 2：自托管版（性能更好，推荐生产环境） -->
<!-- 从 Fontshare 下载 WOFF2 后按 6.1 节方式部署 -->
```

```css
/* Fontshare 字体变量 */
:root {
  --font-clash: 'Clash Display', sans-serif;
  --font-satoshi: 'Satoshi', sans-serif;
  --font-cabinet: 'Cabinet Grotesk', sans-serif;
  --font-general: 'General Sans', sans-serif;
  --font-instrument-serif: 'Instrument Serif', serif;
}
```

### 6.6 字体加载优化清单

```css
/* ========== 完整优化策略 ========== */

/* 1. 只加载实际用到的字重（减少传输量） */
/* ❌ font-weight: 200 900  —— 如果只用 400 和 700 */
/* ✅ font-weight: 400 700 */

/* 2. 使用 unicode-range 分片加载 */
@font-face {
  font-family: 'MyFont';
  src: url('/fonts/MyFont-Latin.woff2') format('woff2');
  font-weight: 400;
  unicode-range: U+0000-00FF;    /* 拉丁文 */
}

@font-face {
  font-family: 'MyFont';
  src: url('/fonts/MyFont-CJK.woff2') format('woff2');
  font-weight: 400;
  unicode-range: U+4E00-9FFF;    /* 中文（按需加载） */
}

/* 3. 非关键字体延迟加载（使用 JS 动态插入） */
/* 在 Intersection Observer 触发后才加载字体 */

/* 4. 使用 link rel=modulepreload 预加载字体（现代方案） */
/* <link rel="modulepreload" href="/fonts/font.woff2" as="font" crossorigin> */
```

---

## 七、Rhythm and Spacing（韵律与间距）

### 7.1 Section 间距系统

```css
:root {
  /* ========== 基于 clamp 的响应式间距 ========== */
  --space-xs:  clamp(0.5rem,  0.4rem + 0.5vw,  1rem);     /* 8-16px */
  --space-sm:  clamp(1rem,    0.8rem + 1vw,    2rem);     /* 16-32px */
  --space-md:  clamp(2rem,    1.5rem + 2.5vw,  4rem);     /* 32-64px */
  --space-lg:  clamp(3rem,    2rem + 5vw,      6rem);     /* 48-96px */
  --space-xl:  clamp(4rem,    2rem + 8vw,      10rem);    /* 64-160px */
  --space-2xl: clamp(6rem,    2rem + 14vw,     16rem);    /* 96-256px */

  /* ========== 8px 基线网格（可选， stricter） ========== */
  --baseline: 8px;
}

/* 区块间距 */
section {
  padding-block: var(--space-xl);
}

.hero-section {
  padding-block: var(--space-2xl);
  min-height: 100svh;
}
```

### 7.2 行高规则

```css
/* ========== 行高规范 ========== */
:root {
  /* 大标题：紧行高 —— 因为字号大，绝对值已经足够 */
  --lh-tight:  0.85;

  /* H2/H3：稍松 */
  --lh-snug:   1.1;

  /* 正文：标准 */
  --lh-normal: 1.65;

  /* 宽屏正文（短行宽时用更松的行高） */
  --lh-relaxed: 1.8;

  /* 无行高：用于 logo、标签 */
  --lh-none: 1;
}

.display { line-height: var(--lh-tight); }
h1, h2, h3 { line-height: var(--lh-snug); }
p          { line-height: var(--lh-normal); }

/* 长文阅读优化 */
.longform p {
  line-height: var(--lh-relaxed);
  max-width: 65ch;  /* 每行 45-75 个字符最佳 */
}
```

### 7.3 最大宽度与可读性

```css
/* ========== 阅读宽度控制 ========== */
body {
  max-width: 1400px;
  margin-inline: auto;
  padding-inline: clamp(1.5rem, 5vw, 4rem);
}

/* 正文段落 —— 黄金阅读宽度 */
p, .prose {
  max-width: 65ch;  /* ~65 个字符 = 最佳阅读体验 */
}

/* 导航 —— 不要太宽 */
nav {
  max-width: 1600px;
  margin-inline: auto;
}

/* 列表 / 标签行 */
.tag-list {
  max-width: 80ch;
}

/* 大标题可以更宽 */
h1 {
  max-width: 90%;
}

/* ========== 段落间距 ========== */
/* 使用 margin-top 而非 margin-bottom（BFC 坍缩原理） */
h2 {
  margin-block-start: var(--space-lg);
  margin-block-end: var(--space-sm);
}

p + p {
  margin-block-start: 1em;
}
```

### 7.4 等宽数字（Tabular Nums）

```css
/* ========== 等宽数字 —— 统计数据、价格、表格 ========== */
.stat-number,
.price,
.data-cell,
.table-row {
  font-variant-numeric: tabular-nums;
}

/* ========== 老式数字 —— 编辑、文学排版 ========== */
.editorial-body {
  font-variant-numeric: oldstyle-nums;  /* 降序数字更优雅 */
}

/* ========== 完整数字排版示例 ========== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-md);
}

.stat-item {
  font-family: 'Space Mono', monospace;
  font-variant-numeric: tabular-nums;
}

.stat-value {
  font-size: clamp(2rem, 5vw, 4rem);
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.03em;
}

.stat-label {
  font-size: var(--fs-xs);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-top: var(--space-xs);
  color: var(--color-muted);
}
```

### 7.5 垂直韵律速查

```css
/* ========== 完整排版韵律系统 ========== */
:root {
  /* 行高统一为基线的倍数 */
  --rhythm: 1.75rem;  /* 28px，正文行高 */

  /* 所有间距为 rhythm 的倍数 */
  --rhythm-1: calc(var(--rhythm) * 1);   /* 28px */
  --rhythm-2: calc(var(--rhythm) * 2);   /* 56px */
  --rhythm-3: calc(var(--rhythm) * 3);   /* 84px */
  --rhythm-4: calc(var(--rhythm) * 4);   /* 112px */

  /* 字号系统（行高映射） */
  --text-2xs: 0.75rem;    line-height: var(--rhythm);  /* padding: 0.53rhythm */
  --text-xs:  0.875rem;   line-height: var(--rhythm);
  --text-sm:  1rem;       line-height: var(--rhythm);
  --text-base: 1.125rem;  line-height: var(--rhythm);
  --text-lg:  1.375rem;   line-height: calc(var(--rhythm) * 1.5);
  --text-xl:  1.75rem;    line-height: calc(var(--rhythm) * 2);
  --text-2xl: 2.5rem;     line-height: calc(var(--rhythm) * 2);
  --text-3xl: 3.5rem;     line-height: calc(var(--rhythm) * 3);
}

/* 使用 clamp 包装，保持韵律的同时响应式 */
:root {
  --text-3xl-clamped: clamp(2.5rem, 2rem + 4vw, 3.5rem);
  --text-hero-clamped: clamp(4rem, 2rem + 12vw, 10rem);
}
```

---

## 附录：快速参考卡片

### A. CSS 变量完整模板

```css
/* ========== 复制即用的排版系统 ========== */
:root {
  /* 字体 */
  --font-display: 'Clash Display Variable', sans-serif;
  --font-body: 'Satoshi Variable', sans-serif;
  --font-mono: 'Space Mono', monospace;

  /* 字号 */
  --fs-hero:  clamp(5rem, 2rem + 16vw, 12.5rem);
  --fs-h1:    clamp(3.5rem, 1.5rem + 8vw, 8rem);
  --fs-h2:    clamp(2.5rem, 1.5rem + 4vw, 5rem);
  --fs-h3:    clamp(1.75rem, 1.3rem + 2vw, 3rem);
  --fs-body:  clamp(1rem, 0.95rem + 0.25vw, 1.0625rem);
  --fs-small: clamp(0.75rem, 0.7rem + 0.25vw, 0.8125rem);

  /* 间距 */
  --space-section: clamp(4rem, 2rem + 8vw, 10rem);

  /* 行高 */
  --lh-display: 0.85;
  --lh-heading: 1.1;
  --lh-body: 1.75;

  /* 字距 */
  --tracking-tight: -0.05em;
  --tracking-normal: 0;
  --tracking-wide: 0.08em;
}
```

### B. 性能检查清单

- [ ] 使用可变字体（Variable Fonts）减少文件数
- [ ] 所有 `@font-face` 设置 `font-display: swap`
- [ ] Hero 区域字体使用 `<link rel="preload">`
- [ ] 为后备字体配置 `size-adjust` 减少 CLS
- [ ] 中文字体使用 `unicode-range` 子集化
- [ ] 字体文件通过 `<link>` 而非 `@import` 加载
- [ ] 使用 `font-variation-settings` 而非离散 `font-weight`（可变字体）
- [ ] 大标题使用 `text-transform` 而非手动输入大写（文件体积优化）

### C. Awwwards 2025 排版趋势速览

| 趋势 | 关键技术 | 代表效果 |
|------|---------|---------|
| 超大标题 | `clamp()` + `letter-spacing: -0.05em` | 200px 紧缩大字 |
| 可变字体动画 | `font-variation-settings` transition | Hover 时粗细平滑变化 |
| 描边文字 | `-webkit-text-stroke` | 大面积描边标题 |
| 渐变填充 | `background-clip: text` | 彩虹渐变 / 品牌色渐变 |
| 竖排文字 | `writing-mode: vertical-rl` | 侧边标签 / 日式排版 |
| 无限 Marquee | CSS `@keyframes` + `translateX(-50%)` | 技能标签 / 品牌滚动 |
| Scroll 驱动 | `animation-timeline: scroll()` | 文字随滚动渐现 |
| 双层字体 | Outline + Fill 叠加 | Hover 填充揭示 |
