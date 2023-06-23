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


class Ticker(Scraper):
    def __init__(self, ticker_index: str, *args, **kwargs):
        """
        Initialize a Ticker object.

        Args:
            ticker_index (str): The ticker index.

        """
        super().__init__(*args, **kwargs)
        self.ticker_index = ticker_index

    def _preprocess_shareholder_data(
        self, parsed_response: dict, date: pd.Timestamp
    ) -> pd.DataFrame:
        """
        Preprocesses the shareholder data.

        Args:
            parsed_response (dict): The parsed response containing shareholder data.
            date (pd.Timestamp): The date of the shareholder data.

        Returns:
            pd.DataFrame: The preprocessed shareholder data.

        """
        preprocessed_response = parsed_response["shareShareholder"]
        if len(preprocessed_response) == 0:
            return pd.DataFrame(columns=SHAREHOLDER_DATA_COLUMNS)

        preprocessed_response = (
            pd.DataFrame(preprocessed_response)
            .rename(columns=SHAREHOLDER_FIELD_MAP)
            .assign(ticker_index=self.ticker_index)
            .assign(req_date=date)
            .drop(["change", "change_amount"], axis=1)
        )
        preprocessed_response["date"] = pd.to_datetime(
            preprocessed_response["date"], format="%Y%m%d"
        )

        return preprocessed_response

    def get_price_history(self, timeout: float = None) -> pd.DataFrame:
        """
        Retrieves the price history for the ticker.

        Args:
            timeout (float): Timeout value for the download request.

        Returns:
            pd.DataFrame: The price history data.

        """
        url = PRICE_HISTORY_URL.format(ticker_index=self.ticker_index)
        response = self._download(url, user_agent=USER_AGENT, timeout=timeout)
        parsed_response = self._parse_csv_response(response)
        ticker_price_history = (
            parsed_response.rename(columns=PRICE_HISTORY_FIELD_MAP)
            .drop("per", axis=1)
            .assign(ticker_index=self.ticker_index)
            .assign(date=lambda df: pd.to_datetime(df["date"], format="%Y%m%d"))
        )
        return ticker_price_history

    def get_traded_dates(self) -> list:
        """
        Retrieves the traded dates for the ticker.

        Returns:
            list: List of traded dates.

        """
        price_history = self.get_price_history()
        return price_history.date.tolist()

    @catch
    def _get_shareholder_data_one_day(self, date: pd.Timestamp) -> pd.DataFrame:
        """
        Retrieves the shareholder data for a specific date.

        Args:
            date (pd.Timestamp): The date for which to retrieve the shareholder data.

        Returns:
            pd.DataFrame: The preprocessed shareholder data.

        """
        url = SHAREHOLDER_URL.format(
            ticker_index=self.ticker_index, date=date.strftime("%Y%m%d")
        )
        response = self._download(url, user_agent=USER_AGENT)
        parsed_response = self._parse_json_response(response)
        return self._preprocess_shareholder_data(parsed_response, date)

    def get_shareholder_data(
        self,
        start_date: pd.Timestamp,
        end_date: pd.Timestamp,
        store_path: str,
        log_path: str,
        lock=None,
        verbose: bool = False,
    ):
        """
        Retrieves and stores the shareholder data for a range of dates.

        Args:
            start_date (pd.Timestamp): The start date of the date range.
            end_date (pd.Timestamp): The end date of the date range.
            store_path (str): The path to store the shareholder data.
            log_path (str): The path to store the log data.
            lock (Optional[threading.Lock]): Optional lock for thread safety.
            verbose (bool): Flag to enable verbose logging.

        """
        log = self._load_or_create_csv(
            log_path, LOG_COLUMNS, parse_dates=["date"], dtype={"ticker_index": str}
        )
        data = self._load_or_create_csv(store_path, SHAREHOLDER_DATA_COLUMNS)
        traded_dates = self.get_traded_dates()
        scraped_dates = self._get_ticker_scraped_dates(log, self.ticker_index)
        not_scraped_dates = self._filter_scraped_dates(traded_dates, scraped_dates)
        filtered_dates = self._filter_dates_range(
            not_scraped_dates, start_date, end_date
        )
        for date in filtered_dates:
            preprocessed_shareholder_data = self._get_shareholder_data_one_day(date)
            if preprocessed_shareholder_data is not None:
                if lock is not None:
                    with lock:
                        self._save_csv(
                            preprocessed_shareholder_data,
                            store_path,
                        )
                        self._save_log(log_path, self.ticker_index, date)
                else:
                    self._save_csv(
                        preprocessed_shareholder_data,
                        store_path,
                    )
                    self._save_log(log_path, self.ticker_index, date)
                if verbose:
                    logger.info(
                        f"scraped {self.ticker_index} shareholder data for {date}."
                    )
