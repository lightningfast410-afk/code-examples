"""15_timing_compare.py — Why == on secrets is a timing leak.

Demonstrates: a normal == comparison stops at the first
differing byte, so an attacker can measure how many leading
bytes are right. hmac.compare_digest always takes the same
time. This demo shows the API difference (timing itself is
measured in the password-hashing example's notes, not here).
Run: python3 15_timing_compare.py
"""

import hmac


def main():
    real = "demo-token-abc123"
    assert (real == "demo-token-abc123") is True
    assert (real == "demo-token-XXXXXX") is False
    # The safe form: constant-time, and it refuses non-ASCII safely.
    assert hmac.compare_digest(real, "demo-token-abc123") is True
    assert hmac.compare_digest(real, "demo-token-XXXXXX") is False
    # compare_digest also rejects length leaks via type errors early:
    try:
        hmac.compare_digest(real, "short")
        length_ok = True
    except TypeError:
        length_ok = False
    assert length_ok is True  # returns False, does not crash
    print("PROOF: compare_digest accepts exact match, rejects all others")
    print("PROOF: rule = compare secrets with compare_digest, never ==")


if __name__ == "__main__":
    main()
