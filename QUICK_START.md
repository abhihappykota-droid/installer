# Prynt Installer - Quick Start

**5-minute guide to get started with localhost testing**

## Prerequisites

- ✅ Mac with backend running
- ✅ Windows laptop on same network
- ✅ Python installed on both machines

---

## Mac (Backend) - 2 minutes

### 1. Find your IP address
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```
Note the IP (e.g., `192.168.1.10`)

### 2. Start backend
```bash
cd backend
python server.py
```

### 3. Create kiosk in admin panel
1. Go to `http://localhost:3000/admin`
2. Kiosks → Add Kiosk
3. Copy the **6-digit setup code**

---

## Windows (Installer) - 3 minutes

### 1. Build installer (first time only)
```cmd
cd installer
pip install -r requirements.txt
pip install pyinstaller
python build_installer.py
```

### 2. Run installer
```cmd
Right-click dist\PryntKioskInstaller.exe
→ Run as administrator
```

### 3. Enter details
- **Server URL**: `http://192.168.1.10:8000` (your Mac's IP)
- **Setup Code**: `ABC123` (from admin panel)
- Click "Validate Setup Code"

### 4. Select printer & install
- Choose printer from list
- Click "Install Prynt Kiosk"
- Wait 10 seconds
- Done! ✅

---

## Test It

1. **Double-click** "Prynt Kiosk" on desktop
2. Chrome opens in full-screen mode
3. Upload a test document
4. Print! 🎉

---

## Troubleshooting One-Liners

**Can't connect**: Ping Mac from Windows: `ping 192.168.1.10`

**Invalid code**: Create new kiosk in admin panel

**No printers**: Install "Microsoft Print to PDF" printer

**Need logs**: `notepad "C:\Program Files\Prynt\logs\agent_YYYYMMDD.log"`

---

## Full Documentation

- **Build Instructions**: `BUILD_INSTRUCTIONS.md`
- **Localhost Testing**: `LOCALHOST_TESTING_GUIDE.md`
- **Complete Guide**: `README.md`

---

**That's it!** You now have a fully functional Prynt kiosk running on your local network.
