# Awwwards 获奖网站交互模式参考手册

> 基于 Awwwards 官方收藏集合及历年 SOTY（年度网站）获奖作品提炼的交互设计模式。
> 每个模式附带可直接使用的实现代码，适用于追求极致体验的现代 Web 项目。

---

## 目录

1. [自定义光标系统](#1-自定义光标系统)
2. [微交互大师课](#2-微交互大师课)
3. [导航模式](#3-导航模式)
4. [WOW 时刻设计框架](#4-wow-时刻设计框架)
5. [滚动交互模式](#5-滚动交互模式)
6. [触屏 / 移动端交互](#6-触屏--移动端交互)
7. [声音设计](#7-声音设计)

---

## 1. 自定义光标系统

> **Awwwards 收藏集：466 项** — 这是获奖网站中出现频率最高的交互模式，几乎成为标配。

### 核心原理

自定义光标的本质是**隐藏系统光标 → 用 DOM 元素追踪鼠标位置 → 根据上下文切换外观**。关键在于：
- **双元素架构**：一个小圆点（精确位置）+ 一个跟随圆环（视觉反馈），两者通过 `lerp`（线性插值）产生延迟跟随效果。
- **上下文感知**：光标需要知道鼠标悬停在什么元素上，并做出对应反应。
- **移动端降级**：触屏设备没有悬停概念，需隐藏自定义光标并提供触摸反馈。

### 1.1 基础圆点 + 跟随器模式

```html
<style>
  /* 隐藏系统光标 */
  * { cursor: none !important; }

  .cursor-dot {
    position: fixed;
    top: 0; left: 0;
    width: 8px; height: 8px;
    background: #000;
    border-radius: 50%;
    pointer-events: none;
    z-index: 99999;
    transform: translate(-50%, -50%);
    transition: width 0.3s ease, height 0.3s ease, background 0.3s ease;
  }

  .cursor-ring {
    position: fixed;
    top: 0; left: 0;
    width: 40px; height: 40px;
    border: 1.5px solid rgba(0,0,0,0.5);
    border-radius: 50%;
    pointer-events: none;
    z-index: 99998;
    transform: translate(-50%, -50%);
    transition: width 0.3s ease, height 0.3s ease, border-color 0.3s ease;
  }
</style>

<div class="cursor-dot"></div>
<div class="cursor-ring"></div>
```

```javascript
class CustomCursor {
  constructor() {
    // 移动端不初始化自定义光标
    if ('ontouchstart' in window) return;

    this.dot = document.querySelector('.cursor-dot');
    this.ring = document.querySelector('.cursor-ring');

    // 光标实际位置（用于 dot — 即时跟随）
    this.pos = { x: 0, y: 0 };
    // 跟随器目标位置（用于 ring — 延迟跟随）
    this.ringPos = { x: 0, y: 0 };

    this.init();
  }

  init() {
    // 即时更新 dot 位置
    document.addEventListener('mousemove', (e) => {
      this.pos.x = e.clientX;
      this.pos.y = e.clientY;
      this.dot.style.left = `${e.clientX}px`;
      this.dot.style.top = `${e.clientY}px`;
    });

    // 用 requestAnimationFrame 让 ring 通过 lerp 平滑跟随
    this.animate();
  }

  animate() {
    // lerp 系数：越小越延迟（0.08 ~ 0.15 体验最佳）
    const lerp = (start, end, factor) => start + (end - start) * factor;

    this.ringPos.x = lerp(this.ringPos.x, this.pos.x, 0.12);
    this.ringPos.y = lerp(this.ringPos.y, this.pos.y, 0.12);

    this.ring.style.left = `${this.ringPos.x}px`;
    this.ring.style.top = `${this.ringPos.y}px`;

    requestAnimationFrame(() => this.animate());
  }
}

new CustomCursor();
```

### 1.2 悬停状态变化（放大 / 变形 / 变色）

通过 `data-cursor` 属性标记不同交互区域：

```html
<a href="#" data-cursor="expand">查看项目</a>
<button data-cursor="pointer">提交</button>
<div data-cursor="view">图片画廊</div>
```

```javascript
class CustomCursor {
  // ... 继承上面的构造函数，添加以下方法：

  bindHoverEvents() {
    // [data-cursor="expand"] — 环形放大（表示"可点击的链接"）
    const expanders = document.querySelectorAll('[data-cursor="expand"]');
    expanders.forEach(el => {
      el.addEventListener('mouseenter', () => {
        this.ring.style.width = '64px';
        this.ring.style.height = '64px';
        this.ring.style.borderColor = 'rgba(0,0,0,0.2)';
        this.dot.style.transform = 'translate(-50%,-50%) scale(0.5)';
      });
      el.addEventListener('mouseleave', () => {
        this.ring.style.width = '40px';
        this.ring.style.height = '40px';
        this.ring.style.borderColor = 'rgba(0,0,0,0.5)';
        this.dot.style.transform = 'translate(-50%,-50%) scale(1)';
      });
    });

    // [data-cursor="pointer"] — 变为竖线（表示按钮/输入框）
    const pointers = document.querySelectorAll('[data-cursor="pointer"]');
    pointers.forEach(el => {
      el.addEventListener('mouseenter', () => {
        this.dot.style.width = '3px';
        this.dot.style.height = '28px';
        this.dot.style.borderRadius = '2px';
        this.ring.style.opacity = '0';
      });
      el.addEventListener('mouseleave', () => {
        this.dot.style.width = '8px';
        this.dot.style.height = '8px';
        this.dot.style.borderRadius = '50%';
        this.ring.style.opacity = '1';
      });
    });

    // [data-cursor="view"] — 中间出现眼睛图标（表示"查看/预览"）
    const viewers = document.querySelectorAll('[data-cursor="view"]');
    viewers.forEach(el => {
      el.addEventListener('mouseenter', () => {
        this.ring.style.width = '72px';
        this.ring.style.height = '72px';
        this.ring.style.background = 'rgba(0,0,0,0.06)';
        this.dot.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>';
      });
      el.addEventListener('mouseleave', () => {
        this.ring.style.width = '40px';
        this.ring.style.height = '40px';
        this.ring.style.background = 'transparent';
        this.dot.innerHTML = '';
      });
    });
  }
}
```

### 1.3 磁性光标效果（Magnetic Cursor）

当鼠标接近按钮时，按钮向光标方向"吸附"偏移：

```javascript
class MagneticElement {
  constructor(el, strength = 0.35) {
    this.el = el;
    this.strength = strength;
    this.bounding = el.getBoundingClientRect();

    el.addEventListener('mousemove', (e) => {
      const dx = e.clientX - (this.bounding.left + this.bounding.width / 2);
      const dy = e.clientY - (this.bounding.top + this.bounding.height / 2);
      this.el.style.transform = `translate(${dx * this.strength}px, ${dy * this.strength}px)`;
    });

    el.addEventListener('mouseleave', () => {
      this.el.style.transition = 'transform 0.5s cubic-bezier(0.23, 1, 0.32, 1)';
      this.el.style.transform = 'translate(0, 0)';
      // transition 结束后清除，避免干扰 hover scale
      setTimeout(() => { this.el.style.transition = ''; }, 500);
    });

    // 窗口 resize 时更新边界
    window.addEventListener('resize', () => {
      this.bounding = el.getBoundingClientRect();
    });
  }
}

// 使用方式
document.querySelectorAll('.magnetic').forEach(el => new MagneticElement(el));
```

### 1.4 光标文字（Cursor Text）

鼠标悬停时在光标位置显示文字：

```html
<a href="/work" data-cursor-text="探索">作品集</a>
```

```javascript
// 在 CustomCursor 类中添加：
initCursorText() {
  this.cursorText = document.createElement('div');
  this.cursorText.className = 'cursor-text';
  this.cursorText.style.cssText = `
    position: fixed; top: 0; left: 0; z-index: 99997;
    pointer-events: none; font-size: 12px; font-weight: 600;
    letter-spacing: 0.05em; text-transform: uppercase;
    transform: translate(-50%, -50%);
    opacity: 0; transition: opacity 0.3s ease;
    color: #000;
  `;
  document.body.appendChild(this.cursorText);

  document.querySelectorAll('[data-cursor-text]').forEach(el => {
    el.addEventListener('mouseenter', () => {
      this.cursorText.textContent = el.dataset.cursorText;
      this.cursorText.style.opacity = '1';
      this.dot.style.opacity = '0';
      this.ring.style.width = '80px';
      this.ring.style.height = '80px';
    });
    el.addEventListener('mouseleave', () => {
      this.cursorText.style.opacity = '0';
      this.dot.style.opacity = '1';
      this.ring.style.width = '40px';
      this.ring.style.height = '40px';
    });
  });

  // cursorText 跟随 ring 的位置（在 animate 循环中添加）
  // this.cursorText.style.left = `${this.ringPos.x}px`;
  // this.cursorText.style.top = `${this.ringPos.y}px`;
}
```

### 1.5 移动端降级策略

```javascript
class CustomCursor {
  constructor() {
    this.isMobile = 'ontouchstart' in window
      || navigator.maxTouchPoints > 0
      || window.matchMedia('(max-width: 768px)').matches;

    if (this.isMobile) {
      this.setupTouchFeedback();
      return;
    }

    // ... 桌面端光标逻辑
  }

  setupTouchFeedback() {
    // 移动端：点击时添加涟漪效果
    document.addEventListener('touchstart', (e) => {
      const touch = e.touches[0];
      const ripple = document.createElement('div');
      ripple.style.cssText = `
        position: fixed;
        left: ${touch.clientX}px; top: ${touch.clientY}px;
        width: 20px; height: 20px;
        border-radius: 50%;
        background: rgba(0,0,0,0.1);
        transform: translate(-50%, -50%) scale(0);
        animation: touchRipple 0.6s ease-out forwards;
        pointer-events: none; z-index: 99999;
      `;
      document.body.appendChild(ripple);
      setTimeout(() => ripple.remove(), 600);
    }, { passive: true });
  }
}

// touchRipple 动画定义
const style = document.createElement('style');
style.textContent = `
  @keyframes touchRipple {
    to { transform: translate(-50%, -50%) scale(6); opacity: 0; }
  }
`;
document.head.appendChild(style);
```

---

## 2. 微交互大师课

> **Awwwards 收藏集：243 项** — 微交互是区分"好网站"与"伟大网站"的关键。

### 2.1 悬停状态（Hover States）

**下划线揭示动画**（文字链接经典模式）：

```css
.hover-underline {
  position: relative;
  display: inline-block;
  text-decoration: none;
  color: inherit;
}

.hover-underline::after {
  content: '';
  position: absolute;
  bottom: -2px; left: 0;
  width: 100%; height: 1.5px;
  background: currentColor;
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 0.4s cubic-bezier(0.23, 1, 0.32, 1);
}

.hover-underline:hover::after {
  transform: scaleX(1);
  transform-origin: left;
}
```

**悬停颜色渐变过渡**：

```css
.color-shift {
  transition: color 0.4s ease;
  background: linear-gradient(90deg, #ff6b6b, #ffd93d, #6bcb77, #4d96ff);
  background-size: 300% 100%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: colorShift 4s ease infinite paused;
}

.color-shift:hover {
  animation-play-state: running;
}

@keyframes colorShift {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
```

**悬停缩放 + 阴影组合**（卡片常用）：

```css
.card-hover {
  transition: transform 0.5s cubic-bezier(0.23, 1, 0.32, 1),
              box-shadow 0.5s cubic-bezier(0.23, 1, 0.32, 1);
  will-change: transform;
}

.card-hover:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow:
    0 20px 40px rgba(0, 0, 0, 0.08),
    0 8px 16px rgba(0, 0, 0, 0.04);
}
```

### 2.2 按钮交互

**按压反馈**：

```css
.btn-press {
  transition: transform 0.15s ease, box-shadow 0.15s ease;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.btn-press:active {
  transform: scale(0.96) translateY(2px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
```

**涟漪点击效果**（Material Design 风格）：

```javascript
document.querySelectorAll('.btn-ripple').forEach(btn => {
  btn.addEventListener('click', function(e) {
    const rect = this.getBoundingClientRect();
    const ripple = document.createElement('span');
    const size = Math.max(rect.width, rect.height) * 2;

    ripple.style.cssText = `
      position: absolute; border-radius: 50%;
      width: ${size}px; height: ${size}px;
      left: ${e.clientX - rect.left - size/2}px;
      top: ${e.clientY - rect.top - size/2}px;
      background: rgba(255,255,255,0.3);
      transform: scale(0); opacity: 1;
      animation: ripple 0.6s ease-out forwards;
      pointer-events: none;
    `;

    this.style.position = 'relative';
    this.style.overflow = 'hidden';
    this.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
  });
});
```

### 2.3 链接悬停图片预览

```javascript
class ImagePreview {
  constructor() {
    this.preview = document.createElement('div');
    this.preview.className = 'link-preview';
    this.preview.style.cssText = `
      position: fixed; z-index: 9999; pointer-events: none;
      width: 320px; height: 200px; border-radius: 8px;
      overflow: hidden; opacity: 0;
      transition: opacity 0.3s ease, transform 0.3s ease;
      transform: translate(-50%, -100%) translateY(-16px);
      box-shadow: 0 20px 60px rgba(0,0,0,0.15);
    `;
    const img = document.createElement('img');
    img.style.cssText = 'width: 100%; height: 100%; object-fit: cover;';
    this.preview.appendChild(img);
    document.body.appendChild(this.preview);
    this.img = img;

    this.bindLinks();
  }

  bindLinks() {
    document.querySelectorAll('[data-preview]').forEach(link => {
      link.addEventListener('mouseenter', (e) => {
        this.img.src = link.dataset.preview;
        this.preview.style.left = `${e.clientX}px`;
        this.preview.style.top = `${e.clientY}px`;
        this.preview.style.opacity = '1';
      });

      link.addEventListener('mousemove', (e) => {
        this.preview.style.left = `${e.clientX}px`;
        this.preview.style.top = `${e.clientY}px`;
      });

      link.addEventListener('mouseleave', () => {
        this.preview.style.opacity = '0';
      });
    });
  }
}
```

### 2.4 表单交互

**浮动标签（Floating Labels）**：

```html
<div class="form-group">
  <input type="email" id="email" required placeholder=" ">
  <label for="email">电子邮箱</label>
</div>
```

```css
.form-group {
  position: relative;
  margin-bottom: 2rem;
}

.form-group input {
  width: 100%;
  padding: 16px 0 8px;
  border: none;
  border-bottom: 2px solid #e0e0e0;
  font-size: 16px;
  outline: none;
  transition: border-color 0.3s ease;
  background: transparent;
}

.form-group label {
  position: absolute;
  left: 0; top: 16px;
  font-size: 16px;
  color: #999;
  pointer-events: none;
  transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
}

/* 输入框聚焦或有内容时，标签上浮 */
.form-group input:focus + label,
.form-group input:not(:placeholder-shown) + label {
  top: -4px;
  font-size: 12px;
  color: #000;
  font-weight: 600;
}

.form-group input:focus {
  border-bottom-color: #000;
}
```

**验证反馈动画**：

```javascript
class FormValidator {
  constructor(form) {
    this.form = form;
    form.querySelectorAll('input').forEach(input => {
      input.addEventListener('blur', () => this.validateField(input));
      input.addEventListener('input', () => this.clearError(input));
    });
  }

  validateField(input) {
    const group = input.closest('.form-group');
    const isValid = input.checkValidity();

    group.classList.toggle('valid', isValid);
    group.classList.toggle('invalid', !isValid);

    if (!isValid) {
      group.querySelector('.error-msg').textContent = input.validationMessage;
    }
  }

  clearError(input) {
    input.closest('.form-group').classList.remove('invalid');
  }
}
```

### 2.5 卡片倾斜悬停（Vanilla-Tilt 模式）

```javascript
class TiltCard {
  constructor(el, options = {}) {
    this.el = el;
    this.maxTilt = options.maxTilt || 10;
    this.perspective = options.perspective || 1000;
    this.speed = options.speed || 400;
    this.glare = options.glare || true;

    this.init();
  }

  init() {
    this.el.style.transformStyle = 'preserve-3d';
    this.el.style.transition = `transform 0.1s ease-out`;

    // 添加光泽层
    if (this.glare) {
      const glare = document.createElement('div');
      glare.className = 'tilt-glare';
      glare.style.cssText = `
        position: absolute; inset: 0; border-radius: inherit;
        pointer-events: none; opacity: 0;
        transition: opacity 0.3s ease;
        background: linear-gradient(
          135deg,
          rgba(255,255,255,0.4) 0%,
          rgba(255,255,255,0) 60%
        );
        transform: translateZ(40px);
      `;
      this.el.style.position = 'relative';
      this.el.appendChild(glare);
      this.glareEl = glare;
    }

    this.el.addEventListener('mousemove', (e) => this.onMove(e));
    this.el.addEventListener('mouseleave', () => this.onLeave());
  }

  onMove(e) {
    const rect = this.el.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const rotateX = ((y - centerY) / centerY) * -this.maxTilt;
    const rotateY = ((x - centerX) / centerX) * this.maxTilt;

    this.el.style.transform = `
      perspective(${this.perspective}px)
      rotateX(${rotateX}deg)
      rotateY(${rotateY}deg)
      scale3d(1.03, 1.03, 1.03)
    `;

    if (this.glareEl) {
      this.glareEl.style.opacity = '1';
      // 光泽跟随鼠标
      const glareX = (x / rect.width) * 100;
      const glareY = (y / rect.height) * 100;
      this.glareEl.style.background = `
        radial-gradient(
          circle at ${glareX}% ${glareY}%,
          rgba(255,255,255,0.35) 0%,
          transparent 60%
        )
      `;
    }
  }

  onLeave() {
    this.el.style.transition = `transform ${this.speed}ms cubic-bezier(0.23, 1, 0.32, 1)`;
    this.el.style.transform = `
      perspective(${this.perspective}px)
      rotateX(0) rotateY(0) scale3d(1, 1, 1)
    `;
    if (this.glareEl) this.glareEl.style.opacity = '0';

    // 重置 transition 时间
    setTimeout(() => {
      this.el.style.transition = 'transform 0.1s ease-out';
    }, this.speed);
  }
}
```

### 2.6 加载状态

**骨架屏（Skeleton Screen）**：

```css
.skeleton {
  background: linear-gradient(
    90deg,
    #f0f0f0 25%,
    #e0e0e0 50%,
    #f0f0f0 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
  border-radius: 4px;
}

@keyframes shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* 骨架屏排版示例 */
.skeleton-card {
  padding: 24px;
  border-radius: 12px;
  background: #fafafa;
}

.skeleton-card .avatar {
  width: 48px; height: 48px;
  border-radius: 50%;
}

.skeleton-card .title {
  width: 60%; height: 20px;
  margin-top: 16px;
}

.skeleton-card .description {
  width: 100%; height: 14px;
  margin-top: 12px;
}

.skeleton-card .description:last-child {
  width: 80%;
}
```

---

## 3. 导航模式

### 3.1 全屏沉浸式导航（Lando Norris 风格）

```javascript
class FullscreenNav {
  constructor() {
    this.nav = document.querySelector('.fullscreen-nav');
    this.overlay = document.querySelector('.nav-overlay');
    this.isOpen = false;

    // 导航项逐个延迟入场
    this.items = this.nav.querySelectorAll('.nav-item');
    this.items.forEach((item, i) => {
      item.style.transition = `
        transform 0.6s cubic-bezier(0.23, 1, 0.32, 1) ${i * 0.08}s,
        opacity 0.6s cubic-bezier(0.23, 1, 0.32, 1) ${i * 0.08}s
      `;
    });

    this.toggle = document.querySelector('.nav-toggle');
    this.toggle.addEventListener('click', () => this.toggleNav());
  }

  toggleNav() {
    this.isOpen = !this.isOpen;
    this.overlay.classList.toggle('active', this.isOpen);
    this.toggle.classList.toggle('active', this.isOpen);

    this.items.forEach(item => {
      item.style.transform = this.isOpen ? 'translateY(0)' : 'translateY(40px)';
      item.style.opacity = this.isOpen ? '1' : '0';
    });
  }
}
```

```css
.fullscreen-nav {
  position: fixed; inset: 0; z-index: 1000;
  display: flex; flex-direction: column;
  justify-content: center; align-items: flex-start;
  padding: 0 10vw;
  background: #0a0a0a;
  clip-path: circle(0% at calc(100% - 40px) 40px);
  transition: clip-path 0.8s cubic-bezier(0.65, 0, 0.35, 1);
}

.fullscreen-nav.active {
  clip-path: circle(150% at calc(100% - 40px) 40px);
}

.fullscreen-nav .nav-item {
  font-size: clamp(2rem, 5vw, 4.5rem);
  font-weight: 700;
  color: #fff;
  transform: translateY(40px);
  opacity: 0;
}

/* 汉堡菜单变形为 X */
.nav-toggle {
  position: fixed; top: 24px; right: 24px; z-index: 1001;
  width: 48px; height: 48px;
  background: none; border: none; cursor: pointer;
}

.nav-toggle span {
  display: block;
  width: 28px; height: 2px;
  background: #000;
  margin: 6px auto;
  transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
}

.nav-toggle.active span:nth-child(1) {
  transform: rotate(45deg) translate(5px, 6px);
  background: #fff;
}

.nav-toggle.active span:nth-child(2) {
  opacity: 0;
}

.nav-toggle.active span:nth-child(3) {
  transform: rotate(-45deg) translate(5px, -6px);
  background: #fff;
}
```

### 3.2 侧边栏滑出导航

```css
.sidebar-nav {
  position: fixed;
  top: 0; right: 0;
  width: min(400px, 85vw);
  height: 100vh;
  background: #fff;
  box-shadow: -20px 0 60px rgba(0,0,0,0.1);
  transform: translateX(100%);
  transition: transform 0.6s cubic-bezier(0.23, 1, 0.32, 1);
  z-index: 1000;
  padding: 80px 40px;
}

.sidebar-nav.open {
  transform: translateX(0);
}

.sidebar-backdrop {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.4);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.4s ease;
  z-index: 999;
}

.sidebar-backdrop.visible {
  opacity: 1;
  pointer-events: auto;
}
```

### 3.3 游戏化导航（Messenger SOTY 2025 灵感）

将导航项设计为可交互的游戏元素——例如弹跳球体、角色选择界面：

```javascript
class GameNav {
  constructor() {
    this.container = document.querySelector('.game-nav');
    this.navItems = this.container.querySelectorAll('.game-nav-item');

    // 每个导航项是一个可"弹射"的球体
    this.navItems.forEach((item, i) => {
      item.addEventListener('mouseenter', () => {
        item.style.transform = `scale(1.2) rotate(${Math.random() * 20 - 10}deg)`;
        item.style.boxShadow = `0 0 30px rgba(${this.getHue(i)}, 80%, 60%, 0.5)`;
      });
      item.addEventListener('mouseleave', () => {
        item.style.transform = 'scale(1) rotate(0deg)';
        item.style.boxShadow = 'none';
      });
      item.addEventListener('click', () => {
        // 点击后播放弹跳动画
        item.animate([
          { transform: 'scale(0.8)' },
          { transform: 'scale(1.3)' },
          { transform: 'scale(1)' }
        ], { duration: 400, easing: 'cubic-bezier(0.34, 1.56, 0.64, 1)' });
      });
    });
  }

  getHue(index) {
    return (index * 60) % 360; // 每个项不同色相
  }
}
```

### 3.4 水平标签页导航

```css
.tab-nav {
  display: flex;
  gap: 0;
  border-bottom: 1px solid #e0e0e0;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}

.tab-nav::-webkit-scrollbar { display: none; }

.tab-nav-item {
  padding: 16px 24px;
  white-space: nowrap;
  font-weight: 500;
  position: relative;
  transition: color 0.3s ease;
}

/* 滑动指示器 */
.tab-indicator {
  position: absolute;
  bottom: 0; height: 2px;
  background: #000;
  transition: left 0.4s cubic-bezier(0.23, 1, 0.32, 1),
              width 0.4s cubic-bezier(0.23, 1, 0.32, 1);
}
```

```javascript
class TabNav {
  constructor() {
    this.nav = document.querySelector('.tab-nav');
    this.items = this.nav.querySelectorAll('.tab-nav-item');
    this.indicator = document.querySelector('.tab-indicator');

    this.items.forEach(item => {
      item.addEventListener('click', () => this.setActive(item));
    });

    // 初始化指示器位置
    this.setActive(this.items[0]);
  }

  setActive(activeItem) {
    const rect = activeItem.getBoundingClientRect();
    const navRect = this.nav.getBoundingClientRect();

    this.indicator.style.left = `${rect.left - navRect.left}px`;
    this.indicator.style.width = `${rect.width}px`;

    this.items.forEach(item => item.classList.remove('active'));
    activeItem.classList.add('active');
  }
}
```

### 3.5 滚动触发导航（粘性 / 隐藏）

```javascript
class ScrollNav {
  constructor(nav) {
    this.nav = nav;
    this.lastScroll = 0;
    this.threshold = 100;

    window.addEventListener('scroll', () => this.onScroll(), { passive: true });
  }

  onScroll() {
    const currentScroll = window.scrollY;

    // 向下滚动超过阈值 → 隐藏导航
    if (currentScroll > this.threshold && currentScroll > this.lastScroll) {
      this.nav.style.transform = 'translateY(-100%)';
    }
    // 向上滚动 → 显示导航
    else {
      this.nav.style.transform = 'translateY(0)';
    }

    // 添加背景模糊效果
    this.nav.classList.toggle('scrolled', currentScroll > this.threshold);

    this.lastScroll = currentScroll;
  }
}
```

```css
.scroll-nav {
  position: fixed; top: 0; left: 0; right: 0;
  z-index: 100;
  transition: transform 0.4s cubic-bezier(0.23, 1, 0.32, 1),
              background 0.4s ease,
              backdrop-filter 0.4s ease;
  padding: 20px 0;
}

.scroll-nav.scrolled {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  padding: 12px 0;
  border-bottom: 1px solid rgba(0,0,0,0.05);
}
```

### 3.6 面包屑作为设计元素

```css
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  font-weight: 500;
}

.breadcrumb a {
  color: #999;
  text-decoration: none;
  transition: color 0.3s ease;
  position: relative;
}

.breadcrumb a::after {
  content: '';
  position: absolute;
  bottom: -2px; left: 0;
  width: 100%; height: 1px;
  background: currentColor;
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 0.4s cubic-bezier(0.23, 1, 0.32, 1);
}

.breadcrumb a:hover { color: #000; }
.breadcrumb a:hover::after { transform: scaleX(1); transform-origin: left; }

.breadcrumb .separator {
  color: #ccc;
  font-size: 10px;
}

.breadcrumb .current {
  color: #000;
  font-weight: 700;
}
```

---

## 4. WOW 时刻设计框架

> WOW 时刻是让访客发出"哇"的那一刻。它不是某个具体技术，而是一种**设计思维**。

### 核心公式

```
WOW = Unexpected × Emotional × Polished

Unexpected（意料之外）：打破用户对网页的预期
Emotional（情感共鸣）：让用户感到惊喜、兴奋、感动
Polished（极致打磨）：每个像素、每帧动画都经过精心调优

三者缺一不可。没有 Unexpected 就只是"好看"，没有 Emotional 就只是"炫技"，没有 Polished 就只是"半成品"。
```

### 设计 YOUR WOW 时刻的步骤

1. **明确核心印象**：用户离开网站后，唯一会记住的瞬间是什么？
2. **选择表达载体**：3D / 滚动叙事 / 数据可视化 / 游戏 / 艺术装置
3. **设计惊喜转折**：在哪个节点制造"意料之外"？
4. **注入情感层**：幽默 / 震撼 / 温暖 / 好奇 — 选一种
5. **极致打磨**：easing、timing、loading、降级方案，全部到位

### 模式 1：3D 游戏导航（Bruno Simon — SOTY 2023）

将整个网站变成一个 3D 游戏场景，用户通过驾驶汽车"驶入"不同项目页面。

**关键实现要素**：

```javascript
// Three.js 场景初始化骨架
import * as THREE from 'three';

class GameWebsite {
  constructor() {
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });

    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    document.getElementById('canvas-container').appendChild(this.renderer.domElement);

    // 环境光 + 方向光
    this.scene.add(new THREE.AmbientLight(0xffffff, 0.6));
    const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
    dirLight.position.set(5, 10, 7);
    dirLight.castShadow = true;
    this.scene.add(dirLight);

    this.initPhysics();
    this.initControls();
    this.animate();
  }

  initControls() {
    // WASD 或方向键控制移动
    this.keys = {};
    window.addEventListener('keydown', e => this.keys[e.key] = true);
    window.addEventListener('keyup', e => this.keys[e.key] = false);
  }

  animate() {
    requestAnimationFrame(() => this.animate());

    // 更新物理引擎
    this.updatePhysics();
    // 更新相机跟随
    this.updateCamera();
    // 检测碰撞（到达项目区域）
    this.checkCollisions();

    this.renderer.render(this.scene, this.camera);
  }
}
```

### 模式 2：交互式产品游乐场（Lando Norris）

将产品（赛车/汽车）放入可旋转、可交互的 3D 空间，用户自由探索。

```javascript
// 核心模式：可拖拽旋转的产品查看器
class ProductViewer {
  constructor(container) {
    this.container = container;
    this.isDragging = false;
    this.rotation = { x: 0, y: 0 };
    this.velocity = { x: 0, y: 0 };

    // 触摸/鼠标事件
    container.addEventListener('mousedown', (e) => this.onDragStart(e));
    container.addEventListener('mousemove', (e) => this.onDrag(e));
    container.addEventListener('mouseup', () => this.onDragEnd());
    container.addEventListener('touchstart', (e) => this.onDragStart(e.touches[0]), { passive: true });
    container.addEventListener('touchmove', (e) => this.onDrag(e.touches[0]), { passive: true });
    container.addEventListener('touchend', () => this.onDragEnd());

    this.animate();
  }

  onDragStart(e) {
    this.isDragging = true;
    this.startX = e.clientX;
    this.startY = e.clientY;
    this.velocity = { x: 0, y: 0 };
  }

  onDrag(e) {
    if (!this.isDragging) return;
    const dx = e.clientX - this.startX;
    const dy = e.clientY - this.startY;
    this.velocity.x = dy * 0.005;
    this.velocity.y = dx * 0.005;
    this.rotation.x += this.velocity.x;
    this.rotation.y += this.velocity.y;
    this.startX = e.clientX;
    this.startY = e.clientY;
  }

  onDragEnd() {
    this.isDragging = false;
    // 惯性衰减
  }

  animate() {
    requestAnimationFrame(() => this.animate());

    if (!this.isDragging) {
      this.velocity.x *= 0.95; // 摩擦力衰减
      this.velocity.y *= 0.95;
      this.rotation.x += this.velocity.x;
      this.rotation.y += this.velocity.y;
    }

    this.container.style.transform =
      `rotateX(${this.rotation.x}deg) rotateY(${this.rotation.y}deg)`;
  }
}
```

### 模式 3：滚动叙事体验（Igloo Inc）

用滚动驱动整个故事线，每一屏是一个"章节"。

```javascript
class ScrollStory {
  constructor() {
    this.sections = document.querySelectorAll('.story-section');
    this.progressBar = document.querySelector('.story-progress');

    // 使用 IntersectionObserver 触发章节入场
    this.observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          this.updateProgress(entry.target);
        }
      });
    }, { threshold: 0.3 });

    this.sections.forEach(section => this.observer.observe(section));

    // 滚动进度条
    window.addEventListener('scroll', () => this.updateProgress(), { passive: true });
  }

  updateProgress(activeSection) {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = (scrollTop / docHeight) * 100;
    this.progressBar.style.width = `${progress}%`;
  }
}
```

```css
.story-section {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: translateY(60px);
  transition: opacity 0.8s cubic-bezier(0.23, 1, 0.32, 1),
              transform 0.8s cubic-bezier(0.23, 1, 0.32, 1);
}

.story-section.visible {
  opacity: 1;
  transform: translateY(0);
}

/* 章节标题揭示动画 */
.story-section .chapter-title {
  clip-path: inset(0 100% 0 0);
  animation: revealText 1s cubic-bezier(0.23, 1, 0.32, 1) 0.3s forwards;
}

.story-section.visible .chapter-title {
  clip-path: inset(0 0% 0 0);
}

@keyframes revealText {
  to { clip-path: inset(0 0% 0 0); }
}
```

### 模式 4：数据 × 娱乐（Shopify Globe）

用 Three.js 创建交互式 3D 地球，实时展示全球数据流。

```javascript
// 关键要素：
// 1. 3D 地球模型（球体 + 纹理）
// 2. 数据点标记（发光的小点 + 弧线）
// 3. 鼠标拖拽旋转
// 4. 滚轮缩放
// 5. 点击数据点弹出详情

class DataGlobe {
  constructor() {
    this.scene = new THREE.Scene();
    // ... 初始化渲染器、相机

    // 创建地球
    const geometry = new THREE.SphereGeometry(5, 64, 64);
    const material = new THREE.MeshPhongMaterial({
      color: 0x1a1a2e,
      emissive: 0x0a0a1e,
      specular: 0x333366,
      shininess: 25
    });
    this.globe = new THREE.Mesh(geometry, material);
    this.scene.add(this.globe);

    // 添加数据弧线
    this.addDataArcs();

    // 添加发光数据点
    this.addDataPoints();

    // 自动旋转 + 用户交互
    this.autoRotate = true;
    this.addInteraction();
  }

  addDataArcs() {
    // 在地球表面两点之间绘制发光弧线
    const points = [
      { from: [40.7, -74.0], to: [51.5, -0.1] },   // NYC → London
      { from: [35.6, 139.7], to: [1.3, 103.8] },    // Tokyo → Singapore
    ];

    points.forEach(({ from, to }) => {
      const curve = new THREE.QuadraticBezierCurve3(
        this.latLonToVector3(from[0], from[1], 5),
        this.latLonToVector3(
          (from[0] + to[0]) / 2,
          (from[1] + to[1]) / 2,
          7 // 弧线高度
        ),
        this.latLonToVector3(to[0], to[1], 5)
      );

      const lineGeometry = new THREE.TubeGeometry(curve, 64, 0.02, 8, false);
      const lineMaterial = new THREE.MeshBasicMaterial({
        color: 0x00d4ff,
        transparent: true,
        opacity: 0.6
      });
      this.scene.add(new THREE.Mesh(lineGeometry, lineMaterial));
    });
  }

  latLonToVector3(lat, lon, radius) {
    const phi = (90 - lat) * (Math.PI / 180);
    const theta = (lon + 180) * (Math.PI / 180);
    return new THREE.Vector3(
      -radius * Math.sin(phi) * Math.cos(theta),
      radius * Math.cos(phi),
      radius * Math.sin(phi) * Math.sin(theta)
    );
  }
}
```

### 模式 5：艺术 × 技术融合（Ruinart）

将品牌历史/故事转化为沉浸式艺术体验，通常结合 WebGL、手势交互和声音设计。

```javascript
// 核心模式：鼠标轨迹生成粒子/笔触
class ArtCanvas {
  constructor() {
    this.canvas = document.querySelector('#art-canvas');
    this.ctx = this.canvas.getContext('2d');
    this.particles = [];
    this.isDrawing = false;

    this.resize();
    window.addEventListener('resize', () => this.resize());

    this.canvas.addEventListener('mousedown', () => this.isDrawing = true);
    this.canvas.addEventListener('mouseup', () => this.isDrawing = false);
    this.canvas.addEventListener('mousemove', (e) => this.onMove(e));

    this.animate();
  }

  onMove(e) {
    if (!this.isDrawing) return;
    const rect = this.canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    // 每次移动创建一组粒子
    for (let i = 0; i < 3; i++) {
      this.particles.push({
        x: x + (Math.random() - 0.5) * 20,
        y: y + (Math.random() - 0.5) * 20,
        vx: (Math.random() - 0.5) * 2,
        vy: (Math.random() - 0.5) * 2 - 1, // 轻微向上飘
        life: 1,
        decay: 0.005 + Math.random() * 0.01,
        size: 2 + Math.random() * 6,
        hue: (Date.now() * 0.02) % 360 // 随时间变化的色相
      });
    }
  }

  animate() {
    requestAnimationFrame(() => this.animate());
    this.ctx.fillStyle = 'rgba(0, 0, 0, 0.02)';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    this.particles.forEach((p, i) => {
      p.x += p.vx;
      p.y += p.vy;
      p.life -= p.decay;

      if (p.life <= 0) {
        this.particles.splice(i, 1);
        return;
      }

      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, p.size * p.life, 0, Math.PI * 2);
      this.ctx.fillStyle = `hsla(${p.hue}, 70%, 60%, ${p.life * 0.5})`;
      this.ctx.fill();
    });
  }
}
```

### 模式 6：微交互杰作（Messenger）

不是宏大的 3D 场景，而是通过精心设计的数十个微交互累积出极致体验。

**关键原则**：
- 每一个可交互元素都有专属的响应动画
- 状态切换有清晰的视觉叙事（展开/折叠的动画"讲故事"）
- 组合使用 CSS 动画、Web Animations API、SVG 动画
- 音效与视觉同步

---

## 5. 滚动交互模式

### 5.1 自定义滚动进度条

```javascript
class ScrollProgress {
  constructor() {
    this.bar = document.querySelector('.scroll-progress');
    this.createBar();

    window.addEventListener('scroll', () => this.update(), { passive: true });
  }

  createBar() {
    if (!this.bar) {
      this.bar = document.createElement('div');
      this.bar.className = 'scroll-progress';
      this.bar.style.cssText = `
        position: fixed; top: 0; left: 0; height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        z-index: 10000; width: 0%;
        transition: width 0.1s linear;
      `;
      document.body.appendChild(this.bar);
    }
  }

  update() {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = (scrollTop / docHeight) * 100;
    this.bar.style.width = `${progress}%`;
  }
}
```

### 5.2 滚动触发的章节揭示

```javascript
class ScrollReveal {
  constructor(options = {}) {
    this.threshold = options.threshold || 0.15;
    this.rootMargin = options.rootMargin || '0px 0px -50px 0px';

    this.observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          // 如果只需要触发一次，可以取消观察
          // this.observer.unobserve(entry.target);
        }
      });
    }, { threshold: this.threshold, rootMargin: this.rootMargin });

    document.querySelectorAll('[data-reveal]').forEach(el => {
      this.observer.observe(el);
    });
  }
}

// HTML 使用方式：
// <div data-reveal="fade-up">内容</div>
// <div data-reveal="fade-left">内容</div>
// <div data-reveal="scale-in">内容</div>
// <div data-reveal="stagger">子元素逐个入场</div>
```

```css
/* 基础揭示动画 */
[data-reveal] {
  opacity: 0;
  transition: opacity 0.8s cubic-bezier(0.23, 1, 0.32, 1),
              transform 0.8s cubic-bezier(0.23, 1, 0.32, 1);
}

[data-reveal].revealed { opacity: 1; transform: none; }

[data-reveal="fade-up"]    { transform: translateY(60px); }
[data-reveal="fade-down"]  { transform: translateY(-60px); }
[data-reveal="fade-left"]  { transform: translateX(60px); }
[data-reveal="fade-right"] { transform: translateX(-60px); }
[data-reveal="scale-in"]   { transform: scale(0.85); }

/* 交错入场 */
[data-reveal="stagger"] .stagger-item {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}

[data-reveal="stagger"].revealed .stagger-item {
  opacity: 1;
  transform: translateY(0);
}

/* 通过 CSS 变量实现交错延迟 */
[data-reveal="stagger"].revealed .stagger-item:nth-child(1) { transition-delay: 0.05s; }
[data-reveal="stagger"].revealed .stagger-item:nth-child(2) { transition-delay: 0.1s; }
[data-reveal="stagger"].revealed .stagger-item:nth-child(3) { transition-delay: 0.15s; }
[data-reveal="stagger"].revealed .stagger-item:nth-child(4) { transition-delay: 0.2s; }
[data-reveal="stagger"].revealed .stagger-item:nth-child(5) { transition-delay: 0.25s; }
```

### 5.3 基于滚动速度的效果

```javascript
class ScrollSpeedEffect {
  constructor() {
    this.lastScrollTop = 0;
    this.lastTime = Date.now();
    this.speed = 0;

    window.addEventListener('scroll', () => this.onScroll(), { passive: true });
    requestAnimationFrame(() => this.decelerate());
  }

  onScroll() {
    const now = Date.now();
    const delta = now - this.lastTime;
    const scrollTop = window.scrollY;
    const distance = Math.abs(scrollTop - this.lastScrollTop);

    // 像素/秒
    this.speed = (distance / delta) * 1000;

    this.lastScrollTop = scrollTop;
    this.lastTime = now;

    // 根据速度调整页面效果
    document.body.classList.toggle('fast-scroll', this.speed > 2000);
    document.body.classList.toggle('slow-scroll', this.speed < 500);
  }

  decelerate() {
    this.speed *= 0.95; // 速度衰减
    if (this.speed < 10) this.speed = 0;
    document.body.classList.toggle('fast-scroll', this.speed > 2000);
    requestAnimationFrame(() => this.decelerate());
  }
}
```

```css
/* 快速滚动时的视觉反馈 */
.fast-scroll .hero-title {
  transform: scale(0.95);
  filter: blur(2px);
}

.slow-scroll .hero-title {
  transform: scale(1);
  filter: blur(0);
}

.fast-scroll .parallax-bg {
  filter: blur(4px) brightness(0.7);
}
```

### 5.4 Scroll Snap 分屏滚动

```css
.snap-container {
  height: 100vh;
  overflow-y: scroll;
  scroll-snap-type: y mandatory;
  scroll-behavior: smooth;
}

.snap-section {
  height: 100vh;
  scroll-snap-align: start;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

### 5.5 无限滚动 + 加载动画

```javascript
class InfiniteScroll {
  constructor(loader) {
    this.loader = loader;
    this.loading = false;
    this.page = 1;

    const observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting && !this.loading) {
        this.loadMore();
      }
    }, { rootMargin: '200px' });

    observer.observe(this.loader);
  }

  async loadMore() {
    this.loading = true;
    this.loader.innerHTML = `
      <div class="loading-dots">
        <span></span><span></span><span></span>
      </div>
    `;

    const items = await fetchItems(this.page++);

    const container = document.querySelector('#items-grid');
    items.forEach((item, i) => {
      const el = this.createItemElement(item);
      el.style.opacity = '0';
      el.style.transform = 'translateY(20px)';
      container.appendChild(el);

      // 交错入场动画
      requestAnimationFrame(() => {
        el.style.transition = `opacity 0.5s ease ${i * 0.05}s, transform 0.5s ease ${i * 0.05}s`;
        el.style.opacity = '1';
        el.style.transform = 'translateY(0)';
      });
    });

    this.loader.innerHTML = '';
    this.loading = false;
  }
}
```

```css
.loading-dots {
  display: flex;
  gap: 6px;
  justify-content: center;
  padding: 40px 0;
}

.loading-dots span {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: #999;
  animation: bounce 1.4s ease-in-out infinite;
}

.loading-dots span:nth-child(2) { animation-delay: 0.2s; }
.loading-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
  40% { transform: scale(1); opacity: 1; }
}
```

---

## 6. 触屏 / 移动端交互

### 6.1 滑动手势（水平内容切换）

```javascript
class Swipeable {
  constructor(container, options = {}) {
    this.container = container;
    this.threshold = options.threshold || 50;
    this.startX = 0;
    this.startY = 0;
    this.currentX = 0;
    this.isDragging = false;

    this.container.addEventListener('touchstart', (e) => this.onStart(e), { passive: true });
    this.container.addEventListener('touchmove', (e) => this.onMove(e), { passive: true });
    this.container.addEventListener('touchend', (e) => this.onEnd(e));

    // 也支持鼠标拖拽（桌面端调试用）
    this.container.addEventListener('mousedown', (e) => this.onStart(e));
    this.container.addEventListener('mousemove', (e) => this.onMove(e));
    this.container.addEventListener('mouseup', (e) => this.onEnd(e));
  }

  getX(e) {
    return e.touches ? e.touches[0].clientX : e.clientX;
  }

  getY(e) {
    return e.touches ? e.touches[0].clientY : e.clientY;
  }

  onStart(e) {
    this.isDragging = true;
    this.startX = this.getX(e);
    this.startY = this.getY(e);
    this.container.style.transition = 'none';
  }

  onMove(e) {
    if (!this.isDragging) return;
    this.currentX = this.getX(e) - this.startX;

    // 如果是垂直滑动更多，不处理（让页面自然滚动）
    const currentY = this.getY(e) - this.startY;
    if (Math.abs(currentY) > Math.abs(this.currentX)) {
      this.isDragging = false;
      return;
    }

    this.container.style.transform = `translateX(${this.currentX}px)`;
  }

  onEnd(e) {
    if (!this.isDragging) return;
    this.isDragging = false;

    this.container.style.transition = 'transform 0.5s cubic-bezier(0.23, 1, 0.32, 1)';

    if (Math.abs(this.currentX) > this.threshold) {
      const direction = this.currentX > 0 ? -1 : 1;
      this.container.style.transform = `translateX(${direction * 100}%)`;
      this.container.dispatchEvent(new CustomEvent('swipe', { detail: { direction } }));
    } else {
      // 回弹
      this.container.style.transform = 'translateX(0)';
    }
  }
}
```

### 6.2 下拉刷新

```javascript
class PullToRefresh {
  constructor(container, onRefresh) {
    this.container = container;
    this.onRefresh = onRefresh;
    this.startY = 0;
    this.pullDistance = 0;
    this.threshold = 80;
    this.isRefreshing = false;

    this.indicator = document.createElement('div');
    this.indicator.className = 'pull-indicator';
    this.indicator.innerHTML = `
      <svg width="24" height="24" viewBox="0 0 24 24" class="pull-icon">
        <path d="M12 2v10m0 0l-4-4m4 4l4-4M4 17a8 8 0 1016 0" stroke="currentColor"
              stroke-width="2" fill="none" stroke-linecap="round"/>
      </svg>
      <span class="pull-text">下拉刷新</span>
    `;
    this.container.prepend(this.indicator);

    this.container.addEventListener('touchstart', (e) => {
      if (this.container.scrollTop === 0) {
        this.startY = e.touches[0].clientY;
      }
    }, { passive: true });

    this.container.addEventListener('touchmove', (e) => {
      if (this.isRefreshing) return;
      if (this.container.scrollTop !== 0) return;

      this.pullDistance = Math.max(0, e.touches[0].clientY - this.startY);
      // 阻尼效果：越拉越费力
      const damped = this.pullDistance * 0.4;

      this.indicator.style.transform = `translateY(${-60 + damped}px)`;
      this.indicator.querySelector('.pull-icon').style.transform =
        `rotate(${Math.min(this.pullDistance, this.threshold) / this.threshold * 360}deg)`;

      if (damped > this.threshold) {
        this.indicator.querySelector('.pull-text').textContent = '释放刷新';
      } else {
        this.indicator.querySelector('.pull-text').textContent = '下拉刷新';
      }
    }, { passive: true });

    this.container.addEventListener('touchend', () => {
      if (this.pullDistance * 0.4 > this.threshold && !this.isRefreshing) {
        this.refresh();
      }
      this.indicator.style.transform = 'translateY(-60px)';
      this.indicator.querySelector('.pull-icon').style.transform = 'rotate(0deg)';
      this.pullDistance = 0;
    });
  }

  async refresh() {
    this.isRefreshing = true;
    this.indicator.querySelector('.pull-text').textContent = '刷新中...';
    this.indicator.classList.add('refreshing');

    await this.onRefresh();

    this.indicator.classList.remove('refreshing');
    this.indicator.querySelector('.pull-text').textContent = '下拉刷新';
    this.isRefreshing = false;
  }
}
```

```css
.pull-indicator {
  position: absolute;
  top: -60px; left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #999;
  font-size: 13px;
  transition: transform 0.3s ease;
}

.pull-indicator.refreshing .pull-icon {
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

### 6.3 双指缩放

```javascript
class PinchZoom {
  constructor(element) {
    this.el = element;
    this.scale = 1;
    this.minScale = 1;
    this.maxScale = 4;
    this.lastDistance = 0;

    this.el.addEventListener('touchstart', (e) => {
      if (e.touches.length === 2) {
        this.lastDistance = this.getDistance(e.touches);
        this.el.style.transition = 'none';
      }
    }, { passive: true });

    this.el.addEventListener('touchmove', (e) => {
      if (e.touches.length === 2) {
        e.preventDefault();
        const distance = this.getDistance(e.touches);
        this.scale = Math.min(
          this.maxScale,
          Math.max(this.minScale, this.scale * (distance / this.lastDistance))
        );
        this.el.style.transform = `scale(${this.scale})`;
        this.lastDistance = distance;
      }
    }, { passive: false });

    // 双击恢复原始大小
    let lastTap = 0;
    this.el.addEventListener('touchend', (e) => {
      const now = Date.now();
      if (now - lastTap < 300) {
        this.scale = 1;
        this.el.style.transition = 'transform 0.3s ease';
        this.el.style.transform = 'scale(1)';
      }
      lastTap = now;
    });
  }

  getDistance(touches) {
    const dx = touches[0].clientX - touches[1].clientX;
    const dy = touches[0].clientY - touches[1].clientY;
    return Math.sqrt(dx * dx + dy * dy);
  }
}
```

### 6.4 长按上下文菜单

```javascript
class LongPress {
  constructor(el, callback, duration = 500) {
    this.timer = null;
    this.isLongPress = false;

    el.addEventListener('touchstart', (e) => {
      this.isLongPress = false;
      this.timer = setTimeout(() => {
        this.isLongPress = true;
        callback(e.touches[0]);
        // 触觉反馈
        if (navigator.vibrate) navigator.vibrate(50);
      }, duration);
    }, { passive: true });

    el.addEventListener('touchmove', () => clearTimeout(this.timer), { passive: true });
    el.addEventListener('touchend', (e) => {
      clearTimeout(this.timer);
      // 如果是长按，阻止默认的 click 事件
      if (this.isLongPress) e.preventDefault();
    });

    // 防止长按后的 click 事件
    el.addEventListener('click', (e) => {
      if (this.isLongPress) {
        e.preventDefault();
        e.stopPropagation();
      }
    }, true);
  }
}

// 使用示例
document.querySelectorAll('.long-pressable').forEach(el => {
  new LongPress(el, (touch) => {
    showContextMenu(touch.clientX, touch.clientY);
  });
});
```

### 6.5 触觉反馈模式

```javascript
class HapticFeedback {
  static light() {
    // 轻触 — 适合按钮点击、开关切换
    if (navigator.vibrate) navigator.vibrate(10);
  }

  static medium() {
    // 中等 — 适合成功反馈、任务完成
    if (navigator.vibrate) navigator.vibrate([20, 50, 20]);
  }

  static heavy() {
    // 重触 — 适合错误提示、警告
    if (navigator.vibrate) navigator.vibrate([30, 30, 30, 30, 30]);
  }

  static pattern() {
    // 自定义节奏 — 适合引导步骤
    if (navigator.vibrate) navigator.vibrate([10, 50, 20, 50, 30]);
  }
}

// 结合交互使用
button.addEventListener('click', () => HapticFeedback.light());
toggle.addEventListener('change', (e) => {
  HapticFeedback[e.target.checked ? 'medium' : 'light']();
});
```

---

## 7. 声音设计

> 声音设计是 Awwwards 的**新兴趋势**。优秀的音频设计能让网站体验从"视觉"升维到"感官"。

### 核心原则

1. **用户主动选择**：声音必须默认关闭，由用户手动开启
2. **克制与精致**：声音应该是微妙的提示，不是干扰
3. **一致性**：所有交互的声音应属于同一"声音系统"
4. **性能优先**：使用 Web Audio API，避免加载大型音频文件

### 7.1 交互音效系统

```javascript
class SoundEngine {
  constructor() {
    this.ctx = null;      // AudioContext — 用户交互后创建
    this.enabled = false;  // 默认关闭
    this.volume = 0.3;
    this.masterGain = null;
  }

  // 用户点击"开启声音"按钮后调用
  init() {
    this.ctx = new (window.AudioContext || window.webkitAudioContext)();
    this.masterGain = this.ctx.createGain();
    this.masterGain.gain.value = this.volume;
    this.masterGain.connect(this.ctx.destination);
    this.enabled = true;
  }

  // 悬停音效 — 轻柔的"嘟"
  playHover() {
    if (!this.enabled) return;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(800, this.ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(600, this.ctx.currentTime + 0.1);

    gain.gain.setValueAtTime(0.1, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.1);

    osc.connect(gain);
    gain.connect(this.masterGain);

    osc.start(this.ctx.currentTime);
    osc.stop(this.ctx.currentTime + 0.1);
  }

  // 点击音效 — 清脆的"咔"
  playClick() {
    if (!this.enabled) return;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(1200, this.ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(400, this.ctx.currentTime + 0.15);

    gain.gain.setValueAtTime(0.2, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.15);

    osc.connect(gain);
    gain.connect(this.masterGain);

    osc.start(this.ctx.currentTime);
    osc.stop(this.ctx.currentTime + 0.15);
  }

  // 成功音效 — 上行的"叮"
  playSuccess() {
    if (!this.enabled) return;
    const notes = [523, 659, 784]; // C5, E5, G5 和弦
    notes.forEach((freq, i) => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = 'sine';
      osc.frequency.value = freq;

      const startTime = this.ctx.currentTime + i * 0.1;
      gain.gain.setValueAtTime(0, startTime);
      gain.gain.linearRampToValueAtTime(0.1, startTime + 0.05);
      gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.4);

      osc.connect(gain);
      gain.connect(this.masterGain);
      osc.start(startTime);
      osc.stop(startTime + 0.4);
    });
  }

  // 错误音效 — 低沉的"嗡"
  playError() {
    if (!this.enabled) return;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();

    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(150, this.ctx.currentTime);
    osc.frequency.linearRampToValueAtTime(100, this.ctx.currentTime + 0.3);

    gain.gain.setValueAtTime(0.1, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.3);

    // 添加低通滤波器使声音更柔和
    const filter = this.ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.value = 500;

    osc.connect(filter);
    filter.connect(gain);
    gain.connect(this.masterGain);

    osc.start(this.ctx.currentTime);
    osc.stop(this.ctx.currentTime + 0.3);
  }

  // 导航切换音效 — 柔和的"嗖"
  playTransition() {
    if (!this.enabled) return;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(200, this.ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(800, this.ctx.currentTime + 0.2);
    osc.frequency.exponentialRampToValueAtTime(400, this.ctx.currentTime + 0.4);

    gain.gain.setValueAtTime(0.08, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.4);

    osc.connect(gain);
    gain.connect(this.masterGain);

    osc.start(this.ctx.currentTime);
    osc.stop(this.ctx.currentTime + 0.4);
  }

  // 切换开关
  toggle() {
    this.enabled = !this.enabled;
    return this.enabled;
  }

  // 设置音量 (0~1)
  setVolume(vol) {
    this.volume = vol;
    if (this.masterGain) {
      this.masterGain.gain.value = vol;
    }
  }
}
```

### 7.2 环境音景

```javascript
class AmbientSoundscape {
  constructor() {
    this.ctx = null;
    this.isPlaying = false;
    this.nodes = [];
  }

  // 创建持续的、柔和的环境音
  async start() {
    this.ctx = new (window.AudioContext || window.webkitAudioContext)();
    this.masterGain = this.ctx.createGain();
    this.masterGain.gain.value = 0.05; // 非常轻柔
    this.masterGain.connect(this.ctx.destination);

    // 低频"嗡鸣" — 营造空间感
    const drone = this.ctx.createOscillator();
    drone.type = 'sine';
    drone.frequency.value = 80;
    const droneGain = this.ctx.createGain();
    droneGain.gain.value = 0.3;
    drone.connect(droneGain);
    droneGain.connect(this.masterGain);
    drone.start();

    // 随机"滴答"声 — 营造自然感
    this.startRandomDrops();

    this.isPlaying = true;
  }

  startRandomDrops() {
    const scheduleNext = () => {
      if (!this.isPlaying) return;
      // 随机间隔 2~6 秒
      const delay = 2000 + Math.random() * 4000;

      setTimeout(() => {
        this.playDrop();
        scheduleNext();
      }, delay);
    };
    scheduleNext();
  }

  playDrop() {
    if (!this.ctx) return;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();

    osc.type = 'sine';
    // 随机音高，在"悦耳"范围内
    const baseFreqs = [523, 587, 659, 784, 880, 1047]; // C5, D5, E5, G5, A5, C6
    osc.frequency.value = baseFreqs[Math.floor(Math.random() * baseFreqs.length)];

    gain.gain.setValueAtTime(0.15, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 1.5);

    // 高通滤波器去除低频
    const filter = this.ctx.createBiquadFilter();
    filter.type = 'highpass';
    filter.frequency.value = 400;

    osc.connect(filter);
    filter.connect(gain);
    gain.connect(this.masterGain);

    osc.start(this.ctx.currentTime);
    osc.stop(this.ctx.currentTime + 1.5);
  }

  stop() {
    this.isPlaying = false;
    if (this.ctx) this.ctx.close();
    this.ctx = null;
  }
}
```

### 7.3 音画编排

将声音与滚动位置或动画进度绑定：

```javascript
class AudioVisualSync {
  constructor(soundEngine) {
    this.sound = soundEngine;
    this.lastSection = null;
  }

  // 滚动时触发对应章节的声音
  onScroll(sections) {
    sections.forEach(section => {
      const rect = section.getBoundingClientRect();
      const isVisible = rect.top < window.innerHeight * 0.5
                     && rect.bottom > window.innerHeight * 0.5;

      if (isVisible && this.lastSection !== section.id) {
        this.lastSection = section.id;
        this.sound.playTransition();

        // 根据章节播放不同氛围音
        switch (section.dataset.mood) {
          case 'calm':
            this.playAmbientChord([261, 329, 392]); // C大三和弦
            break;
          case 'tense':
            this.playAmbientChord([293, 349, 415]); // D小三和弦
            break;
          case 'triumph':
            this.playAmbientChord([523, 659, 784]); // C大三和弦（高八度）
            break;
        }
      }
    });
  }

  playAmbientChord(frequencies) {
    frequencies.forEach(freq => {
      const osc = this.sound.ctx.createOscillator();
      const gain = this.sound.ctx.createGain();

      osc.type = 'sine';
      osc.frequency.value = freq;

      gain.gain.setValueAtTime(0, this.sound.ctx.currentTime);
      gain.gain.linearRampToValueAtTime(0.05, this.sound.ctx.currentTime + 0.5);
      gain.gain.linearRampToValueAtTime(0.001, this.sound.ctx.currentTime + 2);

      osc.connect(gain);
      gain.connect(this.sound.masterGain);

      osc.start(this.sound.ctx.currentTime);
      osc.stop(this.sound.ctx.currentTime + 2);
    });
  }
}
```

### 7.4 用户声音设置面板

```html
<div class="sound-toggle" aria-label="切换声音">
  <button id="sound-btn" class="sound-btn">
    <svg class="sound-on" width="20" height="20" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" stroke-width="2">
      <path d="M11 5L6 9H2v6h4l5 4V5z"/>
      <path d="M19.07 4.93a10 10 0 010 14.14M15.54 8.46a5 5 0 010 7.07"/>
    </svg>
    <svg class="sound-off" width="20" height="20" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" stroke-width="2" style="display:none">
      <path d="M11 5L6 9H2v6h4l5 4V5z"/>
      <line x1="23" y1="9" x2="17" y2="15"/>
      <line x1="17" y1="9" x2="23" y2="15"/>
    </svg>
  </button>
  <input type="range" id="sound-volume" min="0" max="100" value="30"
         class="sound-slider" aria-label="音量">
</div>
```

```javascript
// 声音面板交互
const soundEngine = new SoundEngine();
const soundBtn = document.getElementById('sound-btn');
const volumeSlider = document.getElementById('sound-volume');

soundBtn.addEventListener('click', () => {
  const isOn = soundEngine.toggle();

  if (isOn && !soundEngine.ctx) {
    soundEngine.init();
  }

  soundBtn.querySelector('.sound-on').style.display = isOn ? '' : 'none';
  soundBtn.querySelector('.sound-off').style.display = isOn ? 'none' : '';
});

volumeSlider.addEventListener('input', (e) => {
  soundEngine.setVolume(e.target.value / 100);
});

// 为可交互元素绑定声音
document.querySelectorAll('.sound-hover').forEach(el => {
  el.addEventListener('mouseenter', () => soundEngine.playHover());
});

document.querySelectorAll('.sound-click').forEach(el => {
  el.addEventListener('click', () => soundEngine.playClick());
});
```

---

## 附录：性能优化清单

在实现以上所有交互时，务必遵循以下性能准则：

| 原则 | 说明 |
|------|------|
| **`will-change`** | 仅在动画即将开始前设置，动画结束后移除 |
| **`transform` 优先** | 永远用 `transform` / `opacity` 做动画，避免触发 layout/paint |
| **`requestAnimationFrame`** | 所有连续动画（光标跟随、滚动效果）必须使用 rAF |
| **事件节流** | `scroll`、`mousemove`、`touchmove` 事件必须节流或使用 passive listener |
| **IntersectionObserver** | 优先使用 IO 替代 scroll 计算来判断元素可见性 |
| **GPU 合成层** | 为频繁动画的元素创建独立合成层（`transform: translateZ(0)`） |
| **移动端检测** | 触屏设备跳过自定义光标、减少粒子数量、关闭复杂 CSS 效果 |
| **`prefers-reduced-motion`** | 尊重用户的减少动画偏好 |

```css
/* 尊重用户偏好：减少动画 */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }

  .cursor-dot, .cursor-ring { display: none !important; }
  * { cursor: auto !important; }
}
```

```javascript
// JS 中检测用户偏好
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (prefersReducedMotion) {
  // 禁用自定义光标
  // 禁用粒子效果
  // 禁用滚动视差
  // 禁用声音
  console.log('用户偏好减少动画，已跳过复杂交互。');
}
```

---

## 附录：Easing 曲线速查

Awwwards 获奖网站最常用的缓动函数：

```css
/* 通用入场 — 柔和弹跳 */
--ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);

/* 通用出场 — 柔和减速 */
--ease-in-out-circ: cubic-bezier(0.85, 0, 0.15, 1);

/* 弹性效果 — 用于按钮、开关 */
--ease-out-back: cubic-bezier(0.34, 1.56, 0.64, 1);

/* 极速停止 — 用于光标跟随 */
--ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);

/* 超慢启动 — 用于全屏导航展开 */
--ease-in-out-quint: cubic-bezier(0.83, 0, 0.17, 1);

/* 材质感 — 用于拖拽松手回弹 */
--ease-out-cubic: cubic-bezier(0.33, 1, 0.68, 1);
```

---

> **最终建议**：不要试图在一个项目中使用所有模式。选择 2-3 个与你的品牌调性最匹配的模式，将它们打磨到极致。一个完美执行的自定义光标 + 一个精心设计的页面转场，远胜于十个半成品的交互效果。
