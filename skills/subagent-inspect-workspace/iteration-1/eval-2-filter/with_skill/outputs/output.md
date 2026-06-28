# Eval 2: Read 工具调用审计

找到 D--Test-claude-test-subagent-test，5个subagent全部为Explore类型。
**Read 调用全部为 0**。这些 agent 只用 web-search 和 web fetch 类工具。

附加发现：agent-a179 在第36行调用了错误工具名 `mcp__web-fetch__fetchWebContent`，连续报错2次后纠正。
