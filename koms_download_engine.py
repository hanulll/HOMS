#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
==========================================================
HOMS KOMS Download Engine
Version : 2.0
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

    # ======================================================
    # Initialize
    # ======================================================

    def __init__(self):

        self.logger = Logger("koms_download")

        self.display = None
        self.driver = None
        self.wait = None

        self.download_dir = Path(DOWNLOAD_DIR)
        self.orders_dir = Path(ORDERS_DIR)

        self.today = datetime.now().strftime("%Y%m%d")
        self.today_mmdd = datetime.now().strftime("%m/%d")

        self.orders_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ======================================================
    # Logger
    # ======================================================

    def log(self, message):

        self.logger.info(message)

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

        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        prefs = {

            "download.default_directory": str(
                self.download_dir
            ),

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

        self.driver.set_window_size(
            1920,
            1080,
        )

        self.wait = WebDriverWait(
            self.driver,
            WAIT_TIMEOUT,
        )

        self.log("Browser Ready")

    # ======================================================
    # Login
    # ======================================================

    def login(self):

        self.log("Open Login Page")

        self.driver.get(
            KOMS_LOGIN_URL
        )

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

        login_box.find_element(

            By.CSS_SELECTOR,
            "button.login_btn",

        ).click()

        time.sleep(2)

        self.log("Login Success")

    # ======================================================
    # Open Order Page
    # ======================================================

    def open_order_page(self):

        self.log("Open Order Page")

        self.driver.get(KOMS_ORDER_URL)

        time.sleep(5)

        self.driver.save_screenshot(
            "/home/hanul/HOMS/order_page.png"
        )

        self.log("Order Page Ready")


    # ======================================================
    # Find Today Orders
    # ======================================================

    def get_today_order_indexes(self):

        cards = self.driver.find_elements(
            By.CSS_SELECTOR,
            "td.order-min-height",
        )

        if not cards:
            raise RuntimeError(
                "주문 카드를 찾지 못했습니다."
            )

        latest = cards[-1]

        self.log(
            f"Use Latest Card : {latest.text.splitlines()[0]}"
        )

        return [len(cards) - 1]

    # ======================================================
    # Open Detail
    # ======================================================

    def open_detail(self, index):

        cards = self.driver.find_elements(
            By.CSS_SELECTOR,
            "td.order-min-height",
        )

        card = cards[index]

        text = card.text

        import re

        m = re.search(r"(\d{2})/(\d{2})", text)

        if not m:
            raise RuntimeError("배송일을 찾을 수 없습니다.")

        month = m.group(1)
        day = m.group(2)

        year = datetime.now().strftime("%Y")

        delivery = f"{year}{month}{day}"

        url = (
            "https://koms.kyochon.com/bc/od3000c/odst01cDetail"
            f"?deliveryYmd={delivery}"
            "&contSeq=1299"
            f"&searchDeliveryYmd={delivery}"
        )

        self.log(url)

        self.driver.get(url)

        self.wait.until(

            EC.presence_of_element_located(

                (
                    By.CSS_SELECTOR,
                    "div.board_container",
                )

            )

        )

        self.log("Detail Ready")

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

                title = "Unknown"

                spans = container.find_elements(
                    By.TAG_NAME,
                    "span",
                )

                for span in spans:

                    text = span.text.strip()

                    if "/" in text:

                        title = (
                            text.replace(" / ", "_")
                                .replace("/", "_")
                                .replace("(", "")
                                .replace(")", "")
                                .replace(" ", "")
                        )

                        break

            except Exception:

                title = "Unknown"

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

            for f in self.download_dir.glob("*")

        }

        button = board["button"]

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            button,
        )

        time.sleep(1)

        try:

            button.click()

        except Exception:

            self.log(button.text)

            self.driver.execute_script(
                "arguments[0].click();",
                button,
            )

        time.sleep(2)

        return self.wait_download(before)

        file_path = self.wait_download(before)

        if file_path.stat().st_size == 0:

            raise RuntimeError(
                "다운로드 파일이 비어 있습니다."
            )

        return file_path

    # ======================================================
    # Wait Download
    # ======================================================

    def wait_download(self, before):

        end_time = time.time() + DOWNLOAD_TIMEOUT

        while time.time() < end_time:

            if list(self.download_dir.glob("*.crdownload")):

                time.sleep(0.5)

                continue

            files = sorted(

                list(self.download_dir.glob("*.xlsx")) +

                list(self.download_dir.glob("*.xls")),

                key=lambda f: f.stat().st_mtime,

            )

            for file in reversed(files):

                if file.name not in before:

                    self.log(
                        f"Downloaded : {file.name}"
                    )

                    return file

            time.sleep(0.5)

        raise TimeoutError(
            "다운로드 시간 초과"
        )

    # ======================================================
    # Rename File
    # ======================================================

    def rename_file(self, file_path, board):

        filename = (
            f"{self.today}"
            f"_{board['name']}"
            f"_{int(time.time())}"
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
    # Download All Boards
    # ======================================================

    def download_all(self):

        results = []

        boards = self.parse_boards()

        for i in range(len(boards)):

            boards = self.parse_boards()

            board = boards[i]

            file_path = self.download_board(board)

            saved = self.rename_file(
                file_path,
                board,
            )

            results.append(saved)

        self.log(
            f"Downloaded Files : {len(results)}"
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

    def run(self):

        try:

            self.start_browser()

            self.login()

            self.open_order_page()

            indexes = self.get_today_order_indexes()

            total_files = 0

            for order_no, index in enumerate(indexes, start=1):

                self.log(
                    f"===== ORDER {order_no} ====="
                )

                self.open_detail(index)

                files = self.download_all()

                total_files += len(files)

                # 목록으로 복귀
                self.driver.get(
                    KOMS_ORDER_URL
                )

                time.sleep(1)

                self.driver.refresh()

                self.wait.until(

                    EC.presence_of_element_located(

                        (
                            By.CSS_SELECTOR,
                            "td.order-min-height",
                        )

                    )

                )
            self.log(
                f"TOTAL FILES : {total_files}"
            )

            self.log(
                "Download Complete"
            )

        except Exception as e:

            self.log(
                f"ERROR : {e}"
            )

            raise

        finally:

            self.close()


# ======================================================
# Main
# ======================================================

def main():

    engine = KomsDownloadEngine()

    engine.run()


if __name__ == "__main__":

    main()

# == END OF FILE ==
