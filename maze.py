import time
import random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point1.x, self.point1.y,
            self.point2.x, self.point2.y,
            fill=fill_color, width=2
        )

class Cell:
    def __init__(self, x1, y1, x2, y2, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False

        self._x1 = x1  # top-left x
        self._y1 = y1  # top-left y
        self._x2 = x2  # bottom-right x
        self._y2 = y2  # bottom-right y

        self._win = win  # canvas or drawing window

    def draw(self, fill_color="black"):
        # Draw walls conditionally
        top_left = Point(self._x1, self._y1)
        top_right = Point(self._x2, self._y1)
        bottom_left = Point(self._x1, self._y2)
        bottom_right = Point(self._x2, self._y2)
        line_top = Line(top_left, top_right)
        line_right = Line(top_right, bottom_right)
        line_bottom = Line(bottom_right, bottom_left)
        line_left = Line(bottom_left, top_left)
        if self.has_top_wall:
            self._win.draw_line(line_top, fill_color)
        else:
            self._win.draw_line(line_top, "white")
        if self.has_right_wall:
            self._win.draw_line(line_right, fill_color)
        else:
            self._win.draw_line(line_right, "white")
        if self.has_bottom_wall:
            self._win.draw_line(line_bottom, fill_color)
        else:
            self._win.draw_line(line_bottom, "white")
        if self.has_left_wall:
            self._win.draw_line(line_left, fill_color)
        else:
            self._win.draw_line(line_left, "white")

    def draw_move(self, to_cell, undo=False):
        if not undo:
            fill_color = "red"
        else:
            fill_color = "gray"
        point1 = Point((self._x1 + self._x2)/2, (self._y1 + self._y2)/2)
        point2 = Point((to_cell._x1 + to_cell._x2)/2, (to_cell._y1 + to_cell._y2)/2)
        line = Line(point1, point2)
        self._win.draw_line(line, fill_color)

class Maze:
    def __init__(self,x1,y1,num_rows,num_cols,cell_size_x,cell_size_y,win=None,seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed is not None:
            random.seed(seed)

        self._cells = []
        self._create_cells()
        self._breake_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for col in range(self.num_cols):
            column = []
            for row in range(self.num_rows):
                cell = self._draw_cell(col, row)  # Draw each cell as it's created
                column.append(cell)  
            self._cells.append(column)

    def _draw_cell(self, i, j):
        # Calculate pixel positions
        x1 = self.x1 + i * self.cell_size_x
        y1 = self.y1 + j * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y

        # Create and store the cell
        cell = Cell(x1, y1, x2, y2, self.win)
        # Draw and animate
        cell.draw()
        self._animate()
        return cell

    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)  # Delay for visual effect

    def _breake_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False
        self._cells[0][0].draw()
        self._cells[self.num_cols - 1][self.num_rows - 1].draw()

    def _break_walls_r(self, i, j):
        current_cell = self._cells[i][j]
        current_cell.visited = True
        while True:
            to_visit = []
            #left
            if i>0 and self._cells[i-1][j].visited == False:
                to_visit.append(("left", i-1, j))
            #right
            if i<self.num_cols-1 and self._cells[i+1][j].visited == False:
                to_visit.append(("right", i+1, j))
            #top
            if j>0 and self._cells[i][j-1].visited == False:
                to_visit.append(("up", i, j-1))
            #bottom
            if j<self.num_rows-1 and self._cells[i][j+1].visited == False:
                to_visit.append(("down", i, j+1))
            #check possibilities
            if len(to_visit) == 0:
                self._cells[i][j].draw()
                return
            
            direction, next_i, next_j = random.choice(to_visit)
            next_cell = self._cells[next_i][next_j]

            # Knock down the wall between current and next cell
            if direction == "left":
                current_cell.has_left_wall = False
                next_cell.has_right_wall = False
            elif direction == "right":
                current_cell.has_right_wall = False
                next_cell.has_left_wall = False
            elif direction == "up":
                current_cell.has_top_wall = False
                next_cell.has_bottom_wall = False
            elif direction == "down":
                current_cell.has_bottom_wall = False
                next_cell.has_top_wall = False

            # Recursive call
            self._break_walls_r(next_i, next_j)

    def _reset_cells_visited(self):
        for col in range(self.num_cols):
            for row in range(self.num_rows): 
                self._cells[col][row].visited = False
            