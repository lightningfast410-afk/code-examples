"""11_input_validation.py — Validate input at the boundary, reject the rest.

Demonstrates: the single most important security habit — never
trust caller input. Each validator returns a clean value or
raises a clear ValueError; nothing invalid flows downstream.
Run: python3 11_input_validation.py
"""

import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def valid_email(value):
    if not isinstance(value, str) or not EMAIL_RE.match(value):
        raise ValueError(f"invalid email: {value!r}")
    return value.lower()


def valid_age(value):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("age must be an integer")
    if not 0 <= value <= 130:
        raise ValueError("age out of range 0-130")
    return value


def valid_username(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_]{3,20}", value):
        raise ValueError("username must be 3-20 letters, digits or underscore")
    return value


def main():
    assert valid_email("Alice@Example.COM") == "alice@example.com"
    assert valid_age(30) == 30
    assert valid_username("coder_42") == "coder_42"
    rejected = 0
    for bad in (lambda: valid_email("not-an-email"),
                lambda: valid_age(-5),
                lambda: valid_age("thirty"),
                lambda: valid_username("ab"),
                lambda: valid_username("has space")):
        try:
            bad()
        except ValueError:
            rejected += 1
    assert rejected == 5
    print("PROOF: 3 valid inputs accepted, 5 invalid inputs rejected")


if __name__ == "__main__":
    main()
