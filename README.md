# Raspberry Pi Bitcoin Miner

A distributed Bitcoin mining system using Raspberry Pi 4 as the controller
and multiple Raspberry Pi Pico boards as mining workers, organized into
scalable banks for enhanced performance.

## ⚠️ Educational Project Warning

This project is for **educational purposes only**. The hashrate achieved
will be extremely low compared to modern ASIC miners, and the electricity
costs will far exceed any potential earnings. This is not a viable way to
mine Bitcoin profitably.

## Hardware Requirements

### Standard 3-Bank Setup (12 Workers)

- 1x Raspberry Pi 4 Model B (Controller)
- 12x Raspberry Pi Pico (Mining Workers - 3 banks of 4)
- 3x Powered USB Hubs (one per bank, to connect 4 Picos each)
- MicroSD card for Pi 4 (16GB+ recommended)
- Power supply for Pi 4
- USB cables for Picos

### Scalable Configuration

The system supports 1-5 banks with 4 workers each:
- 1 Bank: 4 Pico workers (~150-400 H/s)
- 2 Banks: 8 Pico workers (~300-800 H/s)
- 3 Banks: 12 Pico workers (~450-1200 H/s)
- 4 Banks: 16 Pico workers (~600-1600 H/s)
- 5 Banks: 20 Pico workers (~750-2000 H/s)

## Architecture

```text
┌─────────────────────────────────┐
│    Raspberry Pi 4 (Controller)  │
│  - Work distribution            │
│  - Mining pool communication    │
│  - Result aggregation           │
│  - Monitoring dashboard         │
└──────────────┬──────────────────┘
               │
        ┌──────┴───────────┬───────────────┐
        │                  │               │
   [USB Hub A]        [USB Hub B]    [USB Hub C]
        │                  │               │
  ┌─────┴─────┐      ┌─────┴─────┐   ┌─────┴─────┐
  │ BANK A    │      │ BANK B    │   │ BANK C    │
  │ Pico 0-3  │      │ Pico 4-7  │   │ Pico 8-11 │
  └───────────┘      └───────────┘   └───────────┘
```

### Bank Organization

Each bank consists of 4 Raspberry Pi Pico workers connected to a dedicated
USB hub. This organization provides:

- **Scalability**: Add or remove banks as needed
- **Fault Isolation**: Issues in one bank don't affect others
- **Load Balancing**: Work distributed evenly across banks
- **Easy Maintenance**: Service individual banks without full shutdown

## Project Structure

- `controller/` - Python code for Raspberry Pi 4 controller
- `pico_firmware/` - MicroPython/C firmware for Pico workers
- `config/` - Configuration files
- `scripts/` - Setup and deployment scripts
- `tests/` - Unit and integration tests
- `docs/` - Additional documentation

## Quick Start

1. Set up the Raspberry Pi 4 controller
2. Connect 3 USB hubs to the Pi 4
3. Flash Pico firmware to all 12 worker boards
4. Connect 4 Picos to each USB hub (3 banks total)
5. Configure mining pool settings
6. Run the controller
7. Monitor mining performance by bank

Detailed instructions in [docs/SETUP.md](docs/SETUP.md)

## Features

- Distributed work distribution across multiple banks
- Scalable architecture (1-5 banks supported)
- Bank-level monitoring and statistics
- Real-time dashboard with bank grouping
- SHA-256 hashing implementation
- USB serial communication
- Automatic worker discovery and bank assignment
- Fault isolation per bank
- Performance metrics and statistics by bank

## License

MIT License - See LICENSE file for details
