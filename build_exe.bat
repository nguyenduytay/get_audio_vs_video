@echo off
echo ========================================
echo Multi-Utility Dashboard Builder
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo Python found. Installing dependencies...
pip install -r requirements.txt

echo.
echo Building executable...
python build_exe.py

echo.
echo Build completed!
echo.
echo To distribute:
echo 1. Send the dist/installer/ folder to users
echo 2. Users run install.bat to create desktop shortcut
echo 3. Then run MultiUtilityDashboard.exe
echo.
pause
