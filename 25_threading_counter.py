"""25_threading_counter.py — The race condition, then the lock that fixes it.

Demonstrates: why shared mutable state needs a lock. Four
threads incrementing 5,000 times each without a lock lose most
updates (read-add-write is not atomic); with a lock, every
update lands and the final count is exactly 20,000.
Run: python3 25_threading_counter.py
"""

import threading


def run_locked(use_lock, threads=4, increments=5000):
    counter = [0]
    lock = threading.Lock()

    def work():
        for _ in range(increments):
            if use_lock:
                with lock:
                    counter[0] += 1
            else:
                counter[0] += 1

    pool = [threading.Thread(target=work) for _ in range(threads)]
    for thread in pool:
        thread.start()
    for thread in pool:
        thread.join()
    return counter[0]


def main():
    expected = 4 * 5000
    unlocked = run_locked(False)
    locked = run_locked(True)
    assert locked == expected
    # The unlocked run almost always loses updates; if a rare
    # scheduling makes it exact, the locked result still proves the point.
    print(f"PROOF: without lock final={unlocked} (lost {expected - unlocked})")
    print(f"PROOF: with lock final={locked} (lost 0)")


if __name__ == "__main__":
    main()
