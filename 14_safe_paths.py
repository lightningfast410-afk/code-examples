"""14_safe_paths.py — Stop path traversal before it escapes the base dir.

Demonstrates: resolving a user-supplied relative path against a
base directory and refusing anything that escapes it (e.g.
"../../etc/passwd" or an absolute path). Never join user input
onto a path unchecked.
Run: python3 14_safe_paths.py
"""

import os
import tempfile
from pathlib import Path


def safe_join(base: Path, user_path: str) -> Path:
    """Resolve user_path inside base, or raise ValueError."""
    base = base.resolve()
    target = (base / user_path).resolve()
    if not (target == base or base in target.parents):
        raise ValueError(f"path escapes base directory: {user_path!r}")
    return target


def main():
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        (base / "notes.txt").write_text("hello")
        ok = safe_join(base, "notes.txt")
        assert ok.read_text() == "hello"
        rejected = 0
        for evil in ("../escape.txt", "../../etc/passwd", "/etc/passwd",
                     "subdir/../../escape.txt"):
            try:
                safe_join(base, evil)
            except ValueError:
                rejected += 1
        assert rejected == 4
    print("PROOF: 1 safe path resolved, 4 traversal attempts rejected")


if __name__ == "__main__":
    main()
