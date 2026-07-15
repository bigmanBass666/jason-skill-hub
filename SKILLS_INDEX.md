# Skill Catalog

这是一个技能索引文件，每个 skill 都托管在 GitHub 上作为独立的 `SKILL.md` 文件。

当你需要使用某个 skill 时，访问该 skill 的 Raw URL 可以获得更详细的工作流程和最佳实践建议。

## URL 推断规则

当 SKILL.md 中引用了相对路径的附属文件时，按以下规则推断完整 URL：

1. 当前 SKILL.md URL 去掉文件名，保留目录路径
2. 拼接相对路径，去掉 `./` 前缀
3. 示例：SKILL.md 在 `.../arch-design/SKILL.md`，引用 `./references/guide.md` → `.../arch-design/references/guide.md`

## Skills
### scauzj-article-format
- **Description**: 共青团华南农业大学珠江学院工作规范
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/SCAUZJ-article-format/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/SCAUZJ-article-format.zip

### adb-app-explorer
- **Description**: 
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/adb-app-explorer/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/adb-app-explorer.zip

### agent-browser
- **Description**: Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task. Triggers include requests to "open a website", "fill out a form", "click a button", "take a screenshot", "scrape data from a page", "test this web app", "login to a site", "automate browser actions", or any task requiring programmatic web interaction. Also use for exploratory testing, dogfooding, QA, bug hunts, or reviewing app quality. Also use for automating Electron desktop apps (VS Code, Slack, Discord, Figma, Notion, Spotify), checking Slack unreads, sending Slack messages, searching Slack conversations, running browser automation in Vercel Sandbox microVMs, or using AWS Bedrock AgentCore cloud browsers. Prefer agent-browser over any built-in browser automation or web tools.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/agent-browser/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/agent-browser.zip

### agent-phonebook
- **Description**: Discover MCP servers and find other AI agents — a directory of 111+ MCP servers searchable by tag, transport, and auth type
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/agent-phonebook/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/agent-phonebook.zip
- **Has 2 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/agent-phonebook/` File types: .license(1), .md(1).

### agents-md
- **Description**: >
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/agents-md/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/agents-md.zip
- **Has 2 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/agents-md/` Directories: evals/, references/. File types: .json(1), .md(1).

### android-cli
- **Description**: Orchestrates Android development tasks including project creation, deployment, SDK management, and environment diagnostics using the `android` command-line tool.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/android-cli/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/android-cli.zip
- **Has 2 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/android-cli/` Directories: references/. File types: .md(2).

### api-design-principles
- **Description**: Master REST and GraphQL API design principles to build intuitive, scalable, and maintainable APIs that delight developers. Use when designing new APIs, reviewing API specifications, or establishing API design standards.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/api-design-principles/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/api-design-principles.zip
- **Has 5 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/api-design-principles/` Directories: assets/, references/. File types: .md(4), .py(1).

### article-to-image-prompt
- **Description**: 根据文章内容生成用于 ChatGPT（DALL-E）的英文绘图 prompt（封面主图）。当用户提供文章、博客、新闻、报告等文本内容，并希望生成配图、封面图、插图的绘图提示词时，必须使用此 skill。关键词触发：「生成prompt」「帮我配图」「生成封面」「文章插图」「生图提示词」「image prompt」「cover image」「ChatGPT生图」「DALL-E」。即使用户只说「帮我给这篇文章配张图」也应立即触发此 skill。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/article-to-image-prompt/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/article-to-image-prompt.zip

### ask-matt
- **Description**: 询问当前情境适合哪个技能或流程；它是本仓库所有 skills 的路由器。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/ask-matt/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/ask-matt.zip

