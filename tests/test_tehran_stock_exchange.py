import unittest
import pandas as pd
from finops.tehran_stock_exchange import TehranStockExchange


class TehranStockExchangeTests(unittest.TestCase):
    def setUp(self):
        self.scraper = TehranStockExchange()

    def test_get_tickers(self):
        result = self.scraper.get_tickers()
        expected_result = pd.DataFrame(
            [
                {
                    "name": "مظنه",
                    "full_name": "مظنه پذيره نويسي اوراق دولتي ",
                    "ticker_index": "70967527013451633",
                    "instrument_isin": "IRB1QM020001",
                    "en_name": "Quotes 02",
                    "code": "QM02",
                    "company_isin": "IRB1QM020003",
                    "market": "-",
                    "section": "اوراق تامين مالي",
                    "type": "undefined",
                }
            ]
        )
        pd.testing.assert_frame_equal(result.iloc[0, :].to_frame(), expected_result.iloc[0, :].to_frame())

    def test_convert_isin_to_type_stock(self):
        result = self.scraper._convert_isin_to_type("IRO12300001")
        self.assertEqual(result, "stock")

    def test_convert_isin_to_type_undefined(self):
        result = self.scraper._convert_isin_to_type("IRO99900001")
        self.assertEqual(result, "undefined")

    def test_get_stock_tickers(self):
        self.scraper.get_tickers = lambda: pd.DataFrame(
            [
                {
                    "name": "Name 1",
                    "full_name": "Full Name 1",
                    "ticker_index": "ticker_url_1",
                    "instrument_isin": "IRO12300001",
                    "en_name": "en_name_1",
                    "code": "code_1",
                    "company_isin": "company_isin_1",
                    "market": "market_1",
                    "section": "section_1",
                    "type": "stock",
                },
                {
                    "name": "Name 2",
                    "full_name": "Full Name 2",
                    "ticker_index": "ticker_url_2",
                    "instrument_isin": "IRO99900001",
                    "en_name": "en_name_2",
                    "code": "code_2",
                    "company_isin": "company_isin_2",
                    "market": "market_2",
                    "section": "section_2",
                    "type": "other",
                },
            ]
        )

        result = self.scraper.get_stock_tickers()
        expected_result = pd.DataFrame(
            [
                {
                    "name": "Name 1",
                    "full_name": "Full Name 1",
                    "ticker_index": "ticker_url_1",
                    "instrument_isin": "IRO12300001",
                    "en_name": "en_name_1",
                    "code": "code_1",
                    "company_isin": "company_isin_1",
                    "market": "market_1",
                    "section": "section_1",
                    "type": "stock",
                }
            ]
        )
        pd.testing.assert_frame_equal(result, expected_result)

    def test_get_stock_tickers_index_list(self):
        self.scraper.get_tickers = lambda: pd.DataFrame(
            [
                {"ticker_index": "ticker_url_1", "type": "stock"},
                {"ticker_index": "ticker_url_2", "type": "other"},
                {"ticker_index": "ticker_url_3", "type": "stock"},
            ]
        )

        result = self.scraper.get_stock_tickers_index_list()
        expected_result = ["ticker_url_1", "ticker_url_3"]
        self.assertEqual(result, expected_result)
