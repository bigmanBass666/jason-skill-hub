## 情报扫描报告 | 2026-05-29

### 🔥 紧急情报（14天内新发现的重磅资源）

**1. OpenAI GPT-OSS 系列（开源开放权重模型）— OpenRouter 免费上线**
- 来源：OpenRouter（openai/gpt-oss-120b:free, openai/gpt-oss-20b:free）
- 模型信息：
  - GPT-OSS-120B：120B 参数，Apache 2.0 开源，面向生产级推理和 agent 场景
  - GPT-OSS-20B：21B 参数（MoE，3.6B 活跃），Apache 2.0，面向消费级硬件
- Agent/工具调用能力：**强** — OpenAI 官方明确标注 "strong tool use capabilities"，原生支持 function calling
- 免费/优惠详情：OpenRouter :free 标记，20 RPM / 200 次/天（与其他免费模型共享限制）
- 接入方式：OpenAI 兼容 API，改 base_url 为 `https://openrouter.ai/api/v1`，无需信用卡
- 时效性判断：**[永久]** — Apache 2.0 开源，OpenRouter 免费托管
- 推荐行动：**立即测试 GPT-OSS-120B** — OpenAI 首个开源大模型，agent 能力强，Quality 评分 55（CostGoat），131K 上下文。对 agent 开发者来说这是 5 月最重磅的新增资源

**2. Google Gemma 4 系列（四款新模型）— OpenRouter 免费 + NVIDIA NIM 免费**
- 来源：OpenRouter（google/gemma-4-31b-it:free, google/gemma-4-26b-a4b-it:free）+ NVIDIA NIM
- 模型信息：
  - Gemma 4 31B Dense：262K 上下文，Vision + Tools，Quality 65（CostGoat 免费榜第 3）
  - Gemma 4 26B A4B：MoE 架构（4B 活跃参数），262K 上下文，Vision + Tools
  - 另有 E2B/E4B 轻量版面向端侧部署
  - 2026 年 3 月 31 日发布，Apache 2.0 许可
- Agent/工具调用能力：**中-强** — 支持 function calling，31B 版 Quality 评分仅低于 DeepSeek V4 Flash 和 MiniMax M2.5
- 免费/优惠详情：OpenRouter :free（20 RPM / 200 次/天）；NVIDIA NIM 免费推理（40 RPM）
- 接入方式：OpenAI 兼容 API（OpenRouter/NIM 均可），开源可自部署
- 时效性判断：**[永久]** — Apache 2.0 开源
- 推荐行动：**测试 Gemma 4 31B 用于 agent 工作流** — 基于 Gemini 3 同源研究，Vision+Tools 双能力是免费模型中的稀缺组合

**3. MiniMax M2.7（230B MoE）— NVIDIA NIM 免费推理**
- 来源：NVIDIA NIM（minimaxai/minimax-m2.7）+ OpenRouter
- 模型信息：230B MoE 架构，深度参与自身进化的自演进模型，支持 Agent Teams、动态工具搜索、复杂 Skill 体系
- Agent/工具调用能力：**强** — SWE-Pro 56.22%（匹配 Claude Opus 4.6），专为 agent 场景设计，NIM 上已有 1130 万次使用
- 免费/优惠详情：NVIDIA NIM 免费推理（40 RPM），原生平台 MiniMax API 需付费
- 接入方式：OpenAI 兼容 API，`integrate.api.nvidia.com/v1`，base_url 改为 NIM 即可
- 时效性判断：**[永久]** — 开源开放权重，NIM 长期托管
- 推荐行动：**重点测试** — 对 agent 开发者来说，这是目前 NIM 平台上 agent 能力最强的免费模型。SWE-Pro 分数与 Claude Opus 4.6 持平，且有原生 Agent Teams 支持

**4. 小米 MiMo-V2.5 系列 API 永久降价（最高降幅 99%）**
- 来源：小米技术官方微博 + IT之家 + 多家媒体（2026-05-27 生效）
- 变动详情：
  - 新定价：Input $1/M tokens，Output $3/M tokens，统一价不再区分上下文窗口长度
  - 降幅 57%-99%，缓存命中输入价格降幅最高达 99%
  - 旧用户额度全部重置
  - Token Plan 计费调整后可用 Token 数量提升 5-8 倍
  - 雷军宣布未来三年 AI 投入 600 亿元
