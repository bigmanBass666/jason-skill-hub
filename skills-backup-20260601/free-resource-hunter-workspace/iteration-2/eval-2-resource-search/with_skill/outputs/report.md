## 资源搜索报告 | 2026-05-29

**搜索目标**: 免费代码生成模型 API，agent 能力强
**用户背景**: 当前仅用 NVIDIA NIM，日消耗 1-2 亿 tokens，付费方案不可承受

---

### 核心发现

**一句话结论**: 免费 + 强 agent + 你的吞吐量，三者无法同时满足。现有免费方案中，agent 能力最强的（Gemini 2.5 Flash）吞吐量不够，吞吐量最大的（NVIDIA NIM）agent 能力弱。需要组合使用，并接受工具调用在部分免费模型上不稳定。

---

### 重点推荐（按 agent 能力排序）

#### 1. Google Gemini 2.5 Flash -- 免费层 agent 能力最强

- **来源**: Google AI Studio (ai.google.dev)
- **模型信息**: Gemini 2.5 Flash, frontier 级别, 1M 上下文
- **Agent/工具调用能力**: **强** -- 原生 function calling, JSON mode, code execution, Google Search grounding
- **免费额度**:
  - 1,500 请求/天, 15 RPM, 1M TPM
  - Gemini 2.5 Flash-Lite: 1,500 请求/天, 30 RPM（RPM 更高，适合突发）
  - Gemini 2.5 Pro: 仅 50 请求/天（基本只是试用）
  - 永久免费，无过期，无需信用卡
- **接入方式**: Google SDK / REST API, 非 OpenAI 兼容格式（需适配）
- **国内访问**: **需梯子**，这是最大障碍
- **数据隐私**: 免费层 Google 可用你的 prompt 训练模型（付费层不会）
- **编码基准**: AkitaOnRails 基准中 Gemini 3.1 Pro 得 82/100 Tier A；2.5 Flash 预期 Tier B+
- **日吞吐量**: 按平均 5K tokens/请求算，约 750 万 tokens/天。**远不够你的 1-2 亿**
- **时效性判断**: 永久免费层
- **推荐行动**: 如果有梯子，作为 agent 工作流的主力测试模型。吞吐量不够日常用，但 agent 可靠性最高

#### 2. OpenRouter DeepSeek V4 Flash (free) -- 免费代码推理最强

- **来源**: OpenRouter (openrouter.ai)
- **模型信息**: 284B MoE, 13B 激活, 1M 上下文
- **Agent/工具调用能力**: **中上** -- 支持 tool calling, CostGoat 质量评分 77（免费模型中最高）, AkitaOnRails 编码基准 78/100 Tier B
- **免费额度**:
  - 未充值: **50 请求/天**, 20 请求/分钟
  - 充值 $10 后: **1,000 请求/天**, 20 请求/分钟
  - 50 请求/天 = 按 5K tokens/请求 = 约 25 万 tokens/天，杯水车薪
  - 1,000 请求/天 = 约 500 万 tokens/天，仍然远不够
- **OpenRouter 免费模型区分**: 所有 :free 模型共享同一个请求配额（50 或 1000/天），不是每个模型独立配额
- **接入方式**: OpenAI 兼容, base_url: openrouter.ai/api/v1, model: deepseek/deepseek-v4-flash:free
- **国内访问**: 可直连
- **时效性判断**: 免费模型，但可能随时调整（OpenRouter 历史上有免费模型下线或转付费的先例）
- **推荐行动**: 充 $10 解锁 1000 请求/天，作为编码 agent 测试和轻度使用

#### 3. OpenRouter Qwen3 Coder 480B (free) -- 专为编码 agent 设计

- **来源**: OpenRouter (openrouter.ai)
- **模型信息**: 480B MoE, 35B 激活 (8/160 experts), 1M 上下文, MIT 开源
- **Agent/工具调用能力**: **理论强，实际不稳定** -- 官方优化了 function calling, tool use, 长上下文仓库推理。但已知 bug: 在 OpenRouter 免费层上 tool calling 可能报错 "No endpoints found that support tool use"
- **免费额度**: 与 DeepSeek V4 Flash 共享 OpenRouter 的 50/1000 请求/天配额
- **CostGoat 质量评分**: 41（低于 DeepSeek V4 Flash 的 77，说明社区反馈质量有差距）
- **接入方式**: OpenAI 兼容, model: qwen/qwen3-coder:free
- **编码基准**: 未在 AkitaOnRails 基准中单独测试。其衍生 Qwen 3.6 Plus 得 71/100 Tier B
- **时效性判断**: 永久免费模型
- **推荐行动**: 值得测试，但 tool calling 稳定性是硬伤。如果稳定后是编码场景的顶级免费选择

