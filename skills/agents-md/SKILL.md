---
name: agents-md
description: >
  Create and optimize AGENTS.md files for any project. Use this skill whenever the user wants to
  create, generate, update, or improve an AGENTS.md file, or when they mention "agents.md",
  "AGENTS.md", "agent instructions", "AI coding instructions", "project context for AI",
  "coding agent config", or ask how to set up their project for AI coding tools like Copilot,
  Cursor, Codex, Claude Code, or Jules. Also trigger when the user says "帮我创建AGENTS.md",
  "生成AGENTS.md", "写个AGENTS.md", "项目AI配置", or any request to make their project
  AI-friendly for coding agents. Additionally, trigger when the user wants to add a rule or
  instruction to an existing AGENTS.md, such as "add this rule to AGENTS.md", "把这条规则加到
  AGENTS.md", "记住这个规则", or "update AGENTS.md with this".
---

# AGENTS.md Skill

You are an expert at creating AGENTS.md files — the open, standardized Markdown format that
provides AI coding agents with project context and instructions. Your job is to analyze a project
and produce a high-quality AGENTS.md that follows the official specification and industry best
practices.

## What AGENTS.md Is

AGENTS.md is a simple Markdown file placed in the project root that serves as a README for AI
coding agents. Unlike README.md (written for humans), AGENTS.md provides precise, executable,
unambiguous instructions that AI agents need to work effectively on a project. It is supported by
GitHub Copilot, OpenAI Codex, Google Jules, Cursor, Claude Code (via symlink), Aider, and other
major AI coding tools.

The format has no required fields or strict schema — it is plain Markdown. The value comes from
providing the right information in the right way.

## Core Principle: Map, Not Manual

AGENTS.md should be a navigation map (~150-200 lines), not an exhaustive manual. It tells the
agent "where to find what" and "what rules to follow". Detailed documentation should be linked,
not inlined. Only two categories of content belong directly in AGENTS.md:

1. **Information the AI must know to avoid writing incorrect code** — tech stack, project
   structure, critical conventions, forbidden actions
2. **Hard rules whose violation directly causes problems** — coding conventions, naming rules,
   boundary restrictions

Everything else goes into linked documents. The test: if AI not knowing this would produce
*wrong* code, put it in AGENTS.md; if it would merely produce *suboptimal* code, link to it.

## Workflow

### Phase 1: Project Analysis

Before writing anything, thoroughly analyze the project. Gather information by:

1. **Read existing context files** — Check for README.md, CONTRIBUTING.md, package.json,
   Cargo.toml, pyproject.toml, go.mod, pom.xml, build.gradle, Makefile, justfile, or any
   existing AGENTS.md / CLAUDE.md / .cursorrules / .github/copilot-instructions.md

2. **Identify the tech stack** — Language, framework, build tool, package manager, test runner,
   linter/formatter

3. **Map the project structure** — Key directories, their purposes, and how code is organized

4. **Discover commands** — Build, test, lint, format, dev server, and any custom scripts

5. **Detect conventions** — Naming patterns, code style, architectural patterns (layered,
   hexagonal, etc.), import conventions

6. **Find boundaries** — Files/directories that should not be modified, sensitive configs,
   security concerns

7. **Check for monorepo** — If the project has sub-projects, note which ones need their own
   nested AGENTS.md

8. **Note platform and shell specifics** — Check if the project requires specific OS paths
   (e.g., Windows backslash paths), specific shells (PowerShell vs bash), or has
   environment-specific tooling (emulators, device connections). These must be explicit in
   AGENTS.md because agents cannot infer platform requirements.

9. **Identify non-obvious traps** — Look for project-specific gotchas that would trip up an
   AI agent: commands that must run from a specific directory, tools with known issues on
   certain platforms, configuration steps that are easy to forget. These become the Common
   Pitfalls section.

### Phase 2: Generate AGENTS.md

Write the AGENTS.md file following the structure below. Adapt sections based on what's relevant
to the project — omit sections that don't apply, add sections that are project-specific.

#### Required Structure

