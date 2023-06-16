import os
import pandas as pd
import requests
import unittest
from unittest.mock import patch, Mock
from io import StringIO
from finops.utils.base_downloader import BaseDownloader


class TestBaseDownloader(unittest.TestCase):
    def setUp(self):
        self.columns = ["col1", "col2", "col3"]
        self.path = "test.csv"
        self.url = "http://cdn.tsetmc.com/api/Shareholder/65883838195688438/20230522"
        self.user_agent = "Mozilla/5.0"
        self.timeout = (1, 1)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_create_csv_file_existing_file(self):
        pd.DataFrame(columns=self.columns).to_csv(self.path, index=False)
        with patch("pandas.read_csv") as mock_read_csv:
            mock_read_csv.return_value.columns.tolist.return_value = self.columns
            BaseDownloader._create_csv_file(self.path, self.columns)
            mock_read_csv.assert_called_once_with(self.path, nrows=0)
        self.assertTrue(os.path.exists(self.path))

    def test_create_csv_file_new_file(self):
        BaseDownloader._create_csv_file(self.path, self.columns)
        self.assertTrue(os.path.exists(self.path))
        df = pd.read_csv(self.path)
        self.assertListEqual(df.columns.tolist(), self.columns)

    @patch("requests.get")
    def test_download(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        response = BaseDownloader._download(self.url, self.user_agent, self.timeout)
        mock_get.assert_called_once_with(
            self.url, headers={"user-agent": self.user_agent}, timeout=self.timeout
        )
        mock_response.raise_for_status.assert_called_once_with()
        self.assertEqual(response, mock_response)

    def test_parse_json_response(self):
        response = Mock()
        response.content.decode.return_value = '{"key": "value"}'
        parsed_response = BaseDownloader._parse_json_response(response)
        self.assertDictEqual(parsed_response, {"key": "value"})

    def test_parse_csv_response(self):
        response = Mock()
        response.content.decode.return_value = "col1,col2,col3\n1,2,3\n4,5,6\n"
        parsed_response = BaseDownloader._parse_csv_response(response)
        expected_df = pd.DataFrame({"col1": [1, 4], "col2": [2, 5], "col3": [3, 6]})
        pd.testing.assert_frame_equal(parsed_response, expected_df)

    def test_store_existing_file(self):
        existing_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4], "col3": [5, 6]})
        existing_df.to_csv(
            self.path, index=False, mode="w", header=True
        )
        new_df = pd.DataFrame({"col1": [7, 8], "col2": [9, 10], "col3": [11, 12]})
        BaseDownloader._save_csv(new_df, self.path)
        stored_df = pd.read_csv(self.path)
        expected_df = pd.concat([existing_df, new_df], ignore_index=True)
        pd.testing.assert_frame_equal(stored_df, expected_df)
