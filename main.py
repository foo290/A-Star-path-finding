import pygame
from typing import List

from algo import AlgorithmAStar
from gui import GuiManager, Cell, MazeDensity


class Driver:
    def __init__(
            self,
            rows: int = 50,
            cols: int = 50,
            width: int = 500,
            height: int = 500,
            fps: int = 30,
            diagonal_move: bool = True,
            win_name: str = "A* Path Finding Algorithm"

    ):
        self._rows = rows
        self._cols = cols
        self._width = width
        self._height = height
        self._win_name = win_name
        self.dig_moves = diagonal_move

        pygame.init()
        self._window = pygame.display.set_mode((self._width, self._height), pygame.RESIZABLE)
        pygame.display.set_caption(self._win_name)

        self._gui = GuiManager()
        self._algo = AlgorithmAStar()

        self._running_loop = True

        self._start: Cell = None
        self._end: Cell = None

        self._grid: List[List[Cell]] = self._gui.make_grid(self._rows, self._cols, self._width, self._height,
                                                           self.dig_moves)
        self.fps = fps

    def create_maze(self, density):
        self._gui.draw_maze(self._rows, self._cols, density, self._grid)

    def allow_diagonal_moves(self, allow: bool):
        self.dig_moves = allow

    def run_main_loop(self):
        while self._running_loop:
            self._gui.draw(self._window, self._grid, self._rows, self._cols, self._width, self._height)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._algo.stop_algo()
                    self._running_loop = False

                if pygame.mouse.get_pressed()[0]:  # LEFT
                    pos = pygame.mouse.get_pos()
                    row, col = self._gui.get_clicked_pos(pos, self._rows, self._width)
                    spot = self._grid[row][col]
                    if not self._start and spot != self._end:
                        self._start = spot
                        self._start.make_start()

                    elif not self._end and spot != self._start:
                        self._end = spot
                        self._end.make_end()

                    elif spot != self._end and spot != self._start:
                        spot.make_barrier()

                elif pygame.mouse.get_pressed()[2]:  # RIGHT
                    pos = pygame.mouse.get_pos()
                    row, col = self._gui.get_clicked_pos(pos, self._rows, self._width)
                    spot = self._grid[row][col]
                    spot.reset()
                    if spot == self._start:
                        self._start = None
                    elif spot == self._end:
                        self._end = None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self._start and self._end:
                        for row in self._grid:
                            for spot in row:
                                spot.update_neighbors(self._grid)

                        draw_func = lambda: self._gui.draw(self._window, self._grid, self._rows, self._cols,
                                                           self._width, self._height)
                        if found := self._algo.algo(draw_func, self._grid, self._start, self._end, self.fps):
                            parent_nodes, end_node, *_ = found
                            self._gui.reconstruct_path(parent_nodes, end_node, draw_func)
                            end_node.make_end()

                    elif event.key == pygame.K_c:
                        pos = pygame.mouse.get_pos()
                        row, col = self._gui.get_clicked_pos(pos, self._rows, self._width)
                        spot = self._grid[row][col]
                        spot.reset()
                        if spot == self._start:
                            self._start = None
                        elif spot == self._end:
                            self._end = None

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and not self._start:
                            pass
        pygame.quit()


if __name__ == '__main__':
    main = Driver(
        width=800,
        height=800,
        fps=120,
        diagonal_move=True
    )

    main.create_maze(MazeDensity.HIGH)
    main.run_main_loop()
