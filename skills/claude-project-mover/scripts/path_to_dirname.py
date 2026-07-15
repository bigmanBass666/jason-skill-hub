#!/usr/bin/env python3
"""path_to_dirname — 将项目路径转换为 Claude Code 历史目录名

转换规则（实测验证）：
  仅保留 [a-zA-Z0-9]，其余所有字符 → '-'
  - 盘符 ':\\' 或 ':/' → '--'
  - 路径分隔符 '\\' 或 '/' → '-'

用法：
  python path_to_dirname.py "D:/Working/programming_projects/AK-Switch"
  python path_to_dirname.py "D:/Working/programming_projects/AK-Switch" --reverse
"""
import argparse
import sys


def path_to_dirname(project_path):
    """将项目路径转换为 Claude Code 的历史目录名。"""
    n = project_path.replace(':\\', '--').replace('\\', '-')
    n = n.replace(':/', '--').replace('/', '-')
    return ''.join(c if c == '-' or 'a' <= c <= 'z' or 'A' <= c <= 'Z' or '0' <= c <= '9' else '-' for c in n)


TEST_CASES = [
    ("D:\\Working\\programming_projects\\AK-Switch",
     "D--Working-programming-projects-AK-Switch"),
    ("C:\\Users\\86150",
     "C--Users-86150"),
    ("D:\\BaiduSyncFolder\\liu-jia-han-sth",
     "D--BaiduSyncFolder-liu-jia-han-sth"),
    ("D:\\Test\\Alvus-fork",
     "D--Test-Alvus-fork"),
    ("D:\\Test",
     "D--Test"),
    ("D:\\a_b-c.d!e@f#g$h%i^j&k(l)m[n]o{p}q~r,s;t'u`v+w x中",
     "D--a-b-c-d-e-f-g-h-i-j-k-l-m-n-o-p-q-r-s-t-u-v-w-x-"),
]


def self_test():
    """运行内置测试用例验证转换规则。"""
    failed = 0
    for path, expected in TEST_CASES:
        result = path_to_dirname(path)
        ok = result == expected
        status = "✅" if ok else "❌"
        if not ok:
            failed += 1
        print(f"{status}  {path}")
        print(f"     预期: {expected}")
        print(f"     实际: {result}")
        print()
    return failed


def main():
    p = argparse.ArgumentParser(
        description="将项目路径转换为 Claude Code 历史目录名")
    p.add_argument("path", nargs="?", help="项目路径（如 D:\\path\\to\\project）")
    p.add_argument("--test", action="store_true", help="运行自测")
    args = p.parse_args()

    if args.test:
        failed = self_test()
        sys.exit(failed)

    if not args.path:
        p.print_help()
        sys.exit(1)

    print(path_to_dirname(args.path))


if __name__ == "__main__":
    main()