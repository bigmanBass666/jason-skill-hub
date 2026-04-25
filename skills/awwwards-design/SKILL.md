---
name: awwwards-design
description: 创建能在 Awwwards 获奖的设计级网站。当用户要求创建视觉震撼、沉浸式体验、获奖级别的网站、作品集、品牌展示页、产品落地页，或任何追求极致视觉与交互体验的 web 项目时，必须使用此 skill。关键词触发：「Awwwards 级别」「沉浸式网站」「震撼视觉」「高端网站」「创意交互」「WebGL」「Scrollytelling」「获奖设计」「极致动效」「创意代理网站」。即使用户只说「帮我做个很酷的网站」也应触发此 skill，因为它包含了创建世界顶级 web 体验所需的全部技术与设计框架。
---

# Awwwards 设计级网站创建指南

此 skill 使 Claude 能够创建达到 Awwwards「年度最佳网站（SOTD/SOTM）」评选标准的 web 体验。

---

## 第一步：建立创意概念（必须先做）

在写任何代码之前，必须完成「概念确立」。Awwwards 评委首先看的是**创意的独特性与执行的一致性**。

### 四维定义框架

1. **叙事核心（Narrative Core）**  
   这个网站在讲什么故事？什么是用户从首屏到尾部的情感弧线？  
   → 例：「从混沌走向秩序」「材质与光的对话」「速度作为一种美学」

2. **视觉语言（Visual Language）**  
   选择一个极端风格并坚定执行：
   - **新极简主义**：超大字体 + 极端留白 + 单色或双色调
   - **有机感官**：流体动画 + 噪点纹理 + 自然色调
   - **数字朋克**：高对比 + 故障美学 + 霓虹色
   - **档案式排版**：密集信息流 + 等宽字体 + 网格系统
   - **电影沉浸**：全屏媒体 + 电影比例 + 黑色背景
   - **几何抽象**：数学美感 + SVG 动画 + 精确布局

3. **交互哲学（Interaction Philosophy）**  
   用一句话定义交互行为：「每一次滚动都是揭开故事的下一页」  
   → 决定：Scroll-driven？鼠标跟随？点击触发叙事？水平滚动？

4. **技术野心（Technical Ambition）**  
   在以下选项中选择合适组合（参见 references/tech-stack.md 获取实现细节）：
   - WebGL / Three.js 3D 场景
   - GSAP ScrollTrigger 叙事动画  
   - Canvas 粒子系统
   - CSS Houdini 特效
   - SVG 形态变换
   - 自定义着色器（GLSL）

---

## 第二步：设计系统构建

### 排版系统（Typography System）

**Awwwards 获奖网站的字体选择规律：**

| 风格 | 展示字体（Display） | 正文字体（Body） | 来源 |
|------|-----------------|--------------|------|
| 现代高端 | Neue Montreal, PP Pangaia | Söhne, Suisse Int'l | Pangram Pangram |
| 档案复古 | Druk Wide, Reforma | Courier Prime | Commercial Type |
| 有机自然 | Canela, Ogg | Freight Text | Commercial Type |
| 数字未来 | Grotesk, Space Mono | Geist Mono | Vercel / Google |
| 实验前卫 | Migra, Hatton | Editorial New | Pangram Pangram |

**关键规则：**
- 禁用：Inter、Roboto、Arial、Helvetica（太普通）
- 字号极端化：Hero 字体应在 `8vw–20vw` 之间
- 行高设计感：`line-height: 0.85–0.9` 用于超大标题
- 字母间距：展示字体用 `-0.03em` 到 `-0.05em`

### 色彩系统（Color System）

```css
/* Awwwards 获奖调色板模式 */

/* 模式1：极端对比（最常获奖） */
--c-bg: #0a0a0a;
--c-text: #f0ece4;
--c-accent: #ff3d00;  /* 一个鲜明的强调色，仅用于关键元素 */

/* 模式2：泥土有机 */
--c-bg: #f5f0e8;
--c-text: #1a1208;
--c-accent: #8b6914;

/* 模式3：冷调数字 */
--c-bg: #f8f8ff;
--c-text: #0d0d1a;
--c-accent: #0037ff;

/* 模式4：暗调奢华 */
--c-bg: #111111;
--c-text: #e8e0d0;
--c-accent: #c9a96e;
```

