import io
import os
import json
import requests
import pandas as pd
from .wrappers import lock
from bs4 import BeautifulSoup


class BaseDownloader:
    @staticmethod
    def _create_csv_file(path, columns):
        if os.path.isfile(path):
            existing_columns = pd.read_csv(path, nrows=0).columns.tolist()
            if existing_columns != columns:
                raise ValueError(
                    f"Columns in the {path} do not match the specified columns."
                )
        else:
            directory = os.path.dirname(path)
            if directory:
                os.makedirs(directory, exist_ok=True)
            pd.DataFrame(columns=columns).to_csv(path, index=False)

    @staticmethod
    def _download(url, user_agent, timeout=None):
        response = requests.get(
            url,
            headers={"user-agent": user_agent},
            timeout=timeout,
        )
        response.raise_for_status()
        return response

    @staticmethod
    def _parse_json_response(response):
        return json.loads(response.content.decode("utf8"))

    @staticmethod
    def _parse_csv_response(response):
        return pd.read_csv(io.StringIO(response.content.decode("utf8")))

    @staticmethod
    def _parse_html_response(response):
        return BeautifulSoup(response.text, "html.parser")

    def _load_or_create_csv(self, path, columns, **kwargs):
        self._create_csv_file(path, columns=columns)
        return pd.read_csv(path, **kwargs)

    @staticmethod
    @lock
    def _save_csv(data, path):
        data.to_csv(path, index=False, mode="a", header=False)
