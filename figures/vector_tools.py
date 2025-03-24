
class Point:
    def __init__(self, *args, event=None):
        if event is not None:
            self.x, self.y = event.x, event.y
        elif len(args) == 1:
            self.x = args[0]
            self.y = args[0]
        elif len(args) == 2 :
            self.x = args[0]
            self.y = args[1]
    
    def inc(self, p):
        return Point(self.x + p.x, self.y + p.y)

    def dec(self, p):
        return Point(self.x - p.x, self.y - p.y)

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False
 


def constrain(lower_limit:int, upper_limit:int, value:int) -> int:
    if value < lower_limit:
        return lower_limit
    if value > upper_limit:
        return upper_limit
    return value
