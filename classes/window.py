from tkinter import Tk, Canvas
import time
from classes.geometry import Line, Cell, Point
import logging

class Window:
    def __init__(self, width=500, height=400, title='boots.dev Maze Solver'):
        self.__width = width
        self.__height = height
        self.__running = False
        self.__title = title
        self.__root, self.__canvas = self.__setup()

    def __setup(self):
        root = Tk()
        # setup window for the application
        root.title( self.__title )

        root.protocol("WM_DELETE_WINDOW", self.__close)

        # create the canvas which will contain geometry objects
        # https://tkinter-docs.readthedocs.io/en/latest/widgets/canvas.html#
        canvas = Canvas(root, width=self.__width, height=self.__height)

        # calling pack will acutally place the child element on the root canvas
        # pack has some options for positioning
        # https://docs.python.org/3/library/tkinter.html#the-packer         
        canvas.pack()

        return root, canvas


    def __close(self):
        self.__running = False
    
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()    

    def draw_line(self, line: Line, fill_color):
        line.draw_line(self.__canvas, fill_color=fill_color)

    def draw_cell(self, cell: Cell):
        cell.draw()

    def get_canvas(self):
        return self.__canvas

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw() 


class Maze:
    def __init__(
            self,
            x1: int,
            y1: int,
            num_rows: int,
            num_cols: int,
            cell_size_x:int ,
            cell_size_y:int,
            window: Window = None
        ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = window

        self._create_cells()

    def _create_cells(self):
        self._cells = []
        canvas = self._win.get_canvas() if self._win else None
        for i in range(self._num_rows):
            row = []
            for j in range(self._num_cols):
                p1_x =  self._x1 + i * self._cell_size_x
                p1_y =  self._y1 + j * self._cell_size_y
                p2_x =  self._x1 + i * self._cell_size_x + self._cell_size_x
                p2_y =  self._y1 + j * self._cell_size_y + self._cell_size_y

                p1 = Point(p1_x, p1_y)
                p2 = Point(p2_x, p2_y)

                row.append(Cell(p1, p2, canvas))
            self._cells.append(row)
        for i in range(self._num_rows):
            for j in range(self._num_cols):
                self._draw_cell(i,j)

    def _draw_cell(self, i, j):
        cell = self._cells[i][j]
        
        if self._win is not None:
            self._win.draw_cell(cell)
            self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.5)