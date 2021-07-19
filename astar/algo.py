import time
from typing import Callable, List
from .gui import Cell
from queue import PriorityQueue


class AlgorithmAStar:
    def __init__(self):
        self.algo_running = False

    @staticmethod
    def calc_heuristic(p1: tuple, p2: tuple) -> int:
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    def stop_algo(self):
        self.algo_running = False

    def fps_to_sec(self, fps):
        return 1 / fps

    def algo(self, draw_func: Callable, grid: List[List[Cell]], start_cell: Cell, end_cell: Cell, fps):
        self.algo_running = True

        count: int = 0

        open_set = PriorityQueue()
        open_set.put((0, count, start_cell))
        parent_node = {}

        g_score = {cell: float('inf') for row in grid for cell in row}
        f_score = {cell: float('inf') for row in grid for cell in row}

        g_score[start_cell] = 0  # Setting g score as 0 for staring node
        f_score[start_cell]: int = self.calc_heuristic(start_cell.get_pos(), end_cell.get_pos())

        open_set_hash = {start_cell}  # A set holding cells similar to open set

        while not open_set.empty():
            if not self.algo_running:
                break

            time.sleep(self.fps_to_sec(fps))

            current_cell: Cell = open_set.get()[2]
            open_set_hash.remove(current_cell)

            if current_cell == end_cell:
                # Found the goal
                return parent_node, end_cell, draw_func

            for neighbour in current_cell.neighbors:
                temp_g_score = g_score[current_cell] + 1

                if temp_g_score < g_score[neighbour]:
                    parent_node[neighbour] = current_cell
                    g_score[neighbour] = temp_g_score
                    f_score[neighbour] = temp_g_score + self.calc_heuristic(neighbour.get_pos(), end_cell.get_pos())

                    if neighbour not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbour], count, neighbour))
                        open_set_hash.add(neighbour)
                        neighbour.make_open()

            draw_func()

            if current_cell != start_cell:
                current_cell.make_closed()
            current_cell.make_current()

        return False
