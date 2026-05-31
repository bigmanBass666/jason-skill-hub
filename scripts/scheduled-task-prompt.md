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

## 扫描质量底线（不可跳过）

以下三条是情报扫描的时效性保障，**不是可选的**：

1. **发散搜索必做（原则 7）**：除了常规关键词搜索，必须对 3-5 个中文厂商做定向巡查（StepFun、智谱、昆仑、阿里通义、字节 Seed 等），用"厂商名 + 新模型/上线/发布"搜索。因为中国厂商新模型上线时英文社区讨论滞后 1-3 天，常规关键词完全命中不到。（Step 3.7 Flash 教训）

2. **官方渠道必查（第 1c 步）**：每次扫描必须查 NVIDIA developer blog (`site:developer.nvidia.com/blog "NIM"`) 和 HuggingFace releases — NIM 新模型上线几乎一定同步发 HF release，这是早于社区讨论的信息源。SPA 页面直采失败时，用 web-search "site:build.nvidia.com model free endpoint" 替代。

3. **直采失败不跳过**：如果 web-reader 拿到 SPA 空壳，不能标注"直采失败"后就跳过该平台。必须切换到 web-search 搜索该平台的最新变动。直采失败≠没有新模型，只是你暂时拿不到列表。

输出偏好：直接显示结果，不需要保存到文件。
