# Skill Catalog

这是一个技能索引文件，每个 skill 都托管在 GitHub 上作为独立的 `SKILL.md` 文件。

当你需要使用某个 skill 时，访问该 skill 的 Raw URL 可以获得更详细的工作流程和最佳实践建议。

## URL 推断规则

当 SKILL.md 中引用了相对路径的附属文件时，按以下规则推断完整 URL：

1. 当前 SKILL.md URL 去掉文件名，保留目录路径
2. 拼接相对路径，去掉 `./` 前缀
3. 示例：SKILL.md 在 `.../arch-design/SKILL.md`，引用 `./references/guide.md` → `.../arch-design/references/guide.md`

## Skills
