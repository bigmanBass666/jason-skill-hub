## 情报扫描报告 | 2026-05-29

### 🔥 紧急情报（14天内新发现，与 agent/function calling 直接相关）

**1. 天工 SkyClaw-v1.0 — 国产原生 Agent 模型，限时免费试用**
- 来源：昆仑万维天工AI（5/22 上线天工 Skywork 平台）
- 模型信息：专为 Agent 场景原生设计，百万 token 上下文，另有轻量版 SkyClaw-v1.-lite
- Agent/工具调用能力：**强** — 在主流 Agent benchmark 中超越 DeepSeek V4 Flash、Qwen 3.6 系列，逼近 DeepSeek V4 Pro 和 Claude Opus 4.6 水平；深度适配 OpenClaw、Claude Code、Codex 等框架
- 免费/优惠详情：限时免费试用，窗口期 2-4 周；正式定价低于 Minimax 2.7 和 Qwen 3.6 的一半
- 接入方式：OpenAI 兼容接口，可通过天工平台或 APIFree（apifree.ai/model/skywork-ai/skyclaw-v1）调用
- 时效性判断：限时免费（2-4 周窗口，预计 6 月中截止）
- 推荐行动：**立即注册测试** — 这是近期最值得关注的 agent 模型，原生 tool calling 优化，免费窗口有限

**2. Qwen3.7-Max — 阿里云新旗舰，Agent 时代专用模型**
- 来源：阿里云（5/20 发布），OpenRouter 已上架
- 模型信息：Qwen 系列最新旗舰，专为 agent 工作负载设计，长程自主执行能力（数百至数千步骤）
- Agent/工具调用能力：**强** — 官方定位 "The Agent Frontier"，在 coding、办公自动化、自主执行方面全面超越前代
- 免费/优惠详情：阿里云百炼新人 7000 万 Token（90 天）可覆盖；OpenRouter 上为付费模型
- 接入方式：阿里云百炼（bailian.console.aliyun.com）/ OpenRouter（qwen/qwen3.7-max），OpenAI 兼容
- 时效性判断：永久上线
- 推荐行动：**通过阿里云百炼新人额度测试** — function calling 能力是用户核心需求，这个模型值得优先验证

**3. InclusionAI Ring-2.6-1T — 蚂蚁集团 1T 模型，OpenRouter 免费**
- 来源：InclusionAI/蚂蚁集团（5/8 上线 OpenRouter），Hugging Face（5/14）
- 模型信息：1T 参数，262K 上下文窗口，Elephant Alpha 的后续迭代（同一组织）
- Agent/工具调用能力：**待验证** — 模型定位偏向推理，tool calling 能力尚无明确 benchmark 数据
- 免费/优惠详情：OpenRouter :free 标记，完全免费
- 接入方式：OpenRouter（inclusionai/ring-2.6-1t:free），OpenAI 兼容
- 时效性判断：免费模型，可能随时调整
- 推荐行动：**值得测试** — 免费的 1T 参数模型，先试 tool calling 表现再决定是否纳入工作流

### 📡 一般动态（平台变动 + 基线遗漏）

- **Owl Alpha 匿名模型上线 OpenRouter**（~4/28）— 新 Stealth 模型，免费，百万 token 上下文，原生 agent 优化。不在基线已知 Stealth 列表中。[基线遗漏，需验证来源]
- **小米 MiMo V2.5 API 永久降价**（5/27）— 最高降幅 99%，取消长上下文阶梯定价，成为市场上最具性价比的 1M 上下文模型之一。已接入平台的用户直接受益。
- **Gemini 3.5 Flash 发布**（5/19，Google I/O）— Google 最新 Flash 模型，定位越级性能 + 极致速度。是否保留免费层待确认。
- **Gemini Pro 免费层已于 4/1 终止** — 基线中 Google 条目（1500 次/天）已过期，Pro 模型不再免费。Flash 模型可能仍保留免费层。[基线需更新]
- **小米 MiMo Orbit 百万亿 Token 活动已到期**（5/28 截止）— 基线中标注的活动已结束。
- **GitHub Copilot 6/1 全面转向用量计费**（3 天后生效）— 用 AI Credits 替代 premium requests，token 计费。基线已预警，现在是最后窗口。
- **Hunter/Healer Alpha 身份已揭晓** — OpenRouter 3/18 确认为小米 MiMo V2 变体（MiMo-V2-Pro 和 MiMo-V2-Omni）。基线中"未知来源"需更新。
- **OpenRouter 免费模型持续下降** — CostGoat 最新统计 27 个免费模型（基线记录 ~30 个，4/26）。
- **OpenCode Zen 平台**（opencode.ai）— 新增多个免费模型接入：MiMo V2.5、Qwen3.7 Max、Gemini 3.5 Flash、DeepSeek V4 Flash。AI 编程工具新玩家。

### 📊 已知资源状态快照

| 平台 | 状态 | 备注 |
|------|------|------|
| NVIDIA NIM | ✅ | 100+ 模型，40 RPM，Step 3.5 Flash 仍为主力稳定模型 |
| OpenRouter | ✅ | 27 个免费模型（持续下降），新增 Ring-2.6-1T、Owl Alpha |
| 小米 MiMo | ✅ | V2.5 API 永久降价 99%，Orbit 活动已结束 |
| 阿里云百炼 | ✅ | 新增 Qwen3.7-Max，新人 7000 万 Token 仍有效 |
| 硅基流动 | ✅ | 200+ 开源模型免费推理 |
| Google Gemini | ⚠️ | Pro 免费层已终止（4/1），Flash 3.5 新发布，免费层待确认 |
| Groq | ✅ | 30-60 RPM 免费 |
| ChatAnywhere | ✅ | 国内直连，转发 GPT/Claude |

### 💀 已过期情报

- 小米 MiMo Orbit 百万亿 Token 计划（4/28-5/28）— 已于昨日到期
- Gemini Pro API 免费层（1500 次/天）— 已于 4/1 终止

### Agent 开发者专项建议

本次扫描发现 3 个与 agent/function calling 直接相关的重磅新资源：

1. **SkyClaw-v1.0** 是最值得关注的 — 原生 agent 设计，官方 benchmark 逼近 Claude Opus 4.6，限时免费 2-4 周
2. **Qwen3.7-Max** 是阿里云专为 agent 时代打造的旗舰，function calling 是其核心卖点，可通过百炼新人额度免费测试
3. **Ring-2.6-1T** 是免费的 1T 参数大模型，但 tool calling 能力尚未确认，建议先跑一轮 agent 工作流测试

已知平台中，NVIDIA NIM 的 Step 3.5 Flash 仍是唯一在高并发下稳定的免费模型，但 agent 能力弱。如果 SkyClaw 或 Qwen3.7-Max 的 agent 表现经测试确认优秀，可能成为新的主力选择。
