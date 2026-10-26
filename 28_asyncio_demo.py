"""28_asyncio_demo.py — Concurrent I/O with asyncio, no threads needed.

Demonstrates: async/await for waiting on several slow things
at once. Three tasks that each sleep 0.2s finish in about
0.2s total when awaited together (not 0.6s), because waiting
does not block the event loop.
Run: python3 28_asyncio_demo.py
"""

import asyncio
import time


async def slow_task(name, delay):
    await asyncio.sleep(delay)
    return name


async def run_all():
    start = time.monotonic()
    results = await asyncio.gather(
        slow_task("a", 0.2), slow_task("b", 0.2), slow_task("c", 0.2))
    elapsed = time.monotonic() - start
    return results, elapsed


def main():
    results, elapsed = asyncio.run(run_all())
    assert results == ["a", "b", "c"]
    assert elapsed < 0.5  # concurrent: ~0.2s, not 0.6s sequential
    print(f"PROOF: results = {results} in {elapsed:.2f}s (not 0.6s)")


if __name__ == "__main__":
    main()
