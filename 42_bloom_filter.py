"""42_bloom_filter.py — A Bloom filter: fast "definitely not here" checks.

Demonstrates: a space-efficient membership test with no false
negatives — if it says "absent", the item is certainly absent.
False positives are possible, so a "present" answer must be
confirmed against the real store. Sizing is the whole game: a
tiny filter saturates and says yes to everything.
Run: python3 42_bloom_filter.py
"""

import hashlib


class BloomFilter:
    def __init__(self, size_bits, hashes=3):
        self.size = size_bits
        self.hashes = hashes
        self.bits = bytearray((size_bits + 7) // 8)

    def _positions(self, item):
        for seed in range(self.hashes):
            digest = hashlib.sha256(f"{seed}:{item}".encode()).digest()
            yield int.from_bytes(digest[:4], "big") % self.size

    def add(self, item):
        for pos in self._positions(item):
            self.bits[pos // 8] |= 1 << (pos % 8)

    def __contains__(self, item):
        return all(self.bits[pos // 8] >> (pos % 8) & 1
                   for pos in self._positions(item))


def main():
    big = BloomFilter(size_bits=1000)
    for item in (f"user-{i}" for i in range(100)):
        big.add(item)
    assert all(f"user-{i}" in big for i in range(100))  # no false negatives
    false_positives = sum(1 for i in range(1000, 2000)
                          if f"user-{i}" in big)
    small = BloomFilter(size_bits=100)
    for item in (f"user-{i}" for i in range(100)):
        small.add(item)
    small_fps = sum(1 for i in range(1000, 2000) if f"user-{i}" in small)
    assert small_fps > false_positives  # smaller filter, more false yeses
    print(f"PROOF: 1000-bit filter: 0 missed, {false_positives}/1000 false positives")
    print(f"PROOF: 100-bit filter: {small_fps}/1000 false positives (sizing matters)")


if __name__ == "__main__":
    main()
