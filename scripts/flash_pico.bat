@echo off
REM Flash MicroPython firmware to a Pico (Windows)

if "%1"=="" (
    echo Usage: flash_pico.bat ^<pico_number^> [COM_port]
    echo Example: flash_pico.bat 1 COM3
    pause
    exit /b 1
)

set PICO_NUM=%1
set COM_PORT=%2

echo Flashing Pico Worker #%PICO_NUM%
echo ================================

REM Check if ampy is installed
pip show adafruit-ampy >nul 2>&1
if errorlevel 1 (
    echo Installing ampy...
    pip install adafruit-ampy
)

REM If no COM port specified, ask user
if "%COM_PORT%"=="" (
    echo Please enter COM port ^(e.g., COM3^):
    set /p COM_PORT=
)

echo Using COM port: %COM_PORT%

REM Upload firmware files
echo Uploading boot.py...
ampy --port %COM_PORT% put pico_firmware\boot.py /boot.py

echo Uploading main.py...
ampy --port %COM_PORT% put pico_firmware\main.py /main.py

echo.
echo Pico #%PICO_NUM% flashed successfully!
echo Disconnect and reconnect to start mining firmware
pause
