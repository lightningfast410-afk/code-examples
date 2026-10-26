"""20_json_handling.py — JSON in, validated data out, safe defaults.

Demonstrates: json.loads with error handling, type-checking
each field before use, and .get() defaults so a missing field
never crashes the program. Unknown extra fields are ignored,
not trusted.
Run: python3 20_json_handling.py
"""

import json


def parse_user(payload: str):
    """Return a clean (name, age) pair or raise ValueError."""
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ValueError(f"not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("expected a JSON object")
    name = data.get("name", "unknown")
    age = data.get("age", 0)
    if not isinstance(name, str) or not isinstance(age, int):
        raise ValueError("wrong field types")
    return name, age


def main():
    assert parse_user('{"name": "alice", "age": 30, "extra": true}') == ("alice", 30)
    assert parse_user('{"name": "bob"}') == ("bob", 0)  # missing age defaults
    rejected = 0
    for bad in ('not json', '{"name": 5}', '[1, 2, 3]'):
        try:
            parse_user(bad)
        except ValueError:
            rejected += 1
    assert rejected == 3
    print("PROOF: valid payloads parsed, defaults applied, 3 bad rejected")


if __name__ == "__main__":
    main()
