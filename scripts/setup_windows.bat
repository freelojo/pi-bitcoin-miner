@echo off
REM Setup script for Raspberry Pi 4 Bitcoin Miner (Windows development)

echo ==========================================
echo Bitcoin Miner Controller Setup (Windows)
echo ==========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python 3 is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Navigate to project root
cd /d "%~dp0\.."

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing Python packages...
pip install -r requirements.txt

REM Create config if it doesn't exist
if not exist "config\.env" (
    echo Creating config file...
    copy "config\.env.example" "config\.env"
    echo Please edit config\.env with your mining pool settings
)

REM Create logs directory
if not exist "logs" mkdir logs

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Edit config\.env with your mining pool settings
echo 2. Flash firmware to all Pico boards (see pico_firmware\README.md)
echo 3. Connect Picos to USB hub
echo 4. Run: scripts\start_mining.bat
echo.
pause
