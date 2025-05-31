import copy
import numpy as np
from lib.math_util import getAverageChanges


class TickerDataContainer:
    def __init__(self, ticker_data_list, index_data_list, startDate, endDate):
        self.startDate = startDate
        self.endDate = endDate

        # filter out index and ticker data just in the date range specified
        self.ticker_data_list = []

        # create copy of ticker data to not corrupt other instances
        tmp_ticker = copy.deepcopy(ticker_data_list)
        for ticker in tmp_ticker:
            ticker.setDateRange(self.startDate, self.endDate)
            self.ticker_data_list.append(ticker)
        self.ticker_data_list = sorted(
            self.ticker_data_list, key=lambda d: d.ticker_name)

        self.index_data_list = []
        # create copy of index data to not corrupt other instances
        tmp_index = copy.deepcopy(index_data_list)
        for index in tmp_index:
            index.setDateRange(self.startDate, self.endDate)
            self.index_data_list.append(index)
        self.index_data_list = sorted(
            self.index_data_list, key=lambda d: d.ticker_name)

        # need to make sure all data has the same days present
        # use for check that all tickers/indexes start on the same day
        first_day = self.ticker_data_list[0].data[0].date

        self.missing_dates = self.ticker_data_list[0].getMissingDays()
        # find missing days from tickers
        for ticker in self.ticker_data_list:
            assert ticker.data[0].date == first_day
            tmp_missing_dates = ticker.getMissingDays()
            for tmp in tmp_missing_dates:
                if tmp not in self.missing_dates:
                    self.missing_dates.append(tmp)

        # find missing days from indexes
        for index in self.index_data_list:
            assert index.data[0].date == first_day
            tmp_missing_dates = index.getMissingDays()
            for tmp in tmp_missing_dates:
                if tmp not in self.missing_dates:
                    self.missing_dates.append(tmp)

        self.missing_dates = sorted(self.missing_dates)

        # remove missing days from all stored tickers
        for ticker in self.ticker_data_list:
            deleted = ticker.removeByDays(self.missing_dates)

        for ticker in self.index_data_list:
            deleted = ticker.removeByDays(self.missing_dates)

    def getMetaText(self):
        sep_str = ""
        for i in range(0, 80):
            sep_str += "*"
        sep_str += "\n"

        meta_text = sep_str
        meta_text += f'Comparison engine ranging [{self.startDate.date()} - {self.endDate.date()}]\n'
        meta_text += f'\nContains {len(self.index_data_list)} indexes:\n'
        for entry in self.index_data_list:
            meta_text += str(entry)+'\n'

        meta_text += f'\nContains {len(self.ticker_data_list)} tickers:\n'
        for entry in self.ticker_data_list:
            meta_text += str(entry)+'\n'
        meta_text += sep_str

        return meta_text

    def printMeta(self):
        print(self.getMetaText())

    def getDateRange(self):
        return self.startDate, self.endDate


class ComparisonEngine(TickerDataContainer):
    def __str__(self):
        return f"Comparison for [{self.startDate}-{self.endDate}] with {len(self.ticker_data_list)} tickers and {len(self.index_data_list)} indexes"

    def __repr__(self):
        return self.__str__()

    def getPercentageChanges(self, include_indexes=True, req_names=[]):
        # filter out only supplied tickers if requested
        req_data = []
        if len(req_names) == 0:
            req_data = self.ticker_data_list
        else:
            for ticker_data in self.ticker_data_list:
                for name in req_names:
                    if name == ticker_data.ticker_name:
                        req_data.append(ticker_data)

        # only include indexes if requested
        tmp_index_data_list = []
        if (include_indexes):
            tmp_index_data_list = self.index_data_list

        changes = []
        names = []
        dates = []

        for index_data in tmp_index_data_list + req_data:
            dates, tmp_changes = index_data.getPercentageChanges()
            names.append(index_data.ticker_name)
            changes.append(tmp_changes)
            dates = dates

        return dates, names, changes

    def getTickerPercentageChange(self, targetName):
        if self.getTicker(targetName):
            return self.getTicker(targetName).getPercentageChanges()
        else:
            return ([], [])

    def getTicker(self, targetName):
        for ticker in self.ticker_data_list:
            if (ticker.ticker_name == targetName):
                return ticker
        return None

    def getAverageIndexChanges(self):
        return getAverageChanges(self.index_data_list)
