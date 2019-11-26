#!/usr/bin/python3
# -*- coding:utf-8 -*-

# Import modules

# Importer numpy pour l'utilisation des arrays
import numpy as np
# Importer matplotlib.pyplot pour tracer les graphiques
import matplotlib.pyplot as plt
# Importer sicpy.optimize pour effectuer la régression
import scipy.optimize as sp_opt

# Récupérer les fonctions définies à l'exo 3
from Exercice3 import *

if __name__ == "__main__":
    data_exo4 = np.array([
            [-1.61, 2.22, 2.14, 2.16, 2.2, 2.1],
            [-1.2, 2.27, 2.29, 2.31, 2.3, 2.3],
            [-0.97, 2.38, 2.38, 2.41, 2.42, 2.42],
            [-0.51, 2.6, 2.4, 2.6, 2.59, 2.57],
            [-0.42, 2.65, 2.65, 2.64, 2.62, 2.61]])

    # On calcule les paramètres optimaux avec les matrices
    mpopt = optimal_parameters(data_exo4)
    print("Mes paramètres optimaux sont :")
    print("Pente : %.3e" % mpopt[0])
    print("Ordonnée à l'origine : %.3e\n" % mpopt[1])

    # On effectue la régression avec scipy
    # On commence par définir la fonction f linéaire
    f = lambda x, a, b : a*x+b
    # On définit x
    x = data_exo4[:, 0]
    # On définit y
    y = data_exo4[:, 1:]
    print(x)
    print(y)

    # On calcule les moyennes et les erreurs
    ym, yerr = compute_means_and_erros(data_exo4)
    # On fait la régression
    popt, pcov = sp_opt.curve_fit(f, x, ym, sigma=yerr)

    print("Les paramètres de régression python sont :")
    print("Pente : %.3e" % popt[0])
    print("Ordonnée à l'origine : %.3e\n" % popt[1])

    # On prévoit la hauteur de l'arbre
    expected_h = np.exp(popt[1]) * 0.8**(popt[0])
    print("On prévoit un arbre de %.3f m de haut\n" % expected_h)

    # On calcule le R²
    print("Le coefficient de détermination est %.3f" % determination_coeff(ym, f(x, *popt), 1./(yerr**2)))
    # On construit un premier graphique
    plt.figure(1)
    # On trace les données avec des points noirs
    plt.plot(x, y, 'k.')
    # On construit un deuxième graphique
    plt.figure(2)
    # On remplace les nuages par une valeur moyenne et une barre d'erreur
    plt.errorbar(x, ym, yerr=yerr, marker='.', color='k', linestyle="", capsize=2.5)
    # On trace la régression avec une ligne pointillée rouge
    plt.plot(x, f(x, *popt), 'r--')
    # On construit un graphique pour comparer la régression pondérée à la
    # régression ordinaire
    plt.figure(3)
    # Faire une régression non pondérée
    popt2, pcov2 = sp_opt.curve_fit(f, x, ym)
    # On remplace les nuages par une valeur moyenne et une barre d'erreur
    plt.errorbar(x, ym, yerr=yerr, marker='.', color='k', linestyle="", capsize=2.5)
    plt.plot(x, f(x,*popt), 'r--', label="Régression pondérée")
    plt.plot(x, f(x, *popt2), 'g--', label="Régression ordinaire")
    # Afficher la légende
    plt.legend(loc="best")
    # On donne des titres aux axes et au graphique
    plt.show()
