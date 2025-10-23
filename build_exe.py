#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script để tạo file .exe từ dashboard
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_executable():
    """Tạo file .exe"""
    print("Building Multi-Utility Dashboard executable...")
    
    # Tạo thư mục dist nếu chưa có
    dist_dir = Path("dist")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Tạo file .exe duy nhất
        "--windowed",                   # Ẩn console window
        "--name=MultiUtilityDashboard", # Tên file .exe
        # "--icon=icon.ico",              # Icon (nếu có)
        "--add-data=modules;modules",   # Thêm thư mục modules
        "--hidden-import=yt_dlp",        # Import ẩn
        "--hidden-import=tkinter",      # Import ẩn
        "--hidden-import=PIL",          # Import ẩn
        "--clean",                      # Dọn dẹp cache
        "main_dashboard.py"             # File chính
    ]
    
    try:
        print("Running PyInstaller...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("Build successful!")
            print(f"Executable location: dist/MultiUtilityDashboard.exe")
            
            # Copy additional files
            print("Copying additional files...")
            if Path("README_DASHBOARD.md").exists():
                shutil.copy2("README_DASHBOARD.md", "dist/README.md")
            shutil.copy2("requirements.txt", "dist/")
            
            # Create run script
            run_script = dist_dir / "run.bat"
            with open(run_script, 'w', encoding='utf-8') as f:
                f.write("""@echo off
echo Starting Multi-Utility Dashboard...
MultiUtilityDashboard.exe
pause""")
            
            print("Build completed successfully!")
            print("\nFiles created:")
            print("  - MultiUtilityDashboard.exe (main executable)")
            print("  - run.bat (launcher)")
            print("  - README.md (documentation)")
            print("  - requirements.txt (dependencies)")
            
        else:
            print("Build failed!")
            print("Error:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("Build timeout!")
        return False
    except Exception as e:
        print(f"Build error: {e}")
        return False
    
    return True

def create_installer_package():
    """Tạo gói cài đặt"""
    print("\nCreating installer package...")
    
    # Tạo thư mục installer
    installer_dir = Path("dist/installer")
    installer_dir.mkdir(exist_ok=True)
    
    # Copy files
    dist_dir = Path("dist")
    files_to_copy = [
        "MultiUtilityDashboard.exe",
        "run.bat", 
        "README.md",
        "requirements.txt"
    ]
    
    for file in files_to_copy:
        if (dist_dir / file).exists():
            shutil.copy2(dist_dir / file, installer_dir / file)
            print(f"Copied {file}")
    
    # Tạo installer script
    installer_script = installer_dir / "install.bat"
    with open(installer_script, 'w', encoding='utf-8') as f:
        f.write("""@echo off
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
echo [InternetShortcut] > "%USERPROFILE%\\Desktop\\Multi-Utility Dashboard.url"
echo URL=file:///%CD%\\MultiUtilityDashboard.exe >> "%USERPROFILE%\\Desktop\\Multi-Utility Dashboard.url"
echo IconFile=%CD%\\MultiUtilityDashboard.exe >> "%USERPROFILE%\\Desktop\\Multi-Utility Dashboard.url"
echo IconIndex=0 >> "%USERPROFILE%\\Desktop\\Multi-Utility Dashboard.url"

echo.
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.
echo Desktop shortcut created!
echo To run: Double-click MultiUtilityDashboard.exe
echo.
pause""")
    
    print("Installer package created!")
    print(f"Location: {installer_dir}")

if __name__ == "__main__":
    print("Multi-Utility Dashboard Builder")
    print("=" * 50)
    
    # Check if PyInstaller is installed
    try:
        subprocess.run(["pyinstaller", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("PyInstaller not found!")
        print("Please install: pip install pyinstaller")
        sys.exit(1)
    
    # Build executable
    if build_executable():
        create_installer_package()
        print("\nAll done! Ready for distribution!")
    else:
        print("\nBuild failed!")
        sys.exit(1)
