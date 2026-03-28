#!/bin/bash
# Bootstrap script for Claude's memory system
# Called by SessionStart hook to generate context injection

CWD="$(cd "$(dirname "$0")/.." && pwd)"
TODAY=$(date +%Y-%m-%d)
DOW=$(date +%u)  # 1=Monday, 7=Sunday

# Find the latest journal entry
LATEST_JOURNAL=$(ls -1 "$CWD/journal/"*.md 2>/dev/null | grep -E '[0-9]{4}-[0-9]{2}-[0-9]{2}' | sort -r | head -1)
LATEST_DATE=""
if [ -n "$LATEST_JOURNAL" ]; then
  LATEST_DATE=$(basename "$LATEST_JOURNAL" .md)
fi

# Check if weekly review is due (Monday, or no review this week)
WEEK_NUM=$(date +%Y-W%V)
WEEKLY_EXISTS="false"
if [ -f "$CWD/journal/weekly/${WEEK_NUM}.md" ]; then
  WEEKLY_EXISTS="true"
fi

# Build context message
MSG="[AUTO-BOOTSTRAP] 启动协议激活。"
MSG="$MSG 今天: $TODAY。"

if [ -n "$LATEST_DATE" ] && [ "$LATEST_DATE" != "$TODAY" ]; then
  MSG="$MSG 上次工作日期: $LATEST_DATE（不是今天，需要检查未完成项）。"
fi

if [ "$DOW" = "1" ] && [ "$WEEKLY_EXISTS" = "false" ]; then
  MSG="$MSG 今天是周一且本周尚无周复盘，完成当前任务后考虑生成 journal/weekly/${WEEK_NUM}.md。"
fi

MSG="$MSG 必须执行: 1) 读 SOUL.md 2) 读 USER.md 3) 读最新日记 ${LATEST_JOURNAL:-'(无)'} 4) 读 HISTORY.md。"

# Output as JSON for Claude Code hook system
echo "{\"hookSpecificOutput\":{\"additionalContext\":\"$MSG\"}}"
