#!/bin/bash
# Flash MicroPython firmware to a single Pico

if [ -z "$1" ]; then
    echo "Usage: ./flash_pico.sh <pico_number> [serial_port]"
    echo "Example: ./flash_pico.sh 1 /dev/ttyACM0"
    exit 1
fi

PICO_NUM=$1
SERIAL_PORT=$2

echo "Flashing Pico Worker #$PICO_NUM"
echo "================================"

# Check if ampy is installed
if ! command -v ampy &> /dev/null; then
    echo "Installing ampy..."
    pip3 install adafruit-ampy
fi

# If no serial port specified, try to detect
if [ -z "$SERIAL_PORT" ]; then
    echo "Detecting Pico on USB..."
    # Try common ports
    for port in /dev/ttyACM* /dev/ttyUSB*; do
        if [ -e "$port" ]; then
            SERIAL_PORT=$port
            break
        fi
    done
    
    if [ -z "$SERIAL_PORT" ]; then
        echo "Error: Could not detect Pico. Please specify serial port."
        exit 1
    fi
fi

echo "Using serial port: $SERIAL_PORT"

# Upload firmware files
echo "Uploading boot.py..."
ampy --port $SERIAL_PORT put pico_firmware/boot.py /boot.py

echo "Uploading main.py..."
ampy --port $SERIAL_PORT put pico_firmware/main.py /main.py

echo ""
echo "Pico #$PICO_NUM flashed successfully!"
echo "Disconnect and reconnect to start mining firmware"
