# Awwwards 级别网站动画模式参考手册

> 涵盖 GSAP、Lenis、Barba.js 及现代 CSS 动画模式，源自 Awwwards SOTD 头奖网站的实战总结。

---

## 目录

1. [Lenis 平滑滚动 + GSAP 集成](#1-lenis-平滑滚动--gsap-集成)
2. [页面入场 / 预加载动画](#2-页面入场--预加载动画)
3. [GSAP ScrollTrigger 实战配方](#3-gsap-scrolltrigger-实战配方)
4. [微交互](#4-微交互)
5. [Barba.js 页面转场](#5-barbajs-页面转场)
6. [纯 CSS 动画模式](#6-纯-css-动画模式)
7. [性能优化动画实践](#7-性能优化动画实践)

---

## 1. Lenis 平滑滚动 + GSAP 集成

> Lenis 已全面取代 Locomotive Scroll，成为 Awwwards 生态的首选平滑滚动方案。
> 核心优势：更轻量（~5KB gzip）、原生 Scroll API 兼容、无虚拟滚动 hack、与 GSAP ScrollTrigger 深度集成。

### 为什么选择 Lenis 而非 Locomotive Scroll

| 对比维度 | Lenis | Locomotive Scroll |
|---------|-------|-------------------|
| 包体积 | ~5KB gzip | ~16KB gzip |
| 滚动模型 | 原生 scroll 拦截 | 虚拟滚动（transform 模拟） |
| ScrollTrigger 兼容 | 原生支持，官方推荐 | 需要 `scrollProxy` hack |
| 锚点/hash 导航 | 开箱即用 | 需要手动处理 |
| 触摸/惯性 | 物理惯性模型，更自然 | 配置有限 |
| 维护状态 | 活跃（Studio Freight 维护） | 基本停止更新 |
| CSS overflow 处理 | `html.lenis, html.lenis body { height: auto; }` | 需要大量 overflow hack |

### 完整安装与基础配置

```html
<!-- CDN -->
<script src="https://unpkg.com/lenis@1.1.18/dist/lenis.min.js"></script>
<script src="https://unpkg.com/gsap@3.12.7/dist/gsap.min.js"></script>
<script src="https://unpkg.com/gsap@3.12.7/dist/ScrollTrigger.min.js"></script>
```

```js
import Lenis from 'lenis';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

// ─── Lenis 初始化 ───
const lenis = new Lenis({
  duration: 1.2,           // 滚动持续时间（秒），越大越丝滑
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), // 自定义缓动
  touchMultiplier: 2,      // 触摸设备灵敏度倍数
  infinite: false,          // 是否允许无限滚动
  orientation: 'vertical',  // 'vertical' | 'horizontal'
  gestureOrientation: 'vertical',
  smoothWheel: true,        // 鼠标滚轮平滑
  wheelMultiplier: 1,       // 鼠标滚轮速度倍数
  autoRaf: false,           // 禁用内置 rAF，手动控制在 GSAP ticker 中
});

// ─── 核心：将 Lenis 的 rAF 整合到 GSAP ticker 中 ───
// 这样 ScrollTrigger 和 Lenis 始终保持同步
lenis.on('scroll', ScrollTrigger.update);

gsap.ticker.add((time) => {
  lenis.raf(time * 1000); // GSAP ticker 使用秒，Lenis 使用毫秒
});

// 关闭 GSAP 的默认 lag smoothing，避免与 Lenis 冲突
gsap.ticker.lagSmoothing(0);
```

### Lenis + ScrollTrigger 实战：滚动进度指示器

```js
// ScrollTrigger 直接使用原生 scroll 位置，无需任何 proxy 配置
const tl = gsap.timeline({
  scrollTrigger: {
    trigger: '.hero-section',
    start: 'top top',
    end: 'bottom top',
    scrub: true,
  },
});

tl.to('.progress-bar', { scaleX: 1, ease: 'none' })
  .to('.hero-title', { y: -100, opacity: 0 }, 0)
  .to('.hero-subtitle', { y: -50, opacity: 0 }, 0.1);
```

### Lenis 控制 API

```js
// 平滑滚动到指定位置
lenis.scrollTo('#about', {
  offset: 0,        // 偏移量
  duration: 1.5,    // 动画时长
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  immediate: false,  // 是否跳过动画
});

// 暂停/恢复滚动（预加载时常用）
lenis.stop();  // 预加载期间禁止滚动
lenis.start(); // 预加载结束后恢复

// 手动销毁
lenis.destroy();
```

### CSS 基础重置（必须）

```css
html.lenis, html.lenis body {
  height: auto;
}

.lenis.lenis-smooth {
  scroll-behavior: auto !important;
}

.lenis.lenis-smooth [data-lenis-prevent] {
  overscroll-behavior: contain;
}

.lenis.lenis-stopped {
  overflow: hidden;
}

.lenis.lenis-smooth iframe {
  pointer-events: none;
}
```

---

## 2. 页面入场 / 预加载动画

> Awwwards 有 542+ 收藏条目涉及预加载动画。这是用户对网站的第一印象，至关重要。

### 模式 A：计数器预加载器（0 → 100%）

```html
<div class="preloader" id="preloader">
  <div class="preloader__counter">
    <span class="preloader__number" id="counter">0</span>
    <span class="preloader__percent">%</span>
  </div>
  <div class="preloader__progress">
    <div class="preloader__bar" id="progress-bar"></div>
  </div>
</div>
```

```css
.preloader {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: #0a0a0a;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.preloader__number {
  font-size: clamp(4rem, 12vw, 10rem);
  font-weight: 700;
  color: #fff;
  font-variant-numeric: tabular-nums;
}

.preloader__bar {
  width: 0%;
  height: 2px;
  background: #fff;
  transition: none;
}
```

```js
function createPreloader() {
  const preloader = document.getElementById('preloader');
  const counter = document.getElementById('counter');
  const bar = document.getElementById('progress-bar');

  const tl = gsap.timeline({
    onComplete: () => {
      // 预加载结束，启动平滑滚动
      lenis.start();
      initPageAnimations();
    },
  });

  // 阶段1：计数器从 0 到 100
  const counterObj = { value: 0 };
  tl.to(counterObj, {
    value: 100,
    duration: 2.5,
    ease: 'power2.inOut',
    onUpdate: () => {
      counter.textContent = Math.floor(counterObj.value);
      bar.style.width = counterObj.value + '%';
    },
  });

  // 阶段2：数字放大淡出
  tl.to(counter, {
    scale: 1.5,
    opacity: 0,
    duration: 0.6,
    ease: 'power3.in',
  }, '-=0.3');

  tl.to(bar, {
    opacity: 0,
    duration: 0.4,
  }, '-=0.5');

  // 阶段3：预加载面板上下分离
  tl.to('.preloader', {
    clipPath: 'inset(50% 0 50% 0)',
    duration: 0.8,
    ease: 'power4.inOut',
  });

  tl.set(preloader, { display: 'none' });

  return tl;
}
```

### 模式 B：品牌遮罩揭示（Mask Reveal）

```css
.brand-reveal {
  position: fixed;
  inset: 0;
  z-index: 9998;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-reveal__text {
  font-size: clamp(3rem, 10vw, 8rem);
  font-weight: 900;
  clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%);
}
```

```js
function brandReveal() {
  const tl = gsap.timeline();

  // 品牌文字从右向左滑入揭示
  tl.from('.brand-reveal__text', {
    clipPath: 'polygon(100% 0, 100% 0, 100% 100%, 100% 100%)',
    duration: 1,
    ease: 'power4.inOut',
  });

  // 文字从左向右滑出，同时背景也跟随
  tl.to('.brand-reveal__text', {
    clipPath: 'polygon(0 0, 0 0, 0 100%, 0 100%)',
    duration: 1,
    ease: 'power4.inOut',
  }, '+=0.3');

  tl.to('.brand-reveal', {
    clipPath: 'polygon(0 0, 0 0, 0 100%, 0 100%)',
    duration: 1,
    ease: 'power4.inOut',
  }, '-=0.7');

  return tl;
}
```

### 模式 C：多步骤入场序列（Multi-step Intro）

```js
function multiStepIntro() {
  const tl = gsap.timeline({
    defaults: { ease: 'power3.out' },
  });

  // 在此期间禁止滚动
  lenis.stop();

  // 步骤1：导航栏从上方滑入
  tl.from('.nav', {
    y: -100,
    opacity: 0,
    duration: 0.8,
  });

  // 步骤2：标题逐字显现
  tl.from('.hero-title .char', {
    y: 120,
    rotateX: -80,
    opacity: 0,
    stagger: 0.03,
    duration: 0.8,
  }, '-=0.3');

  // 步骤3：副标题从下方滑入
  tl.from('.hero-subtitle', {
    y: 40,
    opacity: 0,
    duration: 0.6,
  }, '-=0.2');

  // 步骤4：装饰线条横向展开
  tl.from('.hero-line', {
    scaleX: 0,
    transformOrigin: 'left center',
    duration: 0.8,
  }, '-=0.4');

  // 步骤5：滚动提示淡入
  tl.from('.scroll-indicator', {
    opacity: 0,
    y: 20,
    duration: 0.5,
  }, '-=0.2');

  // 最后恢复滚动
  tl.call(() => lenis.start());

  return tl;
}
```

### 文字拆分工具函数

```js
/**
 * 将文本拆分为独立字符，每个字符包裹在 span 中
 * 支持 splitType 库的替代方案
 */
function splitTextToChars(selector) {
  const elements = document.querySelectorAll(selector);
  elements.forEach((el) => {
    const text = el.textContent;
    el.innerHTML = '';
    el.setAttribute('aria-label', text);

    text.split('').forEach((char) => {
      const span = document.createElement('span');
      span.classList.add('char');
      span.textContent = char === ' ' ? '\u00A0' : char;
      span.style.display = 'inline-block';
      el.appendChild(span);
    });
  });
}

// 使用
splitTextToChars('.hero-title');
// 之后 GSAP 可以动画 .char 元素
```

---

## 3. GSAP ScrollTrigger 实战配方

### 配方 1：逐词揭示（Word-by-Word Reveal）

```js
function wordReveal() {
  // 拆分文本为单词
  const paragraphs = document.querySelectorAll('.reveal-text');
  paragraphs.forEach((p) => {
    const html = p.textContent
      .split(' ')
      .map((word) => `<span class="word"><span class="word-inner">${word}</span></span>`)
      .join(' ');
    p.innerHTML = html;
  });

  gsap.utils.toArray('.reveal-text').forEach((el) => {
    const words = el.querySelectorAll('.word-inner');

    gsap.from(words, {
      y: '120%',
      duration: 0.8,
      ease: 'power3.out',
      stagger: 0.015,
      scrollTrigger: {
        trigger: el,
        start: 'top 80%',
        once: true,
      },
    });
  });
}
```

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

### 配方 2：逐行揭示（Line-by-Line with Overflow）

```js
function lineReveal() {
  gsap.utils.toArray('.reveal-lines').forEach((el) => {
    const lines = el.querySelectorAll('.line-inner');

    gsap.set(lines, { yPercent: 105 });

    gsap.to(lines, {
      yPercent: 0,
      duration: 0.9,
      ease: 'power3.out',
      stagger: 0.12,
      scrollTrigger: {
        trigger: el,
        start: 'top 85%',
        once: true,
      },
    });
  });
}
```

```css
.line {
  display: block;
  overflow: hidden;
}
.line-inner {
  display: block;
}
```

### 配方 3：水平滚动画廊（Pinned）

```html
<section class="horizontal-gallery">
  <div class="gallery-track">
    <div class="gallery-item">...</div>
    <div class="gallery-item">...</div>
    <div class="gallery-item">...</div>
    <div class="gallery-item">...</div>
    <div class="gallery-item">...</div>
  </div>
</section>
```

```css
.horizontal-gallery {
  overflow: hidden;
}
.gallery-track {
  display: flex;
  gap: 2rem;
  width: max-content;
}
.gallery-item {
  width: 60vw;
  flex-shrink: 0;
}
```

```js
function horizontalScroll() {
  const track = document.querySelector('.gallery-track');
  const items = gsap.utils.toArray('.gallery-item');
  const totalScroll = track.scrollWidth - window.innerWidth;

  gsap.to(track, {
    x: -totalScroll,
    ease: 'none',
    scrollTrigger: {
      trigger: '.horizontal-gallery',
      start: 'top top',
      end: () => `+=${totalScroll}`,
      pin: true,            // 固定面板
      scrub: 1,             // 1秒缓动，避免生硬
      anticipatePin: 1,     // 提前1像素预固定，消除抖动
      invalidateOnRefresh: true,
    },
  });
}
```

### 配方 4：视差深度层（Parallax Depth Layers）

```js
function parallaxLayers() {
  // 通用视差工具函数
  const parallaxElements = document.querySelectorAll('[data-speed]');

  parallaxElements.forEach((el) => {
    const speed = parseFloat(el.dataset.speed); // 正数=慢，负数=快，负大值=反向

    gsap.to(el, {
      y: () => speed * 100,
      ease: 'none',
      scrollTrigger: {
        trigger: el.closest('[data-parallax-container]') || el,
        start: 'top bottom',
        end: 'bottom top',
        scrub: true,
      },
    });
  });
}

// HTML 用法示例:
// <div data-parallax-container>
//   <img data-speed="0.3" src="bg.jpg">    <!-- 比滚动慢，远景 -->
//   <img data-speed="-0.1" src="mid.jpg">   <!-- 略快，中景 -->
//   <h2 data-speed="0.6" class="title">     <!-- 很慢，大标题 -->
// </div>
```

### 配方 5：堆叠卡片滚动（Stacked Cards）

```css
.stack-section {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
.stacked-cards {
  position: relative;
  height: 500px;
  width: 100%;
  max-width: 800px;
}
.stack-card {
  position: sticky;
  top: 10vh;
  width: 90%;
  height: 70vh;
  margin: 0 auto 5vh;
  border-radius: 20px;
  overflow: hidden;
  will-change: transform;
}
```

```js
function stackedCards() {
  const cards = gsap.utils.toArray('.stack-card');

  cards.forEach((card, i) => {
    if (i < cards.length - 1) {
      const nextCard = cards[i + 1];
      gsap.to(card.firstElementChild, {
        scale: 0.92,
        filter: 'brightness(0.6)',
        ease: 'none',
        scrollTrigger: {
          trigger: nextCard,
          start: 'top bottom',
          end: 'top 10vh',
          scrub: true,
        },
      });
    }
  });
}
```

### 配方 6：Pin + Scrub 叙事（Storytelling）

```js
function storytellingScroll() {
  const sections = gsap.utils.toArray('.story-section');
  const totalSections = sections.length;

  const tl = gsap.timeline({
    scrollTrigger: {
      trigger: '.story-container',
      start: 'top top',
      end: () => `+=${totalSections * 100}vh`,
      pin: '.story-visual',    // 视觉元素始终固定
      scrub: 1,
      anticipatePin: 1,
    },
  });

  // 每个故事节点对应不同的视觉状态
  sections.forEach((section, i) => {
    tl.to('.story-visual', {
      scale: 1 + i * 0.15,
      rotation: i * 5,
      duration: 1,
    })
    .to('.story-caption', {
      opacity: 0,
      y: -30,
      duration: 0.3,
    }, `<${i}`)
    .from(section.querySelector('.story-caption'), {
      opacity: 0,
      y: 30,
      duration: 0.3,
    }, `>`);
  });
}
```

### 配方 7：进度驱动动画序列

```js
function progressAnimation() {
  const trigger = document.querySelector('.progress-section');

  const tl = gsap.timeline({
    scrollTrigger: {
      trigger,
      start: 'top center',
      end: 'bottom center',
      scrub: true,
    },
  });

  // 0% - 25%：图形展开
  tl.to('.shape', {
    scale: 2,
    rotation: 90,
    borderRadius: '50%',
    duration: 0.25,
  });

  // 25% - 50%：颜色变化
  tl.to('.shape', {
    backgroundColor: '#ff6b6b',
    duration: 0.25,
  });

  // 50% - 75%：分裂
  tl.to('.shape', {
    scale: 0.5,
    x: -100,
    duration: 0.25,
  })
  .to('.shape-clone', {
    scale: 0.5,
    x: 100,
    opacity: 1,
    duration: 0.25,
  }, '<');

  // 75% - 100%：合并消失
  tl.to(['.shape', '.shape-clone'], {
    scale: 0,
    opacity: 0,
    duration: 0.25,
  });
}
```

---

## 4. 微交互

### 磁性按钮（Magnetic Button）

```js
function magneticButtons() {
  const buttons = document.querySelectorAll('[data-magnetic]');

  buttons.forEach((btn) => {
    const strength = parseFloat(btn.dataset.magnetic) || 0.3;

    btn.addEventListener('mousemove', (e) => {
      const rect = btn.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;

      gsap.to(btn, {
        x: x * strength,
        y: y * strength,
        duration: 0.3,
        ease: 'power2.out',
      });

      // 内部文字额外偏移（更强烈的磁性效果）
      const inner = btn.querySelector('[data-magnetic-inner]');
      if (inner) {
        gsap.to(inner, {
          x: x * strength * 1.5,
          y: y * strength * 1.5,
          duration: 0.3,
          ease: 'power2.out',
        });
      }
    });

    btn.addEventListener('mouseleave', () => {
      gsap.to([btn, btn.querySelector('[data-magnetic-inner]')], {
        x: 0,
        y: 0,
        duration: 0.5,
        ease: 'elastic.out(1, 0.4)',
      });
    });
  });
}

// HTML: <button data-magnetic="0.3"><span data-magnetic-inner>探索更多</span></button>
```

### 链接悬停图片揭示（Hover Image Reveal）

```css
.link-with-image {
  position: relative;
  display: inline-block;
}
.hover-image {
  position: fixed;
  width: 300px;
  height: 200px;
  pointer-events: none;
  z-index: 100;
  border-radius: 8px;
  overflow: hidden;
  opacity: 0;
  transform: scale(0.8);
}
```

```js
function hoverImageReveal() {
  const links = document.querySelectorAll('.link-with-image');
  const image = document.querySelector('.hover-image');

  links.forEach((link) => {
    const imgUrl = link.dataset.image;

    link.addEventListener('mouseenter', () => {
      image.style.backgroundImage = `url(${imgUrl})`;
      gsap.to(image, {
        opacity: 1,
        scale: 1,
        duration: 0.4,
        ease: 'power2.out',
      });
    });

    link.addEventListener('mousemove', (e) => {
      gsap.to(image, {
        x: e.clientX - 150,
        y: e.clientY - 100,
        duration: 0.5,
        ease: 'power2.out',
      });
    });

    link.addEventListener('mouseleave', () => {
      gsap.to(image, {
        opacity: 0,
        scale: 0.8,
        duration: 0.3,
        ease: 'power2.in',
      });
    });
  });
}
```

### 按钮点击涟漪效果（Ripple Effect）

```css
.btn-ripple {
  position: relative;
  overflow: hidden;
}
.ripple-circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: scale(0);
  pointer-events: none;
}
```

```js
function createRipple(e) {
  const btn = e.currentTarget;
  const rect = btn.getBoundingClientRect();
  const size = Math.max(rect.width, rect.height) * 2;
  const x = e.clientX - rect.left - size / 2;
  const y = e.clientY - rect.top - size / 2;

  const ripple = document.createElement('span');
  ripple.classList.add('ripple-circle');
  ripple.style.width = ripple.style.height = size + 'px';
  ripple.style.left = x + 'px';
  ripple.style.top = y + 'px';
  btn.appendChild(ripple);

  gsap.to(ripple, {
    scale: 1,
    opacity: 0,
    duration: 0.6,
    ease: 'power2.out',
    onComplete: () => ripple.remove(),
  });
}

// 绑定
document.querySelectorAll('.btn-ripple').forEach((btn) => {
  btn.addEventListener('click', createRipple);
});
```

### 数字计数器动画（Number Counter）

```js
function animateCounter(selector, target, duration = 2, prefix = '', suffix = '') {
  const el = document.querySelector(selector);
  const obj = { value: 0 };

  gsap.to(obj, {
    value: target,
    duration,
    ease: 'power2.out',
    scrollTrigger: {
      trigger: el,
      start: 'top 85%',
      once: true,
    },
    onUpdate: () => {
      el.textContent = prefix + Math.floor(obj.value).toLocaleString() + suffix;
    },
  });
}

// 使用
animateCounter('.stat-number', 12847, 2.5, '', '+');
animateCounter('.revenue-number', 3.5, 2, '$', 'M');
animateCounter('.percent-number', 98, 2, '', '%');
```

### 图片遮罩揭示（Image Mask Reveal）

```css
.image-mask-reveal {
  position: relative;
  overflow: hidden;
  border-radius: 12px;
}
.image-mask-reveal img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scale(1.3);
  transition: transform 1.2s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
.image-mask-reveal.revealed img {
  transform: scale(1);
}
.image-mask-reveal::after {
  content: '';
  position: absolute;
  inset: 0;
  background: #0a0a0a;
  transform-origin: right;
  transition: transform 1s cubic-bezier(0.77, 0, 0.175, 1);
}
.image-mask-reveal.revealed::after {
  transform: scaleX(0);
}
```

```js
// 配合 ScrollTrigger 触发
gsap.utils.toArray('.image-mask-reveal').forEach((el) => {
  ScrollTrigger.create({
    trigger: el,
    start: 'top 80%',
    once: true,
    onEnter: () => el.classList.add('revealed'),
  });
});
```

---

## 5. Barba.js 页面转场

### 完整 Barba + GSAP 设置

```js
import barba from '@barba/core';
import gsap from 'gsap';

// ─── 页面过渡基础配置 ───
barba.init({
  preventRunning: true,
  transitions: [
    {
      name: 'default',

      // 离开当前页面
      leave(data) {
        return gsap.timeline()
          .to(data.current.container, {
            opacity: 0,
            y: -30,
            duration: 0.4,
            ease: 'power2.in',
          });
      },

      // 进入新页面（等待新容器准备好后）
      enter(data) {
        return gsap.timeline()
          .from(data.next.container, {
            opacity: 0,
            y: 30,
            duration: 0.5,
            ease: 'power2.out',
          })
          .call(() => {
            // 进入后初始化页面动画
            initPageAnimations();
          });
      },

      // 离开前/进入后（两个容器同时可见）
      beforeEnter(data) {
        window.scrollTo(0, 0);
        lenis.scrollTo(0, { immediate: true }); // Lenis 立即重置
      },
    },
  ],
});
```

### 遮罩过渡（Overlay Transition）

```js
// ─── HTML（固定在页面上的遮罩层） ───
// <div class="transition-overlay">
//   <div class="transition-overlay__panel panel-top"></div>
//   <div class="transition-overlay__panel panel-bottom"></div>
// </div>

const overlayTransition = {
  name: 'overlay',

  leave(data) {
    const tl = gsap.timeline();

    // 上下两块面板从中间向上下展开
    tl.to('.panel-top', {
      yPercent: -100,
      duration: 0.5,
      ease: 'power4.inOut',
    })
    .to('.panel-bottom', {
      yPercent: 100,
      duration: 0.5,
      ease: 'power4.inOut',
    }, '<')
    // 面板展开后，隐藏旧内容
    .set(data.current.container, { opacity: 0 });

    return tl;
  },

  enter(data) {
    const tl = gsap.timeline();

    // 新内容先就位（隐藏状态）
    tl.set(data.next.container, { opacity: 1 });

    // 面板回收
    tl.to('.panel-top', {
      yPercent: 0,
      duration: 0.5,
      ease: 'power4.inOut',
    })
    .to('.panel-bottom', {
      yPercent: 0,
      duration: 0.5,
      ease: 'power4.inOut',
    }, '<')
    .call(() => {
      initPageAnimations();
    });

    return tl;
  },
};

barba.init({
  transitions: [overlayTransition],
});
```

### 内容预取（Prefetching）

```js
barba.init({
  prefetch: true, // 默认悬停时预取
  prefetchIgnore: ['/admin', '/logout'], // 排除路径
  // 或自定义预取策略
  prevent: ({ href }) => {
    return /\.(pdf|zip|jpg|png)$/.test(href);
  },
});
```

### View Transitions API（原生替代方案）

```js
// 现代 Chrome/Edge 原生 View Transitions
// 无需 Barba.js 的轻量替代

document.startViewTransition(() => {
  // DOM 更新回调
  return updateDOM();
});

// 配合 CSS 自定义动画
// ::view-transition-old(root) { ... }
// ::view-transition-new(root) { ... }

// 兼容性检测
if (!document.startViewTransition) {
  // 降级为普通页面加载或 Barba.js
}
```

```css
/* View Transitions API 自定义动画 */
::view-transition-old(root) {
  animation: fade-out 0.3s ease-in;
}
::view-transition-new(root) {
  animation: fade-in 0.3s ease-out;
}

@keyframes fade-out {
  to { opacity: 0; transform: translateY(-10px); }
}
@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
}
```

---

## 6. 纯 CSS 动画模式

### CSS 滚动驱动动画（Scroll-Driven Animations）

```css
/* ─── 基于滚动进度的动画 ─── */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(60px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.scroll-reveal {
  /* 无需 JS！动画进度与滚动位置绑定 */
  animation: fadeInUp linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}

/* ─── 水平滚动（纯 CSS！） ─── */
@keyframes horizontalScroll {
  to { transform: translateX(calc(-100% + 100vw)); }
}

.horizontal-scroll-container {
  animation: horizontalScroll linear both;
  animation-timeline: scroll();
}

/* ─── 视差效果 ─── */
@keyframes parallax {
  to { transform: translateY(-100px); }
}

.parallax-bg {
  animation: parallax linear both;
  animation-timeline: scroll();
}

/* ─── 进度条 ─── */
@keyframes progress {
  to { scaleX: 1; }
}

.read-progress {
  transform-origin: left;
  animation: progress linear both;
  animation-timeline: scroll(root);
}
```

### CSS 容器查询动画（Container Query Animations）

```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

/* 根据容器宽度触发不同的入场动画 */
@container card (min-width: 400px) {
  .card {
    animation: slideInRight 0.6s ease-out both;
  }
}

@container card (max-width: 399px) {
  .card {
    animation: slideInUp 0.6s ease-out both;
  }
}

@keyframes slideInRight {
  from { opacity: 0; transform: translateX(40px); }
}
@keyframes slideInUp {
  from { opacity: 0; transform: translateY(40px); }
}
```

### CSS @property 实现可动画自定义属性

```css
/* 注册自定义属性使其可插值动画 */
@property --gradient-angle {
  syntax: '<angle>';
  initial-value: 0deg;
  inherits: false;
}

@property --fill-progress {
  syntax: '<percentage>';
  initial-value: 0%;
  inherits: false;
}

@property --border-radius-value {
  syntax: '<length>';
  initial-value: 0px;
  inherits: false;
}

/* 旋转渐变背景 */
.gradient-spin {
  background: conic-gradient(
    from var(--gradient-angle),
    #ff6b6b, #feca57, #48dbfb, #ff9ff3, #ff6b6b
  );
  animation: spin-gradient 3s linear infinite;
}

@keyframes spin-gradient {
  to { --gradient-angle: 360deg; }
}

/* 进度填充 */
.fill-animation {
  width: var(--fill-progress);
  animation: fill 2s ease-out forwards;
}

@keyframes fill {
  to { --fill-progress: 100%; }
}

/* 平滑圆角变化 */
.morphing-shape {
  border-radius: var(--border-radius-value);
  animation: morph 2s ease-in-out infinite alternate;
}

@keyframes morph {
  0% { --border-radius-value: 0px; }
  100% { --border-radius-value: 50%; }
}
```

### View Transitions API（CSS 端）

```css
/* 为特定元素指定 transition name */
.featured-image {
  view-transition-name: hero-image;
}

/* 自定义过渡动画（比默认的交叉淡入淡出更丰富） */
::view-transition-old(hero-image) {
  animation: shrink-out 0.4s ease-in;
}
::view-transition-new(hero-image) {
  animation: grow-in 0.4s ease-out;
}

@keyframes shrink-out {
  to {
    transform: scale(0.8);
    opacity: 0;
    border-radius: 20px;
  }
}
@keyframes grow-in {
  from {
    transform: scale(0.8);
    opacity: 0;
    border-radius: 20px;
  }
}

/* 页面级过渡 */
::view-transition-old(root) {
  animation: 0.4s ease-out both fade-slide-out;
}
::view-transition-new(root) {
  animation: 0.4s ease-in both fade-slide-in;
}

@keyframes fade-slide-out {
  to { opacity: 0; transform: translateX(-30px); }
}
@keyframes fade-slide-in {
  from { opacity: 0; transform: translateX(30px); }
}
```

---

## 7. 性能优化动画实践

### 原则 1：仅使用 transform 和 opacity（GPU 合成层）

```css
/* ✅ 正确：触发 GPU 合成，不触发 Layout/Paint */
.good-animation {
  will-change: transform, opacity;
  transform: translateX(0);
  opacity: 1;
}

/* ❌ 错误：触发 Layout 重排 */
.bad-animation-width {
  transition: width 0.3s;  /* 会触发 Layout */
}

/* ❌ 错误：触发 Paint 重绘 */
.bad-animation-bg {
  transition: background-color 0.3s;  /* 会触发 Paint */
}
```

```js
// ✅ 正确的 GSAP 写法
gsap.to(el, {
  x: 100,        // 使用 x 而非 left
  y: 50,         // 使用 y 而非 top
  scale: 1.2,    // 使用 scale 而非 width/height
  rotation: 45,  // 使用 rotation 而非 transform rotate
  opacity: 0.5,
  duration: 0.5,
});

// ❌ 避免的写法
gsap.to(el, {
  left: 100,          // 触发 Layout
  width: 200,         // 触发 Layout
  backgroundColor: '#red',  // 触发 Paint
  marginTop: 20,      // 触发 Layout
});
```

### 原则 2：will-change 最佳实践

```js
// 动态管理 will-change
function animateSafely(el, props) {
  // 动画前添加
  el.style.willChange = 'transform, opacity';

  const tl = gsap.to(el, {
    ...props,
    onComplete() {
      // 动画后移除，释放 GPU 内存
      el.style.willChange = 'auto';
    },
  });

  return tl;
}
```

> 静态 `will-change` 声明和全局滥用警告，参见 `references/performance-guide.md`。

### 原则 3：requestAnimationFrame vs 滚动事件

```js
// ❌ 错误：scroll 事件触发频率过高，造成卡顿
window.addEventListener('scroll', () => {
  parallaxElement.style.transform = `translateY(${window.scrollY * 0.5}px)`;
});

// ✅ 正确：使用 rAF 节流
let ticking = false;
window.addEventListener('scroll', () => {
  if (!ticking) {
    requestAnimationFrame(() => {
      const scrollY = window.scrollY;
      parallaxElement.style.transform = `translateY(${scrollY * 0.5}px)`;
      ticking = false;
    });
    ticking = true;
  }
});

// ✅✅ 最佳：使用 GSAP ScrollTrigger（内部已优化 rAF）
gsap.to(parallaxElement, {
  y: -100,
  ease: 'none',
  scrollTrigger: {
    trigger: parallaxElement,
    start: 'top bottom',
    end: 'bottom top',
    scrub: true,
  },
});
```

### 原则 4：Intersection Observer 触发动画

```js
// 轻量替代 ScrollTrigger 的方案（简单入场动画）
function observeAnimations() {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target); // 只触发一次
        }
      });
    },
    {
      threshold: 0.15,      // 元素 15% 可见时触发
      rootMargin: '0px 0px -50px 0px',  // 提前/延后触发
    }
  );

  document.querySelectorAll('[data-animate]').forEach((el) => {
    observer.observe(el);
  });
}

// CSS 配合
// [data-animate] { opacity: 0; transform: translateY(30px); transition: 0.6s ease-out; }
// [data-animate].is-visible { opacity: 1; transform: translateY(0); }
```

### 原则 5：防抖与节流

> 完整的 `debounce`/`throttle` 实现参见 `scripts/performance-utils.js`。
> 用法示例：`window.addEventListener('resize', debounce(() => ScrollTrigger.refresh(), 250));`

### 完整性能检查清单

```markdown
## 动画性能检查清单

### GPU 合成层
- [ ] 仅使用 transform (translateX/Y, scale, rotate) 和 opacity
- [ ] 避免动画 width, height, top, left, margin, padding
- [ ] 避免动画 box-shadow, border-radius（会触发 Paint）

### will-change 管理
- [ ] 仅在动画即将开始前添加 will-change
- [ ] 动画结束后移除 will-change: auto
- [ ] 永远不要全局设置 will-change

### 滚动性能
- [ ] 使用 GSAP ScrollTrigger 而非原生 scroll 事件
- [ ] 简单场景使用 Intersection Observer
- [ ] resize 事件必须防抖
- [ ] 鼠标跟随使用节流（16ms ≈ 60fps）

### GSAP 特定
- [ ] 使用 `invalidateOnRefresh: true` 处理动态内容
- [ ] 使用 `anticipatePin: 1` 消除 pin 抖动
- [ ] 大量元素动画使用 `stagger` 而非多个 timeline
- [ ] 使用 `gsap.ticker.lagSmoothing(0)` 配合 Lenis

### 图片/媒体
- [ ] 动画中的大图使用 `will-change: transform`
- [ ] 使用 `loading="lazy"` 延迟加载非首屏图片
- [ ] 避免对 video 元素做复杂 transform
- [ ] 使用 `content-visibility: auto` 优化屏幕外元素

### CSS 层面
- [ ] 动画元素使用 `contain: layout style paint`（隔离重排）
- [ ] 使用 `transform: translateZ(0)` 或 `will-change` 提升合成层
- [ ] 避免在动画中使用 `filter: blur()`（非常耗性能）
```

---

## 附录：快速启动模板

```js
/**
 * Awwwards 级别动画项目快速启动模板
 * 集成 Lenis + GSAP + ScrollTrigger + Barba.js
 */
import Lenis from 'lenis';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import barba from '@barba/core';

gsap.registerPlugin(ScrollTrigger);

// 1. 初始化 Lenis
const lenis = new Lenis({
  duration: 1.2,
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  touchMultiplier: 2,
  autoRaf: false,
});

lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((time) => lenis.raf(time * 1000));
gsap.ticker.lagSmoothing(0);

// 2. 初始化 Barba.js
barba.init({
  transitions: [{
    leave(data) {
      lenis.stop();
      return gsap.to(data.current.container, {
        opacity: 0, y: -30, duration: 0.4,
      });
    },
    enter(data) {
      window.scrollTo(0, 0);
      lenis.scrollTo(0, { immediate: true });
      return gsap.from(data.next.container, {
        opacity: 0, y: 30, duration: 0.5,
        onComplete: () => {
          lenis.start();
          initPageAnimations();
        },
      });
    },
  }],
});

// 3. 页面动画初始化函数
function initPageAnimations() {
  ScrollTrigger.refresh();

  // 文字揭示
  gsap.utils.toArray('.reveal').forEach((el) => {
    gsap.from(el, {
      y: 40, opacity: 0, duration: 0.8, ease: 'power3.out',
      scrollTrigger: { trigger: el, start: 'top 85%', once: true },
    });
  });

  // 图片揭示
  gsap.utils.toArray('.img-reveal').forEach((el) => {
    gsap.from(el.querySelector('img'), {
      scale: 1.3, duration: 1.2, ease: 'power3.out',
      scrollTrigger: { trigger: el, start: 'top 80%', once: true },
    });
  });

  // 磁性按钮
  magneticButtons();
}

// 4. 首次加载
lenis.stop();
window.addEventListener('load', () => {
  multiStepIntro().then(() => lenis.start());
});
```

---

> **参考资源**
> - [Lenis 官方文档](https://github.com/darkroomengineering/lenis)
> - [GSAP ScrollTrigger 文档](https://greensock.com/scrolltrigger/)
> - [Barba.js 文档](https://barba.js.org/)
> - [CSS Scroll-driven Animations 规范](https://drafts.csswg.org/scroll-animations-1/)
> - [View Transitions API 规范](https://drafts.csswg.org/css-view-transitions/)
> - [web.dev 动画性能指南](https://web.dev/animations-guide/)
