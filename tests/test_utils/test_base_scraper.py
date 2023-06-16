import unittest
import pandas as pd
from datetime import date
from finops.utils.base_scraper import BaseScraper


class TestBaseScraper(unittest.TestCase):
    def setUp(self):
        self.traded_dates = [
            date(2022, 1, 1),
            date(2022, 1, 2),
            date(2022, 1, 3),
            date(2022, 1, 4),
            date(2022, 1, 5),
        ]
        self.scraped_dates = [
            date(2022, 1, 1),
            date(2022, 1, 3),
            date(2022, 1, 5),
        ]
        self.start_date = date(2022, 1, 2)
        self.end_date = date(2022, 1, 4)
        self.log = pd.DataFrame(
            {
                "ticker_index": [0, 0, 0, 1, 1, 2],
                "date": [
                    date(2022, 1, 1),
                    date(2022, 1, 2),
                    date(2022, 1, 3),
                    date(2022, 1, 2),
                    date(2022, 1, 3),
                    date(2022, 1, 4),
                ],
            }
        )

    def test_filter_scraped_dates(self):
        not_scraped_dates = BaseScraper._filter_scraped_dates(
            self.traded_dates, self.scraped_dates
        )
        expected_dates = [date(2022, 1, 2), date(2022, 1, 4)]
        self.assertListEqual(not_scraped_dates, expected_dates)

    def test_filter_dates_range(self):
        filtered_dates = BaseScraper._filter_dates_range(
            self.traded_dates, self.start_date, self.end_date
        )
        expected_dates = [date(2022, 1, 3)]
        self.assertListEqual(filtered_dates, expected_dates)

    def test_get_ticker_scraped_dates(self):
        ticker_index = 0
        scraped_dates = BaseScraper._get_ticker_scraped_dates(
            self.log, ticker_index
        )
        expected_dates = [date(2022, 1, 1), date(2022, 1, 2), date(2022, 1, 3)]
        self.assertListEqual(list(scraped_dates), expected_dates)