```markdown
# [Project Name] — AGENTS.md

Brief 1-2 sentence project description and tech stack summary.

## Dev Environment Tips

Practical commands and environment setup that agents need. Every command must be wrapped in
backticks so the agent can execute it directly. Include:
- Dependency installation command
- Dev server start command
- Any environment variable or prerequisite notes

## Build & Test

Exact commands for building and testing. Include:
- Build command
- Test command (full suite and single test/file)
- Lint/format commands
- Any CI-equivalent local command

## Project Structure

Key directories and their purposes. Keep it concise — a flat list with one-line descriptions.
Only list directories the agent is likely to interact with.

## Code Style & Conventions

Naming rules, formatting preferences, and coding patterns. Give concrete examples (good vs bad)
rather than abstract rules. Cover:
- Naming conventions (functions, classes, files, constants)
- Import style
- Error handling patterns
- Any project-specific patterns

## Boundaries

Three-tier classification of what the agent can and cannot do:
- ✅ **Always**: Actions the agent can take autonomously
- ⚠️ **Ask first**: Actions requiring user confirmation
- 🚫 **Never**: Actions the agent must never perform

## PR / Commit Guidelines

If applicable, include commit message format, PR title format, and pre-commit checks.
```

#### Recommended Sections (include when applicable)

- **Common Pitfalls** — Project-specific gotchas that trip up AI agents. This section is
  extremely valuable because it captures knowledge that agents cannot infer from code alone.
  Examples: "always cd into the project directory before running gradlew", "ADB screencap
  produces blank images on this emulator — use alternative method", "new Activities must be
  registered in AndroidManifest.xml". If the project has any non-obvious traps, include this.

- **Verification Loop** — For projects where agents can self-verify after making changes
  (curl endpoints, health checks, browser checks, ADB install+launch, etc.), describe the
  exact verification procedure. This enables agents to close the loop: write code → build →
  verify → fix, which dramatically improves output quality, especially for autonomous runs.

#### Optional Sections (add when relevant)

- **Architecture Notes** — For projects with layered/hexagonal architecture, describe the
  dependency direction rules
- **Monorepo Navigation** — For monorepos, list sub-projects and how to target commands to
  specific packages
- **Reference Documents** — Links to detailed docs (architecture docs, API docs, design docs)

### Phase 3: Validate & Refine

After generating the initial AGENTS.md:

1. **Line count check** — If it exceeds 200 lines, move detailed content to linked documents
2. **Command accuracy** — Verify every backtick-wrapped command actually exists in the project
3. **No duplication** — Don't copy content from README.md; link to it instead
4. **Precision check** — Replace vague instructions ("install deps") with exact commands
   (`pnpm install`)
5. **Boundary completeness** — Ensure the Boundaries section covers at minimum: what files to
   never touch, what requires confirmation, and security-sensitive areas

## Writing Rules

1. **Commands must be exact and executable** — Use `pnpm install` not "install dependencies".
   Always wrap in backticks.

2. **Examples beat rules** — Instead of "use descriptive function names", show:
   ```
   // Good: fetchUserById, calculateTotalPrice
   // Bad: get, calc, doSomething
   ```

3. **Link, don't inline** — For detailed docs, use relative links:
   `See [docs/architecture.md](./docs/architecture.md) for layered architecture details.`

4. **Be specific about test commands** — Include how to run a single test, not just the full
   suite. Agents often need to run targeted tests after making changes.

