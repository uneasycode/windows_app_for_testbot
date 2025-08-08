# setup_windows.bat - Batch file to setup and build Windows executable

@echo off
title Telegram Bot Manager - Windows Setup
color 0A
echo.
echo ===============================================
echo    Telegram Bot Manager - Windows Setup
echo ===============================================
echo.

echo Checking Python installation...
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Python is installed
)

echo.
echo Installing desktop requirements...
python -m pip install --upgrade pip
python -m pip install -r requirements_desktop.txt

if errorlevel 1 (
    echo ❌ Failed to install requirements
    echo Please check your internet connection and try again
    pause
    exit /b 1
) else (
    echo ✅ Requirements installed successfully
)

echo.
echo Building Windows executable...
python build_executable.py

if errorlevel 1 (
    echo ❌ Build failed
    pause
    exit /b 1
)

echo.
echo ===============================================
echo          Build Completed Successfully!
echo ===============================================
echo.
echo Your executable is ready in: TelegramBotManager_Portable/
echo.
echo Next steps:
echo 1. Edit .env file with your Telegram API credentials
echo 2. Run TelegramBotManager.exe to start the application
echo.
echo Instructions:
echo • Get API credentials from: https://my.telegram.org
echo • Add your phone number with country code (e.g., +1234567890)
echo.
pause