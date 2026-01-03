@echo off
REM Build script for Pi Bitcoin Miner Windows Installer
REM This script builds the executable and creates the installer

echo ========================================
echo Pi Bitcoin Miner - Installer Builder
echo ========================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [ERROR] PyInstaller is not installed.
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo [ERROR] Failed to install PyInstaller
        pause
        exit /b 1
    )
)

REM Step 1: Clean previous builds
echo [1/4] Cleaning previous builds...
if exist "..\dist" rmdir /s /q "..\dist"
if exist "..\build" rmdir /s /q "..\build"
if exist "output" rmdir /s /q "output"
echo Done.
echo.

REM Step 2: Build executable with PyInstaller
echo [2/4] Building executable with PyInstaller...
cd ..
pyinstaller pi_bitcoin_miner.spec
if errorlevel 1 (
    echo [ERROR] PyInstaller build failed
    cd installer
    pause
    exit /b 1
)
cd installer
echo Done.
echo.

REM Step 3: Check if Inno Setup is installed
echo [3/4] Checking for Inno Setup...
set INNO_SETUP="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist %INNO_SETUP% (
    set INNO_SETUP="C:\Program Files\Inno Setup 6\ISCC.exe"
)

if not exist %INNO_SETUP% (
    echo [WARNING] Inno Setup not found.
    echo Please install Inno Setup from: https://jrsoftware.org/isinfo.php
    echo.
    echo The executable has been built in: ..\dist\pi-bitcoin-miner\
    echo You can run it directly or install Inno Setup to create an installer.
    pause
    exit /b 0
)

REM Step 4: Build installer with Inno Setup
echo [4/4] Building installer with Inno Setup...
%INNO_SETUP% setup.iss
if errorlevel 1 (
    echo [ERROR] Inno Setup compilation failed
    pause
    exit /b 1
)
echo Done.
echo.

echo ========================================
echo BUILD COMPLETE!
echo ========================================
echo.
echo Executable location: ..\dist\pi-bitcoin-miner\
echo Installer location:   output\PiBitcoinMiner-Setup-1.0.0.exe
echo.
pause
