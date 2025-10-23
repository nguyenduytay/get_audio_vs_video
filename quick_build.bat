@echo off
echo ========================================
echo Quick Build Script
echo ========================================
echo.

REM Kích hoạt môi trường ảo
call .\venv\Scripts\Activate.ps1

REM Build executable
echo Building executable...
python build_exe.py

if %errorlevel% == 0 (
    echo.
    echo ✅ Build completed successfully!
    echo 📁 Executable: dist\MultiUtilityDashboard.exe
    echo.
    echo To run: dist\MultiUtilityDashboard.exe
) else (
    echo.
    echo ❌ Build failed!
)

echo.
pause
