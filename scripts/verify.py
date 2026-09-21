"""Cross-platform verify gate: lint then test. Exit code is nonzero on any failure.
Usage: python scripts/verify.py
"""

import subprocess
import sys

STEPS = [
    ("ruff", [sys.executable, "-m", "ruff", "check", "src", "tests"]),
    ("pytest", [sys.executable, "-m", "pytest", "-q"]),
]


def main() -> int:
    for name, cmd in STEPS:
        print(f"== {name}", flush=True)
        if subprocess.call(cmd) != 0:
            print(f"VERIFY FAIL at {name}")
            return 1
    print("VERIFY PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
