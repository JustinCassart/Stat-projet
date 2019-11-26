import numpy as np 
import os.path

def extract_data(filename):
    if not os.path.isfile(filename):
        raise FileNotFoundError
    else:
        datas = []
        with open(filename) as file:
            for line in file:
                data = tuple(line.split())
                datas.append(data)
    return np.array(datas)

def extract_systems(datas):
    n_syst = len(datas[0])-1 # Il faut retirer les x
    systems = []
    for i in range(n_syst):
        systems.append((datas[:,0], datas[:,i+1]))
    return np.array(systems)

def reording(datas):
    x = datas[0]
    y = datas[1]
    i = 0
    v = x[i]
    new_data = [[float(v)]]
    while i < len(x):
        if x[i] != v:
            new_data.append([float(x[i])])
            v = x[i]
        new_data[-1].append(float(y[i]))
        i += 1
    return np.array(new_data)

def extract(filename):
    d = [reording(i) for i in extract_systems(extract_data(filename))]
    return np.array(d)
