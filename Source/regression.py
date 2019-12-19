from Source.utils import moyennes, variances, mean_error_calculator
import numpy

def alpha_beta_calculator(processor, id_processor = None):
    # print(processor)
    x = processor[:,0]
    y = processor[:,1:]
    y_mean, y_err = mean_error_calculator(processor)
    if any(y_err) == 0: # dans le cas du bootstrap
        weight = numpy.ones(len(y))
    else:
        weight = 1/(y_err ** 2)
    A = numpy.zeros((2,2))
    b = numpy.zeros(2)
    for i in range(len(y)):
        A[0][0] += weight[i] * (x[i] ** 2)
        A[0][1] += weight[i] * x[i]
        A[1][0] += weight[i] * x[i]
        A[1][1] += weight[i]
        b[0] += weight[i] * y_mean[i] * x[i]
        b[1] += weight[i] * y_mean[i]
    alpha, beta = numpy.dot(numpy.linalg.inv(A),b)
    alpha_error = beta_error = 0
    if id_processor:
        message = "alpha : {} précision : {}\nbeta : {} précision {}".format(alpha, alpha_error, beta, beta_error)
        f = open("processeur{}_regression.txt".format(id_processor), "w")
        f.write(message)
        f.close()
    return alpha, beta


def SST(y, y_bar, y_hat, weight, y_mean):
    r = 0
    for i in range(len(y)):
        r += weight[i] * (y_mean[i] - y_bar) ** 2
    return r

def SSE(y, y_hat, y_bar, weight):
    r = 0
    for i in range(len(y)):
        r += weight[i] * (y_hat[i] - y_bar) ** 2
    return r

def SSR(y, y_hat, y_bar, weight):
    r = 0
    for i in range(len(y)):
        r += weight[i] * (y_bar - y_hat[i]) ** 2
    return r

def quality(processor, alpha, beta):
    f = lambda x : alpha * x + beta
    x = processor[:,0]
    y = processor[:,1:]
    y_hat = f(x)
    y_mean, y_err = mean_error_calculator(processor)
    y_bar = numpy.sum(y_mean)
    weight = 1 / (y_err ** 2)
    return SSE(y,y_hat, y_bar, weight) / SST(y,y_bar, y_hat, weight, y_mean)