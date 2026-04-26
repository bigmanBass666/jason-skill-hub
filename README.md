# AI Skill Hub

一个**轻量级静态网站**，用于托管 Agent Skills 文件夹，让任何 AI agent 都能通过 URL **自动索引、按需读取** skill 文件及其依赖。

## 🤖 AI 快速开始

**只需告诉 AI 以下链接，它会自动发现所有 skills：**

```
https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/INDEX.md
```

**JSON 格式索引（AI 解析更可靠）：**

```
https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/skills.json
```

> **为什么用 jsDelivr CDN？**
> - 国内 AI 平台访问 GitHub Raw URL 不稳定
> - jsDelivr 是免费的 CDN 服务，访问更可靠
> - 同时提供 gcore 国内加速节点作为备选

AI 会自动：
1. 读取 INDEX.md 发现所有可用 skills
2. 根据 Path 读取对应的 SKILL.md
3. 自动推断并读取关联的参考文件

## 🔗 URL 格式选项

### 方式 1：jsDelivr CDN（推荐）

```
https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/INDEX.md
```

稳定可靠，推荐用于所有 AI 平台。

同样支持 skills.json 格式：`https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/skills.json`

### 方式 2：gcore 国内加速（备选）

```
https://gcore.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/INDEX.md
```

国内访问速度更快，作为备选方案。

同样支持 skills.json 格式：`https://gcore.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/skills.json`

### 方式 3：GitHub Raw（备选）

```
https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/skills/INDEX.md
```

部分 AI 平台可能访问不稳定，仅作备选。

同样支持 skills.json 格式：`https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/skills/skills.json`

## 🤝 AI 平台兼容性

| 平台 | 状态 | 说明 |
|------|------|------|
| 智谱 AI | ✅ 推荐 | 完全支持 skill 引用处理 |
| Kimi.ai | ✅ 可用 | 支持基本访问 |
| 通义千问 | ⚠️ 可用 | 基本功能正常 |
| z.ai | ❌ 不可用 | 网页抓取 403 错误 |
| 文心一言 | ❌ 不可用 | 代码解释器限制 |

## 📦 可用 Skills（15 个）

| Skill | 描述 |
|-------|------|
| **arch-design** | 项目启动前的架构设计向导 |
| **article-to-image-prompt** | 根据文章内容生成绘图 prompt |
| **awwwards-design** | 创建 Awwwards 获奖级别网站 |
| **canvas-design** | Canvas 视觉艺术设计 |
| **code-refactor** | AI Agent 代码优化与重构 |
| **doc-coauthoring** | 文档协作工作流 |
| **docx** | Word 文档操作 |
| **gitignore-gen** | 自动生成 .gitignore 文件 |
| **pdf** | PDF 文件操作 |
| **pptx** | PPT 演示文稿操作 |
| **skill-creator** | Skill 创建与优化 |
| **skill-ref-test** | 引用关系验证测试 |
| **webapp-testing** | Web 应用测试工具集 |
| **xlsx** | Excel 表格操作 |
| **zai-consult** | z.ai 增强推理咨询协议 |

## 🚀 快速部署

### 安装依赖

```bash
npm install
```

### 创建 Skill

在 `skills/` 目录下创建新的 skill 文件夹，每个 skill 必须包含 `SKILL.md` 入口文件：

```
skills/
├── your-skill/
│   ├── SKILL.md          # 必需：skill 入口文件
│   └── references/
│       └── checklist.md  # 可选：引用文件
```

### 生成索引

```bash
npm run scan
```

### 部署到 Netlify

```bash
# 安装 Netlify CLI（仅首次）
npm install -g netlify-cli

# 部署（预览）
netlify deploy

# 生产环境部署
netlify deploy --prod
```

## 📁 项目结构

```
ai-skill-hub/
├── skills/                 # Skill 文件目录
│   ├── INDEX.md           # 自动生成的索引
│   ├── arch-design/       # 架构设计 skill
│   ├── article-to-image-prompt/ # 绘图 prompt 生成
│   ├── awwwards-design/   # Awwwards 网站设计
│   ├── canvas-design/     # Canvas 视觉设计
│   ├── code-refactor/     # 代码优化与重构
│   ├── doc-coauthoring/   # 文档协作工作流
│   ├── docx/              # Word 文档操作
│   ├── gitignore-gen/     # .gitignore 生成
│   ├── pdf/               # PDF 文件操作
│   ├── pptx/              # PPT 演示文稿操作
│   ├── skill-creator/     # Skill 创建与优化
│   ├── skill-ref-test/    # 引用关系验证测试
│   ├── webapp-testing/    # Web 应用测试
│   ├── xlsx/              # Excel 表格操作
│   └── zai-consult/       # z.ai 增强推理咨询
├── docs/                   # 文档目录
│   └── url-guide.md       # URL 推断指南
├── scripts/
│   └── scan.js            # 扫描生成脚本
├── netlify.toml           # Netlify 配置
├── _redirects             # URL 重定向规则（自动生成）
├── AGENTS.md              # AI Agent 提示词
├── AGENTS.md.template     # AI Agent 提示词模板
├── package.json
└── README.md
```

## ⚙️ 配置说明

### netlify.toml

```toml
[build]
  publish = "skills"
  command = "node scripts/scan.js"
```

构建时自动执行 `scan.js` 生成索引和重定向规则。

### _redirects

自动生成的重定向规则，将目录路径重定向到 `SKILL.md`：

```
/arch-design /arch-design/SKILL.md 200
/arch-design/ /arch-design/SKILL.md 200
```

## 💡 AI 使用示例

```markdown
请查看 https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/INDEX.md
使用 awwwards-design skill 帮我创建一个震撼的作品集网站
```

```markdown
请查看 https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/INDEX.md
使用 code-refactor skill 重构我的代码
```

## 🔧 开发

```bash
# 本地预览
npm run dev

# 重新生成索引
npm run scan
```

## License

MIT
