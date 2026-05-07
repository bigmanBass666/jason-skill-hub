# 搜索与情报策略

本文件定义了情报雷达的搜索策略。核心目标：**发现别人没注意到的变化，且第一时间发现。**

## 目录

- [情报扫描关键词](#情报扫描关键词)
- [信息源优先级](#信息源优先级)
- [增量对比搜索策略](#增量对比搜索策略)
- [资源搜索关键词](#资源搜索关键词)
- [搜索流程](#搜索流程)
- [验证清单](#验证清单)

---

## 情报扫描关键词

这些关键词用于"工作流 1：情报扫描"。目标是发现**最近几天到几周内**的新变化。

### 新模型/新平台上线

```
英文:
- "new free AI model API" site:reddit.com
- "new model added" (OpenRouter OR "NVIDIA NIM" OR Groq OR "Together AI" OR "Fireworks")
- "quietly launched" OR "secretly released" AI model free
- "just added" OR "new on" site:openrouter.ai
- "free model" "just released" OR "launched" 2026
- "anonymous model" OR "unnamed model" OR "mystery model" free API
- "sneaked" OR "quietly" "free API" model
- "hunter" model free API
- "secretly testing" AI model free
- "unannounced" model API free

中文:
- "新上线 免费 模型 API"
- "偷偷上线 免费 大模型"
- "新增模型" (OpenRouter OR "NVIDIA NIM" OR 硅基流动)
- "限时免费 大模型 2026"
- "免费 API 新模型 上线"
- "匿名模型 免费 测试"
- "悄悄上线 免费 API"
- "偷偷放出 免费 模型"
```

### Token 赠送 / 激励计划 / 大规模免费活动

> **关键盲区修复**：这类活动往往不走"新模型上线"或"免费API"的常规路径，而是以独立活动页面的形式出现（如 `100t.xiaomimimo.com`），关键词也完全不同。漏掉一次可能错过几十万亿 Token 的免费额度。

```
中文:
- "百万亿" OR "100T" OR "千亿" Token 免费
- "激励计划" 大模型 OR AI OR Token
- "Token 赠送" OR "赠送 Token" OR "发放 Token"
- "Credits 发放" OR "免费 Credits" AI
- "创造者计划" 免费 AI OR 大模型
- "限时发放" Token OR 额度 大模型
- "开放平台" 注册送 OR 免费送 Token

英文:
- "100T tokens" OR "trillion tokens" free AI
- "token giveaway" OR "free credits" AI API 2026
- "creator incentive" program AI free tokens
- "free token" distribution AI model 2026
- "developer program" free tokens API
- "token grant" OR "credits grant" AI

特定平台搜索（基线中的平台要巡查其官网/活动页）:
- site:xiaomimimo.com OR "小米 MiMo" 激励 OR 赠送 OR 免费
- site:openrouter.ai/blog giveaway OR credits OR free
- site:bailian.console.aliyun.com 赠送 OR 活动
- site:cloud.siliconflow.cn 活动 OR 赠送
- "智谱" OR "Zhipu" 激励计划 OR 赠送 Token
- "DeepSeek" 赠送 OR 免费 额度 活动
```

### 免费额度变动

```
英文:
- "free tier" (changed OR updated OR reduced OR increased OR "cut" OR "scrapped") 2026
- "pricing update" free AI API
- "no longer free" OR "removed free tier" OR "ended free"
- "expanded free tier" OR "increased free"
- "free tier ending" OR "free tier expiring"
- "paywall" free AI API

中文:
- "免费额度 调整 2026"
- "缩水" 免费 API
- "取消免费" OR "不再免费"
- "免费层 变更"
- "限时优惠" 大模型 API
- "收费" 以前免费 模型 API
```

### 平台动态

```
英文:
- site:openrouter.ai/blog OR site:openrouter.ai/announcements
- site:blog.nvidia.com NIM free models
- site:groq.com blog OR changelog
- "NVIDIA NIM" new models 2026
- "ChatAnywhere" update OR new model

中文:
- "阿里云百炼" 新模型 OR 新增
- "硅基流动" 新上线
- "火山引擎" 豆包 更新
- site:v2ex.com 免费大模型
- site:zhihu.com 免费 API 汇总 2026
```

### 🔥 重点追踪平台：NVIDIA NIM 模型上新

> **用户核心需求**：NVIDIA NIM 是用户的主力平台（157+ 模型免费），NIM 上新模型是最有价值的情报之一。当第三方模型（如 Kimi K2.6、DeepSeek V4、Claude 等）出现在 NVIDIA NIM 上，意味着多了一个免费推理渠道，这类情报有时效性（匿名模型可能随时撤下），发现后应立即通知用户。

> **⚠️ 关键认知（eval #6 实验证实）**：公开 API 端点 `integrate.api.nvidia.com/v1/models` 返回 136 个模型，但**所有模型的 `created` 字段都是相同的批处理时间戳（735790403 ≈ 2023年6月）**，完全没有日期区分度。这意味着无法区分「上架 9 个月的 GPT-OSS」和「上架 5 天的 kimi-k2.6」。**发现新上架模型依赖方法 4**（Playwright 按 recent 排序爬取 SPA 页面），因为只有 SPA 页面通过 `span[aria-label]` 元素显示每个模型的真实上架日期（如「May 1, 2026」）。

**方案分层设计**：本 skill 提供 5 层 NVIDIA 追踪方案（方法 1-4 + 4-B），按环境能力自动选择：

| 层级 | 方案 | 适用环境 | 核心能力 | **能否发现新模型** |
|------|------|---------|----------|---------------|
| **方法 4** | **Playwright SPA 爬虫（recent 排序）** | **有 shell + Playwright** | **157+ 模型 + 真实上架日期 + 翻页 + 排序** | **✅ 唯一可靠方式** |
| 方法 2 | web-search 时效补盲 | 所有环境（零依赖） | 搜索社区讨论、官方公告 | ⚠️ 依赖社区讨论时效 |
| 方法 3 | SPA 页面信息抽取（兜底） | 所有环境（零依赖） | 搜索片段提取 | ⚠️ 不可靠 |
| 方法 1 | 公开 API 端点直采 | 有 page_reader 的环境 | 136 模型列表，created 全相同 | ❌ **不能判断新模型（仅做总量统计）** |

方法 2-3 零依赖即可运行，保证基础可移植性，但发现新模型的能力有限。方法 4 是给能装软件的云端 Agent 准备的**首选方案**——有 Playwright 却不用方法 4 的话，会漏掉所有 SPA 独有的 21+ 个模型（157+ vs 136），且无法获取任何上架日期。

> **Eval #6 教训**：方法 1 返回的 136 个模型中，`openai/gpt-oss-120b` 已上架 9 个月、`z-ai/glm5` 已上架数月、`meta/llama-4-maverick` 已上架 9 个月。如果仅用方法 1 做增量对比，会把这些老模型全部错误标记为「🔥 新发现」。**方法 1 的 `created` 字段全部是 `735790403`，完全不具备日期区分能力。**

---

**方法 1（辅助）：公开 API 端点 — `integrate.api.nvidia.com/v1/models`**

> **⚠️ 重要定位**：此方法**仅用于总量统计和交叉验证**，不能单独用于发现新模型。返回的模型列表没有日期/排序信息。

NVIDIA 提供了一个可直接获取模型列表的 JSON API 端点：

- **端点**: `https://integrate.api.nvidia.com/v1/models`
- **格式**: OpenAI 兼容 JSON，`{"object": "list", "data": [{"id": "org/model", "owned_by": "org", ...}]}`
- **公开无 key**: 直接用 page_reader 访问即可，返回 136 个模型
- **完全可移植**: 无需任何认证、无需浏览器、无需本地依赖
- **字段说明**: `data[].id` = 完整模型 ID（如 `moonshotai/kimi-k2-instruct-0905`），`data[].owned_by` = 模型提供商
- **致命缺陷**: `data[].created` 字段所有模型返回相同的值 `735790403`（≈2023年6月的批处理时间戳），**无法用于判断模型上架时间**

**正确使用方式**：
1. 用 page_reader 读取上述端点，解析 JSON 中的 `data[].id` 列表
2. **统计模型总数**（如 136 个），与上次扫描的模型总数对比
3. 如果总数增加（如从 136 → 150），说明有新模型上架（但无法知道具体哪些是新的）
4. 如果同时有方法 4 的 SPA 爬取结果，可以用 API 返回的模型 ID 与 SPA 的模型 ID 做交叉验证（SPA 有 157+ 个，API 有 136 个，差异 = SPA 独有的模型）
5. **永远不要**用 `data[].created` 字段判断新模型（所有值都是 `735790403`）

**❌ 错误使用方式**：
- 将 API 返回的模型与基线逐条对比，把基线中没有的模型全部标记为「新发现」——API 没有有意义的日期信息，无法区分「上架 9 个月的 GPT-OSS」和「上架 5 天的 kimi-k2.6」
- 使用 `data[].created` 字段排序或筛选新模型——所有模型的 `created` 值都是 `735790403`，完全相同
- 将方法 1 单独作为新模型发现手段——这是不可能完成的任务

---

**方法 2（补盲）：web-search 时效搜索 — 捕捉公开 API 未覆盖的新模型**

公开端点可能有 1-7 天的延迟（新模型先对认证用户开放，后加入公开列表）。web-search 是唯一可靠的补盲手段：

```
核心搜索（每次扫描必搜）：
- "NVIDIA NIM" "added" OR "now available" OR "just added" model 2026
- "build.nvidia.com" (Kimi OR "DeepSeek" OR Claude OR "Gemma" OR Qwen OR "Llama") NIM
- site:reddit.com/r/LocalLLaMA "NVIDIA NIM" model 2026
- site:reddit.com/r/LocalLLaMA "build.nvidia.com" new
- "NVIDIA NIM" new model API 2026
- "integrate.api.nvidia.com" new model

中文搜索：
- "NVIDIA NIM" 新模型 上线 2026
- "NVIDIA" 新增 模型 免费 API
- site:v2ex.com "NVIDIA NIM" 新模型
- site:zhihu.com "NVIDIA NIM" 模型 更新

第三方追踪（发现别人整理的 NIM 模型列表）：
- "NVIDIA NIM" available models list 2026
- "NVIDIA NIM" free models complete list
- "build.nvidia.com" models API list
```

**补盲逻辑**：如果 web-search 发现了某个模型在 build.nvidia.com 上线，但公开 API 端点中没有该模型 ID，仍然将其标记为 🔥 新发现——这说明它是刚上架的，尚未进入公开 API 列表。

---

**方法 3（兜底）：SPA 页面信息抽取**

如果方法 1 和方法 2 都失败，尝试：
- 搜索 `site:build.nvidia.com "new" OR "available now"` 从搜索片段提取模型名
- 搜索 CostGoat 或其他第三方统计网站的 NVIDIA NIM 模型列表
- 访问 NVIDIA 官方 blog（blog.nvidia.com）搜索 NIM 新模型公告

---

**方法 4（核心）：Playwright SPA 爬虫（recent 排序）— 发现新模型的唯一可靠方式**

> **前置条件**：运行环境可以 `pip install` 和安装 Chromium 浏览器（如云端 Agent、CI/CD、Docker 容器等）。
> **核心能力**：`build.nvidia.com/models` 默认按 `dateCreated:DESC` 排序（Most Recent），每个模型通过 `span[aria-label]` 显示真实上架日期（如「May 1, 2026」）。
> **为什么这是唯一可靠方式**：公开 API 端点（方法 1）返回的模型 `created` 字段全部是 `735790403`，完全无法判断上架时间。SPA 页面按 recent 排序后，第一个模型就是最新上架的，日期从 DOM 的 `span[aria-label]` 元素中提取。

**方案概述**：访问 `build.nvidia.com/models`（默认已是 Most Recent 排序），逐页爬取所有模型卡片信息。
- 真正渲染 build.nvidia.com 的 SPA 页面，获取完整模型卡片信息（名称、厂商、标签、分类、调用量、**发布日期**）
- `build.nvidia.com/models` 默认按 `dateCreated:DESC` 排序，无需手动选择排序
- 支持多页翻页（最多 10 页，每页 24 个模型，共 157+ 个模型）
- 自动从 `span[aria-label]` 提取每个模型的绝对上架日期（如「May 1, 2026」）
- 自动分类模型类型（文本/图像/Embedding）
- 自动关闭 Cookie 弹窗
- 如有 API key，额外调用认证 API 获取完整模型 ID 映射表

**一键安装依赖 + 运行**：
```bash
pip install playwright httpx openai pyyaml
playwright install chromium
python scripts/scrape_nvidia_nim.py --sort recent --output nvidia_models.json
```

脚本位于 `scripts/scrape_nvidia_nim.py`，是一个完整的可执行 Python 脚本，支持以下参数：
- `--sort recent|popular` — 排序方式（默认 recent）
- `--limit N` — 最多爬取数量（默认 200）
- `--output FILE` — 输出文件路径（默认 nvidia_models.json）
- `--no-browser` — 仅用公开 API 模式（无日期信息，仅做总量统计）
- `--days-recent N` — 判定"最近上架"的天数阈值（默认 14）

输出 JSON 包含 `models[]` 数组，每个模型有 `published_at`（绝对日期）、`date_info.is_recent`（是否14天内上架）、`type`（模型类型）等字段，可直接用于增量对比。

> 完整实现见 `scripts/scrape_nvidia_nim.py`（362 行 Python，含类型分类、日期解析、API 交叉验证）。关键实现细节：从 `span[aria-label]` 提取绝对上架日期（如 "May 1, 2026"），备选从卡片文本提取相对时间（如 "5d"），自动关闭 Cookie 弹窗，最多翻 10 页。

**方法 4 与方法 1-3 的关系**：
- 方法 4 **独立运行**，不依赖 page_reader 或 web-search
- 输出格式包含模型 ID + **published_at**（绝对上架日期）+ **relative_date**（相对时间），可直接用于判断新模型
- **方法 4 的排序结果就是"新模型"的权威来源**：排序后前几个就是最新上架的
- 如果环境支持方法 4，优先执行方法 4（排序结果就是新模型的权威来源），方法 2 作为额外补盲
- 方法 1 的 API 返回（136 个模型）可作为交叉验证：比较 SPA 的 157+ 个模型与 API 的 136 个，差异 = 仅 SPA 可见的模型
- 方法 4 的输出可直接回写到 `resource-database.md`，更新「已知可用模型」表

---

**方法 4-B（替代）：agent-browser 无头浏览器方案 — 有 agent-browser skill 但无 shell 的 AI Agent 使用**

> **前置条件**：AI Agent 有 `agent-browser` skill 可用，但没有 shell 能力（无法 `pip install` 或运行 Python 脚本）。
> **核心能力**：通过 agent-browser 的 `open` + `eval` 命令渲染 `build.nvidia.com/models` 并从 DOM 提取模型信息。
> **与方法 4 的区别**：不需要 Python/Playwright，但依赖宿主环境提供 agent-browser 工具。爬取范围有限（单页约 24 个模型），但足以覆盖最新上架的模型。

**执行步骤**：

```bash
# 步骤 1：打开 NVIDIA 模型页面（默认 Most Recent 排序）
agent-browser open "https://build.nvidia.com/models"

# 步骤 2：等待页面加载完成
agent-browser wait 5000

# 步骤 3：关闭 Cookie 弹窗（如果存在）
agent-browser eval "const b=document.querySelector('#onetrust-accept-btn-handler')||document.querySelector('#onetrust-reject-all-handler');if(b)b.click();document.querySelector('#onetrust-banner-sdk')&&(document.querySelector('#onetrust-banner-sdk').style.display='none')"

# 步骤 4：提取第一页模型卡片信息（模型ID + 上架日期）
agent-browser eval "JSON.stringify([...document.querySelectorAll('[data-testid=nv-card-root]')].map(c=>{const l=c.querySelector('a[data-nvtrack-nav-object=artifact-card]');const h=l?l.getAttribute('href'):'';const spans=[...c.querySelectorAll('span[aria-label]')];const date=spans.map(s=>s.getAttribute('aria-label')).find(a=>/(?:January|February|March|April|May|June|July|August|September|October|November|December)\\s+\\d{1,2},?\\s+\\d{4}/.test(a));const name=c.querySelector('h1,h2,h3,h4,h5')?.textContent?.trim()||'';return{id:h?h.replace(/^\//,''):'',name:name,date:date||null}}))"

# 步骤 5（可选）：翻页获取更多模型
agent-browser click "button[aria-label='Go to next page']"
agent-browser wait 3000
agent-browser eval "..."  # 同步骤 4 的 eval 命令
```

**输出格式**：`[{"id": "moonshotai/kimi-k2-6", "name": "Kimi K2.6", "date": "May 1, 2026"}, ...]`

**局限性**：
- 单页只能获取约 24 个模型（取决于页面分页设置）
- 每次翻页需要额外的 open/eval 操作，效率低于方法 4 的 Playwright 脚本
- 依赖宿主环境的 agent-browser 实现（部分环境可能不支持 `eval` 命令）

**适用场景**：
- 有 agent-browser skill 的 AI Agent（如 Super Z、Cursor 等集成了浏览器工具的 AI）
- 无法安装 Python/Playwright 的受限环境
- 快速检查最近上架的 1-2 页模型（发现最新上架的 20-50 个模型已足够）

---

**环境能力自动路由（Agent 必读）**

> 本节定义 AI Agent 如何自动判断自己的环境能力并选择合适的 NVIDIA 追踪方案。
> **完整检测流程见 SKILL.md 第 0.5 步。** 以下补充各等级的运行时策略和降级规则。

**五个环境等级及对应策略**：

**等级 4：满血环境**（有 shell + Playwright + NVIDIA_API_KEY）
- 首选：方法 4（Playwright SPA 爬虫 recent 排序 + 认证 API ID 映射），预计覆盖 157+ 模型 + 真实上架日期
- 辅助：方法 2（4 组 web-search 补盲）+ 方法 1（公开 API 端点作为交叉验证，`created` 字段无用）
- 方法 3 不执行（不需要）
- 预计耗时：30-60 秒（Playwright 爬取 + API 映射）

**等级 3：增强环境**（有 shell + Playwright，无 API key）
- 首选：方法 4-P（Playwright SPA 爬虫 recent 排序 + `span[aria-label]` 日期提取，无认证 API 调用），157+ 模型 + 真实上架日期
- 辅助：方法 2（4 组 web-search 补盲）+ 方法 1（公开 API 端点作为交叉验证）
- 方法 3 不执行
- 预计耗时：30-60 秒

**等级 2-B：浏览器替代环境**（有 agent-browser，无 shell/Playwright）
- 首选：方法 4-B（agent-browser 渲染 SPA + eval 提取模型 ID 和日期），单页约 24 个最新模型 + 真实上架日期
- 辅助：方法 2（4 组 web-search 补盲）
- 方法 1 可选（如果同时有 page_reader）
- 方法 3 不执行
- ⚠️ 本等级只能获取前 1-2 页的模型（约 24-48 个），但已足够发现最新上架的模型
- 预计耗时：20-40 秒

**等级 2：标准环境**（有 page_reader，无 shell/Playwright/agent-browser）
- 首选：方法 2（web-search 补盲，**至少 6 组**搜索，这是发现新模型的主要手段）
- 辅助：方法 1（page_reader 读公开 API 端点，**仅做总量统计**，`created` 字段全部是 `735790403`，不能判断新模型）
- 兜底：方法 3（如果搜索无结果）
- ⚠️ 本等级**无法可靠判断哪些模型是新上架的**，只能依赖社区讨论和搜索线索推断
- 预计耗时：20-40 秒

**等级 1：受限环境**（仅 web-search，无 page_reader 无 shell 无 agent-browser）
- 首选：方法 2（web-search，**搜索组数翻倍到至少 6-8 组**）
- 兜底：方法 3（搜索第三方整理的 NIM 模型列表）
- 方法 1 和方法 4/4-B 无法执行
- 预计耗时：20-40 秒（搜索次数多）
- **额外策略**：
  - 搜索包含完整模型列表的页面（博客文章、GitHub 仓库、第三方统计）
  - 关注搜索结果片段（snippet）中的模型名称，即使无法访问页面
  - 对每条搜索结果做更细的交叉验证

**运行时降级规则**（方案执行中途失败时）：

```
等级 4/3 执行中如果 Playwright 失败（浏览器 crash、超时、页面结构变化等）：
→ 如果有 agent-browser，降级到等级 2-B 策略（方法 4-B + 2）
→ 如果没有 agent-browser，降级到等级 2 策略（方法 1 + 2 + 3）
→ 在输出中标注："Playwright 爬取失败，已降级为浏览器替代方案/搜索方案"
→ 不要重试 Playwright（避免浪费时间）

等级 2-B 执行中如果 agent-browser 失败：
→ 降级到等级 2 策略（方法 1 + 2 + 3）
→ 在输出中标注："agent-browser 渲染失败，已降级为搜索方案"

等级 2 执行中如果 page_reader 失败（端点不可达、返回空内容等）：
→ 降级到等级 1 策略（仅 web-search，搜索翻倍）
→ 在输出中标注："公开 API 端点不可达，已降级为搜索方案"

等级 1 执行中如果 web-search 无结果：
→ 尝试换一组关键词再搜 2-3 轮
→ 如果仍然无结果，标注 "NVIDIA NIM 追踪本轮未成功获取数据"
→ 继续执行其他平台的扫描，不要因为一个平台失败就放弃整个工作流
```

**避免事项**（会浪费 token 或产生误导结果）：
- ❌ 不从满血逐级降级尝试（如先试方法 4 失败→再试方法 3→再试方法 2→再试方法 1）——逐级试错会消耗大量 token 在重复操作上。按检测等级直接选方案，失败才降一级即可
- ❌ 不为环境检测花费过多时间（检测总耗时不应超过 10 秒）——用户关心的是情报结果，不是环境探测过程
- ❌ 不因为某个方法失败就跳过 web-search 补盲（方法 2 是所有环境的保底）——社区讨论经常能发现 SPA 页面还没更新的最新变动

---

**NVIDIA 模型分类关键词**（从 llm-api-tester 项目提取，用于从 API 返回的模型 ID 中快速分类）

```
文本模型类别关键词（出现即为文本模型）：
text-generation, chat, coding, reasoning, language generation,
instruction following, long-context, agentic, tool calling, moe

排除非文本模型的关键词（出现则非文本模型）：
whisper, flux, parakeet, stable-diffusion, nemoretriever, esm2,
nvclip, nemotron-parse, riva-translate, magpie-tts, genmol,
proteinmpnn, rfdiffusion, shieldgemma, nemoguard, cosmos-,
nv-grounding, starcoder2, openfold, llama-nemotron-embed,
nv-embed, nemotron-asr, nemotron-ocr, nemotron-table,
nemotron-page, nemotron-graphic, parakeet-ctc,
synthetic-video, active-speaker, relighting, lipsync,
embedding, extraction, speech, asr, tts, vision-language

图像模型类别关键词：
image-generation, text-to-image, image-gen
flux, stable-diffusion, sdxl, dall-e, imagen, cogview
```

**验证新模型的**：Agent/工具调用能力、稳定性、速率限制（40 RPM）、是否在免费额度内

---

## 信息源优先级

### 第一梯队：情报最快的地方（每次扫描都搜）

| 信息源 | 为什么快 | 搜索方式 |
|--------|---------|---------|
| **Reddit r/LocalLLaMA** | 全球最大开源 LLM 社区，新模型首发地，社区讨论最快 | `site:reddit.com/r/LocalLLaMA` + 关键词 |
| **Reddit r/LLMDevs** | 开发者视角，关注 API 和工具 | `site:reddit.com/r/LLMDevs` + 关键词 |
| **Hacker News** | 技术前沿，Show HN 经常有新项目 | web-search "Hacker News" + 关键词 |
| **Twitter/X** | AI 圈大佬第一时间发动态（Karpathy, Andrej 等） | web-search site:x.com + 关键词 |
| **GitHub Trending/Releases** | 新开源项目、新 release、star 暴增的项目 | web-search "GitHub" + "released" + 关键词 |

### 第二梯队：官方渠道（准确但可能慢半天到几天）

| 信息源 | 内容 | 搜索方式 |
|--------|------|---------|
| OpenRouter blog/announcements | 模型上线下线通知 | `site:openrouter.ai` |
| NVIDIA NIM blog | 新模型上线 | `site:blog.nvidia.com NIM` |
| Groq changelog | 新模型支持 | `site:groq.com` |
| Together AI blog | 新模型和优惠 | `site:together.ai/blog` |
| ChatAnywhere GitHub | 更新日志 | `site:github.com/chatanywhere` |

### 第三梯队：社区聚合（深度但较慢）

| 信息源 | 内容 | 搜索方式 |
|--------|------|---------|
| 知乎 | 中文技术社区讨论 | `site:zhihu.com` + 关键词 |
| V2EX | 中文开发者社区 | `site:v2ex.com` + 关键词 |
| 掘金 | 中文技术文章 | `site:juejin.cn` + 关键词 |
| Medium / Dev.to | 英文技术博客 | web-search + 关键词 |

### 特殊信息源

| 信息源 | 为什么特殊 |
|--------|-----------|
| **平台模型列表页面** | 直接访问 build.nvidia.com/models、openrouter.ai/models 等页面，对比上次扫描的模型列表。**这是发现"悄悄上线但没人讨论"的模型的唯一可靠方式。** |
| **平台活动页/推广页** | 很多平台会以独立域名做免费活动（如 `100t.xiaomimimo.com`），这些信息在常规搜索中很难被发现——漏掉一次可能错过几十万亿 Token。巡查基线中各平台的官网首页和活动页。 |
| **免费额度汇总文章** | 每隔几周就有新的汇总文章（如"2026 年免费 AI API 汇总"），对比旧文章就能发现变动 |
| **API 中转站公告** | ChatAnywhere、DMXAPI 等中转站经常有新模型上线的公告 |

### 平台活动页巡查清单

> 每次扫描时，对基线中的核心平台做一轮活动页巡查。这能发现独立活动页面上线的大规模免费活动。

| 平台 | 官网 | 活动页巡查 URL | 检查什么 |
|------|------|---------------|---------|
| 小米 MiMo | mimo.xiaomi.com | 100t.xiaomimimo.com, platform.xiaomimimo.com | Token 赠送活动、激励计划 |
| OpenRouter | openrouter.ai | openrouter.ai/blog | 免费额度活动、giveaway |
| 阿里云百炼 | bailian.console.aliyun.com | — | 新人活动、Token 赠送 |
| 硅基流动 | cloud.siliconflow.cn | — | 注册活动、免费额度 |
| 智谱 AI | open.bigmodel.cn | — | 激励计划、Token 赠送 |
| DeepSeek | platform.deepseek.com | — | 注册活动、免费额度 |
| 火山引擎 | console.volcengine.com/ark | — | 新人礼包、Token 赠送 |

---

## 增量对比搜索策略

这是情报扫描区别于普通搜索的核心。增量对比有两条路径：

### 路径 A：社区信号 → 验证

```
社区出现讨论（Reddit/Twitter/HN）
→ 搜索该话题，收集线索
→ 用 web-reader 访问官方页面验证
→ 与 resource-database.md 对比
→ 确认为新情报 → 输出
```

**优点**：信息通常经过社区初步筛选，质量较高。
**缺点**：依赖社区讨论，纯悄悄上线的可能遗漏。

### 路径 B：平台直采 → 对比

```
直接访问平台模型列表页面（web-reader）
→ 提取当前模型列表
→ 与 resource-database.md 中的记录对比
→ 发现差异（新增/消失）→ 验证
→ 确认为新情报 → 输出
```

**优点**：能发现社区还没讨论的悄悄变化。
**缺点**：需要解析页面内容，部分平台可能有反爬。

### 组合策略

**两条路径同时执行。** 只跑路径 A 会漏掉没人讨论的悄悄上线（如 NIM 上架 kimi-k2.6），只跑路径 B 会漏掉社区讨论中的限时活动。两者互补才能最大化时效性。

---

## 资源搜索关键词

这些关键词用于"工作流 2：资源搜索"。目标是在用户指定一个方向后，系统性地搜全。

### 按资源类型

#### AI 模型聚合平台（最优先搜这个类型）
```
英文:
- "free AI model API aggregation platform 2026"
- "like NVIDIA NIM" free models API
- "OpenRouter alternatives" free tier 2026
- "free model inference" multiple providers
- "one API key" multiple AI models free
- "AI gateway" free tier models
- "free AI API hub" OR "free AI API marketplace"

中文:
- "免费大模型API聚合平台 2026"
- "类似NVIDIA NIM 免费 多模型"
- "免费API中转站 大模型 2026"
- "一个key调用多个模型 免费"
- "免费AI模型网关"
```

#### 云部署/数据库/工具等其他资源
这部分根据用户具体需求动态搜索，不预设关键词列表。

---

## 搜索流程

### 情报扫描流程（工作流 1）

```
第 0 步：加载基线
└─ 读取 references/resource-database.md，建立已知资源清单

第 1a 步：社区信号搜索（5-8 个搜索）
├─ Reddit r/LocalLLaMA 最新帖 + 时效性关键词
├─ "free AI model" + 时间限定（近 7 天）
├─ "新上线 免费 模型" 中文
├─ Hacker News 新帖
├─ Twitter/X AI 圈动态
└─ GitHub trending/releases

第 1b 步：平台直采
├─ NVIDIA NIM（🔥 最高优先级，5 层方案按环境自动选择）
│   ├─ [云端 Agent] 方法 4：Playwright SPA 爬虫 + 认证 API（157+ 模型，满血）
│   ├─ [所有环境] 方法 1：page_reader 公开 API 端点（136 模型，零依赖）
│   └─ [所有环境] 方法 2：web-search 补盲（捕捉公开 API 延迟覆盖的新模型）
├─ web-reader OpenRouter 模型列表
└─ 其他核心平台（根据 resource-database.md 中的列表）

第 1c 步：官方渠道巡查
├─ 各平台 blog/changelog 搜索
└─ 免费 API 汇总文章

第 2 步：增量对比
├─ 社区信号 vs 基线 → 新情报候选
├─ 平台直采结果 vs 基线 → 新情报候选
├─ 去重合并
└─ 分类（新增/变动/消失/预警）

第 3 步：验证和深挖
├─ 对每条候选用 web-reader 验证
├─ 评估模型质量（agent 能力优先）
└─ 搜索社区反馈

第 4 步：输出情报简报
├─ 按 push-format.md 格式输出
├─ 只输出增量（新变化）
└─ 将新发现回写到 resource-database.md
```

### 资源搜索流程（工作流 2）

```
第 1 步：读取基线
└─ 确认用户已知的资源，避免重复推荐

第 2 步：广度搜索（3-5 轮不同角度）
├─ 平台级资源关键词
├─ 具体需求关键词
└─ 社区推荐和评测

第 3 步：深度验证（访问官方页面）
├─ 确认免费政策和限制
├─ 确认模型列表和 API 格式
└─ 确认国内可访问性

第 4 步：平台级优先过滤
├─ 优先推荐聚合平台
└─ 其次推荐单个 API

第 5 步：模型能力评估
├─ agent/function calling 能力优先
├─ 推理质量其次
└─ 免费额度最后

第 6 步：结构化输出
└─ 按情报简报格式输出
```

---

## 验证清单

对每条情报，用 web-reader 验证后确认：

### 基础验证
- [ ] 信息来源是否可靠
- [ ] 是否真的是"新"的（不是旧新闻被重新发布）
- [ ] 免费还是收费？限制是什么？

### 模型相关验证
- [ ] 模型参数量/类型（MoE? Dense?）
- [ ] agent/function calling 能力（搜索 benchmark 或社区反馈）
- [ ] 推理速度（如果有人测试过的话）
- [ ] API 是否兼容 OpenAI 格式

### 时效性判断
- [ ] 是永久免费、限时免费、还是测试期？
- [ ] 平台历史上是否经常缩水/撤下免费模型？
- [ ] 预计这个资源还能免费多久？

### 可操作性
- [ ] 用户能否直接注册使用？
- [ ] 需要什么条件？（绑卡？邀请码？GitHub 账号？）
- [ ] 国内能否直接访问？
- [ ] 有没有现成的接入教程或 SDK？
