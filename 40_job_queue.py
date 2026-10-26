"""40_job_queue.py — An in-memory job queue with retries and a dead pile.

Demonstrates: a small reliable-work pattern — jobs run in
order, a failing job is retried up to N times, and a job that
keeps failing lands in a dead-letter list for a human instead
of looping forever. No external broker needed for the pattern.
Run: python3 40_job_queue.py
"""

from collections import deque


class JobQueue:
    def __init__(self, max_retries=2):
        self.pending = deque()
        self.dead = []
        self.completed = []
        self.max_retries = max_retries

    def add(self, job):
        self.pending.append({"job": job, "attempts": 0})

    def run_all(self, handler):
        while self.pending:
            entry = self.pending.popleft()
            try:
                handler(entry["job"])
            except Exception:
                entry["attempts"] += 1
                if entry["attempts"] <= self.max_retries:
                    self.pending.append(entry)
                else:
                    self.dead.append(entry["job"])
            else:
                self.completed.append(entry["job"])


def main():
    attempts = {}

    def handler(job):
        attempts[job] = attempts.get(job, 0) + 1
        if job == "flaky" and attempts[job] < 3:
            raise RuntimeError("transient failure")
        if job == "broken":
            raise RuntimeError("always fails")

    queue = JobQueue(max_retries=2)
    for job in ("ok", "flaky", "broken"):
        queue.add(job)
    queue.run_all(handler)
    assert queue.completed == ["ok", "flaky"]  # flaky won on retry 3
    assert queue.dead == ["broken"]  # gave up after retries, parked
    assert attempts["flaky"] == 3 and attempts["broken"] == 3
    print(f"PROOF: completed = {queue.completed}, dead = {queue.dead}")


if __name__ == "__main__":
    main()
