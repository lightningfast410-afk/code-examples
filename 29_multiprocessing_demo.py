"""29_multiprocessing_demo.py — CPU work spread across processes.

Demonstrates: ProcessPoolExecutor for work the GIL would
serialize in threads. Each worker sums a range independently;
the parent adds the partial sums. The __main__ guard matters:
without it, child processes would re-run the whole script.
Run: python3 29_multiprocessing_demo.py
"""

from concurrent.futures import ProcessPoolExecutor


def partial_sum(bounds):
    lo, hi = bounds
    return sum(range(lo, hi))


def main():
    ranges = [(0, 250_000), (250_000, 500_000),
              (500_000, 750_000), (750_000, 1_000_000)]
    with ProcessPoolExecutor(max_workers=4) as pool:
        parts = list(pool.map(partial_sum, ranges))
    total = sum(parts)
    assert total == sum(range(1_000_000)) == 499999500000
    print(f"PROOF: partial sums = {parts}")
    print(f"PROOF: total = {total}")


if __name__ == "__main__":
    main()
