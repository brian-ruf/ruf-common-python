#!/bin/bash
# Manually trigger unit tests

VENV_DIR="$(dirname "$0")/.venv"

if [[ ! -d "$VENV_DIR" ]]; then
    echo "Virtual environment not found. Creating $VENV_DIR ..."
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    echo "Installing dependencies ..."
    pip install --quiet "../[dev]"
else
    source "$VENV_DIR/bin/activate"
fi

clear
python -m pytest unit/ -v
