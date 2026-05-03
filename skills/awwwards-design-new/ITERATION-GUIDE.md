# Awwwards Skill 迭代优化 Prompt

基于 skill-creator 的标准和流程，专为 `awwwards-design` skill 的持续迭代设计。

---

## 完整版（全面迭代 — 每季度一次）

````
# Awwwards Skill 迭代优化任务

你是一位世界级的 Web 设计系统架构师，同时精通 skill-creator 的方法论。你的任务是对现有的 `awwwards-design` skill 进行一次完整的审计与迭代优化。

## 前置准备

### 加载并整理文件

所有从 jsDelivr 加载的文件按以下目录结构整理，保持工作目录清洁：

```
/home/z/my-project/download/
├── old awwwards skill/          ← 从 jsDelivr 加载的原始 awwwards-design（作为 baseline）
│   ├── SKILL.md
│   └── references/
├── skill creator skill/         ← 从 jsDelivr 加载的 skill-Creators（审计框架）
│   ├── SKILL.md
│   ├── references/
│   └── agents/
└── improved awwwards skill/     ← 改进后的版本（工作副本 + 最终输出）
    ├── SKILL.md
    └── references/
```

具体操作：

1. 访问 INDEX 入口：`https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/INDEX.md`
2. 在 INDEX 中找到 `awwwards-design`，加载其 `SKILL.md` 及所有引用文件 → 保存到 `old awwwards skill/` 文件夹（保留原始结构）。如果该文件夹已存在且内容一致，跳过下载。
3. 在 INDEX 中找到 `skill-Creators`，加载其 `SKILL.md` 及所有引用文件（`references/schemas.md`、`agents/analyzer.md`、`agents/grader.md`、`agents/comparator.md`）→ 保存到 `skill creator skill/` 文件夹。如果已存在且内容一致，跳过下载。
4. `improved awwwards skill/` 是改进后的输出目录，如果已存在上一版本的改进结果，作为 baseline 保留。

## 工作流程

严格按以下阶段顺序执行，**研究完成前不修改任何 skill 文件**：

---

### Phase 1：深度调研（先做研究，再动文件）

进行多维度的信息搜集，英文资源优先，不限于以下方向：

1. **最新获奖案例趋势**：Awwwards 近 3 个月的 SOTD/Developer Award/Motion Award 获奖网站，分析它们的共同设计模式和技术实现
2. **技术生态演进**：GSAP、Three.js、Lenis、Astro、View Transitions API 等核心工具库的最新版本和最佳实践变化
3. **设计趋势变化**：排版趋势、色彩趋势、交互范式的新变化（对比 skill 中现有内容）
4. **社区最佳实践**：CSS-Tricks、Smashing Magazine、Web.dev、AWWWARDS Academy 等平台的深度文章
5. **竞品 Skill/系统**：其他高质量的前端设计系统、design tokens 体系、animation libraries 的文档结构和方法论
6. **实际使用反馈**：回顾 skill 中是否有模糊、矛盾、过时、或实际执行困难的指令

**输出要求**：整理一份结构化的调研报告，标注哪些发现对应 skill 中的哪些部分需要更新。

---

### Phase 2：基于 skill-creator 标准审计

读取 awwwards-design skill 的所有文件，用以下两层标准逐一审计：

#### 第一层：skill-creator 结构与写作标准

这些是 skill-creator 定义的核心质量指标，逐项检查：

| 标准 | 检查内容 | 对应 skill-creator 原文 |
|------|---------|----------------------|
| **Progressive Disclosure** | SKILL.md 是否 ≤500 行？三级加载是否清晰（Metadata → Body → Resources）？引用文件是否有明确的"何时读取"指引？ | "Keep SKILL.md under 500 lines; reference files clearly with guidance on when to read them" |
| **Explain the Why** | 指令是否解释了原因？是否用"why"替代了过多的 MUST/ALWAYS/NEVER？ | "Try to explain to the model why things are important in lieu of heavy-handed musty MUSTs" |
| **Description 质量** | frontmatter description 是否足够"pushy"？是否同时包含"做什么"和"何时触发"？是否覆盖了足够的触发场景？ | "include both what the skill does AND specific contexts for when to use it... make descriptions a little bit pushy" |
| **通用性 vs 狭隘性** | 指令是基于设计原理的通用指导，还是绑定在特定案例上的死板规则？ | "Try to make the skill general and not super-narrow to specific examples" |
| **Imperative 写作** | 是否使用祈使句？是否避免了模糊的"应该""可以"？ | "Prefer using the imperative form in instructions" |
| **引用文件结构** | 大文件（>300 行）是否有目录？多框架/多场景是否按 variant 分文件组织？ | "For large reference files (>300 lines), include a table of contents" |
| **Lean Prompt** | 是否有冗余内容在消耗 token 但没产生价值？ | "Remove things that aren't pulling their weight" |
| **脚本化复用** | 多个测试用例中是否出现重复工作？是否应该抽取为 scripts/ 下的可执行文件？ | "If all test cases resulted in the subagent writing similar helper scripts, that's a strong signal the skill should bundle that script" |

