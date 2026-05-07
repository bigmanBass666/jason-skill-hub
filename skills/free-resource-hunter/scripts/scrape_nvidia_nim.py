#!/usr/bin/env python3
"""
NVIDIA NIM 模型列表爬虫 — free-resource-hunter skill 的核心采集脚本

用途：从 build.nvidia.com/models 按 Most Recent 排序爬取所有模型信息，
      提取每个模型的真实上架日期（span[aria-label]），用于增量对比判断新模型。

依赖：pip install playwright httpx openai pyyaml && playwright install chromium

输出：JSON 文件，包含模型列表 [{id, name, vendor, category, published_at, relative_date, source}]

用法：
    python scrape_nvidia_nim.py                    # 默认按 recent 排序，最多 200 个
    python scrape_nvidia_nim.py --sort popular     # 按热度排序
    python scrape_nvidia_nim.py --limit 50         # 只爬前 50 个
    python scrape_nvidia_nim.py --output my.json   # 自定义输出文件名
    python scrape_nvidia_nim.py --no-browser        # 仅用公开 API（无日期信息，仅统计）

环境变量：
    NVIDIA_API_KEY — 可选，有 key 时额外获取完整模型 ID 映射（认证 API 返回更多字段）

输出字段说明：
    id           — 模型完整 ID（如 "moonshotai/kimi-k2-instruct-0905"）
    name         — 模型显示名称
    vendor       — 模型厂商/提供方（小写）
    category     — 模型分类（从卡片推断）
    published_at — 上架日期（绝对日期，如 "May 1, 2026"）— 来自 span[aria-label]
    relative_date— 上架时间（相对时间，如 "5d"、"2mo"）— 备选
    source       — 数据来源标识（"playwright" 或 "api"）
"""

import argparse
import asyncio
import json
import os
import re
import sys
from datetime import datetime

try:
    import httpx
except ImportError:
    print("缺少 httpx 依赖，请运行: pip install httpx")
    sys.exit(1)

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("缺少 playwright 依赖，请运行: pip install playwright && playwright install chromium")
    sys.exit(1)


def parse_date(published_at: str) -> dict:
    """将绝对日期字符串解析为结构化信息，方便下游做时效性判断"""
    if not published_at:
        return {"raw": None, "days_ago": None, "is_recent": False}

    try:
        dt = datetime.strptime(published_at, "%B %d, %Y")
        days_ago = (datetime.now() - dt).days
        return {
            "raw": published_at,
            "days_ago": days_ago,
            "is_recent": days_ago <= 14,
            "parsed": dt.isoformat()
        }
    except (ValueError, TypeError):
        return {"raw": published_at, "days_ago": None, "is_recent": False}


def classify_model(model_id: str, category: str) -> str:
    """根据模型 ID 和分类推断模型类型"""
    id_lower = model_id.lower()

    # 拼接 id + category 用于关键词匹配，避免 "text-to-image" 被 "text" 先命中
    combined = f"{id_lower} {category.lower()}" if category else id_lower

    # 排除非文本模型的关键词
    exclude_keywords = [
        "whisper", "parakeet", "stable-diffusion", "nemoretriever", "esm2",
        "nvclip", "nemotron-parse", "riva-translate", "magpie-tts", "genmol",
        "proteinmpnn", "rfdiffusion", "shieldgemma", "nemoguard", "cosmos-",
        "nv-grounding", "starcoder2", "openfold", "llama-nemotron-embed",
        "nv-embed", "nemotron-asr", "nemotron-ocr", "nemotron-table",
        "nemotron-page", "nemotron-graphic", "parakeet-ctc",
        "synthetic-video", "active-speaker", "relighting", "lipsync",
        "embedding", "extraction", "speech", "asr", "tts", "vision-language",
        "text-to-image", "image-generation", "image-gen", "sdxl", "cogview",
    ]

    for kw in exclude_keywords:
        if kw in combined:
            return "non-text"

    # 图像生成模型（flux 在 exclude 里被标记为 non-text，这里捕获其他图像模型）
    image_keywords = ["dall-e", "imagen", "flux", "text-to-image", "image-gen",
                      "image-generation", "cogview", "stable-diffusion", "sdxl"]
    for kw in image_keywords:
        if kw in combined:
            return "image"

    # 排除 text-to-image 等复合词中的 "text" 误匹配
    if category and any(t in category for t in ["chat", "language", "agentic",
                                                  "coding", "reasoning", "moe"]):
        return "text"

    return "text"  # 默认假设为文本模型