#### 4. OpenRouter 其他支持 tool calling 的免费模型

| 模型 | 质量评分 | 上下文 | 特点 |
|------|---------|--------|------|
| MiniMax M2.5 (free) | 70 | 262K | 支持 tool calling, 国产 |
| GPT-OSS 120B (free) | 55 | 131K | OpenAI 开源, 支持 tool calling |
| Kimi K2.6 (free) | -- | 262K | 视觉+工具调用, AkitaOnRails 87/100 Tier A |
| Nemotron 3 Super 120B (free) | 60 | 1M | NVIDIA, 支持 tool calling |
| GLM-4.5 Air (free) | 38 | 131K | 智谱 AI, 支持 tool calling |

**注意**: 以上所有 :free 模型共享同一个请求配额池。

---

### 其他可选方案

#### 5. DeepSeek 官方 API -- 一次性赠送，付费极便宜

- **免费额度**: 新用户 500 万 tokens（一次性，30 天有效）
- **速率限制**: 60 RPM，无日总量限制
- **模型**: V4 Pro (1.6T MoE, 49B 激活) -- **编码 agent SOTA**, AkitaOnRails 89/100 Tier A（通过 DeepClaude）; V4 Flash (284B, 13B 激活)
- **Agent 能力**: **强** -- V4 Pro 在 agentic coding 基准中为开源 SOTA, SWE-bench 80.6%, LiveCodeBench 93.5
- **国内访问**: 直连
- **API 格式**: OpenAI 兼容
- **关键信息**: 500 万 tokens 按你的消耗量不到 1 小时就用完。但 V4 付费价格极低（$0.27/M input, $1.10/M output），1 亿 tokens/天约 $68/天 = $2,040/月。对你的吞吐量来说仍然不便宜
- **推荐行动**: 注册领 500 万免费 tokens 测试 V4 Pro 的 agent 能力，作为质量基准

#### 6. Cerebras -- 最慷慨日吞吐量

- **免费额度**: **100 万 tokens/天**, 30 RPM, 60K-100K TPM
- **模型**: Llama 3.1 8B, GPT-OSS 120B（模型少，无专门编码模型）
- **上下文限制**: 免费层 **8,192 tokens**（重大限制，agent 工作流基本不可用）
- **编码/Agent 能力**: **弱** -- 通用模型，无编码优化，8K 上下文无法跑 agent
- **国内访问**: 可直连
- **推荐行动**: 不适合你的编码 agent 需求。但 1M tokens/天 + 极快推理速度适合非 agent 场景的高吞吐任务

#### 7. 硅基流动 SiliconCloud -- 国内直连，月度免费

- **免费模型**: Qwen2.5-72B (200 万 tokens/月), DeepSeek-V3 (100 万 tokens/月), GLM-4-9B (500 万 tokens/月), CodeLlama-34B (100 万 tokens/月)
- **Agent 能力**: Qwen2.5-72B 中等，CodeLlama 代码专用但 agent 弱
- **国内访问**: 直连，延迟低
- **API 格式**: OpenAI 兼容
- **日吞吐量**: 最高约 16 万 tokens/天（200 万/30 天），远远不够
- **推荐行动**: 作为国内直连备用通道，吞吐量太低无法当主力

#### 8. 火山引擎豆包 -- 国内平台，新用户赠送

- **免费额度**: 每款豆包模型 50 万 tokens，企业用户可申请 500 万
- **边缘大模型网关**: 豆包 1.6 系列可申请 1000 万 tokens
- **国内访问**: 直连
- **API 格式**: OpenAI 兼容
- **推荐行动**: 额度太低，不值得作为主力。可以注册领一下额度备用

---

### 你已经在用的资源状态

| 平台 | 当前状态 | Agent 能力 | 你的吞吐量适配 |
|------|---------|-----------|--------------|
| NVIDIA NIM | 40 RPM, 无日总量上限, 100+ 模型 | 仅 Step 3.5 Flash 稳定但 agent 弱 | **唯一能承载你吞吐量的免费方案** |

