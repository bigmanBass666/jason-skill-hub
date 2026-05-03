#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# long-agent harness — automated multi-session Claude CLI runner
#
# Usage:
#   harness.sh "build a todo app"
#   harness.sh --resume --infinite
#   harness.sh --resume --max-sessions 10
#   harness.sh --resume --dir ./my-project --infinite
#
# Options:
#   --max-sessions N   Stop after N sessions (default: 10)
#   --infinite         Run until all features pass (no session limit)
#   --dir PATH         Project directory (default: current directory)
#   --resume           Skip initializer, go straight to coding agent
#   --dry-run          Print what would run, but don't execute claude
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$SCRIPT_DIR"

TASK=""
MAX_SESSIONS=10
INFINITE=false
PROJECT_DIR="$(pwd)"
RESUME=false
DRY_RUN=false
SKIP_PERMISSIONS=false
LOG_DIR="$HOME/.claude/long-agent-logs"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

while [[ $# -gt 0 ]]; do
  case "$1" in
    --max-sessions)
      MAX_SESSIONS="$2"
      if ! [[ "$MAX_SESSIONS" =~ ^[0-9]+$ ]] || [ "$MAX_SESSIONS" -lt 1 ]; then
        echo -e "${RED}Error: --max-sessions must be a positive integer${RESET}" >&2; exit 1
      fi
      shift 2 ;;
    --infinite)       INFINITE=true;  shift ;;
    --dir)
      PROJECT_DIR="$(cd "$2" 2>/dev/null && pwd)" || { echo -e "${RED}Error: directory '$2' not found${RESET}" >&2; exit 1; }
      shift 2 ;;
    --resume)         RESUME=true;    shift ;;
    --dry-run)        DRY_RUN=true;   shift ;;
    --dangerously-skip-permissions) SKIP_PERMISSIONS=true; shift ;;
    --help|-h)        sed -n '3,17p' "$0" | sed 's/^# \?//'; exit 0 ;;
    -*)               echo -e "${RED}Error: unknown option '$1'${RESET}" >&2; exit 1 ;;
    *)                TASK="$1"; shift ;;
  esac
done

if [ -z "$TASK" ] && [ "$RESUME" = false ]; then
  echo "Error: task description required (or pass --resume)"; exit 1
fi

if [ ! -f "$PLUGIN_DIR/commands/init.md" ] || [ ! -f "$PLUGIN_DIR/commands/code.md" ]; then
  echo "Error: plugin prompts not found in $PLUGIN_DIR/commands/"; exit 1
fi

log()  { echo -e "$@"; }
hr()   { echo -e "${BLUE}────────────────────────────────────────────────────────────${RESET}"; }
ts()   { date '+%Y-%m-%d %H:%M:%S'; }

count_remaining() {
  command -v jq &>/dev/null && [ -f "$PROJECT_DIR/feature_list.json" ] \
    && jq '[.[] | select(.passes == false)] | length' "$PROJECT_DIR/feature_list.json" 2>/dev/null \
    || echo "?"
}
count_total() {
  command -v jq &>/dev/null && [ -f "$PROJECT_DIR/feature_list.json" ] \
    && jq 'length' "$PROJECT_DIR/feature_list.json" 2>/dev/null \
    || echo "?"
}
all_features_pass() {
  if command -v jq &>/dev/null && [ -f "$PROJECT_DIR/feature_list.json" ]; then
    local r; r=$(jq '[.[] | select(.passes == false)] | length' "$PROJECT_DIR/feature_list.json" 2>/dev/null || echo "1")
    [ "$r" -eq 0 ]
  else
    grep -q "^STATUS: COMPLETE" "$PROJECT_DIR/claude-progress.txt" 2>/dev/null
  fi
}

