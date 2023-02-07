import numpy as np
from random import randrange, uniform

from config import HEIGHT_CONST
from config import WIDTH_CONST
from config import RESOURCE_STOCK
from config import RESOURCE_VELOCITY


class Resource:

    def __init__(self):
        self.position = np.array([randrange(50, WIDTH_CONST - 50), randrange(50, HEIGHT_CONST - 50)], dtype=float)  # cluster within an area
        self.angle = uniform(0, 2 * np.pi)
        self.velocity = RESOURCE_VELOCITY  # constant for resource
        self.color = randrange(1, 4)  # 1 is red, 2 is green, 3 is blue
        self.stock = RESOURCE_STOCK

    def give(self):
        self.stock -= 1
        if self.stock == 0:
            self.resurrect()

    def resurrect(self):
        self.position = np.array([randrange(50, WIDTH_CONST - 50), randrange(50, HEIGHT_CONST - 50)], dtype=float)
        self.color = randrange(1, 4)
        self.stock = RESOURCE_STOCK

    def step(self):
        self.angle += randrange(-10, 11) / 100  # [-0.01, 0.01]
        # no edgerunners
        if self.position[0] < 10 or self.position[0] > WIDTH_CONST - 10 or self.position[1] < 10 or self.position[1] > HEIGHT_CONST - 10:
            self.angle += np.pi

        self.position[0] += self.velocity * np.sin(self.angle)
        self.position[1] += self.velocity * np.cos(self.angle)
        pass
