import pygame
from typing import Callable, List
import random


class MazeDensity:
    NORMAL = 4
    HIGH = 2
    LOW = 8


class Colors:
    RED = (255, 255, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 255, 0)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PURPLE = (128, 0, 128)
    ORANGE = (255, 165, 0)
    GREY = (128, 128, 128)
    TURQUOISE = (64, 224, 208)


class Cell:
    """
    This class represents a cell in the grid
    Each cell has a complete set of functions and properties and capable of changing states visually
    """

    def __init__(self, row: int, col: int, width: int, height: int, total_rows: int, total_cols: int,
                 dig_move: bool = True):
        self._c = Colors()
        self.color = self._c.WHITE
        self.x = row * width
        self.y = col * height
        self.row = row
        self.col = col
        self.width = width
        self.neighbors = []
        self.height = height
        self.total_rows = total_rows
        self.total_cols = total_cols
        self.dig_move = dig_move

    def get_pos(self) -> tuple:
        """
        Returns the position of a cell in the grid as a tuple
        :return: Tuple
        """
        return self.row, self.col

    def is_closed(self) -> bool:
        return self.color == self._c.RED

    def is_open(self) -> bool:
        return self.color == self._c.GREEN

    def is_barrier(self) -> bool:
        return self.color == self._c.BLACK

    def is_start(self) -> bool:
        return self.color == self._c.ORANGE

    def is_end(self) -> bool:
        return self.color == self._c.TURQUOISE

    def reset(self):
        self.color = self._c.WHITE

    def make_start(self):
        self.color = self._c.ORANGE

    def make_current(self):
        self.color = self._c.RED

    def make_closed(self):
        self.color = self._c.RED

    def make_open(self):
        self.color = self._c.GREEN

    def make_barrier(self):
        self.color = self._c.BLACK

    def make_end(self):
        self.color = self._c.TURQUOISE

    def make_path(self):
        self.color = self._c.PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

        if self.dig_move:
            if self.col > 0 and self.row > 0 and not grid[self.row - 1][self.col - 1].is_barrier():  # LEFT UP Dig
                self.neighbors.append(grid[self.row - 1][self.col - 1])

            if self.col < self.total_cols - 1 and \
                    self.row < self.total_rows - 1 and not \
                    grid[self.row + 1][self.col + 1].is_barrier():  # RIGHT UP Dig

                self.neighbors.append(grid[self.row + 1][self.col + 1])

            if self.col > 0 and \
                    self.row < self.total_rows - 1 and not \
                    grid[self.row + 1][self.col - 1].is_barrier():  # LEFT DOWN Dig

                self.neighbors.append(grid[self.row + 1][self.col - 1])

            if self.col < self.total_cols - 1 and \
                    self.row < self.total_rows - 1 and not \
                    grid[self.row + 1][self.col + 1].is_barrier():  # RIGHT DOWN Dig

                self.neighbors.append(grid[self.row + 1][self.col + 1])

    def __lt__(self, other):
        return False


class GuiManager:
    def __init__(self):
        self.c = Colors()

    @staticmethod
    def reconstruct_path(parent_node: dict, current_node: Cell, draw_func: Callable) -> None:
        while current_node in parent_node:
            current_node = parent_node[current_node]
            current_node.make_path()
            draw_func()

    @staticmethod
    def draw_maze(rows, cols, density: int, grid: List[List[Cell]]):
        for i in range(rows // density):
            for spot in grid:
                rand = random.randrange(0, rows)
                cell = spot[rand]
                if cell.is_barrier():
                    continue
                spot[rand].make_barrier()

    @staticmethod
    def make_grid(rows: int, cols: int, width: int, height: int, dig_moves: bool) -> List[List[Cell]]:
        grid = []
        gap = width // rows
        for i in range(rows):
            grid.append([])
            for j in range(cols):
                spot = Cell(i, j, gap, height // cols, rows, cols, dig_moves)
                grid[i].append(spot)

        return grid

    def draw_grid(self, win, rows: int, cols: int, width: int, height: int) -> None:
        gap = width // rows
        for i in range(rows):
            pygame.draw.line(win, self.c.GREY, (0, i * gap), (width, i * gap))
            for j in range(cols):
                pygame.draw.line(win, self.c.GREY, (j * gap, 0), (j * gap, height))

    def draw(self, win, grid: List[List[Cell]], rows: int, cols: int, width: int, height: int) -> None:
        win.fill(self.c.WHITE)

        for row in grid:
            for spot in row:
                spot.draw(win)

        self.draw_grid(win, rows, cols, width, height)
        pygame.display.update()

    @staticmethod
    def get_clicked_pos(pos: tuple, rows: int, width: int) -> tuple:
        gap = width // rows
        y, x = pos

        row = y // gap
        col = x // gap

        return row, col
