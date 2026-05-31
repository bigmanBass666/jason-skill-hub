---
name: long-running-agent
description: Long-running agent implementation based on Anthropic's "Effective harnesses for long-running agents" article
---

# Long-Running Agent Skill

A comprehensive implementation of Anthropic's long-running agent pattern for Claude Code.

## Features

- **Initializer Agent** (`init`): Analyzes requirements and creates detailed feature lists
- **Coding Agent** (`code`): Implements features incrementally with strict 10-step process
- **Automation Mode** (`auto`): Full automation with task queue management
- **Context Management**: Handles multi-session workflows with clean context state
- **Browser Testing**: Mandatory end-to-end browser automation testing

## Quick Start

```bash
# Initialize a new project
/long-running-agent init "Build a task management application"

# Start automated development
/long-running-agent auto --time-limit 8

# Check progress anytime
/long-running-agent status
```

## Core Design

Based on Anthropic's research on effective harnesses for long-running agents, this skill implements:

1. **Two-phase agent architecture**: Initializer Agent + Coding Agent
2. **Strict incremental progress**: One feature at a time
3. **Comprehensive failure prevention**: 12 layers of protection
4. **State persistence**: File-based state management with recovery
5. **Automation orchestration**: Task queue management and session control

## File Structure

Required files created by the skill:
- `feature_list.json` - Complete feature list (200+ items)
- `claude-progress.txt` - Session-by-session progress log
- `init.sh` - Environment setup script
- `app_spec.txt` - Project specification
- `task_queue.json` - Automation task queue

## Context Management

The skill addresses the core challenge of long-running agents: working across multiple context windows without memory. It implements:

- **File-based state persistence**: All progress saved to filesystem
- **Git history tracking**: Full code change history
- **Session recovery**: Checkpoint system for interruption recovery
- **Context cleanup**: Regular `/clear` and `/compact` integration

## Browser Automation Testing

Every feature requires end-to-end browser automation testing using Playwright MCP:

- Real UI interaction (clicks, typing, navigation)
- Screenshot verification
- Console error checking
- Full user flow validation

## Automation Features

- **Smart task selection**: Priority-based feature queue
- **Session monitoring**: Timeout and failure detection
- **Progress tracking**: Real-time statistics and reporting
- **Quality gates**: Automated code quality checks
- **Failure recovery**: Intelligent retry mechanisms

## Usage Examples

```bash
# Manual development mode
/long-running-agent init "Build an e-commerce website"
/long-running-agent code  # Complete feature #1
/long-running-agent code  # Complete feature #2

# Full automation
/long-running-agent auto --max-sessions 5 --time-limit 4

# Control automation
/long-running-agent pause     # Pause after current session
/long-running-agent resume    # Resume automation
/long-running-agent status    # Check current status
```

## Advanced Configuration

Customize through `task_queue.json`:
```json
{
  "settings": {
    "max_consecutive_failures": 3,
    "auto_restart": true,
    "session_timeout_minutes": 120,
    "max_sessions_per_day": 10,
    "quality_gate_enabled": true
  }
}
```

Environment variables:
```bash
export LRA_SESSION_TIMEOUT=180      # Session timeout in minutes
export LRA_MAX_SESSIONS_PER_DAY=20  # Daily session limit
export LRA_DEBUG=true               # Enable debug logging
```

## Version History

**v2.0** (Current):
- Full automation mode (`auto` command)
- Task queue management system
- State persistence and recovery
- Checkpoint system
- Smart session management
- Progress monitoring and reporting

**v1.0** (Initial):
- Initializer Agent (`init`)
- Coding Agent (`code`)
- Basic failure prevention
- Key file management

---

*Based on Anthropic's article "Effective harnesses for long-running agents" and Claude Agent SDK best practices.*