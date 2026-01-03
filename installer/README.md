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
