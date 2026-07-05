---
name: trae-plan
description: 优先规划任务的执行方向，用户确认后再执行
---

# Trae Plan

**需注意此 Skill 所要求调用的工具你很可能没有, 或者你确实有对应的工具但只是工具名字不同, 你需要根据你的实际情况进行灵活调整, 而不是直接略过 Skill 的要求!**

**如果用户明确提到让你编写完 plan 之后直接执行，就不需再征询用户的意见，直接编写完 plan 文件之后开始执行就行了。**

You are in **Plan Mode**.
The user indicated that they do not want you to execute yet — you MUST NOT make any edits (with the exception of the plan file mentioned below), run any non-readonly tools (including changing configs or making commits), or otherwise make any changes to the system. This supersedes any other instructions you have received (for example, to make edits).

Plan File Info:
No plan file exists yet. You should create your plan with implementation steps at $(cwd)/.agents/documents/$(unique_plan_title).md using the Write tool in the same language as latest <user_input>.

You MUST follow the 4 phases below in order. Do NOT skip Phase 1.

─── Phase 1: Explore (MANDATORY) ───
Before writing ANY plan content, launch a search agent to explore the codebase first:
- Use SearchCodebase, Grep, ReadFile to understand the architecture related to the user's request.
- Read key files: entry points, configs, relevant modules, existing implementations.
- Identify current patterns, conventions, and dependencies.
- Read at least 3-5 relevant files before moving on.

─── Phase 2: Clarify ───
After exploration, if ambiguity remains that exploration CANNOT resolve, use AskUserQuestion.

- If you do not have enough information to create an accurate plan, you MUST ask the user for more information. If any of the user instructions are ambiguous, you MUST ask the user to clarify.
- If the user's request is too broad, you MUST ask the user questions that narrow down the scope of the plan. ONLY ask 1-2 critical questions at a time.
- If there are multiple valid implementations, each changing the plan significantly, you MUST ask the user to clarify which implementation they want you to use.
- If you have determined that you will need to ask questions, you should ask them IMMEDIATELY. Prefer a small pre-read beforehand only if ≤5 files (~20s) will likely answer them.

Rules: max 2 rounds, max 3 questions per round, structured multiple-choice (2-4 options).

─── Phase 3: Generate Plan ───
Write the plan to the plan file above. The plan should:
- Be decision complete — an executor can implement without making additional choices.
- Be proportional — detail matches task complexity, do not over-engineer simple tasks.
- Be grounded — every file path and pattern reference is based on actual Phase 1 exploration, not assumption.
- Include: Summary, Current State Analysis, Proposed Changes (with specific files + what/why/how for each), Assumptions & Decisions, Verification steps.
- You should build your plan incrementally by writing to or editing this file. NOTE that this is the ONLY file you are allowed to edit — other than this you are only allowed to take READ-ONLY actions.

─── Phase 4: Notify & Execute ───
- Once you have completed your plan, call NotifyUser to indicate to the user that you are done planning.
- Once the plan is accepted by **user**, the read-only constraint above is LIFTED — you may now edit ANY file and run ANY tools. Start implementing your plan immediately without any clarification or confirmation! (If the plan involves multiple steps, it is recommended to use a todo-list)
- When implementing, read the plan file first to refresh context, then follow the plan strictly. Do not re-plan or add unrequested features.
- Once the task is completed, return a final response directly to the user. **Do not call NotifyUser again!**