### canvas-design
- **Description**: Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to create a poster, piece of art, design, or other static piece. Create original visual designs, never copying existing artists' work to avoid copyright violations.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/canvas-design.zip
- **Has 28 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/canvas-design/` Directories: canvas-fonts/. File types: .txt(28).

### cc-switch
- **Description**: 管理和操作 cc-switch 配置数据库。当用户提到 cc-switch、provider 管理、MCP 服务器配置、AI 供应商切换、故障转移设置、代理配置时触发。覆盖：添加/删除/切换 provider、MCP 服务器管理、Skills 管理、Prompts 管理、Failover 队列、Proxy 配置、环境检查。即使用户只是说「加个 AI 供应商」「切一下 provider」「看看 cc-switch 配置」也应触发。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/cc-switch/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/cc-switch.zip
- **Has 2 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/cc-switch/` Directories: references/. File types: .disabled(1), .md(1).

### chaoxing-auto-answer
- **Description**: >
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/chaoxing-auto-answer/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/chaoxing-auto-answer.zip
- **Has 1 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/chaoxing-auto-answer/` Directories: evals/. File types: .json(1).

### claude-handoff
- **Description**: 为 Claude Code 创建交接摘要。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/claude-handoff/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/claude-handoff.zip

### claude-project-mover
- **Description**: 在两个项目路径之间同步 Claude 会话历史（非搬文件）。覆盖两种场景：(1) 全量历史迁移 — 用户自己搬了项目文件夹后迁移所有历史会话；(2) 单会话同步 — 把当前或指定会话复制到另一项目目录（worktree / 多目录场景）。当用户说"搬项目"、"迁移历史"、"同步聊天记录"、"sync session"、"保留对话"、"claude 历史不见了"、"change project path but keep history"、"relocate project"、"move this folder but keep claude history"时触发。注意：用户说"聊天记录不见了"或"历史会话不见了"通常也是这个 skill 的触发场景——先检查 `~/.claude/projects/` 下的目录是否存在且名字匹配实际项目路径。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/claude-project-mover/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/claude-project-mover.zip
- **Has 2 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/claude-project-mover/` Directories: scripts/. File types: .py(2).

### code-review
- **Description**: 从固定点（commit、branch、tag 或 merge-base）开始，按 Standards（代码是否符合本仓库记录的编码标准？）和 Spec（代码是否符合来源 issue/PRD 的要求？）两个轴线审查变更。两个审查会在并行子代理中运行，并并排报告。适用于用户想审查 branch、PR、进行中的变更，或要求 “review since X” 时。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/code-review/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/code-review.zip

### code-review-skill
- **Description**: |
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/code-review-skill/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/code-review-skill.zip
- **Has 47 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/code-review-skill/` Directories: .hive/, assets/, reference/, scripts/. File types: .md(40), .html(2), .py(2), .gitignore(1), .nojekyll(1), .license(1).

### codebase-design
- **Description**: 用于设计深模块的共享词汇。适用于用户想设计或改进模块接口、寻找深化机会、决定 seam 放在哪里、让代码更容易测试或更适合 AI 导航，或其他技能需要深模块词汇时。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/codebase-design/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/codebase-design.zip
- **Has 2 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/codebase-design/` File types: .md(2).

### design-an-interface
- **Description**: 使用并行子代理为模块生成多个显著不同的接口设计。适用于用户想设计 API、探索接口选项、比较模块形状，或提到 “design it twice” 时。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/design-an-interface/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/design-an-interface.zip

### design-principles
- **Description**: 软件设计原则审查器。用 SOLID、DRY、OCP 等经典原则对代码进行结构化审查，识别违反原则的设计并给出具体修复建议。当用户提到"设计原则"、"代码质量"、"SOLID"、"DRY"、"开闭原则"、"重构建议"、"架构审查"、"代码评审"、"设计模式"、"principles"、"code review"、"architecture review"、"代码坏味道"、"耦合"、"内聚"、"职责不清"时，必须使用此 skill。即使用户只是说"这段代码有什么问题"或"帮我看看架构合不合理"也应触发。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/design-principles/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/design-principles.zip
- **Has 1 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/design-principles/` Directories: references/. File types: .md(1).

### diagnosing-bugs
- **Description**: 面向棘手缺陷和性能回退的诊断循环。适用于用户说 “diagnose” / “debug this”，或报告某些东西 broken、throwing、failing、slow 时。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/diagnosing-bugs/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/diagnosing-bugs.zip
- **Has 1 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/diagnosing-bugs/` Directories: scripts/. File types: .sh(1).

