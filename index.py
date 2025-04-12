from tkinter import Tk, Canvas
from maze import Maze

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = Tk()
        self.root.title("My Window")
        self.root.geometry(f"{width}x{height}")
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(self.root, width=width, height=height, background="white")
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
    
    m1 = Maze(0, 0, 29, 39, 20, 20, win)
    m1.solve()
    win.wait_for_close()

main()