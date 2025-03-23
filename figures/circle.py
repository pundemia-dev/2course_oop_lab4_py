from math import sqrt


class Circle:
    def __init__(self, x: int, y: int, color, canvas):
        self.x = x
        self.y = y
        self.radius = 35
        self.color = color
        self.selected = False
        self.canvas = canvas

    def check_point(self, x: int, y: int) -> bool:
        return ((x - self.x) ** 2 + (y - self.y) ** 2) <= self.radius ** 2

    def dist_point(self, x: int, y: int):
        return sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def select(self):
        self.selected = not (self.selected)

    def unselect(self):
        self.selected = False

    def paint(self):
        x1, y1 = (self.x - self.radius), (self.y - self.radius)
        x2, y2 = (self.x + self.radius), (self.y + self.radius)
        border_color = "#1f6aa5" if self.selected else self.color
        self.canvas.create_oval(x1, y1, x2, y2,
                                fill=self.color,
                                width=5,
                                outline=border_color)  # negative
    def resize(self, event):
        if self.selected:
            pass

    def move(self, x_offset, y_offset):
        if self.selected:
            self.x += x_offset
            self.y += y_offset

    def fill(self, color):
        if self.selected:
            self.color = color

    def self_destruct(self):
        if self.selected:
            del self
            return True