- Agent/工具调用能力：**中-强** — ClawEval 64% pass^3，定位 Agent 场景
- 接入方式：OpenAI 兼容 API，国内直连，platform.xiaomimimo.com
- 时效性判断：**[永久]** — 5 月 27 日起永久生效
- 推荐行动：**关注定价变化，适时接入** — 价格已降至极具竞争力的水平，且原生支持 Agent 场景

**5. OpenRouter $113M Series B 融资（2026-05-28）**
- 来源：OpenRouter 官方公告 + TechCrunch + BusinessWire + NYT
- 详情：
  - 融资额：$113M Series B
  - 领投：CapitalG（Alphabet 独立成长基金）
  - 跟投：NVentures（NVIDIA 风投）、ServiceNow、MongoDB、Snowflake、Databricks Ventures、a16z、Menlo Ventures
  - 估值：$1.3B（一年内翻倍以上）
  - 规模：8M+ 开发者，400+ 模型，周 Token 量从 5T 增长至 25T（6 个月 5 倍）
  - 预计年处理量将超过 1 quadrillion tokens
- 平台意义：投资阵容（Google/NVIDIA/ServiceNow/MongoDB/Snowflake/Databricks）表明多模型路由基础设施已成为企业 AI 的核心层
- 推荐行动：**持续关注** — 平台融资后大概率会加速免费模型扩张和企业功能建设

---

### 📡 一般动态（平台变动 + 新模型 + 政策调整）

**新模型上线 OpenRouter 免费层：**
- **NVIDIA Nemotron 3 Super 120B** — 120B 参数 MoE（12B 活跃），Mamba-Transformer 混合架构，1M 上下文，专为协作 Agent 和高吞吐工作负载优化。Quality 60，Popularity #12，支持 Tools。注意：NIM 上该模型仅付费端点可用（Bitdeer/CoreWeave $0.20/$0.80/M tokens），OpenRouter 是目前唯一免费通道
- **Poolside Laguna 系列（XS.2 + M.1）** — 专注 agentic coding 的新模型。Laguna M.1 是旗舰编码 agent 模型，XS.2 是高效版（33B，fp8 量化）。两者均支持 tool calling + reasoning，262K 上下文。免费 on OpenRouter
- **Qwen3 Next 80B A3B Instruct** — Qwen 新一代模型，262K 上下文，支持 Tools，免费 on OpenRouter
- **LiquidAI LFM 2.5 1.2B Thinking** — 小型推理模型（1.2B 参数），33K 上下文，支持 Reasoning 能力。极轻量，适合端侧推理场景
- **Google Lyria 3 Pro Preview / Lyria 3 Clip Preview** — Google DeepMind 音乐生成模型首次登陆 OpenRouter，1M 上下文。免费 on OpenRouter（非 agent 相关，但对多模态开发者有价值）
- **Kimi K2.6 (moonshotai)** — Moonshot AI 的最新模型，262K 上下文，支持 Vision + Tools，免费 on OpenRouter

**NVIDIA NIM 平台更新（截至 2026-05-13）：**
- 免费模型总数扩展至 **46 个**（来自 12 个发布者）
- **Mistral Nemotron** — Mistral + NVIDIA 联合优化，专为 agent workflow、function calling、instruction following 设计，NIM 上 760 万次使用。被称为"最佳 function calling 模型之一"
- **Mistral Large 3 675B** — MoE 架构（41B 活跃），256K 上下文，通用推理 + 代码，NIM 免费
- **Llama 4 Maverick** — Meta 多模态模型，NIM 上最受欢迎（2200 万次使用）
- **Step-3.5 Flash** — Stepfun 200B MoE 推理引擎，专为 agentic AI 设计，1120 万次使用
- **Seed-OSS 36B（字节跳动）** — 新上线 NIM
- 部分模型出现 deprecation notice：Kimi K2 Instruct、Kimi K2 Thinking、GLM-4.7、Gemma 3 27B

