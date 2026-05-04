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
- **Description**: 创建具有 Awwwards 头奖级水准的设计级网站。当用户要求创建视觉震撼、沉浸式体验、头奖级的网站、作品集、品牌展示页、产品落地页、创意代理网站，或任何追求极致视觉与交互体验的 web 项目时，必须使用此 skill。关键词触发：「Awwwards 级别」「沉浸式网站」「震撼视觉」「高端网站」「创意交互」「WebGL」「Scrollytelling」「头奖设计」「极致动效」「创意代理网站」「Site of the Day」「SOTD」「超酷网站」「逼格网站」「设计感网站」「3D 网站」「滚动动画」「叙事滚动」「品牌体验」「作品集」「Portfolio」。即使用户只说「帮我做个很酷的网站」「做个有设计感的页面」也应触发此 skill。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/awwwards-design/SKILL.md
- **Has 12 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/awwwards-design/` Directories: references/, scripts/. File types: .md(8), .js(4).

### brainstorming
- **Description**: You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/brainstorming/SKILL.md
- **Has 7 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/brainstorming/` Directories: scripts/. File types: .sh(2), .md(2), .html(1), .js(1), .cjs(1).

### canvas-design
- **Description**: Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to create a poster, piece of art, design, or other static piece. Create original visual designs, never copying existing artists' work to avoid copyright violations.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/SKILL.md
- **Has 28 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/` Directories: canvas-fonts/. File types: .txt(28).

### design-principles
- **Description**: 软件设计原则审查器。用 SOLID、DRY、OCP 等经典原则对代码进行结构化审查，识别违反原则的设计并给出具体修复建议。当用户提到"设计原则"、"代码质量"、"SOLID"、"DRY"、"开闭原则"、"重构建议"、"架构审查"、"代码评审"、"设计模式"、"principles"、"code review"、"architecture review"、"代码坏味道"、"耦合"、"内聚"、"职责不清"时，必须使用此 skill。即使用户只是说"这段代码有什么问题"或"帮我看看架构合不合理"也应触发。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/design-principles/SKILL.md
- **Has 1 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/design-principles/` Directories: references/. File types: .md(1).

### doc-coauthoring
- **Description**: Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This workflow helps users efficiently transfer context, refine content through iteration, and verify the doc works for readers. Trigger when user mentions writing docs, creating proposals, drafting specs, or similar documentation tasks.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/doc-coauthoring/SKILL.md

### docx
- **Description**: Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/docx/SKILL.md
- **Has 60 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/docx/` Directories: scripts/. File types: .xsd(39), .py(15), .xml(5), .txt(1).

### find-skills
- **Description**: Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/find-skills/SKILL.md

### free-resource-hunter
- **Description**: 开发者免费资源情报雷达。通过增量对比扫描法（加载基线→多源搜索→计算差异→验证→输出增量）帮助开发者实时追踪 AI 模型 API、云服务、工具的免费/优惠变动。核心行为：对已知资源基线做增量对比，发现新增平台、模型变动、免费额度缩水、限时优惠等情报，输出结构化简报并回写基线。触发场景：免费资源搜索、免费 API 发现、资源变动追踪、限时优惠、模型上新、白嫖情报、平台评估。即使用户只说「最近有什么免费的」「扫一下」「跑一次」也应触发。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/free-resource-hunter/SKILL.md
- **Has 4 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/free-resource-hunter/` Directories: references/. File types: .md(4).

### frontend-design
- **Description**: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic AI aesthetics.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/frontend-design/SKILL.md
- **Has 1 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/frontend-design/` File types: .txt(1).

### gitignore-gen
- **Description**: 自动分析当前 git 仓库的内容与用途，生成精准的 .gitignore 文件。适用于一切使用 git 进行版本管理的场景，不限于软件开发——包括写作/文档管理、数据分析、设计资产、学术研究、知识库、运维配置、财务记录、游戏开发等任意工作流。当用户说「帮我生成 gitignore」「生成 .gitignore」「我需要 gitignore」「仓库缺少 gitignore」「gitignore 怎么写」「帮我忽略不必要的文件」「哪些文件不需要提交」「git 应该忽略什么」时，必须使用此 skill。即使用户只是说「我在用 git 管理我的 XX，怎么配置忽略规则」也应立即触发。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/gitignore-gen/SKILL.md
- **Has 9 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/gitignore-gen/` Directories: scripts/. File types: .py(9).

