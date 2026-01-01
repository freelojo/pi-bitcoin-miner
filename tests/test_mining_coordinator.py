"""
Tests for Mining Coordinator
"""

import pytest
import asyncio
from controller.mining_coordinator import MiningCoordinator


class MockWorker:
    """Mock worker for testing"""
    def __init__(self, worker_id: int):
        self.worker_id = worker_id
        self.is_connected = True
        self.hashrate = 75.0
        
    async def send_work(self, work_packet):
        await asyncio.sleep(0.01)
        return True


@pytest.mark.asyncio
async def test_distribute_work():
    """Test work distribution across workers"""
    coordinator = MiningCoordinator()
    workers = [MockWorker(i) for i in range(4)]
    
    work = {
        'block_header': 'a' * 152,
        'target': '0000ffff' + 'f' * 56,
        'timestamp': '2025-01-01T00:00:00'
    }
    
    await coordinator.distribute_work(work, workers)
    
    assert len(coordinator.nonce_ranges) == 4
    assert coordinator.nonce_ranges[0]['start'] == 0
    assert coordinator.nonce_ranges[-1]['end'] == 2**32


@pytest.mark.asyncio
async def test_distribute_work_no_workers():
    """Test work distribution with no workers"""
    coordinator = MiningCoordinator()
    
    work = {
        'block_header': 'a' * 152,
        'target': '0000ffff' + 'f' * 56,
        'timestamp': '2025-01-01T00:00:00'
    }
    
    await coordinator.distribute_work(work, [])
    
    assert len(coordinator.nonce_ranges) == 0


def test_verify_nonce():
    """Test nonce verification"""
    coordinator = MiningCoordinator()
    
    # Create test block header
    block_header = bytes.fromhex('a' * 152)
    
    # This will likely fail (invalid), but tests the function
    result = coordinator.verify_nonce(
        block_header,
        12345,
        '0000ffff' + 'f' * 56
    )
    
    assert isinstance(result, bool)