**原则：背景 + 文字 + 1个强调色 = 完整调色板。不要超过3色。**

### 动画缓动曲线（Easing Curves）

```javascript
// 这些是 Awwwards 级别动画的标准缓动曲线
const easings = {
  // 出现动画：快入慢出，有份量感
  enter: "cubic-bezier(0.16, 1, 0.3, 1)",  // Expo Out
  
  // 悬停微交互：自然弹性
  hover: "cubic-bezier(0.34, 1.56, 0.64, 1)",  // Back Out (轻微超调)
  
  // 页面切换：电影感
  pageTransition: "cubic-bezier(0.87, 0, 0.13, 1)",  // Expo InOut
  
  // 慢揭示：文字和重要元素
  reveal: "cubic-bezier(0.25, 1, 0.5, 1)",  // Quart Out
}
```

---

## 第三步：核心技术实现模式

### 模式A：GSAP ScrollTrigger 叙事滚动

```html
<!-- CDN 引入（适合 HTML Artifact） -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
```

```javascript
// 文字逐词揭示（最常见的 Awwwards 效果）
function splitAndReveal(selector) {
  const el = document.querySelector(selector);
  const words = el.textContent.split(' ');
  el.innerHTML = words.map(w => 
    `<span class="word"><span class="word-inner">${w}</span></span>`
  ).join(' ');
  
  gsap.from(`${selector} .word-inner`, {
    yPercent: 110,
    duration: 0.9,
    ease: "expo.out",
    stagger: 0.04,
    scrollTrigger: {
      trigger: selector,
      start: "top 85%",
    }
  });
}

// 固定视差滚动叙事（Scrollytelling）
gsap.timeline({
  scrollTrigger: {
    trigger: ".narrative-section",
    start: "top top",
    end: "+=300%",
    scrub: 1.5,  // 越大越平滑，1.5 是甜点
    pin: true,
  }
})
.from(".scene-element", { scale: 0.6, opacity: 0 })
.to(".title", { xPercent: -100, opacity: 0 }, "<0.3")
.fromTo(".next-content", { yPercent: 30 }, { yPercent: 0 });
```

### 模式B：Three.js WebGL 背景

```javascript
// 粒子系统背景（最适合 Awwwards 的 Three.js 用法）
// 详细实现参见 references/webgl-patterns.md

// 核心结构：
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, W/H, 0.1, 100);
const renderer = new THREE.WebGLRenderer({ 
  antialias: true, 
  alpha: true  // 透明背景，允许 CSS 控制底色
});

// 鼠标跟随让 3D 场景有生命感
let mouseX = 0, mouseY = 0;
document.addEventListener('mousemove', (e) => {
  mouseX = (e.clientX / W - 0.5) * 2;
  mouseY = -(e.clientY / H - 0.5) * 2;
});

// 在 animate 中平滑跟随
camera.position.x += (mouseX * 0.5 - camera.position.x) * 0.05;
camera.position.y += (mouseY * 0.3 - camera.position.y) * 0.05;
camera.lookAt(scene.position);
```

### 模式C：CSS 高级视觉效果（无需 JS）

```css
/* 噪点纹理叠加（给设计增加质感） */
.noise-overlay::after {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,..."); /* SVG 噪点 */
  opacity: 0.04;
  pointer-events: none;
  z-index: 9999;
}

/* 渐变网格背景（Aurora 效果） */
.aurora-bg {
  background: 
    radial-gradient(ellipse 80% 50% at 20% 40%, rgba(120,40,200,0.15), transparent),
    radial-gradient(ellipse 60% 80% at 80% 60%, rgba(0,100,255,0.1), transparent),
    radial-gradient(ellipse 40% 40% at 50% 80%, rgba(255,80,0,0.08), transparent);
  animation: aurora-shift 8s ease-in-out infinite alternate;
}

/* 文字遮罩裁剪（把图片填充到文字里） */
.clip-text {
  background-image: url('./texture.jpg');
  background-size: cover;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 水平滚动容器 */
.h-scroll-wrapper {
  display: flex;
  width: max-content;
  will-change: transform;  /* GPU 加速 */
}
```

