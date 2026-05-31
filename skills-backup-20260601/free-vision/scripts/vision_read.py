"""Vision Arsenal — 给纯文本模型扩展视觉能力的多后端路由系统。

用法：
    python vision_read.py <图片路径或URL> [prompt]
    python vision_read.py --backend <id> <图片路径或URL> [prompt]
    python vision_read.py --list
    python vision_read.py --list --extended

环境变量：
    ZHIPU_VISION_API_KEY  — 智谱 API Key（推荐）
    NVIDIA_VISION_API_KEY — NVIDIA NIM API Key（可选扩展）

默认路由只使用稳定模型。扩展模型需通过 --backend 手动指定。
"""
import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.request
import urllib.error

DEFAULT_PROMPT = "Describe this image in detail: text, UI elements, layout, colors, and all visual details. / 请详细描述这张图片的内容，包括文字、界面元素、布局、颜色等所有视觉细节。"

# ── 模型注册表 ──────────────────────────────────────────────────────────────
MODELS = [
    # ── 默认组（稳定、自动路由） ──
    {
        "id": "zhipu-4v",
        "group": "default",
        "name": "智谱 GLM-4V-Flash",
        "env_key": "ZHIPU_VISION_API_KEY",
        "base_url": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        "model": "glm-4v-flash",
        "max_tokens": 1024,
        "capabilities": ["image", "ocr", "chinese"],
        "concurrency": 10,
        "ttft": "0.64s",
        "context": "16K",
        "max_output": "1K",
        "strength": "中文最强、并发最高、永久免费",
        "best_for": "Stage 1 快速扫描、中文 OCR、日常看图、界面分析",
    },
    {
        "id": "zhipu-thinking",
        "group": "default",
        "name": "智谱 GLM-4.1V-Thinking-Flash",
        "env_key": "ZHIPU_VISION_API_KEY",
        "base_url": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        "model": "glm-4.1v-thinking-flash",
        "max_tokens": 4096,
        "capabilities": ["image", "video", "reasoning", "chinese"],
        "concurrency": 5,
        "ttft": "0.41s",
        "context": "64K",
        "max_output": "16K",
        "strength": "内置思维链推理、速度反而是最快(0.41s)",
        "best_for": "复杂图表分析、数据可视化推理、需要深度分析的图片、数学/科学图像",
    },
    {
        "id": "nvidia-phi4",
        "group": "default",
        "name": "NVIDIA Phi-4-Multimodal",
        "env_key": "NVIDIA_VISION_API_KEY",
        "base_url": "https://integrate.api.nvidia.com/v1/chat/completions",
        "model": "microsoft/phi-4-multimodal-instruct",
        "max_tokens": 1024,
        "capabilities": ["image", "audio", "english"],
        "concurrency": "~40/min",
        "ttft": "0.38s",
        "context": "128K",
        "max_output": "~4K",
        "strength": "最快(0.38s)、唯一支持音频输入",
        "best_for": "英文快速识别、音频转写",
        "caution": "NVIDIA API 不稳定，实测有 500 错误，模型可能随时下线",
    },
    # ── 扩展组（按需手动指定） ──
    {
        "id": "zhipu-46v",
        "group": "extended",
        "name": "智谱 GLM-4.6V-Flash",
        "env_key": "ZHIPU_VISION_API_KEY",
        "base_url": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        "model": "glm-4.6v-flash",
        "max_tokens": 8192,
        "capabilities": ["image", "video", "reasoning", "function_call", "chinese"],
        "concurrency": 1,
        "ttft": "1.52s",
        "context": "128K",
        "max_output": "32K",
        "strength": "Function Call + 思考模式可开关、128K 大上下文、32K 输出",
        "best_for": "需要工具调用的多模态 Agent、视频分析、需要大输出的场景",
        "caution": "并发=1，频繁调用会排队；速度较慢",
    },
    {
        "id": "nvidia-maverick",
        "group": "extended",
        "name": "NVIDIA Llama-4-Maverick-17B-128E",
        "env_key": "NVIDIA_VISION_API_KEY",
        "base_url": "https://integrate.api.nvidia.com/v1/chat/completions",
        "model": "meta/llama-4-maverick-17b-128e-instruct",
        "max_tokens": 1024,
        "capabilities": ["image", "function_call", "structured_output", "multilingual"],
        "concurrency": "~40/min",
        "ttft": "4.4s",
        "context": "1M",
        "max_output": "~4K",
        "strength": "1M 超大上下文、Function Call、结构化输出、12 语言",
        "best_for": "超大截图/长页面(>128K)、多语言、需要结构化输出",
        "caution": "TTFT 4.4s 非常慢；NVIDIA API 不稳定；400B MoE 模型冷启动慢",
    },
    {
        "id": "nvidia-llama32",
        "group": "extended",
        "name": "NVIDIA Llama-3.2-11B-Vision",
        "env_key": "NVIDIA_VISION_API_KEY",
        "base_url": "https://integrate.api.nvidia.com/v1/chat/completions",
        "model": "meta/llama-3.2-11b-vision-instruct",
        "max_tokens": 1024,
        "capabilities": ["image", "english"],
        "concurrency": "~40/min",
        "ttft": "0.54s",
        "context": "128K",
        "max_output": "~4K",
        "strength": "轻量快速(0.54s)",
        "best_for": "phi-4 不可用时的 NVIDIA 备用",
        "caution": "仅英文图文；NVIDIA API 不稳定",
    },
    {
        "id": "nvidia-nemotron-12b",
        "group": "extended",
        "name": "NVIDIA Nemotron-Nano-12B-v2-VL",
        "env_key": "NVIDIA_VISION_API_KEY",
        "base_url": "https://integrate.api.nvidia.com/v1/chat/completions",
        "model": "nvidia/nemotron-nano-12b-v2-vl",
        "max_tokens": 1024,
        "capabilities": ["image", "video", "reasoning", "function_call", "english"],
        "concurrency": "~40/min",
        "ttft": "0.75s",
        "context": "128K",
        "max_output": "~4K",
        "strength": "Function Call + 推理模式 + 视频(2FPS, 8-128帧)",
        "best_for": "需要 FC 的英文场景、视频分析",
        "caution": "仅英文；推理模式不支持视频；NVIDIA API 不稳定",
    },
]


