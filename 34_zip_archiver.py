"""34_zip_archiver.py — Build a zip archive and verify its contents.

Demonstrates: zipfile with deflate compression, writing
several files from a temp directory, then reopening the
archive and checking names and contents match. Archives are
verified on read — a zip you never open is a hope, not a backup.
Run: python3 34_zip_archiver.py
"""

import tempfile
import zipfile
from pathlib import Path


def main():
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        (base / "a.txt").write_text("alpha")
        (base / "b.txt").write_text("beta")
        archive = base / "bundle.zip"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(base / "a.txt", arcname="a.txt")
            zf.write(base / "b.txt", arcname="b.txt")
        with zipfile.ZipFile(archive, "r") as zf:
            assert zf.testzip() is None  # None = no corrupt entries
            names = sorted(zf.namelist())
            assert names == ["a.txt", "b.txt"]
            assert zf.read("a.txt").decode() == "alpha"
    print(f"PROOF: archive holds {names}, contents verified, no corruption")


if __name__ == "__main__":
    main()
