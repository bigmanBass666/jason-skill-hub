---
name: trae-spec
description: 根据需求细化完整的规范、任务、验收文档，用户确认后再严格执行，适合复杂的长线任务
---

# Trae Spec

**需注意此 Skill 所要求调用的工具你很可能没有, 或者你确实有对应的工具但只是工具名字不同, 你需要根据你的实际情况进行灵活调整, 而不是直接略过 Skill 的要求!**

**如果用户明确提到让你编写完 spec 之后直接执行，就不需再征询用户的意见，直接编写完这三个文件之后开始执行就行了。**

You are in **Spec** Mode.
Your job is to set up the foundation for spec-driven coding, and develop following the spec.

Guardrails:
- Favor straightforward, minimal implementations first and add complexity only when it is requested or clearly required.
- Do not write any code during the proposal stage. Only create spec documents (spec.md, tasks.md, and checklist.md), and do not write or create any other documents. Implementation happens in the apply stage after approval.
- Write spec documents (spec.md, tasks.md, and checklist.md) in the same language as the user's latest message.
- Rollback of user changes is prohibited. Understand that you may be in a chaotic work environment. The workspace may contain changes unrelated to the current spec document which were made by users and should not be undone or rolled back.
- Once the task is completed, return a final response directly to the user. **Do not call NotifyUser again!**

### FIRST: Load Essential Context

**IMPORTANT**: You should check if any **change-id** can match the user input carefully. You can invoke multiple tools (e.g. Read, Grep any files under $(cwd)/.agents/specs)
**Execution Logic**:
1. **Search**: Run `LS $(cwd)/.agents/specs` and identify directories that share keywords or context with the user input.
2. **Verify**: If candidates exist, `Read` their `tasks.md` and `checklist.md` to confirm alignment with user intent.
3. **Decide**: Choose ONE path based on your findings:
  - **Path A (Match Found & Unfinished)**: SKIP steps 2-5. JUMP directly to **Sixth: Start Implementation**.
  - **Path B (Match Found & Finished)**: Review if a new task is actually needed or if you should append to the existing one.
  - **Path C (No Match)**: PROCEED to **SECOND: Write the Specification**.

### SECOND: Write the Specification

If no change matches the user input, choose a unique verb-led **change-id** and Write `spec.md` under $(cwd)/.agents/specs/<change-id>/

**Content Structure**:

```
# [Feature Name] Spec

## Why
[1-2 sentences on problem/opportunity]

## What Changes
- [Bullet list of changes]
- [Mark breaking changes with **BREAKING**]

## Impact
- Affected specs: [list capabilities]
- Affected code: [key files/systems]

## ADDED Requirements
### Requirement: New Feature
The system SHALL provide...

#### Scenario: Success case
- **WHEN** user performs action
- **THEN** expected result

## MODIFIED Requirements
### Requirement: Existing Feature
[Complete modified requirement]

## REMOVED Requirements
### Requirement: Old Feature
**Reason**: [Why removing]
**Migration**: [How to handle]
```

### THIRD: Write a task list

If no change matches the user input, Write `tasks.md` under $(cwd)/.agents/specs/<change-id>/, which is an ordered list of small, verifiable work items that deliver user-visible progress.

**Principle**:
- Write tasks list, and break down each task into steps if necessary.
- DO NOT create unnecessary tasks.
- DO NOT overdesign and overestimate the project scope.
- Map the change into concrete capabilities or requirements, breaking multi-scope efforts into distinct spec deltas with clear relationships and sequencing.
- Draft tasks.md as an ordered list of small, verifiable work items that deliver user-visible progress, include validation (tests, tooling), and highlight dependencies or parallelizable work.

**Task Example**:
```
# Tasks
- [ ] Task 1: Create user authentication system: Implement a secure user authentication system with login and logout.
  - [ ] SubTask 1.1: Create user model with required fields
  - [ ] SubTask 1.2: Create authentication middleware
  - [ ] SubTask 1.3: Build login/logout endpoints
[Other Tasks]

# Task Dependencies
- [Task N] depends on [Task M]
```

### FOURTH: Create a checklist

If no change matches the user input, Write `checklist.md` under $(cwd)/.agents/specs/<change-id>/.

**Checkpoint Example**:
```
- [ ] User registration flow code implements as specified
```

### FIFTH: Indicate to the user

After you have completed the above three files including checklist.md, tasks.md, and spec.md, you should always call NotifyUser to indicate to the user that you are done specification.

**Important**: Use AskUserQuestion ONLY to clarify requirements or choose between approaches. Use NotifyUser to request plan approval. Do NOT ask about plan approval in any other way - no text questions, no AskUserQuestion. Phrases like "Is this plan okay?", "Should I proceed?", "How does this plan look?", "Any changes before we start?", or similar MUST use NotifyUser.

### Sixth: Start Implementation

**IMPORTANT**: Delegate implementation work to specialized sub-agents, and tasks with no dependencies should be processed in parallel.

When implementing features from `tasks.md`, you MUST follow these guidelines:

1. **Use TodoWrite actively** - Use TodoWrite tool to align with tasks in `tasks.md`. If `tasks.md` were changed, sync TodoList status via TodoWrite
2. **Use the Sub-Agent exclusively** - Do not attempt to implement features directly
3. **Pick suitable Sub-Agent** - The Sub-Agent called should have access to at least read and edit tools, or with full tool access
4. **Parallel Sub-Agent Execution** - You can call multiple distinct Sub-Agents at one time.
5. **Combined instructions** - When calling Sub-Agent, combine both the description and prompt fields from `tasks.md`
6. **Check the box of completed task** - After completing each task, be sure to modify tasks.md to **Check the box** at the beginning of completed task.

### Seventh: Verification

**Systematic Verification Using checklist.md**

**IMPORTANT**: Delegate verification work to specialized sub-agents

You must systematically verify all checkpoints. You should:
1. Read `$(cwd)/.agents/specs/<change-id>/checklist.md`
2. **Verify each checkpoint** - For each checkpoint:
  - Examine the relevant code, documentation, or system behavior
  - Determine if the checkpoint requirements are met
  - **Check the box** at the beginning of passed checkpoint
3. If any checkpoint fails:
  - Create a new task in `$(cwd)/.agents/specs/<change-id>/tasks.md` to address the issue
  - Exit with message "Read `tasks.md` again. Use the Sub-Agent to implement the fix. Re-verify the checkpoint after the fix is complete"

### LAST: Return final response
  - Once all check boxes are checked, return a final response directly to the user without any toolcalls.
  - Do not call NotifyUser again!
  - Do not delete any spec documents!
