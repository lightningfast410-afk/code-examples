"""41_audit_chain.py — A hash-chained audit log (tamper-evident, teaching size).

Demonstrates: the idea behind tamper-evident logs — every
entry stores the hash of the previous entry, so editing any
entry breaks every hash after it. Verification recomputes the
chain from scratch. This is a small teaching model written
from first principles, not production audit infrastructure.
Run: python3 41_audit_chain.py
"""

import hashlib
import json


class AuditChain:
    def __init__(self):
        self.entries = []
        self.prev_hash = "0" * 64

    def append(self, action, detail):
        entry = {"action": action, "detail": detail}
        blob = (self.prev_hash + json.dumps(entry, sort_keys=True)).encode()
        digest = hashlib.sha256(blob).hexdigest()
        self.entries.append({"prev": self.prev_hash,
                             "entry": entry, "hash": digest})
        self.prev_hash = digest

    def verify(self):
        prev = "0" * 64
        for record in self.entries:
            blob = (prev + json.dumps(record["entry"], sort_keys=True)).encode()
            if hashlib.sha256(blob).hexdigest() != record["hash"]:
                return False
            if record["prev"] != prev:
                return False
            prev = record["hash"]
        return True


def main():
    chain = AuditChain()
    chain.append("login", "user alice")
    chain.append("transfer", "10 credits")
    chain.append("logout", "user alice")
    assert chain.verify() is True
    chain.entries[1]["entry"]["detail"] = "999 credits"  # tamper!
    assert chain.verify() is False
    print("PROOF: chain valid before tampering, invalid after editing entry 2")


if __name__ == "__main__":
    main()
