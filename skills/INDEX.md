# Skill Catalog

这是一个技能索引文件，每个 skill 都托管在 GitHub 上作为独立的 `SKILL.md` 文件。

当你需要使用某个 skill 时，访问该 skill 的 Raw URL 可以获得更详细的工作流程和最佳实践建议。

## URL 推断规则

当 SKILL.md 中引用了相对路径的附属文件时，按以下规则推断完整 URL：

1. 当前 SKILL.md URL 去掉文件名，保留目录路径
2. 拼接相对路径，去掉 `./` 前缀
3. 示例：SKILL.md 在 `.../arch-design/SKILL.md`，引用 `./references/guide.md` → `.../arch-design/references/guide.md`

## Skills
### article-to-image-prompt
- **Description**: 根据文章内容生成用于 ChatGPT（DALL-E）的英文绘图 prompt（封面主图）。当用户提供文章、博客、新闻、报告等文本内容，并希望生成配图、封面图、插图的绘图提示词时，必须使用此 skill。关键词触发：「生成prompt」「帮我配图」「生成封面」「文章插图」「生图提示词」「image prompt」「cover image」「ChatGPT生图」「DALL-E」。即使用户只说「帮我给这篇文章配张图」也应立即触发此 skill。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/article-to-image-prompt/SKILL.md

### awwwards-design
- **Description**: 创建能在 Awwwards 获奖的设计级网站。当用户要求创建视觉震撼、沉浸式体验、获奖级别的网站、作品集、品牌展示页、产品落地页、创意代理网站，或任何追求极致视觉与交互体验的 web 项目时，必须使用此 skill。关键词触发：「Awwwards 级别」「沉浸式网站」「震撼视觉」「高端网站」「创意交互」「WebGL」「Scrollytelling」「获奖设计」「极致动效」「创意代理网站」「Site of the Day」「SOTD」「超酷网站」「逼格网站」「设计感网站」「3D 网站」「滚动动画」「叙事滚动」「品牌体验」「作品集」「Portfolio」。即使用户只说「帮我做个很酷的网站」「做个有设计感的页面」也应触发此 skill。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/awwwards-design/SKILL.md
- **Files**:
  - references/animation-patterns.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/awwwards-design/references/animation-patterns.md
  - references/interaction-patterns.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/awwwards-design/references/interaction-patterns.md
  - references/performance-guide.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/awwwards-design/references/performance-guide.md
  - references/quality-framework.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/awwwards-design/references/quality-framework.md
  - references/typography-system.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/awwwards-design/references/typography-system.md
  - references/visual-styles.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/awwwards-design/references/visual-styles.md
  - references/webgl-patterns.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/awwwards-design/references/webgl-patterns.md

### awwwards-design
- **Description**: 创建具有 Awwwards 获奖水准的设计级网站。当用户要求创建视觉震撼、沉浸式体验、获奖级别的网站、作品集、品牌展示页、产品落地页、创意代理网站，或任何追求极致视觉与交互体验的 web 项目时，必须使用此 skill。关键词触发：「Awwwards 级别」「沉浸式网站」「震撼视觉」「高端网站」「创意交互」「WebGL」「Scrollytelling」「获奖设计」「极致动效」「创意代理网站」「Site of the Day」「SOTD」「超酷网站」「逼格网站」「设计感网站」「3D 网站」「滚动动画」「叙事滚动」「品牌体验」「作品集」「Portfolio」。即使用户只说「帮我做个很酷的网站」「做个有设计感的页面」也应触发此 skill。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/awwwards-design-new/SKILL.md
- **Files**:
  - ITERATION-GUIDE.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/awwwards-design-new/ITERATION-GUIDE.md
  - references/animation-patterns.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/awwwards-design-new/references/animation-patterns.md
  - references/design-process.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/awwwards-design-new/references/design-process.md
  - references/interaction-patterns.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/awwwards-design-new/references/interaction-patterns.md
  - references/performance-guide.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/awwwards-design-new/references/performance-guide.md
  - references/quality-framework.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/awwwards-design-new/references/quality-framework.md
  - references/typography-system.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/awwwards-design-new/references/typography-system.md
  - references/visual-styles.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/awwwards-design-new/references/visual-styles.md
  - references/webgl-patterns.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/awwwards-design-new/references/webgl-patterns.md

