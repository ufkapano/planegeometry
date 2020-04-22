#!/usr/bin/python

from planegeometry.structures.points import Point
from planegeometry.algorithms.geomtools import orientation


class GrahamScan:
    """Graham's scan algorithm for finding the convex hull of points.
    
    https://en.wikipedia.org/wiki/Graham_scan
    """

    def __init__(self, point_list):
        """The algorithm initialization."""
        if len(point_list) < 3:
            raise ValueError("small number of points")
        self.point_list = point_list
        self.convex_hull = []   # acting as a stack

    def run(self):
        """Executable pseudocode."""
        # Find the lowest y-coordinate and leftmost point.
        p_min = min(self.point_list, key=lambda p: (p.y, p.x))

        # Sort points by polar angle with p_min, if several points have
        # the same polar angle then only keep the farthest.
        self.point_list.sort(key=lambda p:
            ((p-p_min).alpha(), (p-p_min)*(p-p_min)))

        # After sorting p_min will be at the beginning of point_list.
        for point in self.point_list:
            # Pop the last point from the stack if we turn clockwise
            # to reach this point.
            while len(self.convex_hull) > 1 and orientation(
                self.convex_hull[-2], self.convex_hull[-1], point) <= 0:
                    self.convex_hull.pop()
            self.convex_hull.append(point)

# EOF
