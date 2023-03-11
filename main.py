import matplotlib.pyplot as plt
import pandas as pd
import numpy
import math
from scipy import stats

firstday = 20200305

def read_data(filename):
    turn_to_int = lambda x: 0 if x == "" else int(x)
    datalists = {"date": list(), "EC": list(), "FS": list(), "GP": list(), "KZN": list(), "LP": list(),
                 "MP": list(), "NC": list(), "NW": list(), "WC": list(), "unknown": list()}#, "total": list()}
    numdays = list()
    with open(filename) as file:
        file.readline()
        for line in file:
            line_split = line.split(",")
            datalists["date"].append(pd.to_datetime(line_split[0], dayfirst=True))
            datalists["EC"].append(turn_to_int(line_split[2]))
            datalists["FS"].append(turn_to_int(line_split[3]))
            datalists["GP"].append(turn_to_int(line_split[4]))
            datalists["KZN"].append(turn_to_int(line_split[5]))
            datalists["LP"].append(turn_to_int(line_split[6]))
            datalists["MP"].append(turn_to_int(line_split[7]))
            datalists["NC"].append(turn_to_int(line_split[8]))
            datalists["NW"].append(turn_to_int(line_split[9]))
            datalists["WC"].append(turn_to_int(line_split[10]))
            datalists["unknown"].append(turn_to_int(line_split[11]))
            #datalists["total"].append(turn_to_int(line_split[12]))

    numdays = list()
    firstday = datalists["date"][0]
    for i in datalists["date"]:
        timelapse = i-firstday
        numdays.append(timelapse.days)
    return numdays, datalists

def plot_data(datalists):
    df = pd.DataFrame(datalists)
    df.head()
    df.plot(x="date", title="Line Chart of COVID-19 Cases in Various African Regions in 2020")
    plt.xlabel("Date")
    plt.ylabel("Number of Cases")
    plt.show()
    plt.savefig("LineChartCovid19CasesAfricanRegions2020.pdf")

def main():
    file = "./archive/covid19za_provincial_cumulative_timeline_confirmed.csv"
    numdays, datalists = read_data(file)
    plot_data(datalists)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# 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