## 资源搜索报告 | 2026-05-29

**搜索主题**：免费代码生成模型 API，要求 agent/function calling 能力强
**用户现状**：目前只用过 NVIDIA NIM（100+ 模型，仅 Step 3.5 Flash 稳定，agent 工作流表现差）
**核心逻辑**：模型越强 → agent 工作出错率越低 → 实际 token 消耗越少 → "贵"的免费模型反而更省钱

---

### 🔥 紧急情报（14天内新发现的重磅资源）

**1. DeepSeek V4 Flash — 当前 OpenRouter 免费模型中质量最高（Quality 77），agent 能力强**
- 来源：OpenRouter（`deepseek/deepseek-v4-flash:free`）
- 模型信息：DeepSeek V4 系列轻量版，1M 上下文，支持 thinking/non-thinking 模式
- Agent/工具调用能力：**强** — BFCL v3 得分 ~84.6%，原生 function calling 支持，多轮并行工具调用可靠
- 免费详情：OpenRouter 免费（`:free` 后缀），20 请求/分钟，200 请求/天，无需信用卡
- 接入方式：OpenAI 兼容，`base_url=https://openrouter.ai/api/v1`
- 时效性判断：**永久免费层**（OpenRouter 持续提供 :free 变体，但具体模型可能随时更替）
- 推荐行动：**立即试用** — 这是你当前 agent 工作流中 NVIDIA NIM Step 3.5 Flash 的直接升级替代
- 价格参考：付费 V4-Flash 仅 $0.14/$0.28 per M（in/out），免费额度用完后极低成本兜底

**2. Qwen3 Coder 480B A35B — OpenRouter 免费最强编程专用模型，专为 agentic coding 优化**
- 来源：OpenRouter（`qwen/qwen3-coder:free`）
- 模型信息：480B 总参/35B 活跃参数 MoE，专为代码生成和 agentic 任务优化，1M 上下文
- Agent/工具调用能力：**强** — 原生支持 function calling、tool use、长上下文仓库级推理
- 免费详情：OpenRouter 免费，同上速率限制
- 接入方式：OpenAI 兼容，`base_url=https://openrouter.ai/api/v1`
- 时效性判断：**永久免费层**
- 推荐行动：**立即试用** — 与 DeepSeek V4 Flash 并列首选，一个偏通用推理，一个偏代码专精

**3. Qwen 3.6 Plus — OpenRouter 免费，1M 上下文，强制思维链推理**
- 来源：OpenRouter（`qwen/qwen3.6-plus:free`）
- 模型信息：Qwen 3.6 系列旗舰，1M 上下文，强制思维链推理 + 工具调用
- Agent/工具调用能力：**中强** — 支持 function calling + `preserve_thinking` 参数查看推理过程，对调试 agent 工作流很有价值
- 免费详情：OpenRouter 免费（`qwen/qwen3.6-plus:free`），~20 请求/分钟
- 接入方式：OpenAI 兼容
- 时效性判断：**永久免费层**
- 推荐行动：**值得试用** — 思维链推理对 agent 决策质量有帮助

**4. Kimi K2.6 — OpenRouter 免费，SWE-bench 80.2%，长时 agent 自主运行能力突出**
- 来源：OpenRouter（`moonshotai/kimi-k2.6:free`）
- 模型信息：~1T MoE，256K 上下文，SWE-bench Verified 80.2%（与 Claude Sonnet 4.6 的 79.6% 持平甚至略高）
- Agent/工具调用能力：**强** — 社区实测 12+ 小时自主运行、4000+ 工具调用的成功案例；Agent Swarm 模式
- 免费详情：OpenRouter 免费，支持 vision + tools
- 接入方式：OpenAI 兼容
- 时效性判断：**永久免费层**
- 推荐行动：**值得试用** — agent 自主运行时间是独特卖点

**5. OpenAI GPT-OSS 120B / 20B — OpenRouter 免费新模型，OpenAI 开源**
- 来源：OpenRouter（`openai/gpt-oss-120b:free`、`openai/gpt-oss-20b:free`）
- 模型信息：OpenAI 开源模型，131K 上下文，支持 tools
- Agent/工具调用能力：**待验证** — Quality 55（120B）/ 41（20B），OpenAI 出品理论上 tool use 训练充分
- 免费详情：OpenRouter 免费
- 时效性判断：**永久免费层**
- 推荐行动：**持续关注** — 质量分数中等，但 OpenAI 开源模型值得关注

