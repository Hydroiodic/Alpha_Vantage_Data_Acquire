# import nessarary libraries
from constants import symbols_filename, query_symbols_url
from typing import List
import requests
import pickle
import os


def get_all_symbols() -> List[str]:
    """
    This is a function to get all symbols on AlphaVantage.
    If there's a file saved before, we just load from the file directly.
    """
    # check if there's the cached file
    if os.path.exists(symbols_filename):
        with open(symbols_filename, "rb") as file_handle:
            return pickle.load(file_handle)

    # using requests library to fetch .csv file with regard to symbols
    response = requests.get(query_symbols_url)
    if response != None and response.status_code == 200:
        us_stock_data = response.text
        us_stock_symbols = []
        # split .csv file to get symbols
        for stock in us_stock_data.splitlines()[1:]:
            stock_data = stock.split(",")
            us_stock_symbols.append(stock_data[0])
    else:
        print("Failed to get stock symbols")
        exit(1)

    # write into file for cache
    with open(symbols_filename, "wb") as file_handle:
        pickle.dump(us_stock_symbols, file_handle)

    return us_stock_symbols


if __name__ == "__main__":
    # ATTENTION! for DEBUG only
    get_all_symbols()
