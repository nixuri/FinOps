USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"

# Urls
TICKERS_URL = "http://old.tsetmc.com/Loader.aspx?ParTree=151114"
PRICE_HISTORY_URL = (
    "http://old.tsetmc.com/tsev2/data/Export-txt.aspx?t=i&a=1&b=0&i={ticker_index}"
)
SHAREHOLDER_URL = "http://cdn.tsetmc.com/api/Shareholder/{ticker_index}/{date}"

# Columns
PRICE_HISTORY_DATA_COLUMNS = [
    "en_ticker",
    "date",
    "first",
    "high",
    "low",
    "close",
    "value",
    "volume",
    "open_int",
    "per",
    "open",
    "last",
]
SHAREHOLDER_DATA_COLUMNS = [
    "shareholder_id",
    "shareholder_name",
    "isin",
    "date",
    "n_shares",
    "per_shares",
    "ticker_index",
    "req_date",
]
LOG_COLUMNS = [
    "ticker_index",
    "date",
]

# Field maps
PRICE_HISTORY_FIELD_MAP = {
    "<TICKER>": "en_ticker",
    "<DTYYYYMMDD>": "date",
    "<FIRST>": "first",
    "<HIGH>": "high",
    "<LOW>": "low",
    "<CLOSE>": "close",
    "<VALUE>": "value",
    "<VOL>": "volume",
    "<OPENINT>": "open_int",
    "<PER>": "per",
    "<OPEN>": "open",
    "<LAST>": "last",
}

SHAREHOLDER_FIELD_MAP = {
    "shareHolderID": "shareholder_id",
    "shareHolderName": "shareholder_name",
    "cIsin": "isin",
    "dEven": "date",
    "numberOfShares": "n_shares",
    "perOfShares": "per_shares",
    "change": "change",
    "changeAmount": "change_amount",
}
