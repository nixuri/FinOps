import re
import requests
import concurrent
import pandas as pd
from finops.config import TICKERS_URL, USER_AGENT
from finops.utils.base_scraper import BaseScraper
from finops.ticker import Ticker


class TehranStockExchange(BaseScraper):
    @staticmethod
    def _convert_isin_to_type(isin):
        if re.match(r"^IRO[1357].*0001$", isin):
            return "stock"
        else:
            return "undefined"

    def get_tickers(self):
        response = self._download(TICKERS_URL, user_agent=USER_AGENT)
        parsed_response = self._parse_html_response(response)
        tickers_table = parsed_response.find("table", {"class": "table1"})
        tickers = tickers_table.find_all("tr")
        tickers_data = []
        for ticker in tickers:
            cells = ticker.find_all("td")
            if cells:
                ticker_url = cells[0].find("a")["href"]
                data = {
                    "name": re.findall(r"\(([^()]+)\)", cells[0].text.strip())[0],
                    "full_name": cells[0].text.strip().split("(")[0],
                    "ticker_index": re.findall(r"(\d+)", ticker_url)[-1],
                    "instrument_isin": cells[1].text.strip(),
                    "en_name": cells[2].text.strip(),
                    "code": cells[3].text.strip(),
                    "company_isin": cells[4].text.strip(),
                    "market": cells[5].text.strip(),
                    "section": cells[6].text.strip(),
                    "type": self._convert_isin_to_type(cells[1].text.strip()),
                }
                tickers_data.append(data)

        return pd.DataFrame(tickers_data)

    def get_stock_tickers(self):
        tickers = self.get_tickers()
        stock_tickers = tickers[tickers.type == "stock"]
        return stock_tickers

    def get_stock_tickers_index_list(self):
        stock_tickers_df = self.get_stock_tickers()
        tickers_index_list = stock_tickers_df.ticker_index.tolist()
        return tickers_index_list

    def get_shareholders_data(
        self,
        tickers_index_list,
        start_date,
        end_date,
        store_path,
        log_path,
        n_threads=1,
    ):
        if tickers_index_list is None:
            tickers_index_list = self.get_stock_tickers_index_list()

    def _get_shareholder_data_thread(
        self, ticker_index, start_date, end_date, store_path, log_path
    ):
        Ticker(ticker_index).get_shareholder_data(
            start_date, end_date, store_path, log_path
        )

    def get_shareholders_data(
        self,
        start_date,
        end_date,
        tickers_index_list,
        store_path,
        log_path,
        n_threads=1,
    ):
        if tickers_index_list is None:
            tickers_index_list = self.get_stock_tickers_index_list()
        with concurrent.futures.ThreadPoolExecutor(max_workers=n_threads) as executor:
            futures = [
                executor.submit(
                    self._get_shareholder_data_thread,
                    ticker_index,
                    start_date,
                    end_date,
                    store_path,
                    log_path,
                )
                for ticker_index in tickers_index_list
            ]
            concurrent.futures.wait(futures)