async def fetch_api_models(api_key: str = None) -> tuple[dict, int]:
    """从公开 API 端点获取模型 ID 映射表和总数"""
    model_map = {}
    url = "https://integrate.api.nvidia.com/v1/models"
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(url, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                for m in data.get("data", []):
                    full_id = m.get("id", "")
                    if full_id:
                        short = full_id.split("/")[-1] if "/" in full_id else full_id
                        model_map[short] = full_id
                        model_map[full_id] = full_id
                return model_map, len(model_map)
            else:
                print(f"API 请求失败: HTTP {resp.status_code}", file=sys.stderr)
                return {}, 0
    except Exception as e:
        print(f"API 请求异常: {e}", file=sys.stderr)
        return {}, 0


async def scrape_nvidia_full(sort_by: str = "recent", limit: int = 200) -> list[dict]:
    """
    Playwright 爬取 build.nvidia.com/models，获取完整模型列表 + 上架日期
    """
    api_key = os.getenv("NVIDIA_API_KEY")
    api_model_map, api_count = await fetch_api_models(api_key)
    if api_count:
        print(f"[API] 获取到 {api_count} 个模型 ID 映射", file=sys.stderr)

    models = []
    seen = set()
    base_url = "https://build.nvidia.com"

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--ignore-certificate-errors", "--no-sandbox"]
        )
        page = await browser.new_page()
        page.set_default_timeout(120000)

        # build.nvidia.com/models 默认已是 Most Recent 排序（dateCreated:DESC）
        url = f"{base_url}/models"
        print(f"[Browser] 正在加载 {url} ...", file=sys.stderr)
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(5000)

        # 关闭 Cookie 弹窗
        try:
            await page.evaluate("""() => {
                const btn = document.querySelector('#onetrust-accept-btn-handler')
                    || document.querySelector('.onetrust-close-btn-handler')
                    || document.querySelector('#onetrust-reject-all-handler');
                if (btn) btn.click();
                const banner = document.querySelector('#onetrust-banner-sdk');
                if (banner) banner.style.display = 'none';
            }""")
            await page.wait_for_timeout(1000)
        except Exception:
            pass

        # 仅当需要热度排序时才切换（默认已是 Most Recent）
        if sort_by == "popular":
            print("[Browser] 切换为 Most Popular 排序...", file=sys.stderr)
            await page.locator("text=Sort By").first.click()
            await page.wait_for_timeout(1000)
            await page.locator("text=Most Popular").first.click()
            await page.wait_for_timeout(5000)

        # 分页爬取
        for page_num in range(1, 11):  # 最多 10 页
            cards = await page.query_selector_all("[data-testid='nv-card-root']")
            new_count = 0

            for card in cards:
                try:
                    # 提取模型 ID
                    link = await card.query_selector("a[data-nvtrack-nav-object='artifact-card']")
                    model_id = ""
                    if link:
                        href = await link.get_attribute("href")
                        if href and href.startswith("/"):
                            model_id = href.lstrip("/")

                    if not model_id or model_id in seen:
                        continue
                    seen.add(model_id)
                    new_count += 1

                    # 提取名称
                    name_elem = await card.query_selector("h1,h2,h3,h4,h5")
                    name = (await name_elem.text_content() or "").strip() if name_elem else model_id.split("/")[-1]

                    # 提取厂商
                    vendor_link = await card.query_selector("a[data-nvtrack-nav-object='artifact-card-publisher-link']")
                    vendor = ""
                    if vendor_link:
                        vt = await vendor_link.text_content()
                        if vt:
                            vendor = vt.strip().lower().replace(" ", "-")
                    elif "/" in model_id:
                        vendor = model_id.split("/")[0]

                    # 提取卡片全文
                    card_text = await card.inner_text()
                    lines = [l.strip() for l in card_text.split("\n") if l.strip()]

                    # 关键字段：上架日期（绝对日期，来自 span[aria-label]）
                    published_at = None
                    try:
                        date_spans = await card.query_selector_all("span[aria-label]")
                        for span in date_spans:
                            aria_label = await span.get_attribute("aria-label")
                            if aria_label and re.search(
                                r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}',
                                aria_label
                            ):
                                published_at = aria_label.strip()
                                break
                    except Exception:
                        pass

                    # 备选：相对时间
                    relative_date = None
                    if not published_at:
                        for line in lines:
                            date_match = re.search(r'(\d+d|\d+w|\d+mo|\d+y)', line)
                            if date_match:
                                relative_date = date_match.group(1)
                                break

                    # 提取分类
                    category = None
                    if len(lines) >= 5:
                        category = lines[4].lower()

                    # 用 API 映射补全 ID
                    short_name = model_id.split("/")[-1] if "/" in model_id else model_id
                    full_mapped_id = api_model_map.get(short_name, api_model_map.get(model_id, model_id))

                    date_info = parse_date(published_at)
                    model_type = classify_model(model_id, category or "")

                    models.append({
                        "id": full_mapped_id if api_model_map else model_id,
                        "name": name,
                        "vendor": vendor,
                        "category": category,
                        "type": model_type,
                        "published_at": published_at,
                        "relative_date": relative_date,
                        "date_info": date_info,
                        "source": "playwright"
                    })
                except Exception:
                    continue

            print(f"[Browser] 第 {page_num} 页: {len(cards)} 卡片, {new_count} 个新模型 (累计 {len(models)})", file=sys.stderr)

            if new_count == 0 or len(models) >= limit:
                break

            # 翻页
            try:
                next_btn = await page.query_selector('button[aria-label="Go to next page"]')
                if not next_btn:
                    break
                is_disabled = await next_btn.evaluate("el => el.disabled || el.getAttribute('aria-disabled') === 'true'")
                if is_disabled:
                    break
                await next_btn.click()
                await page.wait_for_timeout(5000)
                await page.wait_for_load_state("networkidle", timeout=10000)
            except Exception:
                break

        await browser.close()

    return models


