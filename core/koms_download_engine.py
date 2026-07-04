#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
==========================================================
HOMS KOMS Download Engine
==========================================================
"""

from __future__ import annotations

import shutil
import time
from datetime import datetime
from pathlib import Path

from pyvirtualdisplay import Display

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import (
    KOMS_ID,
    KOMS_PW,
    KOMS_LOGIN_URL,
    KOMS_ORDER_URL,
    CHROMEDRIVER,
    CHROMIUM,
    DOWNLOAD_DIR,
    ORDERS_DIR,
    WAIT_TIMEOUT,
    DOWNLOAD_TIMEOUT,
)

from core.logger import Logger


class KomsDownloadEngine:

    def __init__(self):

        self.logger = Logger("koms_download")

        self.display = None
        self.driver = None
        self.wait = None

        self.download_dir = Path(DOWNLOAD_DIR)
        self.orders_dir = Path(ORDERS_DIR)

        self.today = datetime.now().strftime("%Y%m%d")


    # ======================================================
    # Utils
    # ======================================================

    def get_today_mmdd(self):

        return datetime.now().strftime("%m/%d")



    # ======================================================
    # Get Today's Order Index
    # ======================================================

    def get_today_order_indexes(self):

        today = self.get_today_mmdd()

        indexes = []

        cards = self.driver.find_elements(
            By.CSS_SELECTOR,
            "td.order-min-height",
        )

        for index, card in enumerate(cards):

            try:

                deadlines = card.find_elements(
                    By.CSS_SELECTOR,
                    "span.notification b",
                )

            except Exception:

                continue

            for deadline in deadlines:

                text = deadline.text.strip()

                if text.startswith("마감") and today in text:

                    indexes.append(index)

                    break

        if not indexes:

            raise RuntimeError(
                f"{today} 주문을 찾지 못했습니다."
            )

        self.log(
            f"Today's Cards : {indexes}"
        )

        return indexes


# ===== END OF PART 1 =====

    # ======================================================
    # Browser
    # ======================================================

    def start_browser(self):

        self.log("Start Browser")

        self.display = Display(
            visible=0,
            size=(1920, 1080),
        )

        self.display.start()

        options = Options()

        options.binary_location = CHROMIUM

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        prefs = {
            "download.default_directory": str(self.download_dir),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        }

        options.add_experimental_option(
            "prefs",
            prefs,
        )

        self.driver = webdriver.Chrome(
            service=Service(CHROMEDRIVER),
            options=options,
        )

        self.wait = WebDriverWait(
            self.driver,
            WAIT_TIMEOUT,
        )

        self.driver.set_window_size(
            1920,
            1080,
        )

        self.log("Browser Ready")

# ===== END OF PART 2 =====


    # ======================================================
    # Login
    # ======================================================

    def login(self):

        self.log("Open Login Page")

        self.driver.get(KOMS_LOGIN_URL)

        login_box = self.wait.until(

            EC.presence_of_element_located(

                (
                    By.CSS_SELECTOR,
                    "fieldset.login_field",
                )

            )

        )

        inputs = login_box.find_elements(
            By.CSS_SELECTOR,
            "input.txt",
        )

        if len(inputs) != 2:

            raise RuntimeError(
                "로그인 입력창을 찾지 못했습니다."
            )

        inputs[0].clear()
        inputs[0].send_keys(KOMS_ID)

        inputs[1].clear()
        inputs[1].send_keys(KOMS_PW)

        login_btn = login_box.find_element(
            By.CSS_SELECTOR,
            "button.login_btn",
        )

        login_btn.click()

        self.wait.until(
            lambda d: d.current_url != KOMS_LOGIN_URL
        )

        self.log("Login Success")

    # ======================================================
    # Order Page
    # ======================================================

    def open_order_page(self):

        self.log("Open Order Page")

        self.driver.get(
            KOMS_ORDER_URL
        )

        self.wait.until(

            EC.presence_of_element_located(

                (
                    By.CSS_SELECTOR,
                    "td.order-min-height",
                )

            )

        )

        self.log("Order Page Ready")


# ===== END OF PART 3 =====


    # ======================================================
    # Open Detail
    # ======================================================

    def open_detail(self, index):

        cards = self.driver.find_elements(
            By.CSS_SELECTOR,
            "td.order-min-height",
        )

        if index >= len(cards):

            raise RuntimeError(
                "카드 Index 오류"
            )

        before = self.driver.current_url

        self.driver.execute_script(
            "arguments[0].click();",
            cards[index],
        )

        self.wait.until(
            lambda d:
            d.current_url != before
        )

        self.wait.until(

            EC.presence_of_element_located(

                (
                    By.CSS_SELECTOR,
                    "div.board_container",
                )

            )

        )

    # ======================================================
    # Find Download Sections
    # ======================================================

    def get_sections(self):

        sections = []

        wrappers = self.driver.find_elements(
            By.CSS_SELECTOR,
            "div.order_wrap > div",
        )

        for wrapper in wrappers:

            try:

                title = wrapper.find_element(
                    By.CSS_SELECTOR,
                    "strong",
                ).text.strip()

            except Exception:

                continue

            try:

                button = wrapper.find_element(
                    By.CSS_SELECTOR,
                    "button.btn_c",
                )

            except Exception:

                continue

            sections.append(

                {
                    "title": title,
                    "button": button,
                }

            )

        self.log(
            f"{len(sections)} Download Sections"
        )

        return sections

# ===== END OF PART 4 =====

    # ======================================================
    # Parse Boards
    # ======================================================

    def parse_boards(self):

        self.log("Parse Boards")

        boards = []

        containers = self.driver.find_elements(
            By.CSS_SELECTOR,
            "div.board_container",
        )

        if not containers:

            raise RuntimeError(
                "board_container를 찾지 못했습니다."
            )

        for container in containers:

            try:

                title = container.find_element(
                    By.CSS_SELECTOR,
                    "div[style*='justify-content: space-between'] span"
                ).text.strip()

            except Exception:

                title = "Unknown"

            try:

                order_no = container.find_element(
                    By.CSS_SELECTOR,
                    "div.notification strong"
                ).text.strip()

            except Exception:

                order_no = ""

            buttons = container.find_elements(
                By.CSS_SELECTOR,
                "button.btn_c",
            )

            download_button = None

            for button in buttons:

                if "엑셀 다운로드" in button.text:

                    download_button = button
                    break

            if download_button is None:

                self.log(
                    f"Skip : {title}"
                )

                continue

            safe_name = (
                title.replace("/", "_")
                     .replace("(", "")
                     .replace(")", "")
                     .replace(" ", "")
            )

            boards.append({

                "title": title,

                "name": safe_name,

                "order_no": order_no,

                "button": download_button,

            })

        self.log(
            f"Boards : {len(boards)}"
        )

        return boards

    # ======================================================
    # Download Board
    # ======================================================

    def download_board(self, board):

        self.log(
            f"Download : {board['title']}"
        )

        before = {

            f.name

            for f in self.download_dir.iterdir()

        }

        self.driver.execute_script(

            "arguments[0].click();",

            board["button"],

        )

        file_path = self.wait_download(before)

        return file_path

    # ======================================================
    # Wait Download
    # ======================================================

    def wait_download(self, before):

        end = time.time() + DOWNLOAD_TIMEOUT

        while time.time() < end:

            if list(self.download_dir.glob("*.crdownload")):

                time.sleep(0.5)
                continue

            files = sorted(
                self.download_dir.glob("*.xlsx"),
                key=lambda x: x.stat().st_mtime,
            )

            new_files = [

                f

                for f in files

                if f.name not in before

            ]

            if new_files:

                latest = new_files[-1]

                self.log(
                    f"Downloaded : {latest.name}"
                )

                return latest

            time.sleep(0.5)

        raise TimeoutError(
            "다운로드 시간 초과"
        )

# ===== END OF PART 6 =====

    # ======================================================
    # Rename File
    # ======================================================

    def rename_file(self, file_path, board):

        filename = (
            f"{self.today}"
            f"_{board['name']}"
            ".xlsx"
        )

        target = self.orders_dir / filename

        if target.exists():

            target.unlink()

        shutil.move(
            str(file_path),
            str(target),
        )

        self.log(
            f"Saved : {target.name}"
        )

        return target

    # ======================================================
    # Download All
    # ======================================================

    def download_all(self):

        boards = self.parse_boards()

        results = []

        for board in boards:

            self.log(
                f"Start : {board['title']}"
            )

            file_path = self.download_board(board)

            saved = self.rename_file(
                file_path,
                board,
            )

            results.append(saved)

        self.log(
            f"Downloaded : {len(results)}"
        )

        return results

    # ======================================================
    # Close
    # ======================================================

    def close(self):

        self.log("Close Browser")

        try:

            if self.driver:

                self.driver.quit()

        finally:

            if self.display:

                self.display.stop()

    # ======================================================
    # Run
    # ======================================================


    indexes = self.get_today_order_indexes()

    total = 0

    for index in indexes:

        self.open_detail(index)

        files = self.download_all()

        total += len(files)

        self.driver.get(KOMS_ORDER_URL)

        self.wait.until(

            EC.presence_of_element_located(

                (
                    By.CSS_SELECTOR,
                    "td.order-min-height",
                )

            )

        )

# ======================================================
# Main
# ======================================================

if __name__ == "__main__":

    engine = KomsDownloadEngine()

    engine.run()

# == END OF FILE ==


