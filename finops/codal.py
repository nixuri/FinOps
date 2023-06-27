import os
import json
import time
import jdatetime
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from finops.utils.scraper import Scraper
from finops.utils.preprocessor import Preprocessor
from finops.utils.wrappers import sleep, retry
from finops.config import (
    CODAL_SEARCH_BASE_URL,
    CODAL_LETTERS_LIST_COLUMNS,
    BALANCE_SHEET_ID,
    PNL_SHEET_ID,
    BALANCE_SHEET_COLUMNS,
    PNL_SHEET_COLUMNS,
    CODAL_BASIC_INFO_COLUMNS,
)
from finops.logger import logger


class Codal(Scraper, Preprocessor):
    def __init__(self, search_params, driver_path="selenium/chromedriver"):
        self.driver = self._initialize_driver(driver_path)
        self.search_params = search_params

    def _initialize_driver(self, driver_path):
        service = Service(driver_path)
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-extensions")
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)
        return driver

    def _create_search_url(self, **kwargs):
        url = CODAL_SEARCH_BASE_URL
        url += "&".join([f"{key}={value}" for key, value in kwargs.items()])
        return url

    def _get_letters_list_pages_number(self):
        search_url = self._create_search_url(**self.search_params)
        response = self._download(search_url)
        parsed_response = self._parse_json_response(response)
        n_pages = parsed_response["Page"]
        return n_pages

    @sleep
    @retry(max_retries=3, wait_time=1)
    def _scrap_letters_list_one_page(self, page_number):
        search_params = self.search_params.copy()
        search_params["PageNumber"] = page_number
        search_url = self._create_search_url(**search_params)
        response = self._download(search_url)
        parsed_response = self._parse_json_response(response)
        letters_list_df = self._preprocess_letters_list(parsed_response)
        return letters_list_df

    def _scrap_letters_list(self, store_path, stocks=None, verbose=True):
        letters_list = self._load_or_create_csv(store_path, CODAL_LETTERS_LIST_COLUMNS)
        scraped_letters = self._get_scraped_ids(letters_list, "tracing_id")
        n_pages = self._get_letters_list_pages_number()
        for page_number in range(1, n_pages + 1):
            letters_list_one_page = self._scrap_letters_list_one_page(page_number)
            if stocks is not None:
                letters_list_one_page = letters_list_one_page[
                    letters_list_one_page.symbol.isin(stocks)
                ]
            letters_list_one_page = letters_list_one_page[
                ~letters_list_one_page.tracing_id.isin(scraped_letters)
            ]
            self._save_csv(letters_list_one_page, store_path)
            time.sleep(1)
            if verbose:
                logger.info(f"Page {page_number} of {n_pages} is scrapped.")

    @sleep
    @retry(max_retries=3, wait_time=1)
    def _scrap_letter(self, letter_url):
        self.driver.get(letter_url)
        wait = WebDriverWait(self.driver, 3)
        response = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".table_wrapper, .rayanDynamicStatement")
            )
        )
        parsed_response = BeautifulSoup(
            response.get_attribute("innerHTML"), "html.parser"
        )
        letter = []
        for row in parsed_response.find_all("tr"):
            letter.append([cell.text for cell in row.find_all("td")])
        return pd.DataFrame(letter)

    def scrap_letters(
        self,
        store_path,
        stocks=None,
        letters_list_path=None,
        scrape_balance_sheets=True,
        scrape_pnl_sheets=True,
    ):
        balance_sheets_path = os.path.join(store_path, "balance_sheets.csv")
        balance_sheets = self._load_or_create_csv(
            balance_sheets_path, BALANCE_SHEET_COLUMNS + CODAL_BASIC_INFO_COLUMNS
        )
        pnl_path = os.path.join(store_path, "pnl.csv")
        pnl_sheets = self._load_or_create_csv(
            pnl_path, PNL_SHEET_COLUMNS + CODAL_BASIC_INFO_COLUMNS
        )
        if letters_list_path is None:
            letters_list_path = os.path.join(store_path, "letters_list.csv")
            letters_list = self._scrap_letters_list(letters_list_path, stocks)
        letters_list = self._load_or_create_csv(
            letters_list_path, CODAL_LETTERS_LIST_COLUMNS
        )
        for index, row in letters_list.iterrows():
            try:
                if scrape_balance_sheets:
                    if row["tracing_id"] not in balance_sheets.tracing_id.values:
                        letter_df = self._preprocess_balance_sheet_df(
                            self._scrap_letter(
                                row["url"] + f"&sheetId={BALANCE_SHEET_ID}"
                            )
                        )
                        self._add_basic_letter_info(letter_df, row)
                        self._save_csv(letter_df, balance_sheets_path)

            except Exception as e:
                print(e)
                print(row["url"] + f"&sheetId={BALANCE_SHEET_ID}")

            try:
                if scrape_pnl_sheets:
                    if row["tracing_id"] not in pnl_sheets.tracing_id.values:
                        letter_df = self._preprocess_pnl_df(
                            self._scrap_letter(row["url"] + f"&sheetId={PNL_SHEET_ID}")
                        )
                        self._add_basic_letter_info(letter_df, row)
                        self._save_csv(letter_df, pnl_path)
            except Exception as e:
                print(e)
                print(row["url"] + f"&sheetId={PNL_SHEET_ID}")
