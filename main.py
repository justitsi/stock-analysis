from lib.comparison_engine import ComparisonEngine
from lib.util import getTrendLine, getEntriesAboveLine
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
# DATA_FOLDER = "./NASDAQ_11052025/"
# from lib.read_nasdaq import read_data
from lib.read_yfinance import read_data


if __name__ == "__main__":
    # data_entries = read_data(DATA_FOLDER)
    data_entries = read_data()
    for entry_index in range(0, len(data_entries)):
        entry = data_entries[entry_index]
        print(f"[{entry_index}]: {entry}: {entry.getDateRange()}")

    # arm start
    arm_start, arm_end = data_entries[2].getDateRange()
    arm_end = arm_end - timedelta(days=1)

    # # extract index entries
    index_entries = []
    index_entries.append(data_entries.pop(12))

    # # comparison = ComparisonEngine(data_entries, index_entries, arm_start, arm_end)  # nopep8
    comparison = ComparisonEngine(data_entries, index_entries, datetime(2024, 6, 14), arm_end)  # nopep8
    comparison.printMeta()

    dates, names, changes = comparison.getPercentageChanges(include_indexes=False, req_names=[])  # nopep8
    dates, index_avg_changes = comparison.getAverageIndexChanges()

    for index in range(0, len(names)):
        days_index, pcnt_index = getEntriesAboveLine(
            changes[index], index_avg_changes)
        days_start, pcnt_start = getEntriesAboveLine(
            changes[index], np.full(len(dates), 1))
        print(f'{names[index]} beat indexes={days_index}/{len(dates)}({pcnt_index}%), beat start={days_start}/{len(dates)}({pcnt_start}%)')

    dates, names, changes = comparison.getPercentageChanges(include_indexes=False, req_names=["AMD", "ARM", "INTC", "NVDA", "META", "IBM", "MSFT", "QCOM"])  # nopep8
    for index in range(0, len(names)):
        plt.subplot(2, 4, index+1)
        plt.plot(dates, changes[index], label=names[index])
        plt.plot(dates, index_avg_changes, label='Index average')
        plt.plot(dates, np.full(len(dates), 1))
        plt.plot(dates, getTrendLine(changes[index]), '--k')

        day_index = []
        for i in range(0, len(dates)):
            day_index.append(i + 1)

        plt.xticks(rotation=45)
        plt.legend()

    plt.show()  # display
