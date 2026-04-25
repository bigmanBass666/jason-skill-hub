# 技术栈参考

## CDN 可用库（HTML Artifact 中使用）

### 动画库
```html
<!-- GSAP 3.12.5 + 插件 -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/TextPlugin.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/SplitText.min.js"></script>

<!-- Three.js r128（WebGL） -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<!-- D3.js（数据可视化） -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
```

### 字体来源
```html
<!-- Fontshare（免费高品质字体） -->
<link href="https://api.fontshare.com/v2/css?f[]=clash-display@700,600,500&display=swap" rel="stylesheet">
<link href="https://api.fontshare.com/v2/css?f[]=satoshi@700,500,400&display=swap" rel="stylesheet">
<link href="https://api.fontshare.com/v2/css?f[]=cabinet-grotesk@800,700&display=swap" rel="stylesheet">
<link href="https://api.fontshare.com/v2/css?f[]=general-sans@600,500&display=swap" rel="stylesheet">

<!-- Google Fonts（谨慎使用，只选独特字体） -->
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Grotesk:wght@300;500;700&display=swap" rel="stylesheet">
```

## React Artifact 技术栈

```javascript
// 可用库
import { gsap } from 'gsap';  // 需通过 cdn 或假设已安装
import * as THREE from 'three';
import * as d3 from 'd3';
import { motion, AnimatePresence } from 'framer-motion';  // 如已安装

// Tailwind 核心类（可用）
// 但对于 Awwwards 级别，优先使用 CSS-in-JS 或 style 属性获得更精确控制
```

## 性能优化要点

```javascript
// 1. 使用 transform 而非 left/top（GPU 加速）
el.style.transform = `translateX(${x}px)`;  // ✅
el.style.left = `${x}px`;  // ❌

// 2. will-change 声明
el.style.willChange = 'transform, opacity';

// 3. 图片懒加载
<img loading="lazy" src="..." />

// 4. 防抖滚动监听
window.addEventListener('scroll', debounce(handler, 16));

// 5. CSS contain 减少重排
.card { contain: layout style; }
```

## 关键 CSS 特性

```css
/* Clamp 响应式字体 */
font-size: clamp(2rem, 8vw, 10rem);

/* 视口单位精确控制 */
height: 100dvh;  /* 动态视口高度，处理移动端地址栏 */

/* 滚动捕捉 */
.container {
  scroll-snap-type: y mandatory;
  overflow-y: scroll;
  height: 100vh;
}
.section { scroll-snap-align: start; }

/* CSS 滚动驱动动画（现代浏览器） */
@keyframes reveal {
  from { opacity: 0; transform: translateY(40px); }
  to { opacity: 1; transform: translateY(0); }
}
.element {
  animation: reveal linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 40%;
}
```
