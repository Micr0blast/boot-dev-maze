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