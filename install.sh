#!/usr/bin/env bash
# ==============================================================================
# Project Initiator - Universal Multi-Agent One-Line Installer & Skill Setup
# Supports: Google Antigravity, Claude Code, Cursor, Windsurf, Cline, Copilot CLI
# ==============================================================================

set -e

REPO_URL="https://github.com/muchandresh/project_initiator.git"
DEFAULT_INSTALL_DIR="$HOME/.local/share/project-initiator"

# Detect if running locally from within the repo or piped via curl | bash
SCRIPT_DIR=""
if [ -n "${BASH_SOURCE[0]}" ] && [ "${BASH_SOURCE[0]}" != "-" ] && [ -f "${BASH_SOURCE[0]}" ]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/SKILL.md" ]; then
  SOURCE_DIR="$SCRIPT_DIR"
elif [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/../SKILL.md" ]; then
  SOURCE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
else
  # Running via curl | bash without local files -> Clone or update into DEFAULT_INSTALL_DIR
  echo "📥 Fetching latest Project Initiator repository..."
  if [ -d "$DEFAULT_INSTALL_DIR/.git" ]; then
    git -C "$DEFAULT_INSTALL_DIR" pull --quiet
  else
    mkdir -p "$(dirname "$DEFAULT_INSTALL_DIR")"
    git clone --quiet --depth=1 "$REPO_URL" "$DEFAULT_INSTALL_DIR" 2>/dev/null || {
      mkdir -p "$DEFAULT_INSTALL_DIR"
    }
  fi
  SOURCE_DIR="$DEFAULT_INSTALL_DIR"
fi

TARGET="${1:---all}"

install_antigravity_global() {
  local target_dir="$HOME/.gemini/config/skills/project-initiator"
  mkdir -p "$HOME/.gemini/config/skills"
  rm -rf "$target_dir"
  ln -s "$SOURCE_DIR" "$target_dir"
  echo "  ✅ Google Antigravity Global: $target_dir"
}

install_claude_code() {
  local target_dir="$HOME/.claude/skills/project-initiator"
  mkdir -p "$HOME/.claude/skills"
  rm -rf "$target_dir"
  ln -s "$SOURCE_DIR" "$target_dir"
  echo "  ✅ Claude Code Global: $target_dir"
}

install_cursor() {
  local target_dir="$HOME/.cursor/rules"
  mkdir -p "$target_dir"
  cp "$SOURCE_DIR/SKILL.md" "$target_dir/project-initiator.mdc" 2>/dev/null || true
  echo "  ✅ Cursor Global Rules: $target_dir/project-initiator.mdc"
}

install_windsurf() {
  local target_dir="$HOME/.codeium/windsurf/skills/project-initiator"
  mkdir -p "$(dirname "$target_dir")"
  rm -rf "$target_dir"
  ln -s "$SOURCE_DIR" "$target_dir" 2>/dev/null || true
  echo "  ✅ Windsurf / Cascade: $target_dir"
}

install_project() {
  local project_root="${2:-$(pwd)}"
  echo "📁 Installing to project workspace: $project_root"
  
  # Antigravity project skill
  mkdir -p "$project_root/.agents/skills"
  rm -rf "$project_root/.agents/skills/project-initiator"
  ln -s "$SOURCE_DIR" "$project_root/.agents/skills/project-initiator"
  
  # Cursor project rule
  mkdir -p "$project_root/.cursor/rules"
  cp "$SOURCE_DIR/SKILL.md" "$project_root/.cursor/rules/project-initiator.mdc" 2>/dev/null || true
  
  echo "  ✅ Attached to workspace (.agents/skills/project-initiator)"
}

print_header() {
  echo ""
  echo "=========================================================="
  echo " 🚀 Project Initiator: Pre-Flight Universal Skill Installer"
  echo "=========================================================="
  echo "Source Directory: $SOURCE_DIR"
  echo ""
}

print_footer() {
  echo ""
  echo "🎉 Installation Complete!"
  echo ""
  echo "💡 Quickstart Trigger:"
  echo "   In Antigravity or any agent chat, type:"
  echo "   /project-init   or   'Initialize a new project'"
  echo "=========================================================="
  echo ""
}

case "$TARGET" in
  --antigravity)
    print_header
    install_antigravity_global
    print_footer
    ;;
  --claude)
    print_header
    install_claude_code
    print_footer
    ;;
  --cursor)
    print_header
    install_cursor
    print_footer
    ;;
  --windsurf)
    print_header
    install_windsurf
    print_footer
    ;;
  --project)
    print_header
    install_project "$@"
    print_footer
    ;;
  --all|*)
    print_header
    echo "Installing across all supported agent ecosystems..."
    install_antigravity_global
    install_claude_code
    install_cursor
    install_windsurf
    print_footer
    ;;
esac
