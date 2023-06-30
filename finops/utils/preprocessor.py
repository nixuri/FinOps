import re
import pandas as pd
import jdatetime
from finops.config import (
    PRICE_HISTORY_URL,
    SHAREHOLDER_URL,
    SHAREHOLDER_DATA_COLUMNS,
    PRICE_HISTORY_DATA_COLUMNS,
    LOG_COLUMNS,
    USER_AGENT,
    PRICE_HISTORY_FIELD_MAP,
    SHAREHOLDER_FIELD_MAP,
    BALANCE_SHEET_COLUMNS,
    PNL_SHEET_COLUMNS,
    CASH_FLOW_SHEET_COLUMNS,
    BALANCE_SHEET_FIX_MISTAKE_MAP,
    PNL_SHEET_FIX_MISTAKE_MAP,
    CASH_FLOW_FIX_MISTAKE_MAP,
)


class Preprocessor:
    @staticmethod
    def _convert_isin_to_type(isin: str) -> str:
        """
        Converts ISIN to the corresponding type.

        Args:
            isin (str): The ISIN code.

        Returns:
            str: The corresponding type.

        """
        if re.match(r"^IRO[1357].*0001$", isin):
            return "stock"
        else:
            return "undefined"

    def _preprocess_tickers_page(self, parsed_response):
        tickers_table = parsed_response.find("table", {"class": "table1"})
        tickers = tickers_table.find_all("tr")
        tickers_data = []
        for ticker in tickers:
            cells = ticker.find_all("td")
            if cells:
                ticker_url = cells[0].find("a")["href"]
                data = {
                    "name": self._preprocess_ticker_name(
                        re.findall(r"\(([^()]+)\)", cells[0].text.strip())[0]
                    ),
                    "full_name": cells[0].text.strip().split("(")[0],
                    "ticker_index": re.findall(r"(\d+)", ticker_url)[-1],
                    "instrument_isin": cells[1].text.strip(),
                    "en_name": cells[2].text.strip(),
                    "code": cells[3].text.strip(),
                    "company_isin": cells[4].text.strip(),
                    "market": cells[5].text.strip(),
                    "section": cells[6].text.strip(),
                    "type": self._convert_isin_to_type(cells[1].text.strip()),
                }
                tickers_data.append(data)
        return pd.DataFrame(tickers_data)

    @staticmethod
    def _preprocess_shareholder_data(parsed_response, req_date, ticker_index):
        preprocessed_shareholder_data = parsed_response["shareShareholder"]
        if len(preprocessed_shareholder_data) == 0:
            return pd.DataFrame(columns=SHAREHOLDER_DATA_COLUMNS)
        else:
            preprocessed_shareholder_data = (
                pd.DataFrame(preprocessed_shareholder_data)
                .rename(columns=SHAREHOLDER_FIELD_MAP)
                .assign(ticker_index=ticker_index)
                .assign(req_date=req_date)
                .assign(date=lambda df: pd.to_datetime(df["date"], format="%Y%m%d"))
                .drop(["change", "change_amount"], axis=1)
            )
        return preprocessed_shareholder_data

    @staticmethod
    def _preprocess_price_history_data(parsed_response, ticker_index):
        preprocessed_price_history = (
            parsed_response.rename(columns=PRICE_HISTORY_FIELD_MAP)
            .drop("per", axis=1)
            .assign(ticker_index=ticker_index)
            .assign(date=lambda df: pd.to_datetime(df["date"], format="%Y%m%d"))
        )
        return preprocessed_price_history

    @staticmethod
    def _preprocess_persian_text(text):
        if text is None:
            return None

        text = text.replace("ي", "ی")
        text = text.replace("ك", "ک")
        text = text.replace("أ", "ا")

        digits_mapping = {
            "۰": "0",
            "۱": "1",
            "۲": "2",
            "۳": "3",
            "۴": "4",
            "۵": "5",
            "۶": "6",
            "۷": "7",
            "۸": "8",
            "۹": "9",
        }
        for digit, replacement in digits_mapping.items():
            text = text.replace(digit, replacement)
        return text

    def _preprocess_ticker_name(self, ticker_name):
        ticker_name = self._preprocess_persian_text(ticker_name)
        if ticker_name is None:
            return None
        ticker_name = ticker_name.replace("\u200c", "")
        return ticker_name

    def _preprocess_codal_text(self, text):
        text = self._preprocess_persian_text(text)
        if text is None:
            return None
        text = text.replace(",", "")
        text = text.replace("--", "")
        text = re.sub("\u200c+", "\u200c", text)
        text = re.sub("[\n\t\r]", "", text)
        text = re.sub(r"\((\d+)\)", r"-\1", text)
        text = re.sub(" +", " ", text)
        text = text.strip()

        if text == "":
            return None

        return text

    @staticmethod
    def safe_select_columns(df, columns):
        selected_columns = []
        for column in columns:
            try:
                selected_columns.append(df.loc[:, column])
            except KeyError:
                selected_columns.append(pd.Series(dtype="object", name=column))
        return pd.concat(selected_columns, axis=1)

    def _preprocess_balance_sheet_df(self, df):
        df = df.applymap(self._preprocess_codal_text)
        if len(df.columns) == 12:
            df = df.iloc[:, 1:3]
        if len(df.columns) == 10:
            df = df.drop(columns=[0, 5])
        if len(df.columns) < 5:
            df = df.iloc[:, :2]
        else:
            section1 = df.iloc[:, 0:2]
            section2 = df.iloc[:, 4:6]
            section2.columns = section1.columns
            df = pd.concat([section1, section2], axis=0, ignore_index=True)
        df = df.dropna(how="any")
        df.columns = ["title", "value"]
        df["title"] = df["title"].map(BALANCE_SHEET_FIX_MISTAKE_MAP).fillna(df["title"])
        df = df.drop_duplicates(subset=["title"], keep="first")
        df = df[df["title"].isin(BALANCE_SHEET_COLUMNS)]
        df = df.set_index("title").T.reset_index(drop=True)
        df = self.safe_select_columns(df, BALANCE_SHEET_COLUMNS)
        return df

    def _preprocess_pnl_df(self, df):
        df = df.applymap(self._preprocess_codal_text)
        if len(df.columns) == 24:
            df = df.iloc[:, 3:5]
        if len(df.columns) == 12:
            df = df.iloc[:, 1:3]
        if len(df.columns) == 5:
            df = df.drop(columns=[0])
        df = df.iloc[:, :2]
        df = df.dropna(how="any")
        df.columns = ["title", "value"]
        df["title"] = df["title"].map(PNL_SHEET_FIX_MISTAKE_MAP).fillna(df["title"])
        df = df.drop_duplicates(subset=["title"], keep="first")
        df = df[df["title"].isin(PNL_SHEET_COLUMNS)]
        df = df.set_index("title").T.reset_index(drop=True)
        df = self.safe_select_columns(df, PNL_SHEET_COLUMNS)
        return df

    def _preprocess_cash_flow_df(self, df):
        df = df.applymap(self._preprocess_codal_text)
        if len(df.columns) == 12:
            df = df.iloc[:, 1:3]
        df = df.iloc[:, :2]
        df = df.dropna(how="any")
        df.columns = ["title", "value"]
        df["title"] = df["title"].map(CASH_FLOW_FIX_MISTAKE_MAP).fillna(df["title"])
        df = df.drop_duplicates(subset=["title"], keep="first")
        df = df[df["title"].isin(CASH_FLOW_SHEET_COLUMNS)]
        df = df.set_index("title").T.reset_index(drop=True)
        df = self.safe_select_columns(df, CASH_FLOW_SHEET_COLUMNS)
        return df

    @staticmethod
    def _preprocess_letters_list(parsed_response):
        letters = parsed_response["Letters"]
        letters_list = []
        for letter in letters:
            letters_list.append(
                {
                    "tracing_id": letter["TracingNo"],
                    "symbol": letter["Symbol"],
                    "letter_title": letter["Title"],
                    "url": "https://www.codal.ir" + letter["Url"],
                }
            )
        letters_list_df = pd.DataFrame(letters_list)
        return letters_list_df

    @staticmethod
    def _add_basic_letter_info(letter_df, info):
        letter_df["tracing_id"] = info["tracing_id"]
        letter_df["symbol"] = info["symbol"]
        letter_df["is_audited"] = "حسابرسی شده" in info["letter_title"]
        letter_df["is_correction"] = "اصلاحیه" in info["letter_title"]
        letter_df["is_consolidated"] = "تلفیقی" in info["letter_title"]
        letter_df["period_type"] = re.search(
            r"(سال مالی|میاندوره‌ای)", info["letter_title"]
        ).group()

        letter_df["period_length"] = (
            re.search(r"\d+(?= ماهه)", info["letter_title"]).group()
            if re.search(r"\d+(?= ماهه)", info["letter_title"])
            else None
        )
        letter_df["period_end_date"] = (
            jdatetime.datetime.strptime(
                re.search(r"\d{4}/\d{2}/\d{2}", info["letter_title"]).group(),
                "%Y/%m/%d",
            )
            .date()
            .togregorian()
        )
        return letter_df
