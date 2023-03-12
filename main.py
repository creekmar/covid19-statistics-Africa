import matplotlib.pyplot as plt
import pandas as pd
import numpy
import math
import os
from scipy import stats


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

    # creating a list of number of days from 5 March 2020 for regression
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
    #plt.show()
    plt.savefig("./Charts/LineChartCovid19CasesAfricanRegions2020.pdf")


def exp_regression(ydata, numdays, region):

    # linearlize data by taking the log
    take_log = lambda t: 0 if t == 0 else math.log10(t)
    linear_y = list()
    for i in ydata:
        linear_y.append(take_log(i))
    plt.scatter(numdays, ydata)

    # regression
    slope, intercept, r, p, std_err = stats.linregress(numdays, linear_y)
    x = numpy.linspace(numdays[0], numdays[len(numdays)-1], 400)
    y = 10**intercept * 10**(slope*x)
    plt.plot(x, y, color="red")
    plt.xlabel("Number of Days Since 5 March 2020")
    plt.ylabel("Number of Cases")
    plt.title("COVID-19 Cases in " + region + " in 2020")
    plt.savefig("./Charts/" + region + "_Covid19Cases2020ExpRegression.pdf")
    #plt.show()
    return "y = 10^" + str(intercept) + " * 10^(" + str(slope) + "*x)"


def poly_regression(ydata, numdays, region):
    get_fit_str = lambda t: "{0:.3f}".format(t) if t < 0 else "+ " + "{0:.3f}".format(t)

    fit = numpy.poly1d(numpy.polyfit(numdays, ydata, 3))
    x = numpy.linspace(numdays[0], numdays[len(numdays)-1], 300)
    y = fit(x)
    plt.scatter(numdays, ydata)
    plt.plot(x, y, color="red")
    plt.xlabel("Number of Days Since 5 March 2020")
    plt.ylabel("Number of Cases")
    plt.title("COVID-19 Cases in " + region + " in 2020")
    #plt.show()
    plt.savefig("./Charts/" + region + "_Covid19Cases2020CubicRegression.pdf")
    return "y = " + get_fit_str(fit[3]) + " x^3 " + get_fit_str(fit[2]) + " x^2 " + get_fit_str(fit[1]) \
        + " x " + get_fit_str(fit[0])


def main():
    if not os.path.exists("./Charts"):
        os.mkdir("./Charts")
    file = "./archive/covid19za_provincial_cumulative_timeline_confirmed.csv"
    numdays, datalists = read_data(file)

    plot_data(datalists)

    # remove date from keys so we can loop through regions
    keys = list(datalists.keys())
    keys.remove("date")
    with open("./Charts/AfricanCovid19CasesRegression.txt", "w") as file:
        file.write("region,exponential regression equation,cubic regression equation\n")
        for i in keys:
            exp_equation = exp_regression(datalists[i], numdays, i)
            cub_equation = poly_regression(datalists[i], numdays, i)
            file.write(i + "," + exp_equation + "," + cub_equation + "\n")
    print("End Program")


if __name__ == '__main__':
    main()
