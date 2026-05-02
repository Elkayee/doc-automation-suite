@echo off
if not exist .venv\Scripts\activate (
    echo Creating virtual environment...
    python -m venv .venv
)
call .venv\Scripts\activate
echo Upgrading pip and installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo Running main.py...
python main.py
if %ERRORLEVEL% NEQ 0 pause