"""
Worker Manager - Handles USB communication with Pico workers
"""

import asyncio
import logging
from typing import List, Dict, Optional, TYPE_CHECKING, Any
import struct

if TYPE_CHECKING:
    import serial
    import serial.tools.list_ports
else:
    try:
        import serial
        import serial.tools.list_ports
    except ImportError:
        serial = None  # type: ignore

logger = logging.getLogger(__name__)


class PicoWorker:
    """Represents a single Pico mining worker"""
    
    def __init__(self, port: str, worker_id: int):
        self.port = port
        self.worker_id = worker_id
        self.serial: Optional[Any] = None
        self.is_connected = False
        self.hashrate = 0
        self.shares_found = 0
        self.errors = 0
        
    async def connect(self, baudrate: int = 115200):
        """Establish serial connection to the Pico"""
        if serial is None:
            logger.error("pyserial not installed. Install with: pip install pyserial")
            return False
        
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=baudrate,
                timeout=1,
                write_timeout=1
            )
            
            # Wait for Pico to initialize
            await asyncio.sleep(2)
            
            # Send handshake
            await self.send_command('HELLO', {'id': self.worker_id})
            response = await self.read_response(timeout=3)
            
            if response and response.get('status') == 'READY':
                self.is_connected = True
                logger.info(f"Worker {self.worker_id} connected on {self.port}")
                return True
            else:
                logger.error(f"Worker {self.worker_id} handshake failed")
                return False
                
        except Exception as e:
            logger.error(f"Failed to connect to worker {self.worker_id}: {e}")
            return False
    
    async def send_command(self, command: str, data: Optional[Dict] = None) -> bool:
        """Send a command to the Pico worker"""
        if not self.is_connected:
            return False
        
        try:
            # Simple protocol: CMD:JSON_DATA\n
            import json
            message = f"{command}:{json.dumps(data or {})}\n"
            if self.serial:
                self.serial.write(message.encode('utf-8'))
            return True
        except Exception as e:
            logger.error(f"Failed to send command to worker {self.worker_id}: {e}")
            self.errors += 1
            return False
    
    async def read_response(self, timeout: float = 5.0) -> Optional[Dict]:
        """Read a response from the Pico worker"""
        if not self.is_connected:
            return None
        
        try:
            import json
            # Non-blocking read with timeout
            start_time = asyncio.get_event_loop().time()
            buffer = b""
            
            while True:
                if self.serial and self.serial.in_waiting:
                    buffer += self.serial.read(self.serial.in_waiting)
                    
                    if b'\n' in buffer:
                        line, buffer = buffer.split(b'\n', 1)
                        result = json.loads(line.decode('utf-8'))
                        return result if isinstance(result, dict) else None
                
                if asyncio.get_event_loop().time() - start_time > timeout:
                    return None
                
                await asyncio.sleep(0.01)
                
        except Exception as e:
            logger.error(f"Failed to read from worker {self.worker_id}: {e}")
            self.errors += 1
            return None
    
    async def send_work(self, work_data: Dict) -> bool:
        """Send mining work to the worker"""
        return await self.send_command('WORK', work_data)
    
    async def get_result(self, timeout: float = 5.0) -> Optional[Dict]:
        """Get mining result from the worker"""
        return await self.read_response(timeout)
    
    def disconnect(self):
        """Close the serial connection"""
        if self.serial:
            try:
                self.serial.close()
                self.is_connected = False
                logger.info(f"Worker {self.worker_id} disconnected")
            except Exception as e:
                logger.error(f"Error disconnecting worker {self.worker_id}: {e}")


class WorkerManager:
    """Manages all Pico workers organized into banks"""
    
    def __init__(self, workers_per_bank: int = 4, number_of_banks: int = 3):
        self.workers: List[PicoWorker] = []
        self.workers_per_bank = workers_per_bank
        self.number_of_banks = number_of_banks
        self.expected_total = workers_per_bank * number_of_banks
        
    async def discover_workers(self):
        """Auto-discover connected Pico boards via USB"""
        if serial is None:
            logger.error("pyserial not installed. Install with: pip install pyserial")
            return
        
        logger.info(f"Scanning for Pico devices (expecting {self.expected_total} workers in {self.number_of_banks} banks)...")
        
        # List all serial ports
        ports = serial.tools.list_ports.comports()
        pico_ports = []
        
        for port in ports:
            # Pico typically shows up as "USB Serial Device" or similar
            # You may need to adjust VID/PID for your specific setup
            if 'USB Serial' in port.description or '2E8A' in str(port.hwid):
                pico_ports.append(port.device)
                logger.info(f"Found potential Pico on {port.device}")
        
        # Connect to each discovered port
        for idx, port in enumerate(pico_ports):
            worker = PicoWorker(port, idx)
            if await worker.connect():
                self.workers.append(worker)
        
        logger.info(f"Successfully connected to {len(self.workers)} workers across {self.get_bank_count()} banks")
    
    def get_bank_id(self, worker_id: int) -> int:
        """Get bank ID for a given worker ID"""
        return worker_id // self.workers_per_bank
    
    def get_bank_name(self, bank_id: int) -> str:
        """Get bank name for display"""
        bank_names = ["Bank-A", "Bank-B", "Bank-C", "Bank-D", "Bank-E"]
        if bank_id < len(bank_names):
            return bank_names[bank_id]
        return f"Bank-{bank_id}"
    
    def get_workers_by_bank(self, bank_id: int) -> List[PicoWorker]:
        """Get all workers in a specific bank"""
        return [w for w in self.workers if self.get_bank_id(w.worker_id) == bank_id]
    
    def get_bank_count(self) -> int:
        """Get number of banks with connected workers"""
        if not self.workers:
            return 0
        max_worker_id = max(w.worker_id for w in self.workers)
        return (max_worker_id // self.workers_per_bank) + 1
    
    def get_active_workers(self) -> List[PicoWorker]:
        """Get list of currently active workers"""
        return [w for w in self.workers if w.is_connected]
    
    def get_worker_stats(self) -> List[Dict]:
        """Get statistics for all workers"""
        return [{
            'id': w.worker_id,
            'bank_id': self.get_bank_id(w.worker_id),
            'bank_name': self.get_bank_name(self.get_bank_id(w.worker_id)),
            'port': w.port,
            'connected': w.is_connected,
            'hashrate': w.hashrate,
            'shares': w.shares_found,
            'errors': w.errors
        } for w in self.workers]
    
    def get_bank_stats(self) -> List[Dict]:
        """Get aggregated statistics by bank"""
        banks = []
        for bank_id in range(self.get_bank_count()):
            bank_workers = self.get_workers_by_bank(bank_id)
            active_workers = [w for w in bank_workers if w.is_connected]
            
            banks.append({
                'bank_id': bank_id,
                'bank_name': self.get_bank_name(bank_id),
                'total_workers': len(bank_workers),
                'active_workers': len(active_workers),
                'total_hashrate': sum(w.hashrate for w in active_workers),
                'total_shares': sum(w.shares_found for w in bank_workers),
                'total_errors': sum(w.errors for w in bank_workers)
            })
        return banks
    
    @property
    def worker_count(self) -> int:
        """Get total number of workers"""
        return len(self.workers)
    
    async def disconnect_all(self):
        """Disconnect all workers"""
        for worker in self.workers:
            worker.disconnect()
