"""27_producer_consumer.py — A queue between producers and consumers.

Demonstrates: the classic pattern for decoupling work — one
thread produces items, worker threads consume them, and a
sentinel value (None) tells each worker to stop. The queue
itself handles all locking; no shared counter is touched.
Run: python3 27_producer_consumer.py
"""

import queue
import threading

WORKERS = 2


def main():
    jobs = queue.Queue()
    done = []

    def worker():
        while True:
            item = jobs.get()
            try:
                if item is None:  # sentinel: stop this worker
                    return
                done.append(item * 2)
            finally:
                jobs.task_done()

    pool = [threading.Thread(target=worker) for _ in range(WORKERS)]
    for thread in pool:
        thread.start()
    for item in range(10):
        jobs.put(item)
    for _ in range(WORKERS):
        jobs.put(None)
    jobs.join()
    for thread in pool:
        thread.join()
    assert sorted(done) == [i * 2 for i in range(10)]
    print(f"PROOF: 10 jobs in, 10 doubled results out: {sorted(done)}")


if __name__ == "__main__":
    main()
