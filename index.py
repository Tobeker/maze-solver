from tkinter import Tk, Canvas
from maze import Cell

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = Tk()
        self.root.title("My Window")
        self.root.geometry(f"{width}x{height}")
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(self.root, width=width, height=height)
        self.canvas.pack()
        self.running = False

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()
    
    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False


def main():
    win = Window(800, 600)
    
    cell1 = Cell(50, 50, 100, 100, win)
    cell2 = Cell(150, 150, 200, 200, win)
    cell3 = Cell(250, 250, 300, 300, win)
    cell4 = Cell(350, 350, 400, 400, win)
    cell1.has_top_wall = False
    cell2.has_right_wall = False
    cell3.has_bottom_wall = False
    cell4.has_left_wall = False
    cell1.draw()
    cell2.draw()
    cell3.draw()
    cell4.draw()
    cell1.draw_move(cell2)
    cell2.draw_move(cell3, True)

    # win.draw_line(line1, "black")
    win.wait_for_close()

main()