### doc-links
- **Description**: 文档链接索引 skill。内部维护各技术栈的 llms.txt 及目录页 URL，当需要查阅官方文档时按域匹配索引、语义查找具体页面。工作方式是：Claude 自行按需 Fetch 索引内容并匹配返回链接。触发场景：用户提到某个技术并需要查阅官方文档、用户直接索要某个技术的文档链接、用户在编码时需要参考官方文档。注意：只返回链接，不做内容总结或解读。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/doc-links/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/doc-links.zip
- **Has 1 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/doc-links/` Directories: references/. File types: .md(1).

### docx
- **Description**: Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/docx/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/docx.zip
- **Has 57 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/docx/` Directories: scripts/. File types: .xsd(39), .py(15), .xml(2), .txt(1).

### domain-modeling
- **Description**: 构建并打磨项目的领域模型。适用于用户想明确领域术语或通用语言、记录架构决策，或其他技能需要维护领域模型时。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/domain-modeling/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/domain-modeling.zip
- **Has 2 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/domain-modeling/` File types: .md(2).

### edit-article
- **Description**: 通过重组章节、提升清晰度、收紧文字来编辑并改进文章。适用于用户想编辑、修订或改进文章草稿时。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/edit-article/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/edit-article.zip

### everything-manager
- **Description**: |
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/everything-manager/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/everything-manager.zip
- **Has 2 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/everything-manager/` Directories: scripts/. File types: .ps1(2).

### find-skills
- **Description**: Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/find-skills/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/find-skills.zip

### free-resource-hunter
- **Description**: 开发者免费资源情报雷达。通过增量对比扫描帮助实时追踪 AI 模型 API、云服务、工具的免费/优惠变动。触发场景：免费资源搜索、模型上新、额度变动、限时优惠、平台评估、Token 赠送。即使用户只说「最近有什么免费的」「扫一下」「跑一次」也应触发。当用户提到任何免费 AI 资源、额度、平台变动相关话题时都应使用此 skill。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/free-resource-hunter/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/free-resource-hunter.zip
- **Has 3 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/free-resource-hunter/` Directories: references/. File types: .md(3).

### free-vision
- **Description**: 为无原生视觉能力的模型提供图片处理能力。当 VISION_BLOCK_READ=1（纯文本模型模式）时，通过此 skill 调用多模型后端分析图片。多模态模型直接使用原生视觉，无需调用此 skill。支持文件路径、URL、Playwright 截图等输入，通过 zhipu-4v / zhipu-thinking / stepfun-3.7 等后端完成视觉任务。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/free-vision/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/free-vision.zip
- **Has 5 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/free-vision/` Directories: evals/, references/, scripts/. File types: .md(2), .py(2), .json(1).

### frontend-design
- **Description**: Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direction, typography, and making choices that don't read as templated defaults.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/frontend-design/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/frontend-design.zip
- **Has 1 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/frontend-design/` File types: .txt(1).

### git-guardrails-claude-code
- **Description**: 设置 Claude Code hooks，在危险 git commands（push、reset --hard、clean、branch -D 等）执行前阻止它们。适用于用户想防止破坏性 git 操作、添加 git safety hooks，或在 Claude Code 中阻止 git push/reset 时。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/git-guardrails-claude-code/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/git-guardrails-claude-code.zip
- **Has 1 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/git-guardrails-claude-code/` Directories: scripts/. File types: .sh(1).

### github-repo-initializer
- **Description**: Initialize a new GitHub open-source repository with all essential community health files (README, CONTRIBUTING, CODE_OF_CONDUCT, LICENSE, SECURITY, SUPPORT, issue/PR templates). Use this skill whenever the user mentions creating a new repo, setting up an open-source project, initializing a GitHub repository, or adding standard community files. Also use it when the user asks about "community profile", "health files", or wants to follow GitHub's best practices for open source.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/github-repo-initializer/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/github-repo-initializer.zip

### goal-generator-lite
- **Description**: >
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/goal-generator-lite/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/goal-generator-lite.zip

