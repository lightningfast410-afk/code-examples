"""31_config_loader.py — Configuration with defaults, file, and overrides.

Demonstrates: the standard precedence — built-in defaults,
then a config file, then environment variables on top. Missing
files are fine (defaults apply); malformed values fail loudly
with the key named. No secrets are read or printed here.
Run: python3 31_config_loader.py
"""

import json
import os
import tempfile
from pathlib import Path

DEFAULTS = {"host": "127.0.0.1", "port": 8080, "workers": 2}


def load_config(path, env):
    config = dict(DEFAULTS)
    if path is not None and Path(path).exists():
        try:
            file_values = json.loads(Path(path).read_text())
        except json.JSONDecodeError as exc:
            raise ValueError(f"bad config file {path}: {exc}") from exc
        if not isinstance(file_values, dict):
            raise ValueError("config file must hold an object")
        config.update(file_values)
    for key in DEFAULTS:
        env_key = f"APP_{key.upper()}"
        if env_key in env:
            value = env[env_key]
            config[key] = int(value) if isinstance(DEFAULTS[key], int) else value
    return config


def main():
    with tempfile.TemporaryDirectory() as tmp:
        cfg_path = Path(tmp) / "config.json"
        cfg_path.write_text(json.dumps({"port": 9000}))
        loaded = load_config(cfg_path, {"APP_WORKERS": "4"})
        assert loaded == {"host": "127.0.0.1", "port": 9000, "workers": 4}
        plain = load_config(None, {})
        assert plain == DEFAULTS
    print(f"PROOF: file + env override -> {loaded}")
    print(f"PROOF: no file, no env -> defaults {plain}")


if __name__ == "__main__":
    main()
