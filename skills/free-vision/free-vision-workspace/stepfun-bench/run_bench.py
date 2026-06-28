"""Background parallel test runner for stepfun-3.7 vs baseline models.
Results written to JSON, no stdout pollution.
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error
import base64
import mimetypes
from datetime import datetime, timezone

SCRIPT = os.path.expanduser(r"~\.agents\skills\free-vision\scripts\vision_read.py")
IMAGE = r"D:\Test\api_key_test\.playwright-mcp\page-2026-05-19T18-18-44-626Z.png"
OUT_DIR = os.path.expanduser(r"~\.agents\skills\free-vision\free-vision-workspace\stepfun-bench")
os.makedirs(OUT_DIR, exist_ok=True)

TESTS = [
    {"id": "stepfun-3.7", "backend": "stepfun-3.7", "prompt": None, "scenario": "default_describe"},
    {"id": "stepfun-3.7", "backend": "stepfun-3.7", "prompt": "提取这张图片里的所有文字内容，用中文回答。", "scenario": "ocr_chinese"},
    {"id": "stepfun-3.7", "backend": "stepfun-3.7", "prompt": "这是一张数据仪表盘截图，请分析其中的数据趋势和关键指标。", "scenario": "data_analysis"},
    {"id": "nvidia-phi4", "backend": "nvidia-phi4", "prompt": None, "scenario": "default_describe"},
    {"id": "nvidia-phi4", "backend": "nvidia-phi4", "prompt": "提取这张图片里的所有文字内容，用中文回答。", "scenario": "ocr_chinese"},
    {"id": "zhipu-4v", "backend": "zhipu-4v", "prompt": None, "scenario": "default_describe"},
    {"id": "zhipu-4v", "backend": "zhipu-4v", "prompt": "提取这张图片里的所有文字内容，用中文回答。", "scenario": "ocr_chinese"},
    {"id": "zhipu-4v", "backend": "zhipu-4v", "prompt": "这是一张数据仪表盘截图，请分析其中的数据趋势和关键指标。", "scenario": "data_analysis"},
]

MODEL_META = {
    "stepfun-3.7": {"model": "stepfun-ai/step-3.7-flash", "base_url": "https://integrate.api.nvidia.com/v1/chat/completions", "env_key": "NVIDIA_VISION_API_KEY", "max_tokens": 4096},
    "nvidia-phi4": {"model": "microsoft/phi-4-multimodal-instruct", "base_url": "https://integrate.api.nvidia.com/v1/chat/completions", "env_key": "NVIDIA_VISION_API_KEY", "max_tokens": 1024},
    "zhipu-4v": {"model": "glm-4v-flash", "base_url": "https://open.bigmodel.cn/api/paas/v4/chat/completions", "env_key": "ZHIPU_VISION_API_KEY", "max_tokens": 1024},
}

DEFAULT_PROMPT = "Describe this image in detail: text, UI elements, layout, colors, and all visual details. / 请详细描述这张图片的内容，包括文字、界面元素、布局、颜色等所有视觉细节。"

def build_image_data_uri(path):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"

def call_direct(meta, image_uri, prompt):
    api_key = os.environ.get(meta["env_key"], "")
    if not api_key:
        return None, "API key not set"
    payload = json.dumps({
        "model": meta["model"],
        "max_tokens": meta["max_tokens"],
        "messages": [{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": image_uri}},
            {"type": "text", "text": prompt},
        ]}],
    }).encode()
    req = urllib.request.Request(meta["base_url"], data=payload, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }, method="POST")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode())
            elapsed = time.time() - t0
            text = result["choices"][0]["message"]["content"]
            usage = result.get("usage", {})
            return {
                "text": text,
                "elapsed_s": round(elapsed, 2),
                "usage": usage,
                "ok": True,
            }, None
    except Exception as e:
        elapsed = time.time() - t0
        return {"elapsed_s": round(elapsed, 2), "ok": False}, str(e)

def run_test(test):
    mid = test["id"]
    meta = MODEL_META[mid]
    prompt = test["prompt"] or DEFAULT_PROMPT
    image_uri = build_image_data_uri(IMAGE)
    result, err = call_direct(meta, image_uri, prompt)
    rec = {
        "model_id": mid,
        "scenario": test["scenario"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "elapsed_s": result.get("elapsed_s") if result else None,
        "ok": result.get("ok", False) if result else False,
        "error": err,
        "usage": result.get("usage") if result else None,
        "output_length": len(result.get("text", "")) if result else 0,
        "output_preview": (result.get("text", "")[:300] if result else ""),
    }
    return rec

if __name__ == "__main__":
    results = []
    for t in TESTS:
        print(f"[RUN] {t['id']} / {t['scenario']} ...", file=sys.stderr)
        r = run_test(t)
        results.append(r)
        status = "OK" if r["ok"] else f"FAIL: {r['error'][:80]}"
        print(f"  -> {status} ({r['elapsed_s']}s, {r['output_length']} chars)", file=sys.stderr)

    # Write results
    out_path = os.path.join(OUT_DIR, f"bench_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"tests": results, "image": IMAGE}, f, ensure_ascii=False, indent=2)
    print(f"\n[DONE] Results: {out_path}", file=sys.stderr)

    # Quick summary to stderr
    ok_count = sum(1 for r in results if r["ok"])
    print(f"Summary: {ok_count}/{len(results)} passed", file=sys.stderr)
    for r in results:
        tag = "PASS" if r["ok"] else "FAIL"
        print(f"  {tag} {r['model_id']:18s} {r['scenario']:20s} {r['elapsed_s']:6.1f}s  {r['output_length']:5d}ch", file=sys.stderr)
