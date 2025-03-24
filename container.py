from figures.circle import Circle
from figures.vector_tools import Point


class Container:
    def __init__(self, canvas):
        self.objects = list()
        self.canvas = canvas
        self.lp = Point(None, None)

    def new_circle(self, color, event):
        if (self.lp) == Point(None, None):
            self.objects.append(Circle(event, color, self.canvas))
        else:
            self.lp = Point(None, None)

    def __getattribute__(self, name):  # paint
        attr = super().__getattribute__(name)
        if callable(attr):
            def wrapper(*args, **kwargs):
                result = attr(*args, **kwargs)
                self.canvas.delete("all")
                for obj in self.objects:
                    obj.paint()
                return result

            return wrapper
        return attr

    def select_objects(self, event):
        sel_objects = list(filter(lambda p: p.check_point(event), self.objects))
        sel_objects.sort(key=lambda p: p.dist_point(event))
        for obj in sel_objects:
            obj.select()
            # break

    def process_interaction(self, action, event):
        if self.lp == Point(None, None):
            self.lp = event
        else:
            for obj in self.objects:
                if action == "move":
                    obj.move(Point(event.x - self.lp.x, event.y - self.lp.y))
                elif action == "resize":
                    obj.resize(self.lp, event)
            self.lp = event

    def fill(self, color):
        for obj in self.objects:
            obj.fill(color)

    def unselect_objects(self, _):
        for obj in self.objects:
            obj.unselect()

    def select_all_objects(self, _):
        for obj in self.objects:
            obj.unselect()
            obj.select()

    def delete_objects(self, _):
        self.objects = [obj for obj in self.objects if not obj.self_destruct()]
