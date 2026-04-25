# Skill Catalog

## 如何获取完整 Raw URL

每个 skill 的信息在下方 **Skills** 列表中。

**Step 1**: 找到你要的 skill（例如 skill-creator）

**Step 2**: 看它的 **Path** 列：`skill-creator/SKILL.md`

**Step 3**: 把这个 Path **直接拼接**在下面这个固定前缀后面：

```
https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/skills/
```

**计算过程**：
```
固定前缀: https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/skills/
Path:      skill-creator/SKILL.md
────────────────────────────────────────
完整URL:   https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/skills/skill-creator/SKILL.md
```

⚠️ **注意**：Path 不是完整URL！必须加上面的固定前缀！URL中间必须有 `skills/` 目录！

**主动抓取完整URL获取 SKILL.md 全文，然后根据内容执行 skill。**

## Skills