### god-view
- **Description**: 
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/god-view/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/god-view.zip

### grill-me
- **Description**: 一个用来打磨计划或设计的持续追问式访谈。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/grill-me/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/grill-me.zip

### grill-with-docs
- **Description**: 一个用来打磨计划或设计的持续追问式访谈，并在过程中创建文档（ADRs 和词汇表）。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/grill-with-docs/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/grill-with-docs.zip

### grilling
- **Description**: 围绕计划或设计持续追问用户。适用于用户想在构建前压力测试计划，或使用任何 “grill” 触发措辞时。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/grilling/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/grilling.zip

### handoff
- **Description**: 把当前对话压缩成交接文档，让另一个代理接手。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/handoff/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/handoff.zip

### huashu-design
- **Description**: 花叔Design——用HTML做高保真原型、幻灯片、动画、可视化与专家评审，需求模糊时给设计方向。触发词：做原型、PPT、幻灯片、动画、设计风格、评审、做个HTML页面、UI mockup、导出MP4/GIF、做个好看的。生产级Web App/需后端的系统不适用。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/huashu-design.zip
- **Has 108 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/huashu-design/` Directories: assets/, demos/, references/, scripts/. File types: .html(46), .md(32), .jsx(7), .mjs(6), .js(4), .json(4), .sh(4), .py(2), .example(1), .gitignore(1), .license(1).

### ima-skill
- **Description**: |
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/ima-skill/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/ima-skill.zip
- **Has 8 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/ima-skill/` Directories: knowledge-base/, notes/. File types: .md(4), .cjs(3), .json(1).

### implement
- **Description**: 基于 spec 或 ticket 集合实现一段工作。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/implement/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/implement.zip

### improve-codebase-architecture
- **Description**: 扫描代码库中的深化机会，生成可视化 HTML 报告，然后围绕你选中的候选项继续追问。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/improve-codebase-architecture/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/improve-codebase-architecture.zip
- **Has 1 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/improve-codebase-architecture/` File types: .md(1).

### kaggle-run
- **Description**: Kaggle-Run v4.0 — Ultimate Kaggle integration. Thin router + fat scripts for zero token waste. Deploy notebooks, auto-fix errors, compete, earn badges, analyze leaderboards. Windows/Mac/Linux.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/kaggle-run/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/kaggle-run.zip
- **Has 7 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/kaggle-run/` Directories: scripts/. File types: .py(7).

### karing
- **Description**: >
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/karing/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/karing.zip
- **Has 1 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/karing/` Directories: references/. File types: .md(1).

### long-running-agent
- **Description**: Long-running agent implementation based on Anthropic's "Effective harnesses for long-running agents" article
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/long-running-agent/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/long-running-agent.zip

### loop-me
- **Description**: 在这个工作区中，就我想构建的工作流规格访谈我。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/loop-me/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/loop-me.zip

### master-builder
- **Description**: Guides beginners to create top-tier software from scratch with built-in design principles. Invoke when user wants to start a new project, says 'I want to build X', or asks how to begin a project.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/master-builder/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/master-builder.zip
- **Has 4 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/master-builder/` Directories: evals/, references/. File types: .md(3), .json(1).

### memory-cleanup
- **Description**: >
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/memory-cleanup/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/memory-cleanup.zip
- **Has 8 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/memory-cleanup/` Directories: evals/. File types: .json(7), .html(1).

### memu-android-guide
- **Description**: >
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/memu-android-guide/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/memu-android-guide.zip

### migrate-to-shoehorn
- **Description**: 将测试文件从 `as` 类型断言迁移到 @total-typescript/shoehorn。适用于用户提到 shoehorn、想替换测试中的 `as`，或需要局部测试数据时。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/migrate-to-shoehorn/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/migrate-to-shoehorn.zip

### obsidian-vault
- **Description**: 在 Obsidian vault 中使用 wikilinks 和索引笔记搜索、创建并管理笔记。适用于用户想在 Obsidian 中查找、创建或组织笔记时。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/obsidian-vault/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/obsidian-vault.zip

### officecli
- **Description**: Create, analyze, proofread, and modify Office documents (.docx, .xlsx, .pptx) using the officecli CLI tool. Use when the user wants to create, inspect, check formatting, find issues, add charts, or modify Office documents.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/officecli/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/officecli.zip

### pdf
- **Description**: Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/pdf/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/pdf.zip
- **Has 11 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/pdf/` Directories: scripts/. File types: .py(8), .md(2), .txt(1).

