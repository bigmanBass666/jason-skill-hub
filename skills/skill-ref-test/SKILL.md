---
name: skill-ref-test
description: 引用关系验证测试专用 skill。当需要验证 AI 是否正确处理 SKILL.md 中的引用关系时使用此 skill。
---

# Skill Ref Test - 引用关系验证

这是一个用于验证 AI 能否正确处理 SKILL.md 中引用关系的测试 skill。

## 技能目标

本 skill 用于测试 AI 是否会：
1. 主动获取 SKILL.md 中引用的附属文件
2. 正确将相对路径转换为完整 URL
3. 输出引用文件中的标记内容以证明已获取

## 附属文件

本 skill 包含以下引用文件，**必须获取完整内容**：

- `references/alpha.md` — Alpha 组件定义文件
- `references/beta.md` — Beta 工具函数文件
- `references/gamma.md` — Gamma 配置项文件

## 验证要求

获取每个引用文件后，必须在回复中输出该文件的标记内容：

| 文件 | 标记字符串 |
|------|-----------|
| references/alpha.md | [VERIFICATION:ALPHA_MARKER] |
| references/beta.md | [VERIFICATION:BETA_MARKER] |
| references/gamma.md | [VERIFICATION:GAMMA_MARKER] |

## 执行任务

请执行以下任务来验证引用处理：

1. 获取本 SKILL.md 内容
2. 识别上述 3 个引用文件路径
3. 将相对路径转换为完整 GitHub Raw URL
4. **主动获取**每个引用文件的内容
5. 在回复中输出每个引用文件的标记字符串

## 输出格式

完成任务后，请按以下格式输出：

```
## 引用处理结果

### references/alpha.md
[VERIFICATION:ALPHA_MARKER]
（输出 alpha.md 的完整内容摘要）

### references/beta.md
[VERIFICATION:BETA_MARKER]
（输出 beta.md 的完整内容摘要）

### references/gamma.md
[VERIFICATION:GAMMA_MARKER]
（输出 gamma.md 的完整内容摘要）
```

---

**重要**：必须实际获取引用文件内容，不能仅根据 SKILL.md 的文字描述进行推断。