### brainstorming
- **Description**: You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/brainstorming/SKILL.md
- **Files**:
  - spec-document-reviewer-prompt.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/brainstorming/spec-document-reviewer-prompt.md
  - visual-companion.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/brainstorming/visual-companion.md

### canvas-design
- **Description**: Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to create a poster, piece of art, design, or other static piece. Create original visual designs, never copying existing artists' work to avoid copyright violations.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/SKILL.md
- **Files**:
  - canvas-fonts/ArsenalSC-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/ArsenalSC-OFL.txt
  - canvas-fonts/BigShoulders-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/BigShoulders-OFL.txt
  - canvas-fonts/Boldonse-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/Boldonse-OFL.txt
  - canvas-fonts/BricolageGrotesque-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/BricolageGrotesque-OFL.txt
  - canvas-fonts/CrimsonPro-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/CrimsonPro-OFL.txt
  - canvas-fonts/DMMono-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/DMMono-OFL.txt
  - canvas-fonts/EricaOne-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/EricaOne-OFL.txt
  - canvas-fonts/GeistMono-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/GeistMono-OFL.txt
  - canvas-fonts/Gloock-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/Gloock-OFL.txt
  - canvas-fonts/IBMPlexMono-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/IBMPlexMono-OFL.txt
  - canvas-fonts/InstrumentSans-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/InstrumentSans-OFL.txt
  - canvas-fonts/Italiana-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/Italiana-OFL.txt
  - canvas-fonts/JetBrainsMono-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/JetBrainsMono-OFL.txt
  - canvas-fonts/Jura-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/Jura-OFL.txt
  - canvas-fonts/LibreBaskerville-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/LibreBaskerville-OFL.txt
  - canvas-fonts/Lora-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/Lora-OFL.txt
  - canvas-fonts/NationalPark-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/NationalPark-OFL.txt
  - canvas-fonts/NothingYouCouldDo-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/NothingYouCouldDo-OFL.txt
  - canvas-fonts/Outfit-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/Outfit-OFL.txt
  - canvas-fonts/PixelifySans-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/PixelifySans-OFL.txt
  - canvas-fonts/PoiretOne-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/PoiretOne-OFL.txt
  - canvas-fonts/RedHatMono-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/RedHatMono-OFL.txt
  - canvas-fonts/Silkscreen-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/Silkscreen-OFL.txt
  - canvas-fonts/SmoochSans-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/SmoochSans-OFL.txt
  - canvas-fonts/Tektur-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/Tektur-OFL.txt
  - canvas-fonts/WorkSans-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/WorkSans-OFL.txt
  - canvas-fonts/YoungSerif-OFL.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/canvas-fonts/YoungSerif-OFL.txt
  - LICENSE.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/LICENSE.txt

### design-principles
- **Description**: 软件设计原则审查器。用 SOLID、DRY、OCP 等经典原则对代码进行结构化审查，识别违反原则的设计并给出具体修复建议。当用户提到"设计原则"、"代码质量"、"SOLID"、"DRY"、"开闭原则"、"重构建议"、"架构审查"、"代码评审"、"设计模式"、"principles"、"code review"、"architecture review"、"代码坏味道"、"耦合"、"内聚"、"职责不清"时，必须使用此 skill。即使用户只是说"这段代码有什么问题"或"帮我看看架构合不合理"也应触发。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/design-principles/SKILL.md
- **Files**:
  - references/principles.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/design-principles/references/principles.md

### doc-coauthoring
- **Description**: Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This workflow helps users efficiently transfer context, refine content through iteration, and verify the doc works for readers. Trigger when user mentions writing docs, creating proposals, drafting specs, or similar documentation tasks.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/doc-coauthoring/SKILL.md

### docx
- **Description**: Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/docx/SKILL.md
- **Files**:
  - LICENSE.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/docx/LICENSE.txt

### find-skills
- **Description**: Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/find-skills/SKILL.md