### pptx
- **Description**: Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions \"deck,\" \"slides,\" \"presentation,\" or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/pptx/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/pptx.zip
- **Has 58 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/pptx/` Directories: scripts/. File types: .xsd(39), .py(16), .md(2), .txt(1).

### prototype
- **Description**: 在承诺方案前构建一次性原型来细化设计。根据问题在两个分支之间选择：用于状态或业务逻辑问题的可运行终端应用，或在同一路由中切换的多个显著不同 UI 变体。适用于用户想做原型、检查数据模型或状态机、模拟 UI、探索设计选项，或说 “prototype this”、“let me play with it”、“try a few designs” 时。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/prototype/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/prototype.zip
- **Has 2 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/prototype/` File types: .md(2).

### qa
- **Description**: 交互式 QA 会话，用户以对话方式报告缺陷或问题，代理创建 GitHub issues。后台探索代码库以获取上下文和领域语言。适用于用户想报告缺陷、执行 QA、以对话方式提交 issues，或提到 “QA session” 时。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/qa/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/qa.zip

### request-refactor-plan
- **Description**: 通过用户访谈创建带小提交的详细重构计划，然后作为 GitHub issue 提交。适用于用户想规划重构、创建重构 RFC，或把重构拆成安全的增量步骤时。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/request-refactor-plan/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/request-refactor-plan.zip

### research
- **Description**: 对照高可信一手来源调研问题，并把发现保存为仓库中的 Markdown 文件。适用于用户想调研主题、收集文档或 API 事实，或把阅读工作委托给后台代理时。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/research/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/research.zip

### resolving-merge-conflicts
- **Description**: 适用于需要解决正在进行的 git merge/rebase 冲突时。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/resolving-merge-conflicts/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/resolving-merge-conflicts.zip

### save-work-dir
- **Description**: 记录当前工作目录到桌面的历史文件。当用户说"记录工作目录"、"保存工作目录"、"记录当前目录"、"save work dir"、"记住这个目录"时触发此 skill。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/save-work-dir/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/save-work-dir.zip

### scaffold-exercises
- **Description**: 创建包含章节、题目、答案和讲解的练习目录结构，并确保通过 linting。适用于用户想 scaffold exercises、创建 exercise stubs，或设置新的课程章节时。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/scaffold-exercises/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/scaffold-exercises.zip

### setup-matt-pocock-skills
- **Description**: 配置此仓库供工程技能使用：设置 issue tracker、分诊标签词汇和领域文档布局。首次使用其他工程技能前运行一次。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/setup-matt-pocock-skills/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/setup-matt-pocock-skills.zip
- **Has 5 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/setup-matt-pocock-skills/` File types: .md(5).

### setup-pre-commit
- **Description**: 在当前仓库设置 Husky pre-commit hooks，集成 lint-staged (Prettier)、类型检查和测试。适用于用户想添加 pre-commit hooks、设置 Husky、配置 lint-staged，或在提交时运行格式化、类型检查和测试时。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/setup-pre-commit/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/setup-pre-commit.zip

### setup-project-mcp
- **Description**: 一键在项目中注册 MCP 服务器，自动创建/更新 .mcp.json。当用户说"添加项目级 MCP"、"配置 MCP 服务器"、"register MCP"、"setup project MCP"、"帮我在项目中注册一个 MCP"或需要将某个 MCP 服务器关联到当前项目时，使用此 skill。即使配置来自其他 MCP 服务器的 deferred tools 列表（系统注入的 <system-reminder>），也应使用此 skill 将其写入 .mcp.json。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/setup-project-mcp/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/setup-project-mcp.zip

### skill-creator
- **Description**: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/skill-creator/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/skill-creator.zip
- **Has 18 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/skill-creator/` Directories: agents/, assets/, eval-viewer/, references/, scripts/. File types: .py(10), .md(4), .html(2), .txt(1), .bak(1).

