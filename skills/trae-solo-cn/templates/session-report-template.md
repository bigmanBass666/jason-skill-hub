# TRAE SOLO CN Automation Session Report

| Field | Value |
|-------|-------|
| **Date** | {DATE} |
| **Session ID** | {SESSION_ID} |
| **Workspace** | {WORKSPACE_NAME} |
| **Duration** | {DURATION} |
| **Tasks Completed** | {COUNT} |

---

## Summary

### Tasks Executed

| # | Prompt | Model | Status | Duration | Output |
|---|--------|-------|--------|----------|--------|
| 1 | {PROMPT_1} | {MODEL} | ✅ Complete | {TIME} | [Screenshot](screenshots/task-01.png) |
| 2 | {PROMPT_2} | {MODEL} | ✅ Complete | {TIME} | [Screenshot](screenshots/task-02.png) |
| 3 | {PROMPT_3} | {MODEL} | ❌ Failed | - | [Error](screenshots/task-03-error.png) |

### Key Findings

- {FINDING_1}
- {FINDING_2}
- {FINDING_3}

---

## Detailed Task Log

### Task 01: {TASK_TITLE}

**Prompt:**
```
{FULL_PROMPT_TEXT}
```

**Configuration:**
| Parameter | Value |
|-----------|-------|
| Model | {MODEL_NAME} |
| Workspace | {WORKSPACE} |
| Timeout | {TIMEOUT}s |

**Execution:**
| Step | Action | Timestamp |
|------|--------|-----------|
| 1 | Connect to CDP | {TIME} |
| 2 | Switch workspace | {TIME} |
| 3 | Send prompt | {TIME} |
| 4 | Task completed | {TIME} |

**Result:**
- Status: ✅ Success
- Duration: {DURATION}
- Output captured: Yes
- Screenshot: [task-01-result.png](screenshots/task-01-result.png)

**AI Response Summary:**
{SUMMARY_OF_AI_RESPONSE}

**Artifacts:**
- Full output: [task-01-output.md](outputs/task-01-output.md)
- Progress screenshots: [task-01-progress/](screenshots/task-01-progress/)

---

### Task 02: {TASK_TITLE}

**Prompt:**
```
{FULL_PROMPT_TEXT}
```

**Configuration:**
| Parameter | Value |
|-----------|-------|
| Model | {MODEL_NAME} |
| Workspace | {WORKSPACE} |

**Execution:**
{SIMILAR_STRUCTURE}

**Result:**
{RESULT_DETAILS}

---

## Issues Encountered

### Issue 01: {ISSUE_TITLE}

| Field | Value |
|-------|-------|
| **Severity** | critical / high / medium / low |
| **Category** | connection / ui / timeout / error |
| **Task** | Task #X |
| **Timestamp** | {TIME} |

**Description:**
{WHAT_WENT_WRONG}

**Reproduction Steps:**
1. {STEP_1}
2. {STEP_2}
3. {STEP_3}

**Evidence:**
- Screenshot: [issue-01.png](screenshots/issue-01.png)
- Console errors: {ERROR_MESSAGES}
- Snapshot: [issue-01-snapshot.txt](snapshots/issue-01-snapshot.txt)

**Resolution:**
{HOW_IT_WAS_RESOLVED_OR_WORKAROUND}

---

## Performance Metrics

### Response Times

| Model | Avg Duration | Min | Max | Tasks |
|-------|--------------|-----|-----|-------|
| GLM-5.1 | {AVG}s | {MIN}s | {MAX}s | {COUNT} |
| Claude | {AVG}s | {MIN}s | {MAX}s | {COUNT} |
| GPT-4 | {AVG}s | {MIN}s | {MAX}s | {COUNT} |

### Success Rate

| Metric | Value |
|--------|-------|
| Total Tasks | {COUNT} |
| Successful | {COUNT} ({PERCENT}%) |
| Failed | {COUNT} ({PERCENT}%) |
| Timeout | {COUNT} ({PERCENT}%) |

---

## Screenshots

| File | Description |
|------|-------------|
| [initial-state.png](screenshots/initial-state.png) | Initial app state |
| [workspace-switch.png](screenshots/workspace-switch.png) | Workspace navigation |
| [task-01-result.png](screenshots/task-01-result.png) | Task 1 completion |
| [task-02-result.png](screenshots/task-02-result.png) | Task 2 completion |

---

## Console Output

### JavaScript Errors

```
{CONSOLE_ERROR_LOG}
```

### Network Errors

```
{NETWORK_ERROR_LOG}
```

---

## Appendix: Raw Snapshots

### Snapshot 01 - Initial State

```
{SNAPSHOT_OUTPUT}
```

### Snapshot 02 - Task Running

```
{SNAPSHOT_OUTPUT}
```

### Snapshot 03 - Task Complete

```
{SNAPSHOT_OUTPUT}
```

---

## Recommendations

### For Future Sessions

1. {RECOMMENDATION_1}
2. {RECOMMENDATION_2}
3. {RECOMMENDATION_3}

### For TRAE SOLO CN Improvement

1. {FEEDBACK_1}
2. {FEEDBACK_2}

---

**Report Generated:** {TIMESTAMP}
**Automation Script:** [session-script.ps1](scripts/session-script.ps1)
