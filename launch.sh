#!/bin/bash
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
echo "Upgrading pip and installing dependencies..."
python3 -m pip install --upgrade pip
pip install -r requirements.txt
echo "Running main.py..."
python3 main.py
if [ $? -ne 0 ]; then
    read -p "Press enter to continue..."
fi