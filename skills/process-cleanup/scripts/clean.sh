#!/bin/bash
# Process Cleanup Script
# 强制终止所有残留的开发进程

set -e

# 进程类型正则表达式
PATTERNS="(node|npm|python|python3|pip|uv|vite|claude|mcp|ruby|bundle|rails|gem|webpack|react-scripts|esbuild)"

echo "🔍 检查当前进程..."
before=$(ps aux | grep -E "$PATTERNS" | grep -v grep | wc -l)
if [ $before -eq 0 ]; then
  echo "✅ 没有发现残留的开发进程"
  exit 0
fi

echo "📋 发现 $before 个相关进程:"
ps aux | grep -E "$PATTERNS" | grep -v grep | awk '{printf "  PID: %s  Command: %s\n", $2, $11}'

echo
echo "💀 正在强制终止所有进程..."
ps -ef | grep -E "$PATTERNS" | grep -v grep | awk '{print $2}' | xargs -r kill -9 2>/dev/null || true

sleep 1

echo
after=$(ps aux | grep -E "$PATTERNS" | grep -v grep | wc -l)
if [ $after -eq 0 ]; then
  echo "✅ 清理完成！所有 $before 个进程已终止"
else
  echo "⚠️  仍有 $after 个进程残留，可能需要管理员权限"
  ps aux | grep -E "$PATTERNS" | grep -v grep
  exit 1
fi