### 模式D：自定义光标（必备）

```javascript
// Awwwards 网站几乎都有自定义光标
const cursor = document.querySelector('.cursor');
const follower = document.querySelector('.cursor-follower');

let cursorX = 0, cursorY = 0;
let followerX = 0, followerY = 0;

document.addEventListener('mousemove', e => {
  cursorX = e.clientX;
  cursorY = e.clientY;
  cursor.style.transform = `translate(${cursorX}px, ${cursorY}px)`;
});

// 用 RAF 让 follower 平滑跟随
function animateCursor() {
  followerX += (cursorX - followerX) * 0.12;
  followerY += (cursorY - followerY) * 0.12;
  follower.style.transform = `translate(${followerX}px, ${followerY}px)`;
  requestAnimationFrame(animateCursor);
}
animateCursor();

// 悬停时变形
document.querySelectorAll('a, button').forEach(el => {
  el.addEventListener('mouseenter', () => follower.classList.add('expanded'));
  el.addEventListener('mouseleave', () => follower.classList.remove('expanded'));
});
```

---

## 第四步：Awwwards 评审标准对应

Awwwards 按四个维度评分（各10分）：

### 1. Design（设计）— 权重最高
- [ ] 视觉层次清晰，第一眼就知道看哪里
- [ ] 字体选择独特且有品位，层级设置精确
- [ ] 颜色系统克制而有力量
- [ ] 每个间距都是刻意设计的，而非随机
- [ ] 图形元素有原创性，非素材库调用

### 2. Usability（可用性）
- [ ] 导航逻辑直观，即使是实验性导航也有清晰暗示
- [ ] 加载时间 < 3秒（或有有趣的加载动画掩盖等待）
- [ ] 移动端体验专门设计，非响应式降级
- [ ] 无障碍：键盘可导航，对比度达标

### 3. Creativity（创意）
- [ ] 至少一个「Wow Moment」——用户第一次看到会截图的瞬间
- [ ] 交互模式有创新性，非套用模板
- [ ] 内容与形式高度统一

### 4. Content（内容）
- [ ] 文案有个性和声音，非通用营销语言
- [ ] 图片/视频质量专业
- [ ] 信息架构服务叙事，而非功能清单

---

## 第五步：必须避免的「AI 网站」特征

❌ **绝对禁止：**
- 蓝白配色 + Inter 字体（最典型的 AI 生成网站特征）
- 卡片 + 圆角 + 阴影的过度使用
- 渐变 hero banner（紫色到蓝色尤其要避免）
- 「我们的特点是...」的三栏 features section
- 底部版权信息作为唯一的 footer 设计
- 无故使用 Bootstrap / 预制 UI 组件库

✅ **转而使用：**
- 超大字体作为视觉锚点（不是图片）
- 有意义的留白（非填满式布局）
- 页面之间的过渡动画
- 滚动行为驱动的内容揭示
- 文本和图像的非对称排版

---

## 第六步：实现检查清单

完成代码前，逐项核查：

**视觉品质**
- [ ] 在最新 Chrome 全屏截图后，是否像一个专业设计作品？
- [ ] 字体是否渲染清晰？（`-webkit-font-smoothing: antialiased`）
- [ ] 所有动画是否流畅？（无卡顿，使用 `transform` 而非 `left/top`）
- [ ] 是否有自定义光标或至少改变了默认光标行为？

**技术质量**
- [ ] CSS 是否使用了 `will-change` 优化动画元素？
- [ ] 图片/资源是否延迟加载？
- [ ] `scroll-behavior: smooth` 是否已设置？
- [ ] 是否有优雅的页面加载动画（Intro animation）？

