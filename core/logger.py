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

        self.log_file = (
            Path(LOG_DIR)
            / f"{name}.log"
        )

    def write(
        self,
        message: str,
    ):

        now = datetime.now()

        line = (
            f"[{now:%Y-%m-%d %H:%M:%S}] "
            f"{message}"
        )

        print(line)

        with open(
            self.log_file,
            "a",
            encoding="utf-8",
        ) as f:

            f.write(
                line + "\n"
            )

    def info(
        self,
        message: str,
    ):

        self.write(
            "[INFO] " + message
        )

    def warning(
        self,
        message: str,
    ):

        self.write(
            "[WARN] " + message
        )

    def error(
        self,
        message: str,
    ):

        self.write(
            "[ERROR] " + message
        )
