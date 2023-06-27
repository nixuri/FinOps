USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"

# Urls
TICKERS_URL = "http://old.tsetmc.com/Loader.aspx?ParTree=151114"
PRICE_HISTORY_URL = (
    "http://old.tsetmc.com/tsev2/data/Export-txt.aspx?t=i&a=1&b=0&i={ticker_index}"
)
SHAREHOLDER_URL = "http://cdn.tsetmc.com/api/Shareholder/{ticker_index}/{date}"
CODAL_SEARCH_BASE_URL = "https://search.codal.ir/api/search/v2/q?"

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
CODAL_LETTERS_LIST_COLUMNS = [
    "tracing_id",
    "symbol",
    "letter_title",
    "url",
]
PNL_SHEET_COLUMNS = [
    "سود (زیان) ناخالص",
    "سود (زیان) عملیاتی",
    "سود (زیان) قبل از کسر مالیات",
    "سود (زیان) خالص",
    "سود (زیان) پایه هر سهم",
    "سود (زیان) خالص هر سهم – ریال",
    "سرمایه",
]
BALANCE_SHEET_COLUMNS = [
    "جمع دارایی‌های جاری",
    "جمع دارایی‌های غیرجاری",
    "جمع دارایی‌ها",
    "جمع بدهی‌های جاری",
    "جمع بدهی‌های غیرجاری",
    "جمع بدهی‌ها",
    "جمع حقوق صاحبان سهام",
    "جمع بدهی‌ها و حقوق صاحبان سهام",
]

CASH_FLOW_SHEET_COLUMNS = [
    "جریان ‌خالص ‌ورود‌ (خروج) ‌نقد حاصل از فعالیت‌های ‌عملیاتی",
    "جریان خالص ورود (خروج) نقد حاصل از فعالیت‌های سرمایه‌گذاری",
    "جریان خالص ورود (خروج) نقد قبل از فعالیت‌های تامین مالی",
    "جریان خالص ورود (خروج) نقد حاصل از فعالیت‌های تامین مالی",
    "خالص افزایش (کاهش) در موجودی نقد",
    "مانده موجودی نقد در ابتدای سال",
    "مانده موجودی نقد در پایان سال",
    "تاثیر تغییرات نرخ ارز",
    "معاملات غیرنقدی",
]

CODAL_BASIC_INFO_COLUMNS = [
    "tracing_id",
    "symbol",
    "is_audited",
    "is_correction",
    "period_end_date",
]
LOG_COLUMNS = [
    "id",
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

BALANCE_SHEET_FIX_MISTAKE_MAP = {
    "جمع داراییهای جاری": "جمع دارایی‌های جاری",
    "جمع داراییهای غیر جاری": "جمع دارایی‌های غیرجاری",
    "جمع داراییها": "جمع دارایی‌ها",
    "جمع بدهیهای جاری": "جمع بدهی‌های جاری",
    "جمع بدهیهای غیر جاری": "جمع بدهی‌های غیرجاری",
    "جمع بدهیهای جاری و غیر جاری": "جمع بدهی‌ها",
    "جمع بدهیها و حقوق صاحبان سهام": "جمع بدهی‌ها و حقوق صاحبان سهام",
    "جمع حقوق مالکانه": "جمع حقوق صاحبان سهام",
    "جمع حقوق مالکانه و بدهی‌ها": "جمع بدهی‌ها و حقوق صاحبان سهام",
    "جمع حقوق سرمایه‌گذاران": "جمع حقوق صاحبان سهام",
    "جمع بدهی‌ها و حقوق سرمایه‌گذاران": "جمع بدهی‌ها و حقوق صاحبان سهام",
    "جمع بدهیها و حقوق مالکانه": "جمع بدهی‌ها و حقوق صاحبان سهام",
    "جمع بدهی ها": "جمع بدهی‌ها",
}

PNL_SHEET_FIX_MISTAKE_MAP = {
    "سود (زیان) خالص هر سهم- ریال": "سود (زیان) خالص هر سهم – ریال",
    "سود (زیان) خالص هر سهم– ریال": "سود (زیان) خالص هر سهم – ریال",
    "درآمدهای عملیاتی": "جمع درآمدهای عملیاتی",
    "بهاى تمام شده درآمدهای عملیاتی": "جمع هزینه های عملیاتی",
    "سود(زیان) عملیاتى": "سود (زیان) عملیاتی",
    "سود(زیان) ناخالص": "سود (زیان) ناخالص",
    "سود(زیان) خالص عملیات در حال تداوم": "سود (زیان) خالص عملیات در حال تداوم",
    "سود(زیان) خالص": "سود (زیان) خالص",
    "سود(زیان) پایه هر سهم": "سود (زیان) پایه هر سهم",
    "سود هر سهم پس از کسر مالیات": "سود (زیان) خالص هر سهم – ریال",
    "سود (زیان) خالص پس از کسر مالیات":  "سود (زیان) خالص",
    "سود(زیان) عملیات در حال تداوم قبل از مالیات": "سود (زیان) قبل از کسر مالیات",
    "سود (زیان) عملیات در حال تداوم قبل از مالیات": "سود (زیان) قبل از کسر مالیات",
    "سود (زیان) قبل از مالیات": "سود (زیان) قبل از کسر مالیات",
    "سود (زیان) ناخالص فعالیتهای بیمه ای": "سود (زیان) ناخالص",
}

CASH_FLOW_FIX_MISTAKE_MAP = {
    "جریان خالص ورود (خروج) وجه نقد ناشی از فعالیت‌های سرمایه‌گذاری": "جریان خالص ورود (خروج) نقد حاصل از فعالیت‌های سرمایه‌گذاری",
}

# CODAL CODES
BALANCE_SHEET_ID = 0
PNL_SHEET_ID = 1
CASH_FLOW_SHEET_ID = 9
