from lib.data_objects import TickerDataEntry


class SimulationPosition:
    def __init__(self, tickerName, amount, entryPrice, dateBought):
        self.open = True
        self.tickerName = str(tickerName)
        self.amount = int(amount)
        self.entryPrice = float(entryPrice)

        self.boughtAt = dateBought
        self.closedAt = None

    def getValue(self, currentPrice):
        return self.amount*currentPrice

    def getProfit(self, currentPrice):
        return self.amount * (currentPrice - self.entryPrice)

    def getCost(self):
        return self.amount*self.entryPrice

    def __repr__(self):
        if self.open:
            return f"Position({self.tickerName}-{self.boughtAt}-{self.getCost()})"
        else:
            return f"Closed Position {self.tickerName}-{self.amount}-{self.boughtAt}:{self.closedAt}"


# generic strategy object with base operations for buying, selling and holding positions
class BaseStrategy():
    def __init__(self, capital: float):
        self.positions = []

        self.balance = round(float(capital), 2)
        self.capital = round(float(capital), 2)

        self.currentDate = None
        self.currentTickers = []
        self.currentIndexes = []
        self.assetValues = []

    def getBestAssetValue(self):
        max_value = self.assetValues[0]
        for value in self.assetValues:
            if value > max_value:
                max_value = value
        return max_value
    
    def getWorstAssetValue(self):
        min_value = self.assetValues[0]
        for value in self.assetValues:
            if value < min_value:
                min_value = value
        return min_value

    def getTickerByName(self, name):
        tickerData = None
        for ticker in self.currentTickers:
            if ticker.name == name:
                tickerData = ticker
                break
        assert (tickerData is not None)

        return tickerData

    def getOpenPositions(self):
        openPositions = []

        for tmp in self.positions:
            if tmp.open == True:
                openPositions.append(tmp)

        return openPositions

    def getTotalAssetValue(self):
        tmp = self.balance

        for pos in self.getOpenPositions():
            posTickerData = self.getTickerByName(pos.tickerName)
            tmp += pos.getValue(posTickerData.getPrice())

        return round(tmp, 2)

    def openPosition(self, tickerDataEntry: TickerDataEntry, amount: float):
        price = tickerDataEntry.getPrice()
        # check if we can actually afford this
        assert (self.balance - amount*price > 0)
        self.balance = self.balance - amount*price

        newPosition = SimulationPosition(
            tickerName=tickerDataEntry.name,
            amount=amount,
            entryPrice=price,
            dateBought=self.currentDate
        )

        self.positions.append(newPosition)

    def closePosition(self, position: SimulationPosition):
        # verify position hasn't been closed before
        assert position.open == True

        tickerData = self.getTickerByName(position.tickerName)
        self.balance += position.getValue(tickerData.getPrice())
        position.open = False
        position.closedAt = self.currentDate

    def updateState(self, currentDate, currentTickers, currentIndexes):
        self.currentDate = currentDate
        self.currentTickers = currentTickers
        self.currentIndexes = currentIndexes
        self.processUpdate()

        # save the current asset value for stats later
        self.assetValues.append(self.getTotalAssetValue())

    # this is the function that is meant to be overloaded by child strategies to implement their logic
    def processUpdate(self):
        raise Exception("BaseStrategy does not implement processUpdate() functionality ")  # nopep8
        

class BasicStrategy(BaseStrategy):
    def __init__(self, capital: float, stockToBuy: str, amount: int):
        super().__init__(capital)
        self.stockToBuy = str(stockToBuy)
        self.amount = amount

    def processUpdate(self):
        # find price of ticker that the strategy uses
        tickerData = self.getTickerByName(self.stockToBuy)

        # debug print
        # print(f"{self.currentDate} - {self.balance} - {tickerData.name} - {tickerData.getPrice()}")  # nopep8
        # print(f"Total assets={self.getTotalAssetValue()}")

        openPos = self.getOpenPositions()
        if (len(openPos)>0):
            for pos in openPos:
                # check if the position is worth more than we bought it for and sell if it is
                currentTickerData = self.getTickerByName(pos.tickerName)
                if (pos.getProfit(currentTickerData.getPrice()) > 0):
                    self.closePosition(pos)
        else:
            self.openPosition(tickerData, self.amount)


class BasicStrategy2(BaseStrategy):
    def __init__(self, capital: float, stockToBuy: str):
        super().__init__(capital)
        self.stockToBuy = str(stockToBuy)
        self.historicalData = []

    def processUpdate(self):
        # find price of ticker that the strategy uses
        tickerData = self.getTickerByName(self.stockToBuy)
        
        # debug print
        # print(f"{self.currentDate} - {self.balance} - {tickerData.name} - {tickerData.getPrice()}")  # nopep8
        # print(f"Total assets={self.getTotalAssetValue()}")

        openPos = self.getOpenPositions()
        if (len(openPos)>0):
            for pos in openPos:
                # check if the position is worth more than we bought it for and sell if it is
                currentTickerData = self.getTickerByName(pos.tickerName)
                if (pos.getProfit(currentTickerData.getPrice()) > 0):
                    self.closePosition(pos)
        else:
            self.openPosition(tickerData, self.amount)