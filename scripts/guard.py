"""PreToolUse guard for shell commands. Chapter 9 of the handbook.

Kiro sends the pending tool call as JSON on stdin. This script:
1. appends the raw event to guard-audit.log (gitignored) so you can see what the agent tried
2. exits 2 with a reason on stderr when the command contains a blocked pattern

Exit code 2 is the block signal for PreToolUse hooks.
"""

import json
import pathlib
import sys

BLOCK = (
    "curl",
    "wget",
    "nc ",
    "Invoke-WebRequest",
    "Invoke-RestMethod",
    "ATTACKER",
    ".kiro/settings",
    "$HOME/.kiro",
    "permissions.yaml",
    "base64",
    "git push --force",
    "git push -f",
)

LOG = pathlib.Path(__file__).resolve().parent.parent / "guard-audit.log"


def main() -> int:
    raw = sys.stdin.read()
    try:
        event = json.loads(raw)
    except json.JSONDecodeError:
        event = {"raw": raw}

    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event)[:2000] + "\n")

    text = json.dumps(event)

    # Extract the pending shell command when available.
    command = event.get("tool_input", {}).get("command", "")
    if not isinstance(command, str):
        command = ""

    if len(command) > 400:
        reason = f"command is {len(command)} characters long (limit is 400)"
        with LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"guard_block_reason": reason}) + "\n")
        print(f"guard.py blocked this command: {reason}. Ask the user instead.", file=sys.stderr)
        return 2

    hit = next((b for b in BLOCK if b in text), None)
    if hit:
        reason = f"command contains blocked pattern '{hit}'"
        with LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"guard_block_reason": reason}) + "\n")
        print(f"guard.py blocked this command: {reason}. Ask the user instead.", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())