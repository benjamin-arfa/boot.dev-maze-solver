from src.window import Window
from src.line import Line
from src.cell import Cell
from src.maze import Maze


def main():
    win = Window(800, 600)
    # Create a maze using the Maze class
    maze = Maze(50, 50, 10, 10, 50, 50, win)

    # Create cells for the maze
    maze._create_cells()

    # The maze._create_cells() method will:
    # 1. Create a matrix of cells
    # 2. Draw each cell at the appropriate position
    # 3. Animate the drawing process

    # Break walls to create the maze paths
    maze._break_walls_r(0, 0)

    maze.solve()

    win.wait_for_close()


if __name__ == "__main__":
    main()
