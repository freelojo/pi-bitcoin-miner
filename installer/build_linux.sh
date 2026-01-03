#!/bin/bash
# Build script for Pi Bitcoin Miner Linux Package
# This creates a standalone executable and optional .deb package

set -e

echo "========================================"
echo "Pi Bitcoin Miner - Linux Builder"
echo "========================================"
echo

# Check if PyInstaller is installed
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "[ERROR] PyInstaller is not installed."
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
fi

# Step 1: Clean previous builds
echo "[1/3] Cleaning previous builds..."
rm -rf ../dist ../build
rm -rf linux_package
echo "Done."
echo

# Step 2: Build executable with PyInstaller
echo "[2/3] Building executable with PyInstaller..."
cd ..
pyinstaller pi_bitcoin_miner.spec
cd installer
echo "Done."
echo

# Step 3: Create .deb package structure (optional)
echo "[3/3] Creating Debian package structure..."
mkdir -p linux_package/pi-bitcoin-miner_1.0.0/DEBIAN
mkdir -p linux_package/pi-bitcoin-miner_1.0.0/usr/bin
mkdir -p linux_package/pi-bitcoin-miner_1.0.0/usr/share/pi-bitcoin-miner
mkdir -p linux_package/pi-bitcoin-miner_1.0.0/usr/share/applications
mkdir -p linux_package/pi-bitcoin-miner_1.0.0/usr/share/doc/pi-bitcoin-miner

# Create control file
cat > linux_package/pi-bitcoin-miner_1.0.0/DEBIAN/control << EOF
Package: pi-bitcoin-miner
Version: 1.0.0
Section: utils
Priority: optional
Architecture: armhf
Depends: python3 (>= 3.8), python3-serial, python3-aiohttp
Maintainer: Pi Bitcoin Miner Team <your.email@example.com>
Description: Distributed Bitcoin mining using Raspberry Pi
 This is an educational project for learning about Bitcoin mining
 using Raspberry Pi 4 as controller and Pico boards as workers.
 Warning: Not profitable for actual mining.
EOF

# Copy files
cp -r ../dist/pi-bitcoin-miner/* linux_package/pi-bitcoin-miner_1.0.0/usr/share/pi-bitcoin-miner/
ln -sf /usr/share/pi-bitcoin-miner/pi-bitcoin-miner linux_package/pi-bitcoin-miner_1.0.0/usr/bin/pi-bitcoin-miner
cp ../README.md linux_package/pi-bitcoin-miner_1.0.0/usr/share/doc/pi-bitcoin-miner/
cp ../LICENSE linux_package/pi-bitcoin-miner_1.0.0/usr/share/doc/pi-bitcoin-miner/

# Create desktop entry
cat > linux_package/pi-bitcoin-miner_1.0.0/usr/share/applications/pi-bitcoin-miner.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Pi Bitcoin Miner
Comment=Distributed Bitcoin mining controller
Exec=/usr/bin/pi-bitcoin-miner
Icon=/usr/share/pi-bitcoin-miner/icon.png
Terminal=true
Categories=Development;Education;
EOF

# Set permissions
chmod 755 linux_package/pi-bitcoin-miner_1.0.0/DEBIAN
chmod 755 linux_package/pi-bitcoin-miner_1.0.0/usr/bin/pi-bitcoin-miner

# Build .deb package
if command -v dpkg-deb &> /dev/null; then
    echo "Building .deb package..."
    dpkg-deb --build linux_package/pi-bitcoin-miner_1.0.0
    mv linux_package/pi-bitcoin-miner_1.0.0.deb linux_package/pi-bitcoin-miner_1.0.0_armhf.deb
    echo "Done."
else
    echo "[WARNING] dpkg-deb not found. Skipping .deb creation."
    echo "Package structure created in: linux_package/"
fi

echo
echo "========================================"
echo "BUILD COMPLETE!"
echo "========================================"
echo
echo "Executable location: ../dist/pi-bitcoin-miner/"
if [ -f "linux_package/pi-bitcoin-miner_1.0.0_armhf.deb" ]; then
    echo "Debian package:      linux_package/pi-bitcoin-miner_1.0.0_armhf.deb"
fi
echo
