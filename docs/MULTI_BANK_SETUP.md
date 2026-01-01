# Multi-Bank Configuration Guide

## Overview

The Raspberry Pi Bitcoin Miner supports organizing workers into multiple
banks for improved scalability and fault isolation. This guide explains
how to configure and optimize your multi-bank setup.

## Bank Architecture

### What is a Bank?

A bank is a group of 4 Raspberry Pi Pico workers connected to a single
USB hub. Banks provide:

- **Scalability**: Add capacity by adding banks
- **Fault Isolation**: Problems in one bank don't affect others
- **Organization**: Logical grouping for monitoring
- **Load Distribution**: Even work distribution across banks

### Supported Configurations

| Banks | Workers | USB Hubs | Expected Hashrate |
|-------|---------|----------|-------------------|
| 1     | 4       | 1        | 150-400 H/s       |
| 2     | 8       | 2        | 300-800 H/s       |
| 3     | 12      | 3        | 450-1200 H/s      |
| 4     | 16      | 4        | 600-1600 H/s      |
| 5     | 20      | 5        | 750-2000 H/s      |

## Configuration File

Edit `config/mining_config.json`:

```json
{
  "worker_settings": {
    "auto_discover": true,
    "expected_workers": 12,
    "workers_per_bank": 4,
    "number_of_banks": 3,
    "reconnect_timeout": 10,
    "communication_baudrate": 115200,
    "bank_names": ["Bank-A", "Bank-B", "Bank-C"]
  },
  
  "mining_settings": {
    "work_timeout": 30,
    "result_collection_timeout": 5.0,
    "difficulty_adjustment": "auto",
    "distribute_by_bank": true
  },
  
  "dashboard_settings": {
    "update_interval": 30,
    "enable_web_dashboard": false,
    "web_dashboard_port": 8080,
    "group_by_bank": true
  }
}
```

### Configuration Options

#### worker_settings

- **expected_workers**: Total number of Pico workers (banks × 4)
- **workers_per_bank**: Workers per bank (always 4)
- **number_of_banks**: Total banks in your setup (1-5)
- **bank_names**: Custom names for each bank (optional)
- **auto_discover**: Automatically find and connect workers

#### mining_settings

- **distribute_by_bank**: Distribute work evenly across banks
- **work_timeout**: Seconds before requesting new work
- **result_collection_timeout**: Seconds to wait for results

#### dashboard_settings

- **group_by_bank**: Display workers grouped by bank
- **update_interval**: Refresh rate in seconds

## Physical Setup

### Single Bank (4 Workers)

```text
Pi 4 → [USB Hub] → [Pico 0, 1, 2, 3]
```

Configuration:
```json
{
  "workers_per_bank": 4,
  "number_of_banks": 1,
  "expected_workers": 4
}
```

### Three Banks (12 Workers) - Recommended

```text
Pi 4 USB Port 1 → [Hub A] → [Pico 0,1,2,3] Bank-A
Pi 4 USB Port 2 → [Hub B] → [Pico 4,5,6,7] Bank-B
Pi 4 USB Port 3 → [Hub C] → [Pico 8,9,10,11] Bank-C
```

Configuration:
```json
{
  "workers_per_bank": 4,
  "number_of_banks": 3,
  "expected_workers": 12
}
```

### Five Banks (20 Workers) - Maximum

```text
Pi 4 USB Ports → 5 Hubs → 20 Picos (5 banks of 4)
```

Configuration:
```json
{
  "workers_per_bank": 4,
  "number_of_banks": 5,
  "expected_workers": 20
}
```

**Note**: Pi 4 has 4 USB ports. For 5 banks, use a powered hub for one bank.

## Dashboard Output

With `group_by_bank: true`, the dashboard shows each bank separately:

