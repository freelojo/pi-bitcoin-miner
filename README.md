# Raspberry Pi Bitcoin Miner

A distributed Bitcoin mining system using Raspberry Pi 4 as the controller
and multiple Raspberry Pi Pico boards as mining workers.

## ⚠️ Educational Project Warning

This project is for **educational purposes only**. The hashrate achieved
will be extremely low compared to modern ASIC miners, and the electricity
costs will far exceed any potential earnings. This is not a viable way to
mine Bitcoin profitably.

## Hardware Requirements

- 1x Raspberry Pi 4 Model B (Controller)
- 4x Raspberry Pi Pico (Mining Workers)
- 1x Powered USB Hub (to connect all Picos)
- MicroSD card for Pi 4 (16GB+ recommended)
- Power supply for Pi 4
- USB cables for Picos

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
        ┌──────┴──────┐ USB Hub
        │             │
   ┌────┴───┬────────┴───┬────────┴───┬────────┴───┐
   │ Pico 0 │  Pico 1    │  Pico 2    │  Pico 3    │
   │ Worker │  Worker    │  Worker    │  Worker    │
   └────────┴────────────┴────────────┴────────────┘
```

## Project Structure

- `controller/` - Python code for Raspberry Pi 4 controller
- `pico_firmware/` - MicroPython/C firmware for Pico workers
- `config/` - Configuration files
- `scripts/` - Setup and deployment scripts
- `tests/` - Unit and integration tests
- `docs/` - Additional documentation

## Quick Start

1. Set up the Raspberry Pi 4 controller
2. Flash Pico firmware to all worker boards
3. Configure mining pool settings
4. Run the controller
5. Monitor mining performance

Detailed instructions in [docs/SETUP.md](docs/SETUP.md)

## Features

- Distributed work distribution across multiple Picos
- Real-time monitoring dashboard
- SHA-256 hashing implementation
- USB serial communication
- Automatic worker reconnection
- Performance metrics and statistics

## License

MIT License - See LICENSE file for details
