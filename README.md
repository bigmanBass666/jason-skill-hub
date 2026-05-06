# Jason Skill Hub — AI Agent 技能库

> 轻量级静态站点，托管 AI Agent 技能文件，支持任意 AI 代理通过 URL 自动索引和读取

## 项目简介

Jason Skill Hub 是一个为 AI Agent 设计的技能托管平台。它将各类 AI 技能（Skills）组织成结构化文档，使任何支持 URL 访问的 AI 代理都能自动发现、索引和调用这些技能。

**在线访问**: [jason-skill-hub.netlify.app](https://jason-skill-hub.netlify.app/)

## 核心特性

- **URL 可访问**：每个技能文件都有唯一的网络地址
- **自动索引**：AI Agent 可通过 `skills.json` 自动发现所有技能
- **分类管理**：技能按领域分类，便于检索
- **Netlify 托管**：全球 CDN 加速，访问速度快
- **自动同步**：支持文件变更自动同步

## 技能清单

| 技能 | 说明 |
|------|------|
| `article-to-image-prompt` | 文章转图像提示词 |
| `awwwards-design` | Awwwards 级别设计规范 |
| `brainstorming` | 头脑风暴方法论 |
| `canvas-design` | Canvas 设计技巧 |
| `design-principles` | 设计原则指南 |
| `doc-coauthoring` | 文档协作撰写 |
| `docx` | Word 文档处理 |
| `find-skills` | 技能发现与检索 |
| `free-resource-hunter` | 免费资源搜寻 |
| `frontend-design` | 前端设计规范 |
| `gitignore-gen` | .gitignore 生成器 |
| `huashu-design` | 话术设计 |
| `long-agent-plugin` | 长时运行 Agent 插件 |
| `long-running-agent` | 长时任务 Agent |
| `master-builder` | 主构建器技能 |
| `officecli` | Office CLI 工具 |
| `pdf` | PDF 处理技能 |
| `pptx` | PPT 处理技能 |
| `skill-creator` | 技能创建器 |
| `super-prompt-architect` | 超级提示词架构师 |
| `ui-ux-pro-max` | UI/UX 专业设计 |
| `xlsx` | Excel 处理技能 |
| `zai-consult` | 咨询对话技能 |

## 技术栈

| 技术 | 说明 |
|------|------|
| **Netlify** | 静态网站托管与部署 |
| **Node.js** | 构建脚本运行环境 |
| **chokidar** | 文件监听与自动同步 |

## 项目结构

```
jason-skill-hub/
├── skills/                  # 技能文件目录
│   ├── INDEX.md            # 技能索引
│   ├── INDEX_HEADER.md     # 索引头部模板
│   ├── skills.json         # 机器可读技能清单
│   └── [skill-name]/       # 各技能目录
│       └── skill.md        # 技能定义文件
├── scripts/                 # 构建脚本
│   ├── scan.js             # 扫描生成索引
│   └── sync-watch.js       # 文件同步监听
├── .github/                 # GitHub 配置
├── package.json
└── netlify.toml            # Netlify 配置
```

## 快速开始

### 安装依赖

```bash
npm install
```

### 扫描生成索引

```bash
npm run scan
```

### 开发模式（文件监听）

```bash
npm run sync
```

### 部署到 Netlify

```bash
npm run deploy
```

## 添加新技能

1. 在 `skills/` 目录下创建新文件夹
2. 编写 `skill.md` 技能定义文件
3. 运行 `npm run scan` 更新索引
4. 提交并推送，Netlify 自动部署

## 技能文件格式

技能文件采用 Markdown 格式，包含：

```markdown
# 技能名称

## 描述
技能功能说明

## 用法
使用示例

## 参数
| 参数 | 类型 | 说明 |

## 示例
具体使用案例
```

## 作者

- **GitHub**: [bigmanBass666](https://github.com/bigmanBass666)

---

*为 AI Agent 赋能，让技能共享更简单*
