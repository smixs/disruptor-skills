#!/usr/bin/env bash
# Disruptor — installer for the full Claude Code skill set (all skills/*).
#
#   curl -fsSL https://raw.githubusercontent.com/smixs/disruptor-skills/main/install.sh | bash
#   ./install.sh              # personal:  ~/.claude/skills/<skill>   (all projects)
#   ./install.sh --project    # project:   ./.claude/skills/<skill>   (this repo only)
#
set -euo pipefail

REPO_URL="${DISRUPTOR_REPO:-https://github.com/smixs/disruptor-skills.git}"

if [ "${1:-}" = "--project" ]; then
  BASE=".claude/skills"
else
  BASE="$HOME/.claude/skills"
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "→ Cloning $REPO_URL"
git clone --depth 1 "$REPO_URL" "$TMP" >/dev/null 2>&1

COUNT=0
for SRC in "$TMP"/skills/*/; do
  NAME="$(basename "$SRC")"
  DEST="$BASE/$NAME"
  rm -rf "$DEST"
  mkdir -p "$DEST"
  cp -R "$SRC". "$DEST/"
  COUNT=$((COUNT + 1))
  echo "  ✓ $NAME → $DEST"
done

echo "✓ Installed $COUNT skills into $BASE/."
echo "  Claude Code picks them up automatically (or restart the session)."
