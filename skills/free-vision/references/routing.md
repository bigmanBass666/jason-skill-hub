# 路由决策

## 场景 → 推荐模型

| 场景 | 首选 | 备选 | 理由 |
|------|------|------|------|
| 中文截图/UI | `zhipu-4v` | `zhipu-thinking` | 中文最强，并发 10 |
| 中文文档 OCR | `zhipu-4v` | `zhipu-thinking` | OCR 识别准确 |
| 英文快速识别 | `nvidia-phi4` | `zhipu-4v` | phi-4 最快 0.38s |
| 复杂图表/数据可视化 | `zhipu-thinking` | `zhipu-4v` | 内置思维链推理 |
| 数学/科学图像 | `zhipu-thinking` | `stepfun-3.7` | 推理能力最强；stepfun 可作为备选 |
| 超大截图/长页面(>128K) | `nvidia-maverick` | `zhipu-46v` | 1M 上下文 |
| 长上下文推理视觉 | `stepfun-3.7` | `zhipu-thinking` | 256K 上下文 + 推理能力 |
| 视频内容 | `zhipu-46v` | `nvidia-nemotron-12b` | 原生视频支持 |
| 音频文件 | `nvidia-phi4` | - | **唯一支持音频** |
| 需要工具调用 | `zhipu-46v` | `nvidia-nemotron-12b` | Function Call |
| 需要结构化输出 | `nvidia-maverick` | `zhipu-46v` | 结构化输出支持 |
| 通用推理/多模态 Agent | `stepfun-3.7` | `zhipu-thinking` | 198B MoE，推理 + Agentic 任务 |

## Two-Stage 模式

不确定图片内容时，分两步走：

```
Stage 1: zhipu-4v 快速扫描 → 判断内容类型/语言
Stage 2: 根据发现选最佳模型重新分析
├── 发现中文 → 可选 zhipu-thinking 深度 OCR
├── 发现复杂图表 → zhipu-thinking 深度分析
├── 发现超大页面 → nvidia-maverick 完整分析
├── 发现是音频 → nvidia-phi4 转写
└── 发现推理/Agent 任务 → stepfun-3.7 深度处理
```

## 默认 Fallback 链

```
zhipu-4v → zhipu-thinking → stepfun-3.7
```

- 首个成功即返回，不尝试后续
- 全部失败则报错退出
- stepfun-3.7 有 35s 冷启动（MoE 首次加载），warm 后约 10s
