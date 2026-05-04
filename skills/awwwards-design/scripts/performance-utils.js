/**
 * performance-utils.js
 * 
 * 性能工具函数集 — Awwwards 级网站性能优化基础设施
 * 来源: references/performance-guide.md + references/animation-patterns.md §7
 * 
 * 功能:
 *   - debounce(fn, delay)        — 防抖（停止触发后延迟执行）
 *   - cancelDebounce(fn)        — 取消防抖
 *   - throttle(fn)               — rAF 节流（对齐帧率，无外部依赖）
 *   - throttle(fn, interval)     — 时间间隔节流（setTimeout 版本）
 *   - LazyWebGL 类               — IntersectionObserver 延迟初始化 WebGL 场景
 *   - disposeScene(scene, renderer) — Three.js 资源完整释放
 *   - observeAnimations(options)  — IntersectionObserver 触发入场动画
 * 
 * 依赖:
 *   LazyWebGL / disposeScene — 可选 Three.js（动态 import）
 *   其他函数 — 无外部依赖
 */

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 防抖 / 节流
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/**
 * 防抖（Debounce）：在最后一次调用后等待 delay 毫秒再执行
 * 适用场景：搜索输入、resize 事件
 *
 * @param {Function} fn    - 要延迟执行的函数
 * @param {number}   delay - 延迟毫秒数（默认 150ms）
 * @returns {Function} 包装后的防抖函数（附 .cancel() 方法）
 */
export function debounce(fn, delay = 150) {
  let timer;
  const debounced = (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };

  /**
   * 取消防抖，立即清除待执行的定时器
   */
  debounced.cancel = () => {
    clearTimeout(timer);
  };

  return debounced;
}

/**
 * 取消防抖的快捷方式
 * 用法: const handleResize = debounce(fn, 200);
 *        cancelDebounce(handleResize);
 *
 * @param {Function} debouncedFn - debounce() 返回的函数
 */
export function cancelDebounce(debouncedFn) {
  if (debouncedFn && typeof debouncedFn.cancel === 'function') {
    debouncedFn.cancel();
  }
}

/**
 * rAF 节流（Throttle）：使用 requestAnimationFrame 对齐帧率
 * 适用场景：鼠标跟随、滚动驱动动画
 * 无需指定间隔，自动对齐到 ~60fps
 *
 * @param {Function} fn - 每帧执行的函数
 * @returns {Function} 节流后的函数
 */
export function throttleRAF(fn) {
  let busy = false;
  return (...args) => {
    if (busy) return;
    busy = true;
    requestAnimationFrame(() => {
      fn(...args);
      busy = false;
    });
  };
}

/**
 * 时间间隔节流（Throttle）：保证在指定间隔内最多执行一次
 * 适用场景：需要精确控制调用频率的场景
 *
 * @param {Function} fn       - 要节流的函数
 * @param {number}   interval - 间隔毫秒数（默认 16ms ≈ 60fps）
 * @returns {Function} 节流后的函数
 */
export function throttle(fn, interval = 16) {
  let lastTime = 0;
  return (...args) => {
    const now = Date.now();
    if (now - lastTime >= interval) {
      lastTime = now;
      fn(...args);
    }
  };
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// WebGL 性能优化
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/**
 * LazyWebGL — 延迟初始化 WebGL 场景
 * 使用 IntersectionObserver 在容器进入视口时才初始化 Three.js，
 * 离开视口时暂停渲染循环，节省 GPU 资源。
 *
 * @param {HTMLElement} container - WebGL 画布的父容器
 *
 * @example
 *   const lazyGL = new LazyWebGL(document.getElementById('webgl-container'));
 */
export class LazyWebGL {
  constructor(container) {
    this.container = container;
    this.initialized = false;
    this.isPaused = false;

    this.observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !this.initialized) {
            this.init();
            this.observer.disconnect();
          } else if (!entry.isIntersecting && this.initialized) {
            this.pause();
          }
        });
      },
      { threshold: 0 }
    );

    this.observer.observe(container);
  }

  /**
   * 初始化 WebGL 场景（动态导入 Three.js）
   * 子类可重写此方法自定义场景
   */
  async init() {
    this.initialized = true;

    // 动态导入 Three.js，避免首屏加载
    if (typeof THREE === 'undefined') {
      try {
        const THREE = await import('three');
        this.THREE = THREE;
      } catch (e) {
        console.warn('[LazyWebGL] Three.js 未安装或无法加载');
        return;
      }
    } else {
      this.THREE = THREE;
    }

    // 子类在此处初始化场景、相机、渲染器...
    this.animate();
  }

  /**
   * 暂停渲染循环（离开视口时调用）
   */
  pause() {
    this.isPaused = true;
  }

  /**
   * 恢复渲染循环（重新进入视口时调用）
   */
  resume() {
    if (this.isPaused) {
      this.isPaused = false;
      this.animate();
    }
  }

  /**
   * 渲染循环（子类重写以实现自定义渲染逻辑）
   */
  animate() {
    if (this.isPaused) return;
    requestAnimationFrame(() => this.animate());
    // 子类在此处更新 & 渲染
  }

  /**
   * 销毁实例
   */
  destroy() {
    this.observer.disconnect();
    this.isPaused = true;
  }
}

