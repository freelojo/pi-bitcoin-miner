# Raspberry Pi Pico Firmware

This directory contains the MicroPython firmware for the Raspberry Pi Pico
mining workers.

## Files

- `main.py` - Main firmware that runs on each Pico
- `boot.py` - Boot configuration (optional)
- `sha256_optimized.py` - Optimized SHA-256 implementation (optional)

## Flashing Instructions

### 1. Install MicroPython on Pico

1. Download latest MicroPython firmware for Pico from:
   <https://micropython.org/download/rp2-pico/>
2. Hold BOOTSEL button while connecting Pico to computer
3. Pico will appear as USB mass storage device
4. Copy `.uf2` firmware file to the Pico drive
5. Pico will reboot and run MicroPython

### 2. Upload Mining Firmware

Using `ampy` (recommended):

```bash
pip install adafruit-ampy
ampy --port COM3 put main.py
```

Or using Thonny IDE:

1. Install Thonny: <https://thonny.org/>
2. Select MicroPython (Raspberry Pi Pico) interpreter
3. Open `pico_firmware/main.py` and save to Pico

### 3. Verify Installation

Connect to Pico serial console:

```bash
# Windows
python -m serial.tools.miniterm COM3 115200

# Linux/Mac
python -m serial.tools.miniterm /dev/ttyACM0 115200
```

You should see "Pico Bitcoin Miner starting..." on boot.

## Performance Notes

- Expected hashrate: ~50-100 H/s per Pico (varies with optimization)
- The RP2040 CPU runs at 133 MHz (can be overclocked to 250+ MHz)
- SHA-256 is computationally intensive for the Pico's ARM Cortex-M0+

## Optimization Ideas

1. **Overclock the CPU**: Increase frequency for more hashes/second
2. **Assembly optimization**: Implement SHA-256 in ARM assembly
3. **PIO state machines**: Use Pico's PIO for parallel operations
4. **Reduce communication overhead**: Batch progress updates

## Troubleshooting

- **Pico not detected**: Try different USB cable, some are power-only
- **Import errors**: Ensure MicroPython firmware is installed correctly
- **Random resets**: Power supply may be insufficient, use powered USB hub
- **Low hashrate**: Normal for ARM Cortex-M0+, consider overclocking
