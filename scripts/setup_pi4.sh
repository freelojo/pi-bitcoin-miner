#!/bin/bash
# Setup script for Raspberry Pi 4 controller

echo "=========================================="
echo "Bitcoin Miner Controller Setup"
echo "=========================================="

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null; then
    echo "Warning: This doesn't appear to be a Raspberry Pi"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Update system
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Python 3 and pip
echo "Installing Python dependencies..."
sudo apt-get install -y python3 python3-pip python3-venv

# Create virtual environment
echo "Creating Python virtual environment..."
cd "$(dirname "$0")/.."
python3 -m venv venv
source venv/bin/activate

# Install Python packages
echo "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Create config from example if it doesn't exist
if [ ! -f "config/.env" ]; then
    echo "Creating config file..."
    cp config/.env.example config/.env
    echo "Please edit config/.env with your mining pool settings"
fi

# Create logs directory
mkdir -p logs

# Set permissions
chmod +x scripts/*.sh

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit config/.env with your mining pool settings"
echo "2. Flash firmware to all Pico boards (see pico_firmware/README.md)"
echo "3. Connect Picos to USB hub"
echo "4. Run: ./scripts/start_mining.sh"
echo ""
