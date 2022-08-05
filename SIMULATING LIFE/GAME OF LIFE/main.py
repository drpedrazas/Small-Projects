from socketserver import BaseRequestHandler
from grid import board
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time
from tkinter import *
root = Tk()
done = True
def doneq():
    global done
    done = False
button = Button(root, text="Done", command=doneq)
button.pack()
grid_size = 30
dummy_grid = np.zeros((grid_size,grid_size))
fig = plt.figure(figsize=(5,5))
ax = plt.axes()
#plotting this grid, it's boring for now, all white, since the grid is nothing but zeros
im = ax.imshow(dummy_grid,cmap='binary')
for n in range(0,len(dummy_grid)):
    plt.axvline(.5+n)
    plt.axhline(.5+n)
startup_points = []
while done:
    pt = plt.ginput(1, timeout=2)
    print(pt)
    if pt == []:
        if not done:
            break
        else:
            continue
    #getting coordinates, rounded to whole numbers
    p_1 = int(round(pt[0][1],0))
    p_2 = int(round(pt[0][0],0))
    coord = (p_1,p_2)
    print(coord)
    #updating the tracking of which points have been selected, and changing the display grid
    if coord in startup_points:
        dummy_grid[p_1][p_2] = 0
        startup_points.remove(coord)
    else:
        dummy_grid[p_1][p_2] = 1
        startup_points.append(coord)
    #update the displayed grid
    plt.imshow(dummy_grid,cmap='binary')
aut = board(startup_points,grid_size,100)
def update(frame_num,img):
    print(frame_num)
    newGrid = aut.history[frame_num]
    img.set_data(newGrid)
updateInterval = 100
grid = dummy_grid
fig, ax = plt.subplots()
img = ax.imshow(grid, interpolation='nearest')
ani = animation.FuncAnimation(fig, update, fargs=(img, ),
frames=100,
interval=updateInterval,
save_count=100)
plt.show()