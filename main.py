from datetime import datetime, timedelta
from lib.report import generateReport

READ_LOCAL_NASDAQ = False

if __name__ == "__main__":
    if (READ_LOCAL_NASDAQ):
        from lib.read_nasdaq import read_data
        data_entries = read_data("./NASDAQ_11052025/")
    else:
        from lib.read_yfinance import read_data
        data_entries = read_data()

    # for entry_index in range(0, len(data_entries)):
    #     entry = data_entries[entry_index]
    #     print(f"[{entry_index}]: {entry}: {entry.getDateRange()}")

    # extract index entries
    index_entries = []
    if (READ_LOCAL_NASDAQ):
        index_entries.append(data_entries.pop(10))
    else:
        index_entries.append(data_entries.pop(12))

    # arm start
    # start = datetime(2024, 6, 14)
    start = datetime.now() - timedelta(days=30)

    stock_start, stock_end = data_entries[0].getDateRange()
    stock_end = stock_end - timedelta(days=1)
    stock_end = stock_end

    interestingTickers = ["AMD", "ARM", "INTC", "NVDA", "META", "IBM", "MSFT", "QCOM"]  # nopep8
    generateReport(start, stock_end, data_entries, index_entries, interestingTickers)  # nopep8
