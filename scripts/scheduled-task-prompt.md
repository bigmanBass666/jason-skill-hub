执行 free-resource-hunter（开发者免费资源情报雷达）的情报扫描工作流。

## 读取参考文档

并行读取：
1. 基线（通过 GitHub MCP get_file_contents）：仓库 `bigmanBass666/skill-baselines`（branch: main），路径 `free-resource-hunter/resource-database.json`
2. 搜索策略：https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/free-resource-hunter/references/search-strategies.md
3. 输出格式：https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/free-resource-hunter/references/push-format.md
4. 完整工作流和评估框架：https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/free-resource-hunter/SKILL.md

**CDN 缓存**：在所有 CDN URL 末尾加 `?t=当前时间戳`（用命令获取），强制获取最新版本。

读取后，严格按照 SKILL.md 中的工作流 1（情报扫描）执行全部步骤。

## 关键规则

- **时间**：用 `TZ=Asia/Shanghai date` 获取中国时区（UTC+8）时间，标题和所有时间标注都用北京时间
- **格式**：严格按 push-format.md 的标准 Markdown 格式输出，每段之间必须有空行
- **评估优先级**：Agent/工具调用能力 > 推理质量 > 免费额度大小
- **日吞吐量**：重点标注 tokens/day，区分同一平台不同模型的额度差异
- **验证规则**：无法通过搜索验证的信息标注"⚠️ 未验证"；来源可疑标注"⚠️ 来源可信度低"；能力声明无 benchmark 支持标注"⚠️ 缺乏依据"
- **增量对比**：只报告与基线的差异，不重复已知信息
- **基线回写**：通过 GitHub MCP create_or_update_file（需先获取 sha）

输出偏好：直接显示结果，不需要保存到文件。
