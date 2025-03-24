from math import hypot
from figures.vector_tools import Point, constrain


class Square:
    def __init__(self, p, color, canvas):
        self.radius = 35
        self.canvas = canvas
        self.p = self.constrain_rectangle_move(p)
        self.color = color
        self.selected = False

    def check_point(self, p) -> bool:
        return hypot(p.x - self.p.x, p.y - self.p.y) <= self.radius

    def dist_point(self, p):
        return hypot(p.x - self.p.x, p.y - self.p.y)

    def select(self):
        self.selected = not (self.selected)

    def unselect(self):
        self.selected = False

    def paint(self):
        p1 = self.p.dec(Point(self.radius))
        p2 = self.p.inc(Point(self.radius))
        border_color = "#1f6aa5" if self.selected else self.color
        self.canvas.create_rectangle(p1.x, p1.y, p2.x, p2.y,
                                     fill=self.color,
                                     width=5,
                                     outline=border_color)  # negative
    def resize(self, lp, np):
        if self.selected:
            l_dist = hypot(lp.x-self.p.x, lp.y-self.p.y)
            n_dist = hypot(np.x-self.p.x, np.y-self.p.y)
            self.radius = self.constrain_rectangle_resize(self.radius+int(n_dist - l_dist))

    def move(self, offset:Point):
        if self.selected:
            self.p = self.constrain_rectangle_move(self.p.inc(offset))
            
    def fill(self, color):
        if self.selected:
            self.color = color

    def constrain_rectangle_move(self, value:Point):
        return Point(
                constrain(self.radius+5, self.canvas.winfo_width()-self.radius-5, value.x),
                constrain(self.radius+5, self.canvas.winfo_height()-self.radius-5, value.y)
            )

    def constrain_rectangle_resize(self, radius):
        ccr_x = constrain(0, min(self.p.x, self.canvas.winfo_width()-self.p.x-5), radius)
        ccr_y = constrain(0, min(self.p.y, self.canvas.winfo_height()-self.p.y-5), radius)
        return min(ccr_x, ccr_y)

    def self_destruct(self):
        if self.selected:
            del self
            return True

