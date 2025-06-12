from datetime import datetime, timedelta
from lib.report import generateReport
from lib.engine_objects import SimulationEngine
from lib.strategy_objects import BasicStrategy
import matplotlib.pyplot as plt

READ_LOCAL_NASDAQ = False

def printStrategiesSummary(type, strat_list):
    print (f"{type} starts made:")

    for index in range(0, len(strat_list)):
        strat = strat_list[index]
        strat_name = strat.stockToBuy
        print(f"Strategy {strat_name} has made ${strat.getTotalAssetValue()-strat.capital}")    
        print(f"Best assets: {strat.getBestAssetValue()}, Worst assets: {strat.getWorstAssetValue()}")

    # plt.subplot(3, 3, index+1)
        # plt.xticks(rotation=30)
        # plt.legend()
        # plt.figure()
    #     plt.plot(simEngine.getDateList(), strat.assetValues, label=strat_name)
    # fig = plt.gcf()
    # fig.tight_layout()
    # plt.show()

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
    # start = datetime(2025, 6, 3)
    start = datetime(2023, 9, 14)
    # start = datetime.now() - timedelta(days=11)

    stock_start, stock_end = data_entries[0].getDateRange()
    # stock_end = stock_end - timedelta(days=3)
    stock_end = datetime(2025, 6, 10)


    stock_end = stock_end

    # interestingTickers = ["AMD", "ARM", "INTC", "NVDA", "META", "IBM", "MSFT", "QCOM"]  # nopep8
    interestingTickers = ["AMD", "ARM", "INTC", "NVDA", "META", "IBM", "MSFT", "QCOM"]  # nopep8

    # generateReport(start.date(), stock_end.date(), data_entries, index_entries, interestingTickers, buildMD=False)  # nopep8
    strat_list = [] 
    for ticker in interestingTickers:
        strat_list.append(BasicStrategy(1000, ticker, 2))

    simEngine = SimulationEngine(data_entries, index_entries, start.date(), stock_end.date(), strat_list)
    simEngine.runSim()

    printStrategiesSummary
        

