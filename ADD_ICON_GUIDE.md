# Adding Prynt Icon to Installer .exe

Quick guide to add the Prynt logo as the executable icon.

---

## Method 1: Automatic (Recommended)

### On Windows:

1. **Navigate to installer directory**:
   ```cmd
   cd installer
   ```

2. **Run icon creator**:
   ```cmd
   python create_icon.py
   ```

3. **Output**:
   ```
   ============================================================
   Prynt Icon Creator
   ============================================================

   ✓ Found logo: ../frontend/public/prynt-logo.png
   ✓ Loaded image: 512x512 pixels
   ✓ Converted to RGBA
   ✓ Created icon: installer/prynt_icon.ico
     Sizes: 16x16, 32x32, 48x48, 256x256

   ✅ Icon created successfully!

   Next step: Run 'python build_installer.py'
   ```

4. **Build installer**:
   ```cmd
   python build_installer.py
   ```

5. **Done!** Your .exe now has the Prynt icon ✅

---

## Method 2: Manual (If you have .ico already)

If you already have a `.ico` file:

1. **Copy your icon** to installer folder:
   ```cmd
   copy your_icon.ico installer\prynt_icon.ico
   ```

2. **Build installer**:
   ```cmd
   cd installer
   python build_installer.py
   ```

---

## Method 3: Online Converter (If create_icon.py fails)

1. **Go to**: https://convertio.co/png-ico/

2. **Upload**: `frontend/public/prynt-logo.png`

3. **Select sizes**: 
   - ✅ 16x16
   - ✅ 32x32
   - ✅ 48x48
   - ✅ 256x256

4. **Download** as `prynt_icon.ico`

5. **Place in installer folder**:
   ```
   installer/prynt_icon.ico
   ```

6. **Build**:
   ```cmd
   python build_installer.py
   ```

---

## Verify Icon Was Added

After building, check if icon is present:

### In File Explorer:
- Right-click `dist\PryntKioskInstaller.exe`
- You should see Prynt logo as the icon

### In Properties:
- Right-click .exe → Properties
- Icon tab should show Prynt logo

---

## Icon Sizes Explained

Windows needs multiple icon sizes for different contexts:

| Size | Used For |
|------|----------|
| 16x16 | File explorer (small icons) |
| 32x32 | File explorer (medium icons) |
| 48x48 | File explorer (large icons) |
| 256x256 | Windows Vista+ (extra large) |

The `create_icon.py` script automatically creates all these sizes from your logo.

---

## Troubleshooting

### "Pillow not installed"

**Install it**:
```cmd
pip install Pillow
```

### "Logo not found"

**Check path**:
- Logo should be at: `frontend/public/prynt-logo.png`
- If elsewhere, update path in `create_icon.py`

### "Icon not showing on .exe"

**Possible causes**:
1. Icon file missing when building
2. Need to rebuild: `python build_installer.py`
3. Windows cache: restart File Explorer

**Fix**:
```cmd
# Clean and rebuild
rmdir /s /q build dist
del PryntKioskInstaller.spec
python build_installer.py
```

### "Icon quality poor"

**Solution**: Use higher resolution source image
- Minimum: 256x256 pixels
- Recommended: 512x512 pixels or higher
- Format: PNG with transparency

---

## How It Works

The build script (`build_installer.py`) checks for `prynt_icon.ico`:

```python
# From build_installer.py
ICON_FILE = Path(__file__).parent / 'prynt_icon.ico'
if ICON_FILE.exists():
    PYINSTALLER_OPTS.extend(['--icon', str(ICON_FILE)])
```

If found, PyInstaller embeds it into the .exe.

---

## File Structure

After creating icon:

```
installer/
├── prynt_installer.py          # Main installer
├── build_installer.py          # Build script
├── create_icon.py              # Icon creator (NEW)
├── prynt_icon.ico              # Generated icon (NEW)
├── requirements.txt
└── dist/
    └── PryntKioskInstaller.exe # With icon! ✅
```

---

## Quick Reference

```cmd
# Complete workflow:

# 1. Create icon
python create_icon.py

# 2. Build installer
python build_installer.py

# 3. Check output
dir dist\PryntKioskInstaller.exe

# Done! Icon embedded ✅
```

---

## Summary

- ✅ **Automatic**: Run `create_icon.py` to generate from logo
- ✅ **Manual**: Place `.ico` file as `prynt_icon.ico`
- ✅ **Build**: `build_installer.py` auto-detects and uses it
- ✅ **Result**: Professional branded .exe with Prynt logo

**Your installer will look much more professional with the icon!** 🎨