### huashu-design
- **Description**: 花叔Design（Huashu-Design）——用HTML做高保真原型、交互Demo、幻灯片、动画、设计变体探索+设计方向顾问+专家评审的一体化设计能力。HTML是工具不是媒介，根据任务embody不同专家（UX设计师/动画师/幻灯片设计师/原型师），避免web design tropes。触发词：做原型、设计Demo、交互原型、HTML演示、动画Demo、设计变体、hi-fi设计、UI mockup、prototype、设计探索、做个HTML页面、做个可视化、app原型、iOS原型、移动应用mockup、导出MP4、导出GIF、60fps视频、设计风格、设计方向、设计哲学、配色方案、视觉风格、推荐风格、选个风格、做个好看的、评审、好不好看、review this design。**主干能力**：Junior Designer工作流（先给假设+reasoning+placeholder再迭代）、反AI slop清单、React+Babel最佳实践、Tweaks变体切换、Speaker Notes演示、Starter Components（幻灯片外壳/变体画布/动画引擎/设备边框）、App原型专属守则（默认从Wikimedia/Met/Unsplash取真图、每台iPhone包AppPhone状态管理器可交互、交付前跑Playwright点击测试）、Playwright验证、HTML动画→MP4/GIF视频导出（25fps基础 + 60fps插帧 + palette优化GIF + 6首场景化BGM + 自动fade）。**需求模糊时的Fallback**：设计方向顾问模式——从5流派×20种设计哲学（Pentagram信息建筑/Field.io运动诗学/Kenya Hara东方极简/Sagmeister实验先锋等）推荐3个差异化方向，展示24个预制showcase（8场景×3风格），并行生成3个视觉Demo让用户选。**交付后可选**：专家级5维度评审（哲学一致性/视觉层级/细节执行/功能性/创新性各打10分+修复清单）。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/SKILL.md
- **Has 86 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/` Directories: assets/, demos/, references/, scripts/. File types: .html(44), .md(23), .jsx(6), .js(3), .mjs(3), .json(2), .sh(2), .gitignore(1), .license(1), .py(1).

### long-running-agent
- **Description**: Long-running agent implementation based on Anthropic's "Effective harnesses for long-running agents" article
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/long-running-agent/SKILL.md

### master-builder
- **Description**: Guides beginners to create top-tier software from scratch with built-in design principles. Invoke when user wants to start a new project, says 'I want to build X', or asks how to begin a project.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/master-builder/SKILL.md
- **Has 4 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/master-builder/` Directories: evals/, references/. File types: .md(3), .json(1).

### officecli
- **Description**: Create, analyze, proofread, and modify Office documents (.docx, .xlsx, .pptx) using the officecli CLI tool. Use when the user wants to create, inspect, check formatting, find issues, add charts, or modify Office documents.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/SKILL.md
- **Has 669 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/` Directories: .github/, examples/, schemas/, skills/, src/, styles/. File types: .cs(194), .md(152), .json(136), .sh(79), .xml(79), .py(19), .js(3), .yml(1), .license(1), .glb(1), .ps1(1), .slnx(1), .css(1), .csproj(1).

### pdf
- **Description**: Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/pdf/SKILL.md
- **Has 11 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/pdf/` Directories: scripts/. File types: .py(8), .md(2), .txt(1).

### pptx
- **Description**: Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions \"deck,\" \"slides,\" \"presentation,\" or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/pptx/SKILL.md
- **Has 58 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/pptx/` Directories: scripts/. File types: .xsd(39), .py(16), .md(2), .txt(1).

### skill-creator
- **Description**: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/skill-creator/SKILL.md
- **Has 17 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/skill-creator/` Directories: agents/, assets/, eval-viewer/, references/, scripts/. File types: .py(10), .md(4), .html(2), .txt(1).

### ui-ux-pro-max
- **Description**: UI/UX design intelligence. 67 styles, 96 palettes, 57 font pairings, 25 charts, 13 stacks (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui). Actions: plan, build, create, design, implement, review, fix, improve, optimize, enhance, refactor, check UI/UX code. Projects: website, landing page, dashboard, admin panel, e-commerce, SaaS, portfolio, blog, mobile app, .html, .tsx, .vue, .svelte. Elements: button, modal, navbar, sidebar, card, table, form, chart. Styles: glassmorphism, claymorphism, minimalism, brutalism, neumorphism, bento grid, dark mode, responsive, skeuomorphism, flat design. Topics: color palette, accessibility, animation, layout, typography, font pairing, spacing, hover, shadow, gradient. Integrations: shadcn/ui MCP for component search and examples.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/ui-ux-pro-max/SKILL.md
- **Has 27 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/ui-ux-pro-max/` Directories: data/, scripts/. File types: .csv(24), .py(3).

### xlsx
- **Description**: Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/xlsx/SKILL.md
- **Has 53 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/xlsx/` Directories: scripts/. File types: .xsd(39), .py(13), .txt(1).

### zai-consult
- **Description**: 通过 z.ai 获取增强推理支持的求助协议。当你在同一个问题上连续尝试 3 次以上仍然失败、陷入深度架构设计/算法死胡同、或遇到超出当前能力的专业知识壁垒时，必须调用此 skill。不要因为小报错就触发，要在真正卡住时才使用。触发关键词：「去问 z.ai」「问一下 z.ai」「z.ai 求助」，或自主判断已满足触发条件。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/zai-consult/SKILL.md

