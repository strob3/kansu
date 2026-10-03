#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# ensure cli and src directories are in sys.path
CLI_DIR = Path(__file__).resolve().parent
SRC_DIR = CLI_DIR.parent
PROJECT_DIR = SRC_DIR.parent

for path in (CLI_DIR, SRC_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

# if textual is not in current environment, auto-switch to project virtual environment
venv_python = PROJECT_DIR / ".venv" / "bin" / "python"
if venv_python.exists() and sys.executable != str(venv_python):
    try:
        import textual
    except ImportError:
        os.execv(str(venv_python), [str(venv_python)] + sys.argv)

try:
    from ui import KansuUI
except ImportError:
    from cli.ui import KansuUI


def main():
    ui = KansuUI()
    ui.run()


if __name__ == "__main__":
    main()