from src.cell import Cell
from src.window import Window
import time
import random


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win,
        seed = None

    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.seed = seed
        if self.seed:
            random.seed(self.seed)

    def _create_cells(self):
        self._cells = [
            [Cell(window=self.win, post_init=False) for row in range(self.num_rows)]
            for col in range(self.num_cols)
        ]
        for col_nr, cell_row in enumerate(self._cells, 1):
            for row_nr, cell in enumerate(cell_row, 1):
                if (row_nr, col_nr) == (1,1):
                    self._break_entrance_and_exit(cell,top=True)
                if (row_nr, col_nr) == (self.num_rows,self.num_cols):
                    self._break_entrance_and_exit(cell,bottom=True)
                self._draw_cell(row_nr, col_nr, cell)
                self._animate()
                # Create a random path from top-left to bottom-right
                self._reset_cells_visited()
                self._break_walls_r(0, 0)

    # This method should fill a self._cells list with lists of cells. Each top-level list is a column of Cell objects. Once the matrix is populated it should call its _draw_cell() method on each Cell.
    def _draw_cell(self, i, j, cell):
        (cell._x1, cell._y1), (cell._x2, cell._y2) = (
            (self.cell_size_x * (i - 1), self.cell_size_y * (j - 1)),
            (self.cell_size_x * i, self.cell_size_y * j),
        )
        cell.draw()

    # This method should calculate the x/y position of the Cell based on i, j, the cell_size, and the x/y position of the Maze itself. The x/y position of the maze represents how many pixels from the top and left the maze should start from the side of the window.

    # Once that's calculated, it should draw the cell and call the maze's _animate() method.
    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(
        self,
        cell: Cell,
        top: bool = False,
        bottom: bool = False):
        if top:
            cell.has_top_wall = False
        if bottom:
            cell.has_bottom_wall = False

    def _break_walls_r(self, i, j):
        cell = self._cells[i][j]
        cell.visited = True
        while True:
            possible_directions = []
            # Check top cell
            if i > 0 and not self._cells[i-1][j].visited:
                possible_directions.append((i-1, j))
            # Check right cell
            if j < len(self._cells[i])-1 and not self._cells[i][j+1].visited:
                possible_directions.append((i, j+1))
            # Check bottom cell
            if i < len(self._cells)-1 and not self._cells[i+1][j].visited:
                possible_directions.append((i+1, j))
            # Check left cell
            if j > 0 and not self._cells[i][j-1].visited:
                possible_directions.append((i, j-1))

            # If no directions available, draw the cell and return
            if len(possible_directions) == 0:
                self._draw_cell(i+1, j+1, cell)
                self._animate()
                return

            new_i, new_j = random.choice(possible_directions)

            # Knock down walls between current and chosen cell
            if new_i < i:  # Moving up
                self._cells[i][j].has_top_wall = False
                self._cells[new_i][new_j].has_bottom_wall = False
            elif new_i > i:  # Moving down
                self._cells[i][j].has_bottom_wall = False
                self._cells[new_i][new_j].has_top_wall = False
            elif new_j < j:  # Moving left
                self._cells[i][j].has_left_wall = False
                self._cells[new_i][new_j].has_right_wall = False
            elif new_j > j:  # Moving right
                self._cells[i][j].has_right_wall = False
                self._cells[new_i][new_j].has_left_wall = False

            # Recursively call the function on the new cell
            self._break_walls_r(new_i, new_j)
        self._reset_cells_visited()

    def _reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0,0)

    def _solve_r(self,i,j):
        solved = False
        self._animate()

        # Mark the current cell as visited
        current_cell = self._cells[i][j]
        current_cell.visited = True

        # If you are at the "end" cell (the goal) then return True
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True

        # Check top direction
        if i > 0 and not current_cell.has_top_wall and not self._cells[i-1][j].visited:
            current_cell.draw_move(self._cells[i-1][j])
            self._animate()
            if self._solve_r(i-1, j):
                return True
            current_cell.draw_move(self._cells[i-1][j], undo=True)
            self._animate()

        # Check right direction
        if j < self.num_rows - 1 and not current_cell.has_right_wall and not self._cells[i][j+1].visited:
            current_cell.draw_move(self._cells[i][j+1])
            self._animate()
            if self._solve_r(i, j+1):
                return True
            current_cell.draw_move(self._cells[i][j+1], undo=True)
            self._animate()

        # Check bottom direction
        if i < self.num_cols - 1 and not current_cell.has_bottom_wall and not self._cells[i+1][j].visited:
            current_cell.draw_move(self._cells[i+1][j])
            self._animate()
            if self._solve_r(i+1, j):
                return True
            current_cell.draw_move(self._cells[i+1][j], undo=True)
            self._animate()

        # Check left direction
        if j > 0 and not current_cell.has_left_wall and not self._cells[i][j-1].visited:
            current_cell.draw_move(self._cells[i][j-1])
            self._animate()
            if self._solve_r(i, j-1):
                return True
            current_cell.draw_move(self._cells[i][j-1], undo=True)
            self._animate()

        # If none of the directions worked out, return False
        return False
