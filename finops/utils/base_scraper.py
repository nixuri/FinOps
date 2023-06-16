import pandas as pd
from .base_downloader import BaseDownloader


class BaseScraper(BaseDownloader):
    @staticmethod
    def _filter_scraped_dates(traded_dates, scraped_dates):
        not_scraped_dates = list(set(traded_dates) - set(scraped_dates))
        return not_scraped_dates

    @staticmethod
    def _filter_dates_range(dates, start_date, end_date):
        filtered_dates = list(filter(lambda date: start_date < date < end_date, dates))
        return filtered_dates

    @staticmethod
    def _get_ticker_scraped_dates(log, ticker_index):
        return log.loc[log.ticker_index == ticker_index, "date"].tolist()

    def _save_log(self, log_path, ticker_index, date):
        log = pd.DataFrame([{"ticker_index": ticker_index, "date": date}])
        self._save_csv(log, log_path)
