#!/usr/bin/env bash
#
# Kansu cli installer
# installs Kansu and configures the 'kansu' command

set -e

# set project source dir
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd)"

if [ -f "$SCRIPT_DIR/src/cli/main.py" ]; then
    PROJECT_DIR="$SCRIPT_DIR"
elif [ -f "$PWD/src/cli/main.py" ]; then
    PROJECT_DIR="$PWD"
else
    # invoked via curl/pipe or outside an existing repo clone
    PROJECT_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/kansu"
    REPO_URL="https://github.com/strob3/kansu.git"

    if [ -d "$PROJECT_DIR/.git" ]; then
        echo "Updating existing Kansu installation at $PROJECT_DIR..."
        git -C "$PROJECT_DIR" pull --ff-only 2>/dev/null || true
    elif [ -d "$PROJECT_DIR" ] && [ -f "$PROJECT_DIR/src/cli/main.py" ]; then
        echo "Kansu installation found at $PROJECT_DIR."
    else
        echo "Downloading Kansu into $PROJECT_DIR..."
        mkdir -p "$(dirname "$PROJECT_DIR")"
        if command -v git >/dev/null 2>&1; then
            git clone --depth 1 "$REPO_URL" "$PROJECT_DIR"
        elif command -v curl >/dev/null 2>&1 && command -v tar >/dev/null 2>&1; then
            mkdir -p "$PROJECT_DIR"
            curl -fsSL "https://github.com/strob3/kansu/archive/refs/heads/main.tar.gz" | tar -xz -C "$PROJECT_DIR" --strip-components=1
        else
            echo "Error: git or (curl + tar) is required to download Kansu."
            exit 1
        fi
    fi
fi

INSTALL_DIR="$HOME/.local/bin"

echo "=========================================="
echo "Installing Kansu (CLI Version)..."
echo "=========================================="
echo "Location: $PROJECT_DIR"

# locate python3
PYTHON_BIN=""
if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
else
    echo "Error: Python 3 is required but was not found on your system."
    return 1 2>/dev/null || exit 1
fi

# verify python version >= 3.9
"$PYTHON_BIN" -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)" 2>/dev/null || {
    echo "Error: Kansu requires Python 3.9 or higher."
    return 1 2>/dev/null || exit 1
}

# venv setup
VENV_DIR="$PROJECT_DIR/.venv"
if [ ! -d "$VENV_DIR" ] || [ ! -x "$VENV_DIR/bin/python" ]; then
    echo "Creating virtual environment at $VENV_DIR..."
    "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

VENV_PYTHON="$VENV_DIR/bin/python"

# install dependencies
echo "Installing dependencies..."
"$VENV_PYTHON" -m pip install --upgrade pip --quiet 2>/dev/null || true
"$VENV_PYTHON" -m pip install -r "$PROJECT_DIR/requirements.txt" --quiet

# initialize kanji database
echo "Initializing database..."
"$VENV_PYTHON" -c "
import sys
sys.path.insert(0, '$PROJECT_DIR/src/cli')
sys.path.insert(0, '$PROJECT_DIR/src')
from database import initialize_database, get_connection

initialize_database()
conn = get_connection()
cursor = conn.cursor()
count = cursor.execute('SELECT COUNT(*) FROM kanji').fetchone()[0]
conn.close()

if count == 0:
    print('Kanji database is empty. Attempting to download initial JLPT N5/N4 datasets...')
    try:
        import import_data
        if hasattr(import_data, 'import_single_level'):
            import_data.import_single_level('n5')
            import_data.import_single_level('n4')
        else:
            sys.argv = ['import_data.py', 'n5']
            import_data.main()
            sys.argv = ['import_data.py', 'n4']
            import_data.main()
    except Exception as exc:
        print(f'Warning: Could not download online datasets ({exc}). You can run import_data.py later.')
else:
    print(f'Database verified ({count} kanji ready).')
"

# create executable wrapper
mkdir -p "$INSTALL_DIR"
WRAPPER_PATH="$INSTALL_DIR/kansu"

cat > "$WRAPPER_PATH" <<EOF
#!/usr/bin/env bash
export KANJI_DB_PATH="\${KANJI_DB_PATH:-$PROJECT_DIR/src/cli/kanji.db}"
export PYTHONPATH="$PROJECT_DIR/src/cli:$PROJECT_DIR/src\${PYTHONPATH:+:\$PYTHONPATH}"
cd "$PROJECT_DIR/src/cli" || exit 1
exec "$PROJECT_DIR/.venv/bin/python" "$PROJECT_DIR/src/cli/main.py" "\$@"
EOF

chmod +x "$WRAPPER_PATH"

# symlink to /usr/local/bin if writable
if [ -w "/usr/local/bin" ]; then
    ln -sf "$WRAPPER_PATH" "/usr/local/bin/kansu" 2>/dev/null || true
fi

# ensure $INSTALL_DIR is in PATH across common shells
PATH_EXPORT_LINE='export PATH="$HOME/.local/bin:$PATH"'

for rc in "$HOME/.bashrc" "$HOME/.bash_profile" "$HOME/.zshrc" "$HOME/.profile"; do
    if [ -f "$rc" ]; then
        if ! grep -qs '\.local/bin' "$rc" 2>/dev/null; then
            echo "" >> "$rc"
            echo "# Added by Kansu installer" >> "$rc"
            echo "$PATH_EXPORT_LINE" >> "$rc"
        fi
    fi
done

# export in current shell session if sourced, and clear hash tables
export PATH="$INSTALL_DIR:$PATH"
hash -r 2>/dev/null || true
if [ -n "$ZSH_VERSION" ]; then
    rehash 2>/dev/null || true
fi

echo
echo "=========================================="
echo "Kansu CLI installed successfully."
echo "=========================================="
echo "Executable located at: $WRAPPER_PATH"

# check if 'kansu' resolves in current environment
if command -v kansu >/dev/null 2>&1; then
    echo
    echo "You can launch Kansu anytime by typing:"
    echo "  kansu"
else
    echo
    echo "Note: To make 'kansu' available in your current terminal session, run:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo "Or start a new terminal session."
fi