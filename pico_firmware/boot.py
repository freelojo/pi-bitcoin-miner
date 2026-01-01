# Boot configuration for Pico miners
# This runs before main.py

try:
    import machine  # type: ignore
except ImportError:
    machine = None  # type: ignore
import time

# Optional: Overclock the Pico for better performance
# WARNING: Overclocking may cause instability or reduce lifespan
# Default is 125 MHz, can go up to 250+ MHz
# Uncomment to enable:
# machine.freq(200000000)  # 200 MHz

# Print boot information
print("=" * 40)
print("Raspberry Pi Pico Bitcoin Miner")
print("Firmware Version: 1.0.0")
print(f"CPU Frequency: {machine.freq() / 1_000_000} MHz")
print(f"Free Memory: {machine.mem_free()} bytes")
print("=" * 40)

# Brief startup delay
time.sleep(0.5)
