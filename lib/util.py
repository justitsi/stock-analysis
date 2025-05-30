import numpy as np


def getAverageLine(data_points):
    return np.full(len(data_points), np.average(data_points))


def getTrendLine(data_points):
    tmp_x = range(1, len(data_points)+1)
    # code from https://stackoverflow.com/questions/6148207/linear-regression-with-matplotlib-numpy
    coef = np.polyfit(tmp_x, data_points, 1)
    poly1d_fn = np.poly1d(coef)

    pred_y = []
    for value in tmp_x:
        pred_y.append(poly1d_fn(value))

    return pred_y


def getAverageChanges(tickers):
    assert len(tickers) > 0
    dates = []
    movement_data = []

    for ticker_data in tickers:
        dates, movements = ticker_data.getPercentageChanges()  # nopep8
        movement_data.append(movements)

    avg_movement_data = movement_data[0]
    if len(tickers) > 1:
        for i in range(1, len(tickers)):
            avg_movement_data += movement_data[i]
        avg_movement_data = avg_movement_data/len(tickers)

    return dates, avg_movement_data


def getEntriesAboveLine(to_check, ref_line):
    count = 0
    tmp = to_check - ref_line

    for value in tmp:
        if value > 0:
            count += 1

    return count, round(count/len(to_check) * 100, ndigits=1)
