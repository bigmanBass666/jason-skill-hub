---
name: code-review
description: 代码审查检查清单 - 帮助 AI 系统化地审查代码质量
version: "1.0"
author: Jason
tags: ["code-review", "quality", "checklist"]
---

# Code Review Skill

## 概述
本 skill 提供一套系统化的代码审查流程，帮助 AI 助手进行全面、一致的代码质量检查。

## 使用时机
- 当需要审查 Pull Request 时
- 当需要检查代码是否符合规范时
- 当需要确保代码质量时

## 步骤
1. 读取待审查的代码
2. 根据 ./references/checklist.md 中的检查项逐一审查
3. 使用 ./references/template.md 格式输出审查结果
4. 提供建设性的改进建议

## 检查维度
- [ ] 代码逻辑正确性
- [ ] 代码可读性
- [ ] 性能影响
- [ ] 安全性考虑
- [ ] 测试覆盖

## 参考
- 检查清单：./references/checklist.md
- 输出模板：./references/template.md
