import yfinance as yf
import os
import pickle
from lib.data_objects import TickerData, TickerDataEntry
from datetime import datetime


CACHE_LOC = './yfinance_cache'

TICKER_NAMES = ['AMD', 'AAPL', 'ARM', 'AMZN', 'TSM', 'ORCL', 'CSCO', 'AVGO', 'COMP',
                'GOOGL', 'IBM', 'INTC', 'META', 'MSFT', 'NVDA', 'QCOM', "NDX"]

RANGE = '1y'


def parseDate(pd_timestamp):
    date_with_offset = pd_timestamp.to_pydatetime()
    return date_with_offset.replace(tzinfo=None)


def read_data():
    ticker_objects = []
    local_cnt = 0
    fetched_names = []

    for name in TICKER_NAMES:
        cache_valid = True
        # attempt to read data from cache
        location_str = f'{CACHE_LOC}/{name}.pkl'
        
        # check if data is available locally and valid
        if (os.path.isfile(location_str)):
            file_handle = open(location_str, 'rb')
            ticker_data = pickle.load(file_handle)

            if (ticker_data.date_created.date() < datetime.today().date()):
                cache_valid = False
        else:
            cache_valid = False

        # if not read from API and then save
        if (cache_valid == False):
            ticker_data = fetch_data(name)
            save_to_cache(ticker_data)
            fetched_names.append(ticker_data.ticker_name)
        else:
            local_cnt+=1

        ticker_objects.append(ticker_data)

    ticker_objects = sorted(
        ticker_objects, key=lambda entry: entry.ticker_name)

    print(f'Read {local_cnt} tickers locally and fetched {fetched_names}')

    return ticker_objects


def fetch_data(ticker_name):
    api_data = yf.Ticker(ticker_name)
    price_data = api_data.history(RANGE)

    object_entries = []
    for index, row in price_data.iterrows():
        # 0 volume is only for indexes - map to -1
        volume = row['Volume']
        if volume == 0:
            volume = -1

        new_object = TickerDataEntry(
            name=ticker_name,
            date=parseDate(index),
            close=row['Close'],
            vol=volume,
            open=-1,
            high=row['Low'],
            low=row['High'],
        )
        object_entries.append(new_object)

    return TickerData(
        ticker_name=ticker_name,
        source_file=f"yahoo-{ticker_name}",
        data=object_entries
    )


def save_to_cache(ticker_data_obj):
    try:
        os.mkdir(CACHE_LOC)
    except FileExistsError:
        pass

    file_handle = open(
        f'./{CACHE_LOC}/{ticker_data_obj.ticker_name}.pkl', 'wb')
    pickle.dump(ticker_data_obj, file_handle)
    file_handle.close()


if __name__ == "__main__":
    data = read_data()
    print(data)
    # indexes vs stock tickers are weird
    # api_data = yf.Ticker("NDX")
    # price_data = api_data.history("max")
    # for index, row in price_data.iterrows():
    #     print (index)
