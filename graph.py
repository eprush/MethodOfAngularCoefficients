from matplotlib import pyplot as plt
import numpy as np
import os


def name(title):
    if title:
        plt.title(title, color="red", size=30)
    return


def save_graph(filename, dirname):
    old_dir = os.getcwd()
    if dirname and (not os.path.isdir(dirname)):
        os.mkdir(dirname)
    os.chdir(dirname)
    if filename:
        plt.savefig(filename)
    os.chdir(old_dir)
    return


def customize_graph(title="", label_x="", label_y=""):
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111)
    ax.tick_params(axis="x", colors="red", size=10)
    ax.tick_params(axis="y", colors="red", size=10)

    plt.grid()
    plt.xticks(size=20)
    plt.yticks(size=20)
    plt.xlabel(label_x, size=30, color="red")
    plt.ylabel(label_y, size=30, color="red")

    name(title)
    return


class Graph:
    def __init__(self):
        # данные взяты из ссылки №2 Links.txt
        k = [1, 0.9092, 0.8341, 0.7711, 0.7177, 0.6720, 0.6320, 0.5970, 0.5659, 0.5384, 0.5136, 0.4914, 0.4711]
        k += [0.4527, 0.4359, 0.4205, 0.4062, 0.3931, 0.3809, 0.3695, 0.3589, 0.3146, 0.2807, 0.2537, 0.2316]
        k += [0.2131, 0.1973, 0.1719, 0.1523, 0.1367, 0.1240, 0.1135]
        k = np.array(k)
        self.k = k
