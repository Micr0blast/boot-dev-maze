from tkinter import Canvas
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class Line:
    def __init__(self, point_a: Point , point_b: Point):
        self.p_1 = point_a
        self.p_2 = point_b

    def draw_line(self, canvas: Canvas, fill_color):
        canvas.create_line(
            self.p_1.x, self.p_1.y, 
            self.p_2.x, self.p_2.y,
            fill=fill_color, width =2)
        
class Cell:
    def __init__(self, p1: Point, p2: Point, canvas: Canvas):
        self.has_left_wall = True
        self.has_top_wall = True
        self.has_right_wall = True
        self.has_bottom_wall = True

        # alternative idea, represent wall as 4bit binary 0000, left,top,right,bottom

        self._x1 = p1.x
        self._y1 = p1.y
        self._x2 = p2.x
        self._y2 = p2.y
        self._canvas = canvas
        
    def __get_cell_points(self) -> list[Point]:
        """
            Calculates the necessary points for the cell walls
        """
        p1 = Point(self._x1, self._y1)
        p2 = Point(self._x2, self._y1)
        p3 = Point(self._x1, self._y2)
        p4 = Point(self._x2, self._y2)

        return p1, p2, p3, p4
    
    def __get_cell_walls(self) -> list[Line]:
        """
            Calculates the Lines of the cell walls
        """
        p1, p2, p3, p4 = self.__get_cell_points()

        left_wall = Line(p1, p3)
        top_wall = Line(p1, p2)
        right_wall = Line(p2, p4)
        bottom_wall = Line(p3, p4)
        return left_wall, top_wall, right_wall, bottom_wall
    
    def draw(self) -> None:
        """
            draws the cell on the canvas using the Lines
        """
        left_wall, top_wall, right_wall, bottom_wall = self.__get_cell_walls()
        print(f'Drawing Walls {self.has_left_wall} {self.has_top_wall}')
        
        if self.has_left_wall:
            left_wall.draw_line(self._canvas, "white")
        if self.has_top_wall:
            top_wall.draw_line(self._canvas, "white")
        if self.has_right_wall:
            right_wall.draw_line(self._canvas, "white")
        if self.has_bottom_wall:
            bottom_wall.draw_line(self._canvas, "white")

    def get_center_point(self) -> Point:
        """
            Calculates the center Point for drawing
        """
        center_x = (self._x2 + self._x1) // 2
        center_y = (self._y2 + self._y1) // 2
        return Point(center_x, center_y)
        

    def draw_move(self, to_cell, undo=False) -> None:
        move = Line(
            self.get_center_point(), 
            to_cell.get_center_point()
            )
        fill_color = 'red' if undo else 'gray'
        move.draw_line(self._canvas, fill_color=fill_color)

    def __str__(self):
        return f"{self._x1} {self._y1}"
        

        

