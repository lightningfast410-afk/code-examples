"""12_rate_limiter.py — Token bucket rate limiting with a fake clock.

Demonstrates: a token bucket (capacity 5, refill 1 per 12s) and
why it beats a fixed window: a fixed window allows a burst at
the boundary (5 at t=59 plus 5 at t=61), while the bucket caps
any short burst at its capacity. A fake clock makes the proof
deterministic — no real sleeping required.
Run: python3 12_rate_limiter.py
"""


class TokenBucket:
    def __init__(self, capacity, refill_per_second):
        self.capacity = capacity
        self.refill = refill_per_second
        self.tokens = capacity
        self.last = 0.0

    def allow(self, now):
        self.tokens = min(self.capacity,
                          self.tokens + (now - self.last) * self.refill)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False


class FixedWindow:
    def __init__(self, limit, window):
        self.limit = limit
        self.window = window
        self.counts = {}

    def allow(self, now):
        slot = int(now // self.window)
        count = self.counts.get(slot, 0)
        if count >= self.limit:
            return False
        self.counts[slot] = count + 1
        return True


def main():
    bucket = TokenBucket(capacity=5, refill_per_second=1 / 12)
    first_burst = [bucket.allow(0) for _ in range(6)]
    assert first_burst == [True] * 5 + [False]
    assert bucket.allow(12) is True  # one token refilled after 12s

    window = FixedWindow(limit=5, window=60)
    burst = [window.allow(59) for _ in range(5)] + [window.allow(61) for _ in range(5)]
    assert burst == [True] * 10  # boundary burst: 10 in 2 seconds
    print("PROOF: bucket allows 5 then denies; fixed window allows 10 in 2s")
    print("PROOF: bucket refills 1 token by t=12")


if __name__ == "__main__":
    main()
