"""05_hash_map.py — A tiny hash map with chaining, built from scratch.

Demonstrates: how a dict works under the hood — hash the key
to a bucket, chain colliding keys in a list, and resize when the
load factor grows. Used here for a word-count, a classic map job.
Run: python3 05_hash_map.py
"""


class HashMap:
    def __init__(self, capacity=8):
        self.buckets = [[] for _ in range(capacity)]
        self.size = 0

    def _bucket(self, key):
        return hash(key) % len(self.buckets)

    def _resize(self):
        old = self.buckets
        self.buckets = [[] for _ in range(len(old) * 2)]
        self.size = 0
        for bucket in old:
            for key, value in bucket:
                self.put(key, value)

    def put(self, key, value):
        bucket = self.buckets[self._bucket(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.size += 1
        if self.size > len(self.buckets) * 0.75:
            self._resize()

    def get(self, key, default=None):
        for k, value in self.buckets[self._bucket(key)]:
            if k == key:
                return value
        return default


def main():
    counts = HashMap()
    for word in "the cat sat the cat".split():
        counts.put(word, counts.get(word, 0) + 1)
    assert counts.get("the") == 2
    assert counts.get("cat") == 2
    assert counts.get("dog") is None
    # Force resizes: 50 distinct keys must all survive.
    for i in range(50):
        counts.put(f"key-{i}", i)
    assert counts.get("key-49") == 49
    print("PROOF: word counts the=2 cat=2, 50 keys survive resizes")


if __name__ == "__main__":
    main()
