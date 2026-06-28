#!/bin/sh
# ensure-junction.sh — 确保 skills/ 是 .agents/skills/ 的有效目录联接
# 如果被 git 操作破坏，自动重建
# 被 .git/hooks/post-checkout / post-merge / post-rewrite 调用

set -e

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
SKILLS="$REPO_ROOT/skills"
TARGET="C:\\Users\\86150\\.agents\\skills"

# 目标目录不存在 → 不做任何事
if [ ! -d "$TARGET" ]; then
  exit 0
fi

# skills/ 不存在 → 直接创建联接
if [ ! -e "$SKILLS" ]; then
  cmd.exe /c "mklink /J \"$SKILLS\" \"$TARGET\"" >/dev/null 2>&1
  exit $?
fi

# skills/ 是联接 → 已就绪
cmd.exe /c "fsutil reparsepoint query \"$SKILLS\" >nul 2>&1"
if [ $? -eq 0 ]; then
  exit 0
fi

# skills/ 存在但不是联接 → 重建
rm -rf "$SKILLS"
cmd.exe /c "mklink /J \"$SKILLS\" \"$TARGET\"" >/dev/null 2>&1
