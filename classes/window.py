from tkinter import Tk, Canvas
import time
import logging
import random
from classes.geometry import Line, Cell, Point


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
        logging.info("Exited application")

class Maze:
    def __init__(
            self,
            x1: int,
            y1: int,
            num_rows: int,
            num_cols: int,
            cell_size_x:int ,
            cell_size_y:int,
            window: Window = None,
            seed: int = None
        ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = window
        self._seed = seed if seed is not None else 0

        random.seed(self._seed)

        self._create_cells()
        self._break_entrance_and_exit_walls()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()


    def _create_cells(self):
        self._cells = []
        canvas = self._win.get_canvas() if self._win else None
        
        if self._num_cols == 0 or self._num_rows == 0:
            raise ValueError("Cannot create Maze without rows or columns") 
        if self._cell_size_x == 0 or self._cell_size_y == 0:
            raise ValueError("Cannot create maze with cell width or length of 0")
        
        if self._x1 < 0 or self._y1 < 0:
            raise ValueError("Cannot create maze out of bounds")

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
        if self._win is None:
            return 
        
        self._win.redraw()
        time.sleep(0.1)

    def _break_entrance_and_exit_walls(self):
        # top left
        entry = self._cells[0][0]
        # bottom right
        exit = self._cells[-1][-1]

        entry.set_cell_walls(0b0000)
        
        exit.set_cell_walls(0b0000)

    def _break_walls_r(self, i, j):
        logging.info(f'BREAKING: Visiting {i} {j}')
        current_cell = self._cells[i][j]
        current_cell.visited = True
        while True:
            to_visit = self._get_neighbours(i, j)
            # if no directions available 
            if len(to_visit) == 0:
                self._draw_cell(i, j)
                break
            # choose random cell and breka walls
            else:

                new_i, new_j = random.choice(to_visit)
                logging.info(f'Chose {new_i} {new_j}')
                next_cell = self._cells[new_i][new_j]

                if new_i == i-1:
                    current_cell.has_left_wall  = False
                    next_cell.has_right_wall = False

                if new_i == i +1:
                    current_cell.has_right_wall = False
                    next_cell.has_left_wall = False
                if new_j == j +1:

                    current_cell.has_top_wall = False
                    next_cell.has_bottom_wall = False
                if new_j == j-1:
                    current_cell.has_bottom_wall = False
                    next_cell.has_top_wall = False



                self._break_walls_r(new_i, new_j)
        
        return None

    
    def _reset_cells_visited(self):

        for row in self._cells:
            for cell in row:
                cell.visited = False
        return None

    def solve(self) -> bool:
        return self._solve_r(i=0, j=0)
    
    def solve_BFS(self):
        path = self._solve_BFS(0,0)
        self._draw_backtracked_path(path)
    
    def _solve_r(self, i, j):
        self._animate()
        logging.info(f"SOLVING: Visiting {i} {j}")
        current = self._cells[i][j]
        current.visited = True
        if i == self._num_rows - 1 and j ==self._num_cols - 1:
            return True

        to_visit = self._get_neighbours_without_borders(i,j)
        for next_i, next_j in to_visit:
            next_c = self._cells[next_i][next_j]
            current.draw_move(next_c)
        
            is_on_path = self._solve_r(next_i, next_j)
            if is_on_path:
                return True
            current.draw_move(next_c, undo=True)

        return False

    def _solve_BFS(self, i,j):
        
        queue = [(i,j)]
        paths = {(i,j): None}
        while queue:
            self._animate()
            current = queue.pop()
            next_i, next_j = current
            next_c = self._cells[next_i][next_j]
            next_c.visited = True
            if (next_i, next_j) == (self._num_rows -1, self._num_cols -1):
                path = []
                while current is not None:
                    path.append(current)
                    current = paths[current]
                # path.reverse()
                return path
            

            neighbours = self._get_neighbours_without_borders(next_i, next_j)
                           
            for neigh_i, neigh_j in neighbours:
                neighbour = self._cells[neigh_i][neigh_j]

                next_c.draw_move(neighbour)
                queue.insert(0, (neigh_i, neigh_j))
                paths[(neigh_i, neigh_j)] = current

        return None

    def _draw_backtracked_path(self, path):
        logging.info(f'BFS: Drawing path {path}')
        if path is None:
            return None
        for idx, cell in enumerate(path[:-1]):
            self._animate()
            i, j = cell
            current = self._cells[i][j]
            n_i, n_j = path[idx + 1]
            next_c = self._cells[n_i][n_j]
            current.draw_move(next_c, True)

    def _get_neighbours(self, i, j) -> list:
        to_visit = []
        # check cells
        # to left
        if i > 0:
            left = self._cells[i-1][j]
            if not left.visited:
                to_visit.append((i-1, j))
        # to right
        if i < self._num_rows - 1:
            right = self._cells[i+1][j]
            if not right.visited:
                to_visit.append((i+1, j))
        # to top
        if j < self._num_cols - 1:
            top = self._cells[i][j+1]
            if not top.visited:
                to_visit.append((i, j+1))
        # to bottom
        if j > 0:
            bottom = self._cells[i][j-1]
            if not bottom.visited:
                to_visit.append((i, j-1))

        return to_visit
    
    def _get_neighbours_without_borders(self, i, j) -> list:
        to_visit = []
        current = self._cells[i][j]
        # check cells
        # to left
        if i > 0:
            left = self._cells[i-1][j]
            if not left.visited and not current.has_left_wall:
                to_visit.append((i-1, j))
        # to right
        if i < self._num_rows - 1:
            right = self._cells[i+1][j]
            if not right.visited and not current.has_right_wall:
                to_visit.append((i+1, j))
        # to top
        if j < self._num_cols - 1:
            top = self._cells[i][j+1]
            if not top.visited and not current.has_top_wall:
                to_visit.append((i, j+1))
        # to bottom
        if j > 0:
            bottom = self._cells[i][j-1]
            if not bottom.visited and not current.has_bottom_wall:
                to_visit.append((i, j-1))
        logging.info(f'Got Neighbours without borders:\n{to_visit}')
        return to_visit