---
name: sub-agent-designer
description: >
  Design and create sub-agent prompts for MCP servers. Use this skill whenever you need to
  create a specialized sub-agent based on an MCP server's tools, design agent prompts that
  wrap MCP capabilities, or systematically test MCP tools to build reliable agent instructions.
  Trigger on: "design sub-agent", "create sub-agent", "MCP agent prompt", "agent prompt design",
  "sub-agent for MCP", "测试MCP写agent", "设计sub agent", "创建子代理", "MCP子代理",
  "agent prompt", or any request to turn MCP tools into a structured agent prompt.
  Also use when the user mentions wanting to wrap, encapsulate, or specialize an MCP server
  into a reusable agent configuration.
---

# Sub-Agent Designer

Turn any MCP server into a well-crafted sub-agent prompt by systematically testing its tools, discovering bugs and limitations, and writing production-ready agent instructions.

## Why This Skill Exists

MCP servers expose tools, but those tools have hidden quirks: bugs, undocumented limitations, surprising error behaviors. A sub-agent prompt that naively lists the tools will produce unreliable agents. This skill enforces a test-first methodology: you must actually call every MCP tool, discover what really happens, and then write the prompt based on empirical evidence — not documentation claims.

## Core Workflow

```
1. DISCOVER  — Identify all MCP tools and their parameters
2. TEST      — Execute every tool, find bugs and edge cases
3. ANALYZE   — Classify tools, map dependencies, document limitations
4. DESIGN    — Write the sub-agent prompt with invocation triggers
5. VERIFY    — Character count check, consistency review
```

## Phase 1: Discover

Before testing, you need a complete inventory of the MCP server's tools.

**Steps:**
1. Ask the user which MCP server to design for, or detect from conversation context
2. List all available MCP tools — look for tools prefixed with `mcp_` in your available tools
3. For each tool, note: name, parameters (with types and required/optional), description
4. Group tools by category (connection management, read operations, write operations, utility, etc.)

**Output:** A structured tool inventory table.

## Phase 2: Test

This is the most critical phase. You must test EVERY tool with real inputs. Read `references/mcp-testing-guide.md` for the detailed testing methodology.

**Testing priorities:**
1. **Happy path first** — each tool with valid, simple inputs
2. **Error paths** — invalid inputs, missing params, wrong types
3. **Edge cases** — empty results, large results, special characters, concurrent operations
4. **Cross-tool interactions** — does tool B depend on tool A's output? What if A fails?
5. **Boundary testing** — what happens at the limits of each parameter?

**Critical rule:** Never assume a tool works as documented. Test it. Document what ACTUALLY happens, including any discrepancies between expected and actual behavior.

**Bug classification:**
| Severity | Meaning | Example |
|----------|---------|---------|
| Critical | Tool is unusable or data-loss risk | Write operation silently fails |
| Major | Tool works but returns wrong/misleading info | Error message but operation succeeds |
| Minor | Cosmetic or inconvenience | Slow response, ugly formatting |
| Note | Unexpected but not harmful | Connection "succeeds" before validation |

**Output:** A bug/limitation report with severity, reproduction steps, and workarounds.

## Phase 3: Analyze

Synthesize test results into an actionable understanding of the MCP server.

**Analysis dimensions:**
1. **Tool taxonomy** — which tools are primary (user-facing) vs. supporting (lifecycle management)
2. **Dependency graph** — which tools must be called before others (e.g., connect before query)
3. **State machine** — what states exist (disconnected → connected → queried → disconnected)
4. **Error landscape** — what errors can occur, which are recoverable, which are fatal
5. **Capability boundaries** — what the MCP server CANNOT do (as important as what it can)

**Output:** A capability analysis with tool relationships and limitation summary.

## Phase 4: Design

Write the sub-agent prompt. Read `references/prompt-template.md` for the full template structure.

**Prompt must include these sections (in order):**

### 1. Title & One-line Description
The agent's name and what it does in one sentence.

### 2. Main Agent Invocation Triggers
When should the main agent delegate to this sub-agent? List:
- Specific user request patterns (e.g., "analyze a database file")
- Domain keywords in any language (e.g., "数据库", "query", "SQL")
- Contextual signals (e.g., user opened a .db file)
- Explicit exclusion: when NOT to invoke

### 3. Available Tools Reference
For each MCP tool:
- Name and purpose
- Required and optional parameters with types
- Connection/dependency requirements (e.g., "must connect first")
- Key behavioral notes from testing

### 4. Known Issues & Workarounds
Every bug and limitation discovered in Phase 2, with:
- Clear description of the issue
- Concrete workaround steps
- Impact on agent behavior

### 5. Standard Workflows
3-5 common operation sequences as step-by-step pseudocode. Each workflow should:
- Start from a clean state (no existing connections)
- Handle errors at each step
- End with cleanup (disconnect, close, etc.)

### 6. Safety Rules
Domain-specific safety constraints. Always include:
- Default to least-destructive operations
- Always clean up resources
- Never expose credentials in output
- Verify destructive operations with a read-back

### 7. Output Format
Templates for presenting results to the main agent/user. Include:
- Schema/table format for structured data
- Status report format for operations
- Error report format

### 8. Error Recovery Table
A quick-reference table: Error → Cause → Recovery action

**Design principles:**
- Explain WHY, not just WHAT — agents perform better when they understand reasoning
- Keep under 10,000 characters (hard limit for sub-agent prompts)
- Prefer workarounds over warnings — tell the agent what TO do, not just what NOT to do
- Include both English and user's language keywords in invocation triggers

## Phase 5: Verify

Before delivering the prompt:

1. **Character count** — must be under 10,000 characters. If over, trim by:
   - Removing redundant examples
   - Compressing error recovery table
   - Moving detailed references to separate files
2. **Consistency check** — every tool mentioned in workflows must be in the tools reference
3. **Completeness check** — every bug found in testing must have a workaround in the prompt
4. **Trigger accuracy** — invocation triggers should be specific enough to avoid false positives

## File Structure

```
sub-agent-designer/
├── SKILL.md                          (this file — workflow & decision logic)
├── references/
│   ├── mcp-testing-guide.md          (detailed testing methodology)
│   └── prompt-template.md            (sub-agent prompt template with examples)
└── scripts/
    └── char_count.py                 (verify prompt character count)
```

## When to Read Reference Files

- **Phase 2 (Test):** Read `references/mcp-testing-guide.md` for the full testing checklist and bug classification system
- **Phase 4 (Design):** Read `references/prompt-template.md` for the detailed prompt structure with a real-world example

## Adapting to Different MCP Servers

This skill is designed to work with ANY MCP server. The testing and design process is the same regardless of domain. However, the specific test cases and safety rules will differ:

| MCP Domain | Testing Focus | Safety Concerns |
|------------|--------------|-----------------|
| Database | Schema discovery, query limits, write verification | Data modification, credential exposure |
| File system | Path handling, permission errors, encoding | Accidental deletion, overwriting files |
| Browser | Navigation, element selection, timeout | Unintended form submissions, auth sessions |
| API | Rate limits, auth flows, pagination | API key exposure, destructive endpoints |
| Cloud | Resource listing, cost queries, deployment | Accidental provisioning, credential leaks |

Adjust your test cases and safety rules based on the domain. The testing methodology stays the same.
