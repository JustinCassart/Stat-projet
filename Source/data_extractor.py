import numpy as np 
import os.path

def extract_data(filename):
    """
    Permet de récupérer les données brutes contenue dans un fichier

    input : filename, le fichier contenant les données à extraire
    output : les données telle qu'elles sont dans le fichier
    effect : None
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError
    else:
        datas = []
        with open(filename) as file:
            for line in file:
                data = tuple(line.split())
                datas.append(data)
    return np.array(datas)

def reording(data):
    """
    Réarange les données selon les valeurs en x

    input : data, une liste de liste contenant les données à trier
    output : une liste contenant les sytèmes triés
    effect : None
    """
    n_syst = len(data[0]) - 1
    systems = []
    for _ in range(n_syst):
        systems.append([])
    current_x = None
    for line in data:
        l = [float(i) for i in line]
        if l[0] != current_x:
            current_x = l[0]
            for i in range(n_syst):
                systems[i].append([current_x])
        for i in range(n_syst):
            systems[i][-1].append(l[i + 1])
    return systems

def extract(filename):
    """
    Permet d'extraire les données d'un fichier

    input : filename, le fichier contenant les données à extraire
    output : une array contenant les données triées par système et valeur en x
    effect : None
    """
    d = reording(extract_data(filename))
    for i in range(len(d)):
        file_name = "processeur{}.txt".format(i+1)
        f = open(file_name, "w")
        for line in d[i]:
            message = " ".join([str(i) for i in line])
            message += "\n"
            f.write(message)
        f.close
    return np.array(d)

if __name__ == "__main__":
    data = extract("datas.dat")
    for i in range(len(data)):
        with open("processeur{}".format(i+1), "w") as file:
            for line in data[i]:
                to_write = " ".join([str(i) for i in line])
                to_write += "\n"
                file.write(to_write)
    # data = reording(data)
    # print("number of syst", len(data))
    # print("number of triangle", len(data[0]))
    # print("number of value for 10000", len(data[0][0]))
    # data2 = extract("datas.dat")
    # print(len(data))
    # print(len(data[0]))
    # print(len(data[0][0]))