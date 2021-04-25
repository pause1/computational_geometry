from typing import List

from Line import Line
from Point import Point


class Operations:

    @staticmethod
    def get_line_cartesian_formula(line: Line, points=False):
        a = (line.start.y - line.end.y) / (line.start.x - line.end.x)
        b = line.start.y - (a * line.start.x)

        if points:
            return a, b
        return f"y = {a}x + {b}"

    @staticmethod
    def which_side(line: Line, point: Point) -> int:
        (a, b) = Operations.get_line_cartesian_formula(line, True)
        # right | left | on line
        if a * point.x - point.y + b > 0:
            return 1
        elif a * point.x - point.y + b < 0:
            return -1
        else:
            return 0

    @staticmethod
    def graham_scan(points: list):
        from functools import reduce

        def _cmp(a, b):
            return (a > b) - (a < b)

        def _turn(p, q, r):
            return _cmp((q.x - p.x) * (r.y - p.y) - (r.x - p.x) * (q.y - p.y), 0)

        def _keep_left(hull, r):
            while len(hull) > 1 and _turn(hull[-2], hull[-1], r) != 1:
                hull.pop()
            if not len(hull) or hull[-1] != r:
                hull.append(r)
            return hull

        points.sort()
        l = reduce(_keep_left, points, [])
        u = reduce(_keep_left, reversed(points), [])
        return l.extend(u[i] for i in range(1, len(u) - 1)) or l

    @staticmethod
    def _check_if_point_on_line(point: Point, line: Line) -> bool:
        from math import sqrt
        d: float = abs((line.end.x - line.start.x) * (line.start.y - point.y) - (line.start.x - point.x) * (
                line.end.y - line.start.y)) / sqrt(
            (line.end.x - line.start.x) ** 2 + (line.end.y - line.start.y) ** 2)

        if 2 > d > -2:
            return True
        return False

    @staticmethod
    def check_if_point_on_line(point: Point, line: Line) -> bool:
        if Operations._check_if_point_on_line(point, line):

            if abs(line.end.x - line.start.x) >= abs(line.end.y - line.start.y):
                if (line.end.x - line.start.x) > 0:
                    return line.start.x <= point.x <= line.end.x
                else:
                    return line.end.x <= point.x <= line.start.x
            else:
                if (line.end.y - line.start.y) > 0:
                    return line.start.y <= point.y <= line.end.y
                else:
                    return line.end.y <= point.y <= line.start.y
        else:
            return False

    @staticmethod
    def is_point_in_polygon(p: Point, poly: list, include_edges=True):
        n = len(poly)
        inside = False

        p1x, p1y = poly[0].x, poly[0].y
        for i in range(1, n + 1):
            p2x, p2y = poly[i % n].x, poly[i % n].y
            if p1y == p2y:
                if p.y == p1y:
                    if min(p1x, p2x) <= p.x <= max(p1x, p2x):
                        inside = include_edges
                        break
                    elif p.x < min(p1x, p2x):
                        inside = not inside
            else:
                if min(p1y, p2y) <= p.y <= max(p1y, p2y):
                    xinters = (p.y - p1y) * (p2x - p1x) / float(p2y - p1y) + p1x

                    if p.x == xinters:
                        inside = include_edges
                        break

                    if p.x < xinters:
                        inside = not inside

            p1x, p1y = p2x, p2y

        return inside

    @staticmethod
    def findTriangleArea(points: List[Point]) -> float:
        return abs((points[0].x * (points[1].y - points[2].y) + (points[1].x * (points[2].y - points[0].y)) +
                    (points[2].x * (points[0].y - points[1].y))) / 2.0)

    @staticmethod
    def crossingPointCartesian(l1: Line, l2: Line) -> Point:
        def det(a, b):
            if isinstance(a, Point) and isinstance(b, Point):
                return a.x * b.y - a.y * b.x
            elif isinstance(a, tuple) and isinstance(b, tuple):
                return a[0] * b[1] - a[1] * b[0]
            else:
                raise ValueError("inconsistent data provided to determinant calc")

        xdiff = (l1.start.x - l1.end.x, l2.start.x - l2.end.x)
        ydiff = (l1.start.y - l1.end.y, l2.start.y - l2.end.y)

        div = det(xdiff, ydiff)

        d = (det(l1.start, l1.end), det(l2.start, l2.end))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return Point(x, y)

    @staticmethod
    def rotateLine(angle: int, head: Point, tail: Point, point: Point):
        from math import radians, cos, sin

        def _rotator(pt, x, y):
            tx, ty = pt.x - x, pt.y - y
            px = (tx * cos(angle) + ty * sin(angle)) + x
            py = (-tx * sin(angle) + ty * cos(angle)) + y
            return px, py

        angle = radians(angle)

        p1x, p1y = _rotator(head, point.x, point.y)
        p2x, p2y = _rotator(tail, point.x, point.y)

        return Line(Point(p1x, p1y), Point(p2x, p2y))
