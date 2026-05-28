执行 free-resource-hunter（开发者免费资源情报雷达）的情报扫描工作流。

## 第一步：读取基线和参考文档

并行读取以下内容：
1. 基线（私有仓库，通过 GitHub MCP get_file_contents）：
   - 仓库：bigmanBass666/skill-baselines（branch: main）
   - 路径：free-resource-hunter/resource-database.json
2. 搜索策略：https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/free-resource-hunter/references/search-strategies.md
3. 输出格式：https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/free-resource-hunter/references/push-format.md

## 第二步：获取当前时间

用命令获取真实时间（不要自己估算）：
- 标题中的日期格式：MM-DD HH:mm
- 用于判断情报是否在 14 天内、限时优惠是否过期

## 第三步：执行增量对比扫描

并行执行：
- 社区信号搜索（Reddit、Hacker News、Twitter/X、知乎、V2EX、GitHub，5-8 次不同角度）
- 平台直采（OpenRouter、NVIDIA NIM、小米 MiMo 等核心平台的模型列表）
- 官方渠道巡查（各平台 blog/changelog）
- 平台活动页巡查（Token 赠送、激励计划等）

## 第四步：增量对比 + 情报过滤

将搜索结果与基线逐一对比，只报告增量（新变化）：
- 🔥 紧急：14 天内新上线的平台/模型、匿名测试模型、重大政策变更
- 📡 一般：额度微调、基线遗漏补充、一般性更新
- 💀 坏消息：免费取消、模型下线
- ⚠️ 预警：可能缩水、不稳定

过期过滤：
- 超过 14 天的情报降级为"📡 一般"
- 已过期的限时优惠标记为 💀
- 不重复基线中已有的信息

## 第五步：验证

对每条新情报验证：
- 是真的新上线还是老新闻？（检查具体日期）
- Agent/工具调用能力如何？（agent 能力是第一评估维度）
- 免费还是收费？限制是什么？日吞吐量（tokens/day）是多少？
- 同一平台不同模型的额度是否不同？（如 OpenRouter 某些模型 200/天，某些 1000/天）
- 国内可访问性如何？

## 第六步：输出情报简报

使用标准 Markdown 格式（不要用自定义符号如 ├ 或 ━━━）。

格式示例：
```
## 情报扫描报告 | MM-DD HH:mm

### 🔥 紧急情报

**1. [资源名称] — [一句话描述]**

- 来源：[平台]
- 模型信息：[参数量/类型/能力]
- Agent/工具调用能力：[强/中/弱/未知]
- 免费详情：[具体额度，包含 tokens/day 或 requests/day]
- 接入方式：[API格式/链接]
- 时效性：[永久] / [限时(截止MM-DD)] / [测试期]
- 推荐行动：[具体建议]

### 📡 一般动态

- **[平台]** [变动描述] — [影响] [时效性标记]

### 📊 已知资源健康

| 平台 | 状态 | 备注 |
|------|------|------|
| NVIDIA NIM | ✅ | 正常运行 |
```

重要格式规则：
- 每段之间必须用空行分隔（Markdown 渲染依赖空行，不空行会挤成一团）
- 标题用 ## / ###
- 列表用 - 
- 表格用标准 Markdown 表格
- 紧急情报最多 3 条，一般动态最多 10 条
- 总长度 ≤ 50 行
- 绝不含废话，不写"总结""关键结论"
- 如果无新变化：输出"📭 本次扫描未发现新变化" + 健康快照

## 第七步：更新基线

通过 GitHub MCP create_or_update_file 将新发现追加到远程基线（需先通过步骤 1 获取 sha）。

## 输出偏好

直接显示输出结果，不需要保存到文件。
