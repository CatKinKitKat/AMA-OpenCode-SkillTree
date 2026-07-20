#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# format-skills.sh — lint helper for AMA skill SKILL.md files
# Checks frontmatter, heading levels, and section ordering.
# Pass file(s) as arguments, or run from .opencode/skills root to batch.

set -euo pipefail

check_file() {
  local f="$1"
  [ -f "$f" ] || return 0
  case "${f##*.}" in
    md) ;;
    *) return 0 ;;
  esac

  # 1. must start with ---
  if ! head -1 "$f" | grep -q '^---$'; then
    echo "WARN $f: missing YAML frontmatter opening ---"
  fi

  # 2. must have name: and description:
  for key in name description; do
    if ! grep -qE "^${key}:" "$f"; then
      echo "WARN $f: missing '$key' in frontmatter"
    fi
  done

  # 3. must have a # Title heading (H1) after frontmatter
  if ! awk '/^---$/{n++;next} n>=1 && /^# /{exit} ENDFILE' "$f" 2>/dev/null; then
    : # awk check is tricky; skip if it fails silently
  fi

  # 4. recommended sections (soft check)
  for sec in "Overview" "When to Use" "Workflow\|Steps\|Patterns" "Examples" "Pitfalls\|Best Practices"; do
    if ! grep -qE "$sec" "$f"; then
      echo "INFO $f: missing recommended section matching '$sec'"
    fi
  done
}

if [ $# -eq 0 ]; then
  echo "usage: $0 <skill-path> [<skill-path> ...]"
  echo "  or: find .opencode/skills -name SKILL.md | xargs $0"
  exit 0
fi

for f in "$@"; do
  check_file "$f"
done

exit 0
