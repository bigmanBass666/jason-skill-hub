# 部署指南

## 1. 本地测试

```bash
# 在项目根目录下
cd D:/Working/programming_projects/jason-skill-hub

# 测试扫描脚本
node scripts/scan.js

# 检查生成的文件
cat skills/INDEX.md
cat _redirects
```

## 2. Netlify 部署

### 方法一：Netlify CLI（推荐）

```bash
# 安装 Netlify CLI
npm install -g netlify-cli

# 登录 Netlify
netlify login

# 初始化项目
netlify init

# 预览部署
netlify deploy

# 生产环境部署
netlify deploy --prod
```

### 方法二：GitHub 集成

1. 将项目推送到 GitHub
2. 在 Netlify 控制台连接 GitHub 仓库
3. 设置构建命令：`node scripts/scan.js`
4. 设置发布目录：`skills`

## 3. 部署后测试

部署完成后，测试以下 URL：

- **根目录**：`https://your-site.netlify.app/` - 应该显示 INDEX.md
- **Skill 目录**：`https://your-site.netlify.app/code-review/` - 应该重定向到 SKILL.md
- **具体文件**：`https://your-site.netlify.app/code-review/SKILL.md` - 应该显示技能内容

## 4. AI 使用示例

```
请查看 https://your-site.netlify.app 的技能库，
使用 code-review skill 帮我审查以下代码...
```

## 5. 添加新技能

1. 在 `skills/` 目录下创建新文件夹
2. 添加 `SKILL.md` 文件（包含 YAML frontmatter）
3. 运行 `node scripts/scan.js`
4. 重新部署

## 6. 故障排除

### 常见问题

- **404 错误**：检查 `_redirects` 文件是否正确生成
- **文件找不到**：确保 `skills/` 目录存在且包含文件
- **部署失败**：检查 Netlify 构建日志

### 日志检查

```bash
# Netlify CLI 查看部署日志
netlify logs
```
