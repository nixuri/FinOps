import pandas as pd
from .downloader import Downloader


class Scraper(Downloader):
    @staticmethod
    def _filter_scraped_dates(dates, scraped_dates):
        not_scraped_dates = list(set(dates) - set(scraped_dates))
        return not_scraped_dates

    @staticmethod
    def _filter_dates_range(dates, start_date, end_date):
        filtered_dates = list(filter(lambda date: start_date < date < end_date, dates))
        return filtered_dates

    @staticmethod
    def _get_scraped_dates(log, id, date_column="date"):
        return log.loc[log.id == id, date_column].tolist()
    
    @staticmethod
    def _get_scraped_ids(log, id_column="id"):
        return log[id_column].tolist()

    @staticmethod
    def _save_log(log_path, **logargs):
        log = pd.DataFrame([logargs])
        self._save_csv(log, log_path)
