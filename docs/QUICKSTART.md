# Quick Start Guide

## Hardware Checklist

- [ ] Raspberry Pi 4 Model B
- [ ] 4x Raspberry Pi Pico boards
- [ ] Powered USB hub
- [ ] USB cables for each Pico
- [ ] MicroSD card with Raspberry Pi OS

## Quick Setup (5 Steps)

### 1. Flash MicroPython to Picos

1. Download: <https://micropython.org/download/rp2-pico/>
2. Hold BOOTSEL, connect Pico, copy .uf2 file
3. Repeat for all 4 Picos

### 2. Upload Mining Firmware to Picos

```bash
# Connect each Pico one at a time
./scripts/flash_pico.sh 1 /dev/ttyACM0
./scripts/flash_pico.sh 2 /dev/ttyACM1
./scripts/flash_pico.sh 3 /dev/ttyACM2
./scripts/flash_pico.sh 4 /dev/ttyACM3
```

### 3. Setup Pi 4 Controller

```bash
cd pi-bitcoin-miner
./scripts/setup_pi4.sh
```

### 4. Configure Settings

```bash
cp config/.env.example config/.env
nano config/.env
```

Set `MINING_MODE=test` for initial testing.

### 5. Connect Hardware & Start Mining

```bash
# Connect all Picos to USB hub
# Connect hub to Pi 4
./scripts/start_mining.sh
```

## Expected Output

```text
Bitcoin Miner Controller
======================================================================
Worker Status:
  0     /dev/ttyACM0    Connected    75.23 H/s
  1     /dev/ttyACM1    Connected    73.45 H/s
  2     /dev/ttyACM2    Connected    74.89 H/s
  3     /dev/ttyACM3    Connected    76.12 H/s

Overall Statistics:
  Total Hashrate:    299.69 H/s
======================================================================
```

## Troubleshooting

**Picos not detected?**

- Check USB cables (some are power-only)
- Add yourself to dialout group: `sudo usermod -a -G dialout $USER`
- Verify MicroPython: `python -m serial.tools.miniterm /dev/ttyACM0 115200`

**Low hashrate?**

- Normal: 50-100 H/s per Pico
- Overclock in `pico_firmware/boot.py`: `machine.freq(200000000)`

**Import errors?**

- Activate venv: `source venv/bin/activate`
- Install deps: `pip install -r requirements.txt`

## Next Steps

- Read [SETUP.md](SETUP.md) for detailed instructions
- Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system
- Join Bitcoin testnet for safe experimentation
- Monitor for 24 hours to ensure stability

## Reality Check ⚠️

- Expected total hashrate: ~300 H/s
- Modern ASIC miner: 100 TH/s (100,000,000,000,000 H/s)
- This is **educational only** - not profitable!
