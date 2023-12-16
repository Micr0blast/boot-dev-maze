from tkinter import Tk, BOTH, Canvas
from classes.window import Window
from classes.geometry import Point, Line, Cell

def generate_test_lines(window: Window):
    points_pairs = [(Point(x + 10, y+ 10), Point(x * 10, y * 3)) for x,y in enumerate(range(1, 100, 10))]
    lines = [Line(p[0],p[1]) for p in points_pairs]
    for line in lines:
        window.draw_line(line, "white")

def generate_test_cells(window: Window):
    width, height = 40, 40
    coords = zip(range(10, 400, width), range(10,400, height))
    point_pairs = [(Point(x, y), Point(x + width, y+ height)) for x,y in coords]
    cells = [Cell(p[0], p[1], window.get_canvas()) for p in point_pairs] 
    for cell in cells:
        window.draw_cell(cell)

def main():
    window = Window()
    generate_test_lines(window)
    generate_test_cells(window)    

    window.wait_for_close()

if __name__ == "__main__":
    main()
