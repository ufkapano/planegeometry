#!/usr/bin/python

from planegeometry.structures.points import Point
from planegeometry.algorithms.geomtools import orientation


class GrahamScan1:
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


def swap(L, left, right):
    """Swap two items on a list."""
    L[left], L[right] = L[right], L[left]


class GrahamScan2:
    """Graham's scan algorithm for finding the convex hull of points."""

    def __init__(self, point_list):
        """The algorithm initialization."""
        if len(point_list) < 3:
            raise ValueError("small number of points")
        self.point_list = point_list
        self.convex_hull = None

    def run(self):
        """Executable pseudocode."""
        p_min = min(self.point_list, key=lambda p: (p.y, p.x))
        self.point_list.sort(key=lambda p:
            ((p-p_min).alpha(), (p-p_min)*(p-p_min)))
        m = 1   # index of the last point included to convex hull
        i = 2   # index of the next point to test
        while i < len(self.point_list):
            if orientation(self.point_list[m-1], 
                           self.point_list[m], 
                           self.point_list[i]) > 0: # left turn
                # self.point_list[m] outside
                m += 1
                swap(self.point_list, m, i)
                i += 1
            else:   # self.point_list[m] inside or on the edge
                if m > 1:   # do not move i, because we need to test m
                    m -= 1
                else:   # we can move i, but still m=1
                    swap(self.point_list, m, i)
                    i += 1
        self.convex_hull = self.point_list[0:m+1]

GrahamScan = GrahamScan1

# EOF
