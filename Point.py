class Point:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.mark = False

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "x: " + str(self.x) + " y: " + str(self.y)

    def __lt__(self, other):
        return self.y < other.y if (self.x == other.x) else self.x < other.x

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise KeyError("Point is only two dimensional.")

    def distance(self, other):
        from math import sqrt
        return sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)
