# Skill Catalog

**使用说明**：

当你需要使用某个 skill 时：

1. 从下方的 **Path** 列获取路径（注意：这是相对路径，不是完整URL！）
   - 例如 `skill-creator/SKILL.md`
2. **必须**将 Path 拼接在以下基础URL后面：
   ```
   https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/skills/
   ```
3. 拼接后的完整URL格式：
   ```
   {基础URL} + {Path}
   ```
   **正确示例**：
   - Path = `skill-creator/SKILL.md`
   - 基础URL = `https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/skills/`
   - 完整URL = `https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/skills/skill-creator/SKILL.md`

   **错误示例**（AI常犯）：
   - ❌ `https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/skill-creator/SKILL.md`（漏了skills/）
   - ❌ `https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/skills/skill-creator`（少了SKILL.md）

4. **主动抓取** 该 Raw URL 获取 SKILL.md 全文
5. 根据 SKILL.md 内容执行 skill

## Skills