#### 第二层：领域专业审计

| 维度 | 审计内容 |
|------|---------|
| **准确性** | 技术信息是否过时？推荐方案是否仍是最优解？版本号、API、兼容性是否正确？ |
| **完整性** | 是否有重要的设计模式/技术方案未被覆盖？是否有明显缺失的领域？ |
| **可执行性** | 指令是否足够具体、无歧义？AI 能否直接执行而不需猜测？有没有"说得漂亮但做不了"的内容？ |
| **前沿性** | 是否包含当前年度的最新趋势和实践？是否有已经被淘汰的做法仍在推荐？ |
| **深度** | 是否只停留在"做什么"而缺少"为什么"和"怎么做"的深层解释？ |

**输出要求**：列出所有发现的问题和改进建议，按优先级排序（Critical / High / Medium / Low），每个问题标注违反了哪个 skill-creator 标准。

---

### Phase 3：实施改进

直接修改 skill 文件。**改进时必须遵守 skill-creator 的核心原则**：

1. **Explain the Why** — 如果发现自己在写大写的 ALWAYS/NEVER/MUST，停下来，重新用"为什么这很重要"来重构这段指令。今天的 LLM 有很强的 theory of mind，理解原因比服从命令更有效。
2. **Generalize from feedback** — 不要针对个别案例做过度狭窄的修改。如果某个指令导致问题，尝试用不同的隐喻或设计模式来表达，而不是添加更多限制。
3. **Keep the prompt lean** — 删除没有产生价值的内容。如果某段指令让 AI 浪费时间做无意义的事，果断砍掉。
4. **增量改进优于推倒重来** — 保留经过验证的有效内容，只改需要改的部分。
5. **每个修改都要有调研依据** — 不凭感觉改，每个变更都对应 Phase 1 的某个发现或 Phase 2 的某个审计发现。
6. **保持文件结构稳定** — 不轻易新增/删除/重命名文件，除非有充分理由。遵循 skill-creator 的目录规范（`SKILL.md` + `references/` + `scripts/`）。
7. **Description 优化** — 检查 frontmatter description，确保它足够"pushy"以对抗 AI 的 undertriggering 倾向。description 应同时包含功能描述和触发场景。
8. **测试思维** — 改完后自检：如果让 AI 用更新后的 skill 做一个网站，它能否产出比之前更好的结果？

---

### Phase 4：设计与运行测试（可选但推荐）

遵循 skill-creator 的测试流程，验证改进效果：

1. **设计 2-3 个测试 prompt** — 模拟真实用户会怎么触发这个 skill（例如："帮我做一个建筑事务所的作品集网站，要 Awwwards 级别的"）
2. **用改进后的 skill 跑一遍** — 观察执行过程，检查是否按预期工作
3. **用上一版本作为 baseline 跑一遍** — 对比输出质量
4. **记录发现** — 哪些地方变好了？哪些地方没有改善？是否引入了新问题？

> 注意：完整的 benchmark + grader + comparator 流程需要 skill-creator 的脚本工具支持。如果环境不完整，可以简化为人工对比评估。

---

### Phase 5：变更摘要

输出一份简明的变更日志：

- **变更了什么**（文件名 + 具体位置）
- **为什么变更**（对应哪个调研发现 / 审计标准）
- **变更前后对比**（关键 diff）
- **符合的 skill-creator 原则**（标注每个变更对应哪条原则）

最后，更新 zip 包：将改进后的 skill 按标准格式（`SKILL.md` + `references/`）重新打包为 `awwwards-design-skill.zip`。
````

