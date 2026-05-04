/**
 * magnetic-button.js
 * 
 * 磁性按钮效果 — Awwwards 获奖网站高频交互模式
 * 来源: references/interaction-patterns.md §1.3 + references/animation-patterns.md §4
 * 
 * 提供两种实现:
 *   1. MagneticElement 类 — 纯 Vanilla JS，无依赖
 *   2. magneticButtons()   — GSAP 版本，带弹性回弹和内部元素额外偏移
 * 
 * HTML 用法:
 *   Vanilla: <button class="magnetic">Click</button>
 *   GSAP:    <button data-magnetic="0.3"><span data-magnetic-inner>探索更多</span></button>
 * 
 * 依赖:
 *   MagneticElement — 无外部依赖
 *   magneticButtons — 需要 GSAP (gsap)
 */

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 方案 1：MagneticElement 类（纯 Vanilla JS）
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/**
 * MagneticElement — 磁性吸附元素
 * 鼠标悬停时，元素向光标方向"吸附"偏移；离开时弹性回弹归位。
 *
 * @param {HTMLElement} el       - 目标 DOM 元素
 * @param {number}      strength - 吸附强度（0.1 ~ 0.5，默认 0.35）
 *
 * @example
 *   document.querySelectorAll('.magnetic').forEach(el => new MagneticElement(el));
 *   document.querySelectorAll('.magnetic-strong').forEach(el => new MagneticElement(el, 0.5));
 */
class MagneticElement {
  constructor(el, strength = 0.35) {
    this.el = el;
    this.strength = strength;
    this.bounding = el.getBoundingClientRect();

    this._onMouseMove = (e) => {
      const dx = e.clientX - (this.bounding.left + this.bounding.width / 2);
      const dy = e.clientY - (this.bounding.top + this.bounding.height / 2);
      this.el.style.transform = `translate(${dx * this.strength}px, ${dy * this.strength}px)`;
    };

    this._onMouseLeave = () => {
      this.el.style.transition = 'transform 0.5s cubic-bezier(0.23, 1, 0.32, 1)';
      this.el.style.transform = 'translate(0, 0)';
      // transition 结束后清除，避免干扰 hover scale
      setTimeout(() => {
        this.el.style.transition = '';
      }, 500);
    };

    this._onResize = () => {
      this.bounding = el.getBoundingClientRect();
    };

    el.addEventListener('mousemove', this._onMouseMove);
    el.addEventListener('mouseleave', this._onMouseLeave);
    window.addEventListener('resize', this._onResize);
  }

  /**
   * 销毁实例，移除所有事件监听
   */
  destroy() {
    this.el.removeEventListener('mousemove', this._onMouseMove);
    this.el.removeEventListener('mouseleave', this._onMouseLeave);
    window.removeEventListener('resize', this._onResize);
  }
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 方案 2：magneticButtons（GSAP 版本）
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/**
 * 初始化所有磁性按钮（GSAP 版本）
 * 支持内部元素（[data-magnetic-inner]）额外偏移，产生更强烈的磁性效果。
 * 离开时使用 elastic.out 弹性缓动回弹。
 *
 * HTML:
 *   <button data-magnetic="0.3">
 *     <span data-magnetic-inner>探索更多</span>
 *   </button>
 */
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

// ─── 使用示例 ───
//
// Vanilla JS 方案（无 GSAP 依赖）:
// document.querySelectorAll('.magnetic').forEach(el => new MagneticElement(el));
//
// GSAP 方案（带弹性回弹和内部偏移）:
// magneticButtons();
