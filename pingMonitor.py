import os
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoLocator, AutoMinorLocator, MaxNLocator
from datetime import datetime

def pltSty(xName = "x-axis", yName = "y-axis", titleName = "", TitleSize = 15, LabelSize = 13):
    ax = plt.gca()
    ax.set_title(titleName, fontsize = TitleSize)
    ax.set_xlabel(xName, fontsize = TitleSize, loc = "right")
    ax.set_ylabel(yName, fontsize = TitleSize, loc = "top")
    ax.xaxis.set_major_locator(MaxNLocator(nbins = 10))
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_major_locator(AutoLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())

    ax.tick_params(direction = "in", length = 9, labelsize = LabelSize, top = True, right = True)
    ax.tick_params(direction = "in", length = 4, which = "minor", labelsize = LabelSize, top = True, right = True)

def main():
    x32, y32 = [], []
    x30, y30 = [], []
    t = 0

    plt.figure(figsize = (15, 5))
    pltSty(xName = "Time", yName = "Connection", titleName = "Ping Monitor", TitleSize = 15, LabelSize = 13)
    plt.plot([], [], linestyle = "-", marker = "*", color = "#202020", markersize = 10, label = "chip02")
    plt.plot([], [], linestyle = "-", marker = ".", color = "g", markersize = 8, label = "cms02")
    plt.legend(loc = "upper right", shadow = True, fontsize = 16)
    while True:
        response32 = os.system("ping -c 1 {}".format(host32))
        response30 = os.system("ping -c 1 {}".format(host30))
        print("---------------------------------------------")

        now = datetime.now()
        if response32 == 0:
            y32.insert(0, 1)
        else:
            y32.insert(0, 0)
        x32.insert(0, now.strftime("%d/%m/%Y %H:%M:%S"))

        if response30 == 0:
            y30.insert(0, 1)
        else:
            y30.insert(0, 0)
        x30.insert(0, now.strftime("%d/%m/%Y %H:%M:%S"))

        plt.xticks(rotation = 20)
        plt.ylim(-0.1, 1.6)
        plt.grid(True)

        plt.plot(x32, y32, linestyle = "-", marker = "*", color = "#202020", markersize = 10)
        plt.plot(x30, y30, linestyle = "-", marker = ".", color = "g", markersize = 8)

        plt.tight_layout()
        plt.pause(1)
        t += 1

    plt.ioff()
    plt.show()


if __name__ == "__main__":
    host32 = "chip02.phy.ncu.edu.tw"
    host30 = "cms02.phy.ncu.edu.tw"

    try:
        main()
    except KeyboardInterrupt:
        print("Exitting on KeyboardInterrupt")
        sys.exit(1)
