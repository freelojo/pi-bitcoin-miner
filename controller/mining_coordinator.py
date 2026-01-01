"""
Mining Coordinator - Distributes work and coordinates mining operations
"""

import asyncio
import logging
from typing import List, Dict
import hashlib
import struct

logger = logging.getLogger(__name__)


class MiningCoordinator:
    """Coordinates mining work distribution and result collection"""
    
    def __init__(self):
        self.current_work = None
        self.nonce_ranges = []
        self.results = []
        self.total_hashes = 0
        self.start_time = None
        
    async def distribute_work(self, work: Dict, workers: List):
        """Distribute mining work across all workers"""
        if not workers:
            logger.warning("No workers available for work distribution")
            return
        
        self.current_work = work
        num_workers = len(workers)
        
        # Calculate nonce ranges for each worker
        # Bitcoin nonce is 32-bit (0 to 4,294,967,295)
        total_nonce_space = 2**32
        nonce_per_worker = total_nonce_space // num_workers
        
        self.nonce_ranges = []
        
        for idx, worker in enumerate(workers):
            start_nonce = idx * nonce_per_worker
            end_nonce = start_nonce + nonce_per_worker if idx < num_workers - 1 else total_nonce_space
            
            work_packet = {
                'block_header': work['block_header'],
                'target': work['target'],
                'start_nonce': start_nonce,
                'end_nonce': end_nonce,
                'timestamp': work.get('timestamp')
            }
            
            self.nonce_ranges.append({
                'worker_id': worker.worker_id,
                'start': start_nonce,
                'end': end_nonce
            })
            
            # Send work to worker
            success = await worker.send_work(work_packet)
            if success:
                logger.debug(f"Sent work to worker {worker.worker_id}: nonce range {start_nonce}-{end_nonce}")
            else:
                logger.warning(f"Failed to send work to worker {worker.worker_id}")
    
    async def collect_results(self, timeout: float = 5.0) -> List[Dict]:
        """Collect mining results from all workers"""
        self.results = []
        
        # This would collect results from workers
        # In practice, workers would send results asynchronously when found
        # This is a simplified polling approach
        
        return self.results
    
    def get_total_hashrate(self) -> float:
        """Calculate total hashrate across all workers (H/s)"""
        # This would calculate based on worker reports
        # For now, return estimated value
        return 0.0
    
    async def stop_all_workers(self):
        """Send stop command to all workers"""
        logger.info("Stopping all workers")
        # Implementation would send STOP command to each worker
    
    def verify_nonce(self, block_header: bytes, nonce: int, target: str) -> bool:
        """Verify if a nonce produces a valid hash"""
        try:
            # Reconstruct block header with nonce
            header_with_nonce = block_header[:76] + struct.pack('<I', nonce)
            
            # Double SHA-256 hash
            hash1 = hashlib.sha256(header_with_nonce).digest()
            hash2 = hashlib.sha256(hash1).digest()
            
            # Convert to integer for comparison
            hash_int = int.from_bytes(hash2[::-1], 'big')
            target_int = int(target, 16)
            
            return hash_int < target_int
            
        except Exception as e:
            logger.error(f"Error verifying nonce: {e}")
            return False