**创意完整性**
- [ ] 第一屏（Above the fold）是否足够震撼？
- [ ] 是否有明确的「Wow Moment」值得截图分享？
- [ ] 整个页面的视觉语言是否统一一致？

---

## 参考文件

更多技术实现细节，请阅读：
- `references/tech-stack.md` — 完整技术栈和库版本
- `references/webgl-patterns.md` — Three.js / WebGL 实现模式
- `references/animation-patterns.md` — GSAP 高级动画配方
- `references/typography-guide.md` — 字体系统和排版规则

---

## 快速启动模板

对于 HTML Artifact（最常用），使用以下基础结构：

```html
<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[项目名]</title>
  
  <!-- 必须的字体 - 选其一 -->
  <link href="https://api.fontshare.com/v2/css?f[]=clash-display@700,600&display=swap" rel="stylesheet">
  
  <!-- GSAP（如需要） -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
  
  <!-- Three.js（如需要 WebGL） -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  
  <style>
    /* ===== CSS 变量系统 ===== */
    :root {
      --c-bg: #0a0a0a;
      --c-text: #f0ece4;
      --c-accent: #ff3d00;
      --font-display: 'Clash Display', sans-serif;
      --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    *, *::before, *::after { 
      box-sizing: border-box; 
      margin: 0; 
      padding: 0; 
    }
    
    html { 
      scroll-behavior: smooth;
      font-size: clamp(14px, 1.2vw, 18px);
    }
    
    body {
      background: var(--c-bg);
      color: var(--c-text);
      font-family: var(--font-display);
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
      cursor: none;  /* 自定义光标时隐藏默认 */
    }
    
    /* ===== 自定义光标 ===== */
    .cursor {
      width: 8px;
      height: 8px;
      background: var(--c-accent);
      border-radius: 50%;
      position: fixed;
      top: -4px;
      left: -4px;
      pointer-events: none;
      z-index: 9999;
      transition: transform 0.1s var(--ease-out-expo);
    }
    
    .cursor-follower {
      width: 40px;
      height: 40px;
      border: 1px solid rgba(240,236,228,0.3);
      border-radius: 50%;
      position: fixed;
      top: -20px;
      left: -20px;
      pointer-events: none;
      z-index: 9998;
      transition: transform 0.1s linear, width 0.3s, height 0.3s, border-radius 0.3s;
    }
    
    .cursor-follower.expanded {
      width: 80px;
      height: 80px;
      top: -40px;
      left: -40px;
      border-color: var(--c-accent);
    }
    
    /* ===== 噪点质感叠加 ===== */
    body::after {
      content: '';
      position: fixed;
      inset: 0;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
      opacity: 0.035;
      pointer-events: none;
      z-index: 99999;
    }
  </style>
</head>
<body>

  <div class="cursor"></div>
  <div class="cursor-follower"></div>
  
  <!-- 你的内容从这里开始 -->

  <script>
    gsap.registerPlugin(ScrollTrigger);
    
    // 自定义光标逻辑
    const cursor = document.querySelector('.cursor');
    const follower = document.querySelector('.cursor-follower');
    let fx = 0, fy = 0, cx = 0, cy = 0;
    
    document.addEventListener('mousemove', e => {
      cx = e.clientX; cy = e.clientY;
      cursor.style.transform = `translate(${cx}px, ${cy}px)`;
    });
    
    (function loop() {
      fx += (cx - fx) * 0.12;
      fy += (cy - fy) * 0.12;
      follower.style.transform = `translate(${fx}px, ${fy}px)`;
      requestAnimationFrame(loop);
    })();
    
    document.querySelectorAll('a, button').forEach(el => {
      el.addEventListener('mouseenter', () => follower.classList.add('expanded'));
      el.addEventListener('mouseleave', () => follower.classList.remove('expanded'));
    });
  </script>
</body>
</html>
```