### sub-agent-designer
- **Description**: >
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/sub-agent-designer/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/sub-agent-designer.zip
- **Has 3 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/sub-agent-designer/` Directories: references/, scripts/. File types: .md(2), .py(1).

### subagent-inspect
- **Description**: 审计 Claude Code 子代理 (subagent) 的完整执行轨迹，涵盖定位 JSONL 日志、审计工具调用序列、诊断 AI 决策-行动断裂点。当用户提到 eval 子代理、子代理推理链、subagent 日志、查看子代理执行过程、审计 sub-agent、分析 agent 决策、为什么 AI 没做 X、subagent trace 时使用此 skill。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/subagent-inspect/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/subagent-inspect.zip
- **Has 5 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/subagent-inspect/` Directories: evals/, references/, scripts/. File types: .md(3), .json(1), .py(1).

### tdd
- **Description**: 测试驱动开发。适用于用户想用先写测试的方式构建功能或修复缺陷、提到 “red-green-refactor”，或需要集成测试时。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/tdd/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/tdd.zip
- **Has 3 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/tdd/` File types: .md(3).

### teach
- **Description**: 在这个工作区中教用户一个新技能或概念。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/teach/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/teach.zip
- **Has 4 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/teach/` File types: .md(4).

### to-issues
- **Description**: 使用 tracer-bullet 垂直切片，把计划、规格或 PRD 拆成项目 issue tracker 上可独立领取的 issues。适用于用户想把计划转成 issues、创建实现议题，或把工作拆成 issues 时。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/to-issues/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/to-issues.zip

### to-prd
- **Description**: 将当前对话上下文转成 PRD，并发布到项目 issue tracker。适用于用户想基于当前上下文创建 PRD 时。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/to-prd/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/to-prd.zip

### trae-forum-pro
- **Description**: >
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/trae-forum-pro/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/trae-forum-pro.zip
- **Has 6 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/trae-forum-pro/` Directories: evals/, references/, scripts/. File types: .md(3), .sh(2), .json(1).

### trae-plan
- **Description**: 优先规划任务的执行方向，用户确认后再执行
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/trae-plan/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/trae-plan.zip

### trae-solo-cn
- **Description**: Automate the TRAE SOLO CN desktop app (ByteDance's AI coding assistant) using agent-browser via Chrome DevTools Protocol. Use when the user needs to interact with TRAE SOLO CN, automate AI chat tasks, manage workspaces, install skills, configure automation jobs, or perform dogfooding/QA on the Solo application. Triggers include 'automate Solo', 'control TRAE SOLO', 'interact with Solo app', 'send prompt to Solo AI', 'switch Solo workspace', 'install Solo skill', 'configure Solo automation', 'dogfood TRAE SOLO', 'test TRAE SOLO CN', or any task requiring automation of the TRAE SOLO CN desktop application. Also trigger when the user mentions 'Solo桌面版', 'Trae Solo', 'TRAE SOLO', 'solo-cn', 'Solo AI', or asks to do anything with the Solo AI coding assistant.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/trae-solo-cn/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/trae-solo-cn.zip
- **Has 8 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/trae-solo-cn/` Directories: references/, scripts/, templates/. File types: .md(5), .ps1(3).

### trae-solo-cn-config
- **Description**: 
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/trae-solo-cn-config/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/trae-solo-cn-config.zip

### trae-spec
- **Description**: 根据需求细化完整的规范、任务、验收文档，用户确认后再严格执行，适合复杂的长线任务
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/trae-spec/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/trae-spec.zip

