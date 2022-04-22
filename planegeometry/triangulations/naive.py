#!/usr/bin/python

import itertools
from planegeometry.structures.points import Point
from planegeometry.structures.triangles import Triangle
from planegeometry.structures.trianglecollections import TriangleCollection
from planegeometry.algorithms.geomtools import orientation


class DelaunayNaive:
    """Delaunay triangulation (naive algorithm) in O(n^4) time.
    
    Points have to be in general position.
    """

    def __init__(self, point_list):
        self.point_list = point_list
        self.tc = TriangleCollection()

    def run(self):
        for (p1, p2, p3) in itertools.combinations(self.point_list, 3):
            # Counterclockwise orientation of points.
            if orientation(p1, p2, p3) < 0:
                p2, p3 = p3, p2
            elif orientation(p1, p2, p3) == 0:   # collinear points
                continue
            triangle = Triangle(p1, p2, p3)
            if all(not triangle.in_circumcircle(p4) for p4 in self.point_list
                if p4 != p1 and p4 != p2 and p4 != p3):
                self.tc.insert(triangle)

# EOF