**OpenRouter 5 月平台功能更新：**
- **Human-in-the-Loop Tools for Agent SDK**（5/8）— 新增 HITL 工具类型，agent 可自动处理常规调用并在高风险操作时暂停等待人工确认
- **Consistent Web Search and Fetch**（5/7）— 所有模型统一支持 web search 和 fetch 能力
- **New Audio APIs**（5/1）— 语音和转录 API
- **Response Caching**（4/30）— 相同请求零成本缓存

**免费层收缩：**
- OpenRouter :free 模型数量：~30 个（4/26 CostGoat 统计）至 **27 个**（5/28 统计），持续收缩趋势
- GPT-5.5 价格上调（5/4 公告）

**政策收紧：**
- NVIDIA NIM 多个模型出现 deprecation notice（Kimi K2 系列、GLM-4.7、Gemma 3 27B），免费模型库非静态
- GitHub Copilot 6/1 起全面转向使用量计费（基线已记录，临近生效）

**生态动态：**
- 支付宝推出 Token Pay，MiniMax、阶跃星辰官宣合作 — 支持 AI 开发者全球订阅、Claw 端内一键充 Token
- 雷军宣布小米未来三年 AI 投入 600 亿元

---

### 📊 已知资源状态快照

| 平台 | 状态 | 备注 |
|------|------|------|
| OpenRouter | ✅ 融资后扩张期 | $1.3B 估值，27 个免费模型，新增 GPT-OSS/Gemma 4/Laguna 等 |
| NVIDIA NIM | ✅ 免费层扩张 | 46 个免费模型，MiniMax M2.7 agent 能力最强，部分旧模型 deprecation |
| 小米 MiMo | ✅ 永久降价 | API 最高降幅 99%，Orbit 活动已收官，V2.5 开源 MIT |
| 阿里云百炼 | ✅ | 7000 万+ Token 新人（90 天），无新变化 |
| 硅基流动 | ✅ | 200+ 开源模型免费推理，无新变化 |
| ChatAnywhere | ⚠️ | 依赖上游，上游变动直接影响可用性，无新验证 |
| Google Gemini | ✅ | 1500 次/天，Gemma 4 开源免费新增 |
| Groq | ✅ | 30-60 RPM 免费，无新变化 |
| 火山引擎豆包 | ✅ | 每日免费，无新变化 |
| Cloudflare Workers AI | ✅ | 100+ 模型，AI Gateway，无新变化 |

---

### 🎯 Agent 开发者重点关注

基于你做 agent 开发、关注 function calling 的需求，本次扫描的核心推荐排序：

1. **MiniMax M2.7（NIM 免费）** — SWE-Pro 56.22% 匹配 Claude Opus 4.6，原生 Agent Teams 支持，是目前免费可用的 agent 能力最强模型
2. **Mistral Nemotron（NIM 免费）** — 专为 function calling + agent workflow 设计，被称为"最佳 function calling 模型之一"
3. **OpenAI GPT-OSS-120B（OpenRouter 免费）** — OpenAI 首个开源大模型，强 tool use 支持，Apache 2.0
4. **Nemotron 3 Super 120B（OpenRouter 免费）** — 120B MoE（12B 活跃），1M 上下文，专为协作 agent 优化。NIM 上仅付费端点
5. **Qwen3 Coder 480B（OpenRouter 免费 + NIM 免费）** — 最强免费编程模型，256K/1M 上下文，function calling 强
6. **Poolside Laguna M.1（OpenRouter 免费）** — 旗舰编码 agent 模型，tool calling + reasoning

**最佳接入策略：** 同时注册 NVIDIA NIM + OpenRouter 两个平台，NIM 用于 MiniMax M2.7 和 Mistral Nemotron（agent 最强），OpenRouter 用于 GPT-OSS-120B 和 Nemotron 3 Super 120B（NIM 上没有免费端点的模型）。两个平台都是 OpenAI 兼容 API，改 base_url 和 key 即可切换。
