#!/usr/bin/env bash
# Idempotent hosted-environment setup for the hooks module.
#
# Runs on every VM boot (startup_commands re-run on reboot), so each step is
# guarded or merges rather than overwrites.
#
# Invoked as: bash "$HOME/$DEFAULT_FOLDER/setup.sh" from exercise_config.yaml's
# startup_commands, AFTER the shared `!include* ai/hle_claude_setup.yaml`
# commands (AWS credentials, Bedrock env in .zshrc, the extension's .vscode
# settings, .claude.json theme, the CLI install). DEFAULT_FOLDER and
# SW_ATTENDANCE_ID reach this script as inherited environment variables.
set -euo pipefail

REPO_DIR="$HOME/$DEFAULT_FOLDER"

# --- Shell extras --------------------------------------------------------
if ! grep -q '# hooks shell extras' "$HOME/.zshrc" 2>/dev/null; then
  cat << 'EOF' >> "$HOME/.zshrc"

# hooks shell extras
export PROMPT=$'%{\e[1m%}🐳 %{\e[1;32m%}%n@%{\e[0m%}:%{\e[1;34m%}%1~%{\e[0m%} $ '
alias python='python3'
# Stop the CLI installing the VS Code extension the config leaves out.
export CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL=1
EOF
fi

# --- ~/.claude.json: skip the first-launch screens ------------------------
# A merge, not an overwrite, so anything the learner has changed since the
# last boot stays. The keys are the ones Claude Code 2.1.311 wrote after
# its first-launch screens were clicked through on a real VM (27 Oct 2026).
CLAUDE_VERSION="$("$HOME/.local/bin/claude" --version 2>/dev/null | cut -d' ' -f1 || true)"
REPO_DIR="$REPO_DIR" CLAUDE_VERSION="$CLAUDE_VERSION" python3 - << 'PYEOF'
import json
import os

path = os.path.expanduser("~/.claude.json")
try:
    with open(path) as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    data = {}

# Theme picker and security notes.
data.setdefault("theme", "auto")
data["hasCompletedOnboarding"] = True
if os.environ["CLAUDE_VERSION"]:
    data.setdefault("lastOnboardingVersion", os.environ["CLAUDE_VERSION"])
# "Use Claude Code's terminal setup?"
data["shiftEnterKeyBindingInstalled"] = True
# The auto mode explanation above the first prompt.
data["hasSeenAutoModeEntryWarning"] = True
# "Do you trust the files in this folder?", as if the learner said yes.
project = data.setdefault("projects", {}).setdefault(os.environ["REPO_DIR"], {})
project["hasTrustDialogAccepted"] = True

with open(path, "w") as f:
    json.dump(data, f, indent=4)
PYEOF

# --- Claude Code user settings: start learners in auto mode -------------
# This has to be user settings — `auto` is ignored from a project's
# .claude/settings.json.
mkdir -p "$HOME/.claude"
cat << 'EOF' > "$HOME/.claude/settings.json"
{
    "permissions": {
        "defaultMode": "auto"
    }
}
EOF

# --- Tools for the exercises ---------------------------------------------
if ! python3 -m pytest --version >/dev/null 2>&1; then
  pip3 install --user pytest
fi

# jq is needed by the hooks the learner writes, to read tool_input off
# stdin. The learner user has no sudo on the AMI (verified 28 Aug 2026:
# apt-get failed silently), so install the static binary into ~/.local/bin,
# which .zshrc puts on PATH — the same route pytest uses.
if [ ! -x "$HOME/.local/bin/jq" ]; then
  mkdir -p "$HOME/.local/bin"
  curl -fsSL -o "$HOME/.local/bin/jq" "https://github.com/jqlang/jq/releases/download/jq-1.7.1/jq-linux-$(dpkg --print-architecture)"
  chmod +x "$HOME/.local/bin/jq"
fi

# --- Services ------------------------------------------------------------
# --wait implies detached mode (so it doesn't block after startup).
cd "$REPO_DIR"
docker compose up --build --wait claude_session_sync_filter sync
