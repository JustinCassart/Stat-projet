import sys
sys.path.append("../")
import Source.regression as regression
import Source.data_show as data_show
import Source.data_extractor as data_extractor
import numpy
import Source.utils as utils
import math
import Source.bootstrap as bootstrap

if __name__ == "__main__":
    """
    La list x ci-dessous n'est utile que pour certaines fonctions
    Elle est créée seulement pour limiter le code et se concentrer sur les fonctions
    """
    x = [10000,20000,30000,40000,50000,60000,70000,80000,90000,100000]
    
    """
    Avant tout il faut extraire les données du fichier datas.dat
    """
    data = data_extractor.extract("datas.dat") # Nous extratons les données
    """ 
    Pour faire un afficher toutes les données brutes sur un même graphique
    il suffit d'appeller la fonction data_show du module data_show
    """
    data_show.data_show(data)

    """
    Pour afficher les donner des processeurs séparemment il faut 
    1. donner les données du processeur
    2. le numéro du proesseur (1, 2 ou 3)
    """
    # Avec ce code ci les trois processeurs sont affichés successivement
    for i in range(len(data)):
        data_show.show_processor(data[i], i+1)

    """
    Pour afficher tous les histogrammes sur un même grahique
    il faut appeller la fonction histogram_show en lui donnant le nombre de triangles
    """
    # Nous demandons d'afficher les histogrammes pour 10 mille triangles
    data_show.histogram_show(data, 100000)
    
    """
    Pour afficher histogramme par histogramme
    il faut utiliser la fonction show_hist
    """
    for i in range(len(data)):
        # Nous allons parcourir chaque ligne des processeurs
        for j in data[0][:,0]:
            data_show.show_hist(data[i], j, i+1)

    """
    Pour afficher les gaussiennes correspondantes
    il faut utiliser la fonction show_gauss en lui donnant
    1. une liste des mu
    2. une liste des sigma
    """
    for v in [0,1,2,3,4,5,6,7,8,9]:
        mu = []
        sigma = []
        for i in range(len(data)): # Nous parcourons les trois processeurs
            y = data[i][v][1:]
            m = utils.moyennes(y) # Nous calculons la moyenne du processeur
            s = utils.variances(y, m) # Nous calculons la variance du processeur
            mu.append(m)
            sigma.append(s)
        data_show.show_gauss(mu, sigma, x[v])

    """
    Pour afficher les résultats du bootstrap il faut
    calculer les y_mean, les alpha et les beta
    """    
    d = data[:,:,1:]
    a = []
    b = []
    for i in range(len(data)):
        syst = data[i]
        y_mean, _ = utils.mean_error_calculator(syst)
        alpha, beta = regression.alpha_beta_calculator(syst)
        f = lambda x : alpha * x + beta
        x = numpy.array(x)
        y_hat = f(x)
        n_a, n_b = bootstrap.bootstrap(x,y_hat, y_mean)
        a.append(n_a)
        b.append(n_b)
    data_show.show_line(numpy.array(x), numpy.array(a), numpy.array(b), processeur=d)