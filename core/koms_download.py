#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil
import time
from pathlib import Path

from selenium.webdriver.common.by import By


class KomsDownload:

    def __init__(self, driver, logger, download_dir, orders_dir):

        self.driver = driver
        self.logger = logger

        self.download_dir = Path(download_dir)
        self.orders_dir = Path(orders_dir)

    def parse_boards(self):

        boards = []

        containers = self.driver.find_elements(
            By.CSS_SELECTOR,
            "div.board_container",
        )

        for container in containers:

            try:

                title = container.find_element(
                    By.CSS_SELECTOR,
                    "span[style*='font-size: 18px']",
                ).text.strip()

            except Exception:

                title = "Unknown"

            buttons = container.find_elements(
                By.CSS_SELECTOR,
                "button.btn_c",
            )

            download = None

            for button in buttons:

                if "엑셀 다운로드" in button.text:

                    download = button
                    break

            if download is None:
                continue

            boards.append({

                "title": title,
                "button": download,

            })

        self.logger.info(
            f"Boards : {len(boards)}"
        )

        return boards
