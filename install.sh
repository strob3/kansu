#!/usr/bin/env bash

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$HOME/.local/bin"

cd "$PROJECT_DIR"

echo "Installing kansu..."

if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: python3 is not installed."
    return 1 2>/dev/null || exit 1
fi

python3 -m venv .venv

source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

cd "$PROJECT_DIR/src"

python -c "from database import initialize_database; initialize_database()"

python import_data.py n5
python import_data.py n4

mkdir -p "$INSTALL_DIR"

cat > "$INSTALL_DIR/kansu" <<EOF
#!/usr/bin/env bash
cd "$PROJECT_DIR/src"
exec "$PROJECT_DIR/.venv/bin/python" main.py "\$@"
EOF

chmod +x "$INSTALL_DIR/kansu"

PATH_LINE='export PATH="$HOME/.local/bin:$PATH"'

case "$SHELL" in
    */bash)
        SHELL_CONFIG="$HOME/.bashrc"
        ;;
    */zsh)
        SHELL_CONFIG="$HOME/.zshrc"
        ;;
    *)
        SHELL_CONFIG="$HOME/.profile"
        ;;
esac

if ! grep -Fxq "$PATH_LINE" "$SHELL_CONFIG" 2>/dev/null; then
    echo "$PATH_LINE" >> "$SHELL_CONFIG"
fi

export PATH="$INSTALL_DIR:$PATH"

echo
echo "kansu installed successfully."
echo
echo "Run:"
echo "  kansu"