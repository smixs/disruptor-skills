#!/usr/bin/env bash
# Disruptor — быстрый установщик Claude Code скилла.
#
#   curl -fsSL https://raw.githubusercontent.com/smixs/disruptor-skills/main/install.sh | bash
#   ./install.sh              # personal:  ~/.claude/skills/disruptor  (во всех проектах)
#   ./install.sh --project    # project:   ./.claude/skills/disruptor  (только этот репо)
#
set -euo pipefail

REPO_URL="${DISRUPTOR_REPO:-https://github.com/smixs/disruptor-skills.git}"
NAME="disruptor"

if [ "${1:-}" = "--project" ]; then
  BASE=".claude/skills"
else
  BASE="$HOME/.claude/skills"
fi
DEST="$BASE/$NAME"

echo "→ Устанавливаю '$NAME' → $DEST"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

git clone --depth 1 "$REPO_URL" "$TMP" >/dev/null 2>&1

mkdir -p "$DEST"
cp "$TMP/SKILL.md" "$DEST/"
rm -rf "$DEST/references"
cp -R "$TMP/references" "$DEST/"

echo "✓ Готово. Открой Claude Code — скилл 'disruptor' подхватится сам (или перезапусти сессию)."
echo "  Проверка: файлы лежат в $DEST/ (SKILL.md + references/)."
