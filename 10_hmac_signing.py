"""10_hmac_signing.py — Message authentication with HMAC-SHA256.

Demonstrates: proving a message came from the key holder and
was not altered, without sharing the key. The receiver recomputes
the tag and compares it in constant time. Tampered content and
wrong keys both fail; the tag alone never reveals the key.
Run: python3 10_hmac_signing.py
"""

import hashlib
import hmac

# Demo-only key for this teaching example, never a real secret.
DEMO_KEY = b"demo-key-for-teaching-only"


def sign(message: bytes) -> str:
    return hmac.new(DEMO_KEY, message, hashlib.sha256).hexdigest()


def verify(message: bytes, tag: str) -> bool:
    return hmac.compare_digest(sign(message), tag)


def main():
    message = b"transfer 10 credits to account-42"
    tag = sign(message)
    assert verify(message, tag) is True
    assert verify(b"transfer 999 credits to account-42", tag) is False
    wrong_key = hmac.new(b"someone-else-key", message, hashlib.sha256).hexdigest()
    assert wrong_key != tag
    print(f"PROOF: valid -> True, tampered -> False, wrong-key tag differs")


if __name__ == "__main__":
    main()
