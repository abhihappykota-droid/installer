# Building Prynt Installer .exe

Complete guide to building the Windows installer executable on a Windows machine.

## Prerequisites

### 1. Windows Machine Requirements
- **OS**: Windows 10 or Windows 11
- **Python**: 3.7 or higher
- **Disk Space**: ~500 MB for tools and build artifacts
- **Admin Rights**: Required for testing installation

### 2. Install Python
Download from: https://www.python.org/downloads/

**Important**: During installation, check ✓ "Add Python to PATH"

Verify installation:
```bash
python --version
```

### 3. Install Git (Optional but Recommended)
Download from: https://git-scm.com/download/win

This allows you to clone the repository directly on Windows.

## Setup Build Environment

### Option A: Clone on Windows (Recommended)

1. Open Command Prompt or PowerShell
2. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd prynt/installer
   ```

### Option B: Transfer Files from Mac

1. Copy the entire `installer/` folder to your Windows machine
2. Use USB drive, network share, or cloud storage
3. Ensure all files are transferred:
   - `prynt_installer.py`
   - `build_installer.py`
   - `requirements.txt`
   - `README.md`
   - `BUILD_INSTRUCTIONS.md`

## Build Steps

### Step 1: Install Dependencies

Open Command Prompt or PowerShell **as Administrator**:

```bash
cd path\to\prynt\installer
pip install -r requirements.txt
pip install pyinstaller
```

This installs:
- `requests` - HTTP client for API calls
- `pywin32` - Windows API for printer detection
- `Pillow` - Image processing for logo
- `pyinstaller` - Executable builder

### Step 2: Test the Installer Script (Optional)

Before building, test that the script runs:

```bash
python prynt_installer.py
```

This should open the installer GUI. You can close it after verifying it works.

### Step 2.5: Create Icon (Adds Prynt Logo to .exe)

**Optional but Recommended** - Makes the .exe look professional!

```bash
python create_icon.py
```

**Expected Output**:
```
============================================================
Prynt Icon Creator
============================================================

✓ Found logo: ../frontend/public/prynt-logo.png
✓ Loaded image: 512x512 pixels
✓ Created icon: prynt_icon.ico
  Sizes: 16x16, 32x32, 48x48, 256x256

✅ Icon created successfully!
```

This creates `prynt_icon.ico` from your logo. The build script will automatically use it.

**Note**: If you don't have the logo or this fails, skip this step. The .exe will still work, just without a custom icon.

### Step 3: Build the .exe

Run the build script:

```bash
python build_installer.py
```

**Expected Output**:
```
============================================================
Building Prynt Kiosk Installer
============================================================

Building PryntKioskInstaller.exe...
Command: pyinstaller --name PryntKioskInstaller --onefile --windowed --clean prynt_installer.py

[... PyInstaller output ...]

============================================================
✓ Build completed successfully!
============================================================

Executable location:
  dist\PryntKioskInstaller.exe

File size: ~15.00 MB

You can now distribute this .exe file to install Prynt kiosks.
```

### Step 4: Verify the Build

The compiled executable will be at:
```
installer\dist\PryntKioskInstaller.exe
```

**Typical file size**: 12-20 MB (includes Python runtime, dependencies, and GUI)

### Step 5: Test the Installer

1. Copy `PryntKioskInstaller.exe` to a test location
2. Right-click → "Run as administrator"
3. Enter server URL and setup code
4. Verify GUI appears with Prynt branding

## Build Artifacts

After building, you'll see these folders:

```
installer/
├── build/              # Temporary build files (can delete)
├── dist/               # OUTPUT: Your .exe is here!
│   └── PryntKioskInstaller.exe
├── __pycache__/        # Python cache (can delete)
└── PryntKioskInstaller.spec  # PyInstaller config (can delete)
```

**Only keep**: `dist/PryntKioskInstaller.exe`

## Customization Options

### Add Custom Icon

1. Create or download a `.ico` file with Prynt logo
2. Save as `installer/prynt_icon.ico`
3. Rebuild - the build script will automatically include it

### Modify Version Information

Edit `build_installer.py`, find `VERSION_INFO` section:

```python
filevers=(1, 0, 0, 0),  # Change version number
prodvers=(1, 0, 0, 0),
StringStruct(u'FileVersion', u'1.0.0.0'),
```

### Change Executable Name

Edit `build_installer.py`:

```python
EXE_NAME = "PryntKioskInstaller"  # Change this
```

## Troubleshooting

### "pip: command not found"
**Solution**: Python not in PATH. Reinstall Python with "Add to PATH" checked.

### "pyinstaller: command not found"
**Solution**: 
```bash
python -m pip install --upgrade pip
pip install pyinstaller
```

### "Module not found" errors during build
**Solution**: Install missing module:
```bash
pip install <module-name>
```

### Antivirus blocking .exe
**Solution**: PyInstaller executables are sometimes flagged. Add exception in antivirus or:
1. Build on clean Windows VM
2. Use code signing certificate (for production)

### Build takes forever
**Solution**: First build is slow (~5-10 min). Subsequent builds are faster. Use SSD if possible.

### .exe is too large (>30 MB)
**Solution**: Normal for --onefile builds. To reduce size:
- Remove unused imports from `prynt_installer.py`
- Use `--exclude-module` in build script
- Consider --onedir instead (creates folder with smaller .exe)

### Testing without Admin rights
**Solution**: Installer needs admin to write to Program Files. For testing:
- Change `INSTALL_DIR` in installer to user folder
- Or always run as admin

## Distribution

### For Localhost Testing

Give to installation team:
1. `PryntKioskInstaller.exe`
2. Server URL (e.g., `http://192.168.1.10:8000`)
3. 6-digit setup code from admin panel

### For Production Deployment

1. **Code Signing** (Recommended):
   - Get code signing certificate
   - Sign the .exe to avoid security warnings
   - Use `signtool.exe` from Windows SDK

2. **Create Installer Package**:
   - Use NSIS, Inno Setup, or WiX for professional installer
   - Include uninstaller
   - Add to Windows Apps & Features

3. **Update Distribution**:
   - Host on your server for easy download
   - Include version checking for auto-updates

## Clean Build

If you need to rebuild from scratch:

```bash
# Delete build artifacts
rmdir /s /q build
rmdir /s /q dist
del PryntKioskInstaller.spec

# Rebuild
python build_installer.py
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `pip install -r requirements.txt` | Install dependencies |
| `pip install pyinstaller` | Install build tool |
| `python prynt_installer.py` | Test installer GUI |
| `python build_installer.py` | Build .exe |
| `dist\PryntKioskInstaller.exe` | Run compiled installer |

## Next Steps

After building successfully:
1. ✅ Test installer on a clean Windows machine
2. ✅ Verify printer detection works
3. ✅ Test with Mac backend on localhost
4. ✅ Create setup code in admin panel
5. ✅ Complete full installation flow
6. 📝 Document any issues or improvements
7. 🚀 Deploy to actual kiosks

## Need Help?

Common issues and solutions in installer/README.md

For build-specific problems, check:
- PyInstaller docs: https://pyinstaller.org/
- Windows Python docs: https://docs.python.org/3/using/windows.html