```text
┌─────────────────────────────────────────────────┐
│ Bank-A - 4/4 ACTIVE    HASHRATE: 310.45 H/s     │
├────┬──────────┬────────┬────────┬───────┬───────┤
│ ID │ PORT     │ STATUS │ RATE   │ SHARES│ ERRORS│
├────┼──────────┼────────┼────────┼───────┼───────┤
│ 00 │ /dev/tty │ ONLINE │ 78 H/s │   5   │   0   │
│ 01 │ /dev/tty │ ONLINE │ 76 H/s │   4   │   0   │
│ 02 │ /dev/tty │ ONLINE │ 79 H/s │   6   │   0   │
│ 03 │ /dev/tty │ ONLINE │ 77 H/s │   5   │   0   │
└────┴──────────┴────────┴────────┴───────┴───────┘

┌─────────────────────────────────────────────────┐
│ Bank-B - 3/4 ACTIVE    HASHRATE: 232.15 H/s     │
...
```

## Scaling Guide

### Adding a New Bank

1. **Physical Setup**:
   - Connect new USB hub to Pi 4
   - Connect 4 new Picos to the hub
   - Flash firmware to new Picos

2. **Update Configuration**:
   ```json
   {
     "number_of_banks": 4,  // Increase from 3
     "expected_workers": 16  // Add 4 workers
   }
   ```

3. **Restart Controller**:
   ```bash
   python controller/main.py
   ```

Workers are auto-discovered and assigned to banks automatically.

### Removing a Bank

1. Physically disconnect the USB hub
2. Update configuration to reduce `number_of_banks`
3. Restart controller

## Troubleshooting

### Workers Not Detected

**Problem**: `Found X workers, expected Y`

**Solutions**:
- Check USB hub connections
- Verify all Picos are powered
- Check firmware is flashed correctly
- Try connecting hubs one at a time

### Uneven Bank Distribution

**Problem**: Banks have different numbers of workers

**Cause**: Workers are assigned IDs in discovery order

**Solution**: Workers are auto-assigned to banks based on ID.
Physical organization doesn't affect performance, but you can:
- Reconnect Picos in desired order
- Restart controller for re-discovery
- Label Picos physically for easier tracking

### Bank Shows All Offline

**Problem**: All workers in one bank are offline

**Solutions**:
- Check USB hub power
- Test hub on another USB port
- Verify hub is recognized by Pi 4: `lsusb`
- Try a different hub

### Low Hashrate on One Bank

**Problem**: One bank performs worse than others

**Solutions**:
- Check for overheating (add cooling)
- Verify USB hub provides adequate power
- Test Picos individually
- Consider worker firmware issues

## Performance Optimization

### Optimal Configuration

For best performance:
```json
{
  "workers_per_bank": 4,
  "number_of_banks": 3,
  "expected_workers": 12,
  "distribute_by_bank": true
}
```

This provides:
- Good scalability
- Manageable complexity
- Adequate hashrate for learning
- All USB ports on Pi 4 used efficiently

### Bank Monitoring

Monitor bank-level statistics:
- Active workers per bank
- Total hashrate per bank
- Shares submitted per bank
- Error counts per bank

Use this data to identify underperforming banks.

## Advanced Configuration

### Custom Bank Names

```json
{
  "bank_names": [
    "Alpha-Mining",
    "Beta-Hash",
    "Gamma-Compute"
  ]
}
```

### Load Balancing

```json
{
  "mining_settings": {
    "distribute_by_bank": true,
    "prefer_active_banks": true
  }
}
```

### Bank-Specific Timeouts

For mixed setups (some banks on longer USB cables):

```json
{
  "worker_settings": {
    "bank_specific_timeouts": {
      "Bank-A": 5.0,
      "Bank-B": 5.0,
      "Bank-C": 7.0
    }
  }
}
```

## Best Practices

1. **Start Small**: Begin with 1-2 banks, then expand
2. **Label Everything**: Physical labels on hubs and Picos
3. **Use Quality Hubs**: Powered hubs with sufficient amperage
4. **Monitor Regularly**: Check dashboard for issues
5. **Balanced Load**: Keep workers per bank consistent
6. **Plan Cooling**: More workers = more heat
7. **Document Changes**: Note which Picos are in which banks

## Conclusion

Multi-bank architecture provides flexibility and scalability for your
educational mining setup. Start with the recommended 3-bank configuration
and adjust based on your learning goals and available hardware.