def get_model(model_id: str) -> dict | None:
    for m in MODELS:
        if m["id"] == model_id:
            return m
    return None


def build_image_url(image_input: str) -> str:
    """构建 OpenAI 格式的 image_url（URL 或 base64 data URI）。"""
    if image_input.startswith(("http://", "https://")):
        return image_input

    if not os.path.isfile(image_input):
        print(f"错误：文件不存在: {image_input}", file=sys.stderr)
        sys.exit(1)

    mime_type = mimetypes.guess_type(image_input)[0] or "image/png"
    with open(image_input, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime_type};base64,{b64}"


def call_model(model: dict, image_input: str, prompt: str) -> tuple[str, dict]:
    """调用单个模型，返回 (文本结果, usage字典)。"""
    api_key = os.environ.get(model["env_key"], "")
    if not api_key:
        raise RuntimeError(f"环境变量 {model['env_key']} 未设置")

    image_url = build_image_url(image_input)
    payload = {
        "model": model["model"],
        "max_tokens": model["max_tokens"],
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_url}},
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        model["base_url"],
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    text = result["choices"][0]["message"]["content"]
    usage = result.get("usage", {})
    return text, usage


def route(image_input: str, prompt: str, model_id: str | None = None) -> str:
    """路由调用：指定模型或按默认组优先级自动切换。"""
    if model_id:
        target = get_model(model_id)
        if not target:
            print(f"错误：未知模型 '{model_id}'", file=sys.stderr)
            print("用 --list 查看所有可用模型", file=sys.stderr)
            sys.exit(1)
        targets = [target]
    else:
        targets = [m for m in MODELS if m["group"] == "default"]

    last_error = None
    for model in targets:
        name = model["name"]
        try:
            print(f"尝试: {name} ...", file=sys.stderr)
            text, usage = call_model(model, image_input, prompt)
            in_tok = usage.get("prompt_tokens", "?")
            out_tok = usage.get("completion_tokens", "?")
            print(f"成功: {name} [tokens: {in_tok}→{out_tok}]", file=sys.stderr)
            return text
        except Exception as e:
            last_error = e
            print(f"失败: {name} — {e}", file=sys.stderr)
            continue

    print(f"\n所有尝试均失败。最后错误: {last_error}", file=sys.stderr)
    sys.exit(1)


def list_models(extended: bool = False):
    """列出模型及可用状态。"""
    groups = ["default"] if not extended else ["default", "extended"]
    for group in groups:
        label = "默认组（自动路由）" if group == "default" else "扩展组（需 --backend 指定）"
        print(f"\n{label}:")
        print(f"  {'ID':22s} {'模型':40s} {'并发':8s} {'TTFT':8s} {'状态':8s}  最佳场景")
        print(f"  {'─'*22} {'─'*40} {'─'*8} {'─'*8} {'─'*8}  {'─'*30}")
        for m in MODELS:
            if m["group"] != group:
                continue
            key = os.environ.get(m["env_key"], "")
            status = "✅" if key else "❌"
            caps = ", ".join(m.get("best_for", "").split("、")[:2])
            caution = " ⚠️" if m.get("caution") else ""
            print(f"  {m['id']:22s} {m['name']:40s} {str(m['concurrency']):8s} {m['ttft']:8s} {status:8s}  {caps}{caution}")


def main():
    parser = argparse.ArgumentParser(description="Vision Arsenal — 纯文本模型的视觉扩展")
    parser.add_argument("image", nargs="?", help="图片路径或 URL")
    parser.add_argument("prompt", nargs="?", default=DEFAULT_PROMPT,
                        help="分析 prompt（默认：详细描述）")
    parser.add_argument("--backend", "-b",
                        choices=[m["id"] for m in MODELS],
                        help="指定模型（默认只用默认组，扩展模型需手动指定）")
    parser.add_argument("--list", "-l", action="store_true",
                        help="列出默认组模型")
    parser.add_argument("--extended", "-e", action="store_true",
                        help="配合 --list 显示所有模型（含扩展组）")
    args = parser.parse_args()

    if args.list:
        list_models(extended=args.extended)
        return

    if not args.image:
        parser.print_help()
        sys.exit(1)

    result = route(args.image, args.prompt, args.backend)
    print(result)


if __name__ == "__main__":
    main()