### free-resource-hunter
- **Description**: 开发者免费资源情报雷达。通过增量对比扫描法（加载基线→多源搜索→计算差异→验证→输出增量）帮助开发者实时追踪 AI 模型 API、云服务、工具的免费/优惠变动。核心行为：对已知资源基线做增量对比，发现新增平台、模型变动、免费额度缩水、限时优惠等情报，输出结构化简报并回写基线。触发场景：免费资源搜索、免费 API 发现、资源变动追踪、限时优惠、模型上新、白嫖情报、平台评估。即使用户只说「最近有什么免费的」「扫一下」「跑一次」也应触发。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/free-resource-hunter/SKILL.md
- **Files**:
  - references/evaluation-framework.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/free-resource-hunter/references/evaluation-framework.md
  - references/push-format.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/free-resource-hunter/references/push-format.md
  - references/resource-database.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/free-resource-hunter/references/resource-database.md
  - references/search-strategies.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/free-resource-hunter/references/search-strategies.md

### frontend-design
- **Description**: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic AI aesthetics.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/frontend-design/SKILL.md
- **Files**:
  - LICENSE.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/frontend-design/LICENSE.txt

### gitignore-gen
- **Description**: 自动分析当前 git 仓库的内容与用途，生成精准的 .gitignore 文件。适用于一切使用 git 进行版本管理的场景，不限于软件开发——包括写作/文档管理、数据分析、设计资产、学术研究、知识库、运维配置、财务记录、游戏开发等任意工作流。当用户说「帮我生成 gitignore」「生成 .gitignore」「我需要 gitignore」「仓库缺少 gitignore」「gitignore 怎么写」「帮我忽略不必要的文件」「哪些文件不需要提交」「git 应该忽略什么」时，必须使用此 skill。即使用户只是说「我在用 git 管理我的 XX，怎么配置忽略规则」也应立即触发。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/gitignore-gen/SKILL.md

### huashu-design
- **Description**: 花叔Design（Huashu-Design）——用HTML做高保真原型、交互Demo、幻灯片、动画、设计变体探索+设计方向顾问+专家评审的一体化设计能力。HTML是工具不是媒介，根据任务embody不同专家（UX设计师/动画师/幻灯片设计师/原型师），避免web design tropes。触发词：做原型、设计Demo、交互原型、HTML演示、动画Demo、设计变体、hi-fi设计、UI mockup、prototype、设计探索、做个HTML页面、做个可视化、app原型、iOS原型、移动应用mockup、导出MP4、导出GIF、60fps视频、设计风格、设计方向、设计哲学、配色方案、视觉风格、推荐风格、选个风格、做个好看的、评审、好不好看、review this design。**主干能力**：Junior Designer工作流（先给假设+reasoning+placeholder再迭代）、反AI slop清单、React+Babel最佳实践、Tweaks变体切换、Speaker Notes演示、Starter Components（幻灯片外壳/变体画布/动画引擎/设备边框）、App原型专属守则（默认从Wikimedia/Met/Unsplash取真图、每台iPhone包AppPhone状态管理器可交互、交付前跑Playwright点击测试）、Playwright验证、HTML动画→MP4/GIF视频导出（25fps基础 + 60fps插帧 + palette优化GIF + 6首场景化BGM + 自动fade）。**需求模糊时的Fallback**：设计方向顾问模式——从5流派×20种设计哲学（Pentagram信息建筑/Field.io运动诗学/Kenya Hara东方极简/Sagmeister实验先锋等）推荐3个差异化方向，展示24个预制showcase（8场景×3风格），并行生成3个视觉Demo让用户选。**交付后可选**：专家级5维度评审（哲学一致性/视觉层级/细节执行/功能性/创新性各打10分+修复清单）。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/SKILL.md
- **Files**:
  - assets/showcases/INDEX.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/assets/showcases/INDEX.md
  - README.en.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/README.en.md
  - README.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/README.md
  - references/animation-best-practices.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/references/animation-best-practices.md
  - references/animation-pitfalls.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/references/animation-pitfalls.md
  - references/animations.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/references/animations.md
  - references/apple-gallery-showcase.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/references/apple-gallery-showcase.md
  - references/audio-design-rules.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/references/audio-design-rules.md
  - references/cinematic-patterns.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/references/cinematic-patterns.md
  - references/content-guidelines.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/references/content-guidelines.md
  - references/critique-guide.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/references/critique-guide.md
  - references/design-context.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/references/design-context.md
  - references/design-styles.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/references/design-styles.md
  - references/editable-pptx.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/references/editable-pptx.md
  - references/hero-animation-case-study.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/references/hero-animation-case-study.md
  - references/react-setup.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/references/react-setup.md
  - references/scene-templates.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/references/scene-templates.md
  - references/sfx-library.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/references/sfx-library.md
  - references/slide-decks.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/references/slide-decks.md
  - references/tweaks-system.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/references/tweaks-system.md
  - references/verification.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/references/verification.md
  - references/video-export.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/references/video-export.md
  - references/workflow.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/references/workflow.md

