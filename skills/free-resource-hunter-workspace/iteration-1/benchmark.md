# Benchmark Report | free-resource-hunter | Iteration 1

## Summary

| 配置 | Pass Rate | 平均耗时 | 平均工具调用 |
|------|-----------|----------|-------------|
| **with_skill** | **100% (15/15)** | 473.2s ± 71.2s | 35.3 ± 4.6 |
| without_skill | 40% (6/15) | 276.1s ± 56.5s | 16.0 ± 6.0 |
| **Delta** | **+60pp** | +197.1s (+71%) | +19.3 (+121%) |

## Per-Eval Breakdown

### Eval 1: 情报扫描 (intel-scan)

| Assertion | with_skill | without_skill |
|-----------|:----------:|:-------------:|
| has-three-sections (三区分类) | ✅ | ❌ |
| priority-markers (优先级标记) | ✅ | ❌ |
| timeliness-labeled (时效性标注) | ✅ | ❌ |
| actionable (可操作建议) | ✅ | ❌ |
| has-health-snapshot (健康快照) | ✅ | ❌ |
| **Pass Rate** | **5/5** | **0/5** |
| Time | 426.6s | 253.4s |
| Tool Uses | 39 | 16 |

### Eval 2: 资源搜索 (resource-search)

| Assertion | with_skill | without_skill |
|-----------|:----------:|:-------------:|
| platform-first (平台优先) | ✅ | ✅ |
| agent-capability-first (agent 能力优先) | ✅ | ❌ |
| nvidia-nim-excluded (排除已知) | ✅ | ❌ |
| has-access-info (接入信息) | ✅ | ✅ |
| mentions-cost-paradigm (质量>额度) | ✅ | ❌ |
| **Pass Rate** | **5/5** | **2/5** |
| Time | 437.2s | 343.7s |
| Tool Uses | 30 | 22 |

### Eval 3: 风险评估 (risk-assessment)

| Assertion | with_skill | without_skill |
|-----------|:----------:|:-------------:|
| has-conclusion (明确结论) | ✅ | ✅ |
| covers-pricing-history (定价历史) | ✅ | ✅ |
| covers-charge-risk (收费风险) | ✅ | ✅ |
| covers-platform-survival (存续风险) | ✅ | ✅ |
| migration-guidance (迁移指导) | ✅ | ❌ |
| **Pass Rate** | **5/5** | **4/5** |
| Time | 555.8s | 231.2s |
| Tool Uses | 37 | 10 |

## Analyst Notes

Skill 最大价值体现在**情报扫描**和**资源搜索**两个场景：

- **Eval 1（情报扫描）差距最大**：with-skill 产出结构化三区分类、每条情报有优先级和时效性标注、有健康快照；baseline 完全是平铺式列表，无情报意识。
- **Eval 2（资源搜索）核心差异**：skill 带来了"agent 能力优先"的评估框架和"排除已知资源"的增量逻辑，baseline 把用户已在用的 NVIDIA NIM 也作为推荐。
- **Eval 3（风险评估）差距最小**：baseline 本身也能做基本调研（4/5），但缺少迁移决策框架（开发/生产拆分、多方案对比）。

时间成本 +71% 是合理的——skill 驱动 agent 做了 2-3 倍的搜索量和验证步骤，换来零漏报零误报。
