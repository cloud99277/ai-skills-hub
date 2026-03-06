#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────────────────────
# AI Skills Hub — Setup Script
#
# This script sets up the centralized skill system by:
#   1. Linking (or copying) this repo to ~/.ai-skills
#   2. Creating agent-specific symlinks so all CLI tools share
#      the same skill catalog
#   3. Verifying Python 3 + PyYAML are available
# ─────────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AI_SKILLS_HOME="$HOME/.ai-skills"

# Agent entry points that should symlink to the centralized repo
# Note: ~/.gemini/skills is intentionally excluded because Gemini CLI
# also scans ~/.agents/skills — having both causes duplicate skill conflicts.
AGENT_DIRS=(
    "$HOME/.claude/skills"
    "$HOME/.codex/skills"
    "$HOME/.agents/skills"
)

# ── Helpers ──────────────────────────────────────────────────

info()  { printf "\033[1;34m[INFO]\033[0m  %s\n" "$1"; }
ok()    { printf "\033[1;32m[OK]\033[0m    %s\n" "$1"; }
warn()  { printf "\033[1;33m[WARN]\033[0m  %s\n" "$1"; }
err()   { printf "\033[1;31m[ERROR]\033[0m %s\n" "$1"; }

confirm() {
    local prompt="$1"
    local default="${2:-y}"
    if [[ "$default" == "y" ]]; then
        prompt="$prompt [Y/n] "
    else
        prompt="$prompt [y/N] "
    fi
    read -rp "$prompt" answer
    answer="${answer:-$default}"
    [[ "$answer" =~ ^[Yy] ]]
}

# ── Step 1: Set up ~/.ai-skills ─────────────────────────────

setup_ai_skills_home() {
    if [[ "$SCRIPT_DIR" == "$AI_SKILLS_HOME" ]]; then
        ok "Repository is already at $AI_SKILLS_HOME"
        return
    fi

    if [[ -e "$AI_SKILLS_HOME" ]]; then
        if [[ -L "$AI_SKILLS_HOME" ]]; then
            local current_target
            current_target="$(readlink -f "$AI_SKILLS_HOME")"
            if [[ "$current_target" == "$SCRIPT_DIR" ]]; then
                ok "$AI_SKILLS_HOME already points to this repository"
                return
            fi
            warn "$AI_SKILLS_HOME is a symlink pointing to: $current_target"
            if confirm "Replace it to point to this repository?"; then
                rm "$AI_SKILLS_HOME"
            else
                err "Aborted. Please resolve $AI_SKILLS_HOME manually."
                exit 1
            fi
        elif [[ -d "$AI_SKILLS_HOME" ]]; then
            warn "$AI_SKILLS_HOME already exists as a directory"
            echo "  Options:"
            echo "    1) Back up existing directory and replace with symlink (recommended)"
            echo "    2) Abort"
            read -rp "  Choose [1/2]: " choice
            case "$choice" in
                1)
                    local backup="$AI_SKILLS_HOME.backup.$(date +%Y%m%d%H%M%S)"
                    mv "$AI_SKILLS_HOME" "$backup"
                    ok "Backed up existing directory to $backup"
                    ;;
                *)
                    err "Aborted. Please resolve $AI_SKILLS_HOME manually."
                    exit 1
                    ;;
            esac
        else
            err "$AI_SKILLS_HOME exists but is not a directory or symlink."
            exit 1
        fi
    fi

    ln -s "$SCRIPT_DIR" "$AI_SKILLS_HOME"
    ok "Created symlink: $AI_SKILLS_HOME -> $SCRIPT_DIR"
}

# ── Step 2: Create agent entry-point symlinks ────────────────

setup_agent_symlinks() {
    for agent_dir in "${AGENT_DIRS[@]}"; do
        local parent_dir
        parent_dir="$(dirname "$agent_dir")"

        # Create parent directory if it doesn't exist
        if [[ ! -d "$parent_dir" ]]; then
            mkdir -p "$parent_dir"
        fi

        if [[ -L "$agent_dir" ]]; then
            local current_target
            current_target="$(readlink -f "$agent_dir")"
            local expected_target
            expected_target="$(readlink -f "$AI_SKILLS_HOME")"
            if [[ "$current_target" == "$expected_target" ]]; then
                ok "$agent_dir already linked"
                continue
            fi
            warn "$agent_dir points to $current_target, updating..."
            rm "$agent_dir"
        elif [[ -d "$agent_dir" ]]; then
            warn "$agent_dir exists as a real directory, skipping (resolve manually)"
            continue
        fi

        ln -s "$AI_SKILLS_HOME" "$agent_dir"
        ok "Linked: $agent_dir -> $AI_SKILLS_HOME"
    done
}

# ── Step 3: Check dependencies ──────────────────────────────

check_dependencies() {
    # Python 3
    if command -v python3 &>/dev/null; then
        local py_version
        py_version="$(python3 --version 2>&1)"
        ok "Python 3 found: $py_version"
    else
        err "Python 3 is required but not found. Please install Python 3.8+."
        exit 1
    fi

    # PyYAML
    if python3 -c "import yaml" 2>/dev/null; then
        ok "PyYAML is available"
    else
        warn "PyYAML is not installed. Some scripts require it."
        if confirm "Install PyYAML now? (pip3 install pyyaml)"; then
            pip3 install pyyaml
            ok "PyYAML installed"
        else
            warn "Skipping PyYAML installation. You'll need to install it manually."
        fi
    fi
}

# ── Step 4: Run a quick self-test ────────────────────────────

self_test() {
    info "Running quick self-test..."
    local lint_script="$AI_SKILLS_HOME/.system/skill-creator/scripts/lint_skills.py"
    if [[ -f "$lint_script" ]]; then
        if python3 "$lint_script" "$AI_SKILLS_HOME" --errors-only >/dev/null 2>&1; then
            ok "Self-test passed: no structural errors found"
        else
            warn "Self-test found issues. Run the full linter for details:"
            echo "  python3 $lint_script $AI_SKILLS_HOME"
        fi
    else
        warn "Lint script not found at $lint_script, skipping self-test"
    fi
}

# ── Main ─────────────────────────────────────────────────────

main() {
    echo ""
    echo "╔══════════════════════════════════════════════════╗"
    echo "║         AI Skills Hub — Setup                   ║"
    echo "║  Centralized skill system for all AI agents     ║"
    echo "╚══════════════════════════════════════════════════╝"
    echo ""

    info "Repository location: $SCRIPT_DIR"
    echo ""

    setup_ai_skills_home
    setup_agent_symlinks
    check_dependencies
    self_test

    echo ""
    echo "────────────────────────────────────────────────────"
    ok "Setup complete!"
    echo ""
    echo "  Your centralized skills live at: $AI_SKILLS_HOME"
    echo ""
    echo "  Next steps:"
    echo "    1. Create your first skill:"
    echo "       python3 $AI_SKILLS_HOME/.system/skill-creator/scripts/init_skill.py my-skill --path $AI_SKILLS_HOME --resources scripts"
    echo ""
    echo "    2. Validate it:"
    echo "       python3 $AI_SKILLS_HOME/.system/skill-creator/scripts/quick_validate.py $AI_SKILLS_HOME/my-skill"
    echo ""
    echo "    3. Lint the whole repository:"
    echo "       python3 $AI_SKILLS_HOME/.system/skill-creator/scripts/lint_skills.py $AI_SKILLS_HOME"
    echo ""
    echo "  All linked agents (Claude, Codex, Gemini, etc.) now share the same skills."
    echo "────────────────────────────────────────────────────"
}

main "$@"
