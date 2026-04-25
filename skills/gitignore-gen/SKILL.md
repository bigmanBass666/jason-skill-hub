---
name: gitignore-gen
description: 自动分析当前 git 仓库的内容与用途，生成精准的 .gitignore 文件。适用于一切使用 git 进行版本管理的场景，不限于软件开发——包括写作/文档管理、数据分析、设计资产、学术研究、知识库、运维配置、财务记录、游戏开发等任意工作流。当用户说「帮我生成 gitignore」「生成 .gitignore」「我需要 gitignore」「仓库缺少 gitignore」「gitignore 怎么写」「帮我忽略不必要的文件」「哪些文件不需要提交」「git 应该忽略什么」时，必须使用此 skill。即使用户只是说「我在用 git 管理我的 XX，怎么配置忽略规则」也应立即触发。
---

# gitignore-gen Skill

分析 git 仓库的**用途类型**与**文件构成**，生成贴合实际工作流的 `.gitignore`——不只是代码项目，任何用 git 做版本管理的场景都适用。

---

## Step 1：判断仓库用途类型

这是最关键的第一步。扫描前先向用户确认（或通过文件特征自动判断）仓库属于哪种工作场景：

| 类型 | 典型特征文件/目录 | 场景示例 |
|------|-----------------|---------|
| **软件开发** | package.json、*.py、Cargo.toml、go.mod、pom.xml | 应用、工具、库、API |
| **数据分析 / 科研** | *.ipynb、*.csv、*.parquet、*.RData、*.mat | 数据探索、机器学习、学术计算 |
| **写作 / 文档** | *.md、*.tex、*.docx、*.rst、*.adoc | 书稿、博客、技术文档、论文 |
| **设计 / 创意资产** | *.fig、*.sketch、*.psd、*.ai、*.xd | UI 设计、品牌资产、插画 |
| **知识管理** | .obsidian/、logseq/、*.org、roam/ | 个人笔记库、团队 Wiki |
| **运维 / 基础设施** | *.tf、*.yaml(k8s)、ansible/、*.hcl | 服务器配置、IaC、CI/CD |
| **游戏开发** | Assets/、*.unity、*.uproject、*.godot | Unity、Unreal、Godot 项目 |
| **学术研究** | *.tex、*.bib、references/、data/ | LaTeX 论文、文献管理、实验数据 |
| **个人 / 业务记录** | *.xlsx、*.numbers、*.pdf、invoices/ | 财务、合同、报表跟踪 |
| **混合型** | 多类型文件并存 | 以上任意组合 |

若无法自动判断，直接问用户：**「这个仓库主要用来做什么？」**

---

## Step 2：扫描目录结构

```bash
# 根目录概览（含隐藏文件）
ls -la <repo_root>

# 扫描所有文件类型分布（排除 .git）
find <repo_root> -maxdepth 4 -type f \
  -not -path "*/.git/*" \
  -not -path "*/node_modules/*" \
  2>/dev/null \
  | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -30

# 检查是否有现有 .gitignore
cat <repo_root>/.gitignore 2>/dev/null || echo "(无现有 .gitignore)"
```

---

## Step 3：按用途生成规则

每个仓库都应包含**通用基础规则**，再按场景叠加专属规则。

### 通用基础规则（所有仓库必含）

```gitignore
# —— 操作系统 ——
# macOS
.DS_Store
.AppleDouble
.LSOverride
._*

# Windows
Thumbs.db
ehthumbs.db
Desktop.ini
$RECYCLE.BIN/

# Linux
*~
.fuse_hidden*
.Trash-*

# —— 编辑器缓存 ——
*.swp
*.swo
*~
.#*
\#*#
```

---

### 场景专属规则速查

#### 📝 写作 / 文档 / 博客

```gitignore
# 编辑器临时文件
*.bak
*.tmp
~$*.docx
~$*.xlsx
~$*.pptx

# 本地导出（渲染产物，不需要提交）
_site/          # Jekyll / Hugo 构建输出
public/         # Hugo public 目录（视情况）
_book/          # GitBook
.cache/

# 私人草稿（如有分区）
drafts/private/
*.private.md
```

#### 🔬 数据分析 / 机器学习 / 科研

