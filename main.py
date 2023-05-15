import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import bugclass as bc
import resourceclass as rc
from config import *

import time

# for animating frame by frame in PyCharm
# import matplotlib
# matplotlib.use("TkAgg")

t0 = time.time()

fig, ax = plt.subplots()
ax.set_xlim(0, WIDTH_CONST)
ax.set_ylim(0, HEIGHT_CONST)
plt.axis('off')

# initialise resources
resources = [rc.Resource() for i in range(RESOURCES_AMOUNT)]
resourcesLine = []

for i in range(RESOURCES_AMOUNT):
    res, = ax.plot([], [], marker='o', markersize=15)
    resourcesLine.append(res)

c = RESOURCE_STOCK/15

# initialise bugs
bugs = [bc.Bug() for i in range(MAX_BUGS_AMOUNT)]
bugsLine = []

for i in range(MAX_BUGS_AMOUNT):
    bug, = ax.plot([], [], 'ko', markersize=0.5)
    bugsLine.append(bug)

# initialise first queen
bugs[0].state = 6
bugs[0].red = QUEEN_STOCK
bugs[0].green = QUEEN_STOCK
bugs[0].blue = QUEEN_STOCK
bugs[0].velocity = QUEEN_VELOCITY
bugs[0].position[0] = WIDTH_CONST / 2
bugs[0].position[1] = HEIGHT_CONST / 2
bugs[0].health = HEALTH + HEALTH//2

bugsLine[0].set_marker('o')
bugsLine[0].set_markersize(13)
bugsLine[0].set_markerfacecolor('tab:orange')
bugsLine[0].set_markeredgecolor('y')


def animate(frames):
    for i in range(RESOURCES_AMOUNT):

        res = resourcesLine[i]
        resobj = resources[i]
        res.set_markersize(resobj.stock / c)
        if resobj.color == 1:
            res.set_markerfacecolor('r')
            res.set_markeredgecolor('r')
        elif resobj.color == 2:
            res.set_markerfacecolor('g')
            res.set_markeredgecolor('g')
        elif resobj.color == 3:
            res.set_markerfacecolor('b')
            res.set_markeredgecolor('b')

        res.set_data([resobj.position[0], resobj.position[1]])
        resobj.step()

    curbugs = 0
    for i in range(MAX_BUGS_AMOUNT):

        bug = bugsLine[i]
        bugobj = bugs[i]
        if bugobj.state == 0:
            bug.set_markersize(0)
            continue
        elif 1 <= bugobj.state <= 4:
            bug.set_markersize(0.5)
            bug.set_markerfacecolor('k')
        elif bugobj.state == 5:
            bug.set_marker('o')
            bug.set_markersize(3)
            bug.set_markeredgewidth(0)
            if bugobj.red != 0:
                bug.set_markerfacecolor('r')
            elif bugobj.green != 0:
                bug.set_markerfacecolor('g')
            else:
                bug.set_markerfacecolor('b')
        elif bugobj.state > 5:
            # bug.set_marker('o')
            # bug.set_markersize(13)
            # bug.set_markerfacecolor('tab:orange')
            # bug.set_markeredgecolor('y')
            if (HEALTH + HEALTH//2) / bugobj.health >= 11:
                bug.set_markeredgewidth(11)
            else:
                bug.set_markeredgewidth((HEALTH + HEALTH//2) / bugobj.health - 1)

        bug.set_data([bugobj.position[0], bugobj.position[1]])
        bugobj.step(bugs, resources)
        curbugs += 1
    ax.set_title(f'Bug amount: {curbugs}')
    return resourcesLine, bugsLine


anim = FuncAnimation(fig, animate, frames=FRAMES, interval=INTERVAL)
# plt.show()
anim.save(FILE_NAME, writer="Pillow", fps=FPS)

print(time.time() - t0)

