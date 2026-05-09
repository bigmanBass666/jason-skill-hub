# agent-phonebook-skill

Discover MCP servers and find other AI agents -- [AgentPhonebook](https://agentphonebook.org) skill for the [skills.sh](https://skills.sh) ecosystem.

## Install

```bash
npx skills add cairn-agent/agent-phonebook-skill
```

## What You Get

Your AI agent can search a directory of 111+ MCP servers by keyword, tag, transport type, or auth type. Find the right server for your task in seconds, or register your own so other agents can find it.

- **35+ agent support**: Claude Code, Cursor, Windsurf, Copilot, and more
- **Zero dependencies**: Pure REST API -- just curl
- **No auth needed to browse**: Search and discover without registering

## Quick Example

```bash
# Find all SSE-based database servers (remote, no install needed)
curl -sL "https://agentphonebook.org/mcp-servers?transport=sse&tag=database"

# Search by keyword
curl -sL "https://agentphonebook.org/mcp-servers/search?q=analytics"
```

## Full API Reference

See [SKILL.md](SKILL.md) or visit https://agentphonebook.org

## License

MIT
