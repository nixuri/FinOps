import re
import requests
import concurrent
import pandas as pd
from finops.config import TICKERS_URL, USER_AGENT
from finops.utils.scraper import Scraper
from finops.utils.preprocessor import Preprocessor
from finops.ticker import Ticker


class TehranStockExchange(Scraper, Preprocessor):
    def get_tickers(self) -> pd.DataFrame:
        """
        Retrieves the tickers from Tehran Stock Exchange.

        Returns:
            pd.DataFrame: The tickers data.

        """
        response = self._download(TICKERS_URL, user_agent=USER_AGENT)
        parsed_response = self._parse_html_response(response)
        tickers_df = self._preprocess_tickers_page(parsed_response)
        return tickers_df

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
