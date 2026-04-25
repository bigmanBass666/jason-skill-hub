# AI URL 推断指南

本文档帮助 AI agent 自动推断并访问 GitHub 仓库中的 raw 文件内容。

## 规则 1：GitHub 仓库 → Raw URL 转换

```
GitHub 仓库地址: https://github.com/{owner}/{repo}
                  ↓
Raw 基础 URL:    https://raw.githubusercontent.com/{owner}/{repo}/master
```

**示例**：
```
GitHub: https://github.com/bigmanBass666/jason-skill-hub
Raw:    https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master
```

## 规则 2：INDEX.md 定位

```
GitHub 仓库 + /skills/INDEX.md
                  ↓
Raw URL: https://raw.githubusercontent.com/{owner}/{repo}/master/skills/INDEX.md
```

**示例**：
```
GitHub: https://github.com/bigmanBass666/jason-skill-hub
Raw INDEX: https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/skills/INDEX.md
```

## 规则 3：Skill 文件路径推断

INDEX.md 中每个 skill 的 Path 格式为：
```
https://raw.githubusercontent.com/{owner}/{repo}/master/{skill-name}/SKILL.md
```

**示例**：
```
code-review skill:
https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/code-review/SKILL.md
```

## 规则 4：相对路径 → 完整 URL 推断

当读取某个 SKILL.md 时，发现相对引用（如 `./references/xxx.md`），按以下规则推断：

```
当前文件 URL: https://raw.githubusercontent.com/{owner}/{repo}/master/code-review/SKILL.md
相对引用:      ./references/checklist.md
                  ↓
完整 URL:      https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/code-review/references/checklist.md
```

**注意**：将 `./` 替换为当前目录路径即可。

## 规则 5：GitHub 目录页 → Raw 文件推断

```
GitHub 目录页: https://github.com/{owner}/{repo}/tree/master/skills/code-review
                  ↓
Raw 文件:       https://raw.githubusercontent.com/{owner}/{repo}/master/skills/code-review/SKILL.md
```

## 快速使用流程

1. **获取仓库**: 用户提供 GitHub 仓库地址
2. **构建 Raw 基础 URL**: `https://raw.githubusercontent.com/{owner}/{repo}/master`
3. **读取 INDEX.md**: 访问 `{raw-base}/skills/INDEX.md`
4. **解析 Skill 列表**: 从 Path 字段获取每个 skill 的完整 URL
5. **按需读取**: 根据相对引用推断并读取所需文件

## 示例对话

**用户**: 我的 skill 库在 https://github.com/bigmanBass666/jason-skill-hub，请读取 code-review skill。

**AI 推断过程**：
```
1. 仓库: https://github.com/bigmanBass666/jason-skill-hub
2. Raw base: https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master
3. INDEX: https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/skills/INDEX.md
4. 发现 code-review Path: https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/code-review/SKILL.md
5. 读取: GET https://raw.githubusercontent.com/bigmanBass666/jason-skill-hub/master/code-review/SKILL.md
```

## 注意事项

- 使用 `master` 作为默认分支名
- 文件路径区分大小写
- 相对路径永远以 `./` 开头，不要忘记
