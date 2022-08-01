import numpy as np
from zeroconf import current_time_millis

class board():
    def __init__(self, ones, size, generations):
        self.size = size
        self.ones = ones
        self.grid = np.zeros((self.size, self.size))
        for i,j in ones:
            self.grid[i,j] = 1
        self.history = [self.grid]
        self.generations = generations
        self.iterate()
        
    def iterate(self):
        current_iteration = self.generations
        while current_iteration > 0:
            temp = np.array(self.grid, copy=True)
            for i in range(self.size):
                for j in range(self.size):
                    neighbors = 0
                    if i == 0:
                        if j == 0:
                            neighbors = self.grid[i+1,j] + self.grid[i+1,j+1] + self.grid[i,j+1]
                        elif j == self.size - 1:
                            neighbors = self.grid[i+1,j] + self.grid[i+1,j-1] + self.grid[i,j-1]
                        else:
                            neighbors = self.grid[i+1,j] + self.grid[i+1,j-1] + self.grid[i+1,j+1] + self.grid[i,j-1] + self.grid[i,j+1]
                    elif j == 0:
                        if i == self.size - 1:
                            neighbors = self.grid[i,j+1] + self.grid[i-1,j+1] + self.grid[i-1,j]
                        else:
                            neighbors = self.grid[i+1,j] + self.grid[i+1,j+1] + self.grid[i-1,j] + self.grid[i-1,j+1] + self.grid[i,j+1]
                    elif i == self.size - 1:
                        neighbors = self.grid[i-1,j] + self.grid[i-1,j+1] + self.grid[i-1,j-1] + self.grid[i,j+1]  + self.grid[i,j-1]
                    elif j == self.size -1:
                        neighbors = self.grid[i-1,j] + self.grid[i+1,j] + self.grid[i,j-1] + self.grid[i-1,j-1] + self.grid[i+1,j-1]
                    else:
                        neighbors = (self.grid[i-1,j] + self.grid[i-1,j-1] + self.grid[i-1,j+1]
                                    +self.grid[i,j-1] + self.grid[i,j+1]
                                    +self.grid[i+1,j] + self.grid[i+1,j+1] + self.grid[i+1,j-1])
                    if self.grid[i,j] == 0 and neighbors == 3:
                        temp[i,j] = 1
                    elif self.grid[i,j] == 1 and (neighbors not in {2,3}):
                        temp[i,j] = 0
            self.history.append(np.array(temp, copy=True))
            self.grid = np.array(temp, copy=True)
            current_iteration -= 1
