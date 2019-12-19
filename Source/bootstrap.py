import Source.regression as regression
import random
import numpy

def bootstrap(x, y_hat, y_mean, B = 100):
    residus = []
    for i in range(len(y_hat)):
        residus.append(y_mean[i] - y_hat[i])
    alpha = []
    beta = []
    for _ in range(B):
        random.shuffle(residus)
        y = []
        for i in range(len(y_hat)):
            y.append(y_hat[i] + residus[i])
        v = []
        for i in range(len(x)):
            v.append([x[i], y[i]])
        v = numpy.array(v)
        a,b = regression.alpha_beta_calculator(v)
        alpha.append(a)
        beta.append(b)
    alpha_bar, beta_bar = 0, 0
    for i in range(len(alpha)):
        alpha_bar += alpha[i]
        beta_bar += beta[i]
    alpha_bar /= B
    beta_bar /= B
    return alpha_bar, beta_bar