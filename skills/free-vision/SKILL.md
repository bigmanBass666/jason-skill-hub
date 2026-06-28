---
name: free-vision
description: "为无原生视觉能力的模型提供图片处理能力。当 VISION_BLOCK_READ=1（纯文本模型模式）时，通过此 skill 调用多模型后端分析图片。多模态模型直接使用原生视觉，无需调用此 skill。支持文件路径、URL、Playwright 截图等输入，通过 zhipu-4v / zhipu-thinking / stepfun-3.7 等后端完成视觉任务。"
argument-hint: "[image-path-or-url] [optional-prompt]"
allowed-tools: Bash, Read, Write, AskUserQuestion
---

# Vision Arsenal

多模型路由系统，为无原生视觉能力的模型提供图片处理能力。

默认路由使用最稳定的 3 个模型覆盖 95% 场景。
当你判断某个场景需要特定模型时，可以通过 `--backend` 调用扩展组的任何模型。

**决策流程：**

1. 先判断场景（调用脚本之前）：读 `references/routing.md`，根据任务描述判断图片场景
   - 场景明确匹配「复杂图表/数据可视化/数学/科学图像/长上下文推理」 → 直接用 `--backend zhipu-thinking` 或 `--backend stepfun-3.7`，一步到位
   - 场景不明确 → 进入步骤 2
2. 场景不明确时，用默认路由跑一次 Stage 1 快速扫描
3. Stage 1 结果揭示新信息后，立即用 `--backend` 切换到更合适的模型执行 Stage 2 深度分析

## Quick Start

```bash
SCRIPT=$(python3 -c "
import pathlib
base = pathlib.Path.home() / '.agents' / 'skills' / 'free-vision'
s = base / 'scripts' / 'vision_read.py'
if s.exists(): print(s)
" 2>/dev/null)

python "$SCRIPT" "/path/to/image.png"
python "$SCRIPT" -b zhipu-thinking "/path/to/chart.png" "分析数据趋势"
```

## 选模型

读 `references/models.md` 看完整模型表，读 `references/routing.md` 看场景→模型映射和 Two-Stage 流程。

## 稳定性

- **智谱**：永久免费、API 稳定、并发明确。首选。
- **NVIDIA**：免费但不稳定——模型可能随时下线、API 偶发 500 错误。用作扩展，不作为唯一依赖。
- 所有后端均 OpenAI 兼容格式，Bearer token 认证。
- 零依赖，纯 Python 标准库。

## 模型选择

读 `references/models.md` 看参数（TTFT、并发、上下文长度、注意事项）。以下按场景给出质性原则：

| 场景 | 推荐模型 | 理由 |
|---|---|---|
| 日常看图、中文 OCR、截图理解 | `zhipu-4v`（默认） | 最稳定、最快 |
| 复杂图表、数据推理 | `zhipu-thinking` | 内置思维链，适合深度分析 |
| 超大截图(>128K tokens) | `nvidia-maverick` | 1M 上下文窗口 |
| 精细中文描述（美食/Logo/场景质感） | `agnes-2.0-flash`（`--backend agnes`） | 中文质量更高，但不稳定 |
| 复杂推理、长上下文视觉 | `stepfun-3.7` | 256K 上下文 + 推理 + 多模态 Agent |
| 英文快速识别 | `nvidia-phi4` | 最快，不稳定 |
| 视频内容 | `zhipu-46v` | 原生视频支持 |

## Error handling

- 默认路由：逐个尝试默认组模型，首个成功即返回。全部失败则报错退出
- 指定 `--backend`：只尝试该模型，失败直接退出（不 fallback）
- 缺少 API key → 跳过该模型，继续尝试默认组下一个
- 文件不存在 → 立即报错
- 全部失败 → 退出并报告最后一个错误
