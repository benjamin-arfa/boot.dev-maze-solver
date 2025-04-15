from tkinter import Canvas
from src.window import Window


class Cell:
    def __init__(
        self,
        point_1: tuple = (0, 0),
        point_2: tuple = (0, 0),
        window: Window = None,
        post_init: bool = True,
    ):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False

        self._win = window

        if post_init:
            self.__post_init__(point_1, point_2)

    def __post_init__(self, point_1: tuple, point_2: tuple):
        self._x1 = point_1[0]
        self._x2 = point_2[0]
        if self._x1 == self._x2:
            raise Exception("It is a line, not a cell!")

        self._y1 = point_1[1]
        self._y2 = point_2[1]
        if self._y1 == self._y2:
            raise Exception("It is a line, not a cell!")

    def get_topleft__bottomright_points(self):
        x_tl = self._x1 if self._x1 < self._x2 else self._x2
        x_br = self._x2 if self._x2 > self._x1 else self._x1
        y_tl = self._y1 if self._y1 < self._y2 else self._y2
        y_br = self._y2 if self._y2 > self._y1 else self._y1
        return (x_tl, y_tl), (x_br, y_br)

    def draw(self):
        (x_tl, y_tl), (x_br, y_br) = self.get_topleft__bottomright_points()
        if self.has_left_wall:
            self._win.canvas.create_line(x_tl, y_tl, x_tl, y_br, fill="black", width=1)

        if self.has_right_wall:
            self._win.canvas.create_line(x_br, y_tl, x_br, y_br, fill="black", width=1)

        if self.has_top_wall:
            self._win.canvas.create_line(x_tl, y_tl, x_br, y_tl, fill="black", width=1)

        if self.has_bottom_wall:
            self._win.canvas.create_line(x_tl, y_br, x_br, y_br, fill="black", width=1)

    def get_center(self):
        return ((self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2)

    def draw_move(self, to_cell, undo=False):
        (x_tl, y_tl), (x_br, y_br) = self.get_center(), to_cell.get_center()
        self._win.canvas.create_line(
            x_tl, y_tl, x_br, y_br, fill="red" if undo else "gray", width=1
        )