```gitignore
# 大型数据文件（建议用 DVC 或 Git LFS 管理）
*.csv
*.tsv
*.parquet
*.feather
*.h5
*.hdf5
*.pkl
*.pickle
data/raw/
data/processed/

# Jupyter
.ipynb_checkpoints/

# Python 环境
__pycache__/
*.py[cod]
.venv/
venv/

# R
.Rhistory
.RData
.Rproj.user/

# MATLAB
*.asv
*.mex*

# 模型权重（体积大，通常不提交）
*.pt
*.pth
*.ckpt
*.safetensors
models/weights/

# 实验日志
mlruns/
wandb/
runs/
```

#### 🎨 设计 / 创意资产

```gitignore
# 中间产物草稿
exports/drafts/
*-draft.*
*-wip.*
*-old.*

# Adobe 临时文件
*-recovery.*
Adobe\ Premiere\ Pro\ Auto-Save/
Adobe\ After\ Effects\ Auto-Save/

# 字体（许可问题，通常不提交）
*.ttf
*.otf
*.woff
*.woff2
# 如需提交字体，明确排除: !fonts/project-font.ttf
```

#### 🧠 知识管理（Obsidian / Logseq / Org-mode）

```gitignore
# Obsidian
.obsidian/workspace
.obsidian/workspace.json
.obsidian/cache
.trash/

# Logseq
logseq/.recycle
logseq/bak/

# Org-mode
*.org_archive
.org-id-locations

# 同步工具冲突文件
*\ (conflict\ copy\ *).md
*.sync-conflict-*

# 私人笔记分区
private/
_private/
personal/
```

#### 🏗️ 运维 / 基础设施 / DevOps

```gitignore
# Terraform
.terraform/
*.tfstate
*.tfstate.backup
*.tfvars
crash.log

# Ansible
*.retry
vault_password_file

# 通用密钥 / 凭证
*.pem
*.key
*.p12
secrets/
credentials/
.secrets

# 本地覆盖配置
*.local.yaml
*.local.yml
docker-compose.override.yml
```

#### 🎮 游戏开发

```gitignore
# Unity
[Ll]ibrary/
[Tt]emp/
[Oo]bj/
[Bb]uilds/
[Ll]ogs/
[Uu]ser[Ss]ettings/

# Unreal Engine
Binaries/
DerivedDataCache/
Intermediate/
Saved/

# Godot
.import/
export.cfg
export_credentials
```

#### 📊 个人 / 业务记录（财务、合同、报表）

```gitignore
# Office 临时锁定文件
~$*.xlsx
~$*.docx
~$*.pptx

# 含敏感信息的本地副本
*-confidential.*
*-private.*
*_internal.*

# PDF 导出（若原始文件已追踪，导出可忽略）
exports/
rendered/
```

#### 💻 软件开发（按语言细分）

```gitignore
# Node.js / TypeScript
node_modules/
dist/
build/
.next/
.nuxt/
.cache/
*.tsbuildinfo
npm-debug.log*

# Python
__pycache__/
*.py[cod]
.venv/
venv/
*.egg-info/
.pytest_cache/

# Go
/bin/
*.test
vendor/

# Rust
/target/

# Java / Kotlin
*.class
target/
build/
.gradle/

# 通用环境配置
.env
.env.local
!.env.example
```

---

## Step 4：处理现有 .gitignore

- **已有**：对比缺失规则，以 diff 形式展示补充建议，询问是否合并
- **无**：直接生成完整文件

---

## Step 5：输出与确认

1. 展示生成内容，说明各区块来源与理由
2. 主动询问：
   - 是否有**含敏感信息**的文件需要额外忽略（密钥、密码、个人数据）？
   - 是否有**体积大**但不需要追踪的文件（数据集、模型、媒体素材）？
   - 是否有**本地专属配置**不应同步给他人？
3. 确认后写入 `<repo_root>/.gitignore`
4. 若有文件已被追踪，提醒：需执行 `git rm --cached <file>` 才能使忽略规则生效

---

## 注意事项

- **不过度忽略**：lock 文件（package-lock.json、yarn.lock）在应用项目中通常应提交
- **大文件用 LFS**：数据集、设计源文件、游戏资产建议用 `git lfs` 而非直接忽略，保留可追踪性
- **分级 .gitignore**：monorepo 或多模块仓库可在子目录放独立 `.gitignore`，规则就近生效
- **团队 vs 个人**：个人编辑器配置可放 `.git/info/exclude`，避免污染团队公共 `.gitignore`
- **已追踪文件**：`.gitignore` 对已追踪文件无效，需先 `git rm --cached <file>`
