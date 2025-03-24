from math import hypot
from figures.vector_tools import Point, constrain


class Line:
    def __init__(self, p, color, canvas):
        self.canvas = canvas
        self.a, self.b = self.constrain_line_move(Point(p.x - 30, p.y), Point(p.x + 30, p.y))
        self.color = color
        self.selected = False

    def check_point(self, p) -> bool:
        return self.dist_point(p) < 15

    def dist_point(self, p):
        dist = Point(self.b.x - self.a.x, self.b.y - self.a.y) 
        if dist == Point(0, 0):
            return int(hypot(p.x - self.a.x, p.y - self.a.y))
        t = max(0, min(1, ((p.x - self.a.x) * dist.x + (p.y - self.a.y) * dist.y) / (dist.x**2 + dist.y**2)))
        px, py = self.a.x + t * dist.x, self.a.y + t * dist.y
        return int(hypot(p.x - px, p.y - py))

    def dist_points(self, a:Point, b:Point):
        return hypot(a.x-b.x, a.y-b.y)

    def select(self):
        self.selected = not (self.selected)

    def unselect(self):
        self.selected = False

    def paint(self):
        color = "#1f6aa5" if self.selected else self.color
        self.canvas.create_line(self.a.x, self.a.y, self.b.x, self.b.y,
                                fill=color)  # negative
    def resize(self, lp, np):
        if self.selected:
            dist_a = self.dist_points(np, self.a)
            dist_b = self.dist_points(np, self.b)
            if min(dist_a, dist_b) == dist_a:
                self.a = self.constrain_line_resize(self.a.inc(Point(np.x-lp.x, np.y-lp.y)))
            elif min(dist_a, dist_b) == dist_b:
                self.b = self.constrain_line_resize(self.b.inc(Point(np.x-lp.x, np.y-lp.y)))           

    def move(self, offset:Point):
        if self.selected:
            self.a, self.b = self.constrain_line_move(self.a.inc(offset), self.b.inc(offset))
            
    def fill(self, color):
        if self.selected:
            self.color = color

    def constrain_line_move(self, value_a:Point, value_b:Point):
        min_x, max_x = 5, self.canvas.winfo_width() - 5
        min_y, max_y = 5, self.canvas.winfo_height() - 5

        dx = max(0, min_x - min(value_a.x, value_b.x)) + min(0, max_x - max(value_a.x, value_b.x))
        dy = max(0, min_y - min(value_a.y, value_b.y)) + min(0, max_y - max(value_a.y, value_b.y))

        return (
            Point(value_a.x + dx, value_a.y + dy),
            Point(value_b.x + dx, value_b.y + dy)
        )

    def constrain_line_resize(self, p):
        pos = Point(
                constrain(5, self.canvas.winfo_width()-5, p.x),
                constrain(5, self.canvas.winfo_height()-5, p.y)
            )
        return pos

    def self_destruct(self):
        if self.selected:
            del self
            return True