---

### 对比总结

| 方案 | Agent 能力 | 日吞吐量上限 | 国内直连 | 推荐度 |
|------|-----------|------------|---------|--------|
| **Google Gemini 2.5 Flash** | **强** | ~750 万 tokens | 需梯子 | 编码 agent 首选（如有梯子） |
| **OpenRouter DS V4 Flash** | 中上 | ~500 万 tokens（充 $10） | 直连 | 性价比最高的免费编码模型 |
| **OpenRouter Qwen3 Coder** | 理论强/实际不稳定 | 共享配额 | 直连 | 值得关注，tool calling 待稳定 |
| **DeepSeek V4 Pro（官方）** | **最强** | 500 万一次性 | 直连 | 质量基准，付费极便宜 |
| **NVIDIA NIM（已在用）** | 弱 | 无上限 | 需特殊方式 | 吞吐量唯一解 |
| **Cerebras** | 弱 | 100 万/天 | 直连 | 8K 上下文不适合 agent |
| **硅基流动** | 中 | ~16 万/天 | 直连 | 备用通道 |
| **火山引擎豆包** | 弱 | ~50 万一次性 | 直连 | 不推荐 |

---

### 推荐行动（按优先级）

1. **注册 Google AI Studio**（如有梯子）-- Gemini 2.5 Flash 免费 1500 请求/天，agent/function calling 最可靠，是测试编码 agent 工作流质量的最佳免费选择
2. **OpenRouter 充 $10** -- 解锁 1000 请求/天，在 DeepSeek V4 Flash (78/100 Tier B) 和 Qwen3 Coder 之间切换测试。$10 是一次性投入，之后所有 :free 模型共享这个配额
3. **注册 DeepSeek 官方 API** -- 领 500 万免费 tokens 测试 V4 Pro（89/100 Tier A），确认 agent 能力上限。如果满意，V4 付费价格是同级别最低
4. **NVIDIA NIM 继续当吞吐量兜底** -- 40 RPM 无总量上限，虽然 agent 弱但吞吐量无可替代

**残酷现实**: 1-2 亿 tokens/天的吞吐量，没有任何免费方案能满足 + agent 强的组合。NVIDIA NIM（agent 弱但吞吐量无限）+ Google Gemini（agent 强但吞吐量有限）的组合是最现实的免费方案。如果 agent 质量是硬需求，DeepSeek V4 Pro 付费（$0.27/M input）是质量/价格最优解。

---

### 新发现 vs 基线对比

| 变化类型 | 内容 | 基线状态 |
|---------|------|---------|
| 模型确认 | OpenRouter 当前 27 个免费模型（5/28 CostGoat 统计），较基线的 ~30 有小幅下降 | 基线记录 ~30 个 |
| 新模型 | MiniMax M2.5 (free) -- 支持 tool calling, 质量评分 70 | 基线未收录 |
| 新模型 | GPT-OSS 120B (free) -- OpenAI 开源模型在 OpenRouter 免费 | 基线未收录 |
| 新模型 | Qwen3 Next 80B (free) -- Qwen 新架构免费上线 | 基线未收录 |
| 平台更新 | Cerebras 免费层确认 100 万 tokens/天，但 8K 上下文限制 | 基线仅记录 "30 RPM 免费" |
| 平台更新 | DeepSeek 官方确认 500 万 tokens 一次性赠送（30 天有效），非每日 | 基线记录 "新用户 500 万 Token" 未说明是一次性 |
| 编码基准 | DeepSeek V4 Pro 89/100 Tier A（通过 DeepClaude），V4 Flash 78/100 Tier B | 基线未收录具体分数 |
| 编码基准 | Kimi K2.6 87/100 Tier A -- 免费模型中编码能力意外强 | 基线记录 "agent 能力未知" |
| OpenRouter 细节 | $10 充值可将免费模型限额从 50 提升到 1000 请求/天 | 基线记录 "50 次/天" 未提及 $10 解锁 |
| 已知问题 | OpenRouter 免费层 tool calling 已知 bug: "No endpoints found that support tool use" | 基线未收录 |

---

*搜索覆盖: 6 轮多源搜索 + 5 个详情页验证 + 1 份编码基准报告交叉参考*
*数据时效: 2026-05-29, 部分平台数据来自 2026-04/05 的第三方实测*
