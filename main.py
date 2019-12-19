import regression
import data_show
import data_extractor
import numpy
import utils
import math
import bootstrap

if __name__ == "__main__":
    import scipy.stats as sc
    data = data_extractor.extract("datas.dat") # Nous extratons les données
    # sys = data[0]
    # x = [sys[:][0]]
    # y = sys[:][1:]
    # while len(x) < len(y):
    #     x.append(x[0])
    # print(len(x), len(y))
    # pente, ordo, r, p, error = sc.linregress(x, y)
    # print(pente, ordo)
    # data = data[0]
    # print(len(data[0][1:]))
    # # m = utils.moyennes(data[0][1:])
    # # s = utils.variances(data[0][1:], m)
    # m, s, _, _ = regression.alpha_beta_calculator(data,7)
    # print(m, s)
    # print(regression.quality(data, m, s))
    # alpha = []
    # beta = []
    # print(len(data))
    # for i in range(len(data)):
    #     a, b, _, _ = regression.alpha_beta_calculator(data[i], i+1)
    #     alpha.append(a)
    #     beta.append(b)
    # print(alpha)
    # print(beta)
    # x = [0,10000,20000,30000,40000,50000,60000,70000,80000,90000]
    # data_show.show_line(numpy.array(x), numpy.array(alpha), numpy.array(beta))
    """ 
    Pour faire un afficher toutes les données brutes sur un même graphique
    il suffit d'appeller la fonction data_show du module data_show
    """
    # data_show.data_show(data)

    """
    Pour afficher les donner des processeurs séparemment il faut 
    1. donner les données du processeur
    2. le numéro du proesseur (1, 2 ou 3)
    """
    # Avec ce code ci les trois processeurs sont affichés successivement
    # for i in range(len(data)):
    #     data_show.show_processor(data[i], i+1)

    """
    Pour afficher tous les histogrammes sur un même grahique
    il faut appeller la fonction histogram_show en lui donnant le nombre de triangles
    """
    # data_show.histogram_show(data, 100000) # On demande l'affichage des histogrammes pour 10 mille triangles
    
    """
    Pour afficher histogramme par histogramme
    il faut utiliser la fonction show_hist
    """
    for i in range(len(data)):
        for j in data[0][:,0]:
            data_show.show_hist(data[i], j)

    """
    Pour afficher les gaussienne correspondantes
    il faut utiliser la fonction show_gauss en lui donnant
    1. une liste des mu
    2. une liste des sigma
    """
    # for v in [2,3,4,5,6,7,8,9]:
    #     mu = []
    #     sigma = []
    #     for i in range(len(data)):
    #         y = data[i][v][1:]
    #         m = utils.moyennes(y)
    #         s = utils.variances(y, m)
    #         mu.append(m)
    #         sigma.append(s)
    #     data_show.show_gauss(mu, sigma)
    a = []
    b = []
    # x = [(i+1) * 10000 for i in range(0, 100000, 10000)]
    x = [10000,20000,30000,40000,50000,60000,70000,80000,90000,100000]
    # for syst in data:
    #     alpha, beta, _, _ = regression.alpha_beta_calculator(syst, 5)
    #     a.append(alpha)
    #     b.append(beta)
    # # r = []
    # # for i in range(len(data)):
    # #     r.append(regression.quality(data[i], a[i], b[i]))
    # # for i in r[0]:
    # #     print(math.sqrt(i))
    d = data[:,:,1:]
    # print(d)
    # import Exercice3
    # for i in range(len(data)):
    #     syst = data[i]
    #     i,j = regression.alpha_beta_calculator(syst, i+1)
    #     a.append(i)
    #     b.append(j)
    # print(a)
    # print(b)
    # for i in range(len(data)):
    #     print(regression.quality(data[i], a[i], b[i]))
    # a = []
    # b = []
    # for i in range(len(data)):
    #     syst = data[i]
    #     y_mean, _ = regression.error_calculator(syst)
    #     alpha, beta = regression.alpha_beta_calculator(syst)
    #     f = lambda x : alpha * x + beta
    #     x = numpy.array(x)
    #     y_hat = f(x)
    #     n_a, n_b = bootstrap.bootstrap(x,y_hat, y_mean)
    #     a.append(n_a)
    #     b.append(n_b)
    # data_show.show_line(numpy.array(x), numpy.array(a), numpy.array(b), processeur=d)