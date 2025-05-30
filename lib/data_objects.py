import numpy as np
from datetime import datetime, timedelta

class TickerDataEntry:
    def __init__(self, name: str, high: float, low: float,
                 open: float, close: float, vol: int, date):
        self.name = str(name)
        self.high = high
        self.low = low
        self.open = open
        self.close = close
        self.vol = int(vol)
        self.date = date

    def __str__(self):
        return f"{self.name} on {self.date}"

    def __repr__(self):
        return self.__str__()

    def getPrice(self):
        return self.close


class TickerData:
    def __init__(self, ticker_name: str, source_file: str, data):
        self.ticker_name = ticker_name
        self.source_file = source_file
        self.data = sorted(data, key=lambda d: d.date)
        self.date_created = datetime.now()

    def __str__(self):
        return f"{self.ticker_name} with {len(self.data)} entries"

    def __repr__(self):
        return self.__str__()

    def check_range_input(self, startDate, endDate):
        current_start, current_end = self.getDateRange()
        assert startDate >= current_start
        assert endDate <= current_end

    def setDateRange(self, startDate, endDate):
        self.check_range_input(startDate, endDate)

        new_data = []

        for data_entry in self.data:
            if (data_entry.date >= startDate and data_entry.date <= endDate):
                new_data.append(data_entry)

        self.data = new_data

    def getDateRange(self):
        return (self.data[0].date, self.data[-1].date)

    def getMissingDays(self):
        missing = []
        
        for index in range (1, len(self.data)):
            prev_day = self.data[index-1].date
            curr_day = self.data[index].date
            diff_days = (curr_day - prev_day).days
            if diff_days > 1:
                new_missing = []
                for tmp_day_diff in range(1, diff_days):
                    new_missing.append(curr_day - timedelta(days=tmp_day_diff))

                for entry in new_missing:
                    missing.append(entry)

        return missing

    def removeByDays(self, days):
        removed = 0
        for day in days:
            ok = self.removeByDay(day)
            if ok:
                removed += 1

        return removed

    def removeByDay(self, day): 
        index = -1
        for i in range (0, len(self.data)):
            if self.data[i].date == day:
                index = i
                break

        if index == -1:
            return False
        else:
            # remove entry if found
            self.data.pop(i)
            return True             

    def getPercentageChanges(self):
        dates = []
        movements = []

        for index in range(0, len(self.data)):
            dates.append(self.data[index].date)

            old_price = self.data[0].getPrice()
            new_price = self.data[index].getPrice()
            movements.append(new_price/old_price)

        # convert to numpy array to allow for faster onwards processing
        movements = np.array(movements, dtype=np.float32)
        return (dates, movements)

    def getPrices(self):
        prices = []
        for entry in self.data:
            prices.append(entry.getPrice())

        return np.array(prices, dtype=np.float32)