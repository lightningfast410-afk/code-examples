"""33_log_rotation.py — Logs that rotate instead of growing forever.

Demonstrates: logging.handlers.RotatingFileHandler with a
small maxBytes so rotation is observable in the demo, plus a
formatter that keeps every line structured (time, level,
message). Backups are kept up to backupCount, then the oldest
is dropped — rotation bounds disk use; it is not an archive.
The proof checks the bound and that the newest lines survive.
Run: python3 33_log_rotation.py
"""

import logging
import logging.handlers
import tempfile
from pathlib import Path


def main():
    with tempfile.TemporaryDirectory() as tmp:
        log_path = Path(tmp) / "app.log"
        handler = logging.handlers.RotatingFileHandler(
            log_path, maxBytes=200, backupCount=3)
        handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s"))
        logger = logging.getLogger("rotation-demo")
        logger.setLevel(logging.INFO)
        logger.handlers = [handler]
        logger.propagate = False
        for i in range(20):
            logger.info("event number %d with some padding text", i)
        handler.close()
        files = sorted(p.name for p in Path(tmp).iterdir())
        assert "app.log" in files
        assert any(name.startswith("app.log.") for name in files)  # rotated
        assert len(files) <= 4  # current log + 3 backups, bounded
        total_bytes = sum((Path(tmp) / name).stat().st_size for name in files)
        assert total_bytes <= 4 * 200 + 200  # bounded, not 20 lines' worth
        newest = (Path(tmp) / "app.log").read_text()
        assert "event number 19" in newest  # newest lines survive
    print(f"PROOF: log files after rotation = {files}")
    print(f"PROOF: total log bytes bounded at {total_bytes}, newest event kept")


if __name__ == "__main__":
    main()
