# 免费资源情报库

> **重要**：本文件是增量对比的基线库。每次情报扫描前必须读取此文件，扫描结果与本文件对比后的差异即为新情报。
>
> **维护规则**：每次情报扫描后，将新发现追加到"历史情报记录"。定期（每周）验证并更新各平台的"最后验证"时间。
>
> 本库中的信息也可能过时，扫描时应验证后更新，而非直接当作最新信息。

## 目录

- [AI 模型聚合平台（核心关注）](#ai-模型聚合平台核心关注)
- [免费 API 中转站](#免费-api-中转站)
- [单家模型 API](#单家模型-api)
- [其他开发者资源](#其他开发者资源)
- [情报源清单](#情报源清单)
- [历史情报记录](#历史情报记录)

---

## AI 模型聚合平台（核心关注）

这类平台提供多种模型，一个 API key 可调用多个模型。**这是最优先关注的资源类型。**

### NVIDIA NIM
- **URL**: build.nvidia.com
- **模型数量**: 100+
- **免费政策**: 免费，40 RPM 速率限制，无总用量上限；rate limit increase 申请不再获批
- **计费模式**: rate limit 制（原 credit 制已废弃，2026 年变更）
- **API 格式**: OpenAI 兼容
- **国内访问**: 需特殊方式
- **上新频率**: 中
- **风险信号**: Bot farm 滥用严重；有用户报告封号（疑似高频触发）；rate limit increase 官方明确拒绝
- **已知可用模型**:

| 模型 | Agent 能力 | 稳定性 | 速度 | 备注 |
|------|-----------|--------|------|------|
| Step 3.5 Flash | 弱（tool calling 频繁出错） | 高 | 快 | 用户主力模型，唯一稳定的，但 agent 工作流中表现差 |
| DeepSeek V4 Flash | 中 | 低 | 快 | 经常不稳定 |
| GLM 5.1 | 未知 | 低 | — | 不稳定 |
| Kimi K2.6 | 未知 | 低 | — | 不稳定 |
| 其他 70+ 模型 | 不等 | 低 | 不等 | 用户已全部测试，仅 Step 稳定 |

- **最后验证**: 2026-04-30
- **备注**: 用户已测试全部 80+ 模型，仅 Step 3.5 Flash 在高并发下稳定可用。**NVIDIA NIM 本身是此 skill v1 发现的资源。**

### OpenRouter
- **URL**: openrouter.ai
- **模型数量**: 397+
- **免费政策**: ~30 个 :free 模型（2026-04-26 CostGoat 统计，较之前 50+ 有下降），无余额时 50 次/天
- **API 格式**: OpenAI 兼容
- **国内访问**: 可直连
- **上新频率**: 高
- **历史事件**: 偷偷上线 Hunter-alpha 匿名推理模型（后被撤下/改收费）
- **Stealth 匿名模型机制**: OpenRouter 已形成系统化的 Stealth 模型发布机制，累计上线 9 个匿名模型（Cypher/Horizon/Pony/Aurora/Hunter/Healer/Sherlock Think/Sherlock Dash/Elephant Alpha）。最新为 Elephant Alpha（4/13，蚂蚁集团 100B，免费）。通过系统提示词泄露和社区逆向识别来源。
- **平台新功能（2026-04）**: Agent SDK（4/27）、Workspaces（4/24）、Video Generation（4/22）、Auto Exacto 自适应路由（4/15）
- **已知 Stealth 模型**: Elephant Alpha (蚂蚁集团 100B 免费), Sherlock Think Alpha (疑似 xAI Grok, 1.8M 上下文), Sherlock Dash Alpha, Hunter Alpha (在线但状态待确认), Healer Alpha
- **⚠️ 即将下线**: Claude 3.7 Sonnet (2026-05-05)
- **最后验证**: 2026-04-30

### 小米 MiMo
- **URL**: platform.xiaomimimo.com / mimo.xiaomi.com
- **活动页**: 100t.xiaomimimo.com（Orbit 百万亿 Token 计划）
- **模型数量**: MiMo-V2.5 系列（V2.5: 310B/15B 活跃 + V2.5-Pro: 1.02T/42B 活跃 MoE）
- **免费政策**: Orbit 百万亿 Token 激励计划进行中（2026-04-28 ~ 2026-05-28），申请制，最高 16 亿 Credits（¥659），审核宽松；MiMo-V2.5 开源（MIT 协议）
- **API 格式**: OpenAI 兼容（可直接配置到 Claude Code/Cursor/OpenClaw）
- **国内访问**: ✅ 可直连
- **上新频率**: 中（4/28 发布 V2.5 + Orbit 计划）
- **备注**: 小米自研大模型，V2.5 定位 Agent 场景，全模态（文本/图像/视频/音频），1M 上下文，ClawEval 64% pass^3，API 成本比上代降低 50%
- **最后验证**: 2026-04-30
- **⚠️ Orbit 计划**: 活动截止 2026-05-28，赠完即止，需申请

### ChatAnywhere
- **URL**: api.chatanywhere.tech
- **GitHub**: 29.1K star
- **转发模型**: GPT-4o/Claude/DeepSeek/Gemini 等
- **免费政策**: 免费层，GitHub 绑定领 Key
- **API 格式**: OpenAI 兼容
- **国内访问**: 可直连
- **上新频率**: 中
- **风险**: 依赖上游，上游变动直接影响可用性
- **最后验证**: 待验证（2026-04-29 发现）

### 阿里云百炼
- **URL**: bailian.console.aliyun.com
- **模型数量**: 70+（含 DeepSeek/Kimi/GLM/Qwen）
- **免费政策**: 7000 万+ Token 新人（90 天）
- **API 格式**: OpenAI 兼容
- **国内访问**: 可直连
- **上新频率**: 中
- **最后验证**: 2026-04-29

### Puter.js
- **URL**: puter.js
- **模型数量**: 500+
- **免费政策**: 完全免费无限制
- **API 格式**: 前端 JS 调用（非标准 API）
- **国内访问**: 可直连
- **上新频率**: 高
- **限制**: 前端 JS 调用，需包装成后端 API 才能用于 agent 工作流
- **最后验证**: 待验证（2026-04-29 发现）

### 硅基流动 SiliconCloud
- **URL**: cloud.siliconflow.cn / api.siliconflow.cn/v1
- **模型数量**: 200+ 开源优化模型
- **免费政策**: 免费层（Qwen/GLM/DeepSeek 系列等开源模型免费推理）
- **API 格式**: OpenAI 兼容
- **国内访问**: ✅ 可直连，延迟低
- **上新频率**: 中
- **最后验证**: 2026-05-01

### 火山引擎豆包
- **URL**: console.volcengine.com/ark
- **模型数量**: 国内多模型
- **免费政策**: 每日免费
- **API 格式**: OpenAI 兼容
- **国内访问**: 可直连
- **上新频率**: 中
- **最后验证**: 待验证

### Cloudflare Workers AI
- **URL**: developers.cloudflare.com/workers-ai
- **模型数量**: 100+ 开源模型
- **免费政策**: 免费层 + AI Gateway（聚合 14+ provider）
- **API 格式**: REST API
- **国内访问**: 可直连
- **上新频率**: 高
- **最后验证**: 待验证（2026-04-29 发现）

### GitHub Models
- **URL**: github.com/marketplace/models
- **模型数量**: GPT-4o/GPT-4.1/o3 等
- **免费政策**: 50-150 次/天
- **API 格式**: OpenAI 兼容（通过 Azure）
- **国内访问**: 需特殊方式
- **上新频率**: 中
- **最后验证**: 待验证
- **⚠️ Copilot 变更**: 2026-04-27 GitHub 宣布 Copilot 全面转向使用量计费（6/1 生效），免费模型取消。GitHub Models API 是否受影响待确认

### Together AI
- **URL**: together.ai
- **模型数量**: 开源模型
- **免费政策**: 有免费额度
- **国内访问**: 需特殊方式
- **上新频率**: 中
- **最后验证**: 待验证

### Fireworks AI
- **URL**: fireworks.ai
- **模型数量**: 开源模型
- **免费政策**: 有免费额度
- **国内访问**: 需特殊方式
- **上新频率**: 中
- **最后验证**: 待验证

### CrazyRouter（🆕 2026-05-01 发现）
- **URL**: crazyrouter.com
- **模型数量**: 627+ 模型，102 个模型家族，20+ 提供商
- **免费政策**: 注册赠送 $0.20；按量付费（pay-as-you-go），比官方便宜 20-50%
- **API 格式**: OpenAI/Anthropic/Gemini 三种格式原生兼容
- **Agent/工具调用能力**: 支持 function calling + structured output，兼容 Claude Code/Cursor/LangChain/Dify/n8n
- **国内访问**: 待验证（7 个全球边缘节点）
- **上新频率**: 高
- **风险**: 新平台，稳定性待验证；无无限免费额度
- **最后验证**: 2026-05-01

### AIMLAPI.com（🆕 2026-05-01 发现）
- **URL**: api.aimlapi.com
- **模型数量**: 400+（GPT-5, Claude 4, Gemini, DeepSeek, Llama 等）
- **免费政策**: Developer 计划免费（$0）；Startup 计划按量付费无月费
- **API 格式**: OpenAI 兼容
- **Agent/工具调用能力**: 支持 function calling，稳定性待验证
- **国内访问**: 待验证（需梯子可能性高）
- **最后验证**: 2026-05-01

### api-hub.ai（🆕 2026-05-01 发现）
- **URL**: api.api-hub.ai
- **模型数量**: 覆盖 OpenAI/Anthropic/Google/Mistral/DeepSeek/xAI 等主要提供商
- **免费政策**: Starter 免费计划（20 请求/天 + $10 免费额度），0% API 加价
- **API 格式**: OpenAI 兼容
- **国内访问**: 待验证
- **最后验证**: 2026-05-01

### Eden AI（🆕 2026-05-01 发现）
- **URL**: edenai.co
- **模型数量**: 500+ 模型
- **免费政策**: 免费层可用（具体额度待确认）
- **差异化**: 智能路由 + 自动 fallback + 负载均衡
- **API 格式**: 统一 API（非纯 OpenAI 兼容，需适配）
- **国内访问**: 需梯子（法国公司）
- **最后验证**: 2026-05-01

### Groq
- **URL**: groq.com
- **模型数量**: 开源模型
- **免费政策**: 30-60 RPM 免费
- **国内访问**: 需特殊方式
- **上新频率**: 中
- **最后验证**: 待验证

---

## 免费 API 中转站

| 平台 | 转发模型 | 免费方式 | 风险 | 国内访问 | 最后验证 |
|------|---------|---------|------|---------|---------|
| ChatAnywhere | GPT-4o/Claude/DeepSeek/Gemini | GitHub 绑定领 Key | 低（29K star，社区大） | ✅ 直连 | 待验证 |
| api-zh-model | GPT/Claude/DeepSeek | 免费 | 中（稳定性不确定） | 待验证 | 待验证 |
| KKSJ AI | 多模型聚合网关 | 商业 | 低（商业服务） | 待验证 | 待验证 |

---

## 单家模型 API

| 提供商 | 模型 | 免费/优惠 | 国内访问 | Agent 能力 | 备注 |
|--------|------|-----------|---------|-----------|------|
| 智谱 AI | GLM-5.1, GLM-4-Flash | GLM-4-Flash 永久免费不限量 | ✅ 直连 | 4-Flash agent 弱 | 5.1 和 4-Flash 完全不同级别 |
| DeepSeek | V4 Pro, V4 Flash, V3.2 | 新用户 500 万 Token | ✅ 直连 | V4 Pro 较强 | V4 的 agent 能力比 R1 成熟 |
| Google | Gemini 2.5 Flash/Pro | 1500 次/天 | 需梯子 | Flash 中等 | 需梯子但额度慷慨 |
| Cerebras | Llama/Qwen 等 | 30 RPM 免费 | 需梯子 | 视模型 | 速度极快 |
| Hugging Face | 开源模型 | 免费（有排队） | ✅ 直连 | 视模型 | 冷启动延迟 |

---

## 其他开发者资源

| 类型 | 资源 | 免费/优惠 | 备注 |
|------|------|-----------|------|
| 云部署 | Vercel / Cloudflare Pages / Netlify | 免费层 | — |
| 数据库 | Supabase / Neon / Turso | 免费层 | — |
| 存储 | Cloudflare R2 | 10GB 免费 | S3 兼容 |
| GPU | Oracle Cloud (ARM 4核 24GB) | 永久免费 | 无 GPU，可跑量化小模型 |
| GPU | Google Colab / Kaggle | ~45-60h GPU/周 | T4 GPU |
| GPU | AutoDL | ~2.93 元/时 4090 | 秒级计费 |

---

## 情报源清单

### 必检源（每次扫描都查）

| 源 | 检查方式 | 检查什么 |
|----|---------|---------|
| Reddit r/LocalLLaMA | `web-search site:reddit.com/r/LocalLLaMA` | 新模型发布、免费 API 发现、平台动态 |
| Reddit r/LLMDevs | `web-search site:reddit.com/r/LLMDevs` | 开发者视角的新资源 |
| Hacker News | `web-search "Hacker News" free AI` | 新项目、新平台 |
| OpenRouter 模型列表 | `web-reader https://openrouter.ai/models`（⚠️ SPA 页面，page_reader 可能无法获取完整列表；备选：搜索 CostGoat 统计 / 直接用 OpenRouter API） | 新模型上线下线 |
| OpenRouter Stealth 页面 | `web-reader https://openrouter.ai/provider/stealth` | 匿名/测试模型 |
| CostGoat 免费模型统计 | `web-reader https://costgoat.com` 或搜索 | OpenRouter 免费模型数量和列表 |
| NVIDIA NIM 模型列表 | `web-reader https://build.nvidia.com/models` | 新模型上线下线 |
| Twitter/X AI 圈 | `web-search site:x.com free AI model` | AI 圈大佬第一时间动态 |
| 知乎/V2EX | `web-search site:zhihu.com/v2ex.com 免费 API` | 国内资源动态 |

### 周期性检查源（每周一次）

| 源 | 检查什么 |
|----|---------|
| OpenRouter blog | 平台政策变更 |
| NVIDIA blog | 新模型公告 |
| ChatAnywhere GitHub | 新模型/新功能 |
| 各平台 pricing 页面 | 免费额度变更 |
| 免费 API 汇总文章 | 对比上次发现的变动 |

---

## 历史情报记录

> 每次情报扫描后，将新发现追加到这里。格式：日期 + 变化类型 + 具体内容。
> 这是增量对比的核心——下次扫描时，新扫描结果与此记录对比，差异即为新情报。

### 2026-04-29 首次扫描

**新增发现：**
- [新增平台] ChatAnywhere（GitHub 29.1K star）：免费转发 GPT-4o/Claude/DeepSeek，国内直连，支持多 Key 轮询。**待用户验证稳定性。**
- [新增平台] Puter.js：500+ 模型完全免费无限制，前端 JS 调用。**需包装成后端 API 才能用于 agent 工作流。**
- [新增能力] Cloudflare Workers AI Gateway：聚合 14+ provider，边缘推理。**免费层详情待验证。**

**已知状态确认：**
- NVIDIA NIM：80+ 模型免费，但仅 Step 3.5 Flash 在 agent 工作流中稳定
- OpenRouter：50+ 免费 :free 模型，50 次/天（无余额时）
- 阿里云百炼：7000 万+ Token 新人，90 天有效

### 2026-04-30 Eval #2-4 补充扫描

**🆕 新增平台：**
- [新增平台] CrazyRouter（627+ 模型，比官方便宜 20-50%）：注册赠 $0.20，支持 function calling，三格式兼容
- [新增平台] AIMLAPI.com（400+ 模型）：Developer 计划免费
- [新增平台] api-hub.ai（$10 免费额度 + 20 请求/天）：0% API 加价
- [新增平台] Eden AI（500+ 模型）：智能路由 + 自动 fallback

**🔥 OpenRouter 深度侦查发现：**
- [🔥 匿名模型] Elephant Alpha（4/13，蚂蚁集团 Inclusion AI，100B，免费）：最新 Stealth 模型
- [🔥 机制发现] OpenRouter 已形成系统化 Stealth 匿名模型发布机制，累计 9 个匿名模型
- [🔥 知名 Stealth] Sherlock Think/Dash Alpha（疑似 xAI Grok，1.8M 上下文窗口）
- [📡 新模型] Claude Opus 4.7、Kimi K2.6 上线 OpenRouter
- [📡 平台功能] Agent SDK + Workspaces + Video Generation 上线
- [📡 免费变化] :free 模型从 50+ 降至 ~30（CostGoat 4/26 统计）
- [💀 模型下线] Ling-2.6-1T (4/30)、Claude 3.7 Sonnet (5/5 即将下线)

**⚠️ NVIDIA NIM 避坑预警：**
- [⚠️ 计费变更] 从 credit 制改为 rate limit 制（40 RPM），无总用量上限
- [⚠️ 政策收紧] rate limit increase 申请不再获批
- [⚠️ 风险信号] Bot farm 滥用严重；有用户报告封号
- [📊 基线修正] NIM 免费政策从「完全免费，无额度限制」修正为「免费，40 RPM 速率限制」
- [📊 基线修正] 模型数量从 80+ 更新为 100+
- [📊 基线修正] 硅基流动模型数量从「多种」更新为 200+

**🔥 紧急情报：**
- [🔥 新活动] 小米 MiMo Orbit 百万亿 Token 创造者激励计划：30 天内发放 100T Token（2026-04-28 ~ 05-28），申请制，最高 16 亿 Credits（¥659），审核极宽松，OpenAI 兼容 API，国内直连。活动页：100t.xiaomimimo.com
- [🔥 新模型] MiMo-V2.5 系列开源（MIT 协议）：V2.5 (310B/15B) + V2.5-Pro (1.02T/42B MoE)，全模态 1M 上下文，Agent 场景优化（ClawEval 64% pass^3），API 成本降 50%
- [🔥 新模型] NVIDIA Nemotron 3 Nano Omni：多模态（视觉+音频+语言），Agent 子任务最高 9x 效率，NIM 免费推理

**💀 坏消息：**
- [💀 政策收紧] GitHub Copilot 6/1 起全面转向使用量计费，免费模型取消。GitHub Models API 影响待确认

**📡 一般动态：**
- [📡 新模型] OpenRouter 新增 Qwen3 Coder 480B A35B (free)：当前最强免费编程模型，262K 上下文，MoE 架构，function calling 强
- [📡 基线遗漏] Qwen OAuth 免费层已于 2026-04-15 终止

**平台更新：**
- 小米 MiMo：从 V2 升级到 V2.5，新增 Orbit 活动页 100t.xiaomimimo.com，URL 更新为 platform.xiaomimimo.com
- GitHub Models：标注 Copilot 6/1 使用量计费变更风险
- OpenRouter：新增 Qwen3 Coder 480B (free)
