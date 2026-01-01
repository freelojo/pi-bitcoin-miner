# Raspberry Pi Pico Bitcoin Miner Firmware
# This firmware runs on each Pico worker board

from typing import TYPE_CHECKING

try:
    import machine  # type: ignore
except ImportError:
    machine = None  # type: ignore

import time
import sys
import json
import struct
import hashlib

# Try to use optimized SHA-256, fallback to hashlib
if not TYPE_CHECKING:
    try:
        from sha256_optimized import double_sha256 as sha256_double  # type: ignore
        USE_OPTIMIZED = True
        print("Using optimized SHA-256")
    except ImportError:
        def sha256_double(data):
            """Fallback double SHA-256 using hashlib"""
            h1 = hashlib.sha256(data).digest()
            return hashlib.sha256(h1).digest()
        USE_OPTIMIZED = False
        print("Using hashlib SHA-256")
else:
    # Type checking fallback
    def sha256_double(data: bytes) -> bytes:
        """Fallback double SHA-256 using hashlib"""
        h1 = hashlib.sha256(data).digest()
        return hashlib.sha256(h1).digest()
    USE_OPTIMIZED = False

# MicroPython time functions compatibility
if hasattr(time, 'ticks_ms'):
    ticks_ms = time.ticks_ms  # type: ignore
    ticks_diff = time.ticks_diff  # type: ignore
else:
    # Fallback for non-MicroPython environments
    def ticks_ms():  # type: ignore
        """Fallback millisecond counter"""
        return int(time.time() * 1000)
    
    def ticks_diff(end, start):  # type: ignore
        """Fallback tick difference"""
        return end - start

# UART for USB communication with Pi 4
if machine is not None:
    uart = machine.UART(0, baudrate=115200)
    # LED for status indication
    led = machine.Pin(25, machine.Pin.OUT)
else:
    # Mock objects for non-Pico environments
    uart = None  # type: ignore
    led = None  # type: ignore

class BitcoinMiner:
    """Bitcoin mining worker for Raspberry Pi Pico"""
    
    def __init__(self):
        self.worker_id = None
        self.is_mining = False
        self.current_work = None
        self.hashes_computed = 0
        self.start_time = 0
        
    def blink_led(self, times=1):
        """Blink LED for status indication"""
        if led is None:
            return
        for _ in range(times):
            led.value(1)
            time.sleep(0.1)
            led.value(0)
            time.sleep(0.1)
    
    def send_message(self, message):
        """Send JSON message to controller"""
        if uart is None:
            print("Mock send: {}".format(message))
            return
        try:
            msg = json.dumps(message) + '\n'
            uart.write(msg.encode('utf-8'))
        except Exception as e:
            print("Send error: {}".format(e))
    
    def read_command(self):
        """Read command from controller (non-blocking)"""
        if uart is None:
            return None, None
        if uart.any():
            try:
                line = uart.readline()
                if line:
                    data = line.decode('utf-8').strip()
                    if ':' in data:
                        cmd, json_data = data.split(':', 1)
                        return cmd, json.loads(json_data)
            except Exception as e:
                print("Read error: {}".format(e))
        return None, None
    
    def double_sha256(self, data):
        """Compute double SHA-256 (Bitcoin block hash)"""
        return sha256_double(data)
    
    def mine_block(self, block_header, target, start_nonce, end_nonce):
        """Mine with given nonce range"""
        self.is_mining = True
        self.start_time = ticks_ms()
        
        # Convert hex block header to bytes
        header_bytes = bytes.fromhex(block_header)
        target_int = int(target, 16)
        
        # Mine through nonce range
        for nonce in range(start_nonce, end_nonce):
            if not self.is_mining:
                break
            
            # Build block header with current nonce
            # Block header is 80 bytes: version(4) + prev_hash(32) + merkle(32) 
            #                          + timestamp(4) + bits(4) + nonce(4)
            header_with_nonce = header_bytes[:76] + struct.pack('<I', nonce)
            
            # Compute double SHA-256
            hash_result = self.double_sha256(header_with_nonce)
            
            # Convert hash to integer (little-endian for Bitcoin)
            hash_int = int.from_bytes(hash_result[::-1], 'big')
            
            self.hashes_computed += 1
            
            # Check if hash meets target difficulty
            if hash_int < target_int:
                # Valid solution found!
                elapsed = ticks_diff(ticks_ms(), self.start_time)
                hashrate = self.hashes_computed / (elapsed / 1000.0) if elapsed > 0 else 0
                
                self.send_message({
                    'type': 'RESULT',
                    'valid': True,
                    'nonce': nonce,
                    'hash': hash_result.hex(),
                    'hashes': self.hashes_computed,
                    'hashrate': hashrate,
                    'worker_id': self.worker_id
                })
                
                self.blink_led(3)  # Blink 3 times for valid share
                return
            
            # Send periodic progress updates (every 10000 hashes)
            if self.hashes_computed % 10000 == 0:
                elapsed = ticks_diff(ticks_ms(), self.start_time)
                hashrate = self.hashes_computed / (elapsed / 1000.0) if elapsed > 0 else 0
                
                self.send_message({
                    'type': 'PROGRESS',
                    'hashes': self.hashes_computed,
                    'hashrate': hashrate,
                    'current_nonce': nonce,
                    'worker_id': self.worker_id
                })
        
        # Completed range without finding solution
        elapsed = ticks_diff(ticks_ms(), self.start_time)
        hashrate = self.hashes_computed / (elapsed / 1000.0) if elapsed > 0 else 0
        
        self.send_message({
            'type': 'RESULT',
            'valid': False,
            'hashes': self.hashes_computed,
            'hashrate': hashrate,
            'worker_id': self.worker_id
        })
        
        self.is_mining = False
    
    def handle_hello(self, data):
        """Handle HELLO handshake from controller"""
        self.worker_id = data.get('id', 0)
        self.send_message({'status': 'READY', 'worker_id': self.worker_id})
        self.blink_led(2)
        print("Worker {} initialized".format(self.worker_id))
    
    def handle_work(self, data):
        """Handle new work assignment"""
        self.current_work = data
        self.hashes_computed = 0
        
        print("Received work: nonce range {}-{}".format(
            data['start_nonce'], data['end_nonce']))
        
        # Start mining
        self.mine_block(
            data['block_header'],
            data['target'],
            data['start_nonce'],
            data['end_nonce']
        )
    
    def handle_stop(self, data):
        """Handle STOP command"""
        self.is_mining = False
        print("Mining stopped")
    
    def run(self):
        """Main worker loop"""
        print("Pico Bitcoin Miner starting...")
        self.blink_led(1)
        
        while True:
            # Check for commands from controller
            cmd, data = self.read_command()
            
            if cmd == 'HELLO':
                self.handle_hello(data)
            elif cmd == 'WORK':
                self.handle_work(data)
            elif cmd == 'STOP':
                self.handle_stop(data)
            
            time.sleep(0.01)  # Small delay


# Main entry point
if __name__ == '__main__':
    miner = BitcoinMiner()
    try:
        miner.run()
    except KeyboardInterrupt:
        print("Shutting down...")
    except Exception as e:
        print("Fatal error: {}".format(e))
        if hasattr(sys, 'print_exception'):
            sys.print_exception(e)  # type: ignore
        else:
            import traceback
            traceback.print_exc()
