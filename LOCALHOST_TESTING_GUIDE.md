# Localhost Testing Guide

Complete guide for testing the Prynt installer on your local network before deploying to production.

## Overview

**Setup**: Mac runs backend server → Windows laptop runs installer → Both connect on local network

This allows you to test the complete installation flow without hosting the server on the internet.

---

## Part 1: Mac Setup (Backend Server)

### Step 1: Find Your Mac's Local IP Address

Open Terminal and run:

```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

**Example output**:
```
inet 192.168.1.10 netmask 0xffffff00 broadcast 192.168.1.255
```

Your Mac's IP: **192.168.1.10** (yours will be different)

**Alternative method** (easier):
1. Open System Preferences → Network
2. Select your active connection (Wi-Fi or Ethernet)
3. Note the IP address shown

### Step 2: Configure Backend for Network Access

The backend needs to listen on all network interfaces (not just localhost).

**Check current server.py startup**:

```bash
cd backend
grep "uvicorn.run" server.py
```

Should show:
```python
uvicorn.run(app, host='0.0.0.0', port=8000)
```

✅ If it says `host='0.0.0.0'` - you're good!
❌ If it says `host='127.0.0.1'` or `host='localhost'` - needs update

**To update** (if needed):
```python
# In server.py, at the bottom:
uvicorn.run(app, host='0.0.0.0', port=8000)  # Listens on all interfaces
```

### Step 3: Check Firewall Settings

Make sure Mac firewall allows Python to accept connections:

1. System Preferences → Security & Privacy → Firewall
2. If firewall is ON, click "Firewall Options"
3. Ensure Python is allowed, or add it

**To temporarily disable firewall for testing**:
```bash
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off
```

**Re-enable after testing**:
```bash
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
```

### Step 4: Start the Backend Server

```bash
cd backend
python server.py
```

**Expected output**:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

✅ Server is now accessible at: `http://192.168.1.10:8000`

### Step 5: Verify Server is Accessible

From Mac, test the server:

```bash
curl http://192.168.1.10:8000/api/features
```

Should return JSON with feature flags.

**Or** open in browser:
```
http://192.168.1.10:8000/api/features
```

### Step 6: Update CORS Settings (Important!)

To allow requests from Windows laptop, update backend `.env`:

```bash
# backend/.env
CORS_ORIGINS=*
```

Or specify your Windows IP:
```bash
CORS_ORIGINS=http://192.168.1.20,http://localhost:3000
```

**Restart server** after changing .env:
```bash
# Press CTRL+C to stop, then:
python server.py
```

---

## Part 2: Windows Laptop Setup

### Step 1: Verify Network Connection

Ensure Windows laptop is on **same network** as Mac.

**Check Windows IP**:
```cmd
ipconfig
```

Look for IPv4 Address - should be in same subnet as Mac:
- Mac: `192.168.1.10` ✅
- Windows: `192.168.1.20` ✅ (same 192.168.1.x subnet)

### Step 2: Test Connection to Mac

Open Command Prompt:

```cmd
ping 192.168.1.10
```

**Expected output**:
```
Reply from 192.168.1.10: bytes=32 time=2ms TTL=64
Reply from 192.168.1.10: bytes=32 time=1ms TTL=64
```

✅ Connection working!

**If ping fails**:
- Check both devices on same Wi-Fi network
- Check Mac firewall settings
- Verify Mac's IP address is correct

### Step 3: Test Backend API Access

Open browser on Windows and visit:
```
http://192.168.1.10:8000/api/features
```

Should show JSON response. ✅ Backend is accessible!

### Step 4: Build or Transfer Installer

**Option A: Build on Windows**
```cmd
cd C:\path\to\prynt\installer
pip install -r requirements.txt
pip install pyinstaller
python build_installer.py
```

**Option B: Transfer from Mac**
If you built elsewhere, just copy `PryntKioskInstaller.exe` to Windows

---

## Part 3: Creating Test Kiosk in Admin Panel

### Step 1: Start Frontend (on Mac)

```bash
cd frontend
npm start
```

Opens at: `http://localhost:3000`

### Step 2: Login to Admin Panel

1. Go to `http://localhost:3000/admin`
2. Login with admin credentials
3. Navigate to **Kiosks** section

### Step 3: Create Test Kiosk

Click "Add Kiosk" and fill in:

- **Name**: `Test Kiosk - Windows Laptop`
- **City**: `Test City`
- **Location**: `Development Lab`
- **Pricing**: Use defaults or customize
- **Student Saver**: Enable if testing that feature
- **Pages/Ink/Paper**: Any values (for testing)

Click **Save**.

