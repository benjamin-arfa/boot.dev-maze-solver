from tkinter import Tk, BOTH, Canvas
from tkinter import ttk
from src.line import Line


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.geometry(f"{width}x{height}")
        self.title = "Maze Solver"
        self.__root.wm_title(self.title)
        self.canvas = Canvas(self.__root, width=width, height=height)
        self.canvas.pack()
        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.canvas, fill_color)

    def close(self):
        self.running = False
