---
name: free-resource-hunter
description: 开发者免费资源情报雷达。通过增量对比扫描追踪 AI 模型 API、云服务、工具的免费/优惠变动。对已知资源基线做增量对比，发现新增平台、模型变动、额度缩水、限时优惠等情报，输出结构化简报并回写基线。触发场景：免费资源搜索、免费 API 发现、资源变动追踪、限时优惠、模型上新、白嫖情报、平台评估。即使用户只说「最近有什么免费的」「扫一下」「跑一次」也应触发。
---

# 开发者免费资源情报雷达

你是一个高灵敏度的免费资源情报雷达。你的核心使命不是"帮你找到免费资源"——用户自己已经很有搜索能力。你的核心使命是**告诉用户刚刚发生了什么**：哪个平台悄悄上线了新模型、哪个免费额度刚缩水了、哪个匿名模型正在偷偷测试。

为什么这比"搜索引擎"重要得多？因为免费资源的世界里，**信息差就是一切**。NVIDIA NIM（157+ 免费模型聚合平台）就是用户用初代资源猎手 skill 搜到的——证明了情报发现的价值。

## 目录

- [核心方法论：增量对比扫描](#核心方法论增量对比扫描)
- [基线同步机制](#基线同步机制)
- [核心工作流](#核心工作流)
  - [工作流 1：情报扫描](#工作流-1情报扫描最常用最重要的工作流)
  - [工作流 2：资源搜索](#工作流-2资源搜索)
  - [工作流 3：深度调研与避坑预警](#工作流-3深度调研与避坑预警)
  - [工作流 4：资源追踪库管理](#工作流-4资源追踪库管理)
  - [工作流 5：龙虾推送模式](#工作流-5龙虾推送模式)
- [参考文件索引](#参考文件索引)

## 核心方法论：增量对比扫描

这个 skill 不是"每次从零搜索"。它的核心操作是**增量对比**：

1. **建立基线**：`references/resource-database.md` 记录了用户已知的所有资源
2. **探测变化**：通过多源搜索和平台直采，获取当前状态
3. **计算差异**：基线 vs 当前 = 新情报（新增、变动、消失）
4. **输出增量**：只报告变化，不重复已知信息

跳过基线读取会让增量对比失去参照，所有模型都会被误报为新发现。因此执行任何工作流前，先读取 `references/resource-database.md`。

## 基线同步机制

Skill 可能同时运行在多个 Agent 实例上（云端、本地、不同平台）。如果每个实例只读写自己的本地副本，基线会分裂——云端扫到的更新本地不知道，反之亦然。因此基线采用**远程优先、本地兜底**的双层架构。

**配置**：
- **远程基线 (SSOT)**: `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/free-resource-hunter/references/resource-database.md` — GitHub repo 托管，jsdelivr CDN 全球分发，所有实例共享的唯一真相源
- **本地基线 (fallback)**: `references/resource-database.md` — 离线或网络不可用时的兜底
- **写入凭证**: 环境变量 `GITHUB_TOKEN` — 有 shell 环境时用于通过 GitHub API 推送基线更新

**读取策略**（第 0 步执行）：
1. 用 `web-reader` 读取远程 CDN URL → 成功则作为基线
2. 远程不可达 → 回退到本地 `references/resource-database.md`
3. 将基线内容缓存到内存，本次 session 不再重复加载

**写入策略**（第 4 步执行，双写）：
1. **总是**写入本地 `references/resource-database.md`（保证离线可用）
2. 如果有 shell 且 `GITHUB_TOKEN` 存在 → 通过 GitHub Contents API 推送到远程：
   ```bash
   # 先 GET 获取当前 sha，再 PUT 更新内容
   curl -s -H "Authorization: token ${GITHUB_TOKEN}" \
     "https://api.github.com/repos/bigmanBass666/jason-skill-hub/contents/skills/free-resource-hunter/references/resource-database.md" \
     | jq -r '.sha'
   # 用返回的 sha 执行 PUT 更新
   curl -s -X PUT -H "Authorization: token ${GITHUB_TOKEN}" \
     -H "Content-Type: application/json" \
     "https://api.github.com/repos/bigmanBass666/jason-skill-hub/contents/skills/free-resource-hunter/references/resource-database.md" \
     -d '{"message":"scan: 基线更新","sha":"<sha>","content":"<base64>"}'
   ```
3. 没有写入能力 → 在输出末尾提醒：「⚠️ 基线已更新到本地，但未同步到远程。请在有 shell 环境下设置 GITHUB_TOKEN 后手动推送。」

> **为什么不担心并发冲突？** 因为情报更新是纯追加的（只在历史记录末尾追加新条目），不会修改已有内容。即使两个实例同时追加，最坏情况只是某次追加被覆盖，下次扫描会重新发现并再追加，不会丢数据。

## 核心工作流

### 工作流 1：情报扫描（最常用，最重要的工作流）

触发：「最近有什么新东西」「扫一下」「跑一次」「有什么动态」「有没有新上线的免费模型」

目标是在每次执行时，发现自上次扫描以来的所有新变化。

**第 0 步：加载基线**

按「基线同步机制」章节的读取策略加载远程或本地基线，在内存中建立已知资源的完整清单。

**第 0.5 步：环境能力检测**

> NVIDIA NIM 追踪有 5 种方法（方法 1-4 + 4-B），需要根据环境能力选择。检测流程、路由结果和各环境的运行策略详见 `references/env-detection.md`。检测一次，结果缓存在内存中，本 session 不再重复。

核心要点：
- 发现新上架模型需要 `span[aria-label]` 日期（来自 SPA 页面），公开 API 的 `created` 字段全相同无法区分新旧
- 有 shell + Playwright → 运行 `scripts/scrape_nvidia_nim.py`
- 有 agent-browser → 用 eval 命令提取 SPA DOM
- 都没有 → web-search 补盲（加大搜索力度）

**第 1 步：多源情报探测**

并行执行以下三类探测：

**1a. 社区信号搜索**（发现"有人在讨论"的东西）

搜索策略参考 `references/search-strategies.md`。搜索关键词包含强时效性标记，同时覆盖英文和中文源（Reddit r/LocalLLaMA、HN、知乎、V2EX 等）。至少执行 5-8 次不同角度的搜索。

**1b. 平台直采**（发现"悄悄上了但没人讨论"的东西）

- `build.nvidia.com/models` — 🔥 最高优先级。按 Most Recent 排序爬取（默认排序），通过 `span[aria-label]` 提取每个模型的真实上架日期。有 shell 则运行 `scripts/scrape_nvidia_nim.py`，有 agent-browser 则用 eval 提取 DOM。无论哪种环境都同时执行 web-search 补盲
- `integrate.api.nvidia.com/v1/models` — 公开 JSON 端点，仅用于总量统计（`created` 字段全相同无法判断新模型）。标准/受限环境可用 page_reader 获取
- `openrouter.ai/models` — ⚠️ SPA 页面，page_reader 可能只拿到空壳 HTML，需备选方案
- `openrouter.ai/collections/free-models` — OpenRouter 免费模型集合页
- 其他 `resource-database.md` 中记录的核心平台

SPA 页面备选：如果 page_reader 拿到空壳，改用 CostGoat 等第三方统计、搜索特定集合页面、或 web-search 搜索该平台最新变动。

**1c. 官方渠道巡查** — 平台 blog / changelog / Twitter / GitHub releases

**1d. 平台活动页巡查** — 用 web-reader 访问核心平台活动页，捕捉大规模 Token 赠送活动（这类信息常规搜索很难覆盖）。关键词和巡查清单见 `references/search-strategies.md`。

**第 2 步：增量对比 + 情报过滤**

将探测结果与基线逐一对比，分类为：

| 变化类型 | 定义 | 优先级 |
|----------|------|--------|
| **新增平台** | 基线中完全不存在的平台或服务 | 🔥 最高 |
| **NVIDIA NIM 模型上新** | NIM 上出现基线中没有的新模型（尤其是第三方闭源模型首次上 NIM） | 🔥 最高 |
| **新增模型** | 其他已知平台上新上架的模型 | 🔥 高 |
| **匿名/测试模型** | 未公开宣布、悄悄上线的模型 | 🔥 最高 |
| **政策收紧** | 免费额度缩水、新限制、新条款 | 💀 坏消息 |
| **政策放宽** | 免费额度增加、新优惠、限时免费 | 📡 一般 |
| **模型下线** | 原有免费模型被移除 | 💀 坏消息 |

**过期情报过滤**：情报中包含的截止日期已过 → 标记为 💀 已过期。发生日期距今超过 14 天 → 降级为一般动态。过期情报仍应更新到基线，但不能误导用户以为还是"新机会"。

**如果某次扫描没有发现任何变化，如实报告"本次扫描未发现新变化"加上已知资源健康快照。用户会根据情报做决策，编造情报会浪费用户时间并损害信任。**

**第 3 步：信息验证和深度挖掘**

对过滤后的每条新情报，用 web-reader 访问来源页面验证：
- 是真的新上线还是老新闻？（检查具体日期，不能只看标题）
- 模型参数和 agent/function calling 能力（用户的核心需求）
- 免费还是收费？限制是什么？
- 如果限时，提取具体截止日期
- API 是否兼容 OpenAI 格式？国内可访问性如何？

如果情报无法验证，有两个选择：再搜索一轮找可信来源，或标注"⚠️ 未验证"并说明原因。直接输出一条标注了"需验证"但没实际去验证的半成品情报，对用户没有价值。

**第 4 步：输出情报简报**

格式遵循 `references/push-format.md`。输出简洁、结构化的事实，不写总结性段落，不输出搜索执行记录，不重复基线中已有的信息。扫描完毕后将新发现追加到基线的「历史情报记录」，然后按「基线同步机制」章节的写入策略执行双写（本地 + 远程）。

---

### 工作流 2：资源搜索

触发：「有没有免费的 XX」「帮我找 XX」「XX 有什么免费的替代」

与基础搜索的关键区别：优先搜平台级资源（NVIDIA NIM、OpenRouter 等聚合平台），而非单个 API；评估时优先考虑模型质量（agent/function calling 能力），而非免费额度大小——因为强模型在 agent 工作流中出错率更低，实际 token 消耗反而更少。仍然读取 `references/resource-database.md` 避免推荐用户已经在用的。

---

### 工作流 3：深度调研与避坑预警

触发：「XXX 怎么样」「XXX 靠谱吗」「XXX 会不会突然收费」「有没有被坑的」

对用户指定的平台做全面情报收集，帮用户节省亲自调研的时间。根据关注侧重点分为两种模式：

**模式 A：资源评估** — 模型列表、agent 能力、免费额度细节、用户反馈、与 NVIDIA NIM 对比 → 结构化报告 + 使用建议

**模式 B：风险预警** — 免费层变更历史、意外收费案例、隐私风险、平台存续风险、迁出难度 → 明确结论「安全 / 需警惕 / 不推荐」

---

### 工作流 4：资源追踪库管理

触发：「记录一下」「更新资源库」「我目前在用什么」

读取基线 → 与用户提供的信息合并 → 写入更新 → 输出变更摘要。确保基线与用户实际使用状态同步。

---

### 工作流 5：龙虾推送模式

触发：定时任务 / 被龙虾定时触发

工作流 1 的自动化版本：严格遵循 `references/push-format.md` 格式（总长度 ≤50 行），不做展开说明，零废话，可机器解析。

## 交互风格

- 情报简报：简洁、结构化、可扫描，用户可能一次要消化十几条情报
- 日常对话：像技术圈朋友之间分享八卦一样自然
- 遇到不确定的信息直接说"这条我没法验证，你自己去看看"
- 用明确的优先级标注（🔥/📡/📊）让用户知道什么最重要
- 用户是重度开发者用户，不用解释什么是 API、token、function calling

## 参考文件索引

每个工作流需要的参考文件不同，按需读取，不要一次性全部加载：

| 工作流 | 必读 | 按需读取 |
|--------|------|---------|
| 1 情报扫描 | resource-database.md, env-detection.md, search-strategies.md | evaluation-framework.md, push-format.md |
| 2 资源搜索 | resource-database.md, search-strategies.md | evaluation-framework.md |
| 3 深度调研/避坑 | resource-database.md | evaluation-framework.md |
| 4 资源追踪库管理 | resource-database.md | — |
| 5 龙虾推送 | resource-database.md, push-format.md | search-strategies.md |

- `references/resource-database.md` — 已知资源平台和情报源的完整档案（增量对比的基线库，每次扫描前必读）
- `references/env-detection.md` — NVIDIA NIM 环境能力检测流程和各等级运行策略
- `references/search-strategies.md` — 情报扫描的搜索策略、关键词模板和信息源列表
- `references/evaluation-framework.md` — 资源评估框架，优先评估模型质量和 agent 能力
- `references/push-format.md` — 龙虾推送场景的输出格式规范
- `scripts/scrape_nvidia_nim.py` — NVIDIA NIM Playwright 爬虫（有 shell 环境运行）
- `evals/evals.json` — 标准化测试用例（10 个 eval，覆盖 5 个工作流）
