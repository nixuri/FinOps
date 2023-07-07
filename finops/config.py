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
    "is_audited",
    "is_correction",
    "is_consolidated",
    "period_type",
    "period_length",
    "period_end_date",
    "url",
]

PNL_SHEET_COLUMNS = [
    "gross_profit",
    "operating_profit",
    "pre_tax_profit",
    "net_profit",
    "basic_earnings_per_share",
    "net_earnings_per_share",
    "capital",
    "tracing_id",
]

BALANCE_SHEET_COLUMNS = [
    "total_current_assets",
    "total_noncurrent_assets",
    "total_assets",
    "total_current_liabilities",
    "total_noncurrent_liabilities",
    "total_liabilities",
    "total_equity",
    "total_liabilities_and_equity",
    "tracing_id",
]

CASH_FLOW_SHEET_COLUMNS = [
    "net_cash_flow_operational",
    "net_cash_flow_investment",
    "net_cash_flow_financing",
    "net_change_in_cash",
    "cash_balance_beginning_year",
    "cash_balance_end_year",
    "effect_exchange_rate_changes",
    "non_cash_transactions",
    "tracing_id",
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
    "جمع داراییهای جاری": "total_current_assets",
    "جمع داراییهای غیر جاری": "total_noncurrent_assets",
    "جمع داراییها": "total_assets",
    "جمع بدهیهای جاری": "total_current_liabilities",
    "جمع بدهیهای غیر جاری": "total_noncurrent_liabilities",
    "جمع بدهیهای جاری و غیر جاری": "total_liabilities",
    "جمع بدهیها و حقوق صاحبان سهام": "total_liabilities_and_equity",
    "جمع حقوق مالکانه و بدهی‌ها": "total_liabilities_and_equity",
    "جمع بدهی‌ها و حقوق سرمایه‌گذاران": "total_liabilities_and_equity",
    "جمع بدهیها و حقوق مالکانه": "total_liabilities_and_equity",
    "جمع حقوق مالکانه": "total_equity",
    "جمع حقوق سرمایه‌گذاران": "total_equity",
    "جمع بدهی ها": "total_liabilities",
    "جمع دارایی‌های جاری": "total_current_assets",
    "جمع دارایی‌های غیرجاری": "total_noncurrent_assets",
    "جمع دارایی‌ها": "total_assets",
    "جمع بدهی‌های جاری": "total_current_liabilities",
    "جمع بدهی‌های غیرجاری": "total_noncurrent_liabilities",
    "جمع بدهی‌ها": "total_liabilities",
    "جمع حقوق صاحبان سهام": "total_equity",
    "جمع بدهی‌ها و حقوق صاحبان سهام": "total_liabilities_and_equity",
}

PNL_SHEET_FIX_MISTAKE_MAP = {
    "سود (زیان) خالص هر سهم- ریال": "net_earnings_per_share",
    "سود (زیان) خالص هر سهم– ریال": "net_earnings_per_share",
    "سود(زیان) عملیاتى": "operating_profit",
    "سود(زیان) ناخالص": "gross_profit",
    "سود(زیان) خالص": "net_profit",
    "سود(زیان) پایه هر سهم": "basic_earnings_per_share",
    "سود هر سهم پس از کسر مالیات": "net_earnings_per_share",
    "سود (زیان) خالص پس از کسر مالیات": "net_profit",
    "سود(زیان) عملیات در حال تداوم قبل از مالیات": "pre_tax_profit",
    "سود (زیان) عملیات در حال تداوم قبل از مالیات": "pre_tax_profit",
    "سود (زیان) قبل از مالیات": "pre_tax_profit",
    "سود (زیان) ناخالص فعالیتهای بیمه ای": "gross_profit",
    "سود (زیان) ناخالص": "gross_profit",
    "سود (زیان) عملیاتی": "operating_profit",
    "سود (زیان) قبل از کسر مالیات": "pre_tax_profit",
    "سود (زیان) خالص": "net_profit",
    "سود (زیان) پایه هر سهم": "basic_earnings_per_share",
    "سود (زیان) خالص هر سهم – ریال": "net_earnings_per_share",
    "سرمایه": "capital",
}

CASH_FLOW_FIX_MISTAKE_MAP = {
    "جریان خالص ورود (خروج) وجه نقد ناشی از فعالیت‌های سرمایه‌گذاری": "net_cash_flow_investment",
    "جریان خالص ورود (خروج) وجه نقد ناشی از فعالیت‌های عملیاتی": "net_cash_flow_operational",
    "جریان خالص ورود (خروج) وجه نقد ناشی از فعالیت‌های تامین مالی": "net_cash_flow_financing",
    "موجودی نقد در ابتدای دوره": "cash_balance_beginning_year",
    "تآثیر تغییرات نرخ ارز": "effect_exchange_rate_changes",
    "موجودی نقد در پایان دوره": "cash_balance_end_year",
    "مبادلات غیرنقدی": "non_cash_transactions",
    "جریان ‌خالص ‌ورود‌ (خروج) ‌نقد حاصل از فعالیت‌های ‌عملیاتی": "net_cash_flow_operational",
    "جریان خالص ورود (خروج) نقد حاصل از فعالیت‌های سرمایه‌گذاری": "net_cash_flow_investment",
    "جریان خالص ورود (خروج) نقد حاصل از فعالیت‌های تامین مالی": "net_cash_flow_financing",
    "خالص افزایش (کاهش) در موجودی نقد": "net_change_in_cash",
    "مانده موجودی نقد در ابتدای سال": "cash_balance_beginning_year",
    "مانده موجودی نقد در پایان سال": "cash_balance_end_year",
    "تاثیر تغییرات نرخ ارز": "effect_exchange_rate_changes",
    "معاملات غیرنقدی": "non_cash_transactions",
}

# CODAL CODES
BALANCE_SHEET_ID = 0
PNL_SHEET_ID = 1
CASH_FLOW_SHEET_ID = 9
