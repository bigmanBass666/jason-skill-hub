---
name: free-vision
description: "Vision Arsenal — give your text-only model full visual capabilities. MUST use this skill whenever the user asks to look at, describe, analyze, OCR, or understand any image — screenshots, photos, diagrams, charts, UI mockups, error screenshots, generated images, or any visual content. Also trigger when built-in image reading fails, returns errors, or is unavailable. CRITICAL: when MCP tools (Playwright, etc.) return screenshots with [Image] tags, do NOT try to process the image directly — use this skill with the saved file path instead. Even trigger when the user mentions an image without explicitly asking you to read it. Supports local files, URLs, audio files, and video. Auto-routes between stable backends with fallback. Never refuse an image request."
argument-hint: "[image-path-or-url] [optional-prompt]"
allowed-tools: Bash, Read, AskUserQuestion
---

# Vision Arsenal

给纯文本模型 (TLM) 扩展视觉能力的多模型路由系统。相当于用极低成本获得了多模态能力。

## 设计理念

这是一个 **视觉能力军火库**。默认路由使用最稳定的 3 个模型覆盖 95% 场景。
但你（AI）拥有完整的信息——当你判断某个场景需要特定模型时，可以通过 `--backend` 调用扩展组的任何模型。

**你的决策流程应该是：**
1. 先用默认路由（自动切换）处理常规任务
2. 如果你能从任务描述中判断出特殊需求，直接指定最合适的模型
3. 如果第一次扫描的结果揭示了新信息（比如发现是中文文档、复杂图表），可以再用更合适的模型重新分析

## Quick Start

```bash
# 脚本自动定位（支持全局和项目级安装）
SCRIPT=$(python3 -c "
import pathlib
for base in [pathlib.Path.home()/'.claude'/'skills'/'free-vision',
             pathlib.Path('.claude')/'skills'/'free-vision']:
    s = base/'scripts'/'vision_read.py'
    if s.exists(): print(s); exit()
cwd=pathlib.Path.cwd()
for p in [cwd,*cwd.parents]:
    s = p/'.claude'/'skills'/'free-vision'/'scripts'/'vision_read.py'
    if s.exists(): print(s); exit()
" 2>/dev/null)

# 查看默认组模型
python "$SCRIPT" --list

# 查看全部模型（含扩展组）
python "$SCRIPT" --list --extended

# 默认路由（自动选稳定模型）
python "$SCRIPT" "/path/to/image.png"

# 指定模型
python "$SCRIPT" -b zhipu-thinking "/path/to/chart.png" "分析数据趋势"

# 自定义 prompt
python "$SCRIPT" "/path/to/screenshot.png" "这段代码有什么 bug？"
```

## 模型全景

### 默认组（自动路由，最稳定）

| ID | 模型 | 并发 | TTFT | 上下文 | 输出 | 最佳场景 |
|---|---|:---:|:---:|:---:|:---:|---|
| `zhipu-4v` | 智谱 GLM-4V-Flash | **10** | 0.64s | 16K | 1K | Stage 1 扫描、中文 OCR、日常看图 |
| `zhipu-thinking` | 智谱 4.1V-Thinking | 5 | **0.41s** | 64K | 16K | 复杂图表、数据推理、深度分析 |
| `nvidia-phi4` | NVIDIA Phi-4 | ~40/min | 0.38s | 128K | ~4K | 英文快速识别、**音频转写** |

### 扩展组（需 `--backend` 手动指定）

| ID | 模型 | 并发 | TTFT | 上下文 | 输出 | 最佳场景 | 注意事项 |
|---|---|:---:|:---:|:---:|:---:|---|---|
| `zhipu-46v` | 智谱 4.6V-Flash | **1** | 1.52s | 128K | 32K | Function Call、视频、大输出 | 并发=1 会排队 |
| `nvidia-maverick` | Llama-4-Maverick | ~40/min | **4.4s** | **1M** | ~4K | 超大截图(>128K)、结构化输出 | 非常慢 |
| `nvidia-llama32` | Llama-3.2-11B | ~40/min | 0.54s | 128K | ~4K | phi-4 备用 | 仅英文 |
| `nvidia-nemotron-12b` | Nemotron-12B-v2 | ~40/min | 0.75s | 128K | ~4K | FC + 视频(2FPS) | 仅英文；推理不支持视频 |

## 决策矩阵：如何选模型

### 场景 → 推荐模型

| 你看到的场景 | 首选 | 备选 | 理由 |
|-------------|------|------|------|
| 中文截图/UI | `zhipu-4v` | `zhipu-thinking` | 中文最强，并发 10 |
| 中文文档 OCR | `zhipu-4v` | `zhipu-thinking` | OCR 识别准确 |
| 英文快速识别 | `nvidia-phi4` | `zhipu-4v` | phi-4 最快 0.38s |
| 复杂图表/数据可视化 | `zhipu-thinking` | `zhipu-4v` | 内置思维链推理 |
| 数学/科学图像 | `zhipu-thinking` | - | 推理能力最强 |
| 超大截图/长页面(>128K) | `nvidia-maverick` | `zhipu-46v` | 1M 上下文 |
| 视频内容 | `zhipu-46v` | `nvidia-nemotron-12b` | 原生视频支持 |
| 音频文件 | `nvidia-phi4` | - | **唯一支持音频** |
| 需要工具调用 | `zhipu-46v` | `nvidia-nemotron-12b` | Function Call |
| 需要结构化输出 | `nvidia-maverick` | `zhipu-46v` | 结构化输出支持 |

### Two-Stage 模式（推荐用于不确定的图片）

当不确定图片内容时，分两步走：

```
Stage 1: python "$SCRIPT" image.png "简要描述这张图片是什么类型，包含什么语言的文字"
    ↓ 分析 Stage 1 的结果
Stage 2: 根据发现选择最佳模型重新分析
    ├── 发现中文 → python "$SCRIPT" -b zhipu-4v image.png "详细OCR"
    ├── 发现复杂图表 → python "$SCRIPT" -b zhipu-thinking image.png "深度分析数据趋势"
    ├── 发现超大页面 → python "$SCRIPT" -b nvidia-maverick image.png "完整分析"
    └── 发现是音频 → python "$SCRIPT" -b nvidia-phi4 audio.mp3 "转写内容"
```

## 稳定性说明

- **智谱**：永久免费、API 稳定、并发明确。首选。
- **NVIDIA**：免费但不稳定——模型可能随时下线、API 偶发 500 错误。用作扩展，不作为唯一依赖。
- 所有后端均 OpenAI 兼容格式，Bearer token 认证。
- 零依赖，纯 Python 标准库。

## Error handling

- 缺少 API key → 跳过该模型，尝试下一个
- HTTP 错误 → 尝试下一个模型
- 全部失败 → 退出并报错
- 文件不存在 → 立即报错，不浪费 API 调用