### Step 4: Copy Setup Code

After creating kiosk, you'll see:

```
✓ Kiosk created successfully!

Setup Code: AB2C3D
Valid for: 24 hours
Share this code with installation team
```

**Copy this code**: `AB2C3D`

---

## Part 4: Running the Installer (Windows)

### Step 1: Run Installer as Administrator

1. Navigate to `dist\PryntKioskInstaller.exe`
2. **Right-click** → "Run as administrator"
3. Click "Yes" on UAC prompt

### Step 2: Enter Server Details

Installer window opens with Prynt branding:

**Server URL**: 
```
http://192.168.1.10:8000
```
(Use your Mac's actual IP)

**Setup Code**: 
```
AB2C3D
```
(From admin panel)

Click **"Validate Setup Code"**

### Step 3: Verify Validation

Should show:
```
✓ Setup code validated successfully!

Kiosk: Test Kiosk - Windows Laptop
Location: Development Lab • Test City
```

### Step 4: Select Printer

Installer auto-detects Windows printers:

1. See list of available printers
2. Default printer is pre-selected
3. Choose the printer for testing
4. Click **"Install Prynt Kiosk"**

### Step 5: Confirm Installation

Review installation details:
```
Install Prynt Kiosk with the following settings?

Kiosk: Test Kiosk - Windows Laptop
Printer: Microsoft Print to PDF
Server: http://192.168.1.10:8000

The installation will:
• Install agent to C:\Program Files\Prynt
• Create desktop shortcut
• Add agent to startup
• Configure kiosk launcher
```

Click **"Yes"**

### Step 6: Wait for Installation

Progress shown in status bar:
```
Installing Prynt Kiosk...
```

Should complete in 5-10 seconds.

### Step 7: Installation Complete

Success message:
```
✓ Prynt Kiosk installed successfully!

Installed to: C:\Program Files\Prynt

Next steps:
1. Double-click 'Prynt Kiosk' on desktop to launch
2. Agent will start automatically on system boot
3. To manually start agent: Run 'start_agent.bat'

The kiosk screen will open in full-screen mode.
Press F11 or Alt+F4 to exit kiosk mode.
```

---

## Part 5: Testing the Installation

### Test 1: Launch Kiosk Screen

1. **Double-click** "Prynt Kiosk" on desktop
2. Chrome should open in full-screen (kiosk mode)
3. Should load: `http://192.168.1.10:8000/kiosk/{kiosk_id}`
4. Kiosk interface should appear

**Exit kiosk mode**: Press `F11` or `Alt+F4`

### Test 2: Start Print Agent

1. Open Command Prompt **as Administrator**
2. Navigate to install directory:
   ```cmd
   cd "C:\Program Files\Prynt"
   start_agent.bat
   ```
3. Should see agent logs:
   ```
   [2024-08-04 10:30:00] Prynt Agent started for kiosk: Test Kiosk (abc-123)
   [2024-08-04 10:30:00] Printer: Microsoft Print to PDF
   [2024-08-04 10:30:00] Server: http://192.168.1.10:8000
   ```

### Test 3: Verify Agent Connection

In admin panel (Mac):
1. Go to Kiosks section
2. Find "Test Kiosk - Windows Laptop"
3. Status should show **"Online"** (green indicator)
4. Last seen: "Just now"

### Test 4: Print Test Job

From kiosk screen:
1. Upload a test PDF
2. Configure print settings
3. Process payment (use test mode)
4. Submit print job

**Check agent logs**:
```
[2024-08-04 10:35:00] Processing job job-123
[2024-08-04 10:35:01] Job job-123 completed successfully
```

### Test 5: Check Installation Files

Verify all files created:

```cmd
dir "C:\Program Files\Prynt"
```

Should show:
```
├── agent\
│   └── agent.py
├── config\
├── logs\
│   └── agent_20240804.log
├── launch_kiosk.bat
└── start_agent.bat
```

---

## Troubleshooting

### Cannot Connect to Server

**Symptoms**: "Cannot connect to server" error during validation

**Solutions**:
1. ✅ Verify Mac IP: `ifconfig | grep inet`
2. ✅ Verify server running: Check Terminal on Mac
3. ✅ Test connection: `ping 192.168.1.10` from Windows
4. ✅ Test API: Visit `http://192.168.1.10:8000/api/features` in browser
5. ✅ Check firewall: Temporarily disable Mac firewall
6. ✅ Check CORS: Ensure `CORS_ORIGINS=*` in backend/.env

### Setup Code Invalid

**Symptoms**: "Invalid or expired setup code"

**Solutions**:
1. ✅ Verify code in admin panel
2. ✅ Check code not expired (24hr limit)
3. ✅ Ensure code not already used
4. ✅ Check server database connection
5. ✅ Create new kiosk and try new code

### Printer Not Detected

**Symptoms**: "No printers found"

**Solutions**:
1. ✅ Install a printer (even virtual like "Microsoft Print to PDF")
2. ✅ Click "Refresh Printers" button
3. ✅ Run installer as Administrator
4. ✅ Check printer is not offline

### Agent Won't Start

**Symptoms**: Agent crashes or exits immediately

**Solutions**:
1. ✅ Check Python installed on Windows
2. ✅ View logs: `C:\Program Files\Prynt\logs\agent_YYYYMMDD.log`
3. ✅ Test manually: `cd "C:\Program Files\Prynt\agent" && python agent.py`
4. ✅ Verify server URL accessible from Windows
5. ✅ Check kiosk_id in agent.py matches database

### Kiosk Screen Won't Load

**Symptoms**: Chrome opens but page doesn't load

**Solutions**:
1. ✅ Check URL: Should be `http://MAC_IP:8000/kiosk/KIOSK_ID`
2. ✅ Test URL in regular browser first
3. ✅ Verify kiosk exists in database
4. ✅ Check CORS settings
5. ✅ View browser console (F12 before kiosk mode)

### "Run as Administrator" Required

**Symptoms**: Permission errors during installation

**Solutions**:
1. ✅ Always right-click installer → "Run as administrator"
2. ✅ UAC prompt must be accepted
3. ✅ Cannot install to Program Files without admin rights

---

## Network Configuration Reference

### Same Network Configuration

✅ **Correct Setup**:
```
Mac (Backend):     192.168.1.10
Windows (Kiosk):   192.168.1.20
Router Gateway:    192.168.1.1
Subnet Mask:       255.255.255.0
```

❌ **Wrong Setup** (different networks):
```
Mac:     192.168.1.10  (Network A)
Windows: 192.168.2.20  (Network B)  ← Different subnet!
```

### Firewall Configuration

**Mac Firewall Rules**:
```
✅ Allow: Python
✅ Allow: Incoming connections on port 8000
✅ Allow: Node.js (for frontend)
```

**Windows Firewall Rules**:
```
✅ Allow: Google Chrome
✅ Allow: Python (for agent)
✅ Allow: Outgoing connections to Mac IP
```

---

## Testing Checklist

Before marking installation as successful, verify:

- [ ] Backend server running on Mac (0.0.0.0:8000)
- [ ] Mac IP address identified and noted
- [ ] Windows laptop can ping Mac IP
- [ ] Backend API accessible from Windows browser
- [ ] Kiosk created in admin panel
- [ ] Setup code copied (6 characters)
- [ ] Installer runs with admin privileges
- [ ] Setup code validates successfully
- [ ] Printer detected and selected
- [ ] Installation completes without errors
- [ ] Desktop shortcut created
- [ ] Agent starts without errors
- [ ] Agent shows in admin panel as online
- [ ] Kiosk screen launches in Chrome
- [ ] Kiosk loads correct URL
- [ ] Test print job processes successfully
- [ ] Installation logs readable

---

## Quick Reference

### Mac Commands
```bash
# Find IP
ifconfig | grep "inet " | grep -v 127.0.0.1

# Start backend
cd backend && python server.py

# Start frontend
cd frontend && npm start

# Test API
curl http://192.168.1.10:8000/api/features
```

### Windows Commands
```cmd
# Check IP
ipconfig

# Test connection
ping 192.168.1.10

# Test agent manually
cd "C:\Program Files\Prynt\agent"
python agent.py

# View logs
notepad "C:\Program Files\Prynt\logs\agent_20240804.log"
```

### Server URLs
```
Backend API:     http://192.168.1.10:8000/api/
Admin Panel:     http://localhost:3000/admin
Kiosk Screen:    http://192.168.1.10:8000/kiosk/{kiosk_id}
```

---

## Next Steps After Successful Testing

1. ✅ Document any issues encountered
2. ✅ Test with different printers
3. ✅ Test with multiple Windows machines
4. ✅ Test Student Saver feature (if enabled)
5. ✅ Test print job queue
6. ✅ Test agent auto-restart on boot
7. 🚀 Prepare for production deployment with hosted server

---

## Support

For localhost testing issues:
- Check this guide's Troubleshooting section
- Review installer/README.md
- Check backend/frontend logs
- Test each component independently

For production deployment:
- Update server URL to production domain
- Configure SSL/HTTPS
- Set up proper database backups
- Configure monitoring and alerts