async def api_only_mode() -> list[dict]:
    """仅用公开 API，不做浏览器爬取（无日期信息，仅用于总量统计）"""
    model_map, count = await fetch_api_models(os.getenv("NVIDIA_API_KEY"))
    models = []
    for short, full in model_map.items():
        if "/" not in short:  # 避免重复
            models.append({
                "id": full,
                "vendor": full.split("/")[0] if "/" in full else "",
                "source": "api",
                "published_at": None,
                "relative_date": None,
                "date_info": parse_date(None),
                "type": classify_model(full, ""),
            })
    return models


def main():
    parser = argparse.ArgumentParser(description="NVIDIA NIM 模型列表爬虫")
    parser.add_argument("--sort", choices=["recent", "popular"], default="recent",
                        help="排序方式: recent=最新上架(默认), popular=热度排序")
    parser.add_argument("--limit", type=int, default=200, help="最多爬取模型数量 (默认 200)")
    parser.add_argument("--output", type=str, default="nvidia_models.json", help="输出文件路径")
    parser.add_argument("--no-browser", action="store_true", help="仅用公开API（无日期信息，仅统计）")
    parser.add_argument("--days-recent", type=int, default=14, help="判定'最近上架'的天数阈值 (默认 14)")
    args = parser.parse_args()

    if args.no_browser:
        print("[INFO] API-only 模式（无日期信息，仅用于总量统计）", file=sys.stderr)
        models = asyncio.run(api_only_mode())
    else:
        models = asyncio.run(scrape_nvidia_full(sort_by=args.sort, limit=args.limit))

    # 统计摘要
    recent_models = [m for m in models if m.get("date_info", {}).get("is_recent")]
    text_models = [m for m in models if m.get("type") == "text"]
    non_text_models = [m for m in models if m.get("type") != "text"]

    print(f"\n{'='*50}", file=sys.stderr)
    print(f"总计: {len(models)} 个模型", file=sys.stderr)
    print(f"  文本模型: {len(text_models)}", file=sys.stderr)
    print(f"  非文本模型: {len(non_text_models)}", file=sys.stderr)
    if recent_models:
        print(f"  最近 {args.days_recent} 天上架: {len(recent_models)}", file=sys.stderr)
        print(f"\n  最新上架的模型:", file=sys.stderr)
        for m in recent_models[:10]:
            date_raw = m.get("published_at") or m.get("relative_date", "?")
            print(f"    {m['id']} — {date_raw}", file=sys.stderr)

    # 输出 JSON
    output = {
        "scraped_at": datetime.now().isoformat(),
        "sort_by": args.sort,
        "total": len(models),
        "text_models": len(text_models),
        "non_text_models": len(non_text_models),
        "recent_count": len(recent_models),
        "recent_threshold_days": args.days_recent,
        "models": models
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] 已保存到 {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