/**
 * Three.js 资源完整释放
 * 遍历场景中所有对象，释放 geometry、material、texture 和 WebGL 上下文。
 *
 * @param {THREE.Scene}     scene     - Three.js 场景对象
 * @param {THREE.WebGLRenderer} renderer - Three.js 渲染器
 *
 * @example
 *   disposeScene(scene, renderer);
 */
export function disposeScene(scene, renderer) {
  // 遍历场景中所有对象
  scene.traverse((object) => {
    // 释放几何体
    if (object.geometry) {
      object.geometry.dispose();
    }

    // 释放材质和纹理
    if (object.material) {
      // 材质可能包含多个材质
      const materials = Array.isArray(object.material)
        ? object.material
        : [object.material];

      materials.forEach((material) => {
        // 释放纹理
        Object.values(material)
          .filter((value) => value && value.isTexture)
          .forEach((texture) => texture.dispose());

        material.dispose();
      });
    }
  });

  // 释放渲染器
  if (renderer) {
    renderer.dispose();
    renderer.forceContextLoss();
    renderer.domElement = null;
  }
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// IntersectionObserver 动画触发
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/**
 * observeAnimations — 轻量级 ScrollTrigger 替代方案
 * 使用 IntersectionObserver 检测 [data-animate] 元素进入视口时添加 .is-visible 类。
 *
 * @param {Object}   [options]                    - 配置项
 * @param {string}   [options.selector]           - 选择器（默认 '[data-animate]'）
 * @param {string}   [options.visibleClass]       - 可见时的类名（默认 'is-visible'）
 * @param {number}   [options.threshold]          - 触发阈值 0~1（默认 0.15）
 * @param {string}   [options.rootMargin]         - 触发偏移量（默认 '0px 0px -50px 0px'）
 * @param {boolean}  [options.once=true]          - 是否只触发一次
 * @param {Function} [options.onEnter]            - 进入视口时的回调
 * @param {Function} [options.onLeave]            - 离开视口时的回调
 * @returns {IntersectionObserver} observer 实例（可用于手动 disconnect）
 *
 * @example
 *   // 基础用法（配合 CSS transition）
 *   observeAnimations();
 *
 *   // 自定义配置
 *   observeAnimations({
 *     selector: '.fade-up',
 *     threshold: 0.3,
 *     rootMargin: '0px 0px -100px 0px',
 *     onEnter: (el) => {
 *       el.style.opacity = '1';
 *       el.style.transform = 'translateY(0)';
 *     }
 *   });
 *
 * CSS 配合:
 *   [data-animate] { opacity: 0; transform: translateY(30px); transition: 0.6s ease-out; }
 *   [data-animate].is-visible { opacity: 1; transform: translateY(0); }
 */
export function observeAnimations(options = {}) {
  const {
    selector = '[data-animate]',
    visibleClass = 'is-visible',
    threshold = 0.15,
    rootMargin = '0px 0px -50px 0px',
    once = true,
    onEnter,
    onLeave,
  } = options;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add(visibleClass);
          if (typeof onEnter === 'function') {
            onEnter(entry.target);
          }
          if (once) {
            observer.unobserve(entry.target);
          }
        } else {
          if (once) return;
          entry.target.classList.remove(visibleClass);
          if (typeof onLeave === 'function') {
            onLeave(entry.target);
          }
        }
      });
    },
    {
      threshold,
      rootMargin,
    }
  );

  document.querySelectorAll(selector).forEach((el) => {
    observer.observe(el);
  });

  return observer;
}

// ─── 使用示例 ───
//
// // 防抖 resize
// window.addEventListener('resize', debounce(() => {
//   recalculateLayout();
// }, 250));
//
// // rAF 节流鼠标跟随
// window.addEventListener('mousemove', throttleRAF((e) => {
//   cursor.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
// }));
//
// // 延迟初始化 WebGL
// new LazyWebGL(document.getElementById('webgl-container'));
//
// // 释放 Three.js 资源
// disposeScene(scene, renderer);
//
// // 滚动入场动画
// observeAnimations();
