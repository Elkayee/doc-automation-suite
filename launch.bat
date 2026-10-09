@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
    echo Creating virtual environment...
    python -m venv .venv
    .venv\Scripts\python.exe -m pip install -r requirements.txt
    if errorlevel 1 exit /b 1
)
echo Running main.py...
.venv\Scripts\python.exe main.py
if %ERRORLEVEL% NEQ 0 pause