### long-running-agent
- **Description**: Long-running agent implementation based on Anthropic's "Effective harnesses for long-running agents" article
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/long-running-agent/SKILL.md

### master-builder
- **Description**: Guides beginners to create top-tier software from scratch with built-in design principles. Invoke when user wants to start a new project, says 'I want to build X', or asks how to begin a project.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/master-builder/SKILL.md
- **Files**:
  - references/edge-cases.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/master-builder/references/edge-cases.md
  - references/principles.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/master-builder/references/principles.md
  - references/project-templates.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/master-builder/references/project-templates.md

### officecli
- **Description**: Create, analyze, proofread, and modify Office documents (.docx, .xlsx, .pptx) using the officecli CLI tool. Use when the user wants to create, inspect, check formatting, find issues, add charts, or modify Office documents.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/SKILL.md
- **Files**:
  - CONTRIBUTING.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/CONTRIBUTING.md
  - CONTRIBUTING.zh.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/CONTRIBUTING.zh.md
  - README.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/README.md
  - README_ja.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/README_ja.md
  - README_ko.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/README_ko.md
  - README_zh.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/README_zh.md
  - examples/README.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/README.md
  - examples/excel/charts-advanced.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/excel/charts-advanced.md
  - examples/excel/charts-area.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/excel/charts-area.md
  - examples/excel/charts-bar.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/excel/charts-bar.md
  - examples/excel/charts-basic.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/excel/charts-basic.md
  - examples/excel/charts-boxwhisker.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/excel/charts-boxwhisker.md
  - examples/excel/charts-bubble.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/excel/charts-bubble.md
  - examples/excel/charts-column.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/excel/charts-column.md
  - examples/excel/charts-combo.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/excel/charts-combo.md
  - examples/excel/charts-demo.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/excel/charts-demo.md
  - examples/excel/charts-extended.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/excel/charts-extended.md
  - examples/excel/charts-histogram.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/excel/charts-histogram.md
  - examples/excel/charts-line.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/excel/charts-line.md
  - examples/excel/charts-pie.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/excel/charts-pie.md
  - examples/excel/charts-radar.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/excel/charts-radar.md
  - examples/excel/charts-scatter.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/excel/charts-scatter.md
  - examples/excel/charts-stock.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/excel/charts-stock.md
  - examples/excel/charts-waterfall.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/excel/charts-waterfall.md
  - examples/excel/charts.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/excel/charts.md
  - examples/excel/pivot-tables.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/excel/pivot-tables.md
  - examples/ppt/3d-model.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/ppt/3d-model.md
  - examples/ppt/animations.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/ppt/animations.md
  - examples/ppt/presentation.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/ppt/presentation.md
  - examples/ppt/templates/README.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/ppt/templates/README.md
  - examples/ppt/templates/styles/product--aionui-promo/outline.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/ppt/templates/styles/product--aionui-promo/outline.md
  - examples/ppt/video.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/ppt/video.md
  - examples/word/formulas.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/word/formulas.md
  - examples/word/tables.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/word/tables.md
  - examples/word/textbox.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/examples/word/textbox.md
  - schemas/README.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/schemas/README.md
  - skills/morph-ppt/SKILL.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/SKILL.md
  - skills/morph-ppt/reference/decision-rules.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/decision-rules.md
  - skills/morph-ppt/reference/pptx-design.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/pptx-design.md
  - skills/morph-ppt/reference/styles/INDEX.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/INDEX.md
  - skills/morph-ppt/reference/styles/bw--brutalist-raw/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/bw--brutalist-raw/style.md
  - skills/morph-ppt/reference/styles/bw--mono-line/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/bw--mono-line/style.md
  - skills/morph-ppt/reference/styles/bw--swiss-bauhaus/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/bw--swiss-bauhaus/style.md
  - skills/morph-ppt/reference/styles/bw--swiss-system/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/bw--swiss-system/style.md
  - skills/morph-ppt/reference/styles/dark--architectural-plan/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/dark--architectural-plan/style.md
  - skills/morph-ppt/reference/styles/dark--aurora-softedge/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/dark--aurora-softedge/style.md
  - skills/morph-ppt/reference/styles/dark--blueprint-grid/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/dark--blueprint-grid/style.md
  - skills/morph-ppt/reference/styles/dark--circle-digital/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/dark--circle-digital/style.md
  - skills/morph-ppt/reference/styles/dark--cosmic-neon/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/dark--cosmic-neon/style.md
  - skills/morph-ppt/reference/styles/dark--cyber-future/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/dark--cyber-future/style.md
  - skills/morph-ppt/reference/styles/dark--diagonal-cut/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/dark--diagonal-cut/style.md
  - skills/morph-ppt/reference/styles/dark--editorial-story/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/dark--editorial-story/style.md
  - skills/morph-ppt/reference/styles/dark--investor-pitch/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/dark--investor-pitch/style.md
  - skills/morph-ppt/reference/styles/dark--liquid-flow/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/dark--liquid-flow/style.md
  - skills/morph-ppt/reference/styles/dark--luxury-minimal/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/dark--luxury-minimal/style.md
  - skills/morph-ppt/reference/styles/dark--midnight-blueprint/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/dark--midnight-blueprint/style.md
  - skills/morph-ppt/reference/styles/dark--neon-productivity/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/dark--neon-productivity/style.md
  - skills/morph-ppt/reference/styles/dark--obsidian-amber/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/dark--obsidian-amber/style.md
  - skills/morph-ppt/reference/styles/dark--premium-navy/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/dark--premium-navy/style.md
  - skills/morph-ppt/reference/styles/dark--sage-grain/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/dark--sage-grain/style.md
  - skills/morph-ppt/reference/styles/dark--space-odyssey/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/dark--space-odyssey/style.md
  - skills/morph-ppt/reference/styles/dark--spotlight-stage/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/dark--spotlight-stage/style.md
  - skills/morph-ppt/reference/styles/dark--velvet-rose/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/dark--velvet-rose/style.md
  - skills/morph-ppt/reference/styles/light--bold-type/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/light--bold-type/style.md
  - skills/morph-ppt/reference/styles/light--firmwise-saas/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/light--firmwise-saas/style.md
  - skills/morph-ppt/reference/styles/light--fluid-gradient/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/light--fluid-gradient/style.md
  - skills/morph-ppt/reference/styles/light--glassmorphism-vc/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/light--glassmorphism-vc/style.md
  - skills/morph-ppt/reference/styles/light--isometric-clean/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/light--isometric-clean/style.md
  - skills/morph-ppt/reference/styles/light--minimal-corporate/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/light--minimal-corporate/style.md
  - skills/morph-ppt/reference/styles/light--minimal-product/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/light--minimal-product/style.md
  - skills/morph-ppt/reference/styles/light--project-proposal/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/light--project-proposal/style.md
  - skills/morph-ppt/reference/styles/light--spring-launch/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/light--spring-launch/style.md
  - skills/morph-ppt/reference/styles/light--training-interactive/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/light--training-interactive/style.md
  - skills/morph-ppt/reference/styles/light--watercolor-wash/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/light--watercolor-wash/style.md
  - skills/morph-ppt/reference/styles/mixed--bauhaus-blocks/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/mixed--bauhaus-blocks/style.md
  - skills/morph-ppt/reference/styles/mixed--chromatic-aberration/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/mixed--chromatic-aberration/style.md
  - skills/morph-ppt/reference/styles/mixed--duotone-split/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/mixed--duotone-split/style.md
  - skills/morph-ppt/reference/styles/mixed--spectral-grid/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/mixed--spectral-grid/style.md
  - skills/morph-ppt/reference/styles/vivid--bauhaus-electric/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/vivid--bauhaus-electric/style.md
  - skills/morph-ppt/reference/styles/vivid--candy-stripe/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/vivid--candy-stripe/style.md
  - skills/morph-ppt/reference/styles/vivid--energy-neon/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/vivid--energy-neon/style.md
  - skills/morph-ppt/reference/styles/vivid--pink-editorial/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/vivid--pink-editorial/style.md
  - skills/morph-ppt/reference/styles/vivid--playful-marketing/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/vivid--playful-marketing/style.md
  - skills/morph-ppt/reference/styles/warm--bloom-academy/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/warm--bloom-academy/style.md
  - skills/morph-ppt/reference/styles/warm--brand-refresh/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/warm--brand-refresh/style.md
  - skills/morph-ppt/reference/styles/warm--coral-culture/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/warm--coral-culture/style.md
  - skills/morph-ppt/reference/styles/warm--earth-organic/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/warm--earth-organic/style.md
  - skills/morph-ppt/reference/styles/warm--monument-editorial/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/warm--monument-editorial/style.md
  - skills/morph-ppt/reference/styles/warm--playful-organic/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/warm--playful-organic/style.md
  - skills/morph-ppt/reference/styles/warm--sunset-mosaic/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/warm--sunset-mosaic/style.md
  - skills/morph-ppt/reference/styles/warm--vital-bloom/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt/reference/styles/warm--vital-bloom/style.md
  - skills/morph-ppt-3d/SKILL.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/morph-ppt-3d/SKILL.md
  - skills/officecli-academic-paper/SKILL.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/officecli-academic-paper/SKILL.md
  - skills/officecli-data-dashboard/SKILL.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/officecli-data-dashboard/SKILL.md
  - skills/officecli-docx/SKILL.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/officecli-docx/SKILL.md
  - skills/officecli-financial-model/SKILL.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/officecli-financial-model/SKILL.md
  - skills/officecli-pitch-deck/SKILL.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/officecli-pitch-deck/SKILL.md
  - skills/officecli-pptx/SKILL.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/officecli-pptx/SKILL.md
  - skills/officecli-word-form/SKILL.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/officecli-word-form/SKILL.md
  - skills/officecli-xlsx/SKILL.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/skills/officecli-xlsx/SKILL.md
  - styles/INDEX.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/INDEX.md
  - styles/bw--brutalist-raw/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/bw--brutalist-raw/style.md
  - styles/bw--mono-line/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/bw--mono-line/style.md
  - styles/bw--swiss-bauhaus/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/bw--swiss-bauhaus/style.md
  - styles/bw--swiss-system/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/bw--swiss-system/style.md
  - styles/dark--architectural-plan/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/dark--architectural-plan/style.md
  - styles/dark--aurora-softedge/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/dark--aurora-softedge/style.md
  - styles/dark--blueprint-grid/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/dark--blueprint-grid/style.md
  - styles/dark--circle-digital/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/dark--circle-digital/style.md
  - styles/dark--cosmic-neon/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/dark--cosmic-neon/style.md
  - styles/dark--cyber-future/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/dark--cyber-future/style.md
  - styles/dark--diagonal-cut/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/dark--diagonal-cut/style.md
  - styles/dark--editorial-story/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/dark--editorial-story/style.md
  - styles/dark--investor-pitch/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/dark--investor-pitch/style.md
  - styles/dark--liquid-flow/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/dark--liquid-flow/style.md
  - styles/dark--luxury-minimal/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/dark--luxury-minimal/style.md
  - styles/dark--midnight-blueprint/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/dark--midnight-blueprint/style.md
  - styles/dark--neon-productivity/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/dark--neon-productivity/style.md
  - styles/dark--obsidian-amber/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/dark--obsidian-amber/style.md
  - styles/dark--premium-navy/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/dark--premium-navy/style.md
  - styles/dark--sage-grain/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/dark--sage-grain/style.md
  - styles/dark--space-odyssey/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/dark--space-odyssey/style.md
  - styles/dark--spotlight-stage/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/dark--spotlight-stage/style.md
  - styles/dark--velvet-rose/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/dark--velvet-rose/style.md
  - styles/light--bold-type/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/light--bold-type/style.md
  - styles/light--firmwise-saas/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/light--firmwise-saas/style.md
  - styles/light--fluid-gradient/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/light--fluid-gradient/style.md
  - styles/light--glassmorphism-vc/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/light--glassmorphism-vc/style.md
  - styles/light--isometric-clean/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/light--isometric-clean/style.md
  - styles/light--minimal-corporate/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/light--minimal-corporate/style.md
  - styles/light--minimal-product/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/light--minimal-product/style.md
  - styles/light--project-proposal/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/light--project-proposal/style.md
  - styles/light--spring-launch/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/light--spring-launch/style.md
  - styles/light--training-interactive/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/light--training-interactive/style.md
  - styles/light--watercolor-wash/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/light--watercolor-wash/style.md
  - styles/mixed--bauhaus-blocks/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/mixed--bauhaus-blocks/style.md
  - styles/mixed--chromatic-aberration/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/mixed--chromatic-aberration/style.md
  - styles/mixed--duotone-split/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/mixed--duotone-split/style.md
  - styles/mixed--spectral-grid/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/mixed--spectral-grid/style.md
  - styles/vivid--bauhaus-electric/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/vivid--bauhaus-electric/style.md
  - styles/vivid--candy-stripe/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/vivid--candy-stripe/style.md
  - styles/vivid--energy-neon/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/vivid--energy-neon/style.md
  - styles/vivid--pink-editorial/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/vivid--pink-editorial/style.md
  - styles/vivid--playful-marketing/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/vivid--playful-marketing/style.md
  - styles/warm--bloom-academy/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/warm--bloom-academy/style.md
  - styles/warm--brand-refresh/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/warm--brand-refresh/style.md
  - styles/warm--coral-culture/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/warm--coral-culture/style.md
  - styles/warm--earth-organic/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/warm--earth-organic/style.md
  - styles/warm--monument-editorial/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/warm--monument-editorial/style.md
  - styles/warm--playful-organic/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/warm--playful-organic/style.md
  - styles/warm--sunset-mosaic/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/warm--sunset-mosaic/style.md
  - styles/warm--vital-bloom/style.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/styles/warm--vital-bloom/style.md

