#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class KomsOrder:

    def __init__(self, driver, wait, logger):

        self.driver = driver
        self.wait = wait
        self.logger = logger

    def open_order_page(self, order_url):

        self.driver.get(order_url)

        self.wait.until(

            EC.presence_of_element_located(

                (
                    By.CSS_SELECTOR,
                    "td.order-min-height",
                )

            )

        )

        self.logger.info("Order Page Ready")

    def find_today_orders(self):

        today = datetime.now().strftime("%m/%d")

        results = []

        cards = self.driver.find_elements(
            By.CSS_SELECTOR,
            "td.order-min-height",
        )

        for card in cards:

            try:

                deadlines = card.find_elements(
                    By.CSS_SELECTOR,
                    "span.notification b",
                )

            except Exception:

                continue

            matched = False

            for deadline in deadlines:

                text = deadline.text.strip()

                if not text.startswith("마감"):
                    continue

                if today not in text:
                    continue

                matched = True
                break

            if matched:

                results.append(card)

        self.logger.info(
            f"Today's Orders : {len(results)}"
        )

        return results

    def open_detail(self, card):

        before = self.driver.current_url

        self.driver.execute_script(
            "arguments[0].click();",
            card,
        )

        self.wait.until(
            lambda d: d.current_url != before
        )

        self.wait.until(

            EC.presence_of_element_located(

                (
                    By.CSS_SELECTOR,
                    "div.board_container",
                )

            )

        )

        self.logger.info("Detail Ready")



# == END OF FILE ==
