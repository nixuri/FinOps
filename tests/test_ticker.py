import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
import pandas as pd
from finops.ticker import Ticker
from finops.config import (
    SHAREHOLDER_URL,
    PRICE_HISTORY_URL,
    PRICE_HISTORY_DATA_COLUMNS,
    SHAREHOLDER_DATA_COLUMNS,PRICE_HISTORY_FIELD_MAP, SHAREHOLDER_FIELD_MAP
)


class TestTicker(unittest.TestCase):
    def setUp(self):
        self.ticker_index = "2400322364771558"
        self.ticker = Ticker(self.ticker_index)

    def test_preprocess_shareholder_data(self):
        parsed_response = {
            "shareShareholder": [
                {
                    "shareholder_id": 1,
                    "shareholder_name": "John Doe",
                    "isin": "ABC123",
                    "date": "20210601",
                    "n_shares": 1000,
                    "per_shares": 10.5,
                    "change": 0.05,
                    "change_amount": 50,
                },
                {
                    "shareholder_id": 2,
                    "shareholder_name": "Jane Smith",
                    "isin": "DEF456",
                    "date": "20210602",
                    "n_shares": 2000,
                    "per_shares": 15.25,
                    "change": 0.1,
                    "change_amount": 100,
                },
            ]
        }
        date = datetime(2021, 6, 1)

        expected_result = pd.DataFrame(
            {
                "shareholder_id": [1, 2],
                "shareholder_name": ["John Doe", "Jane Smith"],
                "isin": ["ABC123", "DEF456"],
                "date": pd.to_datetime(["20210601", "20210602"], format="%Y%m%d"),
                "n_shares": [1000, 2000],
                "per_shares": [10.5, 15.25],
                "ticker_index": self.ticker_index,
                "req_date": datetime(2021, 6, 1),
            }
        )

        result = self.ticker._preprocess_shareholder_data(
            parsed_response, date
        )
        pd.testing.assert_frame_equal(result, expected_result)

    def test_get_price_history(self):
        price_history = self.ticker.get_price_history()
        self.assertIsInstance(price_history, pd.DataFrame)
        expected_columns = [
            "en_ticker",
            "date",
            "first",
            "high",
            "low",
            "close",
            "value",
            "volume",
            "open_int",
            "open",
            "last",
            "ticker_index",
        ]
        self.assertListEqual(list(price_history.columns), expected_columns)
        self.assertEqual(price_history["ticker_index"].unique(), [self.ticker_index])

    def test_get_shareholder_data_one_day(self):
        date = datetime(2023, 5, 22)
        result = self.ticker.get_shareholder_data_one_day(date)
        expected_result = pd.DataFrame(
            [
                {
                    "shareholder_id": 99,
                    "shareholder_name": "سازمان تامين اجتماعي",
                    "isin": "IRO1TAMN0006",
                    "date": datetime(2023, 5, 23),
                    "n_shares": 1408441000222.0,
                    "per_shares": 86.08,
                    "ticker_index": "2400322364771558",
                    "req_date": datetime(2023, 5, 22),
                },
                {
                    "shareholder_id": 77171,
                    "shareholder_name": "شركت واسط مالي مهر-بامسئوليت محدود-",
                    "isin": "IRO1TAMN0006",
                    "date": datetime(2023, 5, 23),
                    "n_shares": 43811610077.0,
                    "per_shares": 2.67,
                    "ticker_index": "2400322364771558",
                    "req_date": datetime(2023, 5, 22),
                },
                {
                    "shareholder_id": 99,
                    "shareholder_name": "سازمان تامين اجتماعي",
                    "isin": "IRO1TAMN0006",
                    "date": datetime(2023, 5, 22),
                    "n_shares": 1408441000222.0,
                    "per_shares": 86.08,
                    "ticker_index": "2400322364771558",
                    "req_date": datetime(2023, 5, 22),
                },
                {
                    "shareholder_id": 77171,
                    "shareholder_name": "شركت واسط مالي مهر-بامسئوليت محدود-",
                    "isin": "IRO1TAMN0006",
                    "date": datetime(2023, 5, 22),
                    "n_shares": 43811610077.0,
                    "per_shares": 2.67,
                    "ticker_index": "2400322364771558",
                    "req_date": datetime(2023, 5, 22),
                },
            ]
        )
        self.assertIsInstance(result, pd.DataFrame)
        pd.testing.assert_frame_equal(result, expected_result)

    def test_get_traded_dates(self):
        traded_dates = self.ticker.get_traded_dates()
        self.assertIsInstance(traded_dates, list)
        self.assertTrue(all(isinstance(date, datetime) for date in traded_dates))