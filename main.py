import pandas as pd

def read_data(filename):
    datalists = {"date": list(), "EC": list(), "FS": list(), "GP": list(), "KZN": list(), "LP": list(),
                 "MP": list(), "NC": list(), "NW": list(), "WC": list(), "unknown": list(), "total": list()}
    with open(filename) as file:
        file.readline()
        for line in file:
            line_split = line.split(",")
            datalists["date"].append(pd.to_datetime(line_split[0], dayfirst=True))
            datalists["EC"].append(line_split[2])
            datalists["FS"].append(line_split[3])
            datalists["GP"].append(line_split[4])
            datalists["KZN"].append(line_split[5])
            datalists["LP"].append(line_split[6])
            datalists["MP"].append(line_split[7])
            datalists["NC"].append(line_split[8])
            datalists["NW"].append(line_split[9])
            datalists["WC"].append(line_split[10])
            datalists["unknown"].append(line_split[11])
            datalists["total"].append(line_split[12])
    return datalists

def plot_data():
    pass

def main():
    file = "./archive/covid19za_provincial_cumulative_timeline_confirmed.csv"
    datalists = read_data(file)
    print(datalists)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
