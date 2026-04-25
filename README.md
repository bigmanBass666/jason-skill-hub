# AI Skill Hub

一个**轻量级静态网站**，用于托管 Agent Skills 文件夹，让任何 AI agent 都能通过 URL **自动索引、按需读取** skill 文件及其依赖。

## 核心价值

解决「线上 chat/agent 无法像本地 CLI 那样便捷访问 skill 文件」的问题——**只需给 AI 一个链接，它就能自己找到并读取需要的 skill**。

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 创建 Skill

在 `skills/` 目录下创建新的 skill 文件夹，每个 skill 必须包含 `SKILL.md` 入口文件：

```
skills/
├── your-skill/
│   ├── SKILL.md          # 必需：skill 入口文件
│   └── references/
│       └── checklist.md  # 可选：引用文件
```

### 3. 生成索引

```bash
npm run scan
```

### 4. 部署到 Netlify

```bash
# 安装 Netlify CLI（仅首次）
npm install -g netlify-cli

# 部署（预览）
netlify deploy

# 生产环境部署
netlify deploy --prod
```

## 项目结构

```
ai-skill-hub/
├── skills/                 # Skill 文件目录
│   ├── INDEX.md           # 自动生成的索引
│   ├── code-review/       # 示例 skill
│   │   ├── SKILL.md
│   │   └── references/
│   └── pr-template/       # 示例 skill
│       └── references/
├── scripts/
│   └── scan.js            # 扫描生成脚本
├── netlify.toml           # Netlify 配置
├── _redirects             # URL 重定向规则（自动生成）
├── package.json
└── README.md
```

## 配置说明

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
/code-review /code-review/SKILL.md 200
/code-review/ /code-review/SKILL.md 200
```

## 可用技能

部署后访问根 URL 查看所有可用技能。

### Code Review
- 路径：`/code-review/SKILL.md`
- 用途：代码审查检查清单

### PR Template
- 路径：`/pr-template/SKILL.md`
- 用途：Pull Request 模板生成

## AI 使用说明

将部署后的 URL 提供给 AI，AI 可以：

1. 访问根 URL 获取技能目录
2. 根据需求访问具体 skill 文件
3. 自动追踪引用并读取依赖文件

示例：
```
请查看 https://your-site.netlify.app 的技能库，
使用 code-review skill 帮我审查以下代码...
```

## 开发

```bash
# 本地预览
npm run dev

# 重新生成索引
npm run scan
```

## License

MIT
