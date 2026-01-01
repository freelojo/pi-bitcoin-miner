"""
Optimized SHA-256 implementation for Raspberry Pi Pico
This module provides a faster SHA-256 implementation than hashlib
for MicroPython on RP2040.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import time as time_module
    # MicroPython compatibility stubs for type checking
    if not hasattr(time_module, 'ticks_ms'):
        def ticks_ms() -> int: ...  # noqa: E704
        def ticks_diff(a: int, b: int) -> int: ...  # noqa: E704
        time_module.ticks_ms = ticks_ms  # type: ignore
        time_module.ticks_diff = ticks_diff  # type: ignore

# SHA-256 constants
K = (
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
)

# Initial hash values (first 32 bits of fractional parts of square roots)
H0 = (
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
)


def rotr(n, b):
    """Rotate right"""
    return ((n >> b) | (n << (32 - b))) & 0xffffffff


def shr(n, b):
    """Shift right"""
    return n >> b


def ch(x, y, z):
    """Choose function"""
    return (x & y) ^ (~x & z)


def maj(x, y, z):
    """Majority function"""
    return (x & y) ^ (x & z) ^ (y & z)


def sum0(x):
    """Sigma 0"""
    return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)


def sum1(x):
    """Sigma 1"""
    return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)


def sigma0(x):
    """Lowercase sigma 0"""
    return rotr(x, 7) ^ rotr(x, 18) ^ shr(x, 3)


def sigma1(x):
    """Lowercase sigma 1"""
    return rotr(x, 17) ^ rotr(x, 19) ^ shr(x, 10)


def sha256_block(block, h):
    """
    Process a single 512-bit (64-byte) block
    block: bytes object of exactly 64 bytes
    h: tuple of 8 uint32 hash values
    Returns: new h tuple
    """
    # Message schedule
    w = [0] * 64
    
    # First 16 words are the block bytes
    for i in range(16):
        w[i] = int.from_bytes(block[i*4:(i+1)*4], 'big')
    
    # Extend the first 16 words into remaining 48 words
    for i in range(16, 64):
        s0 = sigma0(w[i-15])
        s1 = sigma1(w[i-2])
        w[i] = (w[i-16] + s0 + w[i-7] + s1) & 0xffffffff
    
    # Initialize working variables
    a, b, c, d, e, f, g, h_val = h
    
    # Compression function main loop
    for i in range(64):
        S1 = sum1(e)
        ch_val = ch(e, f, g)
        temp1 = (h_val + S1 + ch_val + K[i] + w[i]) & 0xffffffff
        S0 = sum0(a)
        maj_val = maj(a, b, c)
        temp2 = (S0 + maj_val) & 0xffffffff
        
        h_val = g
        g = f
        f = e
        e = (d + temp1) & 0xffffffff
        d = c
        c = b
        b = a
        a = (temp1 + temp2) & 0xffffffff
    
    # Add compressed chunk to current hash value
    return tuple((h[i] + v) & 0xffffffff for i, v in 
                 enumerate([a, b, c, d, e, f, g, h_val]))


def sha256(data):
    """
    Compute SHA-256 hash of data
    data: bytes object
    Returns: bytes object (32 bytes)
    """
    # Pre-processing: padding
    msg_len = len(data)
    data += b'\x80'  # Append bit '1' to message
    
    # Pad with zeros until length is 448 mod 512 (56 mod 64)
    while len(data) % 64 != 56:
        data += b'\x00'
    
    # Append length in bits as 64-bit big-endian integer
    data += (msg_len * 8).to_bytes(8, 'big')
    
    # Process message in 512-bit (64-byte) chunks
    h = H0
    for i in range(0, len(data), 64):
        block = data[i:i+64]
        h = sha256_block(block, h)
    
    # Produce final hash value (big-endian)
    return b''.join(x.to_bytes(4, 'big') for x in h)


def double_sha256(data):
    """
    Compute double SHA-256 (Bitcoin block hash)
    This is what Bitcoin uses for block hashing
    """
    return sha256(sha256(data))


class SHA256:
    """
    SHA-256 hasher class compatible with hashlib interface
    Usage:
        h = SHA256()
        h.update(data)
        digest = h.digest()
    """
    
    def __init__(self, data=None):
        """Initialize with optional data"""
        self.h = H0
        self.buffer = b''
        self.msg_len = 0
        if data:
            self.update(data)
    
    def update(self, data):
        """Update hash with new data"""
        self.msg_len += len(data)
        self.buffer += data
        
        # Process complete blocks
        while len(self.buffer) >= 64:
            block = self.buffer[:64]
            self.buffer = self.buffer[64:]
            self.h = sha256_block(block, self.h)
    
    def digest(self):
        """Return the digest of the data"""
        # Create a copy of current state for final processing
        final_buffer = self.buffer + b'\x80'
        
        # Pad to 56 bytes (448 bits)
        while len(final_buffer) % 64 != 56:
            final_buffer += b'\x00'
        
        # Append length
        final_buffer += (self.msg_len * 8).to_bytes(8, 'big')
        
        # Process final blocks
        h = self.h
        for i in range(0, len(final_buffer), 64):
            block = final_buffer[i:i+64]
            h = sha256_block(block, h)
        
        return b''.join(x.to_bytes(4, 'big') for x in h)
    
    def hexdigest(self):
        """Return hex string of digest"""
        return self.digest().hex()


# Performance comparison function
def benchmark(iterations=1000):
    """
    Benchmark SHA-256 performance
    Returns: hashes per second
    """
    import time
    test_data = b'test data for benchmarking SHA-256 performance'
    
    start = time.ticks_ms() if hasattr(time, 'ticks_ms') else time.time() * 1000  # type: ignore
    
    for _ in range(iterations):
        sha256(test_data)
    
    if hasattr(time, 'ticks_ms'):
        elapsed = time.ticks_diff(time.ticks_ms(), start) / 1000.0  # type: ignore
    else:
        elapsed = (time.time() * 1000 - start) / 1000.0
    
    return iterations / elapsed if elapsed > 0 else 0


# Example usage
if __name__ == '__main__':
    # Test basic functionality
    test_data = b'hello world'
    result = sha256(test_data)
    print("SHA-256 hash:", result.hex())
    
    # Test double SHA-256 (Bitcoin style)
    block_header = b'0' * 80
    bitcoin_hash = double_sha256(block_header)
    print("Double SHA-256:", bitcoin_hash.hex())
    
    # Benchmark
    print("Running benchmark...")
    hps = benchmark(100)
    print("Performance: {:.2f} hashes/second".format(hps))
