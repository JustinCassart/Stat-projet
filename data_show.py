import data_extractor
import matplotlib.pyplot  as plt 
from scipy import stats



def data_show(filename):
    datas = data_extractor.extract(filename)

    for i in range(len(datas)):
        sub_fig, sub_ax = plt.subplots()
        x = datas[i][:,0]
        y = datas[i][:,1:]
        sub_ax.plot(x, y, "k.")
        sub_ax.set_xlabel("Number of triangles")
        sub_ax.set_ylabel("CPU time")
        sub_fig.suptitle("System %d plot data"%(i+1))

    plt.show()

def errorbar_show(filename):
    datas = data_extractor.extract(filename)

    for i in range(len(datas)):
        sub_fig, sub_ax = plt.subplots()
        x = datas[i][:,0]
        y = datas[i][:,1:]
        sub_ax.errorbar(x, y, linestyle = " ", capsize = 2.5)
        sub_ax.set_xlabel("Number of triangles")
        sub_ax.set_ylabel("CPU time")
        sub_fig.suptitle("System %d plot data"%(i+1))

    plt.show()

errorbar_show("datas.dat")