---

## 聚焦版（定向优化某个方面）

当你在社交媒体看到新趋势、或者发现某个具体方向需要更新时，用这个版本：

````
# Awwwards Skill 定向优化

## 优化方向
[勾选一个或多个：]
- [ ] WebGL/3D 模式更新（Three.js 最新 API 变化、WebGPU 进展）
- [ ] 动画系统更新（GSAP 3.12+ 新特性、View Transitions API）
- [ ] 排版趋势更新（Variable Fonts 新动态、Kinetic Typography 新案例）
- [ ] 性能优化策略更新（Core Web Vitals 新标准、最新优化技术）
- [ ] 交互模式更新（新的交互范式、AI 驱动的交互模式）
- [ ] 视觉风格更新（新兴设计风格、色彩/排版趋势变化）
- [ ] 移动端策略更新（移动端 3D、触摸交互新方案）
- [ ] Description/触发优化（优化 frontmatter description 的触发准确率）
- [ ] 其他：__________

## 执行步骤

1. **加载并整理文件**：
   - 从 `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/INDEX.md` 加载 INDEX
   - 找到 `skill-Creators`，加载 SKILL.md + 所有引用文件 → 保存到 `skill creator skill/` 文件夹（已存在则跳过）
   - 找到 `awwwards-design`，加载 SKILL.md + 所有引用文件 → 保存到 `old awwwards skill/` 文件夹（已存在则跳过）
2. **调研**：针对选定方向进行深度搜索（英文资源优先），收集最新信息
3. **审计**：读取 `skill creator skill/` + `old awwwards skill/` + `improved awwwards skill/`，用 skill-creator 标准对比差距
4. **改进**：直接修改 `improved awwwards skill/` 下的文件，遵守 skill-creator 的写作原则（Explain the Why、Lean、Generalize、Imperative）
5. **报告**：输出变更摘要（改了什么、为什么改、符合哪条 skill-creator 原则、改前 vs 改后）

## Skill 文件位置
- 原始版本：`/home/z/my-project/download/old awwwards skill/`
- 审计框架：`/home/z/my-project/download/skill creator skill/`
- 改进版本：`/home/z/my-project/download/improved awwwards skill/`
````

---

## 极简版（一句话触发）

当只想快速检查是否有需要更新的内容：

````
请对 `/home/z/my-project/download/improved awwwards skill/` 下的 awwwards-design skill 进行迭代优化。

流程：
1. 加载并整理文件：从 `https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/INDEX.md` 加载 INDEX → `skill-Creators` 保存到 `skill creator skill/` → `awwwards-design` 保存到 `old awwwards skill/`（已存在则跳过）
2. 深度调研 2025-2026 年最新的 Awwwards 获奖网站趋势和前端技术演进（英文资源优先）
3. 用 skill-creator 的标准（Progressive Disclosure、Explain the Why、Lean Prompt、Description 质量、通用性等）审计现有 skill
4. 直接改进 `/home/z/my-project/download/improved awwwards skill/` 下的文件
5. 输出变更日志 + 重新打包 zip
````

---

## 使用建议

| 场景 | 推荐版本 |
|------|---------|
| 大版本迭代（每季度一次） | 完整版 |
| 看到新趋势想快速更新 | 聚焦版 |
| 日常维护检查 | 极简版 |
| 发现具体 bug 或不准确的内容 | 直接指出，让 AI 修复对应部分即可 |
| 想优化 skill 的触发准确率 | 聚焦版 → 勾选"Description/触发优化" |

## skill-creator 核心原则速查

| 原则 | 一句话解释 |
|------|-----------|
| **Explain the Why** | 用原因说服 AI，而不是用大写 MUST 命令 AI |
| **Lean Prompt** | 删掉没有产生价值的指令，每行都要 earn its place |
| **Progressive Disclosure** | SKILL.md ≤500 行，详细内容放 references/，按需加载 |
| **Generalize** | 基于设计原理写通用指导，不要绑定特定案例 |
| **Pushy Description** | description 要覆盖足够多的触发场景，对抗 AI 的 undertriggering |
| **Imperative Form** | 用祈使句写指令，避免"应该""可以" |
| **Bundle Scripts** | 如果多个用例都在重复做同一件事，抽取为脚本 |
| **Incremental** | 保留有效内容，增量改进而非推倒重来 |
