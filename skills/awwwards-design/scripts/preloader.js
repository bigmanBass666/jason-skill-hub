/**
 * preloader.js
 * 
 * 页面入场 / 预加载动画集 — Awwwards 542+ 收藏条目
 * 来源: references/animation-patterns.md §2
 * 
 * 功能:
 *   - createPreloader()    — 计数器预加载器（0 → 100%，含 clipPath 分离动画）
 *   - brandReveal()        — 品牌遮罩揭示（clipPath 滑入滑出）
 *   - multiStepIntro()     — 多步骤入场序列（导航→标题→副标题→装饰线→滚动提示）
 *   - splitTextToChars()   — 文字拆分工具（将文本拆分为独立 <span class="char">）
 * 
 * 依赖: GSAP (gsap)
 * 
 * HTML 要求（createPreloader）:
 *   <div class="preloader" id="preloader">
 *     <div class="preloader__counter">
 *       <span class="preloader__number" id="counter">0</span>
 *       <span class="preloader__percent">%</span>
 *     </div>
 *     <div class="preloader__progress">
 *       <div class="preloader__bar" id="progress-bar"></div>
 *     </div>
 *   </div>
 */

/**
 * 计数器预加载器
 * 数字从 0 计数到 100，随后数字放大淡出，预加载面板上下分离消失。
 * 完成后调用 lenis.start() 和 initPageAnimations()。
 *
 * @returns {gsap.core.Timeline} GSAP timeline 实例
 */
function createPreloader() {
  const preloader = document.getElementById('preloader');
  const counter = document.getElementById('counter');
  const bar = document.getElementById('progress-bar');

  if (!preloader || !counter) {
    console.warn('[createPreloader] 预加载器 DOM 元素未找到');
    return null;
  }

  const tl = gsap.timeline({
    onComplete: () => {
      // 预加载结束，启动平滑滚动和页面动画
      if (typeof lenis !== 'undefined' && lenis.start) {
        lenis.start();
      }
      if (typeof initPageAnimations === 'function') {
        initPageAnimations();
      }
    },
  });

  // 阶段 1：计数器从 0 到 100
  const counterObj = { value: 0 };
  tl.to(counterObj, {
    value: 100,
    duration: 2.5,
    ease: 'power2.inOut',
    onUpdate: () => {
      counter.textContent = Math.floor(counterObj.value);
      if (bar) {
        bar.style.width = counterObj.value + '%';
      }
    },
  });

  // 阶段 2：数字放大淡出
  tl.to(
    counter,
    {
      scale: 1.5,
      opacity: 0,
      duration: 0.6,
      ease: 'power3.in',
    },
    '-=0.3'
  );

  if (bar) {
    tl.to(
      bar,
      {
        opacity: 0,
        duration: 0.4,
      },
      '-=0.5'
    );
  }

  // 阶段 3：预加载面板上下分离
  tl.to('.preloader', {
    clipPath: 'inset(50% 0 50% 0)',
    duration: 0.8,
    ease: 'power4.inOut',
  });

  tl.set(preloader, { display: 'none' });

  return tl;
}

/**
 * 品牌遮罩揭示（Mask Reveal）
 * 品牌文字从右向左滑入揭示，然后从左向右滑出，同时背景跟随消失。
 *
 * HTML 要求:
 *   <div class="brand-reveal">
 *     <div class="brand-reveal__text">BRAND</div>
 *   </div>
 *
 * CSS 要求:
 *   .brand-reveal { position: fixed; inset: 0; z-index: 9998; background: #fff;
 *                   display: flex; align-items: center; justify-content: center; }
 *   .brand-reveal__text { font-size: clamp(3rem, 10vw, 8rem); font-weight: 900;
 *                          clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%); }
 *
 * @returns {gsap.core.Timeline} GSAP timeline 实例
 */
function brandReveal() {
  const tl = gsap.timeline();

  // 品牌文字从右向左滑入揭示
  tl.from('.brand-reveal__text', {
    clipPath: 'polygon(100% 0, 100% 0, 100% 100%, 100% 100%)',
    duration: 1,
    ease: 'power4.inOut',
  });

  // 文字从左向右滑出
  tl.to(
    '.brand-reveal__text',
    {
      clipPath: 'polygon(0 0, 0 0, 0 100%, 0 100%)',
      duration: 1,
      ease: 'power4.inOut',
    },
    '+=0.3'
  );

  // 背景跟随文字消失
  tl.to(
    '.brand-reveal',
    {
      clipPath: 'polygon(0 0, 0 0, 0 100%, 0 100%)',
      duration: 1,
      ease: 'power4.inOut',
    },
    '-=0.7'
  );

  return tl;
}

/**
 * 多步骤入场序列（Multi-step Intro）
 * 按顺序执行：导航栏滑入 → 标题逐字显现 → 副标题滑入 → 装饰线展开 → 滚动提示淡入
 * 期间禁止滚动，完成后恢复。
 *
 * HTML 要求:
 *   .nav, .hero-title .char, .hero-subtitle, .hero-line, .scroll-indicator
 *   使用前需先调用 splitTextToChars('.hero-title') 拆分文字
 *
 * @returns {gsap.core.Timeline} GSAP timeline 实例
 */
function multiStepIntro() {
  const tl = gsap.timeline({
    defaults: { ease: 'power3.out' },
  });

  // 在此期间禁止滚动
  if (typeof lenis !== 'undefined' && lenis.stop) {
    lenis.stop();
  }

  // 步骤 1：导航栏从上方滑入
  tl.from('.nav', {
    y: -100,
    opacity: 0,
    duration: 0.8,
  });

  // 步骤 2：标题逐字显现
  tl.from(
    '.hero-title .char',
    {
      y: 120,
      rotateX: -80,
      opacity: 0,
      stagger: 0.03,
      duration: 0.8,
    },
    '-=0.3'
  );

  // 步骤 3：副标题从下方滑入
  tl.from(
    '.hero-subtitle',
    {
      y: 40,
      opacity: 0,
      duration: 0.6,
    },
    '-=0.2'
  );

  // 步骤 4：装饰线条横向展开
  tl.from(
    '.hero-line',
    {
      scaleX: 0,
      transformOrigin: 'left center',
      duration: 0.8,
    },
    '-=0.4'
  );

  // 步骤 5：滚动提示淡入
  tl.from(
    '.scroll-indicator',
    {
      opacity: 0,
      y: 20,
      duration: 0.5,
    },
    '-=0.2'
  );

  // 最后恢复滚动
  tl.call(() => {
    if (typeof lenis !== 'undefined' && lenis.start) {
      lenis.start();
    }
  });

  return tl;
}

/**
 * 文字拆分工具函数
 * 将文本拆分为独立字符，每个字符包裹在 <span class="char"> 中。
 * 支持 GSAP stagger 动画。
 *
 * @param {string} selector - CSS 选择器，匹配需要拆分的文本元素
 *
 * @example
 *   splitTextToChars('.hero-title');
 *   // 之后 GSAP 可以动画 .char 元素：
 *   // gsap.from('.hero-title .char', { y: 100, opacity: 0, stagger: 0.03 });
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

// ─── 使用示例 ───
// // 先拆分文字
// splitTextToChars('.hero-title');
//
// // 然后启动预加载器
// createPreloader();
//
// // 或使用品牌揭示
// brandReveal();
//
// // 或使用多步骤入场
// multiStepIntro();
