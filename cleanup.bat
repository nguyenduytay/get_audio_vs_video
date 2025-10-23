@echo off
echo ========================================
echo Project Cleanup Script
echo ========================================
echo.

echo Cleaning up temporary files...

REM Xóa thư mục build
if exist "build" (
    echo Removing build/ directory...
    rmdir /s /q "build"
    echo ✅ Removed build/
)

REM Xóa file .spec
if exist "*.spec" (
    echo Removing .spec files...
    del /q "*.spec"
    echo ✅ Removed .spec files
)

REM Xóa __pycache__
echo Removing __pycache__ directories...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
echo ✅ Removed __pycache__ directories

REM Xóa file .pyc
echo Removing .pyc files...
del /s /q "*.pyc"
echo ✅ Removed .pyc files

REM Xóa file log
if exist "*.log" (
    echo Removing .log files...
    del /q "*.log"
    echo ✅ Removed .log files
)

echo.
echo ========================================
echo Cleanup completed!
echo ========================================
echo.
echo Remaining files:
dir /b
echo.
pause
