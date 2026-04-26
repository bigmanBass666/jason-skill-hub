# Skill Catalog

这是一个技能索引文件，每个 skill 都托管在 GitHub 上作为独立的 `SKILL.md` 文件。

当你需要使用某个 skill 时，访问该 skill 的 Raw URL 可以获得更详细的工作流程和最佳实践建议。

## URL 推断规则

当 SKILL.md 中引用了相对路径的附属文件时，按以下规则推断完整 URL：

1. 当前 SKILL.md URL 去掉文件名，保留目录路径
2. 拼接相对路径，去掉 `./` 前缀
3. 示例：SKILL.md 在 `.../arch-design/SKILL.md`，引用 `./references/guide.md` → `.../arch-design/references/guide.md`

## Skills
### arch-design
- **Description**: 项目启动前的架构设计向导，专为用 AI 开发项目的初学者设计。当用户说「我想做一个新项目」「帮我规划一下架构」「我要开始开发 XX 系统」「我有一个想法想实现」「新项目怎么开始」「帮我想想怎么设计」时，必须使用此 skill，在写任何代码之前引导用户完成完整的架构设计。即使用户只是说「我想做个 XX」也应立即触发此 skill，阻止过早写代码。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/arch-design/SKILL.md

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

### canvas-design
- **Description**: 使用设计哲学创建精美的 .png 和 .pdf 视觉艺术作品。当用户要求创建海报、艺术品、设计稿或其他静态视觉作品时，必须使用此 skill。创建原创视觉设计，绝不复制现有艺术家作品以避免版权问题。关键词触发：「海报设计」「视觉艺术」「Canvas 绘图」「设计稿」「poster」「art design」。即使用户只说「帮我画张海报」也应触发此 skill。
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

### code-refactor
- **Description**: 专门用于 AI Agent 及复杂项目的代码优化与重构。当用户提到代码有 bug、架构混乱、屎山代码、模块不连贯、代码难以维护、想重构项目、需要 code review、遇到奇怪的错误但不知道根因、或者感觉代码越来越难改时，必须使用此 skill。关键词触发：「重构」「屎山」「bug 太多」「架构混乱」「模块耦合」「代码优化」「code review」「refactor」「技术债」「难以维护」「不知道哪里出问题」。即使用户只是说「这段代码越改越乱」也应触发此 skill。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/code-refactor/SKILL.md

### doc-coauthoring
- **Description**: 引导用户通过结构化工作流协作撰写文档。当用户需要撰写文档、提案、技术规格、决策文档或类似结构化内容时，必须使用此 skill。此工作流帮助用户高效传递上下文、通过迭代优化内容、并验证文档对读者的可读性。关键词触发：「写文档」「写提案」「技术规格」「文档协作」「draft spec」「proposal」。即使用户只说「帮我写个文档」也应触发此 skill。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/doc-coauthoring/SKILL.md

### docx
- **Description**: 当用户需要创建、读取、编辑或操作 Word 文档（.docx 文件）时，必须使用此 skill。触发场景包括：任何提及 Word 文档、.docx 的请求，或需要生成带目录、标题、页码、信头等专业格式文档的需求。也适用于从 .docx 文件中提取或重组内容、插入或替换图片、查找替换、处理修订或批注、或将内容转换为精美 Word 文档。如果用户要求以 Word 或 .docx 格式输出报告、备忘录、信件、模板等，使用此 skill。不适用于 PDF、电子表格、Google Docs 或与文档生成无关的编码任务。关键词触发：「Word 文档」「docx」「Word 报告」「文档编辑」。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/docx/SKILL.md
- **Files**:
  - LICENSE.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/docx/LICENSE.txt

### gitignore-gen
- **Description**: 自动分析当前 git 仓库的内容与用途，生成精准的 .gitignore 文件。适用于一切使用 git 进行版本管理的场景，不限于软件开发——包括写作/文档管理、数据分析、设计资产、学术研究、知识库、运维配置、财务记录、游戏开发等任意工作流。当用户说「帮我生成 gitignore」「生成 .gitignore」「我需要 gitignore」「仓库缺少 gitignore」「gitignore 怎么写」「帮我忽略不必要的文件」「哪些文件不需要提交」「git 应该忽略什么」时，必须使用此 skill。即使用户只是说「我在用 git 管理我的 XX，怎么配置忽略规则」也应立即触发。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/gitignore-gen/SKILL.md

