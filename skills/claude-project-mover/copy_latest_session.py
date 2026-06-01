r"""
copy_latest_session.py - 复制当前会话 JSONL 到目标项目目录并修正 cwd

用法:
  python3 copy_latest_session.py <目标目录名>

例:
  python3 copy_latest_session.py C--Users-86150--agents-skills-claude-project-mover
"""
import json
import os
import sys
import uuid


def main():
    if len(sys.argv) < 2:
        print("usage: python3 copy_latest_session.py <target_project_dir_name>")
        sys.exit(1)

    target_dir_name = sys.argv[1]
    source_cwd = r"D:\Test"
    target_cwd = r"C:\Users\86150\.agents\skills\claude-project-mover"
    home = os.path.expanduser("~")

    # Find latest JSONL from source cwd
    src_dir = os.path.join(home, ".claude", "projects", "D--Test")
    if not os.path.isdir(src_dir):
        print("ERROR: source dir not found: {}".format(src_dir))
        sys.exit(1)
    files = sorted(os.listdir(src_dir), key=lambda f: os.path.getmtime(os.path.join(src_dir, f)), reverse=True)
    src = os.path.join(src_dir, files[0])
    if not src.endswith(".jsonl"):
        print("ERROR: no jsonl found in {}".format(src_dir))
        sys.exit(1)

    # Target dir
    dst_dir = os.path.join(home, ".claude", "projects", target_dir_name)
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, str(uuid.uuid4()) + ".jsonl")

    # Fix cwd
    lines = open(src, encoding="utf-8").readlines()
    changed = 0
    for i, line in enumerate(lines):
        d = json.loads(line)
        if d.get("cwd") == source_cwd:
            d["cwd"] = target_cwd
            lines[i] = json.dumps(d, ensure_ascii=False) + "\n"
            changed += 1
    with open(dst, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print("OK")
    print("  source:    {}".format(src))
    print("  target:    {}".format(dst))
    print("  size:      {} bytes, {} lines".format(os.path.getsize(dst), len(lines)))
    print("  cwd fixed: {} entries ({} -> {})".format(changed, source_cwd, target_cwd))
    print("  dir:       {}".format(dst_dir))


if __name__ == "__main__":
    main()
