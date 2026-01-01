# Architecture Overview

## System Design

The Bitcoin mining system consists of two main components:

### 1. Controller (Raspberry Pi 4)

- **Role**: Coordinator and pool interface
- **Language**: Python 3
- **Responsibilities**:
  - Communicate with mining pool (Stratum protocol)
  - Discover and manage Pico workers via USB
  - Distribute work across workers
  - Collect and verify results
  - Monitor performance and statistics
  - Display real-time dashboard

### 2. Workers (Raspberry Pi Pico)

- **Role**: Hash computation engines
- **Language**: MicroPython
- **Responsibilities**:
  - Receive work assignments via USB serial
  - Compute SHA-256 hashes in assigned nonce range
  - Report progress periodically
  - Submit valid solutions immediately

## Communication Protocol

### USB Serial Communication (115200 baud)

**Message Format:**

```text
COMMAND:{"key": "value"}\n
```

**Commands from Controller to Pico:**

1. **HELLO** - Initial handshake

```json
HELLO:{"id": 0}
```

1. **WORK** - Mining assignment

```json
WORK:{
  "block_header": "hex_string",
  "target": "difficulty_target",
  "start_nonce": 0,
  "end_nonce": 1073741824
}
```

1. **STOP** - Stop mining

```json
STOP:{}
```

**Responses from Pico to Controller:**

1. **READY** - Handshake response

```json
{"status": "READY", "worker_id": 0}
```

1. **PROGRESS** - Periodic update

```json
{
  "type": "PROGRESS",
  "hashes": 50000,
  "hashrate": 75.5,
  "current_nonce": 50000,
  "worker_id": 0
}
```

1. **RESULT** - Work completion

```json
{
  "type": "RESULT",
  "valid": true,
  "nonce": 123456,
  "hash": "hex_hash",
  "hashes": 123456,
  "hashrate": 75.5,
  "worker_id": 0
}
```

## Data Flow

```text
Mining Pool
     ↓
  [getwork]
     ↓
Controller (Pi 4)
     ↓
[Work Distribution]
     ↓
  ┌──┴──┬──────┬──────┐
  ↓     ↓      ↓      ↓
Pico0 Pico1 Pico2 Pico3
  ↓     ↓      ↓      ↓
[SHA-256 Hashing]
  ↓     ↓      ↓      ↓
[Results/Progress]
     ↓
Controller (Pi 4)
     ↓
[Verification]
     ↓
  [submit]
     ↓
Mining Pool
```

## Work Distribution Strategy

**Nonce Space Partitioning:**

- Bitcoin nonce range: 0 to 2^32 (4,294,967,296)
- With 4 workers: Each gets ~1.07 billion nonces
- Worker 0: 0 to 1,073,741,823
- Worker 1: 1,073,741,824 to 2,147,483,647
- Worker 2: 2,147,483,648 to 3,221,225,471
- Worker 3: 3,221,225,472 to 4,294,967,295

**Dynamic Reallocation:**

- If a worker disconnects, redistribute its range
- Support for hot-plugging workers
- Load balancing based on hashrate

## Bitcoin Mining Algorithm

### Block Header Structure (80 bytes)

```text
[Version: 4 bytes]
[Previous Block Hash: 32 bytes]
[Merkle Root: 32 bytes]
[Timestamp: 4 bytes]
[Difficulty Bits: 4 bytes]
[Nonce: 4 bytes]
```

### Mining Process

1. Receive block header template from pool
2. Increment nonce (0 to 2^32)
3. Compute double SHA-256: `SHA256(SHA256(header))`
4. Compare result with difficulty target
5. If hash < target: Valid share found
6. Otherwise: Continue to next nonce

### Difficulty Target

- Represented as 256-bit number
- Valid hash must be less than target
- Lower target = higher difficulty
- Bitcoin adjusts every 2016 blocks (~2 weeks)

## Performance Considerations

### Expected Hashrates

- **Single Pico**: 50-100 H/s (stock)
- **Overclocked Pico (200 MHz)**: 80-120 H/s
- **4 Picos**: 200-400 H/s total
- **For comparison**: Modern ASIC miner: 100+ TH/s (terahashes)

### Bottlenecks

1. **CPU Speed**: ARM Cortex-M0+ at 133 MHz
2. **SHA-256 Computation**: No hardware acceleration
3. **USB Communication**: Minimal impact with batching

### Optimization Opportunities

1. **Assembly SHA-256**: 2-3x speedup possible
2. **PIO State Machines**: Parallel operations
3. **Reduced Communication**: Batch updates
4. **Overclocking**: 1.5-2x speedup (with stability risks)

## Fault Tolerance

### Worker Failures

- Automatic reconnection attempts
- Work redistribution to remaining workers
- Error tracking and reporting

### Network Issues

- Connection retry logic
- Work queue buffering
- Graceful degradation

### Power Management

- Clean shutdown on SIGINT/SIGTERM
- State preservation
- Resume capability

## Security Considerations

### Pool Authentication

- Username typically: wallet_address.worker_name
- Password: Usually "x" or any value
- Stratum protocol uses JSON-RPC over TCP

### Data Validation

- Verify block header format
- Validate nonce ranges
- Check hash results before submission
- Prevent duplicate work

## Monitoring & Logging

### Metrics Tracked

- Per-worker hashrate
- Total system hashrate
- Share submission rate
- Share acceptance rate
- Worker uptime
- Error counts

### Dashboard Display

- Real-time statistics every 30 seconds
- Worker status table
- Overall performance metrics
- Share statistics

### Logging

- Console output (INFO level)
- File logging (mining.log)
- Error tracking with stack traces
- Performance metrics history
