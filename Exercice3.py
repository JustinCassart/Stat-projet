#!/usr/bin/python3
# -*- coding:utf-8 -*-

# Import modules

# Importer numpy pour l'utilisation des arrays
import numpy as np
# Importer matplotlib.pyplot pour tracer les graphiques
import matplotlib.pyplot as plt
# Importer sicpy.optimize pour effectuer la régression
import scipy.optimize as sp_opt


def compute_means_and_erros(data):
    """
    Fonction qui calcule le vecteur avec les moyennes des variables dépendantes
    ainsi que le vecteur avec les écart-types des variables dépendantes.

    Paramètres:
    -----------
    data: array
        Contient les données sur lesquels effectuer la régression.
        La première colonne doit être la variable explicative.
        Les autres colonnes doivent représenter chaque série de mesures de la
        variable dépendante.
    Return:
    -------
    ym : array
        Les valeurs moyennes
    yerr: array
        Les valeurs pour les écart-types.
        Si l'échantillon des variables dépendantes est de taille 1, on retourne
        une liste vide
    """
    # Récupérer les valeurs de la variable explicative
    x = data[:, 0]
    # Récupérer les valeurs de la variable dépendante
    y = data[:, 1:]
    # Regarder la forme de y (n lignes et k colonnes). Le nombre de lignes
    # est égal au nombre de variables explicatives. Le nombre de colonnes
    # est égal au nombre de mesures correspondant à chaque variable explicative
    n, k = y.shape

    # Si on possède plus d'une mesure par variable explicative on construit
    # le vecteur avec les valeurs moyennes et le vecteur avec les poids
    ym = np.zeros(n)
    yerr = np.zeros(n)
    if k > 1:
        for i in range(n):
            # Calcul du vecteur avec les moyennes
            ym[i] = np.mean(y[i, :])
            # Calcul du vecteur avec les erreurs
            yerr[i] = np.std(y[i, :])
        return ym, yerr
    # Si on a une unique valeur de la variable dépendante pour chaque valeur de
    # la variable explicative, il n'y pas une erreur connue, on retourne donc 
    # un vecteur vide
    return y, []
    

def optimal_parameters(data):
    """
    Fonction qui calcule les meilleurs paramètres au sens des moindres carrés
    pour une régression linéaire.

    Paramètre:
    ----------
    data: array
        Contient les données sur lesquels effectuer la régression.
        La première colonne doit être la variable explicative.
        Les autres colonnes doivent représenter chaque série de mesures de la
        variable dépendante.
    Return:
    ---------
    popt: array
        Vecteur qui contient les paramètres optimaux.
        Le premier élément est la pente et le second l'ordonée à l'origine.
    """

    # Récupérer les valeurs de la variable explicative
    x = data[:, 0]
    # Récupérer les valeurs de la variable dépendante
    y = data[:, 1:]
    # Regarder la forme de y (n lignes et k colonnes). Le nombre de lignes
    # est égal au nombre de variables explicatives. Le nombre de colonnes
    # est égal au nombre de mesures correspondant à chaque variable explicative
    n, k = y.shape

    # Calculer le vecteur avec les moyennes et celui avec les écart-types pour
    # la variable dépendante
    ym, yerr = compute_means_and_erros(data)
    # print(ym)
    # print(yerr)
    # Calculer le vecteur poids s'il y a une erreur connue sur les y
    if len(yerr):
        w = 1/(yerr**2)
    # Si on ne connait pas l'erreur, un même poids (1) est donné à tous les
    # couples (xi, yi)
    else:
        w = np.ones(n)
    # print(w)

    # On va maintenant calculer la matrice A à inverser et la matrice des termes
    # indépendants b
    A = np.zeros((2,2))
    b = np.zeros(2)

    # On va faire une boucle pour ajouter un a un les termes de la somme
    # Voir les slides pour comprendre chacun des termes
    # print(n)
    # print(x)
    for i in range(n):
        A[0][0] += w[i]*x[i]*x[i]
        A[0][1] += w[i]*x[i]
        A[1][1] += w[i]
        b[0] += w[i]*ym[i]*x[i]
        b[1] += w[i]*ym[i]
    # Les élements hors diagonale sont égaux
    A[1][0] = A[0][1]
    print("A00", A[0][0])
    print("A01", A[0][1])
    print("A10", A[1][0])
    print("A11", A[1][1])
    print("b0", b[0])
    print("b1", b[1])
    # La matrice inverse se calcule via le module d'algèbre linéaire de numpy
    # numpy.linalg avec la fonction inv
    # Le produit matriciel se fait avec la fonction numpy.dot
    return np.dot(np.linalg.inv(A), b)


def SST(y, w):
    ym = np.mean(y)
    return np.sum(w*(y-ym)**2)


def SSE(y, yhat, w):
    ym = np.mean(y)
    return np.sum(w*(yhat-ym)**2)


def SSR(y, yhat, w):
    return np.sum(w*(y-yhat)**2)


def determination_coeff(y, yhat, w):
    return SSE(y, yhat, w)/SST(y, w)


if __name__ == "__main__":
    data_exo3 = np.array([
            [1040, 7.4],
            [1230, 6],
            [1500, 4.5],
            [1600, 3.8],
            [1740, 2.9],
            [1950, 1.9],
            [2200, 1],
            [2530, -1.2],
            [2800, -1.5],
            [3100, -4.5]])

    # On calcule les paramètres optimaux avec les matrices
    mpopt = optimal_parameters(data_exo3)
    print("Mes paramètres optimaux sont :")
    print("Pente : %.3e °C/m" % mpopt[0])
    print("Ordonnée à l'origine : %.3e °C\n" % mpopt[1])

    # On effectue la régression avec scipy
    # On commence par définir la fonction f linéaire
    f = lambda x, a, b : a*x+b
    # On définit x
    x = data_exo3[:, 0]
    # On définit y
    y = data_exo3[:, 1]
    # On fait la régression
    popt, pcov = sp_opt.curve_fit(f, x, y)

    print("Les paramètres de régression python sont :")
    print("Pente : %.3e °C/m" % popt[0])
    print("Ordonnée à l'origine : %.3e °C/m" % popt[1])

    # Calculer le coéfficient de détermation
    print("Le R² est de %.3f" % determination_coeff(y, f(x, *popt), np.ones(len(x))))

    # On prédit la température à 1100 m
    expected_temp = f(1100, *popt)
    print("On prévoit une température de % .3e °C" % expected_temp)

    # On trace les données avec des points noirs
    plt.plot(x, y, 'k.')
    # On trace la régression avec une ligne pointillée rouge
    plt.plot(x, f(x, *popt), 'r--')
    # On donne des titres aux axes et au graphique
    plt.xlabel("Altitude (m)")
    plt.ylabel("Température (°C)")
    plt.title("Evolution de la température en fonction de l'altitude")
    plt.show()