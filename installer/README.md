# Pi Bitcoin Miner - Installer Documentation

This directory contains the installer build scripts and configuration files
for creating distributable packages of the Pi Bitcoin Miner application.

## Contents

- `setup.iss` - Inno Setup script for Windows installer
- `build_installer.bat` - Windows build script
- `build_linux.sh` - Linux/Raspberry Pi build script
- `installer_info.txt` - Pre-installation information shown to users
- `icon.ico` - Application icon (optional, create if needed)

## Building the Installer

### Windows

#### Windows Prerequisites

1. **Python 3.8+** installed
2. **PyInstaller**: Install with `pip install pyinstaller`
3. **Inno Setup 6**: Download from
   [jrsoftware.org/isinfo.php](https://jrsoftware.org/isinfo.php)

#### Windows Build Steps

1. Open a command prompt in the project root directory
2. Run the build script:
   ```batch
   cd installer
   build_installer.bat
   ```

This will:
- Install PyInstaller if needed
- Build the standalone executable using PyInstaller
- Create a Windows installer using Inno Setup
- Output the installer to
  `installer/output/PiBitcoinMiner-Setup-1.0.0.exe`

#### Manual Build

If you prefer to build manually:

```batch
# Build executable
pyinstaller pi_bitcoin_miner.spec

# Build installer (requires Inno Setup installed)
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer\setup.iss
```

### Linux / Raspberry Pi

#### Prerequisites
1. **Python 3.8+** installed
2. **PyInstaller**: Install with `pip3 install pyinstaller`
3. **dpkg-deb** (for .deb package, usually pre-installed)

#### Linux Build Steps

1. Open a terminal in the project root directory
2. Make the script executable and run it:
   ```bash
   cd installer
   chmod +x build_linux.sh
   ./build_linux.sh
   ```

This will:
- Install PyInstaller if needed
- Build the standalone executable
- Create a Debian package structure
- Build a .deb package (if dpkg-deb is available)
- Output to `installer/linux_package/`

#### Installing the .deb Package

```bash
sudo dpkg -i installer/linux_package/pi-bitcoin-miner_1.0.0_armhf.deb
```

Or install dependencies first:
```bash
sudo apt-get install -f
```

### Raspberry Pi 4 Setup (Recommended Method)

The Pi 4 is the primary controller for the mining operation. For most users,
we recommend using the automated setup script rather than building an
installer package.

#### Hardware Requirements

- **Raspberry Pi 4** (4GB+ RAM recommended)
- **Raspberry Pi OS** (64-bit recommended)
- **12x Raspberry Pi Pico** boards (or 4-20 workers)
- **Powered USB Hubs** (one per bank of 4 Picos)
- **Stable internet connection**
- **microSD card** (32GB+ recommended)

#### Hardware Connection

Connect your hardware in banks:
```text
[Pi 4 USB Port 1] → [USB Hub A] → [Pico 0,1,2,3] (Bank A)
[Pi 4 USB Port 2] → [USB Hub B] → [Pico 4,5,6,7] (Bank B)
[Pi 4 USB Port 3] → [USB Hub C] → [Pico 8,9,10,11] (Bank C)
```

**Important**: Use powered USB hubs to ensure stable power delivery to all
Pico boards.

#### Quick Setup on Raspberry Pi 4

1. **Install Raspberry Pi OS**
   - Use Raspberry Pi Imager to flash OS to microSD card
   - Enable SSH during imaging (recommended)
   - Boot the Pi 4

2. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/pi-bitcoin-miner.git
   cd pi-bitcoin-miner
   ```

3. **Run Automated Setup**
   ```bash
   chmod +x scripts/setup_pi4.sh
   ./scripts/setup_pi4.sh
   ```

   The script will:
   - Update system packages
   - Install Python 3 and dependencies
   - Create a virtual environment
   - Install all required Python packages
   - Set up directory structure
   - Create configuration template

4. **Configure Mining Settings**

   Edit the configuration file:
   ```bash
   nano config/mining_config.json
   ```

   Key settings for multi-bank setup:
   ```json
   {
     "worker_settings": {
       "expected_workers": 12,
       "workers_per_bank": 4,
       "number_of_banks": 3,
       "reconnect_delay": 5
     },
     "pool": {
       "url": "stratum+tcp://pool.example.com:3333",
       "worker_name": "worker1",
       "password": "x"
     }
   }
   ```

   - Set `expected_workers` to your total number of Picos
   - Set `number_of_banks` based on your USB hub setup (1-5)
   - Configure pool details for real mining
   - Use `"MINING_MODE": "test"` for testing

5. **Flash Pico Firmware**

   Before starting mining, flash MicroPython firmware to each Pico:
   ```bash
   # See pico_firmware/README.md for detailed instructions
   ./scripts/flash_pico.sh
   ```

   Or manually:
   - Hold BOOTSEL button on Pico while connecting USB
   - Copy `.uf2` firmware file to mounted drive
   - Pico will reboot automatically
   - Repeat for all Picos

6. **Start Mining**
   ```bash
   ./scripts/start_mining.sh
   ```

   Or activate the environment and run directly:
   ```bash
   source venv/bin/activate
   python3 controller/main.py
   ```

#### Pi 4 System Recommendations

For optimal performance on Raspberry Pi 4:

1. **Enable SSH** for remote management:
   ```bash
   sudo raspi-config
   # Navigate to Interface Options → SSH → Enable
   ```

2. **Set Static IP** for reliable network access:
   ```bash
   sudo nano /etc/dhcpcd.conf
   # Add:
   # interface eth0
   # static ip_address=192.168.1.100/24
   # static routers=192.168.1.1
   # static domain_name_servers=8.8.8.8
   ```

3. **Increase USB Power** if using many devices:
   ```bash
   sudo nano /boot/config.txt
   # Add:
   # max_usb_current=1
   ```

4. **Setup Auto-Start** on boot:
   ```bash
   sudo nano /etc/systemd/system/bitcoin-miner.service
   ```

   Add:
   ```ini
   [Unit]
   Description=Pi Bitcoin Miner
   After=network.target

   [Service]
   Type=simple
   User=pi
   WorkingDirectory=/home/pi/pi-bitcoin-miner
   ExecStart=/home/pi/pi-bitcoin-miner/venv/bin/python3 controller/main.py
   Restart=on-failure
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

   Enable the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable bitcoin-miner.service
   sudo systemctl start bitcoin-miner.service
   ```

5. **Monitor Performance**:
   ```bash
   # View logs
   tail -f logs/mining.log

   # Check service status
   sudo systemctl status bitcoin-miner

   # Monitor system resources
   htop
   ```

#### Troubleshooting Pi 4 Setup

**Picos not detected:**
- Check USB connections and powered hub status
- Run `lsusb` to verify Picos are visible
- Try different USB ports
- Ensure MicroPython firmware is flashed

**Permission errors:**
- Add user to dialout group: `sudo usermod -a -G dialout $USER`
- Log out and back in for changes to take effect

**Import errors:**
- Ensure virtual environment is activated: `source venv/bin/activate`
- Reinstall packages: `pip install -r requirements.txt`

**Network connectivity issues:**
- Check internet connection: `ping 8.8.8.8`
- Verify pool URL in configuration
- Check firewall settings: `sudo ufw status`

For more detailed setup information, see:
- `../docs/SETUP.md` - Complete setup guide
- `../docs/QUICKSTART.md` - Quick start guide
- `../docs/MULTI_BANK_SETUP.md` - Multi-bank configuration

## Customization

### Changing Version Number

Edit these files:
- `setup.py` - Update `version="1.0.0"`
- `installer/setup.iss` - Update `#define MyAppVersion "1.0.0"`
- `installer/build_linux.sh` - Update version in package paths

### Adding Application Icon

1. Create an icon file: `installer/icon.ico` (Windows) or `installer/icon.png` (Linux)
2. The build scripts will automatically include it if present

### Modifying Installation Behavior

**Windows (Inno Setup):**
- Edit `installer/setup.iss`
- Modify the `[Files]`, `[Tasks]`, or `[Run]` sections
- See [Inno Setup documentation](https://jrsoftware.org/ishelp/)

**Linux (Debian):**
- Edit `installer/build_linux.sh`
- Modify the package structure or control file
- See [Debian packaging guide](https://www.debian.org/doc/manuals/maint-guide/)

## Distribution

### Windows Distribution

Distribute the file: `installer/output/PiBitcoinMiner-Setup-1.0.0.exe`

Users can:
1. Download and run the installer
2. Follow the installation wizard
3. Launch from Start Menu or Desktop shortcut

### Linux/Raspberry Pi Distribution

Distribute the file:
`installer/linux_package/pi-bitcoin-miner_1.0.0_armhf.deb`

Users can install with:
```bash
sudo dpkg -i pi-bitcoin-miner_1.0.0_armhf.deb
sudo apt-get install -f  # Install dependencies if needed
```

Or run the executable directly from `dist/pi-bitcoin-miner/`

## Troubleshooting

### PyInstaller Issues

**"Module not found" errors:**
- Add missing modules to `hiddenimports` in `pi_bitcoin_miner.spec`

**Large executable size:**
- Exclude unnecessary packages in the spec file
- Use UPX compression (enabled by default)

### Inno Setup Issues

**"Cannot find file" errors:**
- Verify paths in `setup.iss` are correct
- Ensure PyInstaller has completed successfully
- Check that `dist/pi-bitcoin-miner/` exists

### Linux Package Issues

**Missing dependencies:**
```bash
sudo apt-get install python3 python3-pip python3-serial \
  python3-aiohttp
```

**Permission errors:**
- Run the build script with appropriate permissions
- Some files may need `chmod +x`

## Testing

Before distributing:

1. **Test the executable** directly:
   - Windows: Run `dist\pi-bitcoin-miner\pi-bitcoin-miner.exe`
   - Linux: Run `dist/pi-bitcoin-miner/pi-bitcoin-miner`

2. **Test the installer**:
   - Install on a clean system
   - Verify all files are copied
   - Test shortcuts and menu entries
   - Run the installed application
   - Test uninstallation

3. **Verify configuration**:
   - Check that `config/mining_config.json` is accessible
   - Verify documentation files are included
   - Test firmware flashing scripts

## Additional Resources

- [PyInstaller Documentation](https://pyinstaller.org/)
- [Inno Setup Documentation](https://jrsoftware.org/ishelp/)
- [Debian Packaging Guide](https://www.debian.org/doc/manuals/maint-guide/)
