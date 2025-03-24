from math import hypot
from vector_tools import Point, constrain

info = ("▭", 25, "Rectangle")


class Rectangle:
    def __init__(self, p, color, canvas):
        self.r = Point(35, 15)
        self.canvas = canvas
        self.p = self.constrain_rectangle_move(p)
        self.color = color
        self.selected = False

    def check_point(self, p) -> bool:
        return ((p.x-self.p.x) ** 2)/(self.r.x ** 2) + ((p.y-self.p.y) ** 2)/(self.r.y ** 2) <= 1

    def dist_point(self, p):
        return hypot(p.x-self.p.x, p.y-self.p.y) 

    def select(self):
        self.selected = not (self.selected)

    def unselect(self):
        self.selected = False

    def paint(self):
        p1 = self.p.dec(self.r)
        p2 = self.p.inc(self.r)
        border_color = "#1f6aa5" if self.selected else self.color
        self.canvas.create_rectangle(p1.x, p1.y, p2.x, p2.y,
                                     fill=self.color,
                                     width=5,
                                     outline=border_color)  # negative
    def resize(self, lp, np):
        if self.selected:
            offset_x = (max(np.x, self.p.x) - min(np.x, self.p.x)) - (max(lp.x, self.p.x)-min(lp.x,self.p.x))
            offset_y = (max(np.y, self.p.y) - min(np.y, self.p.y)) - (max(lp.y, self.p.y)-min(lp.y,self.p.y))
            self.r = self.constrain_rectangle_resize(self.r.inc(Point(offset_x, offset_y)))

    def move(self, offset:Point):
        if self.selected:
            self.p = self.constrain_rectangle_move(self.p.inc(offset))
            
    def fill(self, color):
        if self.selected:
            self.color = color

    def constrain_rectangle_move(self, value:Point):
        return Point(
                constrain(self.r.x+5, self.canvas.winfo_width()-self.r.x-5, value.x),
                constrain(self.r.y+5, self.canvas.winfo_height()-self.r.y-5, value.y)
            )

    def constrain_rectangle_resize(self, r):
        ccr_x = constrain(0, min(self.p.x, self.canvas.winfo_width()-self.p.x-5), r.x)
        ccr_y = constrain(0, min(self.p.y, self.canvas.winfo_height()-self.p.y-5), r.y)
        return Point(ccr_x, ccr_y)

    def self_destruct(self):
        if self.selected:
            del self
            return True

