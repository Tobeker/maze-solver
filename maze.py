import time

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
    def __init__(self, x1, y1, x2, y2, win):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

        self._x1 = x1  # top-left x
        self._y1 = y1  # top-left y
        self._x2 = x2  # bottom-right x
        self._y2 = y2  # bottom-right y

        self._win = win  # canvas or drawing window

    def draw(self, fill_color="black"):
        # Draw walls conditionally
        if self.has_top_wall:
            point1_top = Point(self._x1, self._y1)
            point2_top = Point(self._x2, self._y1)
            line_top = Line(point1_top, point2_top)
            self._win.draw_line(line_top, fill_color)
        if self.has_right_wall:
            point1_right = Point(self._x2, self._y1)
            point2_right = Point(self._x2, self._y2)
            line_right = Line(point1_right, point2_right)
            self._win.draw_line(line_right, fill_color)
        if self.has_bottom_wall:
            point1_bottom = Point(self._x2, self._y2)
            point2_bottom = Point(self._x1, self._y2)
            line_bottom = Line(point1_bottom, point2_bottom)
            self._win.draw_line(line_bottom, fill_color)
        if self.has_left_wall:
            point1_left = Point(self._x1, self._y2)
            point2_left = Point(self._x1, self._y1)
            line_left = Line(point1_left, point2_left)
            self._win.draw_line(line_left, fill_color)

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
    def __init__(self,x1,y1,num_rows,num_cols,cell_size_x,cell_size_y,win,):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self. num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

        self._cells = []
        self._create_cells()

    def _create_cells(self):
        for col in range(self.num_cols):
            column = []
            for row in range(self.num_rows):
                self._draw_cell(col, row)  # Draw each cell as it's created
                column.append(self._cells[col][row])  # Already created inside _draw_cell
            self._cells.append(column)

    def _draw_cell(self, i, j):
        # Calculate pixel positions
        x1 = self.x1 + i * self.cell_size_x
        y1 = self.y1 + j * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y

        # Create and store the cell
        cell = Cell(x1, y1, x2, y2, self.win)
        
        # Lazy init of columns (since _cells is filled one col at a time)
        if len(self._cells) <= i:
            self._cells.append([])

        self._cells[i].append(cell)

        # Draw and animate
        cell.draw()
        self._animate()

    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)  # Delay for visual effect
