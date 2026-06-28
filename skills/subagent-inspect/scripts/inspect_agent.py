import json, sys, argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Inspect Claude Code agent execution trace from JSONL"
    )
    parser.add_argument("jsonl", help="Path to JSONL transcript file")
    parser.add_argument(
        "--filter",
        choices=["Read", "Skill", "Bash", "PowerShell", "Glob", "Grep",
                 "AskUserQuestion", "Agent", "Write", "Edit"],
        help="Only show events matching this tool",
    )
    parser.add_argument(
        "--no-truncate", action="store_true",
        help="Show full content, no truncation",
    )
    parser.add_argument(
        "--stats", action="store_true",
        help="Print summary statistics after the trace",
    )
    return parser.parse_args()


def truncate(text, limit=300):
    if isinstance(text, str) and len(text) > limit:
        return text[:limit] + "..."
    return text


args = parse_args()
LIMIT = None if args.no_truncate else 300
tool_counts = {}
matching = 0
total = 0

with open(args.jsonl, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue

        t = d.get("type", "?")

        # Stats: count tool calls from assistant messages
        if t == "assistant":
            for block in d.get("message", {}).get("content", []):
                if block.get("type") == "tool_use":
                    name = block.get("name", "?")
                    tool_counts[name] = tool_counts.get(name, 0) + 1

        # Filter: when --filter is set, skip non-matching events
        if args.filter and t == "assistant":
            blocks = d.get("message", {}).get("content", [])
            has_match = any(
                b.get("type") == "tool_use" and b.get("name") == args.filter
                for b in blocks
            )
            if not has_match:
                total += 1
                if t in ("user", "assistant", "tool_result"):
                    matching += 1
                continue

        # Print event
        if t == "user":
            c = d.get("message", {}).get("content", "")
            if isinstance(c, list):
                c = str(c)
            print(f'[USER {i}] {truncate(str(c), LIMIT)}')

        elif t == "assistant":
            msg = d.get("message", {})
            for block in msg.get("content", []):
                bt = block.get("type", "?")
                if bt == "text":
                    print(f'[TEXT {i}] {truncate(block["text"], LIMIT)}')
                elif bt == "tool_use":
                    inp = json.dumps(block.get("input", {}), ensure_ascii=False)
                    print(f'[TOOL {i}] {block["name"]}({truncate(inp, LIMIT)})')
                elif bt == "thinking":
                    print(f'[THINKING {i}] {truncate(block.get("thinking", ""), LIMIT)}')

        elif t == "tool_result":
            content = str(d.get("content", ""))
            print(f'[RESULT {i}] {truncate(content[:LIMIT], LIMIT)}')

        total += 1
        if args.filter and t in ("user", "assistant", "tool_result"):
            matching += 1

    # Summary stats
    if args.stats:
        print("\n=== Stats ===")
        print(f"Total events: {total}")
        if args.filter:
            print(f"Matching '{args.filter}': {matching}")
        print("Tool call counts:")
        for name, count in sorted(tool_counts.items(), key=lambda x: -x[1]):
            print(f"  {name}: {count}")
