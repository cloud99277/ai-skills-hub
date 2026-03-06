#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────────────────────
# AI Skills Hub — Uninstall Script
#
# Removes the symlinks created by setup.sh.
# Does NOT delete any user-created skills or the repository itself.
# ─────────────────────────────────────────────────────────────

AI_SKILLS_HOME="$HOME/.ai-skills"

AGENT_DIRS=(
    "$HOME/.claude/skills"
    "$HOME/.codex/skills"
    "$HOME/.gemini/skills"
    "$HOME/.agents/skills"
)

info()  { printf "\033[1;34m[INFO]\033[0m  %s\n" "$1"; }
ok()    { printf "\033[1;32m[OK]\033[0m    %s\n" "$1"; }
warn()  { printf "\033[1;33m[WARN]\033[0m  %s\n" "$1"; }

echo ""
echo "AI Skills Hub — Uninstall"
echo ""

# Remove agent symlinks
for agent_dir in "${AGENT_DIRS[@]}"; do
    if [[ -L "$agent_dir" ]]; then
        rm "$agent_dir"
        ok "Removed symlink: $agent_dir"
    elif [[ -e "$agent_dir" ]]; then
        warn "$agent_dir is not a symlink, skipping"
    else
        info "$agent_dir does not exist, nothing to remove"
    fi
done

# Remove ~/.ai-skills symlink (only if it's a symlink, not a real directory)
if [[ -L "$AI_SKILLS_HOME" ]]; then
    rm "$AI_SKILLS_HOME"
    ok "Removed symlink: $AI_SKILLS_HOME"
elif [[ -d "$AI_SKILLS_HOME" ]]; then
    warn "$AI_SKILLS_HOME is a real directory, not removing"
    info "If you want to remove it, delete it manually: rm -rf $AI_SKILLS_HOME"
else
    info "$AI_SKILLS_HOME does not exist, nothing to remove"
fi

echo ""
ok "Uninstall complete. Your repository and any created skills are untouched."
