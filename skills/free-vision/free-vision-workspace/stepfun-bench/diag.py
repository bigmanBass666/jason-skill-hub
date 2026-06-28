# 写回修复后的 MODELS 列表
lines = open(r"C:\Users\86150\.agents\skills\free-vision\scripts\vision_read.py", "r", encoding="utf-8").readlines()

# 策略: 找到 MODELS = [ 到 ] 的范围，完全替换
start_idx = None
end_idx = None
for i, line in enumerate(lines):
    if line.strip() == "MODELS = [":
        start_idx = i
    if start_idx is not None and line.strip() == "]" and i > start_idx:
        end_idx = i
        break

print(f"MODELS section: lines {start_idx} to {end_idx}")
print(f"Current line count in section: {end_idx - start_idx + 1}")
