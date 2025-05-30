import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import datetime
DATA_FOLDER = "./NASDAQ_11052025/"


def read_nasdaq_data(folder_name):
    # get all csvs in folder
    filenames = [f for f in os.listdir(
        folder_name) if os.path.isfile(os.path.join(folder_name, f))]

    # read data from csvs
    data_entries = []
    for name in filenames:
        ticker_name = name.split("_")[0],

        handle = open(os.path.join(folder_name, name))
        reader = csv.reader(handle)
        # skip header row
        next(reader)

        data = []
        for row in reader:
            if len(row) == 6:
                data.append({
                    'date': row[0],
                    'close': row[1],
                    'vol': row[2],
                    'open': row[3],
                    'high': row[4],
                    'low': row[5],
                })
            else:
                data.append({
                    'date': row[0],
                    'close': row[1],
                    'open': row[2],
                    'high': row[3],
                    'low': row[4],
                })

        data_entries.append({
            "ticker": ticker_name,
            "filename": name,
            "data": data
        })

        # cleanup from loop
        del reader
        handle.close()

    return data_entries


def parse_date(date_str):
    month = int(date_str[0:2])
    day = int(date_str[3:5])
    year = int(date_str[6:10])

    return datetime.datetime(year, month, day)


def consolidate_data(ticker_data_frames):
    consolidated_data = []

    for ticker_data in ticker_data_frames:
        for ticker_entry in ticker_data['data']:

            # build data to save
            data_to_save = ticker_entry.copy()
            data_to_save['ticker'] = ticker_data['ticker'][0]
            del data_to_save['date']

            # find date index where data should go
            date_data_index = -1
            # pre-parse ticker date before searching for match in existing consolidated data db
            ticker_parsed_date = parse_date(ticker_entry['date'])

            for consolidated_entry_index in range(0, len(consolidated_data)):
                if consolidated_data[consolidated_entry_index]['date'] == ticker_parsed_date:
                    date_data_index = consolidated_entry_index
                    break

            if date_data_index != -1:
                consolidated_data[date_data_index]['data'].append(data_to_save)
            else:
                consolidated_data.append({
                    "date": parse_date(ticker_entry['date']),
                    "data": [data_to_save]
                })

    return consolidated_data


if __name__ == "__main__":
    data_entries = read_nasdaq_data(DATA_FOLDER)
    print("Reading entries")
    consolidated_data = consolidate_data(data_entries)
    print("Sorting by date")
    consolidated_data = sorted(consolidated_data, key=lambda d: d['date'])


    print('Consolidated data is:')
    print(consolidated_data[0])
    # for i in range(0, len(consolidated_data[0]['data'])):
    #     print(consolidated_data[1]['data'][i])

    # plot line chart for each of the graphs
    x_axis = []
    for item in consolidated_data:
        x_axis.append(item['date'])

    y_axis = []
    # for item in consolidated_data:
    #     for ticker in item['data']:
    #         if ticker['ticker'] == 'IBM':
    #             y_axis.append(ticker['close'])
    #             break


    for item in x_axis:
        y_axis.append(1)

    plt.plot(x_axis, y_axis)  # Plot the chart
    plt.show()  # display



# print (len(data_entries))
# print(data_entries)
