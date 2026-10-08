#!/usr/bin/env python3
"""
Build script for creating Prynt Installer .exe
Uses PyInstaller to create a standalone Windows executable.
"""

import os
import sys
import subprocess
from pathlib import Path

# Installer configuration
SCRIPT_NAME = "prynt_installer.py"
EXE_NAME = "PryntKioskInstaller"
ICON_PATH = None  # Will be set if icon file exists

# PyInstaller options
PYINSTALLER_OPTS = [
    '--name', EXE_NAME,
    '--onefile',  # Single executable file
    '--windowed',  # No console window
    '--clean',  # Clean PyInstaller cache
]

# Add icon if available
ICON_FILE = Path(__file__).parent / 'prynt_icon.ico'
if ICON_FILE.exists():
    PYINSTALLER_OPTS.extend(['--icon', str(ICON_FILE)])

# Add version info (Windows only)
VERSION_INFO = """
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Prynt'),
        StringStruct(u'FileDescription', u'Prynt Kiosk Installer'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'PryntInstaller'),
        StringStruct(u'LegalCopyright', u'© 2024 Prynt. All rights reserved.'),
        StringStruct(u'OriginalFilename', u'PryntKioskInstaller.exe'),
        StringStruct(u'ProductName', u'Prynt Kiosk System'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""

def create_version_file():
    """Create version file for Windows executable."""
    version_file = Path(__file__).parent / 'version_info.txt'
    with open(version_file, 'w') as f:
        f.write(VERSION_INFO)
    return version_file

def build_exe():
    """Build the installer executable."""
    print("=" * 60)
    print("Building Prynt Kiosk Installer")
    print("=" * 60)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("ERROR: PyInstaller not found!")
        print("Install it with: pip install pyinstaller")
        sys.exit(1)
    
    # Check if script exists
    script_path = Path(__file__).parent / SCRIPT_NAME
    if not script_path.exists():
        print(f"ERROR: {SCRIPT_NAME} not found!")
        sys.exit(1)
    
    # Create version file
    version_file = create_version_file()
    if version_file.exists():
        PYINSTALLER_OPTS.extend(['--version-file', str(version_file)])
    
    # Build command
    cmd = ['pyinstaller'] + PYINSTALLER_OPTS + [str(script_path)]
    
    print(f"\nBuilding {EXE_NAME}.exe...")
    print(f"Command: {' '.join(cmd)}\n")
    
    # Run PyInstaller
    try:
        result = subprocess.run(cmd, check=True)
        
        print("\n" + "=" * 60)
        print("✓ Build completed successfully!")
        print("=" * 60)
        print(f"\nExecutable location:")
        print(f"  {Path('dist') / f'{EXE_NAME}.exe'}")
        print(f"\nFile size: {(Path('dist') / f'{EXE_NAME}.exe').stat().st_size / 1024 / 1024:.2f} MB")
        print("\nYou can now distribute this .exe file to install Prynt kiosks.")
        
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 60)
        print("✗ Build failed!")
        print("=" * 60)
        print(f"\nError: {e}")
        sys.exit(1)
    
    finally:
        # Cleanup version file
        if version_file.exists():
            version_file.unlink()

if __name__ == "__main__":
    build_exe()
