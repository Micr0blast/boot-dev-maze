from tkinter import Tk, Canvas
from classes.geometry import Line, Cell

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
    
    def __redraw(self):
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
            self.__redraw() 