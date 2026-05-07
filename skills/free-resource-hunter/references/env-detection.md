# 环境能力检测与路由

本文件定义了 NVIDIA NIM 追踪的环境能力检测流程和各等级的运行策略。

## 已验证的事实

- `integrate.api.nvidia.com/v1/models` 返回 136 个模型，但 `created` 字段全部是 `735790403`（≈2023年6月），**无法区分新旧模型**
- `build.nvidia.com/models` 默认按 `dateCreated:DESC` 排序，每个模型通过 `span[aria-label]` 显示真实上架日期
- 因此发现新模型需用方法 4（Playwright）或方法 4-B（agent-browser），方法 1 仅做总量统计（eval #6 实验证实：方法 1 的 `created` 字段全是 `735790403`，会将上架 9 个月的老模型误报为新发现）

## 检测流程

每个 session 只执行一次，结果缓存在内存中，后续不再重复检测。

```
检测 1：我能执行 shell 命令吗？
→ 尝试运行任意一条简单命令（如 echo test 或 dir）
→ 成功 → 我有 shell 能力 → 继续检测 2
→ 失败 → 我没有 shell 能力 → 继续检测 1.5

检测 1.5：我有 agent-browser 工具吗？
→ 检查当前环境是否有 agent-browser / browser automation 工具可用
→ 有 → agent-browser 可用 → 跳到「路由结果」（浏览器替代）
→ 没有 → agent-browser 不可用 → 跳到「路由结果」（受限）

检测 2：Playwright 可用吗？
→ 尝试: python3 -c "from playwright.async_api import async_playwright; print('ok')"
→ 成功 → Playwright 可用 → 继续检测 3
→ 失败 → 尝试安装: pip install playwright httpx openai pyyaml && playwright install chromium
    → 安装成功 → Playwright 可用 → 继续检测 3
    → 安装失败 → Playwright 不可用 → 跳到「路由结果」（标准）

检测 3：我有 NVIDIA_API_KEY 吗？
→ 检查环境变量 NVIDIA_API_KEY 是否存在且非空
→ 有 → 跳到「路由结果」（满血）
→ 没有 → 跳到「路由结果」（增强）
```

## 路由结果

| 检测结果 | 环境等级 | NVIDIA 方案 | 执行动作 |
|----------|---------|-------------|---------|
| 检测3有 key | **满血** | **方法 4 + 2 + 1** | 运行 `scripts/scrape_nvidia_nim.py` + 认证 API 完整映射 + web-search 补盲 |
| 检测3无 key | **增强** | **方法 4-P + 2 + 1** | 运行 `scripts/scrape_nvidia_nim.py` + web-search 补盲 + 公开端点交叉验证 |
| 检测2失败 | **标准** | 方法 2 + 1 + 3 | web-search 补盲为主 + page_reader 公开端点辅助（仅做总量统计） |
| 检测1.5有 agent-browser | **浏览器替代** | **方法 4-B + 2** | agent-browser 渲染 SPA + eval 提取模型ID和日期 + web-search 补盲 |
| 检测1失败且无 agent-browser | **受限** | 方法 2 + 3（加强搜索） | 仅 web-search 补盲（搜索翻倍 6-8 组）+ 第三方列表 |

## 运行时策略

### 满血环境（有 shell + Playwright + NVIDIA_API_KEY）

运行脚本获取完整数据：
```bash
python scripts/scrape_nvidia_nim.py --sort recent --output nvidia_models.json
```
输出 JSON 包含每个模型的 `published_at`（上架日期）和 `date_info.is_recent`（是否14天内上架），可直接用于增量对比。辅助以 4 组 web-search 补盲 + 公开 API 端点交叉验证。

### 增强环境（有 shell + Playwright，无 API key）

同上运行脚本，但无认证 API ID 映射（输出的 `id` 字段来自 SPA 页面 href，格式如 `moonshotai/kimi-k2-6`）。辅助以 4 组 web-search 补盲。

### 浏览器替代环境（有 agent-browser，无 shell）

用 agent-browser 打开 `build.nvidia.com/models`，通过 eval 命令提取模型信息：
```bash
agent-browser open "https://build.nvidia.com/models"
agent-browser eval "JSON.stringify([...document.querySelectorAll('[data-testid=nv-card-root]')].map(c=>{const l=c.querySelector('a[data-nvtrack-nav-object=artifact-card]');const h=l?l.getAttribute('href'):'';const spans=[...c.querySelectorAll('span[aria-label]')];const date=spans.map(s=>s.getAttribute('aria-label')).find(a=>/(?:January|February|March|April|May|June|July|August|September|October|November|December)\\s+\\d{1,2},?\\s+\\d{4}/.test(a));return{id:h?h.replace(/^\//,''):'',date:date||null}}))"
```
单页约 24 个模型，但已足够覆盖最新上架的模型。辅助以 web-search 补盲。

### 标准环境（有 page_reader，无 shell/Playwright/agent-browser）

- web-search 至少 6 组，这是发现新模型的主要手段
- page_reader 读公开 API 端点做总量统计（`created` 字段无用，全相同）
- 搜索第三方整理的 NIM 模型列表作为兜底

### 受限环境（仅 web-search）

- 搜索组数翻倍到至少 6-8 组
- 关注搜索结果片段中的模型名称
- 对每条搜索结果做交叉验证

## 降级规则

方案执行中途失败时才降级，不做逐个试错：

```
等级 4/3 Playwright 失败 → 有 agent-browser 则降级到 2-B，否则降级到 2
等级 2-B agent-browser 失败 → 降级到等级 2
等级 2 page_reader 失败 → 降级到等级 1（仅 web-search，搜索翻倍）
等级 1 web-search 无结果 → 换关键词再搜 2-3 轮，仍无结果则标注本轮未成功
```

降级时在输出中标注降级原因和替代方案。
