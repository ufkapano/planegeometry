#!/usr/bin/python

try:
    integer_types = (int, long)
except NameError:   # Python 3
    integer_types = (int,)
    xrange = range

from planegeometry.structures.avltree1 import AVLTree


class ClosestPairSweepLine:
    """Solving the closest pair problem (sweep line method).
    
    https://people.scs.carleton.ca/~michiel/lecturenotes/ALGGEOM/sweepclosestpair.pdf
    O(n log n) complexity.
"""

    def __init__(self, point_list):
        """Initialize structures."""
        if len(point_list) < 2:
            raise ValueError("minimum 2 points")

        self.point_list = point_list
        self.point_list.sort(key=lambda point: point.y) # sorted along y
        self.active_points = AVLTree()   # sorted along x
        self.closest_pair = self.point_list[0], self.point_list[1]
        self.min_distance = (self.point_list[0] - self.point_list[1]).length()

    def run(self):
        """Finding the closest pair."""
        if len(self.point_list) == 2:
            return self.closest_pair
        top = 2   # index of new point
        new_point = self.point_list[top]   # new point to check
        # Initial horizontal strip, the width is self.min_distance.
        bottom = 0
        while self.point_list[bottom].y <= new_point.y - self.min_distance:
            bottom += 1
        # Inicjalizacja X-struktury.
        for i in xrange(bottom, top):
            self.active_points.insert(self.point_list[i])

        while top < len(self.point_list):
            self.active_points.insert(new_point)
            neighbors = []
            # Szukamy trzech punktow w prawo.
            point = new_point
            for _ in xrange(3):
                node = self.active_points.successor(point)
                if node:
                    point = node.value
                    neighbors.append(point)
                else:
                    break
            # Szukamy trzech punktow w lewo.
            point = new_point
            for _ in xrange(3):
                node = self.active_points.predecessor(point)
                if node:
                    point = node.value
                    neighbors.append(node.value)
                else:
                    break

            for point in neighbors:
                new_distance = (new_point - point).length()
                if new_distance < self.min_distance:
                    self.min_distance = new_distance
                    self.closest_pair = point, new_point

            if top < len(self.point_list) - 1:
                # Przygotowujemy nowy punkt do zbadania.
                new_point = self.point_list[top + 1]
                while self.point_list[bottom].y <= new_point.y - self.min_distance:
                    self.active_points.delete(self.point_list[bottom])
                    bottom += 1

            top += 1
        return self.closest_pair
