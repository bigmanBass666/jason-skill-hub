# 模型全景

### 默认组（自动路由，最稳定）

| ID | 模型 | 并发 | TTFT | 上下文 | 输出 | 最佳场景 |
|---|---|:---:|:---:|:---:|:---:|---|
| `zhipu-4v` | 智谱 GLM-4V-Flash | **10** | **0.64s** | 16K | 1K | Stage 1 扫描、中文 OCR、日常看图 |
| `zhipu-thinking` | 智谱 GLM-4.1V-Thinking-Flash | 5 | **0.41s** | 64K | 16K | 复杂图表、数据推理、深度分析 |
| `stepfun-3.7` | StepFun Step-3.7-Flash | ? | ? | **256K** | **16K** | 复杂推理、长上下文视觉、多模态 Agent |

### 扩展组（需 `--backend` 手动指定）

| ID | 模型 | 并发 | TTFT | 上下文 | 输出 | 最佳场景 | 注意事项 |
|---|---|:---:|:---:|:---:|:---:|---|---|
| `zhipu-46v` | 智谱 GLM-4.6V-Flash | **1** | **1.52s** | 128K | 32K | Function Call、视频、大输出 | 并发=1 会排队 |
| `nvidia-maverick` | Llama-4-Maverick-17B-128E | ~40/min | **4.4s** | **1M** | ~4K | 超大截图(>128K)、结构化输出 | 非常慢 |
| `nvidia-llama32` | Llama-3.2-11B-Vision | ~40/min | 0.54s | 128K | ~4K | phi-4 备用 | 仅英文 |
| `nvidia-nemotron-12b` | Nemotron-Nano-12B-v2-VL | ~40/min | 0.75s | 128K | ~4K | FC + 视频(2FPS) | 仅英文；推理不支持视频 |
| `nvidia-phi4` | NVIDIA Phi-4-Multimodal | ~40/min | **0.38s** | 128K | ~4K | 英文快速识别、音频转写 | 实测 500 错误，不稳定 |
| `agnes` | Agnes 2.0 Flash | 1 | ~9s | ? | 1K | 精细中文描述 | SSL 偶发断开；大图 40s |
