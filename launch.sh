#!/bin/bash
cd "$(dirname "$0")" || exit 1
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    .venv/bin/python -m pip install -r requirements.txt || exit 1
fi
echo "Running main.py..."
.venv/bin/python main.py
if [ $? -ne 0 ]; then
    read -p "Press enter to continue..."
fi
