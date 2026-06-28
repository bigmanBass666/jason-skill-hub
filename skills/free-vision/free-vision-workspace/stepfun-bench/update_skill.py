"""Update SKILL.md with stepfun-3.7 and new routing info."""
import pathlib

path = pathlib.Path.home() / ".agents" / "skills" / "free-vision" / "SKILL.md"
text = path.read_text(encoding="utf-8")

# 1. Update description
text = text.replace(
    '通过 zhipu-4v / zhipu-thinking / nvidia-phi4 等后端完成视觉任务。',
    '通过 zhipu-4v / zhipu-thinking / stepfun-3.7 等后端完成视觉任务。'
)

# 2. Update opening paragraph
text = text.replace(
    '默认路由使用最稳定的 3 个模型覆盖 95% 场景。当你判断某个场景需要特定模型时，可以通过 `--backend` 调用扩展组的任何模型。',
    '默认路由使用 3 个模型覆盖 95% 场景：`zhipu-4v` → `zhipu-thinking` → `stepfun-3.7`。当你判断某个场景需要特定模型时，可以通过 `--backend` 调用扩展组的任何模型。'
)

# 3. Update decision flow
text = text.replace(
    '场景明确匹配「复杂图表/数据可视化/数学/科学图像」 → 直接用 `--backend zhipu-thinking`，一步到位',
    '场景明确匹配「复杂图表/数据可视化/数学/科学图像/长上下文推理」 → 直接用 `--backend zhipu-thinking` 或 `--backend stepfun-3.7`，一步到位'
)

# 4. Add stepfun-3.7 to model selection table
old_table_end = '| 英文快速识别 | `nvidia-phi4` | 最快，不稳定 |\n| 视频内容 | `zhipu-46v` | 原生视频支持 |'
new_table_end = '| 复杂推理、长上下文视觉 | `stepfun-3.7` | 256K 上下文 + 推理 + 多模态 Agent |\n| 英文快速识别 | `nvidia-phi4` | 最快，不稳定 |\n| 视频内容 | `zhipu-46v` | 原生视频支持 |'
text = text.replace(old_table_end, new_table_end)

path.write_text(text, encoding="utf-8")
print("SKILL.md updated successfully")

# Verify
for line in text.split('\n'):
    if 'stepfun' in line.lower() or 'step-3.7' in line:
        print(f'  Found: {line.strip()[:80]}')
