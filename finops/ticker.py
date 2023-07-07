import pandas as pd
from finops.config import (
    PRICE_HISTORY_URL,
    SHAREHOLDER_URL,
    SHAREHOLDER_DATA_COLUMNS,
    PRICE_HISTORY_DATA_COLUMNS,
    LOG_COLUMNS,
    USER_AGENT,
    PRICE_HISTORY_FIELD_MAP,
    SHAREHOLDER_FIELD_MAP,
)
from finops.utils.wrappers import catch
from finops.logger import logger
from finops.utils.scraper import Scraper
from finops.utils.preprocessor import Preprocessor


class Ticker(Scraper, Preprocessor):
    def __init__(self, ticker_index: str, *args, **kwargs):
        """
        Initialize a Ticker object.

        :param ticker_index: The ticker index.
        :type ticker_index: str
        """
        super().__init__(*args, **kwargs)
        self.ticker_index = ticker_index

    def get_price_history(self, timeout: float = None) -> pd.DataFrame:
        """
        Retrieves the price history for the ticker.

        :param timeout: Timeout value for the download request.
        :type timeout: float
        :return: The price history data.
        :rtype: pd.DataFrame
        """
        url = PRICE_HISTORY_URL.format(ticker_index=self.ticker_index)
        response = self._download(url, user_agent=USER_AGENT, timeout=timeout)
        parsed_response = self._parse_csv_response(response)
        preprocessed_price_history_data = self._preprocess_price_history_data(
            parsed_response, self.ticker_index
        )
        return preprocessed_price_history_data

    def get_traded_dates(self) -> list:
        """
        Retrieves the traded dates for the ticker.

        :return: List of traded dates.
        :rtype: list
        """
        price_history = self.get_price_history()
        return price_history.date.tolist()

    @catch
    def _get_shareholder_data_one_day(self, date: pd.Timestamp) -> pd.DataFrame:
        """
        Retrieves the shareholder data for a specific date.

        :param date: The date for which to retrieve the shareholder data.
        :type date: pd.Timestamp
        :return: The preprocessed shareholder data.
        :rtype: pd.DataFrame
        """
        url = SHAREHOLDER_URL.format(
            ticker_index=self.ticker_index, date=date.strftime("%Y%m%d")
        )
        response = self._download(url, user_agent=USER_AGENT)
        parsed_response = self._parse_json_response(response)
        preprocessed_shareholder_data = self._preprocess_shareholder_data(
            parsed_response, date, self.ticker_index
        )
        return preprocessed_shareholder_data

    def get_shareholder_data(
        self,
        start_date: pd.Timestamp,
        end_date: pd.Timestamp,
        store_path: str,
        log_path: str,
        verbose: bool = False,
    ):
        """
        Retrieves and stores the shareholder data for a range of dates.

        :param start_date: The start date of the date range.
        :type start_date: pd.Timestamp
        :param end_date: The end date of the date range.
        :type end_date: pd.Timestamp
        :param store_path: The path to store the shareholder data.
        :type store_path: str
        :param log_path: The path to store the log data.
        :type log_path: str
        :param verbose: Flag to enable verbose logging.
        :type verbose: bool
        """
        log = self._load_or_create_csv(
            log_path, LOG_COLUMNS, parse_dates=["date"], dtype={"id": str}
        )
        data = self._load_or_create_csv(store_path, SHAREHOLDER_DATA_COLUMNS)
        traded_dates = self.get_traded_dates()
        scraped_dates = self._get_scraped_dates(log, self.ticker_index)
        not_scraped_dates = self._filter_scraped_dates(traded_dates, scraped_dates)
        filtered_dates = self._filter_dates_range(
            not_scraped_dates, start_date, end_date
        )
        for date in filtered_dates:
            preprocessed_shareholder_data = self._get_shareholder_data_one_day(date)
            self._save_csv(
                preprocessed_shareholder_data,
                store_path,
            )
            self._save_log(log_path=log_path, id=self.ticker_index, date=date)
            if verbose:
                logger.info(f"scraped {self.ticker_index} shareholder data for {date}.")