**6. Google Gemma 4 31B — OpenRouter 免费，支持 vision + tools**
- 来源：OpenRouter（`google/gemma-4-31b-it:free`）
- 模型信息：262K 上下文，支持视觉和工具调用
- Agent/工具调用能力：**中等** — Quality 65
- 免费详情：OpenRouter 免费
- 推荐行动：**可以试用** — 质量中等，但免费多模态是亮点

---

### 📡 一般动态（平台变动 + 基线遗漏补充）

**OpenRouter 免费模型数量变化**
- 当前 27 个免费模型（CostGoat 5/28 统计），较基线的 ~30 个略有下降
- 新增重要免费模型：DeepSeek V4 Flash、Qwen 3.6 Plus、Qwen3 Coder、Gemma 4 系列、GPT-OSS 系列、MiniMax M2.5、Kimi K2.6
- 速率限制调整为 20 请求/分钟 + 200 请求/天（此前为 50 次/天）

**DeepSeek V4 Pro 定价永久下调**
- 2026-05-22 确认 $0.435/$0.87 per M 为永久价格（原为 75% 限时折扣）
- 新用户注册可获 $1 试用额度（约 700 万 input tokens）
- V4-Pro agent 能力强：多轮并行工具调用可靠，Anthropic 兼容 API 可直接用于 Claude Code

**OpenAI 开源模型上线 OpenRouter**
- GPT-OSS 120B 和 GPT-OSS 20B 免费可用，OpenAI 首次在 OpenRouter 提供免费开源模型

**硅基流动 SiliconCloud 免费层持续更新**
- 200+ 开源模型免费推理（Qwen/GLM/DeepSeek 系列），国内直连，延迟低
- 已知资源，未有重大变化

---

### 📊 已知资源状态快照（基线已有，按 agent 能力排序）

| 平台 | Agent 能力 | 免费政策 | 稳定性 | 你的适用性 |
|------|-----------|---------|--------|-----------|
| NVIDIA NIM（你正在用） | Step 3.5 Flash **弱** | 40 RPM 免费 | Step 稳定，其他不稳定 | 已知 — agent 工作流瓶颈 |
| OpenRouter（27 免费模型） | V4 Flash / Qwen3 Coder **强** | 20 RPM + 200 次/天 | 较高 | **首选补充/替代** |
| 小米 MiMo Orbit | MiMo-V2.5 **中强** | 百万亿 Token 申请制（截止 5/28） | 中 | ⚠️ 活动今天截止！ |
| 阿里云百炼 | Qwen 系列 **中** | 7000 万 Token 新人 90 天 | 高 | 国内直连备选 |
| 硅基流动 SiliconCloud | 开源模型 **中** | 永久免费层 | 中高 | 国内直连备选 |
| DeepSeek 官方 | V4-Pro **强** | 新用户 $1 试用 | 高 | 兜底方案，极低成本 |
| Google Gemini | Flash **中** | 1500 次/天 | 高 | 需梯子 |
| Groq | 开源模型 **视模型** | 30-60 RPM | 高 | 需梯子 |

---

### 💡 针对你的使用建议

你目前只用 NVIDIA NIM，Step 3.5 Flash 稳定但 agent 能力弱。**OpenRouter 的免费 DeepSeek V4 Flash 和 Qwen3 Coder 是最值得立即试用的替代**：

1. **DeepSeek V4 Flash（:free）** — agent 能力 BFCL 84.6%，比 NIM 上任何模型都强一个量级，且 1M 上下文
2. **Qwen3 Coder（:free）** — 专为 agentic coding 设计，480B MoE 参数，function calling 原生优化
3. **Kimi K2.6（:free）** — 12+ 小时自主 agent 运行记录，适合长时间编码任务

三个都走 OpenAI 兼容 API，切换成本极低。建议用 DeepSeek V4 Flash 做主力，Qwen3 Coder 做代码任务主力，二者互补。

如果免费额度不够用（200 次/天），DeepSeek V4 Pro 付费也只要 $0.435/$0.87 per M — 几乎等于免费。
