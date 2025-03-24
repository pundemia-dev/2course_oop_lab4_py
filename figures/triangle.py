from math import hypot
from vector_tools import Point, constrain

info = ("△", 25, "Triangle")


class Triangle:
    def __init__(self, p, color, canvas):
        self.a = Point(p.x, p.y-30)
        self.b = Point(p.x - 30, p.y+30)
        self.c = Point(p.x + 30, p.y+30)
        self.canvas = canvas
        self.color = color
        self.selected = False
        self.a, self.b, self.c = self.constrain_triangle_move(self.a, self.b, self.c)

    def check_point(self, p) -> bool:
        def sign(p1, p2, p3):
            return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

        b1 = sign(p, self.a, self.b) < 0
        b2 = sign(p, self.b, self.c) < 0
        b3 = sign(p, self.c, self.a) < 0
        return (b1 == b2) and (b2 == b3)

    def dist_point(self, p):
        def distance_to_segment(p, a, b):
            dx = b.x - a.x
            dy = b.y - a.y
            if dx == 0 and dy == 0:
                return hypot(p.x - a.x, p.y - a.y)
            t = max(0, min(1, ((p.x - a.x)*dx + (p.y - a.y)*dy)/(dx*dx + dy*dy)))
            px, py = a.x + t*dx, a.y + t*dy
            return hypot(p.x - px, p.y - py)
        
        d1 = distance_to_segment(p, self.a, self.b)
        d2 = distance_to_segment(p, self.b, self.c)
        d3 = distance_to_segment(p, self.c, self.a)
        return min(d1, d2, d3)

    def select(self):
        self.selected = not self.selected

    def unselect(self):
        self.selected = False

    def paint(self):
        border_color = "#1f6aa5" if self.selected else self.color
        self.canvas.create_polygon(
            self.a.x, self.a.y,
            self.b.x, self.b.y,
            self.c.x, self.c.y,
            fill=self.color,
            width=5,
            outline=border_color
        )

    def resize(self, lp, np):
        if self.selected:
            dist_a = self.dist_points(np, self.a)
            dist_b = self.dist_points(np, self.b)
            dist_c = self.dist_points(np, self.c)
            closest = min(dist_a, dist_b, dist_c)
            
            if closest == dist_a:
                self.a = self.constrain_triangle_resize(self.a.inc(Point(np.x - lp.x, np.y - lp.y)))
            elif closest == dist_b:
                self.b = self.constrain_triangle_resize(self.b.inc(Point(np.x - lp.x, np.y - lp.y)))
            elif closest == dist_c:
                self.c = self.constrain_triangle_resize(self.c.inc(Point(np.x - lp.x, np.y - lp.y)))

    def move(self, offset: Point):
        if self.selected:
            new_a = self.a.inc(offset)
            new_b = self.b.inc(offset)
            new_c = self.c.inc(offset)
            self.a, self.b, self.c = self.constrain_triangle_move(new_a, new_b, new_c)

    def fill(self, color):
        if self.selected:
            self.color = color

    def constrain_triangle_move(self, a, b, c):
        min_x, max_x = 5, self.canvas.winfo_width() - 5
        min_y, max_y = 5, self.canvas.winfo_height() - 5

        dx = max(0, min_x - min(a.x, b.x, c.x)) + min(0, max_x - max(a.x, b.x, c.x))
        dy = max(0, min_y - min(a.y, b.y, c.y)) + min(0, max_y - max(a.y, b.y, c.y))

        return (
            Point(a.x + dx, a.y + dy),
            Point(b.x + dx, b.y + dy),
            Point(c.x + dx, c.y + dy)
        )

    def constrain_triangle_resize(self, p):
        return Point(
            constrain(5, self.canvas.winfo_width() - 5, p.x),
            constrain(5, self.canvas.winfo_height() - 5, p.y)
        )

    def self_destruct(self):
        if self.selected:
            del self
            return True

    def dist_points(self, a: Point, b: Point):
        return hypot(a.x - b.x, a.y - b.y)
