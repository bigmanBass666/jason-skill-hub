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
2. 根据 `./references/checklist.md` 中的检查项逐一审查
3. 使用 `./references/template.md` 格式输出审查结果
4. 提供建设性的改进建议

## 如何读取引用文件

当你读取本 SKILL.md 后，如需读取引用文件（如 `./references/checklist.md`），按以下规则**自动推断**完整 URL：

```
本文件 URL: https://raw.githubusercontent.com/{owner}/{repo}/master/code-review/SKILL.md
相对引用:    ./references/checklist.md
                ↓
完整 URL:   https://raw.githubusercontent.com/{owner}/{repo}/master/code-review/references/checklist.md
```

**推断规则**：将 `./` 替换为本文件所在目录 + `/references/`

**本 skill 的完整引用路径**：
- 检查清单: `https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/code-review/references/checklist.md`
- 输出模板: `https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/code-review/references/template.md`

## 检查维度
- [ ] 代码逻辑正确性
- [ ] 代码可读性
- [ ] 性能影响
- [ ] 安全性考虑
- [ ] 测试覆盖

## 参考
- 检查清单：`./references/checklist.md`
- 输出模板：`./references/template.md`
