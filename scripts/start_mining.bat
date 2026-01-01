@echo off
REM Start the Bitcoin mining controller on Windows

cd /d "%~dp0\.."

echo Starting Bitcoin Miner Controller...

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found.
    echo Please run scripts\setup_windows.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if config exists
if not exist "config\.env" (
    echo Error: config\.env not found.
    echo Copy from config\.env.example and configure
    pause
    exit /b 1
)

REM Start the controller
python controller\main.py

REM Deactivate on exit
call venv\Scripts\deactivate.bat
pause
