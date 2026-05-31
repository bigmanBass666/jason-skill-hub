# MCP Testing Guide

Detailed methodology for systematically testing MCP server tools before writing sub-agent prompts.

## Testing Philosophy

MCP servers are third-party software. Their documentation may be incomplete, outdated, or wrong. The only reliable way to understand how an MCP tool behaves is to call it yourself and observe the result. This guide provides a structured approach to testing that ensures you discover all bugs, limitations, and unexpected behaviors before they end up in a sub-agent prompt.

## Pre-Test Preparation

### 1. Identify All Tools

Scan your available tools for the target MCP server's prefix (e.g., `mcp_universal-db_*`, `mcp_filesystem_*`). For each tool, extract:

- Tool name
- Parameter names, types, required/optional status
- Description text (from tool schema)
- Any enum constraints on parameters

### 2. Classify Tools by Risk Level

| Risk Level | Criteria | Testing Intensity |
|------------|----------|-------------------|
| Read-only | No side effects, no state changes | Standard — test happy path + errors |
| Stateful-read | Reads but requires prior state (e.g., must connect first) | Test state dependencies thoroughly |
| Write | Modifies data or state | Test with verification read-back after every write |
| Destructive | Irreversible changes (delete, drop, remove) | Test with safe targets only; verify rollback impossible |

### 3. Prepare Test Fixtures

Create minimal test data that exercises each tool. For example:
- Database MCP: create a small SQLite file with 2-3 tables
- Filesystem MCP: create a temp directory with sample files
- Browser MCP: identify a stable, simple test URL

Test fixtures must be:
- **Reproducible** — can be recreated from a script
- **Isolated** — won't affect real user data
- **Small** — fast to create and clean up

## Testing Checklist

For EACH tool, work through this checklist:

### A. Happy Path

| # | Test | What to Verify |
|---|------|----------------|
| 1 | Call with minimal required params | Returns success with expected data structure |
| 2 | Call with all params (including optional) | Optional params are accepted and affect output |
| 3 | Call with typical realistic input | Output matches expected domain behavior |

### B. Error Path

| # | Test | What to Verify |
|---|------|----------------|
| 4 | Missing required parameter | Returns clear error, no side effects |
| 5 | Invalid parameter type | Returns clear error, no side effects |
| 6 | Invalid parameter value (out of range) | Returns clear error, no side effects |
| 7 | Nonexistent resource (e.g., wrong ID, bad path) | Returns clear error, no side effects |
| 8 | Operation on invalid state (e.g., query before connect) | Returns clear error, no side effects |

### C. Edge Cases

| # | Test | What to Verify |
|---|------|----------------|
| 9 | Empty input/result | Handles gracefully, no crash |
| 10 | Very large input/result | Performance acceptable, no truncation or timeout |
| 11 | Special characters in input | No injection, encoding issues |
| 12 | Unicode/non-ASCII input | Handled correctly |
| 13 | Concurrent operations (if applicable) | No race conditions or data corruption |

### D. Cross-Tool Interactions

| # | Test | What to Verify |
|---|------|----------------|
| 14 | Tool B after Tool A succeeds | B works correctly with A's output |
| 15 | Tool B after Tool A fails | B handles A's failure gracefully |
| 16 | Tool A → Tool B → Tool A (re-entry) | State is consistent |
| 17 | Cleanup after partial failure | Resources are released |

### E. Domain-Specific Tests

These depend on the MCP server's domain. Examples:

**Database MCP:**
- Schema introspection (PRAGMA, information_schema, SHOW TABLES)
- Transaction behavior (does write auto-commit?)
- Connection string format variations
- Multiple simultaneous connections

**Filesystem MCP:**
- Symlink handling
- Permission errors
- Path traversal security
- Binary file handling

**Browser MCP:**
- Page load timeout
- JavaScript execution
- Authentication flows
- File download handling

## Bug Documentation Template

For each bug discovered, record:

```markdown
### Bug: [Short Title]

**Tool:** `tool_name`
**Severity:** Critical / Major / Minor / Note
**Reproduction:**
1. Step one
2. Step two
3. Observe: [what happens]

**Expected:** [what should happen]
**Actual:** [what actually happens]
**Workaround:** [how to achieve the goal despite the bug]
**Impact on Agent:** [how this affects sub-agent behavior]
```

## Bug Severity Classification

### Critical
The tool is unusable, causes data loss, or produces silently wrong results. The sub-agent MUST NOT use this tool, or must use it only with extreme safeguards.

Example: `query_write` silently drops data without error.

### Major
The tool works but returns misleading information. The sub-agent can use it but must verify results through an alternative path.

Example: `query_write` returns an error message, but the operation actually succeeds. The agent must verify with a read-back.

### Minor
The tool works correctly but has cosmetic or convenience issues. The sub-agent can use it normally but should handle the quirk gracefully.

Example: Connection returns success before actually validating, causing delayed errors.

### Note
Unexpected but harmless behavior. Worth documenting so the agent isn't confused, but no workaround needed.

Example: Tool returns results in a slightly different format than documented.

## Testing Anti-Patterns

**Don't:**
- Test only the happy path — errors reveal more about tool behavior than successes
- Trust documentation over observation — doc says X, tool does Y → trust the tool
- Skip cleanup between tests — leftover state can cause false positives/negatives
- Test with production data — always use isolated fixtures
- Assume idempotency — test what happens when you call the same tool twice

**Do:**
- Test in a fresh environment for each tool group
- Record exact error messages — the sub-agent prompt needs them for error recovery
- Test parameter boundaries — empty strings, zero, maximum values
- Verify side effects independently — if a write tool claims success, check with a read tool
- Document what you DIDN'T test — future testers should know the gaps

## Real-World Bug Examples

These are actual bugs found during MCP testing. Use them as inspiration for what to look for.

### Example 1: Silent Write Success with Error Message
- **Tool:** `query_write` (MCP Universal DB Client)
- **Bug:** Returns `"Error: Do not know how to serialize a BigInt"` but the write operation actually executes successfully
- **Severity:** Major
- **Workaround:** Always verify writes with a subsequent `query_read`
- **Impact:** Agent must never trust query_write's error message at face value

### Example 2: Lazy Connection Validation
- **Tool:** `connect_database` (MCP Universal DB Client)
- **Bug:** Returns "Connected" even when the server is unreachable. Errors only surface at query time.
- **Severity:** Minor
- **Workaround:** After connecting, immediately run a simple query (e.g., `SELECT 1`) to validate the connection
- **Impact:** Agent should not report "connection successful" until a query actually works

### Example 3: SQL Parser Rejects Valid SQL
- **Tool:** `query_read` (MCP Universal DB Client)
- **Bug:** The SQL parser rejects `PRAGMA` statements and `sqlite_master` queries that are valid SQLite SQL
- **Severity:** Major
- **Workaround:** Use standard SQL alternatives (SELECT with LIMIT for schema discovery)
- **Impact:** Agent cannot use SQLite-specific introspection; must use workarounds for schema discovery
