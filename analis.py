import io

import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk, ImageSequence
from matplotlib import cm
from matplotlib.backends.backend_tkagg import FigureCanvasAgg
from matplotlib.ticker import NullFormatter  # useful for `logit` scale

import evolution
def start():
    vec = []
    for i in range(5, 41):
        a = evolution.Genetic(100, 0.1, i, 0.1, 50, evolution.F, -30, 30)
        a.startGenetic()
        vec.append(a)
        print(i)
    vec1 = [i.numberLives for i in vec]
    fig, ax = plt.subplots()
    ax.plot(range(5, 41), vec1, color='red')
    ax.set_xlabel('Количество шагов мутации')
    ax.set_ylabel('Количество шагов эволюции')
    fig.suptitle('Зависимость скорости сходимости алгоритма от количества шагов мутации')
    fig.savefig('analis4.png')



