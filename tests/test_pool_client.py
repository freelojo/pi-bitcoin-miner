"""
Tests for Pool Client
"""

import pytest
import asyncio
from controller.pool_client import PoolClient
import tempfile
import json
import os


@pytest.fixture
def temp_config():
    """Create temporary config file"""
    config = {
        'pool_url': 'stratum+tcp://test.pool.com:3333',
        'username': 'test_wallet.worker1',
        'password': 'x',
        'mining_mode': 'test'
    }
    
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.json',
        delete=False
    ) as f:
        json.dump(config, f)
        config_path = f.name
    
    yield config_path
    
    os.unlink(config_path)


def test_pool_client_init(temp_config):
    """Test PoolClient initialization"""
    client = PoolClient(temp_config)
    
    assert client.connected is False
    assert client.shares_submitted == 0
    assert client.shares_accepted == 0
    assert client.shares_rejected == 0


@pytest.mark.asyncio
async def test_connect_test_mode(temp_config):
    """Test connection in test mode"""
    client = PoolClient(temp_config)
    result = await client.connect()
    
    assert result is True
    assert client.connected is True


@pytest.mark.asyncio
async def test_get_work_test_mode(temp_config):
    """Test getting work in test mode"""
    client = PoolClient(temp_config)
    await client.connect()
    
    work = await client.get_work()
    
    assert work is not None
    assert 'block_header' in work
    assert 'target' in work
    assert 'timestamp' in work
    assert 'job_id' in work


@pytest.mark.asyncio
async def test_submit_work_test_mode(temp_config):
    """Test submitting work in test mode"""
    client = PoolClient(temp_config)
    await client.connect()
    
    result = {
        'nonce': 12345,
        'hash': 'abc123',
        'worker_id': 0
    }
    
    success = await client.submit_work(result)
    
    assert success is True
    assert client.shares_submitted == 1
    assert client.shares_accepted == 1


def test_share_stats(temp_config):
    """Test share statistics"""
    client = PoolClient(temp_config)
    
    client.shares_submitted = 10
    client.shares_accepted = 9
    client.shares_rejected = 1
    
    stats = client.get_share_stats()
    
    assert stats['submitted'] == 10
    assert stats['accepted'] == 9
    assert stats['rejected'] == 1
    assert stats['acceptance_rate'] == 90.0
