#!/usr/bin/env python3
"""
Bitcoin Miner Controller for Raspberry Pi 4
Manages work distribution to Pico workers via USB
"""

import asyncio
import logging
from typing import List
from datetime import datetime
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from worker_manager import WorkerManager
from mining_coordinator import MiningCoordinator
from pool_client import PoolClient
from dashboard import Dashboard

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mining.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class BitcoinMinerController:
    """Main controller for the distributed Bitcoin mining system"""
    
    def __init__(self, config_path: str = '../config/mining_config.json'):
        """Initialize the mining controller"""
        logger.info("Initializing Bitcoin Miner Controller")
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize components with config
        workers_per_bank = self.config.get('worker_settings', {}).get('workers_per_bank', 4)
        number_of_banks = self.config.get('worker_settings', {}).get('number_of_banks', 3)
        
        self.worker_manager = WorkerManager(workers_per_bank, number_of_banks)
        self.mining_coordinator = MiningCoordinator()
        self.pool_client = PoolClient(config_path)
        self.dashboard = Dashboard()
        
        self.is_running = False
        self.start_time = None
    
    def _load_config(self, config_path: str):
        """Load mining configuration"""
        import json
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load config: {e}. Using defaults.")
            return {}
        
    async def initialize(self):
        """Initialize all components"""
        logger.info("Discovering and connecting to Pico workers...")
        await self.worker_manager.discover_workers()
        
        bank_count = self.worker_manager.get_bank_count()
        logger.info(f"Found {self.worker_manager.worker_count} workers across {bank_count} banks")
        
        logger.info("Connecting to mining pool...")
        await self.pool_client.connect()
        
        logger.info("Starting dashboard...")
        await self.dashboard.start()
        
    async def run(self):
        """Main mining loop"""
        self.is_running = True
        self.start_time = datetime.now()
        
        logger.info("Starting mining operations...")
        
        try:
            while self.is_running:
                # Get work from mining pool
                work = await self.pool_client.get_work()
                
                if work:
                    # Distribute work to Pico workers
                    await self.mining_coordinator.distribute_work(
                        work, 
                        self.worker_manager.get_active_workers()
                    )
                    
                    # Collect results from workers
                    results = await self.mining_coordinator.collect_results(timeout=5.0)
                    
                    # Submit any valid solutions
                    for result in results:
                        if result['valid']:
                            logger.info(f"Valid share found by worker {result['worker_id']}")
                            await self.pool_client.submit_work(result)
                    
                    # Update dashboard
                    await self.dashboard.update_stats(
                        workers=self.worker_manager.get_worker_stats(),
                        hashrate=self.mining_coordinator.get_total_hashrate(),
                        shares=self.pool_client.get_share_stats()
                    )
                
                await asyncio.sleep(0.1)  # Small delay to prevent CPU spinning
                
        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
        except Exception as e:
            logger.error(f"Error in main loop: {e}", exc_info=True)
        finally:
            await self.shutdown()
    
    async def shutdown(self):
        """Clean shutdown of all components"""
        logger.info("Shutting down mining controller...")
        self.is_running = False
        
        await self.mining_coordinator.stop_all_workers()
        await self.pool_client.disconnect()
        await self.dashboard.stop()
        await self.worker_manager.disconnect_all()
        
        logger.info("Shutdown complete")


async def main():
    """Entry point for the mining controller"""
    controller = BitcoinMinerController()
    
    try:
        await controller.initialize()
        await controller.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
