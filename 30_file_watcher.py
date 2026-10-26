"""30_file_watcher.py — Notice a new file in a directory (polling).

Demonstrates: the simplest reliable watcher — snapshot the
directory, sleep briefly, snapshot again, and report what
appeared. A background thread creates the file mid-run so the
demo proves detection instead of assuming it. Polling is the
portable choice; OS-specific watchers are an upgrade, not a
requirement.
Run: python3 30_file_watcher.py
"""

import tempfile
import threading
import time
from pathlib import Path


def snapshot(directory: Path):
    return {p.name for p in directory.iterdir()}


def main():
    with tempfile.TemporaryDirectory() as tmp:
        directory = Path(tmp)
        before = snapshot(directory)

        def create_later():
            time.sleep(0.2)
            (directory / "report.txt").write_text("done")

        threading.Thread(target=create_later, daemon=True).start()
        new_files = []
        for _ in range(20):  # poll up to 2 seconds
            time.sleep(0.1)
            new_files = sorted(snapshot(directory) - before)
            if new_files:
                break
        assert new_files == ["report.txt"]
    print(f"PROOF: detected new file: {new_files}")


if __name__ == "__main__":
    main()
