"""26_thread_pool.py — Parallel work with a thread pool, results in order.

Demonstrates: concurrent.futures.ThreadPoolExecutor for I/O-style
work (here simulated with tiny sleeps), mapping inputs to
outputs while preserving order, and handling one failing task
without losing the rest.
Run: python3 26_thread_pool.py
"""

import time
from concurrent.futures import ThreadPoolExecutor


def fetch_page(number):
    time.sleep(0.01)  # stand-in for I/O wait
    if number == 3:
        raise ValueError("page 3 failed")
    return f"page-{number}"


def main():
    with ThreadPoolExecutor(max_workers=4) as pool:
        # submit() keeps per-future control; one failure is caught alone.
        futures = {n: pool.submit(fetch_page, n) for n in range(5)}
        results, failures = [], []
        for n in sorted(futures):
            try:
                results.append(futures[n].result())
            except ValueError as exc:
                failures.append(str(exc))
    assert results == ["page-0", "page-1", "page-2", "page-4"]
    assert failures == ["page 3 failed"]
    print(f"PROOF: results in order = {results}")
    print(f"PROOF: failures isolated = {failures}")


if __name__ == "__main__":
    main()
