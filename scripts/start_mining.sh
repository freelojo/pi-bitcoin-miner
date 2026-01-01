#!/bin/bash
# Start the Bitcoin mining controller

cd "$(dirname "$0")/.."

echo "Starting Bitcoin Miner Controller..."

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Error: Virtual environment not found. Run ./scripts/setup_pi4.sh first"
    exit 1
fi

# Check if config exists
if [ ! -f "config/.env" ]; then
    echo "Error: config/.env not found. Copy from config/.env.example and configure"
    exit 1
fi

# Start the controller
python3 controller/main.py

# Deactivate venv on exit
deactivate