### pdf
- **Description**: 当用户需要对 PDF 文件进行任何操作时，必须使用此 skill。包括：读取或提取 PDF 中的文本/表格、合并多个 PDF、拆分 PDF、旋转页面、添加水印、创建新 PDF、填写 PDF 表单、加密/解密 PDF、提取图片、以及对扫描 PDF 进行 OCR 使其可搜索。如果用户提及 .pdf 文件或要求生成 PDF，使用此 skill。关键词触发：「PDF」「合并 PDF」「拆分 PDF」「PDF 表单」「OCR」。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/pdf/SKILL.md
- **Files**:
  - forms.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/pdf/forms.md
  - LICENSE.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/pdf/LICENSE.txt
  - reference.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/pdf/reference.md

### pptx
- **Description**: 当涉及 .pptx 文件时（无论是输入、输出还是两者兼有），必须使用此 skill。包括：创建幻灯片、演示文稿或 PPT；读取、解析或提取 .pptx 文件中的文本；编辑、修改或更新现有演示文稿；合并或拆分幻灯片文件；处理模板、布局、演讲者备注或批注。当用户提及「演示文稿」「PPT」「幻灯片」「slides」「deck」或引用 .pptx 文件名时触发。只要需要打开、创建或操作 .pptx 文件，就使用此 skill。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/pptx/SKILL.md
- **Files**:
  - editing.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/pptx/editing.md
  - LICENSE.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/pptx/LICENSE.txt
  - pptxgenjs.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/pptx/pptxgenjs.md

### skill-creator
- **Description**: 创建新 skill、修改和改进现有 skill、以及衡量 skill 性能。当用户想从零创建 skill、更新或优化现有 skill、运行评估测试 skill、通过方差分析基准测试 skill 性能、或优化 skill 描述以提高触发准确性时，必须使用此 skill。关键词触发：「创建 skill」「优化 skill」「skill 评估」「skill 测试」「skill 性能」。即使用户只说「帮我写个 skill」也应触发此 skill。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/skill-creator/SKILL.md
- **Files**:
  - agents/analyzer.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/skill-creator/agents/analyzer.md
  - agents/comparator.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/skill-creator/agents/comparator.md
  - agents/grader.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/skill-creator/agents/grader.md
  - LICENSE.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/skill-creator/LICENSE.txt
  - references/schemas.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/skill-creator/references/schemas.md

### skill-ref-test
- **Description**: 引用关系验证测试专用 skill。当需要验证 AI 是否正确处理 SKILL.md 中的引用关系时使用此 skill。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/skill-ref-test/SKILL.md
- **Files**:
  - references/alpha.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/skill-ref-test/references/alpha.md
  - references/beta.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/skill-ref-test/references/beta.md
  - references/gamma.md → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/skill-ref-test/references/gamma.md

### webapp-testing
- **Description**: 使用 Playwright 与本地 Web 应用交互和测试的工具集。支持验证前端功能、调试 UI 行为、捕获浏览器截图和查看浏览器日志。当用户需要测试网页应用、调试前端问题、自动化浏览器操作、或验证 UI 行为时，必须使用此 skill。关键词触发：「测试网页」「Playwright」「浏览器测试」「UI 测试」「前端调试」「截图」。即使用户只说「帮我测试一下这个网页」也应触发此 skill。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/webapp-testing/SKILL.md
- **Files**:
  - LICENSE.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/webapp-testing/LICENSE.txt

### xlsx
- **Description**: 当电子表格文件是主要输入或输出时，必须使用此 skill。包括：打开、读取、编辑或修复 .xlsx、.xlsm、.csv 或 .tsv 文件（如添加列、计算公式、格式化、图表、清理数据）；从零创建电子表格或从其他数据源生成；在表格文件格式之间转换。当用户按名称或路径引用电子表格文件时尤其触发——即使是随口提及（如「我下载里的那个 xlsx」）。也适用于清理或重构混乱的表格数据文件（格式错误的行、错位的表头、垃圾数据）。交付物必须是电子表格文件。不适用于主要交付物是 Word 文档、HTML 报告、独立 Python 脚本、数据库管道或 Google Sheets API 集成的场景。关键词触发：「Excel」「表格」「xlsx」「csv」「电子表格」。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/xlsx/SKILL.md
- **Files**:
  - LICENSE.txt → https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/xlsx/LICENSE.txt

### zai-consult
- **Description**: 通过 z.ai 获取增强推理支持的求助协议。当你在同一个问题上连续尝试 3 次以上仍然失败、陷入深度架构设计/算法死胡同、或遇到超出当前能力的专业知识壁垒时，必须调用此 skill。不要因为小报错就触发，要在真正卡住时才使用。触发关键词：「去问 z.ai」「问一下 z.ai」「z.ai 求助」，或自主判断已满足触发条件。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/zai-consult/SKILL.md