# ── run_claude ────────────────────────────────────────────────────────────────
# ROOT CAUSE of blank output (confirmed via GitHub issues):
#   `claude -p --verbose` is NOT live-streaming. It buffers all output and only
#   prints after the session ends — by design. This is a known limitation.
#   See: https://github.com/anthropics/claude-code/issues/4346
#
# FIX: use --output-format stream-json which emits NDJSON lines in real time.
#   We parse each line with jq to render human-readable output as it streams.
#   Tool calls, text, and results all appear live.
# ─────────────────────────────────────────────────────────────────────────────
run_claude() {
  local session_num="$1"
  local prompt="$2"
  mkdir -p "$LOG_DIR"
  local log_file="$LOG_DIR/session-$(printf '%03d' "$session_num")-$(date +%Y%m%d-%H%M%S).jsonl"

  if [ "$DRY_RUN" = true ]; then
    log "${CYAN}[DRY RUN] claude -p ... --output-format stream-json | jq ...${RESET}"; return 0
  fi

  local skip_flag=""
  [ "$SKIP_PERMISSIONS" = true ] && skip_flag="--dangerously-skip-permissions"

  log "${CYAN}  Log → $log_file${RESET}"

  local exit_code=0
  pushd "$PROJECT_DIR" > /dev/null

  # Stream NDJSON from claude, tee raw log, parse live for terminal display.
  #
  # jq filter explanation:
  #   - assistant text blocks  → printed as-is
  #   - tool_use (Bash/Read…)  → show "▶ ToolName: input_summary"
  #   - tool_result            → show "◀ result (first 120 chars)"
  #   - result (final summary) → show cost + duration
  claude -p "$prompt" $skip_flag --verbose --output-format stream-json \
    | tee "$log_file" \
    | jq -rj '
        if .type == "assistant" then
          ( .message.content // [] )
          | .[]
          | if .type == "text" then .text
            elif .type == "tool_use" then
              "\n\u001b[35m▶ \(.name)\u001b[0m: " +
              ( .input | to_entries | map("\(.key)=\(.value | tostring | .[0:80])") | join(" ") ) + "\n"
            else empty end
        elif .type == "tool_result" then
          "\u001b[36m◀ " +
          ( [ .content[]? | select(.type=="text") | .text ] | join("") | .[0:120] | gsub("\n";" ") ) +
          "\u001b[0m\n"
        elif .type == "result" then
          "\n\u001b[32m✓ done\u001b[0m" +
          (if .total_cost_usd then "  cost=$\(.total_cost_usd | . * 1000 | round / 1000)" else "" end) +
          (if .duration_ms then "  \(.duration_ms / 1000 | . * 10 | round / 10)s" else "" end) +
          "\n"
        else empty end
      ' 2>/dev/null \
    || exit_code=$?

  popd > /dev/null

  [ $exit_code -ne 0 ] && log "${YELLOW}  ⚠ Session $session_num exited with code $exit_code${RESET}"
  return $exit_code
}

build_init_prompt() {
  printf '%s\n\n%s' "$1" "$(cat "$PLUGIN_DIR/commands/init.md")"
}

# ── Banner ────────────────────────────────────────────────────────────────────
hr
log "${BOLD}  long-agent harness${RESET}"
log "  Project : ${CYAN}$PROJECT_DIR${RESET}"
[ "$RESUME" = false ] && log "  Task    : ${CYAN}$TASK${RESET}"
[ "$INFINITE" = true ] && log "  Limit   : ${CYAN}unlimited sessions${RESET}" \
                       || log "  Limit   : ${CYAN}max $MAX_SESSIONS sessions${RESET}"
log "  Logs    : ${CYAN}$LOG_DIR${RESET}"
hr

SESSION=1

if [ "$RESUME" = false ] && [ ! -f "$PROJECT_DIR/feature_list.json" ]; then
  log ""; log "${BOLD}🚀 Session 1 — Initializer agent${RESET}"; log "   $(ts)"
  run_claude 1 "$(build_init_prompt "$TASK")" || true
  SESSION=2
  MISSING=()
  [ ! -f "$PROJECT_DIR/feature_list.json" ]   && MISSING+=("feature_list.json")
  [ ! -f "$PROJECT_DIR/claude-progress.txt" ] && MISSING+=("claude-progress.txt")
  [ ! -f "$PROJECT_DIR/init.sh" ]             && MISSING+=("init.sh")
  if [ ${#MISSING[@]} -gt 0 ]; then
    log "${RED}⚠ Missing: ${MISSING[*]}${RESET}"
    log "  Resume with: ${CYAN}harness.sh --resume --dir \"$PROJECT_DIR\"${RESET}"; exit 1
  fi
  log "${GREEN}✓ Initializer complete — $(count_total) features${RESET}"

elif [ "$RESUME" = true ]; then
  if [ -f "$PROJECT_DIR/claude-progress.txt" ]; then
    LAST=$(grep -oP '(?<=Session )\d+' "$PROJECT_DIR/claude-progress.txt" 2>/dev/null | tail -1 || true)
    SESSION=$(( ${LAST:-1} + 1 ))
  fi
  log "${CYAN}Resuming from session $SESSION${RESET}"

else
  log "${CYAN}feature_list.json found — skipping initializer${RESET}"
fi

CODE_PROMPT=$(cat "$PLUGIN_DIR/commands/code.md")

while true; do
  hr
  REMAINING=$(count_remaining); TOTAL=$(count_total)

  if all_features_pass; then
    log ""; log "${GREEN}${BOLD}✅ All features passing! Task complete.${RESET}"
    log "   Sessions: $((SESSION-1))   Features: $TOTAL/$TOTAL"
    tail -20 "$PROJECT_DIR/claude-progress.txt" 2>/dev/null || true
    exit 0
  fi

  if [ "$INFINITE" = false ] && [ "$SESSION" -gt "$MAX_SESSIONS" ]; then
    log ""; log "${YELLOW}${BOLD}⏹ Reached max sessions ($MAX_SESSIONS).${RESET}"
    log "   Remaining: ${REMAINING}/${TOTAL}"
    log "   ${CYAN}harness.sh --resume --dir \"$PROJECT_DIR\" --infinite${RESET}"; exit 1
  fi

  log ""; log "${BOLD}🔄 Session $SESSION — Coding agent${RESET}"
  log "   $(ts)   Features remaining: ${CYAN}${REMAINING}/${TOTAL}${RESET}"

  run_claude "$SESSION" "$CODE_PROMPT" || true
  SESSION=$((SESSION + 1))
done
