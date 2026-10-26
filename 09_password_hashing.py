"""09_password_hashing.py — Slow, salted password hashing done right.

Demonstrates: why plain SHA-256 is wrong for passwords (fast =
guessable) and how PBKDF2-HMAC-SHA256 with a random salt fixes
it. Demo values only — no real credentials are used anywhere.
Run: python3 09_password_hashing.py
"""

import hashlib
import hmac
import os

ITERATIONS = 100_000


def hash_password(password: str):
    """Return (salt, digest); the salt is random per password."""
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt, ITERATIONS)
    return salt, digest


def verify(password: str, salt: bytes, digest: bytes) -> bool:
    """Timing-safe comparison: never compare digests with ==."""
    candidate = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt, ITERATIONS)
    return hmac.compare_digest(candidate, digest)


def main():
    demo_password = "demo-only-password"  # demo value, not a real secret
    salt_a, digest_a = hash_password(demo_password)
    salt_b, digest_b = hash_password(demo_password)
    assert digest_a != digest_b  # different salts -> different digests
    assert verify(demo_password, salt_a, digest_a) is True
    assert verify("wrong-password", salt_a, digest_a) is False
    print("PROOF: same password, different salts -> different digests")
    print("PROOF: verify(correct) = True, verify(wrong) = False")


if __name__ == "__main__":
    main()
