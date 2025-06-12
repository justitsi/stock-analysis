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

    # extract index entries
    index_entries = []
    if (READ_LOCAL_NASDAQ):
        index_entries.append(data_entries.pop(10))
    else:
        index_entries.append(data_entries.pop(12))

    # arm start
    start = datetime(2023, 9, 14)

    stock_start, stock_end = data_entries[0].getDateRange()
    # stock_end = stock_end - timedelta(days=3)
    stock_end = datetime(2025, 6, 10)
    stock_end = stock_end

    interestingTickers = ["AMD", "ARM", "INTC", "NVDA", "META", "IBM", "MSFT", "QCOM"]  # nopep8

    generateReport(start.date(), stock_end.date(), data_entries, index_entries, interestingTickers, buildMD=False)  # nopep8
        

