"""13_log_redaction.py — Redact sensitive fields before a log is written.

Demonstrates: the rule that a secret reaching a log file is
already leaked. Redaction happens by FIELD NAME, before writing,
so values are never printed — not even for this demo. A check
at the end proves no demo value appears in the rendered output.
Run: python3 13_log_redaction.py
"""

import json

SENSITIVE = ("password", "secret", "token", "api_key", "auth")


def redact(record):
    """Return a copy with sensitive fields replaced, recursively."""
    if isinstance(record, dict):
        return {key: ("[REDACTED]" if any(s in key.lower() for s in SENSITIVE)
                      else redact(value))
                for key, value in record.items()}
    if isinstance(record, list):
        return [redact(item) for item in record]
    return record


def main():
    entry = {"user": "alice", "action": "login",
             "api_key": "demo-key-value-1234",
             "nested": {"token": "demo-token-value-5678", "ok": True}}
    rendered = json.dumps(redact(entry))
    assert "demo-key-value-1234" not in rendered
    assert "demo-token-value-5678" not in rendered
    assert rendered.count("[REDACTED]") == 2
    assert '"user": "alice"' in rendered  # harmless fields survive
    print(f"PROOF: rendered log = {rendered}")
    print("PROOF: 2 fields redacted, 0 secret values in output")


if __name__ == "__main__":
    main()
