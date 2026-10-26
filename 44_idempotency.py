"""44_idempotency.py — Retries must never double-charge or double-apply.

Demonstrates: idempotency keys — the first request with a key
executes and stores its result; a retry with the same key
returns the stored result without re-executing; the same key
with different work is a conflict, not a second execution.
The key and its result must be stored together, or a crash
re-opens the double-charge window.
Run: python3 44_idempotency.py
"""


class IdempotentStore:
    def __init__(self):
        self.results = {}
        self.executions = 0

    def execute(self, key, amount, work):
        """work is a callable run only on first sight of key."""
        if key in self.results:
            stored_amount, stored_result = self.results[key]
            if stored_amount != amount:
                raise ValueError("same key, different amount: conflict")
            return stored_result, False  # duplicate: no re-execution
        result = work()
        self.executions += 1
        self.results[key] = (amount, result)
        return result, True


def main():
    store = IdempotentStore()
    first, fresh = store.execute("order-1", 99, lambda: "receipt-A")
    retry, fresh2 = store.execute("order-1", 99, lambda: "receipt-B")
    assert (first, fresh) == ("receipt-A", True)
    assert (retry, fresh2) == ("receipt-A", False)  # same receipt, no re-run
    store.execute("order-2", 50, lambda: "receipt-C")
    assert store.executions == 2  # 3 requests, 2 executions
    try:
        store.execute("order-1", 50, lambda: "receipt-X")
        raise AssertionError("amount conflict should have raised")
    except ValueError:
        pass
    print("PROOF: 3 requests -> 2 executions; retry returned stored receipt")


if __name__ == "__main__":
    main()
