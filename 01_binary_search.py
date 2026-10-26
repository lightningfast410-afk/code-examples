"""01_binary_search.py — Binary search, manual and with bisect.

Demonstrates: O(log n) search over a sorted list, handling the
not-found case cleanly instead of raising.
Run: python3 01_binary_search.py
"""

import bisect


def binary_search(sorted_items, target):
    """Return the index of target, or -1 when it is absent."""
    lo, hi = 0, len(sorted_items) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_items[mid] == target:
            return mid
        if sorted_items[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def main():
    data = [3, 7, 12, 19, 24, 31, 42, 58]
    found = binary_search(data, 24)
    missing = binary_search(data, 25)
    # Cross-check against the standard library.
    assert found == bisect.bisect_left(data, 24)
    assert missing == -1
    print(f"PROOF: search(24) -> index {found}, search(25) -> {missing}")


if __name__ == "__main__":
    main()
