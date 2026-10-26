"""39_lru_cache.py — An LRU cache: bounded memory, recent items win.

Demonstrates: OrderedDict as the backing store — get() moves
an item to the "recent" end, put() evicts from the "old" end
when capacity is exceeded. The demo proves eviction order and
that a cache hit refreshes recency.
Run: python3 39_lru_cache.py
"""

from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self.capacity = capacity
        self.store = OrderedDict()

    def get(self, key, default=None):
        if key not in self.store:
            return default
        self.store.move_to_end(key)  # a hit makes it most recent
        return self.store[key]

    def put(self, key, value):
        if key in self.store:
            self.store.move_to_end(key)
        self.store[key] = value
        if len(self.store) > self.capacity:
            self.store.popitem(last=False)  # evict least recently used

    def keys(self):
        return list(self.store.keys())


def main():
    cache = LRUCache(capacity=3)
    for key in ("a", "b", "c"):
        cache.put(key, key.upper())
    cache.get("a")  # "a" is now most recent; "b" is oldest
    cache.put("d", "D")  # capacity exceeded: "b" is evicted
    assert cache.keys() == ["c", "a", "d"]
    assert cache.get("b") is None
    assert cache.get("a") == "A"
    print(f"PROOF: keys after eviction = {cache.keys()}, evicted 'b' gone")


if __name__ == "__main__":
    main()
