import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import style
import numpy as np
import multiprocessing

style.use("ggplot")

t = np.linspace(0, 20, 400)

def plot_response(poles, continuous=True):
    plt.clf()
    if continuous:
        y = generate_cont_resp_func(poles)
        plt.plot(t, [y(t[i]) for i in range(len(t))])

def generate_cont_resp_func(poles):
    def y(t):
        _y = 0
        for pole in poles:
            _y += np.exp(pole[0] * t) * np.cos(pole[1] * t)
        return _y

    return y

def read_poles():
    with open("poles.txt", "r") as pole_file:
        poles_str = pole_file.read().rstrip()
        return [] if poles_str == "" else list(map(lambda p: list(map(float, p.split(","))),
                                                poles_str.split(" ")))

def animate(_):
    poles = read_poles()
    plot_response(poles)

def run():
    ani = FuncAnimation(plt.gcf(), animate, interval=50)
    print("Showing graph")
    plt.show()

thread = multiprocessing.Process(target=run)
