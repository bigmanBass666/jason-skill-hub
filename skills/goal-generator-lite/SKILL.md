---
name: goal-generator-lite
description: >
  极简版 goal 生成。触发后直接读取原文为当前对话设计一个 goal。
  当用户提到 /goal、目标工作、让 Claude 自主多轮执行时使用。
context: fork
agent: general-purpose
---

!`powershell -Command "Invoke-WebRequest -Uri 'https://code.claude.com/docs/zh-CN/goal.md' -UseBasicParsing | Select-Object -ExpandProperty Content"`

使用 Fetch(), 精读 https://code.claude.com/docs/zh-CN/goal.md, 为当前对话设计一个goal, 放在根目录下: goal.md
