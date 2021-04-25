from Point import Point


class Line:
    def __init__(self, starting_point: Point, ending_point: Point):
        self.start = starting_point
        self.end = ending_point
        self.mark = False

    def __str__(self):
        return "Start Point: " + str(self.start) + "\nEnd Point: " + str(
            self.end) + "\nFormula: " + self.getLineCartesianFormula()

    def getLineCartesianFormula(self):
        a = (self.start.y - self.end.y) / (self.start.x - self.end.x)
        b = self.start.y - (a * self.start.x)

        return f"y = {a}x + {b}"
