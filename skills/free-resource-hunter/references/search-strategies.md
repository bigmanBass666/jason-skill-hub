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
| **平台活动页/推广页** | 很多平台会以独立域名做免费活动（如 `100t.xiaomimimo.com`），这些信息在常规搜索中很难被发现。**必须巡查基线中各平台的官网首页和活动页。** |
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

**两条路径必须同时执行。** 路径 A 发现"有人在讨论的新东西"，路径 B 发现"没人注意到的新东西"。两者互补，才能最大化时效性。

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
├─ web-reader OpenRouter 模型列表
├─ web-reader NVIDIA NIM 模型列表
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
