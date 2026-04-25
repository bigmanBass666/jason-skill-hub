# Skill Catalog

## URL拼接规则（必读）

所有skill文件都在GitHub的`skills/`目录下。

**基础URL**: `https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/`

**完整URL公式**: `https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/skills/` + **Path**

**示例**:
- INDEX.md在: `https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/skills/INDEX.md`
- skill-creator的SKILL.md在: `https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/skills/skill-creator/SKILL.md`
- awwwards-design的SKILL.md在: `https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/skills/awwwards-design/SKILL.md`

## 使用方法

**第一步**: 从下方选择一个skill

**第二步**: 找到它的Path，将Path直接拼接在`https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/skills/`后面

**第三步**: 访问完整URL抓取SKILL.md原文

> **⚠️ 强制要求**：
> - 你必须实际访问完整URL获取SKILL.md内容，**不能仅凭description推断**
> - 抓取后必须先输出SKILL.md的完整内容，证明你真的读取了
> - 必须按照SKILL.md里的步骤执行

## Skills### arch-design
- **Description**: 项目启动前的架构设计向导，专为用 AI 开发项目的初学者设计。当用户说「我想做一个新项目」「帮我规划一下架构」「我要开始开发 XX 系统」「我有一个想法想实现」「新项目怎么开始」「帮我想想怎么设计」时，必须使用此 skill，在写任何代码之前引导用户完成完整的架构设计。即使用户只是说「我想做个 XX」也应立即触发此 skill，阻止过早写代码。
- **Path**: `arch-design/SKILL.md`

### article-to-image-prompt
- **Description**: 根据文章内容生成用于 ChatGPT（DALL-E）的英文绘图 prompt（封面主图）。当用户提供文章、博客、新闻、报告等文本内容，并希望生成配图、封面图、插图的绘图提示词时，必须使用此 skill。关键词触发：「生成prompt」「帮我配图」「生成封面」「文章插图」「生图提示词」「image prompt」「cover image」「ChatGPT生图」「DALL-E」。即使用户只说「帮我给这篇文章配张图」也应立即触发此 skill。
- **Path**: `article-to-image-prompt/SKILL.md`

### awwwards-design
- **Description**: 创建能在 Awwwards 获奖的设计级网站。当用户要求创建视觉震撼、沉浸式体验、获奖级别的网站、作品集、品牌展示页、产品落地页，或任何追求极致视觉与交互体验的 web 项目时，必须使用此 skill。关键词触发：「Awwwards 级别」「沉浸式网站」「震撼视觉」「高端网站」「创意交互」「WebGL」「Scrollytelling」「获奖设计」「极致动效」「创意代理网站」。即使用户只说「帮我做个很酷的网站」也应触发此 skill，因为它包含了创建世界顶级 web 体验所需的全部技术与设计框架。
- **Path**: `awwwards-design/SKILL.md`

### canvas-design
- **Description**: 
- **Path**: `canvas-design/SKILL.md`

### code-refactor
- **Description**: 专门用于 AI Agent 及复杂项目的代码优化与重构。当用户提到代码有 bug、架构混乱、屎山代码、模块不连贯、代码难以维护、想重构项目、需要 code review、遇到奇怪的错误但不知道根因、或者感觉代码越来越难改时，必须使用此 skill。关键词触发：「重构」「屎山」「bug 太多」「架构混乱」「模块耦合」「代码优化」「code review」「refactor」「技术债」「难以维护」「不知道哪里出问题」。即使用户只是说「这段代码越改越乱」也应触发此 skill。
- **Path**: `code-refactor/SKILL.md`

### daily-summary
- **Description**: 以 AI 第一人称视角，总结用户在 Claude Code 中的对话活动，生成日记形式的工作记录。
- **Path**: `daily-summary/SKILL.md`

### diary-recorder
- **Description**: 以 AI 第一人称视角，根据真实 Claude 对话、本地 Claude 记录，以及用户提供的日记草稿或笔记，生成可写入日记的成稿。文风可偏文学，但不得虚构事实。
- **Path**: `diary-recorder/SKILL.md`

### doc-coauthoring
- **Description**: 
- **Path**: `doc-coauthoring/SKILL.md`

### docx
- **Description**: 
- **Path**: `docx/SKILL.md`

### gitignore-gen
- **Description**: 自动分析当前 git 仓库的内容与用途，生成精准的 .gitignore 文件。适用于一切使用 git 进行版本管理的场景，不限于软件开发——包括写作/文档管理、数据分析、设计资产、学术研究、知识库、运维配置、财务记录、游戏开发等任意工作流。当用户说「帮我生成 gitignore」「生成 .gitignore」「我需要 gitignore」「仓库缺少 gitignore」「gitignore 怎么写」「帮我忽略不必要的文件」「哪些文件不需要提交」「git 应该忽略什么」时，必须使用此 skill。即使用户只是说「我在用 git 管理我的 XX，怎么配置忽略规则」也应立即触发。
- **Path**: `gitignore-gen/SKILL.md`

### learning-report
- **Description**: 以 AI 第一人称视角、用户作为主角，生成学习过程报告。用于总结用户在一次协作中展现的能力、思维过程和学习成果。
- **Path**: `learning-report/SKILL.md`

### long-running-agent
- **Description**: Long-running agent implementation based on Anthropics Effective harnesses for long-running agents article
- **Path**: `long-running-agent/SKILL.md`

### pdf
- **Description**: 
- **Path**: `pdf/SKILL.md`

### pptx
- **Description**: 
- **Path**: `pptx/SKILL.md`

### pr-template
- **Description**: Pull Request 模板生成器 - 自动生成标准化的 PR 描述
- **Path**: `pr-template/SKILL.md`

### process-cleanup
- **Description**: 自动检测并清理所有残留的开发进程。当用户提到清理进程、清理残留、结束工作或需要释放资源时使用。支持清理 Node.js/npm、Python、Claude/MCP、Ruby 等各类开发相关进程，采用强制终止确保彻底清理。
- **Path**: `process-cleanup/SKILL.md`

### skill-creator
- **Description**: 
- **Path**: `skill-creator/SKILL.md`

### webapp-testing
- **Description**: 
- **Path**: `webapp-testing/SKILL.md`

### xlsx
- **Description**: 
- **Path**: `xlsx/SKILL.md`

### zai-consult
- **Description**: 通过 z.ai 获取增强推理支持的求助协议。当你在同一个问题上连续尝试 3 次以上仍然失败、陷入深度架构设计/算法死胡同、或遇到超出当前能力的专业知识壁垒时，必须调用此 skill。不要因为小报错就触发，要在真正卡住时才使用。触发关键词：「去问 z.ai」「问一下 z.ai」「z.ai 求助」，或自主判断已满足触发条件。
- **Path**: `zai-consult/SKILL.md`

