/**
 * custom-cursor.js
 * 
 * 自定义光标系统 — Awwwards 获奖网站标配交互模式
 * 来源: references/interaction-patterns.md §1
 * 
 * 功能:
 *   - CustomCursor 类：双元素架构（dot + ring），lerp 延迟跟随
 *   - bindHoverEvents()：data-cursor="expand" / "pointer" / "view" 悬停处理
 *   - initCursorText()：光标文字跟随（data-cursor-text）
 *   - setupTouchFeedback()：移动端触摸涟漪降级
 *   - 自动检测移动设备，仅在桌面端初始化
 * 
 * 依赖: 无外部依赖（纯 Vanilla JS）
 * 
 * HTML 要求:
 *   <div class="cursor-dot"></div>
 *   <div class="cursor-ring"></div>
 *   <style>* { cursor: none !important; }</style>
 */

class CustomCursor {
  constructor(options = {}) {
    this.lerpFactor = options.lerpFactor || 0.12;
    this.dotSize = options.dotSize || 8;
    this.ringSize = options.ringSize || 40;
    this.isMobile =
      'ontouchstart' in window ||
      navigator.maxTouchPoints > 0 ||
      window.matchMedia('(max-width: 768px)').matches;

    if (this.isMobile) {
      this._injectTouchRippleStyle();
      this.setupTouchFeedback();
      return;
    }

    this.dot = document.querySelector('.cursor-dot');
    this.ring = document.querySelector('.cursor-ring');

    if (!this.dot || !this.ring) {
      console.warn('[CustomCursor] .cursor-dot / .cursor-ring 元素未找到');
      return;
    }

    // 光标实际位置（用于 dot — 即时跟随）
    this.pos = { x: 0, y: 0 };
    // 跟随器目标位置（用于 ring — 延迟跟随）
    this.ringPos = { x: 0, y: 0 };

    this.init();
    this.bindHoverEvents();
    this.initCursorText();
  }

  /**
   * 初始化鼠标移动监听和动画循环
   */
  init() {
    document.addEventListener('mousemove', (e) => {
      this.pos.x = e.clientX;
      this.pos.y = e.clientY;
      this.dot.style.left = `${e.clientX}px`;
      this.dot.style.top = `${e.clientY}px`;
    });

    this._animate();
  }

  /**
   * 使用 requestAnimationFrame + lerp 让 ring 平滑跟随
   */
  _animate() {
    const lerp = (start, end, factor) => start + (end - start) * factor;

    this.ringPos.x = lerp(this.ringPos.x, this.pos.x, this.lerpFactor);
    this.ringPos.y = lerp(this.ringPos.y, this.pos.y, this.lerpFactor);

    this.ring.style.left = `${this.ringPos.x}px`;
    this.ring.style.top = `${this.ringPos.y}px`;

    // 如果有光标文字，也跟随 ring
    if (this.cursorText && this.cursorText.style.opacity === '1') {
      this.cursorText.style.left = `${this.ringPos.x}px`;
      this.cursorText.style.top = `${this.ringPos.y}px`;
    }

    requestAnimationFrame(() => this._animate());
  }

  /**
   * 绑定 data-cursor 悬停事件
   * - "expand"：环形放大（表示可点击链接）
   * - "pointer"：变为竖线（表示按钮/输入框）
   * - "view"：中间出现眼睛图标（表示查看/预览）
   */
  bindHoverEvents() {
    // [data-cursor="expand"] — 环形放大
    const expanders = document.querySelectorAll('[data-cursor="expand"]');
    expanders.forEach((el) => {
      el.addEventListener('mouseenter', () => {
        this.ring.style.width = '64px';
        this.ring.style.height = '64px';
        this.ring.style.borderColor = 'rgba(0,0,0,0.2)';
        this.dot.style.transform = 'translate(-50%,-50%) scale(0.5)';
      });
      el.addEventListener('mouseleave', () => {
        this.ring.style.width = `${this.ringSize}px`;
        this.ring.style.height = `${this.ringSize}px`;
        this.ring.style.borderColor = 'rgba(0,0,0,0.5)';
        this.dot.style.transform = 'translate(-50%,-50%) scale(1)';
      });
    });

    // [data-cursor="pointer"] — 变为竖线
    const pointers = document.querySelectorAll('[data-cursor="pointer"]');
    pointers.forEach((el) => {
      el.addEventListener('mouseenter', () => {
        this.dot.style.width = '3px';
        this.dot.style.height = '28px';
        this.dot.style.borderRadius = '2px';
        this.ring.style.opacity = '0';
      });
      el.addEventListener('mouseleave', () => {
        this.dot.style.width = `${this.dotSize}px`;
        this.dot.style.height = `${this.dotSize}px`;
        this.dot.style.borderRadius = '50%';
        this.ring.style.opacity = '1';
      });
    });

    // [data-cursor="view"] — 中间出现眼睛图标
    const viewers = document.querySelectorAll('[data-cursor="view"]');
    viewers.forEach((el) => {
      el.addEventListener('mouseenter', () => {
        this.ring.style.width = '72px';
        this.ring.style.height = '72px';
        this.ring.style.background = 'rgba(0,0,0,0.06)';
        this.dot.innerHTML =
          '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>';
      });
      el.addEventListener('mouseleave', () => {
        this.ring.style.width = `${this.ringSize}px`;
        this.ring.style.height = `${this.ringSize}px`;
        this.ring.style.background = 'transparent';
        this.dot.innerHTML = '';
      });
    });
  }

  /**
   * 初始化光标文字（data-cursor-text）
   * 悬停时在光标位置显示自定义文字
   */
  initCursorText() {
    const textElements = document.querySelectorAll('[data-cursor-text]');
    if (textElements.length === 0) return;

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

    textElements.forEach((el) => {
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
        this.ring.style.width = `${this.ringSize}px`;
        this.ring.style.height = `${this.ringSize}px`;
      });
    });
  }

  /**
   * 移动端降级：触摸涟漪反馈
   */
  setupTouchFeedback() {
    document.addEventListener(
      'touchstart',
      (e) => {
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
      },
      { passive: true }
    );
  }

  /**
   * 注入 touchRipple 关键帧动画
   */
  _injectTouchRippleStyle() {
    if (document.getElementById('touch-ripple-style')) return;
    const style = document.createElement('style');
    style.id = 'touch-ripple-style';
    style.textContent = `
      @keyframes touchRipple {
        to { transform: translate(-50%, -50%) scale(6); opacity: 0; }
      }
    `;
    document.head.appendChild(style);
  }

  /**
   * 销毁光标实例，移除事件监听
   */
  destroy() {
    this.dot?.remove();
    this.ring?.remove();
    this.cursorText?.remove();
  }
}

// ─── 使用示例 ───
// 确保页面中有 <div class="cursor-dot"></div> 和 <div class="cursor-ring"></div>
// new CustomCursor();
