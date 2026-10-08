# Prynt Kiosk Installer

Windows installer for Prynt printing kiosk system. Provides automated setup with server connection, printer detection, and agent configuration.

## Features

- **Setup Code Validation**: Secure kiosk registration using 6-digit codes
- **Auto Printer Detection**: Automatically detects installed Windows printers
- **Agent Installation**: Installs and configures print agent as Windows service
- **Kiosk Launcher**: Creates Chrome kiosk mode launcher
- **Desktop Shortcuts**: Adds convenient desktop shortcuts
- **Auto Startup**: Configures agent to start on system boot
- **Prynt Branding**: Professional installer with Prynt logo and colors

## Building the Installer

### Prerequisites

1. **Windows Development Machine** (or Windows VM)
2. **Python 3.7+** installed
3. **Required packages**:
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

### Build Steps

1. Navigate to installer directory:
   ```bash
   cd installer
   ```

2. Run the build script:
   ```bash
   python build_installer.py
   ```

3. Find the compiled .exe in:
   ```
   installer/dist/PryntKioskInstaller.exe
   ```

### Build Options

The build script (`build_installer.py`) supports:
- Single-file executable (--onefile)
- No console window (--windowed)
- Version information embedded
- Optional icon file (place `prynt_icon.ico` in installer/ directory)

## Using the Installer

### For Administrators

1. **Create Kiosk in Admin Panel**:
   - Go to Admin → Kiosks → Add Kiosk
   - Fill in kiosk details
   - Note the **setup code** (valid for 24 hours)

2. **Share with Installation Team**:
   - Provide `PryntKioskInstaller.exe`
   - Share the 6-digit setup code
   - Share server URL (for localhost testing: `http://YOUR_MAC_IP:8000`)

### For Installation Team

1. **Run Installer** (as Administrator):
   - Right-click `PryntKioskInstaller.exe`
   - Select "Run as administrator"

2. **Enter Server Details**:
   - Server URL: `http://192.168.1.10:8000` (example)
   - Setup Code: `ABC123` (from admin)

3. **Select Printer**:
   - Choose from detected printers
   - Or refresh to re-scan

4. **Complete Installation**:
   - Click "Install Prynt Kiosk"
   - Wait for completion
   - Kiosk will launch automatically

## Installation Location

```
C:\Program Files\Prynt\
├── agent\
│   └── agent.py          # Print agent script
├── config\
│   └── (configuration files)
├── logs\
│   └── agent_YYYYMMDD.log
├── launch_kiosk.bat      # Chrome kiosk launcher
└── start_agent.bat       # Agent service starter
```

## Desktop Shortcuts

After installation, you'll find:
- **Prynt Kiosk.lnk** - Launch kiosk in full-screen mode

## Auto-Start

The agent is configured to start automatically on system boot via Windows Startup folder.

## Localhost Testing (Dev Mode)

For testing before hosting on internet:

### Mac (Backend Server):

1. Find your Mac's local IP:
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```
   Example: `192.168.1.10`

2. Start backend with network access:
   ```bash
   cd backend
   python server.py
   ```
   Server will be available at: `http://192.168.1.10:8000`

### Windows (Kiosk Machine):

1. Ensure both machines on same network
2. Run installer with server URL: `http://192.168.1.10:8000`
3. Enter setup code from admin panel

## Troubleshooting

### Printer Not Found
- Ensure printer is installed and set as default
- Check printer is turned on
- Click "Refresh Printers" button

### Cannot Connect to Server
- Check server URL is correct
- Verify server is running: visit `http://SERVER_URL/api/features`
- Ensure both machines on same network (for localhost)
- Check firewall settings

### Setup Code Invalid
- Code may have expired (24hr limit)
- Code may have been used already
- Contact admin for new code

### Agent Not Starting
- Check logs in: `C:\Program Files\Prynt\logs\`
- Verify Python is installed on target machine
- Run `start_agent.bat` manually to see errors

### Kiosk Won't Launch
- Ensure Google Chrome is installed
- Check server URL is reachable
- Verify kiosk_id in agent config

## Manual Operations

### Start Agent Manually:
```bash
cd "C:\Program Files\Prynt"
start_agent.bat
```

### Launch Kiosk Manually:
```bash
cd "C:\Program Files\Prynt"
launch_kiosk.bat
```

### View Agent Logs:
```bash
cd "C:\Program Files\Prynt\logs"
notepad agent_20240804.log
```

## Security Notes

- Setup codes expire after 24 hours
- Each setup code can only be used once
- Agent communicates with server via HTTPS (production)
- No sensitive credentials stored on kiosk machine

## Production vs Development

### Development (Localhost):
- Server URL: `http://192.168.1.10:8000`
- Manual server URL entry required
- Used for testing before deployment

### Production (Hosted):
- Server URL: `https://api.prynt.com`
- Server URL pre-configured in installer
- Used for actual deployments

## Support

For installation support:
- Check logs in `C:\Program Files\Prynt\logs\`
- Contact your system administrator
- Refer to main Prynt documentation

## Version History

### v1.0.0 (Phase 1 - Dev Testing)
- Setup code validation system
- Manual server URL input for localhost testing
- Automated printer detection
- Agent installation and configuration
- Chrome kiosk mode launcher
- Desktop shortcuts and auto-startup
- Prynt branding and professional UI
