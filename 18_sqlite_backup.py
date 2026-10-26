"""18_sqlite_backup.py — Back up a database and prove the restore works.

Demonstrates: SQLite's online backup API (not a raw file copy
of a live database), then a restore into a fresh database whose
rows and content hash match the original. An untested backup is
a hope, not a backup — this one is verified.
Run: python3 18_sqlite_backup.py
"""

import hashlib
import sqlite3
import tempfile
from pathlib import Path


def content_hash(db):
    rows = db.execute("SELECT * FROM items ORDER BY id").fetchall()
    return hashlib.sha256(repr(rows).encode()).hexdigest()[:16]


def main():
    with tempfile.TemporaryDirectory() as tmp:
        src_path = Path(tmp) / "source.db"
        bak_path = Path(tmp) / "backup.db"
        src = sqlite3.connect(src_path)
        src.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT)")
        src.executemany("INSERT INTO items VALUES (?, ?)",
                        [(1, "alpha"), (2, "beta"), (3, "gamma")])
        src.commit()
        original_hash = content_hash(src)
        # Online backup: safe while the source is open.
        dst = sqlite3.connect(bak_path)
        src.backup(dst)
        dst.close()
        src.close()
        # Simulate loss, then restore from the backup file.
        src_path.unlink()
        restored = sqlite3.connect(bak_path)
        restored_rows = restored.execute(
            "SELECT * FROM items ORDER BY id").fetchall()
        assert restored_rows == [(1, "alpha"), (2, "beta"), (3, "gamma")]
        assert content_hash(restored) == original_hash
    print("PROOF: restored rows match original, content hash matches")


if __name__ == "__main__":
    main()
