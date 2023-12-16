from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width=500, height=400, title='boots.dev Maze Solver'):
        self.__width = width
        self.__height = height
        self.__running = False
        self.__title = title
        self.__setup()

    def __setup(self):
        self.__root = Tk()
        # setup window for the application
        self.__root.title( self.__title )

        self.__root.protocol("WM_DELETE_WINDOW", self.__close)

        # create the canvas which will contain geometry objects
        # https://tkinter-docs.readthedocs.io/en/latest/widgets/canvas.html#
        self.__canvas = Canvas(self.__root, width=self.__width, height=self.__height)

        # calling pack will acutally place the child element on the root canvas
        # pack has some options for positioning
        # https://docs.python.org/3/library/tkinter.html#the-packer         
        self.__canvas.pack()

    def __close(self):
        self.__running = False
    
    def __redraw(self):
        self.__root.update_idletasks()
        self.__root.update()    

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.__redraw() 

# start app


def main():
    window = Window()
    window.wait_for_close()

if __name__ == "__main__":
    main()
