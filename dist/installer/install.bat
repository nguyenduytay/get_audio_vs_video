@echo off
echo ========================================
echo Multi-Utility Dashboard Installer
echo ========================================
echo.

REM Check if executable exists
if not exist "MultiUtilityDashboard.exe" (
    echo Error: Executable not found!
    pause
    exit /b 1
)

echo Creating desktop shortcut...
echo [InternetShortcut] > "%USERPROFILE%\Desktop\Multi-Utility Dashboard.url"
echo URL=file:///%CD%\MultiUtilityDashboard.exe >> "%USERPROFILE%\Desktop\Multi-Utility Dashboard.url"
echo IconFile=%CD%\MultiUtilityDashboard.exe >> "%USERPROFILE%\Desktop\Multi-Utility Dashboard.url"
echo IconIndex=0 >> "%USERPROFILE%\Desktop\Multi-Utility Dashboard.url"

echo.
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.
echo Desktop shortcut created!
echo To run: Double-click MultiUtilityDashboard.exe
echo.
pause