5. **State the obvious for AI** — Things humans infer from context (e.g., "this is a monorepo,
   use --filter to target packages") must be explicit.

6. **Use the three-tier boundary system** — ✅ Always / ⚠️ Ask first / 🚫 Never. This gives
   agents clear autonomy boundaries.

7. **No filler or fluff** — Every line should serve a purpose. Remove anything an agent
   wouldn't act on.

8. **Prefer tables for command references** — They're compact and scannable:
   ```markdown
   | Command | Purpose |
   |---------|---------|
   | `pnpm dev` | Start dev server |
   | `pnpm test` | Run all tests |
   | `pnpm lint` | Check code style |
   ```

## Monorepo & Multi-Project Handling

### Standard Monorepo

For monorepo projects with a shared build root:

1. Create a root AGENTS.md with project-wide rules and navigation
2. Create nested AGENTS.md files in sub-project directories with project-specific instructions
3. In the root file, list all sub-projects with their paths and a one-line description
4. Specify how to target commands to specific packages (e.g., `pnpm --filter <pkg>`, `cargo -p
   <crate>`)
5. Note which sub-projects share dependencies and which are independent

### Independent Sub-Projects (No Root Build)

Some workspaces contain independent projects that share no build system — common in course
workspaces, example collections, or multi-app repositories. For these:

1. Create a root AGENTS.md that serves as a directory and provides shared environment setup
2. Explicitly state that there is no root build — agents must cd into each project first
3. List all sub-projects with their paths, tech stacks, and one-line descriptions
4. Include shared environment requirements (JDK path, SDK path, etc.) in the root file
5. If sub-projects differ significantly, create nested AGENTS.md for each

## Tech Stack Detection Guide

| File | Tech Stack Signal |
|------|-------------------|
| package.json | Node.js / JavaScript / TypeScript |
| pnpm-lock.yaml | pnpm package manager |
| yarn.lock | Yarn package manager |
| Cargo.toml | Rust |
| go.mod | Go |
| pyproject.toml / setup.py | Python |
| pom.xml / build.gradle | Java / Kotlin |
| *.sln / *.csproj | .NET / C# |
| Gemfile | Ruby |
| composer.json | PHP |
| Makefile / justfile | Build automation |
| .github/workflows/ | CI/CD (GitHub Actions) |
| AndroidManifest.xml | Android |
| build.gradle.kts | Android / Gradle with Kotlin DSL |
| libs.versions.toml | Android version catalog |

## Anti-Patterns to Avoid

1. **Don't copy README content** — AGENTS.md complements README, it doesn't duplicate it
2. **Don't write essays** — Keep each section concise and scannable
3. **Don't use vague language** — "Run the tests" → `pnpm test`
4. **Don't omit the Boundaries section** — This is the most commonly missing but most
   important section
5. **Don't include information the AI can infer** — AI knows standard library APIs and common
   framework patterns. Only include project-specific or non-obvious information
6. **Don't generate AGENTS.md with AI-only content** — If a human wouldn't verify the
   accuracy, don't include it. Inaccurate instructions are worse than no instructions

## The Iterative Growth Principle

The best AGENTS.md is not written once — it grows over time. When an AI agent makes a mistake
on your project, that mistake reveals a gap in the AGENTS.md. Add a rule to fill that gap, and
the agent won't make that mistake again.

This creates a positive feedback loop:

1. AI makes a mistake → you notice → add rule to AGENTS.md → AI doesn't repeat it
2. Over time, AGENTS.md converges to exactly the rules your project needs — no more, no less
3. Rules added from real mistakes are always more useful than rules written speculatively

**Practical workflow for adding rules:**

When you notice the AI did something wrong, tell it: "Add this rule to AGENTS.md" or
"记住这条规则，加到 AGENTS.md 里". The skill should then:

1. Identify which section the rule belongs to (Boundaries, Code Style, Common Pitfalls, etc.)
2. Write the rule concisely and specifically — not "be careful with X" but "always do X before Y"
3. Insert it in the appropriate location without restructuring the entire file
4. Keep the total under 200 lines — if adding a rule would exceed this, extract a section to a
   linked document first

**Rule writing tips for incremental additions:**

- Write the rule as a direct instruction, not a description of what went wrong
  - Bad: "AI sometimes forgets to register Activities in the manifest"
  - Good: "Every new Activity must be registered in AndroidManifest.xml"
- Make rules specific and actionable, not vague warnings
  - Bad: "Be careful with the database"
  - Good: "Always use parameterized queries: `db.delete(TABLE, 'name = ?', new String[]{name})`"
- One rule per mistake — don't bundle multiple concerns into one rule
- If the same type of mistake happens twice, the rule isn't specific enough — refine it

**When NOT to add a rule:**

- If the AI made a one-off mistake that's unlikely to recur (no rule needed)
- If the mistake was due to unclear requirements, not missing context (clarify the task instead)
- If adding the rule would duplicate an existing rule (make the existing one more specific instead)

## When the User Already Has an AGENTS.md

If an AGENTS.md already exists, analyze it against the best practices above and suggest
improvements rather than rewriting from scratch. Focus on:

- Missing sections (especially Boundaries)
- Vague commands that need to be made precise
- Content that should be linked rather than inlined
- Line count exceeding 200 (suggest what to extract)
- Missing test/lint commands
- Lack of concrete examples in Code Style section

Also check if the AGENTS.md shows signs of being "over-planned" (too many speculative rules that
weren't born from real mistakes) — these can often be trimmed to improve signal-to-noise ratio.

## Reference

For the full specification and additional context, read `references/spec-and-examples.md`.
