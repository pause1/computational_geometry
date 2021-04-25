from typing import Union, List

from Point import Point


class Node:
    def __init__(self, point: Point, left=None, right=None):
        self.point: Point = point
        self.left = left
        self.right = right


class KDTree:
    def __init__(self):
        self.root: Union[Node, None] = None
        pass

    def _insert(self, root: Node, point: Point, depth: int) -> Node:
        if root is None:
            root = Node(point)
            return root

        cd: int = depth % 2

        if point[cd] < root.point[cd]:
            root.left = self._insert(root.left, point, depth + 1)
        else:
            root.right = self._insert(root.right, point, depth + 1)

        return root

    def insert(self, point: Point) -> None:
        self.root = self._insert(self.root, point, 0)

    def _includes(self, root: Node, point: Point, depth: int) -> bool:
        if root is None:
            return False
        if root.point == point:
            return True

        cd = depth % 2

        if point[cd] < root.point[cd]:
            return self._includes(root.left, point, depth + 1)
        return self._includes(root.right, point, depth + 1)

    def includes(self, point: Point) -> bool:
        return self._includes(self.root, point, 0)

    def generate(self, plist: List[Point]) -> None:
        for elem in plist:
            self.insert(elem)

    def find_nearest_neighbor(self, point: Point) -> Union[Point, None]:
        class DistancePoint:
            def __init__(self, pt: Point, distance: float):
                self.point: Point = pt
                self.distance: float = distance

        best: Union[DistancePoint, None] = None

        def search(root: Node, depth: int):
            nonlocal best
            if root is None:
                return None

            distance: float = root.point.distance(point)
            if root.point != point and (best is None or distance < best.distance):
                best = DistancePoint(root.point, distance)

            cd = depth % 2
            diff = point[cd] - root.point[cd]
            if diff <= 0:
                close, away = root.left, root.right
            else:
                close, away = root.right, root.left

            search(close, depth + 1)
            if not best or diff ** 2 < best.distance:
                search(away, depth + 1)

        search(self.root, 0)
        return best.point
