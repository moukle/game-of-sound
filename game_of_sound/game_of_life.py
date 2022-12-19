import numpy as np
import pygame

class GameOfLife:
    def __init__(self, height, width, cellsize):
        self.height = height
        self.width = width
        self.cellsize = cellsize

        # init grid
        threshold = 0.6
        self.grid = np.random.rand(height, width)
        self.grid = self.grid > threshold
        self.updated_grid = np.zeros_like(self.grid)

        pygame.init()
        pygame.display.set_caption("Game of Sound")
        self.surface = pygame.display.set_mode((width*cellsize, height*cellsize))


    def step(self) -> None:
        # check rules for each cell
        for i in range(self.width):
            for j in range(self.height):
                self.update_cell(idx=(i,j))

        # once completed, update all cells for epoch
        self.grid = self.updated_grid.copy()

    def update_cell(self, idx) -> None:
        # kernel size used for striding over the grid (aka neighbors in xy dir)
        # ks = 3
        k1 = 1
        k2 = 2

        i, j = idx
        alive_neighbors = np.sum(self.grid[i-k1:i+k2,
                                            j-k1:j+k2]
                                ) - self.grid[i,j]

        # If a cell is ON and has fewer than two neighbors that are ON, it turns OFF.
        # If a cell is ON and has either two or three neighbors that are ON, it remains ON.
        # If a cell is ON and has more than three neighbors that are ON, it turns OFF.
        # If a cell is OFF and has exactly three neighbors that are ON, it turns ON.
        if       self.grid[idx] and alive_neighbors < 2:       self.updated_grid[idx] = False
        elif     self.grid[idx] and alive_neighbors in [2, 3]: self.updated_grid[idx] = True
        elif     self.grid[idx] and alive_neighbors > 3:       self.updated_grid[idx] = False
        elif not self.grid[idx] and alive_neighbors == 3:      self.updated_grid[idx] = True

    def draw(self):
        col_alive = (55, 55, 55)
        col_background = (10, 10, 10)

        # col_grid = (30, 30, 60)
        # col_about_to_die = (200, 200, 225)

        cs = self.cellsize

        for i in range(self.width):
            for j in range(self.height):
                col = col_alive if self.grid[i,j] else col_background

                pygame.draw.rect(self.surface, col, (i*cs, j*cs, cs, cs))
        pygame.display.update()