### triage
- **Description**: 通过分诊角色驱动的状态机分诊 issues。适用于用户想创建 issue、分诊 issues、审查 incoming bugs 或 feature requests、为 AFK agent 准备 issues，或管理 issue workflow 时。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/triage/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/triage.zip
- **Has 2 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/triage/` File types: .md(2).

### ubiquitous-language
- **Description**: 从当前对话提取 DDD 风格的 ubiquitous language glossary，标记歧义并提出标准术语。保存到 UBIQUITOUS_LANGUAGE.md。适用于用户想定义领域术语、构建词汇表、收紧术语、创建通用语言，或提到 “domain model” / “DDD” 时。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/ubiquitous-language/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/ubiquitous-language.zip

### ui-ux-pro-max
- **Description**: UI/UX design intelligence. 67 styles, 96 palettes, 57 font pairings, 25 charts, 13 stacks (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui). Actions: plan, build, create, design, implement, review, fix, improve, optimize, enhance, refactor, check UI/UX code. Projects: website, landing page, dashboard, admin panel, e-commerce, SaaS, portfolio, blog, mobile app, .html, .tsx, .vue, .svelte. Elements: button, modal, navbar, sidebar, card, table, form, chart. Styles: glassmorphism, claymorphism, minimalism, brutalism, neumorphism, bento grid, dark mode, responsive, skeuomorphism, flat design. Topics: color palette, accessibility, animation, layout, typography, font pairing, spacing, hover, shadow, gradient. Integrations: shadcn/ui MCP for component search and examples.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/ui-ux-pro-max/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/ui-ux-pro-max.zip
- **Has 27 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/ui-ux-pro-max/` Directories: data/, scripts/. File types: .csv(24), .py(3).

### wayfinder
- **Description**: 把单个代理会话装不下的大块工作规划成 issue tracker 上的调查议题共享地图，并一次解决一个议题，直到通往目标的路径清晰。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/wayfinder/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/wayfinder.zip

### wizard
- **Description**: 运行向导模板，引导多步骤命令行流程。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/wizard/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/wizard.zip
- **Has 1 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/wizard/` File types: .sh(1).

### wiztree-cli
- **Description**: >
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/wiztree-cli/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/wiztree-cli.zip

### writing-beats
- **Description**: 以自选路径风格，把文章塑造成一段节拍旅程。用户从原始素材中选择起始节拍，你只写这一段，然后提供下一步转向选项，逐个节拍推进，直到文章自然结束。适用于用户已有原始素材，并想把它组装成叙事而不是论证时。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/writing-beats/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/writing-beats.zip

### writing-fragments
- **Description**: 一种追问式会话，用来从用户那里挖掘片段，也就是各类写作素材（主张、小场景、尖锐句子、半成形想法），并追加到单一文档中，作为未来文章的原始素材。适用于用户想在施加结构前发展想法，或提到 “fragments”、“ideate”、“raw material” 写作素材时。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/writing-fragments/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/writing-fragments.zip

### writing-great-skills
- **Description**: 编写和编辑优秀 skills 的参考：让技能可预测的词汇和原则。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/writing-great-skills/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/writing-great-skills.zip
- **Has 1 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/writing-great-skills/` File types: .md(1).

### writing-shape
- **Description**: 通过对话会话，把一份原始素材 Markdown 文件塑造成文章：起草候选开头，逐段扩展，并在每一步讨论格式（列表、表格、提示块、引用）。适用于用户有一堆笔记、片段或粗稿，并希望把它变成可发布作品时。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/writing-shape/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/writing-shape.zip

### xlsx
- **Description**: Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved.
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/xlsx/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/xlsx.zip
- **Has 53 file(s)**: ⚠️ You MUST read these files before using this skill. Access by appending relative path to the Raw URL base: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/xlsx/` Directories: scripts/. File types: .xsd(39), .py(13), .txt(1).

### zai-consult
- **Description**: 通过 z.ai 获取增强推理支持的求助协议。当你在同一个问题上连续尝试 3 次以上仍然失败、陷入深度架构设计/算法死胡同、或遇到超出当前能力的专业知识壁垒时，必须调用此 skill。不要因为小报错就触发，要在真正卡住时才使用。触发关键词：「去问 z.ai」「问一下 z.ai」「z.ai 求助」，或自主判断已满足触发条件。
- **Raw**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/zai-consult/SKILL.md
- **Zip**: https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@pkg/zai-consult.zip

