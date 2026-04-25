# GSAP 高级动画配方

## 配方1：页面加载 Intro 动画

```javascript
// 专业级页面加载序列
function playIntro() {
  const tl = gsap.timeline();
  
  // 1. 加载遮罩
  tl.to('.loader-bar', {
    scaleX: 1,
    duration: 1.2,
    ease: 'expo.inOut',
    transformOrigin: 'left center',
  })
  // 2. 显示进度数字
  .to('.loader-num', { innerHTML: 100, duration: 1.2, snap: { innerHTML: 1 } }, '<')
  // 3. 遮罩退场
  .to('.loader', { 
    yPercent: -100, 
    duration: 0.9, 
    ease: 'expo.inOut',
    delay: 0.2
  })
  // 4. Hero 内容入场
  .from('.hero-title .word-inner', {
    yPercent: 110,
    duration: 1.1,
    ease: 'expo.out',
    stagger: 0.05,
  }, '-=0.4')
  .from('.hero-sub', { opacity: 0, y: 20, duration: 0.8, ease: 'expo.out' }, '-=0.6')
  .from('.hero-cta', { opacity: 0, y: 15, duration: 0.6 }, '-=0.4');
  
  return tl;
}
```

## 配方2：磁性按钮（Magnetic Button）

```javascript
// 鼠标靠近时按钮被「吸引」
function magneticButton(el) {
  const strength = 0.3;
  
  el.addEventListener('mousemove', e => {
    const rect = el.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    const dx = e.clientX - cx;
    const dy = e.clientY - cy;
    
    gsap.to(el, {
      x: dx * strength,
      y: dy * strength,
      duration: 0.4,
      ease: 'power2.out',
    });
  });
  
  el.addEventListener('mouseleave', () => {
    gsap.to(el, { x: 0, y: 0, duration: 0.7, ease: 'elastic.out(1, 0.3)' });
  });
}
```

## 配方3：文字逐行揭示

```javascript
// 每行文字从下方滑入（遮罩效果）
function setupTextReveals() {
  // CSS 需要：.line { overflow: hidden; }
  gsap.utils.toArray('.reveal-text').forEach(el => {
    const lines = el.querySelectorAll('.line');
    
    gsap.from(lines, {
      yPercent: 100,
      duration: 0.9,
      ease: 'expo.out',
      stagger: 0.08,
      scrollTrigger: {
        trigger: el,
        start: 'top 80%',
        toggleActions: 'play none none reset',
      }
    });
  });
}
```

## 配方4：横向滚动画廊

```javascript
function horizontalScroll(containerEl) {
  const sections = containerEl.querySelectorAll('.h-section');
  
  gsap.to(sections, {
    xPercent: -100 * (sections.length - 1),
    ease: 'none',
    scrollTrigger: {
      trigger: containerEl,
      pin: true,
      scrub: 1,
      snap: 1 / (sections.length - 1),
      end: () => `+=${containerEl.offsetWidth}`,
    },
  });
}
```

## 配方5：视差深度层次

```javascript
// 多层速度不同的视差
function setupParallax() {
  // 快速层（前景）
  gsap.to('.parallax-fast', {
    yPercent: -30,
    ease: 'none',
    scrollTrigger: { scrub: true }
  });
  
  // 慢速层（背景）
  gsap.to('.parallax-slow', {
    yPercent: -10,
    ease: 'none',
    scrollTrigger: { scrub: true }
  });
  
  // 反向层（向下移动，增加深度感）
  gsap.to('.parallax-reverse', {
    yPercent: 20,
    ease: 'none',
    scrollTrigger: { scrub: true }
  });
}
```

## 配方6：数字计数动画

```javascript
// 数字滚动增加到目标值
function animateCounter(el, target, suffix = '') {
  const obj = { val: 0 };
  gsap.to(obj, {
    val: target,
    duration: 2,
    ease: 'power2.out',
    snap: { val: 1 },
    onUpdate: () => {
      el.textContent = obj.val.toLocaleString() + suffix;
    },
    scrollTrigger: {
      trigger: el,
      start: 'top 80%',
      once: true,
    }
  });
}
```

## 配方7：图片遮罩揭示

```javascript
// 图片从左到右或从下到上揭示，带遮罩效果
function imageReveal(container) {
  const img = container.querySelector('img');
  const overlay = container.querySelector('.img-overlay');
  
  const tl = gsap.timeline({
    scrollTrigger: {
      trigger: container,
      start: 'top 75%',
    }
  });
  
  tl.to(overlay, {
    scaleX: 0,
    transformOrigin: 'right center',
    duration: 0.9,
    ease: 'expo.inOut',
  })
  .from(img, {
    scale: 1.2,
    duration: 0.9,
    ease: 'expo.out',
  }, '<');
}
```

## ScrollTrigger 调试技巧

```javascript
// 开发时显示标记
ScrollTrigger.defaults({
  markers: process.env.NODE_ENV === 'development',
});

// 刷新（添加动态内容后调用）
ScrollTrigger.refresh();

// 页面离开时清理
window.addEventListener('beforeunload', () => {
  ScrollTrigger.getAll().forEach(t => t.kill());
});
```
