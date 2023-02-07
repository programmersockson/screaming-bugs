import numpy as np
from random import randrange, uniform

from config import *


class Bug:
    dist = HEARING_DISTANCE

    def __init__(self):
        self.state = randrange(0, 5)  # 0-spirit, 1-R, 2-G, 3-B, 4-scout, 5-to queen, 6-qR, 7-qG, 8-qB
        self.position = np.array([randrange(50, WIDTH_CONST - 50), randrange(50, HEIGHT_CONST - 50)], dtype=float)  # cluster within an area
        self.angle = uniform(0, 2 * np.pi)
        self.velocity = uniform(BUG_VELOCITY_MIN, BUG_VELOCITY_MAX)
        self.health = HEALTH + randrange(-HEALTH//5, HEALTH//5)
        self.red = 0
        self.green = 0
        self.blue = 0
        self.distR = ESTIMATED_DISTANCE
        self.distG = ESTIMATED_DISTANCE
        self.distB = ESTIMATED_DISTANCE
        self.distQ = ESTIMATED_DISTANCE
        self.order = 1  # order of cry

    def reproduce(self, bugs):
        for bug in bugs:
            if bug.state == 0:
                bug.state = randrange(1, 5)
                bug.position[0] = self.position[0]
                bug.position[1] = self.position[1]
                bug.angle = uniform(0, 2 * np.pi)
                bug.velocity = uniform(BUG_VELOCITY_MIN, BUG_VELOCITY_MAX)
                bug.health = HEALTH + randrange(-HEALTH//5, HEALTH//5)
                bug.red = 0
                bug.green = 0
                bug.blue = 0
                bug.distR = ESTIMATED_DISTANCE
                bug.distG = ESTIMATED_DISTANCE
                bug.distB = ESTIMATED_DISTANCE
                bug.distQ = ESTIMATED_DISTANCE
                bug.order = 1
                break

    def die(self):
        self.state = 0

    def step(self, bugs, resources):

        self.angle += randrange(-5, 6) / 100  # [-0.05, 0.05]

        # no edgerunners
        if self.position[0] < 10 or self.position[0] > WIDTH_CONST - 10 or self.position[1] < 10 or self.position[1] > HEIGHT_CONST - 10:
            self.angle += np.pi

        self.position[0] += self.velocity * np.sin(self.angle)
        self.position[1] += self.velocity * np.cos(self.angle)

        if self.state >= 6:
            self.step_queen(bugs)
            self.health -= 2  # dies faster, because performs two functions

        elif 1 <= self.state <= 5:
            self.step_worker(bugs, resources)
            self.health -= 1
            self.order += 1
            if self.order == 4:  # nothing pinned
                self.order = 5
            if self.order == 6:  # return to distR
                self.order = 1

        if self.health < 1:
            self.die()

    def step_queen(self, bugs):
        self.distR += 1
        self.distG += 1
        self.distB += 1

        if self.distR >= self.distG and self.distR >= self.distB:
            self.state = 6
        elif self.distG >= self.distR and self.distG >= self.distB:
            self.state = 7
        else:
            self.state = 8

        self.cry_queen(bugs)  # queen's scream

        if self.red > 1 and self.green > 1 and self.blue > 1:
            self.red -= 1
            self.green -= 1
            self.blue -= 1

            if self.health <= (HEALTH + HEALTH//5 - 50) and randrange(100) > 90:
                self.health += 50
            else:
                self.reproduce(bugs)

    def step_worker(self, bugs, resources):
        self.distR += 1
        self.distG += 1
        self.distB += 1
        self.distQ += 1

        # locate resource
        for resource in resources:
            if abs(resource.position[0] - self.position[0]) <= 10 and abs(resource.position[1] - self.position[1]) <= 10:
                cl = resource.color
                st = self.state

                # coronation
                if self.distQ > ESTIMATED_DISTANCE and randrange(1000) > 960:
                    self.state = cl + 5  # same color as absorbed
                    if cl == 1:
                        self.red += resource.stock
                    elif cl == 2:
                        self.green += resource.stock
                    elif cl == 3:
                        self.blue += resource.stock
                    resource.resurrect()
                    self.velocity = QUEEN_VELOCITY  # constant for queen
                    self.red = QUEEN_STOCK
                    self.green = QUEEN_STOCK
                    self.blue = QUEEN_STOCK
                    self.health = HEALTH + HEALTH//5
                    # print('New queen!') # debugging
                    return None  # it's queen now

                if cl == 1:  # red
                    self.distR = 0
                elif cl == 2:  # green
                    self.distG = 0
                elif cl == 3:  # blue
                    self.distB = 0

                # color match
                if cl == st:

                    resource.give()

                    if st == 1 or st == 4:
                        self.red += 1
                    elif st == 2 or st == 4:
                        self.green += 1
                    elif st == 3 or st == 4:
                        self.blue += 1
                    self.angle += np.pi
                    self.state = 5  # to queen

                break

        self.cry_worker(self.order, bugs)

    def cry_queen(self, bugs):
        for bug in bugs:
            if 1 <= bug.state <= 5:  # except dead and queens
                if abs(self.position[0] - bug.position[0]) <= self.dist and abs(self.position[1] - bug.position[1]) <= self.dist:
                    if bug.distQ > self.dist:
                        d = np.linalg.norm(self.position - bug.position)  # euclidean distance
                        if d <= self.dist:
                            bug.distQ = self.dist
                            if bug.state == 5:
                                bug.set_angle(self.position, d)
                                if d < 20:
                                    self.red += bug.red
                                    bug.red = 0
                                    self.green += bug.green
                                    bug.green = 0
                                    self.blue += bug.blue
                                    bug.blue = 0
                                    bug.state = randrange(1, 5)
                                    bug.angle = uniform(0, 2 * np.pi)

    def cry_worker(self, order, bugs):
        if order == 1:  # red
            for bug in bugs:
                if abs(self.position[0] - bug.position[0]) <= self.dist and abs(self.position[1] - bug.position[1]) <= self.dist:
                    if bug.distR > self.distR + self.dist:
                        d = np.linalg.norm(self.position - bug.position)  # euclidean distance
                        if d <= self.dist:
                            bug.distR = self.distR + self.dist
                            if bug.state == 1 or bug.state == 6:
                                bug.set_angle(self.position, d)
        elif order == 2:  # green
            for bug in bugs:
                if abs(self.position[0] - bug.position[0]) <= self.dist and abs(self.position[1] - bug.position[1]) <= self.dist:
                    if bug.distG > self.distG + self.dist:
                        d = np.linalg.norm(self.position - bug.position)  # euclidean distance
                        if d <= self.dist:
                            bug.distG = self.distG + self.dist
                            if bug.state == 2 or bug.state == 7:
                                bug.set_angle(self.position, d)
        elif order == 3:  # blue
            for bug in bugs:
                if abs(self.position[0] - bug.position[0]) <= self.dist and abs(self.position[1] - bug.position[1]) <= self.dist:
                    if bug.distB > self.distB + self.dist:
                        d = np.linalg.norm(self.position - bug.position)  # euclidean distance
                        if d <= self.dist:
                            bug.distB = self.distB + self.dist
                            if bug.state == 3 or bug.state == 8:
                                bug.set_angle(self.position, d)
        elif order == 5:  # to queen
            for bug in bugs:
                if abs(self.position[0] - bug.position[0]) <= self.dist and abs(self.position[1] - bug.position[1]) <= self.dist:
                    if bug.distQ > self.distQ + self.dist:
                        d = np.linalg.norm(self.position - bug.position)  # euclidean distance
                        if d <= self.dist:
                            bug.distQ = self.distQ + self.dist
                            if bug.state == 5:
                                bug.set_angle(self.position, d)

    def set_angle(self, position_to_go, distance):
        x_to = position_to_go[0]
        y_to = position_to_go[1]
        x_from = self.position[0]
        y_from = self.position[1]
        angle = np.arccos((y_to - y_from) / distance)
        if x_to > x_from:
            self.angle = angle
        else:
            self.angle = 2 * np.pi - angle
