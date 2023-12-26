from tkinter import Tk, BOTH, Canvas
import logging
from classes.window import Window, Maze
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

def generate_test_cell_lines(window: Window):
    width, height = 40, 40
    coordinate_list = zip(range(40, 460, 42), [150 for x in range(40,440,40)])
    point_pairs_list = [(Point(x, y), Point(x + width, y+ height)) for x,y in coordinate_list]
    cell_list= [Cell(p[0], p[1], window.get_canvas()) for p in point_pairs_list] 
    
    for i in range( len(cell_list)-1):
        cell = cell_list[i]
        cell.has_left_wall = False
        cell.has_right_wall = False
        window.draw_cell(cell)
        cell.draw_move(cell_list[i + 1], undo=False)
    cell_list[-1].has_left_wall = False
    window.draw_cell(cell_list[-1])

def generate_test_maze(window: Window):
    maze = Maze(
        x1=50,
        y1=50,
        num_rows=3,
        num_cols=3,
        cell_size_x=20,
        cell_size_y=20, 
        window=window
        )
    

def main():
    logging.basicConfig(filename="app.log", filemode="w", level=logging.DEBUG)
    logging.info('Started -- Creating window')
    window = Window()
    # generate_test_lines(window)
    # generate_test_cells(window)    
    # generate_test_cell_lines(window)
    generate_test_maze(window)
    window.wait_for_close()

if __name__ == "__main__":
    main()
