"""
Tests for Worker Manager
"""

import pytest
from controller.worker_manager import PicoWorker, WorkerManager


def test_pico_worker_init():
    """Test PicoWorker initialization"""
    worker = PicoWorker('/dev/ttyACM0', 0)
    
    assert worker.port == '/dev/ttyACM0'
    assert worker.worker_id == 0
    assert worker.is_connected is False
    assert worker.hashrate == 0
    assert worker.shares_found == 0
    assert worker.errors == 0


def test_worker_manager_init():
    """Test WorkerManager initialization"""
    manager = WorkerManager()
    
    assert isinstance(manager.workers, list)
    assert len(manager.workers) == 0
    assert manager.worker_count == 0


def test_worker_stats_empty():
    """Test getting stats with no workers"""
    manager = WorkerManager()
    stats = manager.get_worker_stats()
    
    assert isinstance(stats, list)
    assert len(stats) == 0


def test_worker_stats_with_workers():
    """Test getting stats with workers"""
    manager = WorkerManager()
    
    # Manually add workers for testing
    worker1 = PicoWorker('/dev/ttyACM0', 0)
    worker2 = PicoWorker('/dev/ttyACM1', 1)
    manager.workers = [worker1, worker2]
    
    stats = manager.get_worker_stats()
    
    assert len(stats) == 2
    assert stats[0]['id'] == 0
    assert stats[1]['id'] == 1
    assert stats[0]['connected'] is False
