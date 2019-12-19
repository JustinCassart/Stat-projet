import data_extractor
import numpy
import math
from scipy.stats import norm, fisher_exact
import data_show
from scipy.integrate import quad

def means(data, GPU_number):
    y = data[GPU_number][:,1:]
    # y = data[:,1:]
    # print(len(y))
    y_mean = []
    for line in y:
        y_mean.append(numpy.mean(line))
    # print(len(y_mean))
    return numpy.array(y_mean)

def errors(data, GPU_number):
    y = data[GPU_number][:,1:]
    # y = data[:,1:]
    y_err = []
    for line in y:
        y_err.append(numpy.std(line))
    return numpy.array(y_err)

def moyennes(var):
    return numpy.sum(var)/(len(var))

def variances(var, m):
    r = 0
    for v in var:
        r += (v - m) ** 2
    return r / (len(var)-1)

def allmusigma(data):
    for i in range(len(data)):
        with open("processeur{}_para.txt".format(i+1), "w") as file:
            for var in data[i]:
                x = var[0]
                y = var[1:]
                m = moyennes(y)
                r = variances(y, m)
                to_write = "{} {} {}\n".format(x, m, r)
                file.write(to_write)

def repartition(var):
    rep = []
    for i in range(len(var)):
        rep.append((i + 1) / len(var))
    return numpy.array(rep)

def calculate_r(var, m, rh):
    r = []
    for v in var:
        r.append((v - m) / rh)
    return numpy.array(r)

def calculate_prob(r):
    f = []
    for i in r:
        f.append(norm.cdf(i))
    return numpy.array(f)

def calculate_diff(f, fn):
    return abs(f - fn)

def d_alpha(var, pourcent):
    tab = {1:1.629, 2:1.518, 5:1.358, 10:1.223, 20:1.073}
    return tab[pourcent] / math.sqrt(len(var))

def test_kolmorgov(data, pourcent):
    test = []
    for _ in range(len(data)): # Ajout du nombre de systèmes
        test.append([])
    for i in range(len(data)):
        for j in range(len(data[i])):
            var = data[i][j][1:]
            var.sort()
            mu = moyennes(var)
            sigma = math.sqrt(variances(var, mu))
            rep = repartition(var)
            prob = calculate_prob(calculate_r(var, mu, sigma))
            d = max(calculate_diff(rep, prob))
            d_a = d_alpha(var, pourcent)
            test[i].append((d, d_a, d < d_a))
    return test

def save_test(test):
    n_syst = len(test)
    with open("kolmorgov_test.txt", "w") as f:
        for i in range(len(test[0])):
            line = ""
            for j in range(n_syst):
                for v in test[j][i]:
                    line += str(v) + " "
                line += "| "
            line += "\n"
            f.write(line)

def calcul_gauss(x, mu, sigma):
    f = lambda x : (1/(sigma * numpy.square(2 * numpy.pi))) * (numpy.exp( - ( x - mu / sigma ) ** 2 ) / 2)
    return quad(f, - numpy.inf, x)[0]

def test_variances(variances, alpha, seuil, processor_seq):
    # alpha = 0.01
    # seuil = 1.16
    tests = []
    for n in range(len(variances)):
        for i, j in processor_seq:
            message = str((n+1) * 10000)
            v1 = variances[n][i] #** 2
            v2 = variances[n][j] #** 2
            if v1 > v2:
                F = v1 / v2
                message += " S1 > S2"
            else:
                F = v2 / v1
                message += " S2 > S1"
            message += " résultat = {} seuil = {} résultat < seuil : {}\n".format(F, seuil, F < seuil)
            file_name = "processeur{}{}_test_variancess{}.txt".format(i+1, j+1, alpha)
            if n == 0:
                f = open(file_name, "w")
            else:
                f = open(file_name, "a")
            f.write(message)
            f.close()
            tests.append((F, seuil, F < seuil))
    return tests

def test_moyennes(moyennes, variances, alpha, seuil, processor_seq):
    tests = []
    for n in range(len(moyennes)):
        for i,j in processor_seq:
            message = str((n+1) * 10000)
            m1, m2 = moyennes[n][i], moyennes[n][j]
            ecart1, ecart2 = variances[n][i], variances[n][j]
            n1 = n2 = 1000
            res = ((m1 - m2) / math.sqrt(((n1 - 1) * ecart1 + (n2 - 1) * ecart2) / (n1 + n2 - 2))) * (1/math.sqrt(1/n1 + 1/n2))
            
            message += " résultat = {} seuil = {} résultat < seuil : {}\n".format(res, seuil, abs(res) < seuil)
            file_name = "processeur{}{}_test_moyennes{}.txt".format(i+1, j+1, alpha)
            if n == 0:
                f = open(file_name, "w")
            else:
                f = open(file_name, "a")
            f.write(message)
            f.close()
            tests.append((res, seuil, abs(res) < seuil))
    return tests

if __name__ == "__main__":
    # data = data_extractor.extract("datas.dat")
    # # print(len(data))
    # # print(len(data[0]))
    # # print(len(data[0][0]))
    # # allmusigma(data)
    variances = []
    moyenne = []
    for i in range(3):
        with open("processeur{}_para.txt".format(i + 1)) as file:
            i = 0
            for line in file:
                line = line.split()
                if len(variances) < 10:
                    variances.append([float(line[2])])
                    moyenne.append([float(line[1])])
                else:
                    variances[i].append(float(line[2]))
                    moyenne[i].append(float(line[1]))
                i += 1
    print(len(variances), len(moyenne))
    # tests = test_variances(variances, 2.5, 1.11, [(0,1)])
    tests = test_moyennes(moyenne, variances, 10, 1.96, [(1,2)])
    résussi = 0
    for t in tests:
        if t[-1]:
            résussi += 1
        print(t)
    # for t in tests:
    #     if t[-1]:
    #         résussi += 1
    #     print(t)
    print("réussi à", 100 / len(tests) * résussi)
    # print(variances[0][0], variances[0][1])
    # print(moyenne[0][0], moyenne[0][1])
    # # for v in variances:
    # #     print(v)
    # #     input()
    pass