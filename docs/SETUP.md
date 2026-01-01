# Setup and Installation Guide

This guide will help you set up your Raspberry Pi Bitcoin mining system with
multiple banks of workers.

## Hardware Setup

### 1. Prepare the Hardware

- **Raspberry Pi 4**: Install Raspberry Pi OS (64-bit recommended)
- **12x Raspberry Pi Pico**: No initial setup needed (3 banks of 4)
- **3x Powered USB Hubs**: One per bank, connect to Pi 4 USB ports
- **Power Supply**: Ensure adequate power for Pi 4

### 2. Connect Everything

```text
[Pi 4 USB Port 1] → [USB Hub A] → [Pico 0,1,2,3] (Bank A)
[Pi 4 USB Port 2] → [USB Hub B] → [Pico 4,5,6,7] (Bank B)
[Pi 4 USB Port 3] → [USB Hub C] → [Pico 8,9,10,11] (Bank C)
```

**Note**: Label your USB hubs and Picos for easy identification.
Workers are auto-discovered but maintaining physical order helps
troubleshooting.

## Software Installation

### On Raspberry Pi 4

#### Option A: Automated Setup (Recommended)

```bash
cd pi-bitcoin-miner
chmod +x scripts/*.sh
./scripts/setup_pi4.sh
```

#### Option B: Manual Setup

1. **Update System**

   ```bash
   sudo apt-get upgrade -y
   ```

2. **Install Python Dependencies**

   ```bash
   sudo apt-get install python3 python3-pip python3-venv -y
   ```

3. **Create Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install Python Packages**

   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Settings**

Edit the configuration:

   ```bash
   nano config/mining_config.json
   ```

Important settings for multi-bank setup:

   ```json
   {
     "worker_settings": {
       "expected_workers": 12,
       "workers_per_bank": 4,
       "number_of_banks": 3
     }
   }
   ```

- Set `MINING_MODE=test` for testing
- Adjust `number_of_banks` based on your setup (1-5)
- Set `workers_per_bank` to 4 (recommended)
- Add your Bitcoin wallet address for production
- Configure pool URL if using real mining

### On Each Raspberry Pi Pico

#### 1. Install MicroPython

1. Download MicroPython firmware:
   - Visit: <https://micropython.org/download/rp2-pico/>
   - Download latest `.uf2` file

2. Flash MicroPython:
   - Hold BOOTSEL button on Pico
   - Connect to computer via USB
   - Pico appears as USB drive
   - Copy `.uf2` file to Pico
   - Pico will reboot automatically

#### 2. Upload Mining Firmware

**Using the provided script:**

```bash
# Linux/Mac
./scripts/flash_pico.sh 1 /dev/ttyACM0
./scripts/flash_pico.sh 2 /dev/ttyACM1
# ... repeat for all Picos

# Windows
scripts\flash_pico.bat 1 COM3
scripts\flash_pico.bat 2 COM4
# ... repeat for all Picos
```

1. Install Thonny: <https://thonny.org/>
2. Connect Pico via USB
3. Select "MicroPython (Raspberry Pi Pico)" interpreter
4. Open `pico_firmware/boot.py` → Save to Pico as `boot.py`
5. Open `pico_firmware/main.py` → Save to Pico as `main.py`
6. Restart Pico

#### 3. Verify Pico Installation

Connect to serial console:

```bash
# Linux/Mac
python -m serial.tools.miniterm /dev/ttyACM0 115200

# Windows
python -m serial.tools.miniterm COM3 115200
```

You should see:

```text
========================================
Raspberry Pi Pico Bitcoin Miner
Firmware Version: 1.0.0
CPU Frequency: 125.0 MHz
========================================
Pico Bitcoin Miner starting...
```

## Configuration

### Mining Pool Setup

Edit `config/.env` or `config/mining_config.json`:

```json
{
  "pool_url": "stratum+tcp://pool.example.com:3333",
  "username": "YOUR_BITCOIN_WALLET_ADDRESS.worker1",
  "password": "x",
  "mining_mode": "production"
}
```

**Popular Mining Pools:**

- Slush Pool: <https://slushpool.com/>
- F2Pool: <https://www.f2pool.com/>
- Antpool: <https://www.antpool.com/>

**Note:** Most pools have minimum payout thresholds. With low hashrate,
consider joining a pool that supports low-power miners or use testnet.

## Test Mode

For testing without connecting to a real pool:

```json
{
  "mining_mode": "test"
}
```

This generates simulated work locally.

## Running the Miner

### Start Mining

**Raspberry Pi 4:**

```bash
cd pi-bitcoin-miner
./scripts/start_mining.sh
```

**Windows (for development):**

```cmd
cd pi-bitcoin-miner
scripts\start_mining.bat
```

### Monitor Output

You should see:

```text
Bitcoin Miner Controller
======================================================================
  Bitcoin Miner Dashboard - Uptime: 0:01:30
======================================================================

Worker Status:
  ID    Port            Status       Hashrate        Shares   Errors
----------------------------------------------------------------------
  0     /dev/ttyACM0    Connected    75.23 H/s       0        0
  1     /dev/ttyACM1    Connected    73.45 H/s       0        0
  2     /dev/ttyACM2    Connected    74.89 H/s       0        0
  3     /dev/ttyACM3    Connected    76.12 H/s       0        0

Overall Statistics:
  Total Hashrate:    299.69 H/s
  Shares Submitted:  0
  Shares Accepted:   0
  Shares Rejected:   0
  Acceptance Rate:   0.0%
======================================================================
```

## Troubleshooting

### Picos Not Detected

1. **Check USB connections**: Try different cables/ports
1. **Check permissions** (Linux):

   ```bash
   sudo usermod -a -G dialout $USER
   # Logout and login again
   ```

1. **Verify MicroPython**: Connect to serial and check for Python prompt
1. **Check USB hub power**: Ensure hub provides sufficient power

### Low Hashrate

- Normal: 50-100 H/s per Pico
- Enable overclocking in `pico_firmware/boot.py`:

  ```python
  machine.freq(200000000)  # 200 MHz
  ```

### Connection Errors

1. Check serial baudrate (115200)
2. Verify firmware is uploaded correctly
3. Check USB hub compatibility
4. Try connecting Picos one at a time

### Mining Pool Errors

1. Verify wallet address is correct
2. Check pool URL and port
3. Ensure internet connection is working
4. Try test mode first to verify local operation

## Performance Optimization

### Pico Overclocking

Edit `pico_firmware/boot.py`:

```python
# Conservative: 200 MHz
machine.freq(200000000)

# Aggressive: 250 MHz (may be unstable)
machine.freq(250000000)
```

### Reduce USB Communication Overhead

In `pico_firmware/main.py`, reduce progress update frequency:

```python
# Send progress every 50000 hashes instead of 10000
if self.hashes_computed % 50000 == 0:
```

## Next Steps

- Monitor for 24 hours to ensure stability
- Check pool dashboard for share statistics
- Consider joining Bitcoin testnet for learning
- Explore assembly-optimized SHA-256 implementations

## Safety Notes

⚠️ **Important Reminders:**

- This will NOT mine Bitcoin profitably
- Electricity costs exceed any earnings
- This is educational/experimental only
- Overclocking may reduce hardware lifespan
- Monitor temperatures if overclocking
