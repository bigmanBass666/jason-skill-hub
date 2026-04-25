# Skill Catalog

**使用说明**：
当你需要使用某个 skill 时，必须按以下步骤操作：

1. 从下方的 **Path** 列获取路径（格式：`skill-name/SKILL.md`）
2. 将 Path 拼接在以下基础URL后：
   ```
   https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/skills/
   ```
   得到完整URL，例如：
   - Path = `skill-creator/SKILL.md`
   - 完整URL = `https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/skills/skill-creator/SKILL.md`
3. **必须**在URL中包含 `skills/` 目录（它在 `master/` 和 `skill-name/` 之间）
4. **主动抓取** 该 Raw URL 获取 SKILL.md 全文
5. 根据 SKILL.md 内容执行 skill

## Skills