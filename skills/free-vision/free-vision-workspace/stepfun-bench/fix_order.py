"""Rebuild MODELS list with correct ordering."""
import ast

path = r"C:\Users\86150\.agents\skills\free-vision\scripts\vision_read.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

tree = ast.parse(text)
source_lines = text.split("\n")

# Find MODELS = [ line and matching ]
models_start = None
for i, line in enumerate(source_lines):
    if line.strip().startswith("MODELS = ["):
        models_start = i
        break

# Find closing ] at top level after models_start
depth = 0
models_end = None
for i in range(models_start, len(source_lines)):
    depth += source_lines[i].count("[") - source_lines[i].count("]")
    if depth <= 0 and i > models_start:
        models_end = i
        break

# Extract model dicts using AST to get exact positions
model_nodes = []
for node in ast.walk(tree):
    if isinstance(node, ast.Dict):
        # Check if it's a model entry by looking for "id" and "group" keys
        keys_vals = {}
        for k, v in zip(node.keys, node.values):
            if isinstance(k, ast.Constant) and isinstance(v, ast.Constant):
                keys_vals[k.value] = v.value
        if "id" in keys_vals and "group" in keys_vals and "name" in keys_vals:
            model_nodes.append((node, keys_vals))

# Get line:col of each model dict node
model_positions = []
for node, kv in model_nodes:
    model_positions.append((node.lineno, node.col_offset, kv))

model_positions.sort(key=lambda x: x[0])

# Extract the text for each model dict using AST end_lineno (Python 3.8+)
model_blocks = {}
for node, kv in model_positions:
    start_line = node.lineno - 1  # 0-indexed
    end_line = node.end_lineno  # already 1-indexed, exclusive
    block_text = "\n".join(source_lines[start_line:end_line])
    model_blocks[kv["id"]] = block_text

# Build new MODELS section
DEFAULT_ORDER = ["zhipu-4v", "zhipu-thinking", "stepfun-3.7"]
EXTENDED_ORDER = ["zhipu-46v", "nvidia-maverick", "nvidia-llama32", "nvidia-nemotron-12b", "nvidia-phi4", "agnes"]

new_section = "MODELS = [\n"
new_section += '# ── 默认组（稳定、自动路由） ──\n'
for mid in DEFAULT_ORDER:
    block = model_blocks.get(mid)
    if block:
        new_section += block + "\n"

new_section += "# ── 扩展组（需 `--backend` 手动指定） ──\n"
for mid in EXTENDED_ORDER:
    block = model_blocks.get(mid)
    if block:
        new_section += block + "\n"

new_section = new_section.rstrip("\n") + "\n]\n"

# Replace
new_lines = source_lines[:models_start] + new_section.split("\n") + source_lines[models_end + 1:]
new_text = "\n".join(new_lines)

with open(path, "w", encoding="utf-8") as f:
    f.write(new_text)

ast.parse(new_text)
print("Syntax OK")

# Verify order
for mid in DEFAULT_ORDER:
    print(f"  model-ids/{mid}")
print("  ---")
for mid in EXTENDED_ORDER:
    print(f"  model-ids/{mid}")
