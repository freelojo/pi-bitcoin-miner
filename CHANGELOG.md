# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.1.0] - 2025-12-27

### Added - Multi-Bank Support
- Multi-bank architecture for organizing workers into scalable groups
- Support for 1-5 banks with 4 workers each (4-20 workers total)
- Bank-level statistics and monitoring
- Bank-grouped dashboard display
- Automatic worker-to-bank assignment
- Configurable bank names
- Bank-specific work distribution
- Fault isolation per bank
- New `MULTI_BANK_SETUP.md` documentation guide
- Bank statistics API in WorkerManager
- `get_bank_id()`, `get_bank_name()`, `get_workers_by_bank()` methods
- Bank count tracking and display

### Changed
- Worker Manager now accepts `workers_per_bank` and `number_of_banks` parameters
- Dashboard displays workers grouped by bank when `group_by_bank=true`
- Worker stats now include `bank_id` and `bank_name` fields
- Configuration updated for multi-bank support
- Documentation updated with 3-bank setup as default
- Architecture diagrams updated to show bank organization
- Expected worker count now 12 (3 banks × 4 workers)

### Enhanced
- Dashboard now shows per-bank statistics (active workers, hashrate)
- Improved scalability with modular bank design
- Better fault isolation and troubleshooting
- Enhanced monitoring with bank-level metrics

## [1.0.0] - 2025-12-27

### Added
- Initial release of Raspberry Pi Bitcoin Miner
- Worker manager for USB communication with Pico devices
- Mining coordinator for work distribution
- Pool client with Stratum protocol support (test mode)
- Real-time dashboard with sci-fi themed interface
- Support for 4 Raspberry Pi Pico workers
- Test mode for development without hardware
- Automated setup scripts for Pi 4 and Windows
- Comprehensive documentation and setup guides
- Unit tests for core components
- Type hints and mypy configuration
- Example configuration files

### Features
- Distributed work distribution across multiple workers
- Automatic worker discovery and connection
- SHA-256 hashing implementation
- USB serial communication protocol
- Nonce range allocation per worker
- Share submission tracking
- Performance metrics and statistics
- Colored terminal output
- Logging to file and console

### Documentation
- README with project overview
- Setup guide (SETUP.md)
- Architecture documentation (ARCHITECTURE.md)
- Quick start guide (QUICKSTART.md)
- Contributing guidelines (CONTRIBUTING.md)
- Inline code documentation

## [Unreleased]

### Planned
- Web-based dashboard interface
- Support for additional mining pools
- Enhanced error recovery mechanisms
- Assembly-optimized SHA-256 for Pico
- Overclocking profiles
- Worker health monitoring
- Automatic reconnection logic
- Configuration validation
- Integration tests
- Performance benchmarks
