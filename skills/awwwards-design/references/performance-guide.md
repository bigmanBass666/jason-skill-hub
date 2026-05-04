# Awwwards 级网站性能优化指南

> 面向获得 Awwwards 认可的高端创意网站，平衡视觉表现力与加载性能。
> 核心理念：**首屏快、交互顺、资源省、体感佳。**

---

## 目录

1. [Core Web Vitals 深度指南](#1-core-web-vitals-深度指南)
2. [图片优化](#2-图片优化)
3. [字体优化](#3-字体优化)
4. [JavaScript 性能](#4-javascript-性能)
5. [CSS 性能](#5-css-性能)
6. [3D/WebGL 性能](#6-3dwebgl-性能)
7. [构建与部署优化](#7-构建与部署优化)
8. [性能预算模板](#8-性能预算模板)

---

## 1. Core Web Vitals 深度指南

### 1.1 LCP（Largest Contentful Paint）目标 < 1.5s

LCP 衡量视口内最大内容元素的渲染时间，通常是 hero 图片、大标题或背景视频。

**优化策略：**

```html
<!-- ① Preload hero 图片 -->
<link rel="preload" as="image" href="/hero.avif" type="image/avif" fetchpriority="high">

<!-- ② Preload 关键字体 -->
<link rel="preload" as="font" href="/fonts/headline.woff2" type="font/woff2" crossorigin>

<!-- ③ 关键 CSS 内联，避免渲染阻塞 -->
<style>
  /* 仅包含首屏关键样式 */
  .hero { background: #000; min-height: 100vh; }
  .hero-title { font-family: 'Headline', sans-serif; font-size: clamp(2rem, 8vw, 6rem); }
</style>

<!-- ④ 非关键 CSS 异步加载 -->
<link rel="stylesheet" href="/styles/main.css" media="print" onload="this.media='all'">
```

**服务端优化：**

```nginx
# Nginx: 启用 Brotli + 缓存静态资源
location ~* \.(avif|webp|woff2|js|css)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    brotli_static on;
}

# 启用 Early Hints（需要 Nginx 1.25.3+）
add_header Link "</hero.avif>; rel=preload; as=image; type=image/avif" early;
```

```javascript
// ⑤ CDN 边缘缓存策略示例（Vercel / Cloudflare Workers）
// vercel.json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" }
      ]
    }
  ]
}
```

> **实战提示：** Awwwards SOTD 头奖网站通常使用 SSR/SSG 预渲染首屏 HTML，确保爬虫和首屏访问都能在 < 1s 内获得完整内容。Next.js 的 `generateStaticParams` + ISR 是常见选择。

---

### 1.2 CLS（Cumulative Layout Shift）目标 < 0.05

CLS 衡量页面加载过程中元素的意外位移。

**关键措施：**

```css
/* ① 图片始终设置宽高比 */
.hero-image {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
}

/* ② 字体使用 size-adjust 消除 FOIT 导致的布局偏移 */
@font-face {
  font-family: 'Display';
  src: url('/fonts/display.woff2') format('woff2');
  font-weight: 700;
  font-style: normal;
  font-display: swap;
  size-adjust: 105%;        /* 微调垂直尺寸 */
  ascent-override: 90%;     /* 校正基线 */
  descent-override: 25%;
}

/* ③ 动态内容预留空间（骨架屏 / 插槽） */
.ad-slot,
.dynamic-content {
  min-height: 250px;        /* 为广告 / 异步内容预留最小高度 */
  contain: layout style;    /* 隔离布局计算 */
}

/* ④ 为字体设置明确的 fallback 尺寸 */
body {
  font-family: 'Body', system-ui, -apple-system, sans-serif;
  /* fallback 字体行高应与主字体匹配 */
  line-height: 1.5;
}
```

```html
<!-- ⑤ 图片使用 width/height 属性（浏览器据此计算纵横比） -->
<img
  src="/hero.avif"
  width="1200"
  height="675"
  alt="Hero"
  loading="eager"
  fetchpriority="high"
>
```

> **实战提示：** 使用 `font-style-matcher` 工具比对 Web 字体与系统 fallback 的度量差异，精确设置 `size-adjust`。

---

### 1.3 INP（Interaction to Next Paint）目标 < 100ms

INP 替代 FID，衡量所有用户交互（点击、按键、拖拽）的响应延迟。

**优化策略：**

> 完整的 `debounce`/`throttle` 实现参见 `scripts/performance-utils.js`。

```javascript
// ③ 使用示例：滚动驱动动画
const handleScroll = throttle(() => {
  const y = window.scrollY;
  document.querySelector('.parallax').style.transform = `translateY(${y * 0.3}px)`;
});
window.addEventListener('scroll', handleScroll, { passive: true });

// ④ Web Worker 处理重计算
const worker = new Worker('/workers/heavy-calc.js');
worker.postMessage({ data: largeDataset });
worker.onmessage = (e) => {
  renderResults(e.data); // 主线程仅负责渲染
};
```

```javascript
// workers/heavy-calc.js
self.onmessage = (e) => {
  const result = expensiveComputation(e.data);
  self.postMessage(result);
};

function expensiveComputation(data) {
  // 粒子物理、复杂排序、图像处理等
  return data.map(item => /* ... */);
}
```

**主线程优化清单：**
- 避免长任务（> 50ms），使用 `scheduler.postTask()` 或 `setTimeout(..., 0)` 分片
- 动画一律使用 `requestAnimationFrame`，不使用 `setInterval` / `setTimeout`
- 使用 `event.isTrusted` 检测真实用户交互
- 虚拟列表处理大数据集渲染

---

### 1.4 测量工具

| 工具 | 用途 | 特点 |
|------|------|------|
| **Lighthouse** | 综合评分 + Web Vitals | CI 集成，自动化回归 |
| **Chrome Web Vitals 扩展** | 实时监控真实用户指标 | 桌面端实时显示 LCP/CLS/INP |
| **Chrome DevTools → Performance** | 火焰图 + 长任务分析 | 逐帧分析渲染瓶颈 |
| **Chrome DevTools → Coverage** | 检测未使用的 JS/CSS | 识别冗余代码 |
| **web-vitals 库** | 生产环境 RUM 采集 | `npm i web-vitals` |

```javascript
// 生产环境 Web Vitals 上报（Next.js App Router）
import { onLCP, onCLS, onINP, onFCP, onTTFB } from 'web-vitals';

function sendToAnalytics(metric) {
  const body = JSON.stringify({
    name: metric.name,
    value: metric.value,
    rating: metric.rating,
    navigationType: metric.navigationType,
  });
  // 发送到分析端点
  if (navigator.sendBeacon) {
    navigator.sendBeacon('/api/vitals', body);
  } else {
    fetch('/api/vitals', { body, method: 'POST', keepalive: true });
  }
}

onLCP(sendToAnalytics);
onCLS(sendToAnalytics);
onINP(sendToAnalytics);
onFCP(sendToAnalytics);
onTTFB(sendToAnalytics);
```

---

## 2. 图片优化

### 2.1 现代格式优先：AVIF > WebP > JPEG

```html
<picture>
  <!-- AVIF：最佳压缩率，主流浏览器已支持 -->
  <source
    type="image/avif"
    srcset="
      /hero-400.avif 400w,
      /hero-800.avif 800w,
      /hero-1200.avif 1200w,
      /hero-1600.avif 1600w
    "
    sizes="100vw"
  >
  <!-- WebP：兼容性回退 -->
  <source
    type="image/webp"
    srcset="
      /hero-400.webp 400w,
      /hero-800.webp 800w,
      /hero-1200.webp 1200w,
      /hero-1600.webp 1600w
    "
    sizes="100vw"
  >
  <!-- JPEG：最终回退 -->
  <img
    src="/hero-800.jpg"
    srcset="
      /hero-400.jpg 400w,
      /hero-800.jpg 800w,
      /hero-1200.jpg 1200w
    "
    sizes="100vw"
    alt="Hero"
    width="1600"
    height="900"
    loading="eager"
    fetchpriority="high"
    decoding="async"
  >
</picture>
```

### 2.2 模糊占位符（LQIP / BlurHash）

```javascript
// Next.js Image 组件原生支持 blurDataURL
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Hero"
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,/9j/4AAQ..." // 20x20 的极低质量 base64
  width={1600}
  height={900}
  priority
/>
```

```css
/* 纯 CSS 实现 LQIP 效果 */
.hero-image-wrapper {
  position: relative;
  background: url('/hero-lqip.webp') center/cover no-repeat;
  filter: blur(20px);
  transform: scale(1.1); /* 避免模糊边缘白缝 */
}

.hero-image-wrapper img {
  position: relative;
  z-index: 1;
  transition: opacity 0.4s ease;
}

.hero-image-wrapper img.loaded {
  /* 高清图加载完成，覆盖模糊底图 */
}
```

### 2.3 懒加载（Intersection Observer）

```javascript
class LazyImage {
  constructor(img) {
    this.img = img;
    this.observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            this.load();
            this.observer.disconnect();
          }
        });
      },
      { rootMargin: '200px 0px' } // 提前 200px 开始加载
    );
    this.observer.observe(img);
  }

  load() {
    const src = this.img.dataset.src;
    if (!src) return;

    // 用 fetch 预加载 + 解码，避免渲染卡顿
    fetch(src)
      .then(res => res.blob())
      .then(blob => createImageBitmap(blob))
      .then(bitmap => {
        this.img.src = URL.createObjectURL(blob);
        this.img.onload = () => URL.revokeObjectURL(this.img.src);
        this.img.classList.add('loaded');
      });
  }
}

document.querySelectorAll('img[data-src]').forEach(img => new LazyImage(img));
```

### 2.4 视频优化

```html
<video
  autoplay
  muted
  loop
  playsinline
  preload="auto"
  poster="/hero-poster.jpg"  <!-- 帧截图作为回退 -->
  width="1600"
  height="900"
>
  <!-- H.264 编码，兼容性最佳 -->
  <source src="/hero-loop.mp4" type="video/mp4">
</video>

<style>
  video {
    object-fit: cover;
    width: 100%;
    height: 100%;
  }
</style>
```

> **实战提示：** Hero 循环视频控制在 < 2MB，时长 5-15 秒，分辨率 1280x720（移动端降至 640x360）。使用 HandBrake / FFmpeg 压缩：`ffmpeg -i input.mp4 -c:v libx264 -crf 28 -preset slow -an -t 10 output.mp4`

---

## 3. 字体优化

### 3.1 WOFF2 自托管 + font-display

```css
@font-face {
  font-family: 'Headline';
  src: url('/fonts/headline.woff2') format('woff2');
  font-weight: 700;
  font-style: normal;
  font-display: swap;          /* 先显示 fallback，字体加载完再替换 */
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6,
    U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193,
    U+2212, U+2215, U+FEFF, U+FFFD; /* 仅加载拉丁字符子集 */
}
```

### 3.2 Preload 关键字体

```html
<!-- 仅 preload 首屏可见文字所用的字体文件 -->
<link
  rel="preload"
  as="font"
  href="/fonts/headline.woff2"
  type="font/woff2"
  crossorigin="anonymous"
>
```

> **注意：** 不要 preload 所有字体，仅预加载 LCP 元素（hero 标题）所需的 1-2 个字体文件。

### 3.3 Variable Fonts（可变字体）

```css
/* 可变字体：一个文件包含所有字重，节省请求和体积 */
@font-face {
  font-family: 'Body';
  src: url('/fonts/body-var.woff2') format('woff2') tech('variations');
  font-weight: 300 900;  /* 字重范围 */
  font-style: oblique 0deg 12deg;  /* 支持可变斜体 */
  font-display: swap;
}

/* 单文件 vs 多文件对比 */
/* 可变字体：1 个文件，~80KB（覆盖 300-900 所有字重） */
/* 固定字重：6 个文件（300/400/500/600/700/900），总计 ~120KB + 6 个 HTTP 请求 */
```

> **权衡：** 可变字体首次加载略大，但整体传输量更小、HTTP 请求更少。Awwwards 网站通常使用可变字体来提供精细的排版控制。

### 3.4 CLS 字体度量校准

```css
/* 使用 @font-face 描述符精确匹配 fallback 度量 */
@font-face {
  font-family: 'Display';
  src: url('/fonts/display.woff2') format('woff2');
  font-weight: 800;
  font-display: swap;
  /* 以下数值通过 font-style-matcher 工具获取 */
  ascent-override: 85%;
  descent-override: 20%;
  line-gap-override: 0%;
  size-adjust: 108%;
}
```

**工作流程：**
1. 在 [font-style-matcher](https://meowni.ca/font-style-matcher/) 中打开 Web 字体
2. 调整滑块，直到 Web 字体与系统 fallback 完全对齐
3. 复制生成的 `size-adjust` / `ascent-override` 等数值
4. 粘贴到 `@font-face` 声明中

---

## 4. JavaScript 性能

### 4.1 动态导入重库

```javascript
// ❌ 静态导入 — 所有页面都会加载 Three.js（~600KB）
import * as THREE from 'three';
import { Canvas } from '@react-three/fiber';

// ✅ 动态导入 — 仅在需要时加载
async function init3DScene() {
  const THREE = await import('three');
  const { OrbitControls } = await import('three/examples/jsm/controls/OrbitControls.js');

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  // ...
}

// 在用户交互或可见时触发加载
const observer = new IntersectionObserver((entries) => {
  if (entries[0].isIntersecting) {
    init3DScene();
    observer.disconnect();
  }
}, { threshold: 0.1 });

observer.observe(document.getElementById('webgl-container'));
```

```javascript
// GSAP 动态导入示例
async function playEntryAnimation() {
  const { gsap } = await import('gsap');
  const { ScrollTrigger } = await import('gsap/ScrollTrigger');
  gsap.registerPlugin(ScrollTrigger);

  gsap.from('.hero-title', {
    y: 100,
    opacity: 0,
    duration: 1.2,
    ease: 'power3.out',
  });
}
```

### 4.2 requestAnimationFrame 代替 scroll 事件

```javascript
// ❌ 直接绑定 scroll 事件 — 可能每秒触发 60+ 次
window.addEventListener('scroll', () => {
  document.querySelector('.parallax').style.transform = `translateY(${window.scrollY}px)`;
});

// ✅ rAF 节流 + passive 事件
let ticking = false;
window.addEventListener('scroll', () => {
  if (!ticking) {
    requestAnimationFrame(() => {
      const y = window.scrollY;
      document.querySelector('.parallax').style.transform = `translateY(${y * 0.5}px)`;
      ticking = false;
    });
    ticking = true;
  }
}, { passive: true }); // passive 声明不会阻塞滚动
```

### 4.3 防抖 / 节流工具库

> 完整的 `debounce`/`throttle` 实现参见 `scripts/performance-utils.js`，包含 TypeScript 类型注释、cancel 功能和 leading/trailing 模式。

```javascript
// 使用示例：从 scripts/performance-utils.js 导入
import { debounce, throttle } from './scripts/performance-utils.js';

const handleResize = debounce(() => {
  recalculateLayout();
  ScrollTrigger.refresh(); // GSAP ScrollTrigger 需要在 resize 后刷新
}, 200);

const handleMouseMove = throttle((e) => {
  updateCursor(e.clientX, e.clientY);
}, 16); // ~60fps
```

### 4.4 Tree-Shaking

```javascript
// ❌ 导入整个库
import _ from 'lodash';              // ~70KB
import { animate } from 'animejs';   // 可能拉入全部代码

// ✅ 仅导入需要的函数
import cloneDeep from 'lodash/cloneDeep';  // ~2KB

// ✅ Lodash ES Module 版本天然支持 tree-shaking
import { cloneDeep, debounce } from 'lodash-es';
```

```javascript
// webpack/rollup 的 sideEffects 声明（package.json）
// 确保 tree-shaking 能正确移除未使用代码
{
  "sideEffects": false,
  // 或指定有副作用的文件
  "sideEffects": ["./src/polyfills.ts"]
}
```

---

## 5. CSS 性能

### 5.1 will-change 使用指南

```css
/* ✅ 在动画即将开始前声明，动画结束后移除 */
.parallax-element {
  will-change: transform;
}

.parallax-element.is-animating {
  /* 浏览器将在动画期间为其创建独立合成层 */
}

/* ❌ 不要滥用 will-change */
* { will-change: transform; }
/* 这会导致 GPU 内存暴涨，移动端尤其危险 */

/* ✅ 使用 JavaScript 动态管理 will-change */
```

```javascript
// 在动画开始前添加 will-change
element.addEventListener('mouseenter', () => {
  element.style.willChange = 'transform, opacity';
});

// 动画结束后移除
element.addEventListener('animationend', () => {
  element.style.willChange = 'auto';
});
```

### 5.2 CSS Containment

```css
/* 隔离元素的布局、样式、绘制，减少浏览器重算范围 */
.card {
  contain: layout style paint;
}

/* 更细粒度的控制 */
.sidebar {
  contain: layout style;    /* 侧边栏变化不影响主内容区布局 */
}

.offscreen-canvas {
  contain: strict;          /* 等同于 contain: size layout style paint */
  content-visibility: auto; /* 滚动外时跳过渲染 */
}
```

### 5.3 仅使用 transform/opacity 做动画

```css
/* ✅ GPU 合成层属性 — 不触发 layout 或 paint */
.smooth-entrance {
  animation: fadeSlideUp 0.6s ease-out;
}

@keyframes fadeSlideUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ❌ 触发 layout + paint — 性能差 */
.bad-animation {
  animation: badSlide 0.6s ease-out;
}

@keyframes badSlide {
  from {
    margin-top: 40px;       /* 触发 layout */
    width: 80%;             /* 触发 layout */
    background: red;        /* 触发 paint */
  }
}
```

### 5.4 避免 Layout Thrashing

```javascript
// ❌ 读写交替 → 强制同步布局
elements.forEach(el => {
  const height = el.offsetHeight;       // 读 → 触发 layout
  el.style.height = height + 10 + 'px'; // 写 → 脏标记
  // 下一次循环再次读取时，浏览器被迫重新计算 layout
});

// ✅ 批量读取 → 批量写入
const heights = elements.map(el => el.offsetHeight); // 批量读
elements.forEach((el, i) => {
  el.style.height = heights[i] + 10 + 'px';         // 批量写
});
```

### 5.5 关键 CSS 内联

```javascript
// 使用 Critters（Webpack 插件）或 inline-critical 自动提取关键 CSS
// next.config.js
module.exports = {
  experimental: {
    optimizeCss: true, // Next.js 内置 Critical CSS 提取
  },
};

// 独立工具方案
// npm i -D critters-webpack-plugin
const Critters = require('critters-webpack-plugin');
module.exports = {
  plugins: [
    new Critters({
      preload: 'swap',      // 字体加载策略
      inlineFonts: false,   // 不内联字体
    }),
  ],
};
```

---

## 6. 3D/WebGL 性能

### 6.1 延迟初始化 WebGL

> 完整的 `LazyWebGL` 类实现（含 pause/resume）参见 `scripts/performance-utils.js`。
> WebGL 初始化和渲染优化模式，参见 `references/webgl-patterns.md`。

### 6.2 GPU 层级检测

```javascript
import detectGPU from 'detect-gpu';

async function getQualitySettings() {
  const gpu = await detectGPU();
  const tier = gpu.tier; // 0-3，数字越大性能越强
  const isMobile = /Mobi|Android/i.test(navigator.userAgent);

  return {
    pixelRatio: isMobile ? 1 : Math.min(window.devicePixelRatio, 2),
    shadowMapSize: tier >= 2 ? 2048 : 1024,
    antialias: tier >= 2,
    particleCount: isMobile ? 500 : tier >= 2 ? 5000 : 2000,
    postProcessing: tier >= 2, // 移动端关闭后处理
    textureSize: isMobile ? 1024 : tier >= 2 ? 2048 : 1024,
  };
}
```

### 6.3 像素比上限

```javascript
const renderer = new THREE.WebGLRenderer({ antialias: true });
const MAX_DPR = 2; // 限制最大像素比，避免 3x/4x 屏幕性能问题
renderer.setPixelRatio(Math.min(window.devicePixelRatio, MAX_DPR));
renderer.setSize(container.clientWidth, container.clientHeight);
```

### 6.4 资源释放模式

> 完整的 `disposeScene()` 实现参见 `scripts/performance-utils.js`。

### 6.5 粒子对象池

```javascript
class ParticlePool {
  constructor(maxParticles) {
    this.maxParticles = maxParticles;
    this.particles = [];
    this.activeCount = 0;

    // 预分配所有粒子
    for (let i = 0; i < maxParticles; i++) {
      this.particles.push({
        position: new Float32Array(3),
        velocity: new Float32Array(3),
        life: 0,
        active: false,
      });
    }
  }

  emit(position, velocity) {
    const p = this.particles[this.activeCount % this.maxParticles];
    p.position.set(position);
    p.velocity.set(velocity);
    p.life = 1.0;
    p.active = true;
    this.activeCount++;
  }

  update(dt) {
    for (let i = 0; i < this.maxParticles; i++) {
      const p = this.particles[i];
      if (!p.active) continue;
      p.life -= dt;
      if (p.life <= 0) {
        p.active = false;
        continue;
      }
      p.position[0] += p.velocity[0] * dt;
      p.position[1] += p.velocity[1] * dt;
      p.position[2] += p.velocity[2] * dt;
    }
  }
}
```

### 6.6 LOD（Level of Detail）

```javascript
import { LOD } from 'three';

function createLODModel() {
  const lod = new LOD();

  // 高细节（近距离）
  lod.addLevel(highDetailMesh, 0);

  // 中细节（中距离）
  lod.addLevel(mediumDetailMesh, 50);

  // 低细节（远距离）
  lod.addLevel(lowDetailMesh, 150);

  // 仅保留包围盒（极远距离）
  lod.addLevel(boundingBoxMesh, 300);

  return lod;
}

// 在渲染循环中自动更新
scene.add(lod);
// Three.js 会根据相机距离自动切换细节层级
```

---

## 7. 构建与部署优化

### 7.1 Next.js Image 组件

```tsx
import Image from 'next/image';

export default function Hero() {
  return (
    <div className="relative w-full h-screen">
      {/* 自动处理：格式转换、响应式、懒加载、占位符 */}
      <Image
        src="/hero.jpg"
        alt="Hero background"
        fill
        sizes="100vw"
        quality={85}       // AVIF/WebP 质量
        priority            // 首屏图片，预加载
        placeholder="blur"
        blurDataURL="/hero-lqip.webp"
      />
      <div className="relative z-10 flex items-center justify-center h-full">
        <h1 className="text-6xl font-bold">标题</h1>
      </div>
    </div>
  );
}
```

### 7.2 代码分割策略

```javascript
// next.config.js — 路由级代码分割（Next.js 默认行为）
module.exports = {
  experimental: {
    optimizePackageImports: [
      'three',
      'gsap',
      'framer-motion',
      'lodash',
      'd3',
    ],
  },
};

// 手动动态导入（组件级）
import dynamic from 'next/dynamic';

const Heavy3DScene = dynamic(() => import('@/components/3DScene'), {
  loading: () => <div className="animate-pulse bg-gray-200 h-screen" />,
  ssr: false, // WebGL 组件不需要 SSR
});

const ContactForm = dynamic(() => import('@/components/ContactForm'), {
  loading: () => <SkeletonForm />,
});
```

### 7.3 Edge / CDN 部署

```javascript
// Vercel Edge Middleware — 基于地理位置 / 设备的动态优化
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const response = NextResponse.next();
  const country = request.geo?.country;

  // 为不同地区设置不同的缓存策略
  response.headers.set('X-Country', country || 'unknown');

  return response;
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

### 7.4 Prefetching（next/link）

```tsx
import Link from 'next/link';

export default function Navigation() {
  return (
    <nav>
      {/* next/link 默认在链接进入视口时 prefetch */}
      <Link href="/about" prefetch={true}>
        关于我们
      </Link>

      {/* 低优先级页面可关闭自动 prefetch */}
      <Link href="/terms" prefetch={false}>
        服务条款
      </Link>
    </nav>
  );
}
```

### 7.5 Bundle 分析

```bash
# 安装分析工具
npm i -D @next/bundle-analyzer

# next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
  // ... 其他配置
});

# 运行分析
ANALYZE=true npm run build
```

```javascript
// 使用 webpack-bundle-analyzer 查看依赖占比
// 识别哪些库占用了过多的 bundle 体积
// 常见优化目标：
// - moment.js → date-fns 或 dayjs（~2KB vs ~300KB）
// - lodash → lodash-es（tree-shakeable）
// - three.js → 动态导入 + 按需引入
```

---

## 8. 性能预算模板

### 8.1 预算定义

```javascript
// performance-budget.json — 可集成到 Lighthouse CI
[
  {
    "path": "/*",
    "options": {
      "preset": "desktop"
    },
    "budgets": [
      {
        "resourceType": "document",
        "budget": 30                 // HTML < 30KB
      },
      {
        "resourceType": "script",
        "budget": 200,               // JS < 200KB（压缩后）
        "warning": 150
      },
      {
        "resourceType": "stylesheet",
        "budget": 50,                // CSS < 50KB（压缩后）
        "warning": 30
      },
      {
        "resourceType": "font",
        "budget": 100,               // 字体 < 100KB 总计
        "warning": 75
      },
      {
        "resourceType": "image",
        "budget": 500,               // 首屏图片 < 500KB
        "warning": 300
      },
      {
        "resourceType": "media",
        "budget": 1500               // 视频 < 1.5MB
      },
      {
        "resourceType": "total",
        "budget": 3000               // 总页面 < 3MB
      }
    ]
  }
]
```

### 8.2 资源预算总表

| 资源类型 | 预算上限 | 警告阈值 | 关键策略 |
|---------|---------|---------|---------|
| **HTML** | 30 KB | 20 KB | SSG/SSR，压缩，去除冗余 |
| **JavaScript** | 200 KB | 150 KB | Tree-shaking，动态导入，代码分割 |
| **CSS** | 50 KB | 30 KB | 关键 CSS 内联，PurgeCSS，Tailwind |
| **字体** | 100 KB | 75 KB | WOFF2，可变字体，unicode-range 子集 |
| **首屏图片** | 500 KB | 300 KB | AVIF，响应式 srcset，LQIP |
| **3D 资产** | 500 KB | 300 KB | GLTF Draco 压缩，LOD，延迟加载 |
| **视频** | 1.5 MB | 1 MB | H.264，短循环，低分辨率 |
| **页面总重** | 3 MB | 2 MB | 全部策略综合应用 |
| **HTTP 请求数** | 50 | 30 | 合并资源，HTTP/2 复用 |

### 8.3 CI 集成检查

```yaml
# .github/workflows/performance.yml
name: Performance Budget

on: [pull_request]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: treosh/lighthouse-ci-action@v11
        with:
          configPath: ./lighthouserc.json
          budgetPath: ./performance-budget.json
          uploadArtifacts: true
```

```json
// lighthouserc.json
{
  "ci": {
    "collect": {
      "staticDistDir": "./out",
      "settings": {
        "preset": "desktop"
      }
    },
    "assert": {
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.9 }],
        "categories:accessibility": ["error", { "minScore": 0.85 }],
        "first-contentful-paint": ["error", { "maxNumericValue": 1500 }],
        "largest-contentful-paint": ["error", { "maxNumericValue": 2000 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.05 }],
        "total-blocking-time": ["error", { "maxNumericValue": 200 }],
        "interactive": ["error", { "maxNumericValue": 3000 }]
      }
    }
  }
}
```

### 8.4 运行时性能监控

```javascript
// 实时性能预算超限提醒（开发环境）
if (process.env.NODE_ENV === 'development') {
  setInterval(() => {
    const entries = performance.getEntriesByType('resource');
    const totalSize = entries.reduce((sum, entry) => sum + (entry.transferSize || 0), 0);
    const jsSize = entries
      .filter(e => e.name.endsWith('.js'))
      .reduce((sum, e) => sum + (e.transferSize || 0), 0);

    if (jsSize > 200 * 1024) {
      console.warn(
        `%c⚠ JS Bundle 超出预算: ${(jsSize / 1024).toFixed(1)}KB / 200KB`,
        'color: orange; font-weight: bold; font-size: 14px;'
      );
    }

    if (totalSize > 3 * 1024 * 1024) {
      console.warn(
        `%c⚠ 页面总大小超出预算: ${(totalSize / 1024 / 1024).toFixed(2)}MB / 3MB`,
        'color: red; font-weight: bold; font-size: 14px;'
      );
    }
  }, 5000);
}
```

---

## 附录：快速检查清单

### 发布前必检

- [ ] Lighthouse Performance > 90（桌面端）
- [ ] LCP < 1.5s，CLS < 0.05，INP < 100ms
- [ ] 页面总大小 < 3MB
- [ ] JS Bundle < 200KB（gzip）
- [ ] 所有图片使用 AVIF/WebP + srcset
- [ ] 字体 WOFF2 自托管 + font-display: swap
- [ ] 3D 资产延迟加载 + GPU 分级
- [ ] 移动端 Pixel Ratio ≤ 2
- [ ] 动画仅使用 transform/opacity
- [ ] 无 Layout Thrashing（批量 DOM 读写）
- [ ] CDN 缓存策略正确（immutable + long max-age）
- [ ] Web Vitals 上报到分析平台

### Awwwards 专项

- [ ] 页面加载有精心设计的加载动画（loading sequence）
- [ ] 3D/WebGL 场景与页面叙事融为一体
- [ ] 滚动体验流畅（60fps），无掉帧
- [ ] 响应式设计覆盖 320px - 2560px
- [ ] 所有交互都有视觉反馈（hover, active, focus）
- [ ] 深色模式 / 浅色模式切换无闪烁
- [ ] 页面切换有过渡动画（View Transitions API）

---

> **最后提醒：** 性能优化是一个持续过程，不是一次性任务。建议在 CI 中集成 Lighthouse 检查，在生产环境中持续监控 Core Web Vitals，并定期进行 Bundle 分析和审计。
