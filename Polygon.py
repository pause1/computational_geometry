from typing import List

from Point import Point


class Polygon:
    def __init__(self, points: List[Point]):
        self.points: List[Point] = points
        self.mark = False
