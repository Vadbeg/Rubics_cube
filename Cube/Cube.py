import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


class Cubic:
    def __init__(self, number):
        self.edges = 6
        self.number = number
        self.cube = list()
        self.colors = dict(zip(list(range(0, 6)), 6 * [number * number]))
        self.color = {0: 'b', 1: 'g', 2: 'r', 3: 'c', 4: 'y', 5: 'm'}
        self.pltpos = [(0., 0.), (0., 1.05), (2.10, 0.), (0., -1.05), (-1.05, 0.), (1.05, 0.)]

    def create_cube(self):
        self.cube = np.array([[[0 for _ in range(0, self.number)]
                               for _ in range(0, self.number)]
                              for _ in range(0, self.edges)])

        for i in range(0, self.edges):
            for j in range(0, self.number):
                for k in range(0, self.number):
                    self.cube[i][j][k] = i
                    self.colors[i] -= 1

    def rotate(self, index):
        self.cube[index] = np.rot90(self.cube[index])

        if index == 0:
            self.scroll([(1, 'left'), (5, 'left'), (3, 'left'), (4, 'right')])
        elif index == 1:
            self.scroll([(4, 'top'), (2, 'top'), (5, 'top'), (0, 'top')])
        elif index == 2:
            self.scroll([(1, 'right'), (4, 'left'), (3, 'right'), (5, 'right')])
        elif index == 3:
            self.scroll([(5, 'bottom'), (2, 'bottom'), (4, 'bottom'), (0, 'bottom')])
        elif index == 4:
            self.scroll([(1, 'top'), (0, 'left'), (3, 'bottom'), (2, 'right')])
        elif index == 5:
            self.scroll([(1, 'bottom'), (2, 'left'), (3, 'top'), (0, 'right')])

    def get_arr(self, index, align):
        if align == 'left':
            return self.cube[index][:, 0]
        elif align == 'right':
            return self.cube[index][:, 2]
        elif align == 'top':
            return self.cube[index][0, :]
        elif align == 'bottom':
            return self.cube[index][2, :]
        else:
            raise ModuleNotFoundError

    def app_arr(self, index, align, new_arr):
        if align == 'left':
            self.cube[index][:, 0] = new_arr
        elif align == 'right':
            self.cube[index][:, 2] = new_arr
        elif align == 'top':
            self.cube[index][0, :] = new_arr
        elif align == 'bottom':
            self.cube[index][2, :] = new_arr
        else:
            raise ModuleNotFoundError

    def scroll(self, connections):
        new_connections = list()

        for i in range(len(connections)):

            new_arr = deepcopy(self.get_arr(connections[i][0], connections[i][1]))
            new_connections.append(new_arr)

        for i in range(len(new_connections)):

            if i + 1 == len(connections):
                self.app_arr(connections[0][0], connections[0][1], new_connections[i])
                break

            self.app_arr(connections[i + 1][0], connections[i + 1][1], new_connections[i])

    def replace(self):
        draw_cube = deepcopy(self.cube)

        # draw_cube[1] = np.rot90(draw_cube[1], 1)
        draw_cube[2] = np.rot90(draw_cube[2], 3)
        draw_cube[3] = np.rot90(draw_cube[3], 2)
        draw_cube[4] = np.rot90(draw_cube[4], 3)
        draw_cube[5] = np.rot90(draw_cube[5], 3)
        draw_cube[0] = np.rot90(draw_cube[0], 3)

        return draw_cube

    def draw(self, fig):

        ax = fig.add_axes((0, 0, 1, 1), frameon=False,
                          xticks=[], yticks=[])

        draw_cube = self.replace()

        for i in range(len(self.cube)):
            x0, y0 = self.pltpos[i]
            cs = 1. / len(self.cube[0])
            for j in range(len(self.cube[0])):
                for k in range(len(self.cube[0][0])):
                    ax.add_artist(Rectangle((x0 + j * cs, y0 + k * cs), cs, cs,
                                            facecolor=self.color[draw_cube[i][j][k]],
                                            fill=True, edgecolor='k'))

        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

        return None


cubic = Cubic(3)
cubic.create_cube()
# print(cubic.cube)
# cubic.rotate(2)
# cubic.rotate(5)
# print(cubic.cube)

xlim = (-2.4, 3.4)
ylim = (-1.2, 4.)
fig = plt.figure(figsize=((xlim[1] - xlim[0]) * len(cubic.cube[0][0]) / 4., (ylim[1] - ylim[0]) * len(cubic.cube[0][0]) / 4.))


def press(event):
    print('press', event.key)

    fig.canvas.draw()

    if event.key == '0':
        cubic.rotate(0)
        cubic.draw(fig)
    if event.key == '1':
        cubic.rotate(1)
        cubic.draw(fig)
    if event.key == '2':
        cubic.rotate(2)
        cubic.draw(fig)
    if event.key == '3':
        cubic.rotate(3)
        cubic.draw(fig)
    if event.key == '4':
        cubic.rotate(4)
        cubic.draw(fig)
    if event.key == '5':
        cubic.rotate(5)
        cubic.draw(fig)

    fig.canvas.draw()


cubic.draw(fig)
fig.canvas.mpl_connect('key_press_event', press)
plt.show()



