"""Fix MODELS list: remove stray { lines and add missing }, closings."""
import ast

path = r"C:\Users\86150\.agents\skills\free-vision\scripts\vision_read.py"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Strategy: find each model entry by "id": line, then ensure proper braces.

# Current broken state:
#   Line X:   "id": "...",
#   entry lines...
#   Line Y:   "best_for": "...",
#   Then either:
#     a) stray "{" line (should be removed)
#     b) missing "}," (should be added)

fixed = []
i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.strip()

    # Stray lone "{" on a line by itself (after best_for closing)
    if stripped == "{" and i > 0:
        # Check if previous non-empty line is inside a model dict (has "key": pattern)
        prev_idx = i - 1
        while prev_idx >= 0 and not lines[prev_idx].strip():
            prev_idx -= 1
        prev_line = lines[prev_idx].strip() if prev_idx >= 0 else ""
        # If prev line looks like a model field, this { is an orphan
        if ':' in prev_line and not prev_line.startswith("{"):
            i += 1
            continue  # skip the stray {

    # Check if a "best_for" line at end of model should have "},"
    if stripped.startswith('"best_for":') and stripped.endswith('",'):
        fixed.append(line)
        # Peek ahead: is next non-empty line something unexpected?
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines):
            next_stripped = lines[j].strip()
            # If next is stray "{" or another "id":, the current entry is missing },
            if next_stripped == "{" or next_stripped.startswith('"id":'):
                fixed.append("    },\n")
        i += 1
        continue

    fixed.append(line)
    i += 1

new_text = "".join(fixed)

# Verify
import ast
try:
    ast.parse(new_text)
    print("Syntax OK")
except SyntaxError as e:
    print(f"Syntax error at line {e.lineno}: {e.msg}")
    print(f"  {e.text}")
    # Write anyway for inspection
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)
    exit(1)

with open(path, "w", encoding="utf-8") as f:
    f.write(new_text)
print("Fixed successfully")
