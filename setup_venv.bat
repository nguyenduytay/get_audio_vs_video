@echo off
echo ========================================
echo Facebook & TikTok Downloader Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [OK] Python found
python --version

echo.
echo Creating virtual environment...
python -m venv venv

if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)

echo [OK] Virtual environment created

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo [OK] Virtual environment activated

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To run the application:
echo 1. Double-click run.bat
echo 2. Or manually activate venv and run:
echo    - venv\Scripts\activate.bat
echo    - python video_downloader.py
echo.
echo To deactivate virtual environment:
echo    - deactivate
echo.
pause
