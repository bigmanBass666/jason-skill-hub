---
name: article-to-image-prompt
description: 根据文章内容生成用于 ChatGPT（DALL-E）的英文绘图 prompt（封面主图）。当用户提供文章、博客、新闻、报告等文本内容，并希望生成配图、封面图、插图的绘图提示词时，必须使用此 skill。关键词触发：「生成prompt」「帮我配图」「生成封面」「文章插图」「生图提示词」「image prompt」「cover image」「ChatGPT生图」「DALL-E」。即使用户只说「帮我给这篇文章配张图」也应立即触发此 skill。
---

# Article → Image Prompt Generator（ChatGPT / DALL-E 专用）

根据文章内容，生成一个高质量的 DALL-E 绘图 prompt，专门针对 ChatGPT 的图像生成进行优化。

> **DALL-E Prompt 核心原则**：用**自然语言句子**描述，而非逗号堆砌的关键词标签。描述要具体、有画面感，像在给摄影师或插画师下指令。

---

## 工作流程

### Step 1：分析文章

阅读文章，提取以下核心要素：

- **核心主题**：文章在讲什么？（一句话概括）
- **情绪基调**：严肃/轻松/紧张/温暖/震撼/科技感……
- **关键意象**：文章中有哪些具体的视觉元素或隐喻？
- **目标受众**：文章面向谁？（影响画风选择）
- **用途场景**：封面主图，需要有视觉冲击力、信息传达清晰

### Step 2：选择画风

根据文章类型匹配最适合的画风：

| 文章类型 | 推荐风格 |
|----------|----------|
| 科技/AI | Cinematic digital art, futuristic, neon accents |
| 商业/财经 | Clean editorial illustration, flat design |
| 人文/情感 | Painterly, warm tones, impressionistic |
| 新闻/时事 | Photorealistic, documentary style |
| 生活方式 | Lifestyle photography aesthetic, bright and airy |
| 历史/文化 | Classical oil painting style, rich textures |
| 自然/环保 | National Geographic style, epic landscape |

### Step 3：构建 Prompt

DALL-E prompt 用**2-4句自然语言**描述，结构如下：

1. **第一句：主体场景**——谁/什么在哪里，在做什么
2. **第二句：风格与媒介**——"rendered as / painted in / photographed in the style of…"
3. **第三句：光线与氛围**——光线方向、色调、情绪
4. **第四句（可选）：构图细节**——视角、景深、比例

**DALL-E 专用技巧**：
- ✅ 用 `"in the style of [genre/medium]"` 而非具体艺术家名字
- ✅ 明确说 `"no text, no letters, no watermarks"` 避免乱入文字
- ✅ 指定比例：`"in a 16:9 wide format"` 或 `"square composition"`
- ✅ 用 `"photorealistic"` / `"digital illustration"` / `"oil painting style"` 控制质感
- ❌ 避免堆砌逗号分隔的标签（那是 Midjourney 风格，DALL-E 对句子理解更好）

### Step 4：输出格式

---

**🎨 封面图 Prompt**

```
[完整的英文 prompt，2-4句自然语言]
```

**📋 设计思路**
- 主视觉：[选择了什么画面，为什么]
- 风格：[为何匹配这篇文章]
- 氛围：[传达什么情绪/感受]

**💡 使用方式**
直接粘贴到 ChatGPT 对话框，发送给 DALL-E 生成即可。如需调整比例，可追加说明如 `"Please generate this in landscape 16:9 format"`。

---

## 注意事项

- **避免文字入画**：不要在 prompt 中描述包含文字、标题、logo 的场景（AI 生图对文字支持差）
- **避免真实人物**：不要使用名人姓名，改用描述性词语（如 `a middle-aged businessman` 而非具体姓名）
- **保持聚焦**：封面图只需一个视觉焦点，不要试图塞入文章所有内容
- **隐喻优先**：抽象主题（如「数字经济」）优先用视觉隐喻，而非字面呈现
