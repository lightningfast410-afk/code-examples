"""24_api_validation.py — Validate an API payload and report every error.

Demonstrates: collecting ALL validation errors instead of
failing on the first one, so a caller can fix everything in
one round trip. Each rule is a small function; the validator
just runs them and gathers messages.
Run: python3 24_api_validation.py
"""


def validate_order(payload):
    """Return a list of error strings; empty means valid."""
    errors = []
    if not isinstance(payload, dict):
        return ["payload must be an object"]
    item = payload.get("item")
    if not isinstance(item, str) or not item.strip():
        errors.append("item must be a non-empty string")
    qty = payload.get("quantity")
    if not isinstance(qty, int) or isinstance(qty, bool) or qty < 1:
        errors.append("quantity must be a positive integer")
    price = payload.get("price")
    if not isinstance(price, (int, float)) or isinstance(price, bool) or price < 0:
        errors.append("price must be a non-negative number")
    return errors


def main():
    assert validate_order({"item": "widget", "quantity": 3, "price": 9.99}) == []
    bad = validate_order({"item": "", "quantity": 0, "price": -1})
    assert len(bad) == 3  # all three problems reported at once
    assert validate_order("not-a-dict") == ["payload must be an object"]
    print(f"PROOF: valid order -> no errors; bad order -> {bad}")


if __name__ == "__main__":
    main()
