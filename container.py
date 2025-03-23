from figures.circle import Circle


class Container:
    def __init__(self, canvas):
        self.objects = list()
        self.canvas = canvas
        self.lp_x = None
        self.lp_y = None

    def new_circle(self, color, event):
        if (self.lp_x, self.lp_y) == (None, None):
            self.objects.append(Circle(event.x, event.y, color, self.canvas))
        else:
            self.lp_x, self.lp_y = None, None

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
        sel_objects = list(filter(lambda p: p.check_point(event.x, event.y), self.objects))
        sel_objects.sort(key=lambda p: p.dist_point(event.x, event.y))
        for obj in sel_objects:
            obj.select()
            # break

    def process_interaction(self, action, event):
        if (self.lp_x, self.lp_y) == (None, None):
            self.lp_x, self.lp_y = event.x, event.y
        else:
            for obj in self.objects:
                if action == "move":
                    obj.move(event.x - self.lp_x, event.y - self.lp_y)
                elif action == "resize":
                    obj.resize(self.lp_x, self.lp_y, event.x, event.y)
            self.lp_x, self.lp_y = event.x, event.y

    def fill(self, color):
        for obj in self.objects:
            obj.fill(color)

    def unselect_objects(self, _):
        for obj in self.objects:
            obj.unselect()

    def delete_objects(self, _):
        self.objects = [obj for obj in self.objects if not obj.self_destruct()]