### pdf
- **Description**: Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/pdf/SKILL.md
- **Files**:
  - forms.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/pdf/forms.md
  - LICENSE.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/pdf/LICENSE.txt
  - reference.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/pdf/reference.md

### pptx
- **Description**: Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions \"deck,\" \"slides,\" \"presentation,\" or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/pptx/SKILL.md
- **Files**:
  - editing.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/pptx/editing.md
  - LICENSE.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/pptx/LICENSE.txt
  - pptxgenjs.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/pptx/pptxgenjs.md

### skill-creator
- **Description**: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/skill-creator/SKILL.md
- **Files**:
  - agents/analyzer.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/skill-creator/agents/analyzer.md
  - agents/comparator.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/skill-creator/agents/comparator.md
  - agents/grader.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/skill-creator/agents/grader.md
  - LICENSE.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/skill-creator/LICENSE.txt
  - references/schemas.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/skill-creator/references/schemas.md

### ui-ux-pro-max
- **Description**: UI/UX design intelligence. 67 styles, 96 palettes, 57 font pairings, 25 charts, 13 stacks (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui). Actions: plan, build, create, design, implement, review, fix, improve, optimize, enhance, refactor, check UI/UX code. Projects: website, landing page, dashboard, admin panel, e-commerce, SaaS, portfolio, blog, mobile app, .html, .tsx, .vue, .svelte. Elements: button, modal, navbar, sidebar, card, table, form, chart. Styles: glassmorphism, claymorphism, minimalism, brutalism, neumorphism, bento grid, dark mode, responsive, skeuomorphism, flat design. Topics: color palette, accessibility, animation, layout, typography, font pairing, spacing, hover, shadow, gradient. Integrations: shadcn/ui MCP for component search and examples.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/ui-ux-pro-max/SKILL.md

### xlsx
- **Description**: Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/xlsx/SKILL.md
- **Files**:
  - LICENSE.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/xlsx/LICENSE.txt

### zai-consult
- **Description**: 通过 z.ai 获取增强推理支持的求助协议。当你在同一个问题上连续尝试 3 次以上仍然失败、陷入深度架构设计/算法死胡同、或遇到超出当前能力的专业知识壁垒时，必须调用此 skill。不要因为小报错就触发，要在真正卡住时才使用。触发关键词：「去问 z.ai」「问一下 z.ai」「z.ai 求助」，或自主判断已满足触发条件。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/zai-consult/SKILL.md

