# import those nessarary libraries
import os
import pandas as pd
from typing import List
from threading import Thread, Lock
from alpha_vantage.timeseries import TimeSeries

from get_symbol import get_all_symbols
from constants import key, output_directory, query_thread_number, maximum_retry_times

# the variable below records the current symbol index
current_symbol_index: int = 0
# all existing symbols
symbols: List[str] = get_all_symbols()
# threads here
threads: List[Thread] = []
thread_lock: Lock = Lock()


def download_one_symbol() -> None:
    """
    This is a function used by a thread. As we all know, multi-threads
    is very useful when we acquire something from internet.
    """
    # declaration for global variable current_symbol_index
    global current_symbol_index

    while True:
        # using lock to prevent data race
        with thread_lock:
            # the same operation as fetch_and_increase
            symbol_index: int = current_symbol_index
            current_symbol_index += 1
        # if the index exceeds the range of symbols, return directly
        if symbol_index >= len(symbols):
            return

        # filename for the current file
        current_symbol: str = symbols[symbol_index]
        filename: str = os.path.join(output_directory, f"{current_symbol}.csv")
        # check whether the file exists already
        if os.path.exists(filename):
            continue

        # try to send http request and write data into file system
        repeat_time: int = 0
        while True:
            try:
                # get data and write them into .csv file
                data, metadata = ts.get_daily_adjusted(
                    current_symbol, outputsize="full"
                )
                pd.DataFrame(data).to_csv(filename)
                break
            except Exception as e:
                # if repeat time has exceeded the maximum try-time, continue
                if repeat_time > maximum_retry_times:
                    print(
                        f"Error processing {current_symbol}: {e}. "
                        f"This is the {repeat_time}-th try, now skip it."
                    )
                    break
                else:
                    print(
                        f"Error processing {current_symbol}: {e}. "
                        f"This is the {repeat_time}-th try, now try again."
                    )
                    repeat_time += 1


if __name__ == "__main__":
    # the type of TimeSeries
    ts = TimeSeries(key=key, output_format="pandas")

    # ensure the output path exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # create threads to access the data
    for _ in range(query_thread_number):
        threads.append(Thread(target=download_one_symbol))
        threads[-1].start()

    # wait for all processes to return
    for i in range(query_thread_number):
        threads[i].join()
