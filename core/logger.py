"""
==========================================================
HOMS Logger
==========================================================
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from config import LOG_DIR


class Logger:
    def __init__(self, name: str):
        self.name = name
        self.log_file = Path(LOG_DIR) / f"{name}.log"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def write(self, message: str):
        now = datetime.now()
        line = f"[{now:%Y-%m-%d %H:%M:%S}] {message}"

        print(line)

        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception as e:
            print(f"[LOGGER ERROR] Unable to write log: {e}")

    def info(self, message: str):
        self.write("[INFO] " + message)

    def warning(self, message: str):
        self.write("[WARN] " + message)

    def error(self, message: str):
        self.write("[ERROR] " + message)
