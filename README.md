# FinOps

FinOps is a python package for financial operations.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install finops.

```pip install finops```

## Usage
```
import finops
import datetime

ticker = finops.Ticker("778253364357513")
ticker.get_price_history()


tse = finops.TehranStockExchange()
tse.get_shareholders_data(start_date=datetime(2020, 1, 1), end_date=datetime(2023, 1, 1))
```

## Contributing

Contributions are always welcome!