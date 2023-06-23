import re
import requests
import concurrent
import pandas as pd
from finops.config import TICKERS_URL, USER_AGENT
from finops.utils.scraper import Scraper
from finops.ticker import Ticker


class TehranStockExchange(Scraper):
    @staticmethod
    def _convert_isin_to_type(isin: str) -> str:
        """
        Converts ISIN to the corresponding type.

        Args:
            isin (str): The ISIN code.

        Returns:
            str: The corresponding type.

        """
        if re.match(r"^IRO[1357].*0001$", isin):
            return "stock"
        else:
            return "undefined"

    def get_tickers(self) -> pd.DataFrame:
        """
        Retrieves the tickers from Tehran Stock Exchange.

        Returns:
            pd.DataFrame: The tickers data.

        """
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

    def get_stock_tickers(self) -> pd.DataFrame:
        """
        Retrieves the stock tickers.

        Returns:
            pd.DataFrame: The stock tickers.

        """
        tickers = self.get_tickers()
        stock_tickers = tickers[tickers.type == "stock"]
        return stock_tickers

    def get_stock_tickers_index_list(self) -> list:
        """
        Retrieves the list of stock ticker indices.

        Returns:
            list: List of stock ticker indices.

        """
        stock_tickers_df = self.get_stock_tickers()
        tickers_index_list = stock_tickers_df.ticker_index.tolist()
        return tickers_index_list

    def _get_shareholder_data_thread(
        self,
        ticker_index: str,
        start_date: pd.Timestamp,
        end_date: pd.Timestamp,
        store_path: str,
        log_path: str,
    ):
        Ticker(ticker_index).get_shareholder_data(
            start_date, end_date, store_path, log_path
        )

    def get_shareholders_data(
        self,
        start_date: pd.Timestamp,
        end_date: pd.Timestamp,
        store_path: str,
        log_path: str,
        tickers_index_list: list = None,
        n_threads: int = 1,
    ):
        """
        Retrieves and stores the shareholder data for multiple tickers.

        Args:
            start_date (pd.Timestamp): The start date.
            end_date (pd.Timestamp): The end date.
            store_path (str): The path to store the shareholder data.
            log_path (str): The path to store the log data.
            tickers_index_list (list, optional): List of ticker indices. If not provided, stock tickers will be used.
            n_threads (int, optional): The number of threads to use for concurrent execution.

        """
        if tickers_index_list is None:
            tickers_index_list = self.get_stock_tickers_index_list()
        lock = concurrent.futures.Lock()
        with concurrent.futures.ThreadPoolExecutor(max_workers=n_threads) as executor:
            futures = [
                executor.submit(
                    self._get_shareholder_data_thread,
                    ticker_index,
                    start_date,
                    end_date,
                    store_path,
                    log_path,
                    lock,
                )
                for ticker_index in tickers_index_list
            ]
            concurrent.futures.wait(futures)
