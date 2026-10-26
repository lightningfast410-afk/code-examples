"""35_temp_files.py — Temporary files that always clean up after themselves.

Demonstrates: tempfile.TemporaryDirectory as a context
manager — everything inside vanishes when the block exits,
even if an exception is raised. The demo proves the cleanup
by checking the directory is gone afterwards.
Run: python3 35_temp_files.py
"""

import tempfile
from pathlib import Path


def main():
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "work.txt"
        work.write_text("scratch data")
        assert work.read_text() == "scratch data"
        saved = tmp
    assert not Path(saved).exists()  # gone after the block
    # Same guarantee under an exception.
    try:
        with tempfile.TemporaryDirectory() as tmp2:
            (Path(tmp2) / "x.txt").write_text("x")
            raise RuntimeError("simulated failure")
    except RuntimeError:
        pass
    assert not Path(tmp2).exists()
    print("PROOF: temp dir removed after normal exit and after exception")


if __name__ == "__main__":
    main()
