#!/usr/bin/env python3

try:
    integer_types = (int, long)
    range = xrange
except NameError:   # Python 3
    integer_types = (int,)

from planegeometry.algorithms.geomtools import oriented_area
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment

def swap(L, left, right):
    """Swap two items on a list."""
    L[left], L[right] = L[right], L[left]

class JarvisMarch:
    """Jarvis march for finding the convex hull of points.
    
    https://en.wikipedia.org/wiki/Gift_wrapping_algorithm
    
    Jarvis (1973). O(nh) time complexity (output-sensitive).
    n - the number of points in the set P,
    h - the number of points in the convex hull CH(P),
    """

    def __init__(self, point_list):
        """The algorithm initialization."""
        if len(point_list) < 3:
            raise ValueError("small number of points")
        self.point_list = point_list
        self.convex_hull = None

    def run(self):
        """Executable pseudocode."""
        p_min = min(self.point_list, key=lambda p: (p.y, p.x))   # O(n)
        if p_min != self.point_list[0]:
            idx = self.point_list.index(p_min)   # O(n)
            swap(self.point_list, 0, idx)
        m = 0   # index of the last point included to convex hull
        while True:
            i = (m + 1) % len(self.point_list)   # new candidate
            for j in range(len(self.point_list)):
                if i == j or j == m:   # the same point
                    continue
                orient = oriented_area(self.point_list[m],
                                       self.point_list[i],
                                       self.point_list[j])
                if orient < 0:
                    i = j   # new candidate to convex hull
                elif orient == 0:   # degeneracy
                    segment = Segment(self.point_list[m], self.point_list[j])
                    if self.point_list[i] in segment:
                        i = j
            if i == 0:   # doszlismy do p_min
                break
            else:
                m += 1
                swap(self.point_list, m, i)
        self.convex_hull = self.point_list[0:m+1]

# EOF
