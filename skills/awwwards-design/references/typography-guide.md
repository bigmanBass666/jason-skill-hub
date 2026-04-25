# 排版系统指南

## 字体比例系统

```css
/* 基于黄金比例的字体层级 */
:root {
  --text-xs:   clamp(0.7rem,  1vw,  0.85rem);
  --text-sm:   clamp(0.85rem, 1.2vw, 1rem);
  --text-base: clamp(1rem,    1.5vw, 1.2rem);
  --text-lg:   clamp(1.2rem,  2vw,   1.5rem);
  --text-xl:   clamp(1.5rem,  3vw,   2rem);
  --text-2xl:  clamp(2rem,    5vw,   4rem);
  --text-3xl:  clamp(3rem,    8vw,   7rem);
  --text-hero: clamp(4rem,    12vw,  12rem); /* Hero 超大字 */
}
```

## 字体配对系统

### 配对1：现代对比（最稳健）
```css
@import url('https://api.fontshare.com/v2/css?f[]=clash-display@700,600&display=swap');
@import url('https://api.fontshare.com/v2/css?f[]=satoshi@400,500&display=swap');

.display { font-family: 'Clash Display', sans-serif; font-weight: 700; }
.body    { font-family: 'Satoshi', sans-serif; font-weight: 400; }
```

### 配对2：档案式严肃
```css
/* Druk Wide Bold + Courier New */
.display { font-family: 'Druk Wide', 'Impact', sans-serif; font-weight: 700; letter-spacing: -0.02em; }
.body    { font-family: 'Courier New', monospace; font-size: 0.9em; }
```

### 配对3：有机温暖
```css
@import url('https://api.fontshare.com/v2/css?f[]=cabinet-grotesk@800&display=swap');
.display { font-family: 'Cabinet Grotesk', sans-serif; font-weight: 800; }
.body    { font-family: 'Georgia', serif; }
```

### 配对4：极简科技
```css
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&display=swap');
.display { font-family: 'Space Grotesk', sans-serif; font-weight: 700; }
.mono    { font-family: 'Space Mono', monospace; }
```

## 排版效果 CSS

```css
/* 超大标题标准设置 */
.hero-title {
  font-size: var(--text-hero);
  font-weight: 700;
  line-height: 0.88;          /* 比1小，有紧实感 */
  letter-spacing: -0.04em;    /* 大字体时收紧间距 */
  text-transform: uppercase;  /* 可选，增加力量感 */
}

/* 动态文字描边（仅轮廓，无填充） */
.outline-text {
  -webkit-text-stroke: 1px currentColor;
  color: transparent;
}

/* 混合描边+填充（常见创意效果） */
.mixed-title span:nth-child(odd)  { color: var(--c-text); }
.mixed-title span:nth-child(even) { 
  -webkit-text-stroke: 1px var(--c-text);
  color: transparent; 
}

/* 文字遮罩（用图片填充文字） */
.texture-text {
  background: url('./grain.jpg') center / cover;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* 竖排文字（日式设计感） */
.vertical-text {
  writing-mode: vertical-rl;
  text-orientation: mixed;
  letter-spacing: 0.15em;
}

/* 标签/标注小字 */
.label {
  font-size: var(--text-xs);
  font-weight: 500;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  opacity: 0.5;
}
```

## 文字动画 HTML 结构

```html
<!-- 逐词动画所需结构 -->
<h1 class="hero-title" data-split="words">
  Creating digital <span class="outline-text">experiences</span> that matter
</h1>

<!-- JS 自动处理拆分 -->
<script>
document.querySelectorAll('[data-split="words"]').forEach(el => {
  el.innerHTML = el.innerHTML
    .split(/(\s+)/)
    .filter(Boolean)
    .map(part => part.trim() 
      ? `<span class="word"><span class="word-inner">${part}</span></span>`
      : '<span class="space"> </span>'
    )
    .join('');
});
</script>

<style>
.word { 
  display: inline-block; 
  overflow: hidden; 
  vertical-align: top; 
}
.word-inner { 
  display: inline-block; 
  /* GSAP 会 animate yPercent: 110 → 0 */
}
</style>
```

## 排版排版节奏（Rhythm）

```css
/* 标准章节间距 */
.section { padding: clamp(80px, 15vw, 200px) clamp(20px, 5vw, 80px); }

/* 标题与正文间距 */
.section-title { margin-bottom: clamp(40px, 5vw, 80px); }

/* 行间距节奏 */
p { 
  line-height: 1.6; 
  max-width: 65ch;  /* 可读性最佳宽度 */
}

/* 数字角色（等宽数字，用于统计） */
.stat { font-variant-numeric: tabular-nums; }
```
