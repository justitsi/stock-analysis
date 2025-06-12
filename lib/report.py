from lib.engine_objects import ComparisonEngine
from lib.math_util import getTrendLine, countEntriesAboveLine, getAverageDistance
import numpy as np
import matplotlib.pyplot as plt
from lib.util import tryMakeDir
from markdown_pdf import MarkdownPdf, Section

def generateTickerChart(dates, changes, compare, name, comapre_name, reportDir):
    plt.plot(dates, changes, label=name)
    plt.plot(dates, compare, label=comapre_name)

    plt.plot(dates, np.full(len(dates), 1))
    plt.plot(dates, getTrendLine(changes), '--k')

    plt.xticks(rotation=45)
    plt.legend()

    if (reportDir):
        plt.xticks(rotation=20)
        plt.savefig(f"{reportDir}/plots/{name}.png", dpi=200)
        plt.close()
        plt.figure()


def comparePerf(changes, compare):
    days, pcnt = countEntriesAboveLine(changes, compare)  # nopep8

    return days, pcnt


def getTickerStats(name, dates, changes, compare):
    days_index, pcnt_index = comparePerf(changes, compare)
    days_start, pcnt_start = comparePerf(changes, np.full(len(dates), 1))

    return {
        "name": name,
        "days_index": days_index,
        "pcnt_index": pcnt_index,
        "days_start": days_start,
        "pcnt_start": pcnt_start,
        "price_change": round(float(changes[-1] - 1)*100, ndigits=1),
        "avg_index_dist": getAverageDistance(changes, compare)
    }


def getTickerSummary(name, dates, changes, compare, reportDir, buildMD=True):
    generateTickerChart(dates, changes, compare, name, "Index_avg", reportDir)
    stats = getTickerStats(name, dates, changes, compare)

    text = f"<h2 id={name}>{name}</h2>\n\n"
    if(buildMD):
        text += f"![{name} performance plot](./plots/{name}.png)\n\n"
    else:
        text += f"![{name} performance plot](./{reportDir}/plots/{name}.png)\n\n"

    text += f"* Price change: {stats['price_change']}%\n"
    text += f"* Beat index movements {stats['days_index']}/{len(dates)} days ({stats['pcnt_index']}%)\n"
    text += f"* Beat start price {stats['days_start']}/{len(dates)} days ({stats['pcnt_start']}%)\n"
    text += f"* Average distance from index: {stats['avg_index_dist']}%\n\n"
    text += f"[See more on yfinance](https://finance.yahoo.com/quote/{name})"
    if(not buildMD):
        text += f'<div style="page-break-after: always;"></div>'

    return text, stats


def addLink(name):
    return f"[{name}](#{name})"


def generateReport(startDate, endDate, tickers, indexes, interestingTickers, reportDir='./report_output', buildMD=True):
    tryMakeDir(reportDir)
    tryMakeDir(f"{reportDir}/plots")
    
    comparison = ComparisonEngine(tickers, indexes, startDate, endDate)  # nopep8
    comparison.printMeta()

    dates, index_avg_changes = comparison.getAverageIndexChanges()
    dates, names, changes = comparison.getPercentageChanges(include_indexes=False, req_names=interestingTickers)  # nopep8
    for index in range(0, len(names)):
        plt.subplot(4, 2, index+1)
        generateTickerChart(dates,
                            changes[index], index_avg_changes,
                            names[index], "Index avg", False)

    fig = plt.gcf()
    fig.set_size_inches(10, 15)
    fig.tight_layout()
    # plt.show()  # display
    plt.savefig(f"{reportDir}/plots/overview.png", dpi=100)
    plt.figure()

    report_text = f"# Report [{startDate} - {endDate}]\n\n"
    report_text += f'Report spans a total of {len(changes[0])} work days. The best performing stocks in the time period were:\n\n'

    dates, names, changes = comparison.getPercentageChanges(include_indexes=False, req_names=[])  # nopep8
    stock_performance = []
    stock_text_body = ''
    for index in range(0, len(names)):
        tmp_txt, stats = getTickerSummary(
            names[index], dates, changes[index], index_avg_changes, reportDir, buildMD)
        stock_text_body += tmp_txt
        stock_performance.append(stats)

    # generate performance summary table:
    vs_price_perf = sorted(stock_performance, key=lambda d: d['price_change'])
    vs_price_perf.reverse()
    vs_index_perf = sorted(stock_performance, key=lambda d: d['pcnt_index']) #nopep8
    vs_index_perf.reverse()
    vs_start_perf = sorted(stock_performance, key=lambda d: d['pcnt_start']) #nopep8
    vs_start_perf.reverse()
    avg_index_dist = sorted(stock_performance, key=lambda d: d['avg_index_dist']) #nopep8
    avg_index_dist.reverse()

    table_txt = "|Rank|By price change|By time beat indexes|By time beat start| By average index distance|\n|-|-|-|-|-|\n"
    for i in range(1, len(stock_performance)+1):
        table_txt += f"|{i}|"
        table_txt += f"{addLink(vs_price_perf[i-1]['name'])}: {vs_price_perf[i-1]['price_change']}%|"
        table_txt += f"{addLink(vs_index_perf[i-1]['name'])}: {vs_index_perf[i-1]['pcnt_index']}%|"
        table_txt += f"{addLink(vs_start_perf[i-1]['name'])}: {vs_start_perf[i-1]['pcnt_start']}%|"
        table_txt += f"{addLink(avg_index_dist[i-1]['name'])}: {avg_index_dist[i-1]['avg_index_dist']}%|"
        table_txt += "\n"

    report_text += table_txt + "\n"
    if (buildMD):
        report_text += f"![Report Summary](./plots/overview.png)\n"
    else:
        report_text += f"![Report Summary](./{reportDir}/plots/overview.png)\n"

    report_text += "\n" + stock_text_body

    if (buildMD):
        report_handle = open(f"{reportDir}/report.md", 'w')
        report_handle.write(report_text)
        report_handle.close()
    else:
        # now also save this to PDF
        pdf = MarkdownPdf(toc_level=2, optimize=True)

        pdf.add_section(Section(report_text))
        pdf.save(f"{reportDir}/report.pdf")