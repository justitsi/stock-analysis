import os
import csv
import datetime
from lib.data_objects import TickerData, TickerDataEntry


def clean_price_string(price_str):
    price_str = price_str.replace("$", "")
    return float(price_str)


def parse_date(date_str):
    month = int(date_str[0:2])
    day = int(date_str[3:5])
    year = int(date_str[6:10])

    return datetime.datetime(year, month, day).date()


def read_data(folder_name):
    # get all csvs in folder
    filenames = [f for f in os.listdir(
        folder_name) if os.path.isfile(os.path.join(folder_name, f))]

    # read data from csvs
    data_entries = []
    for name in filenames:
        handle = open(os.path.join(folder_name, name))
        reader = csv.reader(handle)
        # skip header row
        next(reader)
        ticker_name = name.split("_")[0]

        data = []
        for row in reader:
            # handle normal stocks
            if len(row) == 6:
                data.append(TickerDataEntry(
                    name=ticker_name,
                    date=parse_date(row[0]),
                    close=clean_price_string(row[1]),
                    vol=clean_price_string(row[2]),
                    open=clean_price_string(row[3]),
                    high=clean_price_string(row[4]),
                    low=clean_price_string(row[5]),
                ))
            # handle indexes
            else:
                data.append(TickerDataEntry(
                    name=ticker_name,
                    date=parse_date(row[0]),
                    close=clean_price_string(row[1]),
                    open=clean_price_string(row[2]),
                    high=clean_price_string(row[3]),
                    low=clean_price_string(row[4]),
                    vol=-1
                ))

        data_entries.append(TickerData(
            ticker_name=ticker_name,
            source_file=name,
            data=data
        ))

        # cleanup from loop
        del reader
        handle.close()

    data_entries = sorted(data_entries, key=lambda entry: entry.ticker_name)
    return data_entries
