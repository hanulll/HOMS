#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

from pyvirtualdisplay import Display

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import (
    CHROMEDRIVER,
    CHROMIUM,
    DOWNLOAD_DIR,
    WAIT_TIMEOUT,
    KOMS_LOGIN_URL,
    KOMS_ID,
    KOMS_PW,
)


class KomsLogin:

    def __init__(self, logger):

        self.logger = logger

        self.display = None
        self.driver = None
        self.wait = None

        self.download_dir = Path(DOWNLOAD_DIR)

    def start_browser(self):

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

        self.logger.info("Browser Started")

    def login(self):

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
            raise RuntimeError("로그인 입력창을 찾을 수 없습니다.")

        inputs[0].send_keys(KOMS_ID)
        inputs[1].send_keys(KOMS_PW)

        login_box.find_element(
            By.CSS_SELECTOR,
            "button.login_btn",
        ).click()

        self.wait.until(
            lambda d: d.current_url != KOMS_LOGIN_URL
        )

        self.logger.info("Login Success")

    def close(self):

        try:

            if self.driver:

                self.driver.quit()

        finally:

            if self.display:

                self.display.stop()

# == END OF FILE ==


