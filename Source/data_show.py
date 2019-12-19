import matplotlib.pyplot  as plt 
from scipy import stats
import scipy.optimize as opt 
import numpy
from math import ceil
import Source.utils as utils

COLOR = {0 : "k.", 1 : "b.", 2 : "r."}

def data_show(data):
    for i in range(len(data)):
        x = data[i][:,0]
        y = data[i][:,1:]
        plt.plot(x, y, COLOR[i])
    plt.show()

def show_processor(processor_data, id_processor):
    x = processor_data[:,0]
    y = processor_data[:,1:]
    sub_fig, sub_ax = plt.subplots()
    sub_ax.plot(x, y, COLOR[id_processor - 1])
    sub_ax.set_xlabel("Number of triangles")
    sub_ax.set_ylabel("GPU time")
    sub_fig.suptitle("Processor %d plot data"%(id_processor))
    plt.show()

def errorbar_show(data):
    f = lambda x, a, b : a*x+b

    for i in range(len(data)):
        sub_fig, sub_ax = plt.subplots()
        x = data[i][:,0]
        # x = data[:,0]
        y_mean, y_err = utils.mean_error_calculator(data[i])
        sub_ax.errorbar(x, y_mean, yerr = y_err, marker = "*", linestyle = "", capsize = 2.5)
        for _ in range(5):
            a, _ = opt.curve_fit(f, x, y_mean, sigma=y_err)
            b, _ = opt.curve_fit(f, x, y_mean)
        sub_ax.plot(x, f(x, *a), "r--", label = "Régression pondéré")
        sub_ax.plot(x, f(x, *b), "g--", label = "Régression ordinaire")
        sub_ax.set_xlabel("Number of triangles")
        sub_ax.set_ylabel("CPU time")
        sub_fig.suptitle("System %d errorbar"%(i+1))

    plt.show()

def get_index(element, admissible):
    for i in range(len(admissible)):
        if element <= admissible[i]:
            return i
    return len(admissible) - 1

def histogram_show(data, n_triangles):
    if not n_triangles in data[0][:,0]:
        raise Exception

    time = int(n_triangles /10000) - 1

    for i in range(len(data)):
        y = data[i][:,1:][time]
        begin = int(min(y))
        end = int(max(y))
        step = end // 30
        admissible = [i for i in range(begin, end, step)]
        a = [get_index(i, admissible) for i in y]
        plt.hist(a, align="left", bins=len(admissible) - 1, histtype="step", color=COLOR[i][0])
        plt.xticks(range(len(admissible)), admissible)
    plt.show()

def show_hist(processor, n_triangles, id_processor=None):
    i = int(n_triangles/10000) - 1
    y = processor[i, 1:]
    begin = int(min(y))
    end = int(max(y))
    sep = 30 + (i+1) * 5
    step = end // sep
    admissible = [v for v in range(begin, end, step)]
    a = [get_index(v, admissible) for v in y]
    plt.hist(a, align="left", bins=len(admissible) - 1, label="Histogramme processeur {} pour {} triangles".format(id_processor, n_triangles), color=COLOR[id_processor-1][0])
    plt.xticks(range(len(admissible)), admissible)
    plt.xlabel("Temps d'exécution")
    plt.ylabel("Proportion")
    plt.legend(loc="upper left")
    plt.show()

def show_gauss(_mu, _rho, n_triangles=None):
    for i in range(len(_mu)):
        x = numpy.linspace(_mu[i] - 3*_rho[i], _mu[i] + 3*_rho[i])
        plt.plot(x, stats.norm.pdf(x, _mu[i], _rho[i]), label = "Processeur {}".format(i+1), color=COLOR[i][0])
        plt.legend(loc = "upper left")
        if n_triangles:
            plt.xlabel("Proportion pour {}".format(n_triangles))
    plt.show()

def show_line(x, alpha, beta, processeur=[]):
    f = lambda x, a, b : a * x + b
    for i in range(len(alpha)):
        y = f(x, alpha[i], beta[i])
        if len(processeur) > 0:
            plt.plot(x, processeur[i], COLOR[i])
        plt.plot(x, y, COLOR[i][0], label = "GPU avec processeur {}".format(i+1))
        plt.legend(loc = "upper left")
    plt.show()



if __name__ == "__main__":
    # show_gauss(0, 1)
    data = data_extractor.extract("data.dat")
    # a = []
    # b = []
    # x = [(i+1) * 10000 for i in range(0, 100000, 10000)]
    # for syst in data:
    #     alpha, beta, _, _ = regression.alpha_beta_calculator(syst, 45)
    #     a.append(alpha)
    #     b.append(beta)
    # show_line(x, a, b)
    # data_show("data.dat")
    # histogram_show("data.dat", 100000)
    # proc1 = data[0]
    # data = []
    # for line in proc1:
    #     data.extend(line[1:])
    # histo(data)
    # show_hist(data[0], 100000)or j in = "processeur {}".format(i))
    #     elif i == 2:
    #         plt.plot(x, y, "b.", label = "processeur {}".format(i))
    #     else:
    #         plt.plot(x, y, "r.", label = "processeur {}".format(i))
    #     i += 1
    # plt.legend(loc = "upper left")
    # plt.show()

    # show(data[0], "k.", 1)
    # show(data[1], "b.", 2)
    # show(data[2], "r.", 3)
    # data_show("data.dat")

    # histogram_show("data.dat", 10000)
# errorbar_show("data.dat")
# data_show("data.dat")


# finalGrades = [-3, -3, 10, 2, 10, 0, 7, 7, 12, -3, 7, 0, 12, 12, 12 ,12, 12, 0, 0, 0, 4]
# possibleGrades = [-3, 0, 2, 4, 7, 10, 12]
# fin = [ possibleGrades.index(i) for i in finalGrades]
# print(fin)
# plt.hist(fin, bins=range(8), align="left")
# plt.xticks(range(7), possibleGrades)

# plt.title("Final Grades plot")
# plt.xlabel("All possible grades")
# plt.ylabel("Number of students")
# plt.show()